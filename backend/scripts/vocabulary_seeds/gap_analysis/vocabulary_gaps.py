"""
Vocabulary Gap Analyzer

Identify vocabulary gaps and recommend next generation targets.
Analyzes category gaps and CEFR distribution mismatches.
"""

from typing import Dict, List
from sqlalchemy import func
import logging

logger = logging.getLogger(__name__)


class VocabularyGapAnalyzer:
    """Analyze vocabulary gaps and recommend next batches"""

    def __init__(self, db_session, config):
        """
        Initialize analyzer

        Args:
            db_session: SQLAlchemy database session
            config: BatchConfig instance
        """
        self.db = db_session
        self.config = config
        logger.info("Initialized VocabularyGapAnalyzer")

    def analyze_category_gaps(self) -> List[Dict]:
        """
        Returns gaps by category

        Returns:
            List of gap dictionaries sorted by priority (highest first)
            [
                {
                    "category": "business",
                    "current_count": 150,
                    "target_count": 3500,
                    "gap_size": 3350,
                    "gap_percentage": 95.7,
                    "priority_score": 95,
                    "is_priority": True
                }
            ]
        """
        try:
            # Import models
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sys.path.insert(0, backend_dir)

            from app.models.vocabulary import Vocabulary

            # Query current counts by category
            category_counts = self.db.query(
                Vocabulary.category,
                func.count(Vocabulary.id).label('count')
            ).group_by(Vocabulary.category).all()

            # Convert to dictionary
            current_counts = {row[0]: row[1] for row in category_counts}

            # Define target counts per category (customize as needed)
            target_counts = {
                'business': 3500,
                'cefr_core': 5000,
                'daily_life': 3000,
                'advanced': 2000,
                'linguistic': 1500,
                'thematic': 2000,
            }

            # Calculate gaps
            gaps = []
            for category, target in target_counts.items():
                current = current_counts.get(category, 0)
                gap_size = max(0, target - current)
                gap_percentage = (gap_size / target * 100) if target > 0 else 0
                is_priority = category in self.config.vocab_priority_categories

                # Calculate priority score
                priority_score = self._calculate_category_priority(
                    category=category,
                    gap_size=gap_size,
                    gap_percentage=gap_percentage,
                    is_priority=is_priority
                )

                gaps.append({
                    'category': category,
                    'current_count': current,
                    'target_count': target,
                    'gap_size': gap_size,
                    'gap_percentage': round(gap_percentage, 1),
                    'priority_score': priority_score,
                    'is_priority': is_priority
                })

            # Sort by priority score (highest first)
            gaps.sort(key=lambda x: x['priority_score'], reverse=True)

            logger.info(f"Analyzed {len(gaps)} category gaps")
            return gaps

        except Exception as e:
            logger.error(f"Failed to analyze category gaps: {e}")
            return []

    def analyze_cefr_distribution(self) -> Dict:
        """
        Returns current vs target CEFR distribution

        Returns:
            {
                "A1": {"current_count": 50, "current_pct": 3.0, "target_pct": 5, "gap_pct": -2.0},
                "A2": {"current_count": 100, "current_pct": 6.0, "target_pct": 10, "gap_pct": -4.0},
                ...
            }
        """
        try:
            # Import models
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            sys.path.insert(0, backend_dir)

            from app.models.vocabulary import Vocabulary

            # Query current counts by difficulty
            difficulty_counts = self.db.query(
                Vocabulary.difficulty,
                func.count(Vocabulary.id).label('count')
            ).group_by(Vocabulary.difficulty).all()

            # Convert to dictionary
            current_counts = {row[0]: row[1] for row in difficulty_counts}
            total_words = sum(current_counts.values())

            # Calculate distribution
            distribution = {}
            for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
                current_count = current_counts.get(level, 0)
                current_pct = (current_count / total_words * 100) if total_words > 0 else 0
                target_pct = self.config.cefr_distribution.get(level, 0)
                gap_pct = current_pct - target_pct

                distribution[level] = {
                    'current_count': current_count,
                    'current_pct': round(current_pct, 1),
                    'target_pct': target_pct,
                    'gap_pct': round(gap_pct, 1)
                }

            logger.info(f"Analyzed CEFR distribution (total words: {total_words})")
            return distribution

        except Exception as e:
            logger.error(f"Failed to analyze CEFR distribution: {e}")
            return {}

    def recommend_next_batch(self, max_words: int) -> Dict:
        """
        Recommend next batch to generate

        Args:
            max_words: Maximum words to recommend

        Returns:
            {
                "category": "business",
                "difficulty": "B2",
                "word_count": 50,
                "reason": "High priority category, CEFR gap",
                "details": {
                    "category_gap": 3350,
                    "cefr_gap_pct": -5.0,
                    "priority_score": 95
                }
            }
        """
        try:
            # Get gaps
            category_gaps = self.analyze_category_gaps()
            cefr_distribution = self.analyze_cefr_distribution()

            # Find biggest CEFR gap (most negative gap_pct)
            cefr_gaps_sorted = sorted(
                cefr_distribution.items(),
                key=lambda x: x[1]['gap_pct']
            )

            # Get top category gap
            if not category_gaps:
                return {
                    'category': None,
                    'difficulty': None,
                    'word_count': 0,
                    'reason': 'No gaps found',
                    'details': {}
                }

            top_category = category_gaps[0]

            # Get CEFR level that needs the most words
            target_difficulty = cefr_gaps_sorted[0][0] if cefr_gaps_sorted else 'B2'

            # Build recommendation
            recommendation = {
                'category': top_category['category'],
                'difficulty': target_difficulty,
                'word_count': min(max_words, top_category['gap_size']),
                'reason': self._build_reason(top_category, cefr_distribution.get(target_difficulty, {})),
                'details': {
                    'category_gap': top_category['gap_size'],
                    'category_priority': top_category['priority_score'],
                    'cefr_gap_pct': cefr_distribution.get(target_difficulty, {}).get('gap_pct', 0),
                    'is_priority_category': top_category['is_priority']
                }
            }

            logger.info(f"Recommended next batch: {recommendation['category']} ({recommendation['difficulty']}) - {recommendation['word_count']} words")
            return recommendation

        except Exception as e:
            logger.error(f"Failed to generate recommendation: {e}")
            return {
                'category': 'business',  # Fallback to default
                'difficulty': 'B2',
                'word_count': max_words,
                'reason': 'Default recommendation (error in analysis)',
                'details': {}
            }

    def _calculate_category_priority(self, category: str, gap_size: int, gap_percentage: float, is_priority: bool) -> int:
        """Calculate priority score for category"""
        priority = 50  # Base priority

        # Category bonus
        if is_priority:
            priority += 30

        # Gap size bonus (larger gaps = higher priority)
        priority += min(gap_size / 100, 20)  # Cap at 20 points

        # Gap percentage bonus
        if gap_percentage > 50:
            priority += 15

        return int(priority)

    def _build_reason(self, category_data: Dict, cefr_data: Dict) -> str:
        """Build human-readable reason for recommendation"""
        reasons = []

        if category_data.get('is_priority'):
            reasons.append("High priority category")

        if category_data.get('gap_size', 0) > 1000:
            reasons.append("Large category gap")

        if cefr_data.get('gap_pct', 0) < -3:
            reasons.append("CEFR distribution gap")

        return ", ".join(reasons) if reasons else "Smallest gap available"

    def get_gap_summary(self) -> str:
        """Get formatted gap summary for display"""
        category_gaps = self.analyze_category_gaps()
        cefr_distribution = self.analyze_cefr_distribution()

        lines = [
            "============================================================",
            "VOCABULARY GAP ANALYSIS",
            "============================================================",
            "",
            "📚 CATEGORY GAPS (Top 5):",
            ""
        ]

        # Show top 5 category gaps
        for i, gap in enumerate(category_gaps[:5], 1):
            priority_icon = "⭐" if gap['is_priority'] else "  "
            lines.append(
                f"{i}. {priority_icon} {gap['category'].replace('_', ' ').title()} [Priority: {gap['priority_score']}]"
            )
            lines.append(
                f"   Current: {gap['current_count']} words | Target: {gap['target_count']} | Gap: {gap['gap_size']}"
            )
            lines.append("")

        # Show CEFR distribution
        lines.append("📊 CEFR DISTRIBUTION:")
        lines.append("")

        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            data = cefr_distribution.get(level, {})
            current_pct = data.get('current_pct', 0)
            target_pct = data.get('target_pct', 0)
            gap_pct = data.get('gap_pct', 0)
            count = data.get('current_count', 0)

            # Visual bar
            bar_length = int(current_pct / 2)  # Scale to fit
            bar = '█' * bar_length

            gap_indicator = "⚠️" if gap_pct < -3 else "✓"
            lines.append(
                f"  {gap_indicator} {level}: {current_pct:5.1f}% (target: {target_pct}%) {bar} ({count} words)"
            )

        lines.append("")
        lines.append("============================================================")

        return "\n".join(lines)


if __name__ == "__main__":
    # Test gap analysis (requires database connection)
    logging.basicConfig(level=logging.INFO)

    import sys
    import os

    # Add backend to path
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, backend_dir)

    from app.database import SessionLocal
    from core.batch_config import BatchConfig

    # Load config
    config = BatchConfig.load()

    # Create database session
    db = SessionLocal()

    try:
        # Create analyzer
        analyzer = VocabularyGapAnalyzer(db, config)

        # Analyze gaps
        print(analyzer.get_gap_summary())

        # Get recommendation
        recommendation = analyzer.recommend_next_batch(50)
        print(f"\n📝 RECOMMENDATION:")
        print(f"   Category: {recommendation['category']}")
        print(f"   Difficulty: {recommendation['difficulty']}")
        print(f"   Word count: {recommendation['word_count']}")
        print(f"   Reason: {recommendation['reason']}")

    finally:
        db.close()
