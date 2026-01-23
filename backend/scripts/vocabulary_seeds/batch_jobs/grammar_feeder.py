"""
Grammar Batch Feeder

Execute grammar exercise batch generation AND new topic creation.
Orchestrates gap analysis, exercise generation, deduplication, and database insertion.
"""

import time
import logging
from datetime import datetime
from typing import Dict, List
import sys
import os

# Add backend to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, backend_dir)

logger = logging.getLogger(__name__)


class GrammarBatchFeeder:
    """Execute grammar exercise batch generation and topic creation"""

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
        from scripts.vocabulary_seeds.gap_analysis.grammar_gaps import GrammarGapAnalyzer
        from scripts.vocabulary_seeds.core.deduplicator import GrammarDeduplicator
        from scripts.vocabulary_seeds.gap_analysis.grammar_topic_generator import GrammarTopicGenerator
        from app.services.grammar_ai_service import GrammarAIService
        from app.models.grammar import GrammarTopic, GrammarExercise

        # Initialize components
        self.tracker = BatchExecutionTracker(
            config.execution_log_path,
            config.history_retention_days
        )
        self.gap_analyzer = GrammarGapAnalyzer(db_session, config)
        self.deduplicator = GrammarDeduplicator(
            db_session,
            config.vocab_similarity_threshold  # Use vocab threshold for now
        )
        self.grammar_ai_service = GrammarAIService()
        self.topic_generator = GrammarTopicGenerator(self.grammar_ai_service)

        # Store model references
        self.GrammarTopic = GrammarTopic
        self.GrammarExercise = GrammarExercise

        logger.info("Initialized GrammarBatchFeeder")

    def execute(self, force: bool = False) -> Dict:
        """
        Main execution method

        Args:
            force: Bypass caps (use with caution)

        Returns:
            {
                "status": "completed" | "skipped" | "failed",
                "action": "fill_exercises" | "create_topic",
                "topics_processed": [topic1, topic2],
                "new_topics_created": 0,
                "exercises_generated": 22,
                "exercises_inserted": 20,
                "skipped_duplicates": 2,
                "ai_calls": 5,
                "duration_seconds": 67.3,
                "errors": []
            }
        """
        start_time = time.time()
        execution_id = f"grammar_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"🚀 Starting grammar batch execution: {execution_id}")

        try:
            # Step 1: Check caps
            if not force:
                can_execute, reason = self._check_caps(self.config.grammar_max_per_run)
                if not can_execute:
                    result = {
                        "execution_id": execution_id,
                        "status": "skipped",
                        "reason": reason,
                        "action": None,
                        "topics_processed": [],
                        "new_topics_created": 0,
                        "exercises_generated": 0,
                        "exercises_inserted": 0,
                        "skipped_duplicates": 0,
                        "ai_calls": 0,
                        "duration_seconds": 0,
                        "errors": []
                    }
                    logger.warning(f"⏭️  Batch skipped: {reason}")
                    return result

            # Step 2: Decide action (fill exercises or create topic)
            logger.info("📊 Analyzing gaps and deciding action...")
            action_plan = self._decide_action()

            if not action_plan.get('action'):
                result = {
                    "execution_id": execution_id,
                    "status": "skipped",
                    "reason": "No gaps found",
                    "action": None,
                    "topics_processed": [],
                    "new_topics_created": 0,
                    "exercises_generated": 0,
                    "exercises_inserted": 0,
                    "skipped_duplicates": 0,
                    "ai_calls": 0,
                    "duration_seconds": time.time() - start_time,
                    "errors": []
                }
                logger.info("✅ No gaps found, all targets met")
                return result

            logger.info(f"📝 Action: {action_plan['action']}")

            # Step 3: Execute action
            if action_plan['action'] == 'fill_exercises':
                result = self._fill_exercises_for_topics(
                    action_plan['targets'],
                    execution_id,
                    start_time
                )
            elif action_plan['action'] == 'create_topic':
                result = self._create_new_topics(
                    action_plan['targets'],
                    execution_id,
                    start_time
                )
            else:
                raise ValueError(f"Unknown action: {action_plan['action']}")

            # Step 4: Log execution
            self.tracker.log_execution(result)

            duration = time.time() - start_time
            logger.info(f"✅ Grammar batch completed in {duration:.1f}s")

            return result

        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"❌ Grammar batch failed: {e}", exc_info=True)

            result = {
                "execution_id": execution_id,
                "type": "grammar",
                "status": "failed",
                "reason": f"Exception: {str(e)}",
                "results": {
                    "exercises_generated": 0,
                    "exercises_inserted": 0,
                    "skipped_duplicates": 0,
                    "new_topics_created": 0,
                    "ai_calls": 0,
                    "duration_seconds": round(duration, 2),
                    "errors": [str(e)]
                }
            }

            try:
                self.tracker.log_execution(result)
            except:
                pass

            return result

    def _check_caps(self, requested_count: int) -> tuple:
        """Check if batch can proceed"""
        return self.tracker.can_execute_grammar(
            requested_count=requested_count,
            daily_cap=self.config.daily_cap_exercises,
            weekly_cap=self.config.weekly_cap_exercises,
            global_cap=self.config.grammar_max_total
        )

    def _decide_action(self) -> Dict:
        """
        Decide whether to fill exercises or create new topic

        Returns:
            {
                "action": "fill_exercises" | "create_topic",
                "targets": [recommended topics/topic specs]
            }
        """
        # Get recommendations
        recommendations = self.gap_analyzer.recommend_next_topics(
            max_topics=self.config.grammar_max_new_topics
        )

        if not recommendations:
            return {'action': None, 'targets': []}

        # Check first recommendation
        first_rec = recommendations[0]

        if first_rec['action'] == 'fill_exercises':
            # Fill exercises for incomplete topics
            return {
                'action': 'fill_exercises',
                'targets': [r for r in recommendations if r['action'] == 'fill_exercises']
            }
        else:
            # Create new topics
            return {
                'action': 'create_topic',
                'targets': [r for r in recommendations if r['action'] == 'create_topic']
            }

    def _fill_exercises_for_topics(self, topics: List[Dict], execution_id: str, start_time: float) -> Dict:
        """Generate exercises for incomplete topics"""
        logger.info(f"📝 Filling exercises for {len(topics)} topics...")

        total_generated = 0
        total_inserted = 0
        total_skipped = 0
        total_ai_calls = 0
        errors = []
        topics_processed = []

        for topic_data in topics:
            try:
                topic_id = topic_data['topic_id']
                exercises_needed = min(
                    topic_data['exercises_needed'],
                    self.config.grammar_max_per_run - total_generated
                )

                if exercises_needed <= 0:
                    break  # Reached batch limit

                logger.info(f"   Topic: {topic_data['topic_name']} - generating {exercises_needed} exercises")

                # Generate exercises
                exercises = self._generate_exercises_for_topic(
                    topic_id=topic_id,
                    topic_data=topic_data,
                    count=exercises_needed
                )

                total_ai_calls += len(topic_data.get('missing_types', [])) or 1

                # Filter and insert
                inserted, skipped = self._filter_and_insert_exercises(
                    exercises,
                    topic_id
                )

                total_generated += len(exercises)
                total_inserted += inserted
                total_skipped += skipped

                topics_processed.append({
                    'topic_id': topic_id,
                    'topic_name': topic_data['topic_name'],
                    'exercises_generated': len(exercises),
                    'exercises_inserted': inserted
                })

                logger.info(f"   ✅ Inserted {inserted}, skipped {skipped}")

            except Exception as e:
                logger.error(f"   ❌ Failed to process topic {topic_data.get('topic_name')}: {e}")
                errors.append(f"Topic {topic_data.get('topic_name')}: {str(e)}")
                continue

        duration = time.time() - start_time

        return {
            "execution_id": execution_id,
            "type": "grammar",
            "status": "completed" if total_inserted > 0 else "failed",
            "reason": "Success" if not errors else f"Partial success ({len(errors)} errors)",
            "action": "fill_exercises",
            "config_snapshot": {
                "max_exercises": self.config.grammar_max_per_run,
                "target_per_topic": self.config.grammar_target_per_topic,
            },
            "results": {
                "topics_processed": topics_processed,
                "new_topics_created": 0,
                "exercises_generated": total_generated,
                "exercises_inserted": total_inserted,
                "skipped_duplicates": total_skipped,
                "ai_calls": total_ai_calls,
                "duration_seconds": round(duration, 2),
                "errors": errors
            }
        }

    def _create_new_topics(self, topic_specs: List[Dict], execution_id: str, start_time: float) -> Dict:
        """Create new topics with initial exercises"""
        logger.info(f"🆕 Creating {len(topic_specs)} new topics...")

        topics_created = 0
        total_exercises_generated = 0
        total_exercises_inserted = 0
        total_ai_calls = 0
        errors = []
        topics_processed = []

        for spec in topic_specs[:self.config.grammar_max_new_topics]:
            try:
                topic_name = spec['topic_name']
                logger.info(f"   Creating topic: {topic_name}")

                # Generate topic metadata using AI
                topic_metadata = self.topic_generator.generate_topic_metadata(topic_name)
                total_ai_calls += 1

                # Create topic in database
                topic = self.GrammarTopic(
                    name_de=topic_metadata.get('name_de', topic_name),
                    name_en=topic_metadata.get('name_en', topic_name),
                    category=topic_metadata.get('category', 'other'),
                    difficulty_level=topic_metadata.get('difficulty_level', 'B1'),
                    description_de=topic_metadata.get('description_de', ''),
                    explanation_de=topic_metadata.get('explanation_de', ''),
                    order_index=topic_metadata.get('order_index', 999),
                    parent_topic_id=topic_metadata.get('parent_topic_id')
                )

                self.db.add(topic)
                self.db.flush()  # Get topic ID

                logger.info(f"   ✅ Topic created with ID: {topic.id}")
                topics_created += 1

                # Generate initial exercises (20 exercises)
                initial_exercise_count = 20
                logger.info(f"   Generating {initial_exercise_count} initial exercises...")

                topic_data_for_generation = {
                    'topic_id': topic.id,
                    'topic_name': topic.name_en,
                    'difficulty': topic.difficulty_level,
                    'exercises_needed': initial_exercise_count,
                    'missing_types': []  # Will generate mixed types
                }

                exercises = self._generate_exercises_for_topic(
                    topic_id=topic.id,
                    topic_data=topic_data_for_generation,
                    count=initial_exercise_count
                )

                total_ai_calls += 4  # Estimate 4 calls for mixed types

                # Insert exercises
                inserted, skipped = self._filter_and_insert_exercises(
                    exercises,
                    topic.id
                )

                total_exercises_generated += len(exercises)
                total_exercises_inserted += inserted

                topics_processed.append({
                    'topic_id': topic.id,
                    'topic_name': topic.name_en,
                    'exercises_generated': len(exercises),
                    'exercises_inserted': inserted
                })

                logger.info(f"   ✅ Inserted {inserted} exercises for new topic")

                # Commit topic and exercises
                self.db.commit()

            except Exception as e:
                logger.error(f"   ❌ Failed to create topic {spec.get('topic_name')}: {e}")
                errors.append(f"Topic {spec.get('topic_name')}: {str(e)}")
                self.db.rollback()
                continue

        duration = time.time() - start_time

        return {
            "execution_id": execution_id,
            "type": "grammar",
            "status": "completed" if topics_created > 0 else "failed",
            "reason": "Success" if not errors else f"Partial success ({len(errors)} errors)",
            "action": "create_topic",
            "config_snapshot": {
                "max_new_topics": self.config.grammar_max_new_topics,
            },
            "results": {
                "topics_processed": topics_processed,
                "new_topics_created": topics_created,
                "exercises_generated": total_exercises_generated,
                "exercises_inserted": total_exercises_inserted,
                "skipped_duplicates": 0,
                "ai_calls": total_ai_calls,
                "duration_seconds": round(duration, 2),
                "errors": errors
            }
        }

    def _generate_exercises_for_topic(self, topic_id: int, topic_data: Dict, count: int) -> List[Dict]:
        """Use GrammarAIService to generate exercises"""
        try:
            # Get topic from database
            topic = self.db.query(self.GrammarTopic).filter_by(id=topic_id).first()

            if not topic:
                logger.error(f"Topic {topic_id} not found")
                return []

            # Determine exercise types to generate
            missing_types = topic_data.get('missing_types', [])
            if missing_types:
                # Generate missing types
                types_to_generate = missing_types
            else:
                # Generate mixed types
                types_to_generate = ['fill_blank', 'multiple_choice', 'translation', 'error_correction']

            # Distribute count across types
            exercises_per_type = max(1, count // len(types_to_generate))
            all_exercises = []

            for exercise_type in types_to_generate:
                try:
                    batch = self.grammar_ai_service.generate_exercises(
                        topic_name=topic.name_de,
                        topic_explanation=topic.explanation_de or "",
                        difficulty_level=topic.difficulty_level,
                        exercise_type=exercise_type,
                        count=exercises_per_type
                    )

                    # Add topic_id to each exercise
                    for ex in batch:
                        ex['topic_id'] = topic_id

                    all_exercises.extend(batch)

                except Exception as e:
                    logger.error(f"Failed to generate {exercise_type} exercises: {e}")
                    continue

            return all_exercises[:count]  # Trim to exact count

        except Exception as e:
            logger.error(f"Exercise generation failed: {e}")
            return []

    def _filter_and_insert_exercises(self, exercises: List[Dict], topic_id: int) -> tuple:
        """Deduplicate and insert exercises"""
        if not exercises:
            return 0, 0

        try:
            # Check duplicates if enabled
            if self.config.grammar_check_duplicates:
                unique_exercises, duplicate_exercises = self.deduplicator.filter_duplicate_exercises(
                    exercises,
                    topic_id=topic_id
                )
            else:
                unique_exercises = exercises
                duplicate_exercises = []

            # Insert exercises
            inserted = 0
            for exercise_data in unique_exercises:
                try:
                    exercise = self.GrammarExercise(**exercise_data)
                    self.db.add(exercise)
                    inserted += 1
                except Exception as e:
                    logger.error(f"Failed to insert exercise: {e}")
                    continue

            self.db.commit()

            return inserted, len(duplicate_exercises)

        except Exception as e:
            logger.error(f"Exercise insertion failed: {e}")
            self.db.rollback()
            return 0, 0


if __name__ == "__main__":
    # Test grammar feeder
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
        feeder = GrammarBatchFeeder(db, config)

        # Execute batch
        result = feeder.execute(force=False)

        # Print result
        print("\n" + "=" * 60)
        print("EXECUTION RESULT")
        print("=" * 60)
        print(f"Status: {result['status']}")
        print(f"Action: {result.get('action', 'N/A')}")
        if result['status'] == 'completed':
            results = result.get('results', {})
            print(f"Exercises Generated: {results.get('exercises_generated', 0)}")
            print(f"Exercises Inserted: {results.get('exercises_inserted', 0)}")
            print(f"New Topics: {results.get('new_topics_created', 0)}")
            print(f"AI Calls: {results.get('ai_calls', 0)}")
            print(f"Duration: {results.get('duration_seconds', 0):.1f}s")
        print("=" * 60)

    finally:
        db.close()
