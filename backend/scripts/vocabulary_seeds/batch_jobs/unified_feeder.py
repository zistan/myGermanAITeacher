"""
Unified Batch Feeder

Coordinate both vocabulary and grammar batch execution.
Provides single entry point for combined batch feeding.
"""

import time
import logging
from typing import Dict
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, backend_dir)

logger = logging.getLogger(__name__)


class UnifiedBatchFeeder:
    """Coordinate both vocabulary and grammar batch execution"""

    def __init__(self, db_session, config):
        """
        Initialize unified feeder

        Args:
            db_session: SQLAlchemy database session
            config: BatchConfig instance
        """
        self.db = db_session
        self.config = config

        # Import feeders
        from .vocabulary_feeder import VocabularyBatchFeeder
        from .grammar_feeder import GrammarBatchFeeder

        # Initialize feeders
        self.vocab_feeder = VocabularyBatchFeeder(db_session, config)
        self.grammar_feeder = GrammarBatchFeeder(db_session, config)

        logger.info("Initialized UnifiedBatchFeeder")

    def execute(self, mode: str = "both", force: bool = False) -> Dict:
        """
        Execute batch feeding

        Args:
            mode: "vocabulary" | "grammar" | "both"
            force: Bypass caps (use with caution)

        Returns:
            {
                "vocabulary": {...vocab results...},
                "grammar": {...grammar results...},
                "total_duration": 112.5
            }
        """
        start_time = time.time()

        logger.info(f"🚀 Starting unified batch execution (mode: {mode})")

        results = {}

        # Execute vocabulary batch
        if mode in ["vocabulary", "both"]:
            logger.info("\n" + "="*60)
            logger.info("📚 VOCABULARY BATCH")
            logger.info("="*60)

            try:
                vocab_result = self.vocab_feeder.execute(force=force)
                results['vocabulary'] = vocab_result

                # Log summary
                if vocab_result['status'] == 'completed':
                    vocab_results = vocab_result.get('results', {})
                    logger.info(f"✅ Vocabulary: {vocab_results.get('inserted', 0)} words inserted")
                elif vocab_result['status'] == 'skipped':
                    logger.info(f"⏭️  Vocabulary: {vocab_result.get('reason', 'Skipped')}")
                else:
                    logger.warning(f"❌ Vocabulary: {vocab_result.get('reason', 'Failed')}")

            except Exception as e:
                logger.error(f"❌ Vocabulary batch failed: {e}")
                results['vocabulary'] = {
                    'status': 'failed',
                    'reason': str(e),
                    'errors': [str(e)]
                }

        # Execute grammar batch
        if mode in ["grammar", "both"]:
            logger.info("\n" + "="*60)
            logger.info("✏️  GRAMMAR BATCH")
            logger.info("="*60)

            try:
                grammar_result = self.grammar_feeder.execute(force=force)
                results['grammar'] = grammar_result

                # Log summary
                if grammar_result['status'] == 'completed':
                    grammar_results = grammar_result.get('results', {})
                    logger.info(f"✅ Grammar: {grammar_results.get('exercises_inserted', 0)} exercises inserted")
                    if grammar_results.get('new_topics_created', 0) > 0:
                        logger.info(f"   🆕 Created {grammar_results['new_topics_created']} new topics")
                elif grammar_result['status'] == 'skipped':
                    logger.info(f"⏭️  Grammar: {grammar_result.get('reason', 'Skipped')}")
                else:
                    logger.warning(f"❌ Grammar: {grammar_result.get('reason', 'Failed')}")

            except Exception as e:
                logger.error(f"❌ Grammar batch failed: {e}")
                results['grammar'] = {
                    'status': 'failed',
                    'reason': str(e),
                    'errors': [str(e)]
                }

        # Calculate total duration
        total_duration = time.time() - start_time
        results['total_duration'] = round(total_duration, 2)

        logger.info("\n" + "="*60)
        logger.info(f"✅ Unified batch completed in {total_duration:.1f}s")
        logger.info("="*60)

        return results

    def get_summary(self) -> str:
        """Get formatted execution summary"""
        from ..core.batch_tracker import BatchExecutionTracker

        tracker = BatchExecutionTracker(
            self.config.execution_log_path,
            self.config.history_retention_days
        )

        summary = tracker.get_execution_summary()

        lines = [
            "============================================================",
            "UNIFIED BATCH FEEDER SUMMARY",
            "============================================================",
            "",
            f"📚 VOCABULARY:",
            f"   Total executions: {summary['vocabulary']['total_executions']}",
            f"   Successful: {summary['vocabulary']['successful']}",
            f"   Words generated: {summary['vocabulary']['total_words_generated']:,}",
            "",
            f"✏️  GRAMMAR:",
            f"   Total executions: {summary['grammar']['total_executions']}",
            f"   Successful: {summary['grammar']['successful']}",
            f"   Exercises generated: {summary['grammar']['total_exercises_generated']:,}",
            "",
            f"📅 TODAY:",
            f"   Words: {summary['daily_totals']['words']}",
            f"   Exercises: {summary['daily_totals']['exercises']}",
            "",
            f"📆 THIS WEEK:",
            f"   Words: {summary['weekly_totals']['words']}",
            f"   Exercises: {summary['weekly_totals']['exercises']}",
            "",
            "============================================================"
        ]

        return "\n".join(lines)


if __name__ == "__main__":
    # Test unified feeder
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from app.database import SessionLocal
    from ..core.batch_config import BatchConfig

    # Load config
    config = BatchConfig.load()

    # Create database session
    db = SessionLocal()

    try:
        # Create unified feeder
        feeder = UnifiedBatchFeeder(db, config)

        # Execute both batches
        results = feeder.execute(mode="both", force=False)

        # Print summary
        print("\n" + feeder.get_summary())

        # Print detailed results
        print("\n" + "=" * 60)
        print("DETAILED RESULTS")
        print("=" * 60)

        if 'vocabulary' in results:
            print("\n📚 VOCABULARY:")
            vocab = results['vocabulary']
            print(f"   Status: {vocab.get('status', 'N/A')}")
            if vocab.get('status') == 'completed':
                vocab_results = vocab.get('results', {})
                print(f"   Generated: {vocab_results.get('generated', 0)}")
                print(f"   Inserted: {vocab_results.get('inserted', 0)}")
                print(f"   Duration: {vocab_results.get('duration_seconds', 0):.1f}s")

        if 'grammar' in results:
            print("\n✏️  GRAMMAR:")
            grammar = results['grammar']
            print(f"   Status: {grammar.get('status', 'N/A')}")
            if grammar.get('status') == 'completed':
                grammar_results = grammar.get('results', {})
                print(f"   Exercises: {grammar_results.get('exercises_inserted', 0)}")
                print(f"   New Topics: {grammar_results.get('new_topics_created', 0)}")
                print(f"   Duration: {grammar_results.get('duration_seconds', 0):.1f}s")

        print(f"\n⏱️  Total Duration: {results.get('total_duration', 0):.1f}s")
        print("=" * 60)

    finally:
        db.close()
