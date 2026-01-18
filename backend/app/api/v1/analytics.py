"""
Analytics and progress tracking API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from typing import List, Optional
from datetime import datetime, timedelta

from app.database import get_db
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement, UserStats, ProgressSnapshot
from app.schemas.analytics import (
    OverallProgressResponse, ErrorPatternAnalysisResponse, ProgressSnapshotResponse,
    CreateSnapshotRequest, AchievementResponse, UserAchievementResponse,
    AchievementProgressResponse, ShowcaseAchievementRequest, UserStatsResponse,
    ProgressComparisonResponse, LeaderboardResponse, LeaderboardEntry,
    ActivityHeatmapResponse, HeatmapCell, GrammarHeatmapResponse, GrammarTopicHeatmap,
    WeeklyReport, MonthlyReport, PersonalizedRecommendationsResponse, StudyRecommendation
)
from app.services.analytics_service import AnalyticsService
from app.api.deps import get_current_user

router = APIRouter()


# ========== HELPER FUNCTIONS ==========

def json_serialize_datetimes(obj):
    """Convert datetime objects to ISO format strings for JSON serialization."""
    if isinstance(obj, dict):
        return {key: json_serialize_datetimes(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [json_serialize_datetimes(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return obj


# ========== OVERALL PROGRESS ENDPOINTS ==========

@router.get("/v1/analytics/progress", response_model=OverallProgressResponse)
def get_overall_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get comprehensive progress across all modules."""
    analytics = AnalyticsService(db)
    progress = analytics.get_overall_progress(current_user.id)
    return progress


