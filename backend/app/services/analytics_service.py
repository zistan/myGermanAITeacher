"""
Analytics Service - comprehensive progress tracking and analysis.
Tracks user progress across conversation, grammar, and vocabulary modules.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_, desc, distinct
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from app.models.user import User
from app.models.session import Session as ConversationSession, ConversationTurn
from app.models.grammar import (
    GrammarTopic, UserGrammarProgress, GrammarSession,
    GrammarExerciseAttempt, DiagnosticTest
)
from app.models.vocabulary import (
    Vocabulary, UserVocabularyProgress, VocabularyReview,
    UserVocabularyList
)


class AnalyticsService:
    """Service for analytics and progress tracking."""

    def __init__(self, db: Session):
        """Initialize analytics service.

        Args:
            db: Database session
        """
        self.db = db

    # ========== OVERALL PROGRESS ANALYTICS ==========

    def get_overall_progress(self, user_id: int) -> Dict:
        """Get comprehensive progress across all modules.

        Args:
            user_id: User ID

        Returns:
            Dictionary with overall progress metrics
        """
        conversation_stats = self._get_conversation_stats(user_id)
        grammar_stats = self._get_grammar_stats(user_id)
        vocabulary_stats = self._get_vocabulary_stats(user_id)
        activity_stats = self._get_activity_stats(user_id)

        # Calculate overall score (0-100)
        overall_score = self._calculate_overall_score(
            conversation_stats,
            grammar_stats,
            vocabulary_stats
        )

        return {
            "user_id": user_id,
            "overall_score": overall_score,
            "last_updated": datetime.utcnow(),
            "conversation": conversation_stats,
            "grammar": grammar_stats,
            "vocabulary": vocabulary_stats,
            "activity": activity_stats,
            "weekly_goal_progress": self._get_weekly_goal_progress(user_id)
        }

    def _get_conversation_stats(self, user_id: int) -> Dict:
        """Get conversation module statistics."""
        # Total sessions
        total_sessions = self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.ended_at.isnot(None)
        ).count()

        # Total messages
        total_messages = self.db.query(ConversationTurn).join(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationTurn.speaker == "user"
        ).count()

        # Average session duration
        sessions_with_duration = self.db.query(
            func.extract('epoch', ConversationSession.ended_at - ConversationSession.started_at).label('duration')
        ).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.ended_at.isnot(None)
        ).all()

        avg_duration = 0
        if sessions_with_duration:
            durations = [s.duration for s in sessions_with_duration if s.duration]
            avg_duration = sum(durations) / len(durations) if durations else 0

        # Context variety
        unique_contexts = self.db.query(
            distinct(ConversationSession.context_id)
        ).filter(
            ConversationSession.user_id == user_id
        ).count()

        # Recent activity (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_sessions = self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.started_at >= week_ago
        ).count()

        return {
            "total_sessions": total_sessions,
            "total_messages": total_messages,
            "average_session_duration_minutes": round(avg_duration / 60, 1) if avg_duration else 0,
            "unique_contexts_practiced": unique_contexts,
            "sessions_last_7_days": recent_sessions,
            "estimated_conversation_hours": round((total_messages * 2) / 60, 1)  # ~2 min per message
        }

    def _get_grammar_stats(self, user_id: int) -> Dict:
        """Get grammar module statistics."""
        # Total topics practiced
        topics_practiced = self.db.query(UserGrammarProgress).filter(
            UserGrammarProgress.user_id == user_id
        ).count()

        # Topics mastered (mastery >= 4.0)
        topics_mastered = self.db.query(UserGrammarProgress).filter(
            UserGrammarProgress.user_id == user_id,
            UserGrammarProgress.mastery_level >= 4.0
        ).count()

        # Total exercises attempted
        total_exercises = self.db.query(GrammarExerciseAttempt).join(GrammarSession).filter(
            GrammarSession.user_id == user_id
        ).count()

        # Overall accuracy
        attempts = self.db.query(GrammarExerciseAttempt).join(GrammarSession).filter(
            GrammarSession.user_id == user_id
        ).all()

        overall_accuracy = 0
        if attempts:
            correct_count = sum(1 for a in attempts if a.is_correct)
            overall_accuracy = (correct_count / len(attempts)) * 100

        # Average mastery level
        all_progress = self.db.query(UserGrammarProgress).filter(
            UserGrammarProgress.user_id == user_id
        ).all()

        avg_mastery = 0
        if all_progress:
            avg_mastery = sum(p.mastery_level for p in all_progress) / len(all_progress)

        # Weak areas (mastery < 2.5)
        weak_areas = self.db.query(UserGrammarProgress, GrammarTopic).join(
            GrammarTopic, UserGrammarProgress.topic_id == GrammarTopic.id
        ).filter(
            UserGrammarProgress.user_id == user_id,
            UserGrammarProgress.mastery_level < 2.5
        ).order_by(UserGrammarProgress.mastery_level).limit(5).all()

        weak_topics = [
            {"topic_id": p.topic_id, "topic_name": t.name_de, "mastery": p.mastery_level}
            for p, t in weak_areas
        ]

        # Strong areas (mastery >= 4.0)
        strong_areas = self.db.query(UserGrammarProgress, GrammarTopic).join(
            GrammarTopic, UserGrammarProgress.topic_id == GrammarTopic.id
        ).filter(
            UserGrammarProgress.user_id == user_id,
            UserGrammarProgress.mastery_level >= 4.0
        ).order_by(desc(UserGrammarProgress.mastery_level)).limit(5).all()

        strong_topics = [
            {"topic_id": p.topic_id, "topic_name": t.name_de, "mastery": p.mastery_level}
            for p, t in strong_areas
        ]

        return {
            "topics_practiced": topics_practiced,
            "topics_mastered": topics_mastered,
            "total_exercises_attempted": total_exercises,
            "overall_accuracy_percentage": round(overall_accuracy, 1),
            "average_mastery_level": round(avg_mastery, 2),
            "weak_areas": weak_topics,
            "strong_areas": strong_topics
        }

    def _get_vocabulary_stats(self, user_id: int) -> Dict:
        """Get vocabulary module statistics."""
        # Total words learned
        words_learned = self.db.query(UserVocabularyProgress).filter(
            UserVocabularyProgress.user_id == user_id
        ).count()

        # Words mastered (mastery_level == 5)
        words_mastered = self.db.query(UserVocabularyProgress).filter(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.mastery_level == 5
        ).count()

        # Total reviews
        total_reviews = self.db.query(VocabularyReview).filter(
            VocabularyReview.user_id == user_id
        ).count()

        # Overall accuracy
        reviews = self.db.query(VocabularyReview).filter(
            VocabularyReview.user_id == user_id
        ).all()

        vocab_accuracy = 0
        if reviews:
            correct_count = sum(1 for r in reviews if r.was_correct)
            vocab_accuracy = (correct_count / len(reviews)) * 100

        # Words by CEFR level
        words_by_level = {}
        progress_list = self.db.query(UserVocabularyProgress).filter(
            UserVocabularyProgress.user_id == user_id
        ).all()

        for progress in progress_list:
            word = self.db.query(Vocabulary).filter(
                Vocabulary.id == progress.word_id
            ).first()
            if word:
                level = word.difficulty
                words_by_level[level] = words_by_level.get(level, 0) + 1

        # Personal lists
        personal_lists = self.db.query(UserVocabularyList).filter(
            UserVocabularyList.user_id == user_id
        ).count()

        # Current streak
        streak = self._calculate_vocabulary_streak(user_id)

        return {
            "total_words_learned": words_learned,
            "words_mastered": words_mastered,
            "total_reviews": total_reviews,
            "overall_accuracy_percentage": round(vocab_accuracy, 1),
            "words_by_cefr_level": words_by_level,
            "personal_vocabulary_lists": personal_lists,
            "current_streak_days": streak
        }

    def _get_activity_stats(self, user_id: int) -> Dict:
        """Get overall activity statistics."""
        # Total study days
        all_dates = set()

        # Conversation dates
        conv_sessions = self.db.query(ConversationSession.started_at).filter(
            ConversationSession.user_id == user_id
        ).all()
        all_dates.update(s.started_at.date() for s in conv_sessions)

        # Grammar dates
        grammar_sessions = self.db.query(GrammarSession.started_at).filter(
            GrammarSession.user_id == user_id
        ).all()
        all_dates.update(s.started_at.date() for s in grammar_sessions)

        # Vocabulary dates
        vocab_reviews = self.db.query(VocabularyReview.reviewed_at).filter(
            VocabularyReview.user_id == user_id
        ).all()
        all_dates.update(r.reviewed_at.date() for r in vocab_reviews)

        total_study_days = len(all_dates)

        # Current streak
        current_streak = 0
        check_date = datetime.utcnow().date()
        while check_date in all_dates:
            current_streak += 1
            check_date -= timedelta(days=1)

        # Longest streak
        sorted_dates = sorted(all_dates)
        longest_streak = 0
        current_run = 0

        for i, date in enumerate(sorted_dates):
            if i == 0:
                current_run = 1
            elif date == sorted_dates[i-1] + timedelta(days=1):
                current_run += 1
            else:
                current_run = 1
            longest_streak = max(longest_streak, current_run)

        # Average sessions per week
        if total_study_days > 0:
            weeks = max(1, total_study_days / 7)
            avg_sessions_per_week = len(conv_sessions + grammar_sessions) / weeks
        else:
            avg_sessions_per_week = 0

        return {
            "total_study_days": total_study_days,
            "current_streak_days": current_streak,
            "longest_streak_days": longest_streak,
            "average_sessions_per_week": round(avg_sessions_per_week, 1)
        }

    def _calculate_overall_score(
        self,
        conversation_stats: Dict,
        grammar_stats: Dict,
        vocabulary_stats: Dict
    ) -> int:
        """Calculate overall progress score (0-100)."""
        # Weight different aspects
        conversation_score = min(100, conversation_stats["total_sessions"] * 5)
        grammar_score = grammar_stats["average_mastery_level"] * 20
        vocabulary_score = min(100, vocabulary_stats["total_words_learned"] * 2)

        # Weighted average
        overall = (conversation_score * 0.3 + grammar_score * 0.4 + vocabulary_score * 0.3)
        return round(min(100, overall))

    def _calculate_vocabulary_streak(self, user_id: int) -> int:
        """Calculate current vocabulary review streak."""
        reviews = self.db.query(VocabularyReview).filter(
            VocabularyReview.user_id == user_id
        ).order_by(desc(VocabularyReview.reviewed_at)).all()

        if not reviews:
            return 0

        review_dates = set(r.reviewed_at.date() for r in reviews)
        current_streak = 0
        check_date = datetime.utcnow().date()

        while check_date in review_dates:
            current_streak += 1
            check_date -= timedelta(days=1)

        return current_streak

    def _get_weekly_goal_progress(self, user_id: int) -> Dict:
        """Get progress toward weekly goals (5+ sessions)."""
        week_start = datetime.utcnow() - timedelta(days=7)

        # Count all session types this week
        conversation_count = self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.started_at >= week_start
        ).count()

        grammar_count = self.db.query(GrammarSession).filter(
            GrammarSession.user_id == user_id,
            GrammarSession.started_at >= week_start
        ).count()

        total_sessions = conversation_count + grammar_count
        goal_sessions = 5

        return {
            "sessions_this_week": total_sessions,
            "goal_sessions": goal_sessions,
            "goal_percentage": min(100, round((total_sessions / goal_sessions) * 100)),
            "goal_met": total_sessions >= goal_sessions
        }

    # ========== ERROR PATTERN ANALYSIS ==========

    def analyze_error_patterns(self, user_id: int, days: int = 30) -> Dict:
        """Analyze common error patterns across grammar and conversation.

        Args:
            user_id: User ID
            days: Number of days to analyze

        Returns:
            Dictionary with error pattern analysis
        """
        cutoff_date = datetime.utcnow() - timedelta(days=days)

        # Grammar errors
        grammar_errors = self._analyze_grammar_errors(user_id, cutoff_date)

        # Most frequent error types
        error_types = defaultdict(int)
        for error in grammar_errors:
            error_types[error["topic_name"]] += 1

        top_errors = sorted(
            [{"topic": k, "count": v} for k, v in error_types.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:10]

        # Recurring mistakes (same topic failed multiple times)
        recurring = self._find_recurring_mistakes(user_id, cutoff_date)

        # Improvement trends
        trends = self._analyze_improvement_trends(user_id, cutoff_date)

        return {
            "analysis_period_days": days,
            "total_errors": len(grammar_errors),
            "top_error_topics": top_errors,
            "recurring_mistakes": recurring,
            "improvement_trends": trends,
            "recommendations": self._generate_recommendations(top_errors, recurring)
        }

    def _analyze_grammar_errors(self, user_id: int, cutoff_date: datetime) -> List[Dict]:
        """Get all grammar errors in time period."""
        attempts = self.db.query(GrammarExerciseAttempt, GrammarTopic).join(
            GrammarSession
        ).join(
            GrammarTopic, GrammarExerciseAttempt.topic_id == GrammarTopic.id
        ).filter(
            GrammarSession.user_id == user_id,
            GrammarExerciseAttempt.attempted_at >= cutoff_date,
            GrammarExerciseAttempt.is_correct == False
        ).all()

        return [
            {
                "topic_id": topic.id,
                "topic_name": topic.name_de,
                "category": topic.category,
                "attempted_at": attempt.attempted_at,
                "difficulty": topic.difficulty_level
            }
            for attempt, topic in attempts
        ]

    def _find_recurring_mistakes(self, user_id: int, cutoff_date: datetime) -> List[Dict]:
        """Find topics with recurring errors."""
        # Get all incorrect attempts
        incorrect_attempts = self.db.query(
            GrammarExerciseAttempt.topic_id,
            func.count(GrammarExerciseAttempt.id).label('error_count')
        ).join(GrammarSession).filter(
            GrammarSession.user_id == user_id,
            GrammarExerciseAttempt.attempted_at >= cutoff_date,
            GrammarExerciseAttempt.is_correct == False
        ).group_by(GrammarExerciseAttempt.topic_id).having(
            func.count(GrammarExerciseAttempt.id) >= 3  # 3+ errors = recurring
        ).all()

        recurring = []
        for topic_id, error_count in incorrect_attempts:
            topic = self.db.query(GrammarTopic).filter(GrammarTopic.id == topic_id).first()
            if topic:
                recurring.append({
                    "topic_id": topic_id,
                    "topic_name": topic.name_de,
                    "error_count": error_count,
                    "severity": "high" if error_count >= 5 else "medium"
                })

        return sorted(recurring, key=lambda x: x["error_count"], reverse=True)

    def _analyze_improvement_trends(self, user_id: int, cutoff_date: datetime) -> List[Dict]:
        """Analyze which topics are improving."""
        progress_records = self.db.query(UserGrammarProgress, GrammarTopic).join(
            GrammarTopic
        ).filter(
            UserGrammarProgress.user_id == user_id,
            UserGrammarProgress.last_practiced >= cutoff_date
        ).all()

        trends = []
        for progress, topic in progress_records:
            # Check if accuracy is improving
            recent_attempts = self.db.query(GrammarExerciseAttempt).join(
                GrammarSession
            ).filter(
                GrammarSession.user_id == user_id,
                GrammarExerciseAttempt.topic_id == topic.id,
                GrammarExerciseAttempt.attempted_at >= cutoff_date
            ).order_by(GrammarExerciseAttempt.attempted_at).all()

            if len(recent_attempts) >= 5:
                first_half = recent_attempts[:len(recent_attempts)//2]
                second_half = recent_attempts[len(recent_attempts)//2:]

                first_accuracy = sum(1 for a in first_half if a.is_correct) / len(first_half) * 100
                second_accuracy = sum(1 for a in second_half if a.is_correct) / len(second_half) * 100

                improvement = second_accuracy - first_accuracy

                if abs(improvement) > 10:  # Significant change
                    trends.append({
                        "topic_id": topic.id,
                        "topic_name": topic.name_de,
                        "trend": "improving" if improvement > 0 else "declining",
                        "improvement_percentage": round(improvement, 1)
                    })

        return sorted(trends, key=lambda x: abs(x["improvement_percentage"]), reverse=True)[:10]

    def _generate_recommendations(self, top_errors: List[Dict], recurring: List[Dict]) -> List[str]:
        """Generate learning recommendations based on error analysis."""
        recommendations = []

        if top_errors:
            top_topic = top_errors[0]["topic"]
            recommendations.append(
                f"Focus on '{top_topic}' - this is your most frequent error area"
            )

        if recurring:
            for mistake in recurring[:2]:
                recommendations.append(
                    f"Review '{mistake['topic_name']}' fundamentals - you have {mistake['error_count']} recurring errors"
                )

        if len(recommendations) < 3:
            recommendations.append("Continue with regular practice across all topics")

        return recommendations

    # ========== PROGRESS SNAPSHOTS ==========

    def create_progress_snapshot(self, user_id: int) -> Dict:
        """Create a point-in-time snapshot of user progress.

        Args:
            user_id: User ID

        Returns:
            Progress snapshot dictionary
        """
        overall_progress = self.get_overall_progress(user_id)
        error_patterns = self.analyze_error_patterns(user_id, days=30)

        return {
            "snapshot_date": datetime.utcnow(),
            "user_id": user_id,
            "overall_progress": overall_progress,
            "error_analysis": error_patterns,
            "milestones_achieved": self._get_milestones(user_id),
            "next_goals": self._suggest_next_goals(overall_progress)
        }

    def _get_milestones(self, user_id: int) -> List[Dict]:
        """Get achieved milestones."""
        milestones = []

        overall = self.get_overall_progress(user_id)

        # Conversation milestones
        if overall["conversation"]["total_sessions"] >= 10:
            milestones.append({"type": "conversation", "milestone": "10_sessions"})
        if overall["conversation"]["total_sessions"] >= 50:
            milestones.append({"type": "conversation", "milestone": "50_sessions"})

        # Grammar milestones
        if overall["grammar"]["topics_mastered"] >= 5:
            milestones.append({"type": "grammar", "milestone": "5_topics_mastered"})
        if overall["grammar"]["topics_mastered"] >= 20:
            milestones.append({"type": "grammar", "milestone": "20_topics_mastered"})

        # Vocabulary milestones
        if overall["vocabulary"]["total_words_learned"] >= 100:
            milestones.append({"type": "vocabulary", "milestone": "100_words"})
        if overall["vocabulary"]["total_words_learned"] >= 500:
            milestones.append({"type": "vocabulary", "milestone": "500_words"})

        # Streak milestones
        if overall["activity"]["current_streak_days"] >= 7:
            milestones.append({"type": "activity", "milestone": "7_day_streak"})
        if overall["activity"]["current_streak_days"] >= 30:
            milestones.append({"type": "activity", "milestone": "30_day_streak"})

        return milestones

    def _suggest_next_goals(self, overall_progress: Dict) -> List[str]:
        """Suggest next learning goals."""
        goals = []

        # Weekly goal
        if not overall_progress["weekly_goal_progress"]["goal_met"]:
            remaining = 5 - overall_progress["weekly_goal_progress"]["sessions_this_week"]
            goals.append(f"Complete {remaining} more sessions this week to reach your weekly goal")

        # Grammar goals
        if overall_progress["grammar"]["topics_practiced"] < 10:
            goals.append("Practice at least 10 grammar topics to build a strong foundation")

        if overall_progress["grammar"]["weak_areas"]:
            weak_topic = overall_progress["grammar"]["weak_areas"][0]["topic_name"]
            goals.append(f"Improve mastery in '{weak_topic}' to 3.0+")

        # Vocabulary goals
        if overall_progress["vocabulary"]["total_words_learned"] < 100:
            goals.append("Learn at least 100 vocabulary words")

        # Activity goals
        if overall_progress["activity"]["current_streak_days"] < 7:
            goals.append("Build a 7-day study streak")

        return goals[:5]  # Return top 5 goals

    # ========== COMPARATIVE ANALYTICS ==========

    def get_progress_comparison(self, user_id: int, period_days: int = 30) -> Dict:
        """Compare progress between two time periods.

        Args:
            user_id: User ID
            period_days: Days in each period

        Returns:
            Comparison between current and previous period
        """
        current_end = datetime.utcnow()
        current_start = current_end - timedelta(days=period_days)
        previous_start = current_start - timedelta(days=period_days)

        current_stats = self._get_period_stats(user_id, current_start, current_end)
        previous_stats = self._get_period_stats(user_id, previous_start, current_start)

        return {
            "period_days": period_days,
            "current_period": current_stats,
            "previous_period": previous_stats,
            "changes": self._calculate_changes(current_stats, previous_stats)
        }

    def _get_period_stats(self, user_id: int, start: datetime, end: datetime) -> Dict:
        """Get statistics for a specific time period."""
        # Sessions
        conv_sessions = self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.started_at >= start,
            ConversationSession.started_at < end
        ).count()

        grammar_sessions = self.db.query(GrammarSession).filter(
            GrammarSession.user_id == user_id,
            GrammarSession.started_at >= start,
            GrammarSession.started_at < end
        ).count()

        # Exercises
        exercises = self.db.query(GrammarExerciseAttempt).join(GrammarSession).filter(
            GrammarSession.user_id == user_id,
            GrammarExerciseAttempt.attempted_at >= start,
            GrammarExerciseAttempt.attempted_at < end
        ).all()

        exercise_accuracy = 0
        if exercises:
            correct = sum(1 for e in exercises if e.is_correct)
            exercise_accuracy = (correct / len(exercises)) * 100

        # Vocabulary reviews
        reviews = self.db.query(VocabularyReview).filter(
            VocabularyReview.user_id == user_id,
            VocabularyReview.reviewed_at >= start,
            VocabularyReview.reviewed_at < end
        ).count()

        return {
            "total_sessions": conv_sessions + grammar_sessions,
            "conversation_sessions": conv_sessions,
            "grammar_sessions": grammar_sessions,
            "exercises_completed": len(exercises),
            "exercise_accuracy": round(exercise_accuracy, 1),
            "vocabulary_reviews": reviews
        }

    def _calculate_changes(self, current: Dict, previous: Dict) -> Dict:
        """Calculate percentage changes between periods."""
        changes = {}

        for key in current.keys():
            if isinstance(current[key], (int, float)):
                if previous[key] == 0:
                    change = 100 if current[key] > 0 else 0
                else:
                    change = ((current[key] - previous[key]) / previous[key]) * 100

                changes[f"{key}_change_percent"] = round(change, 1)
                changes[f"{key}_trend"] = "up" if change > 0 else ("down" if change < 0 else "stable")

        return changes
