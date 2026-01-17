"""
Grammar learning endpoints for practice sessions, exercises, and progress tracking.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime, timedelta
import random

from app.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.grammar import (
    GrammarTopic,
    GrammarExercise,
    UserGrammarProgress,
    GrammarSession,
    GrammarExerciseAttempt,
    DiagnosticTest
)
from app.schemas.grammar import (
    GrammarTopicResponse,
    GrammarTopicWithStats,
    GrammarExerciseResponse,
    StartGrammarPracticeRequest,
    GrammarPracticeSessionResponse,
    SubmitExerciseAnswerRequest,
    SubmitExerciseAnswerResponse,
    ExerciseFeedback,
    StartDiagnosticTestRequest,
    DiagnosticTestResponse,
    DiagnosticTestResults,
    GrammarProgressSummary,
    TopicProgressDetail,
    WeakAreasResponse,
    GenerateExercisesRequest,
    GenerateExercisesResponse,
    ReviewQueueResponse,
    ReviewQueueItem
)
from app.services.grammar_ai_service import GrammarAIService

router = APIRouter(prefix="/grammar", tags=["grammar"])


# ========== TOPIC ENDPOINTS ==========

@router.get("/topics", response_model=List[GrammarTopicResponse])
def list_grammar_topics(
    category: str | None = None,
    difficulty: str | None = None,
    db: Session = Depends(get_db)
):
    """List all grammar topics with optional filtering."""
    query = db.query(GrammarTopic)

    if category:
        query = query.filter(GrammarTopic.category == category)
    if difficulty:
        query = query.filter(GrammarTopic.difficulty_level == difficulty)

    topics = query.order_by(GrammarTopic.order_index).all()
    return topics


@router.get("/topics/{topic_id}", response_model=GrammarTopicWithStats)
def get_grammar_topic(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific grammar topic with user's progress stats."""
    topic = db.query(GrammarTopic).filter(GrammarTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Get user's progress on this topic
    progress = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id,
        UserGrammarProgress.topic_id == topic_id
    ).first()

    # Calculate stats
    if progress:
        total = progress.total_attempts
        correct = progress.correct_attempts
        accuracy = (correct / total * 100) if total > 0 else 0
        return GrammarTopicWithStats(
            **topic.__dict__,
            user_accuracy=accuracy,
            total_attempts=total,
            last_practiced=progress.last_practiced_at
        )
    else:
        return GrammarTopicWithStats(
            **topic.__dict__,
            user_accuracy=None,
            total_attempts=0,
            last_practiced=None
        )


