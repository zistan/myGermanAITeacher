"""
Grammar Gap Analyzer

Identify incomplete grammar topics and recommend exercise generation.
Analyzes exercise count per topic, type distribution, and missing topics.
"""

from typing import Dict, List
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


class GrammarGapAnalyzer:
    """Analyze grammar gaps and recommend next topics"""

    def __init__(self, db_session, config):
        """
        Initialize analyzer

        Args:
            db_session: SQLAlchemy database session
            config: BatchConfig instance
        """
        self.db = db_session
        self.config = config
        logger.info("Initialized GrammarGapAnalyzer")

    def analyze_topic_gaps(self) -> List[Dict]:
        """
        Returns incomplete topics

        Returns:
            List of topic gap dictionaries sorted by priority (highest first)
            [
                {
                    "topic_id": 5,
                    "topic_name": "Akkusativ",
                    "category": "cases",
                    "difficulty_level": "A2",
                    "current_total": 25,
                    "target_total": 50,
                    "gap_size": 25,
                    "missing_types": ["translation", "sentence_building"],
                    "priority_score": 85
                }
            ]
        """
        try:
            # Import models
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.grammar import GrammarTopic, GrammarExercise

            # Query all topics with exercise counts
            topics = self.db.query(GrammarTopic).all()

            gaps = []
            for topic in topics:
                # Count exercises for this topic
                exercise_count = self.db.query(func.count(GrammarExercise.id)).filter(
                    GrammarExercise.topic_id == topic.id
                ).scalar()

                # Get exercise types for this topic
                exercise_types = self.db.query(GrammarExercise.exercise_type).filter(
                    GrammarExercise.topic_id == topic.id
                ).distinct().all()
                existing_types = {row[0] for row in exercise_types}

                # Check if topic is incomplete
                target_total = self.config.grammar_target_per_topic
                if exercise_count < target_total:
                    # Identify missing exercise types
                    all_types = {'fill_blank', 'multiple_choice', 'translation', 'error_correction', 'sentence_building'}
                    missing_types = list(all_types - existing_types)

                    # Calculate priority
                    priority_score = self._calculate_topic_priority(
                        topic=topic,
                        current_total=exercise_count,
                        target_total=target_total,
                        missing_types_count=len(missing_types)
                    )

                    gaps.append({
                        'topic_id': topic.id,
                        'topic_name': topic.name_en,
                        'category': topic.category,
                        'difficulty_level': topic.difficulty_level,
                        'current_total': exercise_count,
                        'target_total': target_total,
                        'gap_size': target_total - exercise_count,
                        'missing_types': missing_types,
                        'priority_score': priority_score
                    })

            # Sort by priority score (highest first)
            gaps.sort(key=lambda x: x['priority_score'], reverse=True)

            logger.info(f"Analyzed {len(gaps)} incomplete topics")
            return gaps

        except Exception as e:
            logger.error(f"Failed to analyze topic gaps: {e}")
            return []

    def analyze_missing_topics(self) -> List[str]:
        """
        Returns list of important topics not yet in database

        Returns:
            List of topic names from BATCH_GRAMMAR_MISSING_TOPICS config
        """
        try:
            # Import models
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.grammar import GrammarTopic

            # Get all existing topic names
            existing_topics = self.db.query(GrammarTopic.name_en).all()
            existing_names = {row[0].lower().replace(' ', '_') for row in existing_topics}

            # Filter missing topics
            missing = []
            for topic_name in self.config.grammar_missing_topics:
                normalized_name = topic_name.lower().strip().replace(' ', '_')
                if normalized_name not in existing_names:
                    missing.append(topic_name)

            logger.info(f"Found {len(missing)} missing topics")
            return missing

        except Exception as e:
            logger.error(f"Failed to analyze missing topics: {e}")
            return self.config.grammar_missing_topics  # Return all from config as fallback

    def recommend_next_topics(self, max_topics: int = 5) -> List[Dict]:
        """
        Recommend top N topics to work on

        Prioritizes: incomplete topics first, then missing topics

        Args:
            max_topics: Maximum topics to recommend

        Returns:
            List of recommendations
            [
                {
                    "action": "fill_exercises",
                    "topic_id": 5,
                    "topic_name": "Akkusativ",
                    "difficulty": "A2",
                    "exercises_needed": 25,
                    "priority_score": 85
                }
            ]
        """
        try:
            recommendations = []

            # Get incomplete topics
            topic_gaps = self.analyze_topic_gaps()

            # Add incomplete topics to recommendations
            for gap in topic_gaps[:max_topics]:
                recommendations.append({
                    'action': 'fill_exercises',
                    'topic_id': gap['topic_id'],
                    'topic_name': gap['topic_name'],
                    'category': gap['category'],
                    'difficulty': gap['difficulty_level'],
                    'exercises_needed': gap['gap_size'],
                    'missing_types': gap['missing_types'],
                    'priority_score': gap['priority_score']
                })

            # If we still have room and all topics are complete, add missing topics
            if len(recommendations) < max_topics:
                missing_topics = self.analyze_missing_topics()
                remaining_slots = max_topics - len(recommendations)

                for topic_name in missing_topics[:remaining_slots]:
                    recommendations.append({
                        'action': 'create_topic',
                        'topic_id': None,
                        'topic_name': topic_name,
                        'category': 'to_be_determined',
                        'difficulty': 'to_be_determined',
                        'exercises_needed': 20,  # Initial batch
                        'missing_types': [],
                        'priority_score': 50  # Lower priority than filling existing topics
                    })

            logger.info(f"Generated {len(recommendations)} topic recommendations")
            return recommendations

        except Exception as e:
            logger.error(f"Failed to generate recommendations: {e}")
            return []

    def _calculate_topic_priority(self, topic, current_total: int, target_total: int, missing_types_count: int) -> int:
        """Calculate priority score for topic"""
        priority = 50  # Base priority

        # Difficulty bonuses (focus on core learning levels)
        if topic.difficulty_level in ['A1', 'A2']:
            priority += 30  # Foundational
        elif topic.difficulty_level in ['B1', 'B2']:
            priority += 20  # Core learning
        elif topic.difficulty_level in ['C1', 'C2']:
            priority += 10  # Advanced

        # Completeness bonuses
        if current_total < 10:
            priority += 20  # Very incomplete
        elif current_total < 25:
            priority += 10  # Moderately incomplete

        # Category bonuses (core grammar)
        if topic.category in self.config.grammar_priority_categories:
            priority += 15

        # Missing types bonus
        if missing_types_count >= 3:
            priority += 10

        return int(priority)

    def get_gap_summary(self) -> str:
        """Get formatted gap summary for display"""
        topic_gaps = self.analyze_topic_gaps()
        missing_topics = self.analyze_missing_topics()

        lines = [
            "============================================================",
            "GRAMMAR GAP ANALYSIS",
            "============================================================",
            "",
            "✏️  INCOMPLETE TOPICS (Top 5):",
            ""
        ]

        # Show top 5 incomplete topics
        if topic_gaps:
            for i, gap in enumerate(topic_gaps[:5], 1):
                priority_icon = "⭐" if gap['category'] in self.config.grammar_priority_categories else "  "
                lines.append(
                    f"{i}. {priority_icon} {gap['topic_name']} ({gap['difficulty_level']}) [Priority: {gap['priority_score']}]"
                )
                lines.append(
                    f"   Exercises: {gap['current_total']}/{gap['target_total']} | Gap: {gap['gap_size']}"
                )
                if gap['missing_types']:
                    lines.append(f"   Missing types: {', '.join(gap['missing_types'])}")
                lines.append("")
        else:
            lines.append("  ✅ All existing topics have sufficient exercises!")
            lines.append("")

        # Show missing topics
        if missing_topics:
            lines.append("🆕 MISSING GRAMMAR TOPICS:")
            lines.append("")
            for i, topic in enumerate(missing_topics, 1):
                lines.append(f"  {i}. {topic.replace('_', ' ').title()}")
            lines.append("")
        else:
            lines.append("🆕 MISSING GRAMMAR TOPICS:")
            lines.append("")
            lines.append("  ✅ All configured topics exist in database!")
            lines.append("")

        lines.append("============================================================")

        return "\n".join(lines)

    def get_total_exercises(self) -> int:
        """Get total number of grammar exercises in database"""
        try:
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.grammar import GrammarExercise

            total = self.db.query(func.count(GrammarExercise.id)).scalar()
            return total or 0

        except Exception as e:
            logger.error(f"Failed to get total exercises: {e}")
            return 0

    def get_total_topics(self) -> int:
        """Get total number of grammar topics in database"""
        try:
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.grammar import GrammarTopic

            total = self.db.query(func.count(GrammarTopic.id)).scalar()
            return total or 0

        except Exception as e:
            logger.error(f"Failed to get total topics: {e}")
            return 0


if __name__ == "__main__":
    # Test gap analysis (requires database connection)
    logging.basicConfig(level=logging.INFO)

    import sys
    import os

    # Add backend to path
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, backend_dir)

    from app.database import SessionLocal
    from core.batch_config import BatchConfig

    # Load config
    config = BatchConfig.load()

    # Create database session
    db = SessionLocal()

    try:
        # Create analyzer
        analyzer = GrammarGapAnalyzer(db, config)

        # Analyze gaps
        print(analyzer.get_gap_summary())

        # Get recommendations
        recommendations = analyzer.recommend_next_topics(max_topics=3)
        print(f"\n📝 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. Action: {rec['action']}")
            print(f"   Topic: {rec['topic_name']} ({rec.get('difficulty', 'TBD')})")
            print(f"   Exercises needed: {rec['exercises_needed']}")
            print(f"   Priority: {rec['priority_score']}")
            print()

        # Get totals
        print(f"📊 TOTALS:")
        print(f"   Topics: {analyzer.get_total_topics()}")
        print(f"   Exercises: {analyzer.get_total_exercises()}")

    finally:
        db.close()
