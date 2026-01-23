"""
Vocabulary Batch Feeder

Execute vocabulary batch generation workflow.
Orchestrates gap analysis, deduplication, AI generation, and database insertion.
"""

import time
import logging
from datetime import datetime
from typing import Dict, List, Set
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, backend_dir)

logger = logging.getLogger(__name__)


class VocabularyBatchFeeder:
    """Execute vocabulary batch generation workflow"""

    def __init__(self, db_session, config):
        """
        Initialize feeder

        Args:
            db_session: SQLAlchemy database session
            config: BatchConfig instance
        """
        self.db = db_session
        self.config = config

        # Import components (absolute imports since script is run directly)
        from scripts.vocabulary_seeds.core.batch_tracker import BatchExecutionTracker
        from scripts.vocabulary_seeds.gap_analysis.vocabulary_gaps import VocabularyGapAnalyzer
        from scripts.vocabulary_seeds.core.deduplicator import VocabularyDeduplicator
        from scripts.vocabulary_seeds.core.ai_generator import VocabularyGenerator
        from scripts.vocabulary_seeds.core.validation import VocabularyValidator
        from scripts.vocabulary_seeds.core.bulk_insert import VocabularyInserter

        # Initialize components
        self.tracker = BatchExecutionTracker(
            config.execution_log_path,
            config.history_retention_days
        )
        self.gap_analyzer = VocabularyGapAnalyzer(db_session, config)
        self.deduplicator = VocabularyDeduplicator(
            db_session,
            config.vocab_similarity_threshold
        )
        self.ai_generator = VocabularyGenerator(
            api_key=config.anthropic_api_key,
            verbose=False
        )
        self.validator = VocabularyValidator(verbose=False)
        self.inserter = VocabularyInserter(db_session, dry_run=False)

        logger.info("Initialized VocabularyBatchFeeder")

    def execute(self, force: bool = False) -> Dict:
        """
        Main execution method

        Args:
            force: Bypass caps (use with caution)

        Returns:
            {
                "status": "completed" | "skipped" | "failed",
                "reason": "explanation",
                "generated": 48,
                "inserted": 45,
                "skipped_duplicates": 3,
                "ai_calls": 2,
                "duration_seconds": 45.2,
                "errors": []
            }
        """
        start_time = time.time()
        execution_id = f"vocab_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"🚀 Starting vocabulary batch execution: {execution_id}")

        try:
            # Step 1: Check caps
            if not force:
                can_execute, reason = self._check_caps(self.config.vocab_max_per_run)
                if not can_execute:
                    result = {
                        "execution_id": execution_id,
                        "status": "skipped",
                        "reason": reason,
                        "generated": 0,
                        "inserted": 0,
                        "skipped_duplicates": 0,
                        "ai_calls": 0,
                        "duration_seconds": 0,
                        "errors": []
                    }
                    logger.warning(f"⏭️  Batch skipped: {reason}")
                    return result

            # Step 2: Get recommendation from gap analysis
            logger.info("📊 Analyzing gaps...")
            recommendation = self.gap_analyzer.recommend_next_batch(
                self.config.vocab_max_per_run
            )

            if not recommendation.get('category'):
                result = {
                    "execution_id": execution_id,
                    "status": "skipped",
                    "reason": "No gaps found",
                    "generated": 0,
                    "inserted": 0,
                    "skipped_duplicates": 0,
                    "ai_calls": 0,
                    "duration_seconds": time.time() - start_time,
                    "errors": []
                }
                logger.info("✅ No gaps found, all targets met")
                return result

            logger.info(f"📝 Recommendation: {recommendation['category']} ({recommendation['difficulty']}) - {recommendation['word_count']} words")

            # Step 3: Query existing words for deduplication
            if self.config.vocab_check_existing:
                logger.info("🔍 Loading existing words for deduplication...")
                existing_words = self._query_existing_words(
                    recommendation['category'],
                    recommendation['difficulty']
                )
                logger.info(f"   Found {len(existing_words)} existing words")
            else:
                existing_words = set()
                logger.info("⏭️  Skipping deduplication check (disabled in config)")

            # Step 4: Generate vocabulary using AI
            logger.info("🤖 Generating vocabulary with AI...")
            generated_words = self._generate_vocabulary(recommendation)

            if not generated_words:
                result = {
                    "execution_id": execution_id,
                    "status": "failed",
                    "reason": "AI generation failed",
                    "generated": 0,
                    "inserted": 0,
                    "skipped_duplicates": 0,
                    "ai_calls": 1,
                    "duration_seconds": time.time() - start_time,
                    "errors": ["AI generation returned no words"]
                }
                logger.error("❌ AI generation failed")
                return result

            # Calculate AI calls (chunking logic)
            chunk_size = self.config.vocab_chunk_size
            ai_calls = max(1, (len(generated_words) + chunk_size - 1) // chunk_size)

            logger.info(f"✅ Generated {len(generated_words)} words ({ai_calls} AI calls)")

            # Step 5: Filter and validate
            logger.info("🔍 Filtering duplicates and validating...")
            unique_words, duplicate_words = self._filter_and_validate(
                generated_words,
                existing_words
            )

            logger.info(f"   Unique: {len(unique_words)}, Duplicates: {len(duplicate_words)}")

            # Step 6: Insert words into database
            if unique_words:
                logger.info("💾 Inserting words into database...")
                inserted_count = self._insert_words(unique_words)
                logger.info(f"✅ Inserted {inserted_count} words")
            else:
                inserted_count = 0
                logger.warning("⚠️  No unique words to insert")

            # Step 7: Log execution
            duration = time.time() - start_time

            result = {
                "execution_id": execution_id,
                "type": "vocabulary",
                "status": "completed",
                "reason": "Success",
                "config_snapshot": {
                    "category": recommendation['category'],
                    "difficulty": recommendation['difficulty'],
                    "max_words": self.config.vocab_max_per_run,
                },
                "results": {
                    "generated": len(generated_words),
                    "inserted": inserted_count,
                    "skipped_duplicates": len(duplicate_words),
                    "ai_calls": ai_calls,
                    "duration_seconds": round(duration, 2),
                    "errors": []
                }
            }

            self.tracker.log_execution(result)

            logger.info(f"✅ Vocabulary batch completed in {duration:.1f}s")
            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ Vocabulary batch failed: {e}", exc_info=True)

            result = {
                "execution_id": execution_id,
                "type": "vocabulary",
                "status": "failed",
                "reason": f"Exception: {str(e)}",
                "results": {
                    "generated": 0,
                    "inserted": 0,
                    "skipped_duplicates": 0,
                    "ai_calls": 0,
                    "duration_seconds": round(duration, 2),
                    "errors": [str(e)]
                }
            }

            try:
                self.tracker.log_execution(result)
            except:
                pass  # Don't fail if logging fails

            return result

    def _check_caps(self, requested_count: int) -> tuple:
        """Check if batch can proceed (daily/weekly/global caps)"""
        return self.tracker.can_execute_vocabulary(
            requested_count=requested_count,
            daily_cap=self.config.daily_cap_words,
            weekly_cap=self.config.weekly_cap_words,
            global_cap=self.config.vocab_max_total
        )

    def _query_existing_words(self, category: str, difficulty: str) -> Set[str]:
        """Get existing words for deduplication"""
        return self.deduplicator.get_existing_words(
            category=category,
            difficulty=difficulty
        )

    def _generate_vocabulary(self, recommendation: Dict) -> List[Dict]:
        """Call AI to generate vocabulary (with chunking, rate limiting)"""
        try:
            # Map recommendation to generator parameters
            words = self.ai_generator.generate_vocabulary(
                category=recommendation['category'],
                subcategory=recommendation['category'],  # Use category as subcategory
                count=recommendation['word_count'],
                difficulty=recommendation['difficulty'],
                context="",
                auto_chunk=True,
                chunk_size=self.config.vocab_chunk_size
            )

            return words

        except Exception as e:
            logger.error(f"AI generation failed: {e}")
            return []

    def _filter_and_validate(self, words: List[Dict], existing: Set[str]) -> tuple:
        """Deduplicate and validate"""
        # Extract word strings from dictionaries
        word_strings = [w.get('word', w.get('word_de', '')) for w in words]

        # Filter duplicates
        unique_strings, duplicate_strings = self.deduplicator.filter_duplicates(
            word_strings,
            existing
        )

        # Filter original word dicts based on unique strings
        unique_strings_set = set(unique_strings)
        unique_words = [
            w for w in words
            if (w.get('word', w.get('word_de', '')) in unique_strings_set)
        ]
        duplicate_words = [
            w for w in words
            if (w.get('word', w.get('word_de', '')) not in unique_strings_set)
        ]

        return unique_words, duplicate_words

    def _insert_words(self, words: List[Dict]) -> int:
        """Bulk insert to database"""
        try:
            # Use existing bulk inserter
            result = self.inserter.insert_words(words)
            return result.get('inserted', 0)

        except Exception as e:
            logger.error(f"Database insertion failed: {e}")
            # Fallback: Try manual insertion
            try:
                from app.models.vocabulary import Vocabulary

                inserted = 0
                for word_data in words:
                    try:
                        # Create Vocabulary instance
                        vocab = Vocabulary(**word_data)
                        self.db.add(vocab)
                        inserted += 1
                    except Exception as word_error:
                        logger.error(f"Failed to insert word: {word_error}")
                        continue

                self.db.commit()
                logger.info(f"✅ Manual insertion: {inserted} words")
                return inserted

            except Exception as fallback_error:
                logger.error(f"Manual insertion also failed: {fallback_error}")
                self.db.rollback()
                return 0


if __name__ == "__main__":
    # Test vocabulary feeder
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    from app.database import SessionLocal
    from scripts.vocabulary_seeds.core.batch_config import BatchConfig

    # Load config
    config = BatchConfig.load()

    # Create database session
    db = SessionLocal()

    try:
        # Create feeder
        feeder = VocabularyBatchFeeder(db, config)

        # Execute batch
        result = feeder.execute(force=False)

        # Print result
        print("\n" + "=" * 60)
        print("EXECUTION RESULT")
        print("=" * 60)
        print(f"Status: {result['status']}")
        print(f"Reason: {result['reason']}")
        if result['status'] == 'completed':
            results = result.get('results', {})
            print(f"Generated: {results.get('generated', 0)}")
            print(f"Inserted: {results.get('inserted', 0)}")
            print(f"Skipped: {results.get('skipped_duplicates', 0)}")
            print(f"AI Calls: {results.get('ai_calls', 0)}")
            print(f"Duration: {results.get('duration_seconds', 0):.1f}s")
        print("=" * 60)

    finally:
        db.close()
