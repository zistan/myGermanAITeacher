"""
Integration Service - connects all modules seamlessly.
Provides cross-module workflows and intelligent recommendations.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

from app.models.user import User
from app.models.session import Session as ConversationSession, ConversationTurn
from app.models.context import Context
from app.models.grammar import (
    GrammarTopic, UserGrammarProgress, GrammarSession,
    GrammarExerciseAttempt, GrammarExercise
)
from app.models.vocabulary import (
    Vocabulary, UserVocabularyProgress, VocabularyReview
)
from app.services.analytics_service import AnalyticsService


class IntegrationService:
    """Service for cross-module integration and intelligent workflows."""

    def __init__(self, db: Session):
        """Initialize integration service.

        Args:
            db: Database session
        """
        self.db = db
        self.analytics = AnalyticsService(db)

    # ========== CONVERSATION → GRAMMAR/VOCABULARY FLOW ==========

    def analyze_conversation_session(self, session_id: int, user_id: int) -> Dict:
        """Analyze a conversation session and suggest grammar/vocabulary practice.

        Args:
            session_id: Conversation session ID
            user_id: User ID

        Returns:
            Dictionary with session analysis and recommendations
        """
        session = self.db.query(ConversationSession).filter(
            ConversationSession.id == session_id,
            ConversationSession.user_id == user_id
        ).first()

        if not session:
            return {"error": "Session not found"}

        # Get all messages from session
        messages = self.db.query(ConversationTurn).filter(
            ConversationTurn.session_id == session_id
        ).order_by(ConversationTurn.created_at).all()

        user_messages = [m for m in messages if m.role == "user"]
        ai_messages = [m for m in messages if m.role == "assistant"]

        # Analyze session
        duration = None
        if session.ended_at and session.started_at:
            duration = (session.ended_at - session.started_at).total_seconds() / 60

        # Extract grammar/vocabulary from session metadata
        grammar_detected = session.grammar_topics_detected or []
        vocabulary_detected = session.vocabulary_words_detected or []

        # Get grammar recommendations
        grammar_recommendations = self._get_grammar_recommendations_from_session(
            grammar_detected, user_id
        )

        # Get vocabulary recommendations
        vocabulary_recommendations = self._get_vocabulary_recommendations_from_session(
            vocabulary_detected, user_id
        )

        # Get context info
        context = None
        if session.context_id:
            context = self.db.query(Context).filter(Context.id == session.context_id).first()

        return {
            "session_id": session_id,
            "started_at": session.started_at,
            "ended_at": session.ended_at,
            "duration_minutes": round(duration, 1) if duration else None,
            "context": {
                "id": context.id,
                "name": context.name,
                "category": context.category,
                "difficulty_level": context.difficulty_level
            } if context else None,
            "message_count": len(user_messages),
            "grammar_topics_detected": grammar_detected,
            "vocabulary_words_detected": vocabulary_detected,
            "recommendations": {
                "grammar": grammar_recommendations,
                "vocabulary": vocabulary_recommendations,
                "next_steps": self._generate_next_steps(
                    grammar_recommendations,
                    vocabulary_recommendations,
                    context
                )
            }
        }

    def _get_grammar_recommendations_from_session(
        self,
        detected_topics: List[str],
        user_id: int
    ) -> List[Dict]:
        """Get grammar practice recommendations based on detected topics."""
        recommendations = []

        for topic_name in detected_topics[:5]:  # Top 5
            # Find topic
            topic = self.db.query(GrammarTopic).filter(
                GrammarTopic.name_de.ilike(f"%{topic_name}%")
            ).first()

            if not topic:
                continue

            # Check user's mastery
            progress = self.db.query(UserGrammarProgress).filter(
                UserGrammarProgress.user_id == user_id,
                UserGrammarProgress.topic_id == topic.id
            ).first()

            mastery_level = progress.mastery_level if progress else 0
            priority = "high" if mastery_level < 3.0 else "medium"

            recommendations.append({
                "topic_id": topic.id,
                "topic_name": topic.name_de,
                "category": topic.category,
                "current_mastery": mastery_level,
                "priority": priority,
                "reason": f"Detected in conversation - current mastery: {mastery_level:.1f}/5.0"
            })

        return recommendations

    def _get_vocabulary_recommendations_from_session(
        self,
        detected_words: List[str],
        user_id: int
    ) -> List[Dict]:
        """Get vocabulary practice recommendations based on detected words."""
        recommendations = []

        for word in detected_words[:10]:  # Top 10
            # Find word
            vocab_word = self.db.query(Vocabulary).filter(
                Vocabulary.word.ilike(f"%{word}%")
            ).first()

            if not vocab_word:
                # Suggest adding it
                recommendations.append({
                    "word": word,
                    "status": "not_in_database",
                    "priority": "medium",
                    "reason": "New word detected - consider adding to vocabulary"
                })
                continue

            # Check user's progress
            progress = self.db.query(UserVocabularyProgress).filter(
                UserVocabularyProgress.user_id == user_id,
                UserVocabularyProgress.word_id == vocab_word.id
            ).first()

            if not progress:
                # Not learned yet
                recommendations.append({
                    "word_id": vocab_word.id,
                    "word": vocab_word.word,
                    "translation_it": vocab_word.translation_it,
                    "difficulty": vocab_word.difficulty,
                    "status": "not_learned",
                    "priority": "high",
                    "reason": "Used in conversation but not yet in your vocabulary"
                })
            elif progress.mastery_level < 3:
                # Needs practice
                recommendations.append({
                    "word_id": vocab_word.id,
                    "word": vocab_word.word,
                    "translation_it": vocab_word.translation_it,
                    "difficulty": vocab_word.difficulty,
                    "status": "needs_practice",
                    "mastery_level": progress.mastery_level,
                    "priority": "medium",
                    "reason": f"Mastery level {progress.mastery_level}/5 - practice recommended"
                })

        return recommendations

    def _generate_next_steps(
        self,
        grammar_recs: List[Dict],
        vocabulary_recs: List[Dict],
        context: Optional[Context]
    ) -> List[str]:
        """Generate actionable next steps based on recommendations."""
        steps = []

        # Grammar steps
        high_priority_grammar = [g for g in grammar_recs if g.get("priority") == "high"]
        if high_priority_grammar:
            topic_names = [g["topic_name"] for g in high_priority_grammar[:2]]
            steps.append(f"Practice grammar: {', '.join(topic_names)}")

        # Vocabulary steps
        not_learned = [v for v in vocabulary_recs if v.get("status") == "not_learned"]
        if not_learned:
            steps.append(f"Learn {len(not_learned)} new words from this conversation")

        needs_practice = [v for v in vocabulary_recs if v.get("status") == "needs_practice"]
        if needs_practice:
            steps.append(f"Review {len(needs_practice)} words that need more practice")

        # Context-based step
        if context and context.category:
            steps.append(f"Continue practicing {context.category} conversations to build fluency")

        if not steps:
            steps.append("Great session! Continue with regular practice")

        return steps[:4]  # Max 4 steps

    # ========== LEARNING PATH RECOMMENDATIONS ==========

    def get_personalized_learning_path(self, user_id: int) -> Dict:
        """Generate a personalized learning path across all modules.

        Args:
            user_id: User ID

        Returns:
            Personalized learning path with prioritized activities
        """
        # Get overall progress
        overall_progress = self.analytics.get_overall_progress(user_id)
        error_analysis = self.analytics.analyze_error_patterns(user_id, days=14)

        # Determine focus areas
        focus_areas = self._determine_focus_areas(overall_progress, error_analysis)

        # Generate daily plan
        daily_plan = self._generate_daily_plan(user_id, focus_areas, overall_progress)

        # Generate weekly plan
        weekly_plan = self._generate_weekly_plan(user_id, focus_areas)

        # Get recommended contexts
        recommended_contexts = self._get_recommended_contexts(
            user_id, overall_progress["conversation"]["unique_contexts_practiced"]
        )

        return {
            "user_id": user_id,
            "generated_at": datetime.utcnow(),
            "focus_areas": focus_areas,
            "daily_plan": daily_plan,
            "weekly_plan": weekly_plan,
            "recommended_contexts": recommended_contexts,
            "motivation_message": self._generate_motivation_message(overall_progress)
        }

    def _determine_focus_areas(self, overall_progress: Dict, error_analysis: Dict) -> List[Dict]:
        """Determine what the user should focus on."""
        focus_areas = []

        # Check grammar weak areas
        if overall_progress["grammar"]["weak_areas"]:
            for weak_area in overall_progress["grammar"]["weak_areas"][:3]:
                focus_areas.append({
                    "module": "grammar",
                    "area": weak_area["topic_name"],
                    "priority": "high",
                    "reason": f"Low mastery ({weak_area['mastery']:.1f}/5.0)"
                })

        # Check recurring errors
        if error_analysis.get("recurring_mistakes"):
            for mistake in error_analysis["recurring_mistakes"][:2]:
                if mistake["severity"] == "high":
                    focus_areas.append({
                        "module": "grammar",
                        "area": mistake["topic_name"],
                        "priority": "critical",
                        "reason": f"Recurring errors ({mistake['error_count']} times)"
                    })

        # Check vocabulary
        if overall_progress["vocabulary"]["total_words_learned"] < 100:
            focus_areas.append({
                "module": "vocabulary",
                "area": "Build vocabulary foundation",
                "priority": "high",
                "reason": "Fewer than 100 words learned"
            })

        # Check conversation variety
        if overall_progress["conversation"]["unique_contexts_practiced"] < 5:
            focus_areas.append({
                "module": "conversation",
                "area": "Explore more contexts",
                "priority": "medium",
                "reason": "Limited context variety"
            })

        return focus_areas[:5]  # Top 5 focus areas

    def _generate_daily_plan(
        self,
        user_id: int,
        focus_areas: List[Dict],
        overall_progress: Dict
    ) -> Dict:
        """Generate a daily study plan (60-90 minutes)."""
        plan = {
            "total_duration_minutes": 75,
            "activities": []
        }

        # Morning: Vocabulary review (15 min)
        words_due_today = overall_progress["weekly_goal_progress"].get("sessions_this_week", 0)
        plan["activities"].append({
            "time_of_day": "morning",
            "activity": "vocabulary_review",
            "duration_minutes": 15,
            "description": "Review vocabulary flashcards",
            "priority": "high"
        })

        # Midday: Grammar practice (30 min)
        grammar_focus = next(
            (f for f in focus_areas if f["module"] == "grammar"),
            None
        )
        if grammar_focus:
            plan["activities"].append({
                "time_of_day": "midday",
                "activity": "grammar_practice",
                "topic": grammar_focus["area"],
                "duration_minutes": 30,
                "description": f"Practice {grammar_focus['area']}",
                "priority": grammar_focus["priority"]
            })

        # Evening: Conversation (30 min)
        plan["activities"].append({
            "time_of_day": "evening",
            "activity": "conversation",
            "duration_minutes": 30,
            "description": "Conversation practice in varied contexts",
            "priority": "medium"
        })

        return plan

    def _generate_weekly_plan(self, user_id: int, focus_areas: List[Dict]) -> Dict:
        """Generate a weekly study plan."""
        return {
            "goal_sessions": 5,
            "focus_distribution": {
                "conversation": 2,  # 2 sessions/week
                "grammar": 2,       # 2 sessions/week
                "vocabulary": 1     # 1 dedicated session/week
            },
            "milestones": [
                "Complete 5+ total sessions",
                "Practice all identified weak areas",
                "Learn 20+ new vocabulary words",
                "Improve accuracy in recurring error topics"
            ]
        }

    def _get_recommended_contexts(
        self,
        user_id: int,
        contexts_practiced: int
    ) -> List[Dict]:
        """Get recommended conversation contexts."""
        # Get contexts not yet practiced or least practiced
        practiced_context_ids = self.db.query(
            ConversationSession.context_id,
            func.count(ConversationSession.id).label('session_count')
        ).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.context_id.isnot(None)
        ).group_by(ConversationSession.context_id).all()

        practiced_dict = {ctx_id: count for ctx_id, count in practiced_context_ids}

        # Get all active contexts
        all_contexts = self.db.query(Context).filter(Context.is_active == True).all()

        recommendations = []
        for context in all_contexts:
            practice_count = practiced_dict.get(context.id, 0)

            # Prioritize unpracticed or rarely practiced
            if practice_count == 0:
                priority = "high"
                reason = "Not yet practiced"
            elif practice_count < 3:
                priority = "medium"
                reason = f"Practiced {practice_count} times - good for review"
            else:
                priority = "low"
                reason = f"Well practiced ({practice_count} sessions)"

            recommendations.append({
                "context_id": context.id,
                "name": context.name,
                "category": context.category,
                "difficulty_level": context.difficulty_level,
                "times_practiced": practice_count,
                "priority": priority,
                "reason": reason
            })

        # Sort by priority and practice count
        priority_order = {"high": 0, "medium": 1, "low": 2}
        recommendations.sort(key=lambda x: (priority_order[x["priority"]], x["times_practiced"]))

        return recommendations[:8]  # Top 8 recommendations

    def _generate_motivation_message(self, overall_progress: Dict) -> str:
        """Generate a motivational message based on progress."""
        score = overall_progress["overall_score"]
        streak = overall_progress["activity"]["current_streak_days"]

        if score >= 80:
            message = "Hervorragend! You're making excellent progress!"
        elif score >= 60:
            message = "Sehr gut! You're on the right track!"
        elif score >= 40:
            message = "Gut gemacht! Keep up the consistent practice!"
        else:
            message = "Los geht's! Every session brings you closer to fluency!"

        if streak >= 7:
            message += f" 🔥 Amazing {streak}-day streak!"
        elif streak >= 3:
            message += f" Keep your {streak}-day streak going!"

        return message

    # ========== UNIFIED DASHBOARD DATA ==========

    def get_dashboard_data(self, user_id: int) -> Dict:
        """Get comprehensive dashboard data combining all modules.

        Args:
            user_id: User ID

        Returns:
            Complete dashboard data
        """
        # Get overall progress
        overall_progress = self.analytics.get_overall_progress(user_id)

        # Get learning path
        learning_path = self.get_personalized_learning_path(user_id)

        # Get due items
        due_items = self._get_due_items(user_id)

        # Get recent activity
        recent_activity = self._get_recent_activity(user_id, days=7)

        # Get achievements progress (top incomplete)
        from app.models.achievement import Achievement, UserAchievement

        close_achievements = []
        all_achievements = self.db.query(Achievement).filter(
            Achievement.is_active == True
        ).limit(20).all()

        for achievement in all_achievements:
            user_achievement = self.db.query(UserAchievement).filter(
                UserAchievement.user_id == user_id,
                UserAchievement.achievement_id == achievement.id
            ).first()

            if user_achievement and user_achievement.is_completed:
                continue  # Skip completed

            # Calculate progress
            current_progress = self._calculate_achievement_progress_value(
                achievement, overall_progress
            )

            progress_percent = min(100, int((current_progress / achievement.criteria_value) * 100))

            if progress_percent >= 50:  # Close to completion
                close_achievements.append({
                    "achievement_name": achievement.name,
                    "progress_percent": progress_percent,
                    "current_value": current_progress,
                    "target_value": achievement.criteria_value,
                    "tier": achievement.tier,
                    "points": achievement.points
                })

        close_achievements.sort(key=lambda x: x["progress_percent"], reverse=True)

        return {
            "user_id": user_id,
            "last_updated": datetime.utcnow(),
            "overall_progress": overall_progress,
            "learning_path": learning_path,
            "due_items": due_items,
            "recent_activity": recent_activity,
            "close_achievements": close_achievements[:5],
            "quick_actions": self._generate_quick_actions(due_items, learning_path)
        }

    def _get_due_items(self, user_id: int) -> Dict:
        """Get items due for review/practice today."""
        now = datetime.utcnow()

        # Grammar topics due
        grammar_due = self.db.query(UserGrammarProgress, GrammarTopic).join(
            GrammarTopic
        ).filter(
            UserGrammarProgress.user_id == user_id,
            UserGrammarProgress.next_review_date <= now
        ).limit(10).all()

        # Vocabulary words due
        vocabulary_due = self.db.query(UserVocabularyProgress, Vocabulary).join(
            Vocabulary
        ).filter(
            UserVocabularyProgress.user_id == user_id,
            UserVocabularyProgress.next_review_due <= now
        ).limit(20).all()

        return {
            "grammar_topics": [
                {
                    "topic_id": topic.id,
                    "topic_name": topic.name_de,
                    "mastery_level": progress.mastery_level,
                    "days_overdue": (now - progress.next_review_date).days if progress.next_review_date else 0
                }
                for progress, topic in grammar_due
            ],
            "vocabulary_words": [
                {
                    "word_id": word.id,
                    "word": word.word,
                    "translation_it": word.translation_it,
                    "mastery_level": progress.mastery_level,
                    "days_overdue": (now - progress.next_review_due).days if progress.next_review_due else 0
                }
                for progress, word in vocabulary_due
            ],
            "total_due": len(grammar_due) + len(vocabulary_due)
        }

    def _get_recent_activity(self, user_id: int, days: int = 7) -> List[Dict]:
        """Get recent activity across all modules."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        activities = []

        # Conversation sessions
        conv_sessions = self.db.query(ConversationSession).filter(
            ConversationSession.user_id == user_id,
            ConversationSession.started_at >= cutoff
        ).order_by(desc(ConversationSession.started_at)).limit(10).all()

        for session in conv_sessions:
            context = self.db.query(Context).filter(Context.id == session.context_id).first()
            activities.append({
                "type": "conversation",
                "timestamp": session.started_at,
                "description": f"Conversation: {context.name if context else 'Unknown context'}",
                "details": {"session_id": session.id}
            })

        # Grammar sessions
        grammar_sessions = self.db.query(GrammarSession).filter(
            GrammarSession.user_id == user_id,
            GrammarSession.started_at >= cutoff
        ).order_by(desc(GrammarSession.started_at)).limit(10).all()

        for session in grammar_sessions:
            topic = self.db.query(GrammarTopic).filter(GrammarTopic.id == session.topic_id).first()
            activities.append({
                "type": "grammar",
                "timestamp": session.started_at,
                "description": f"Grammar practice: {topic.name_de if topic else 'Unknown topic'}",
                "details": {"session_id": session.id, "exercises_completed": session.exercises_completed}
            })

        # Vocabulary reviews (sample recent)
        recent_reviews = self.db.query(VocabularyReview).filter(
            VocabularyReview.user_id == user_id,
            VocabularyReview.reviewed_at >= cutoff
        ).order_by(desc(VocabularyReview.reviewed_at)).limit(5).all()

        if recent_reviews:
            activities.append({
                "type": "vocabulary",
                "timestamp": recent_reviews[0].reviewed_at,
                "description": f"Vocabulary review: {len(recent_reviews)} words",
                "details": {"review_count": len(recent_reviews)}
            })

        # Sort by timestamp
        activities.sort(key=lambda x: x["timestamp"], reverse=True)

        return activities[:15]  # Last 15 activities

    def _generate_quick_actions(self, due_items: Dict, learning_path: Dict) -> List[Dict]:
        """Generate quick action buttons for dashboard."""
        actions = []

        # Due items action
        if due_items["total_due"] > 0:
            actions.append({
                "action": "review_due_items",
                "label": f"Review {due_items['total_due']} due items",
                "priority": "high",
                "icon": "clock"
            })

        # Daily plan action
        if learning_path["daily_plan"]["activities"]:
            next_activity = learning_path["daily_plan"]["activities"][0]
            actions.append({
                "action": "start_daily_plan",
                "label": f"Start today's plan: {next_activity['activity'].replace('_', ' ').title()}",
                "priority": "medium",
                "icon": "play"
            })

        # Conversation action
        if learning_path["recommended_contexts"]:
            top_context = learning_path["recommended_contexts"][0]
            actions.append({
                "action": "start_conversation",
                "label": f"Practice: {top_context['name']}",
                "priority": "medium",
                "icon": "chat",
                "context_id": top_context["context_id"]
            })

        # Grammar action
        if learning_path["focus_areas"]:
            grammar_focus = next(
                (f for f in learning_path["focus_areas"] if f["module"] == "grammar"),
                None
            )
            if grammar_focus:
                actions.append({
                    "action": "practice_grammar",
                    "label": f"Improve: {grammar_focus['area']}",
                    "priority": grammar_focus["priority"],
                    "icon": "book"
                })

        return actions[:4]  # Top 4 quick actions

    def _calculate_achievement_progress_value(
        self,
        achievement,
        overall_progress: Dict
    ) -> int:
        """Calculate current progress value for an achievement."""
        criteria_type = achievement.criteria_type

        if criteria_type == "sessions_count":
            return overall_progress["conversation"]["total_sessions"] + overall_progress["grammar"]["topics_practiced"]
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
        else:
            return 0