@router.get("/topics/{topic_id}/exercises", response_model=List[GrammarExerciseResponse])
def get_topic_exercises(
    topic_id: int,
    exercise_type: str | None = None,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get exercises for a specific topic."""
    query = db.query(GrammarExercise).filter(GrammarExercise.topic_id == topic_id)

    if exercise_type:
        query = query.filter(GrammarExercise.exercise_type == exercise_type)

    exercises = query.limit(limit).all()
    return exercises


# ========== PRACTICE SESSION ENDPOINTS ==========

@router.post("/practice/start", response_model=GrammarPracticeSessionResponse)
def start_grammar_practice(
    request: StartGrammarPracticeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Start a new grammar practice session."""
    # Build query for exercises
    query = db.query(GrammarExercise)

    # Filter by topics
    if request.topic_ids:
        query = query.filter(GrammarExercise.topic_id.in_(request.topic_ids))

    # Filter by difficulty
    if request.difficulty_level:
        query = query.filter(GrammarExercise.difficulty_level == request.difficulty_level)

    # Filter by exercise types
    if request.exercise_types:
        query = query.filter(GrammarExercise.exercise_type.in_(request.exercise_types))

    # Filter by context
    if request.context_category:
        query = query.filter(GrammarExercise.context_category == request.context_category)

    # Get exercises
    all_exercises = query.all()

    if not all_exercises:
        raise HTTPException(
            status_code=404,
            detail="No exercises found matching the criteria"
        )

    # Use spaced repetition if enabled
    if request.use_spaced_repetition:
        # Prioritize topics that need review
        # (This is a simplified version - full implementation would be more sophisticated)
        progress_records = db.query(UserGrammarProgress).filter(
            UserGrammarProgress.user_id == current_user.id,
            UserGrammarProgress.next_review_date <= datetime.utcnow()
        ).all()

        priority_topic_ids = [p.topic_id for p in progress_records]
        priority_exercises = [ex for ex in all_exercises if ex.topic_id in priority_topic_ids]

        if priority_exercises:
            # Mix 70% priority, 30% random
            num_priority = int(request.exercise_count * 0.7)
            num_random = request.exercise_count - num_priority

            selected = random.sample(
                priority_exercises,
                min(num_priority, len(priority_exercises))
            )
            remaining_needed = request.exercise_count - len(selected)
            if remaining_needed > 0:
                other_exercises = [ex for ex in all_exercises if ex not in selected]
                selected += random.sample(
                    other_exercises,
                    min(remaining_needed, len(other_exercises))
                )
        else:
            # No priority exercises, just random selection
            selected = random.sample(
                all_exercises,
                min(request.exercise_count, len(all_exercises))
            )
    else:
        # Random selection
        selected = random.sample(
            all_exercises,
            min(request.exercise_count, len(all_exercises))
        )

    # Create session
    session = GrammarSession(
        user_id=current_user.id,
        session_type="practice",
        target_level=request.difficulty_level or current_user.proficiency_level,
        total_exercises=len(selected)
    )
    db.add(session)
    db.commit()
    db.refresh(session)

    # Store exercise IDs in session (simplified - in production, use a session table)
    # For now, we'll just return the session info and client will fetch exercises

    # Get unique topics
    unique_topics = list(set([ex.topic_id for ex in selected]))
    topic_names = db.query(GrammarTopic.name_de).filter(
        GrammarTopic.id.in_(unique_topics)
    ).all()

    return GrammarPracticeSessionResponse(
        session_id=session.id,
        total_exercises=len(selected),
        current_exercise_number=1,
        estimated_duration_minutes=len(selected) * 2,  # Estimate 2 min per exercise
        topics_included=[t[0] for t in topic_names]
    )


@router.post("/practice/{session_id}/answer", response_model=SubmitExerciseAnswerResponse)
def submit_exercise_answer(
    session_id: int,
    request: SubmitExerciseAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Submit an answer to an exercise in a practice session."""
    # Get session
    session = db.query(GrammarSession).filter(
        GrammarSession.id == session_id,
        GrammarSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.ended_at:
        raise HTTPException(status_code=400, detail="Session already ended")

    # Get exercise
    exercise = db.query(GrammarExercise).filter(
        GrammarExercise.id == request.exercise_id
    ).first()

    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Use AI service to evaluate answer
    ai_service = GrammarAIService()
    topic = db.query(GrammarTopic).filter(GrammarTopic.id == exercise.topic_id).first()

    evaluation = ai_service.evaluate_answer(
        question_text=exercise.question_text,
        user_answer=request.user_answer,
        correct_answer=exercise.correct_answer,
        topic_name=topic.name_de if topic else "Grammar",
        difficulty_level=exercise.difficulty_level
    )

    # Determine points (1-3 based on difficulty and correctness)
    points = 0
    if evaluation["is_correct"]:
        difficulty_points = {"A1": 1, "A2": 1, "B1": 2, "B2": 2, "C1": 3, "C2": 3}
        points = difficulty_points.get(exercise.difficulty_level, 1)
    elif evaluation.get("is_partially_correct"):
        points = 1

    # Record attempt
    attempt = GrammarExerciseAttempt(
        session_id=session_id,
        exercise_id=request.exercise_id,
        user_answer=request.user_answer,
        is_correct=evaluation["is_correct"],
        time_spent_seconds=request.time_spent_seconds,
        points_earned=points
    )
    db.add(attempt)

    # Update session stats
    session.total_correct += 1 if evaluation["is_correct"] else 0
    session.total_attempted += 1

    # Update user progress on topic
    progress = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id,
        UserGrammarProgress.topic_id == exercise.topic_id
    ).first()

    if not progress:
        progress = UserGrammarProgress(
            user_id=current_user.id,
            topic_id=exercise.topic_id,
            mastery_level="beginner"
        )
        db.add(progress)

    progress.total_attempts += 1
    progress.correct_attempts += 1 if evaluation["is_correct"] else 0
    progress.last_practiced_at = datetime.utcnow()

    # Update next review date (spaced repetition)
    if evaluation["is_correct"]:
        # Increase interval if correct
        progress.consecutive_correct += 1
        days_interval = min(30, 2 ** progress.consecutive_correct)  # Exponential backoff, max 30 days
    else:
        # Reset interval if incorrect
        progress.consecutive_correct = 0
        days_interval = 1

    progress.next_review_date = datetime.utcnow() + timedelta(days=days_interval)

    # Update mastery level
    if progress.total_attempts >= 5:
        accuracy = progress.correct_attempts / progress.total_attempts
        if accuracy >= 0.9:
            progress.mastery_level = "mastered"
        elif accuracy >= 0.75:
            progress.mastery_level = "advanced"
        elif accuracy >= 0.5:
            progress.mastery_level = "intermediate"
        else:
            progress.mastery_level = "beginner"

    db.commit()

    # Prepare feedback
    feedback = ExerciseFeedback(
        is_correct=evaluation["is_correct"],
        is_partially_correct=evaluation.get("is_partially_correct", False),
        correct_answer=exercise.correct_answer,
        user_answer=request.user_answer,
        feedback_de=evaluation["feedback_de"],
        specific_errors=evaluation.get("specific_errors", []),
        suggestions=evaluation.get("suggestions", []),
        points_earned=points
    )

    # Session progress
    session_progress = {
        "completed": session.total_attempted,
        "total": session.total_exercises,
        "correct": session.total_correct,
        "accuracy": (session.total_correct / session.total_attempted * 100)
        if session.total_attempted > 0 else 0
    }

    # Get next exercise (if any)
    next_exercise = None
    if session.total_attempted < session.total_exercises:
        # In production, this would get the next exercise from the session's exercise list
        pass

    return SubmitExerciseAnswerResponse(
        feedback=feedback,
        session_progress=session_progress,
        next_exercise=next_exercise
    )


@router.post("/practice/{session_id}/end")
def end_grammar_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """End a grammar practice session."""
    session = db.query(GrammarSession).filter(
        GrammarSession.id == session_id,
        GrammarSession.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.ended_at:
        raise HTTPException(status_code=400, detail="Session already ended")

    session.ended_at = datetime.utcnow()

    # Calculate score
    if session.total_attempted > 0:
        session.overall_score = (session.total_correct / session.total_attempted) * 100
    else:
        session.overall_score = 0

    db.commit()

    duration = (session.ended_at - session.started_at).total_seconds() / 60

    return {
        "session_id": session_id,
        "summary": {
            "total_exercises": session.total_exercises,
            "completed": session.total_attempted,
            "correct": session.total_correct,
            "accuracy": session.overall_score,
            "duration_minutes": round(duration, 1)
        }
    }


# ========== PROGRESS TRACKING ENDPOINTS ==========

@router.get("/progress/summary", response_model=GrammarProgressSummary)
def get_grammar_progress_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get overall grammar learning progress summary."""
    # Get all user's sessions
    sessions = db.query(GrammarSession).filter(
        GrammarSession.user_id == current_user.id
    ).all()

    total_exercises = sum(s.total_attempted for s in sessions)
    total_correct = sum(s.total_correct for s in sessions)
    total_time = sum(
        (s.ended_at - s.started_at).total_seconds() / 60
        for s in sessions if s.ended_at
    )

    # Get topic progress
    progress_records = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id
    ).all()

    topics_mastered = sum(1 for p in progress_records if p.mastery_level == "mastered")
    topics_in_progress = sum(1 for p in progress_records if p.mastery_level in ["beginner", "intermediate", "advanced"])

    total_topics = db.query(GrammarTopic).count()
    topics_not_started = total_topics - len(progress_records)

    # Calculate current streak
    recent_sessions = sorted(sessions, key=lambda x: x.started_at, reverse=True)
    streak_days = 0
    if recent_sessions:
        last_date = recent_sessions[0].started_at.date()
        current_date = datetime.utcnow().date()

        if last_date == current_date or last_date == current_date - timedelta(days=1):
            streak_days = 1
            for i in range(1, len(recent_sessions)):
                prev_date = recent_sessions[i].started_at.date()
                if (last_date - prev_date).days == 1:
                    streak_days += 1
                    last_date = prev_date
                else:
                    break

    # Recent activity
    recent_activity = [
        {
            "date": s.started_at.isoformat(),
            "exercises_completed": s.total_attempted,
            "accuracy": (s.total_correct / s.total_attempted * 100) if s.total_attempted > 0 else 0
        }
        for s in recent_sessions[:7]
    ]

    # Progress by level
    level_progress = {}
    for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
        level_progress[level] = {
            "attempted": sum(
                1 for p in progress_records
                if db.query(GrammarTopic).filter(
                    GrammarTopic.id == p.topic_id,
                    GrammarTopic.difficulty_level == level
                ).first()
            ),
            "mastered": sum(
                1 for p in progress_records
                if p.mastery_level == "mastered" and db.query(GrammarTopic).filter(
                    GrammarTopic.id == p.topic_id,
                    GrammarTopic.difficulty_level == level
                ).first()
            )
        }

    return GrammarProgressSummary(
        total_exercises_completed=total_exercises,
        total_practice_time_minutes=int(total_time),
        overall_accuracy=(total_correct / total_exercises * 100) if total_exercises > 0 else 0,
        current_streak_days=streak_days,
        topics_mastered=topics_mastered,
        topics_in_progress=topics_in_progress,
        topics_not_started=topics_not_started,
        level_progress=level_progress,
        recent_activity=recent_activity
    )


@router.get("/progress/topics/{topic_id}", response_model=TopicProgressDetail)
def get_topic_progress_detail(
    topic_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get detailed progress for a specific topic."""
    topic = db.query(GrammarTopic).filter(GrammarTopic.id == topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    progress = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id,
        UserGrammarProgress.topic_id == topic_id
    ).first()

    exercises_available = db.query(GrammarExercise).filter(
        GrammarExercise.topic_id == topic_id
    ).count()

    if not progress:
        return TopicProgressDetail(
            topic=topic,
            total_attempts=0,
            correct_attempts=0,
            accuracy=0,
            mastery_level="not_started",
            last_practiced=None,
            next_review_due=None,
            exercises_available=exercises_available,
            exercises_completed=0
        )

    accuracy = (progress.correct_attempts / progress.total_attempts * 100) if progress.total_attempts > 0 else 0

    # Count unique exercises attempted
    exercises_completed = db.query(GrammarExerciseAttempt).join(GrammarSession).filter(
        GrammarSession.user_id == current_user.id,
        GrammarExerciseAttempt.exercise_id.in_(
            db.query(GrammarExercise.id).filter(GrammarExercise.topic_id == topic_id)
        )
    ).distinct(GrammarExerciseAttempt.exercise_id).count()

    return TopicProgressDetail(
        topic=topic,
        total_attempts=progress.total_attempts,
        correct_attempts=progress.correct_attempts,
        accuracy=accuracy,
        mastery_level=progress.mastery_level,
        last_practiced=progress.last_practiced_at,
        next_review_due=progress.next_review_date,
        exercises_available=exercises_available,
        exercises_completed=exercises_completed
    )


@router.get("/progress/weak-areas", response_model=WeakAreasResponse)
def get_weak_areas(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get user's weak areas and personalized recommendations."""
    # Get topics with low accuracy
    progress_records = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id,
        UserGrammarProgress.total_attempts >= 3  # Only consider topics with enough attempts
    ).all()

    weak_topics = []
    for progress in progress_records:
        accuracy = (progress.correct_attempts / progress.total_attempts * 100) if progress.total_attempts > 0 else 0
        if accuracy < 70:  # Less than 70% accuracy
            topic = db.query(GrammarTopic).filter(GrammarTopic.id == progress.topic_id).first()
            if topic:
                weak_topics.append(TopicProgressDetail(
                    topic=topic,
                    total_attempts=progress.total_attempts,
                    correct_attempts=progress.correct_attempts,
                    accuracy=accuracy,
                    mastery_level=progress.mastery_level,
                    last_practiced=progress.last_practiced_at,
                    next_review_due=progress.next_review_date,
                    exercises_available=db.query(GrammarExercise).filter(
                        GrammarExercise.topic_id == topic.id
                    ).count(),
                    exercises_completed=0
                ))

    # Sort by accuracy (lowest first)
    weak_topics.sort(key=lambda x: x.accuracy)

    # Create practice plan
    practice_plan = []
    for i, topic_detail in enumerate(weak_topics[:5]):  # Top 5 weak areas
        practice_plan.append({
            "priority": i + 1,
            "topic_id": topic_detail.topic.id,
            "topic_name": topic_detail.topic.name_de,
            "recommended_exercises": 10,
            "estimated_time_minutes": 20,
            "reason": f"Aktuelle Genauigkeit: {topic_detail.accuracy:.1f}%"
        })

    # Estimate time to improvement
    total_exercises_needed = sum(p["recommended_exercises"] for p in practice_plan)
    estimated_days = (total_exercises_needed // 10) + 1  # Assuming 10 exercises per day

    return WeakAreasResponse(
        weak_topics=weak_topics[:10],
        recommended_practice_plan=practice_plan,
        estimated_time_to_improve=estimated_days
    )


@router.get("/progress/review-queue", response_model=ReviewQueueResponse)
def get_review_queue(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get spaced repetition review queue."""
    now = datetime.utcnow()

    # Get all user progress
    progress_records = db.query(UserGrammarProgress).filter(
        UserGrammarProgress.user_id == current_user.id
    ).all()

    overdue_items = []
    due_today_items = []
    upcoming_items = []

    for progress in progress_records:
        if not progress.next_review_date:
            continue

        topic = db.query(GrammarTopic).filter(GrammarTopic.id == progress.topic_id).first()
        if not topic:
            continue

        days_diff = (progress.next_review_date.date() - now.date()).days

        # Calculate priority (1-5, higher = more urgent)
        if days_diff < 0:
            priority = min(5, abs(days_diff) + 3)
        elif days_diff == 0:
            priority = 3
        else:
            priority = max(1, 3 - days_diff)

        item = ReviewQueueItem(
            topic_id=topic.id,
            topic_name=topic.name_de,
            due_date=progress.next_review_date,
            priority=priority,
            days_overdue=abs(days_diff) if days_diff < 0 else 0
        )

        if days_diff < 0:
            overdue_items.append(item)
        elif days_diff == 0:
            due_today_items.append(item)
        elif days_diff <= 7:
            upcoming_items.append(item)

    # Sort by priority
    overdue_items.sort(key=lambda x: x.priority, reverse=True)
    due_today_items.sort(key=lambda x: x.priority, reverse=True)
    upcoming_items.sort(key=lambda x: x.due_date)

    return ReviewQueueResponse(
        overdue_count=len(overdue_items),
        due_today_count=len(due_today_items),
        upcoming_count=len(upcoming_items),
        overdue_items=overdue_items,
        due_today_items=due_today_items,
        upcoming_items=upcoming_items[:10]
    )


# ========== AI GENERATION ENDPOINTS ==========

@router.post("/generate/exercises", response_model=GenerateExercisesResponse)
def generate_exercises_ai(
    request: GenerateExercisesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Generate new exercises using AI for a specific topic."""
    topic = db.query(GrammarTopic).filter(GrammarTopic.id == request.topic_id).first()
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    ai_service = GrammarAIService()

    # Generate exercises
    generated_exercises = ai_service.generate_exercises(
        topic_name=topic.name_de,
        topic_explanation=topic.explanation_de,
        difficulty_level=topic.difficulty_level,
        exercise_type=request.exercise_type,
        count=request.count,
        context_category=request.context_category
    )

    if not generated_exercises:
        raise HTTPException(status_code=500, detail="Failed to generate exercises")

    # Save to database
    saved_exercises = []
    for ex_data in generated_exercises:
        exercise = GrammarExercise(
            topic_id=request.topic_id,
            exercise_type=ex_data["exercise_type"],
            difficulty_level=ex_data["difficulty_level"],
            question_text=ex_data["question_text"],
            correct_answer=ex_data["correct_answer"],
            alternative_answers=ex_data.get("alternative_answers", []),
            explanation_de=ex_data["explanation_de"],
            hints=ex_data.get("hints", []),
            context_category=ex_data["context_category"]
        )
        db.add(exercise)
        saved_exercises.append(exercise)

    db.commit()

    for ex in saved_exercises:
        db.refresh(ex)

    return GenerateExercisesResponse(
        generated_count=len(saved_exercises),
        exercises=saved_exercises
    )