@router.get("/v1/analytics/progress/comparison", response_model=ProgressComparisonResponse)
def get_progress_comparison(
    period_days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Compare progress between current and previous period."""
    analytics = AnalyticsService(db)
    comparison = analytics.get_progress_comparison(current_user.id, period_days)
    return comparison


# ========== ERROR PATTERN ANALYSIS ENDPOINTS ==========

@router.get("/v1/analytics/errors", response_model=ErrorPatternAnalysisResponse)
def analyze_error_patterns(
    days: int = Query(30, ge=7, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze common error patterns across grammar and conversation."""
    analytics = AnalyticsService(db)
    error_analysis = analytics.analyze_error_patterns(current_user.id, days)
    return error_analysis


# ========== PROGRESS SNAPSHOT ENDPOINTS ==========

@router.post("/v1/analytics/snapshots", response_model=ProgressSnapshotResponse)
def create_progress_snapshot(
    request: CreateSnapshotRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a point-in-time snapshot of user progress."""
    analytics = AnalyticsService(db)
    snapshot_data = analytics.create_progress_snapshot(current_user.id)

    # Save to database (convert datetime objects to ISO strings for JSON serialization)
    snapshot = ProgressSnapshot(
        user_id=current_user.id,
        snapshot_type=request.snapshot_type,
        overall_progress=json_serialize_datetimes(snapshot_data["overall_progress"]),
        error_analysis=json_serialize_datetimes(snapshot_data["error_analysis"]),
        overall_score=snapshot_data["overall_progress"]["overall_score"],
        total_sessions=(
            snapshot_data["overall_progress"]["conversation"]["total_sessions"] +
            snapshot_data["overall_progress"]["grammar"].get("topics_practiced", 0)
        )
    )

    db.add(snapshot)
    db.commit()
    db.refresh(snapshot)

    return snapshot_data


@router.get("/v1/analytics/snapshots", response_model=List[ProgressSnapshotResponse])
def get_progress_snapshots(
    limit: int = Query(10, ge=1, le=50),
    snapshot_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get historical progress snapshots."""
    query = db.query(ProgressSnapshot).filter(
        ProgressSnapshot.user_id == current_user.id
    )

    if snapshot_type:
        query = query.filter(ProgressSnapshot.snapshot_type == snapshot_type)

    snapshots = query.order_by(desc(ProgressSnapshot.snapshot_date)).limit(limit).all()

    # Format snapshots
    results = []
    for snapshot in snapshots:
        results.append({
            "snapshot_date": snapshot.snapshot_date,
            "user_id": snapshot.user_id,
            "overall_progress": snapshot.overall_progress,
            "error_analysis": snapshot.error_analysis,
            "milestones_achieved": [],
            "next_goals": []
        })

    return results


# ========== ACHIEVEMENT ENDPOINTS ==========

@router.get("/v1/analytics/achievements", response_model=List[AchievementResponse])
def get_all_achievements(
    category: Optional[str] = None,
    tier: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all available achievements."""
    query = db.query(Achievement).filter(Achievement.is_active == True)

    if category:
        query = query.filter(Achievement.category == category)
    if tier:
        query = query.filter(Achievement.tier == tier)

    achievements = query.all()
    return achievements


@router.get("/v1/analytics/achievements/earned", response_model=List[UserAchievementResponse])
def get_user_achievements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's earned achievements."""
    user_achievements = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id,
        UserAchievement.is_completed == True
    ).all()

    return user_achievements


@router.get("/v1/analytics/achievements/progress", response_model=List[AchievementProgressResponse])
def get_achievement_progress(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get progress toward all achievements."""
    analytics = AnalyticsService(db)
    overall_progress = analytics.get_overall_progress(current_user.id)

    all_achievements = db.query(Achievement).filter(Achievement.is_active == True).all()
    progress_list = []

    for achievement in all_achievements:
        # Calculate current progress based on criteria type
        current_progress = _calculate_achievement_progress(
            achievement, overall_progress, current_user.id, db
        )

        # Check if earned
        user_achievement = db.query(UserAchievement).filter(
            UserAchievement.user_id == current_user.id,
            UserAchievement.achievement_id == achievement.id
        ).first()

        is_completed = user_achievement.is_completed if user_achievement else False
        earned_at = user_achievement.earned_at if (user_achievement and user_achievement.is_completed) else None

        progress_percentage = min(100, int((current_progress / achievement.criteria_value) * 100))

        progress_list.append({
            "achievement": achievement,
            "current_progress": current_progress,
            "target_value": achievement.criteria_value,
            "progress_percentage": progress_percentage,
            "is_completed": is_completed,
            "earned_at": earned_at
        })

    return progress_list


@router.post("/v1/analytics/achievements/{achievement_id}/showcase")
def showcase_achievement(
    achievement_id: int,
    request: ShowcaseAchievementRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle achievement showcase status."""
    user_achievement = db.query(UserAchievement).filter(
        UserAchievement.user_id == current_user.id,
        UserAchievement.achievement_id == achievement_id,
        UserAchievement.is_completed == True
    ).first()

    if not user_achievement:
        raise HTTPException(status_code=404, detail="Achievement not earned")

    user_achievement.is_showcased = request.is_showcased
    db.commit()

    return {"message": "Showcase status updated"}


# ========== USER STATS ENDPOINTS ==========

@router.get("/v1/analytics/stats", response_model=UserStatsResponse)
def get_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get aggregate user statistics."""
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()

    if not stats:
        # Create initial stats
        stats = UserStats(user_id=current_user.id)
        db.add(stats)
        db.commit()
        db.refresh(stats)

    return stats


@router.post("/v1/analytics/stats/refresh")
def refresh_user_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Manually refresh user statistics."""
    analytics = AnalyticsService(db)
    overall_progress = analytics.get_overall_progress(current_user.id)

    # Update or create stats
    stats = db.query(UserStats).filter(UserStats.user_id == current_user.id).first()

    if not stats:
        stats = UserStats(user_id=current_user.id)
        db.add(stats)

    # Update from progress data
    stats.total_sessions = (
        overall_progress["conversation"]["total_sessions"] +
        overall_progress["grammar"]["total_sessions"]
    )
    stats.current_streak_days = overall_progress["activity"]["current_streak_days"]
    stats.longest_streak_days = overall_progress["activity"]["longest_streak_days"]

    stats.conversation_sessions = overall_progress["conversation"]["total_sessions"]
    stats.total_messages_sent = overall_progress["conversation"]["total_messages"]

    stats.grammar_sessions = overall_progress["grammar"]["total_sessions"]
    stats.grammar_exercises_completed = overall_progress["grammar"]["total_exercises_attempted"]
    stats.grammar_topics_mastered = overall_progress["grammar"]["topics_mastered"]
    stats.average_grammar_accuracy = int(overall_progress["grammar"]["overall_accuracy_percentage"])

    stats.vocabulary_words_learned = overall_progress["vocabulary"]["total_words_learned"]
    stats.vocabulary_words_mastered = overall_progress["vocabulary"]["words_mastered"]
    stats.vocabulary_reviews_completed = overall_progress["vocabulary"]["total_reviews"]
    stats.average_vocabulary_accuracy = int(overall_progress["vocabulary"]["overall_accuracy_percentage"])

    stats.last_activity_date = datetime.utcnow()
    stats.updated_at = datetime.utcnow()

    db.commit()

    return {"message": "Stats refreshed successfully"}


# ========== LEADERBOARD ENDPOINTS ==========

@router.get("/v1/analytics/leaderboard/{leaderboard_type}", response_model=LeaderboardResponse)
def get_leaderboard(
    leaderboard_type: str,
    period: str = Query("all_time", pattern="^(all_time|monthly|weekly)$"),
    limit: int = Query(100, ge=10, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get leaderboard rankings."""
    # Determine metric column
    metric_map = {
        "overall": UserStats.total_sessions,
        "grammar": UserStats.grammar_topics_mastered,
        "vocabulary": UserStats.vocabulary_words_learned,
        "streak": UserStats.current_streak_days
    }

    if leaderboard_type not in metric_map:
        raise HTTPException(status_code=400, detail="Invalid leaderboard type")

    metric_column = metric_map[leaderboard_type]

    # Get top users
    top_users = db.query(User, UserStats).join(
        UserStats, User.id == UserStats.user_id
    ).order_by(desc(metric_column)).limit(limit).all()

    entries = []
    user_rank = None
    user_entry = None

    for rank, (user, stats) in enumerate(top_users, start=1):
        metric_value = getattr(stats, metric_column.key)

        entry = LeaderboardEntry(
            rank=rank,
            user_id=user.id,
            username=user.username,
            score=stats.total_achievement_points,
            metric_value=metric_value
        )

        entries.append(entry)

        if user.id == current_user.id:
            user_rank = rank
            user_entry = entry

    # If user not in top, find their rank
    if user_rank is None:
        all_users = db.query(UserStats).order_by(desc(metric_column)).all()
        for rank, stats in enumerate(all_users, start=1):
            if stats.user_id == current_user.id:
                user_rank = rank
                user_entry = LeaderboardEntry(
                    rank=rank,
                    user_id=current_user.id,
                    username=current_user.username,
                    score=stats.total_achievement_points,
                    metric_value=getattr(stats, metric_column.key)
                )
                break

    total_users = db.query(UserStats).count()

    return {
        "leaderboard_type": leaderboard_type,
        "period": period,
        "entries": entries,
        "user_rank": user_rank,
        "user_entry": user_entry,
        "total_users": total_users
    }


# ========== HEATMAP ENDPOINTS ==========

@router.get("/v1/analytics/heatmap/activity", response_model=ActivityHeatmapResponse)
def get_activity_heatmap(
    days: int = Query(365, ge=30, le=730),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get activity heatmap for calendar display."""
    analytics = AnalyticsService(db)

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    # Get overall progress to access activity
    overall_progress = analytics.get_overall_progress(current_user.id)

    # Build heatmap cells
    from app.models.session import Session as ConversationSession
    from app.models.grammar import GrammarSession
    from app.models.vocabulary import VocabularyReview

    cells = []
    active_days = 0

    current_date = start_date
    while current_date <= end_date:
        # Count sessions on this date
        day_start = datetime.combine(current_date, datetime.min.time())
        day_end = datetime.combine(current_date, datetime.max.time())

        conv_count = db.query(ConversationSession).filter(
            ConversationSession.user_id == current_user.id,
            ConversationSession.started_at >= day_start,
            ConversationSession.started_at <= day_end
        ).count()

        grammar_count = db.query(GrammarSession).filter(
            GrammarSession.user_id == current_user.id,
            GrammarSession.started_at >= day_start,
            GrammarSession.started_at <= day_end
        ).count()

        vocab_count = db.query(VocabularyReview).filter(
            VocabularyReview.user_id == current_user.id,
            VocabularyReview.reviewed_at >= day_start,
            VocabularyReview.reviewed_at <= day_end
        ).count()

        total_activity = conv_count + grammar_count + vocab_count

        # Determine intensity level (0-4)
        if total_activity == 0:
            level = 0
        elif total_activity <= 2:
            level = 1
        elif total_activity <= 5:
            level = 2
        elif total_activity <= 10:
            level = 3
        else:
            level = 4

        if total_activity > 0:
            active_days += 1

        cells.append({
            "date": current_date.isoformat(),
            "value": total_activity,
            "level": level
        })

        current_date += timedelta(days=1)

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "cells": cells,
        "total_days": days,
        "active_days": active_days
    }


@router.get("/v1/analytics/heatmap/grammar", response_model=GrammarHeatmapResponse)
def get_grammar_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get grammar topic mastery heatmap."""
    from app.models.grammar import UserGrammarProgress, GrammarTopic

    progress_records = db.query(UserGrammarProgress, GrammarTopic).join(
        GrammarTopic
    ).filter(
        UserGrammarProgress.user_id == current_user.id
    ).all()

    topics = []
    categories = set()
    total_mastery = 0

    for progress, topic in progress_records:
        # Determine color intensity (0-4)
        mastery = progress.mastery_level
        if mastery < 1.0:
            intensity = 0
        elif mastery < 2.0:
            intensity = 1
        elif mastery < 3.0:
            intensity = 2
        elif mastery < 4.0:
            intensity = 3
        else:
            intensity = 4

        topics.append({
            "topic_id": topic.id,
            "topic_name": topic.name_de,
            "category": topic.category,
            "mastery_level": mastery,
            "last_practiced": progress.last_practiced,
            "color_intensity": intensity
        })

        categories.add(topic.category)
        total_mastery += mastery

    overall_mastery = total_mastery / len(topics) if topics else 0

    return {
        "topics": topics,
        "categories": sorted(list(categories)),
        "overall_mastery": round(overall_mastery, 2)
    }


# ========== HELPER FUNCTIONS ==========

def _calculate_achievement_progress(
    achievement: Achievement,
    overall_progress: dict,
    user_id: int,
    db: Session
) -> int:
    """Calculate current progress toward an achievement."""
    criteria_type = achievement.criteria_type

    if criteria_type == "sessions_count":
        return overall_progress["conversation"]["total_sessions"] + overall_progress["grammar"]["total_sessions"]
    elif criteria_type == "words_learned":
        return overall_progress["vocabulary"]["total_words_learned"]
    elif criteria_type == "words_mastered":
        return overall_progress["vocabulary"]["words_mastered"]
    elif criteria_type == "streak_days":
        return overall_progress["activity"]["current_streak_days"]
    elif criteria_type == "topics_mastered":
        return overall_progress["grammar"]["topics_mastered"]
    elif criteria_type == "conversation_sessions":
        return overall_progress["conversation"]["total_sessions"]
    elif criteria_type == "grammar_accuracy":
        return int(overall_progress["grammar"]["overall_accuracy_percentage"])
    elif criteria_type == "vocabulary_accuracy":
        return int(overall_progress["vocabulary"]["overall_accuracy_percentage"])
    else:
        return 0
