"""
Batch Configuration Manager

Centralized configuration management for batch feeding system.
Reads directly from .env file using python-dotenv.
"""

import os
from dataclasses import dataclass
from typing import Dict, Optional
from dotenv import load_dotenv
import logging

logger = logging.getLogger(__name__)


@dataclass
class BatchConfig:
    """Type-safe configuration for batch feeding system"""

    # Database
    database_url: str

    # API Keys
    anthropic_api_key: str

    # Vocabulary Limits
    vocab_max_per_run: int
    vocab_max_total: int
    vocab_chunk_size: int

    # Grammar Limits
    grammar_max_per_run: int
    grammar_max_total: int
    grammar_target_per_topic: int
    grammar_max_new_topics: int

    # AI Rate Limiting
    ai_calls_per_minute: int
    ai_retry_delay_seconds: int
    ai_max_retries: int

    # Daily/Weekly Caps
    daily_cap_words: int
    daily_cap_exercises: int
    weekly_cap_words: int
    weekly_cap_exercises: int

    # Deduplication
    vocab_check_existing: bool
    vocab_similarity_threshold: float
    grammar_check_duplicates: bool

    # Execution Tracking
    execution_log_path: str
    history_retention_days: int

    # Content Priority
    vocab_priority_categories: list
    cefr_distribution: Dict[str, int]  # {"A1": 5, "A2": 10, ...}
    grammar_priority_categories: list
    grammar_missing_topics: list

    @staticmethod
    def load(env_path: Optional[str] = None) -> 'BatchConfig':
        """
        Load configuration from .env file with validation

        Args:
            env_path: Optional path to .env file (defaults to backend/.env)

        Returns:
            BatchConfig instance

        Raises:
            ValueError: If required config is missing or invalid
        """
        # Load .env file
        if env_path is None:
            # Default to backend/.env
            # Path: backend/scripts/vocabulary_seeds/core/batch_config.py -> backend/
            # Need 4 levels up: core -> vocabulary_seeds -> scripts -> backend
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            env_path = os.path.join(backend_dir, '.env')

        if not os.path.exists(env_path):
            logger.warning(f".env file not found at {env_path}, using environment variables only")
        else:
            load_dotenv(env_path)

        # Parse CEFR distribution
        cefr_dist_str = os.getenv('BATCH_VOCAB_CEFR_DISTRIBUTION', 'A1:5,A2:10,B1:20,B2:30,C1:25,C2:10')
        cefr_distribution = {}
        for pair in cefr_dist_str.split(','):
            level, percentage = pair.split(':')
            cefr_distribution[level.strip()] = int(percentage.strip())

        # Validate CEFR distribution sums to 100
        total_percentage = sum(cefr_distribution.values())
        if total_percentage != 100:
            logger.warning(f"CEFR distribution sums to {total_percentage}%, not 100%. Adjusting...")

        # Parse priority categories
        vocab_priority = os.getenv('BATCH_VOCAB_PRIORITY_CATEGORIES', 'business,cefr_core')
        vocab_priority_list = [cat.strip() for cat in vocab_priority.split(',') if cat.strip()]

        grammar_priority = os.getenv('BATCH_GRAMMAR_PRIORITY_CATEGORIES', 'cases,verbs,tenses')
        grammar_priority_list = [cat.strip() for cat in grammar_priority.split(',') if cat.strip()]

        grammar_missing = os.getenv('BATCH_GRAMMAR_MISSING_TOPICS', 'subjunctive,passive_voice,indirect_speech')
        grammar_missing_list = [topic.strip() for topic in grammar_missing.split(',') if topic.strip()]

        # Create config instance
        config = BatchConfig(
            # Database
            database_url=os.getenv('DATABASE_URL', ''),

            # API Keys
            anthropic_api_key=os.getenv('ANTHROPIC_API_KEY', ''),

            # Vocabulary Limits
            vocab_max_per_run=int(os.getenv('BATCH_VOCAB_MAX_WORDS_PER_RUN', '50')),
            vocab_max_total=int(os.getenv('BATCH_VOCAB_MAX_WORDS_TOTAL', '25000')),
            vocab_chunk_size=int(os.getenv('BATCH_VOCAB_CHUNK_SIZE', '40')),

            # Grammar Limits
            grammar_max_per_run=int(os.getenv('BATCH_GRAMMAR_MAX_EXERCISES_PER_RUN', '25')),
            grammar_max_total=int(os.getenv('BATCH_GRAMMAR_MAX_EXERCISES_TOTAL', '5000')),
            grammar_target_per_topic=int(os.getenv('BATCH_GRAMMAR_TARGET_PER_TOPIC', '50')),
            grammar_max_new_topics=int(os.getenv('BATCH_GRAMMAR_MAX_NEW_TOPICS_PER_RUN', '2')),

            # AI Rate Limiting
            ai_calls_per_minute=int(os.getenv('BATCH_AI_CALLS_PER_MINUTE', '20')),
            ai_retry_delay_seconds=int(os.getenv('BATCH_AI_RETRY_DELAY_SECONDS', '5')),
            ai_max_retries=int(os.getenv('BATCH_AI_MAX_RETRIES', '3')),

            # Daily/Weekly Caps
            daily_cap_words=int(os.getenv('BATCH_DAILY_CAP_WORDS', '50')),
            daily_cap_exercises=int(os.getenv('BATCH_DAILY_CAP_EXERCISES', '25')),
            weekly_cap_words=int(os.getenv('BATCH_WEEKLY_CAP_WORDS', '200')),
            weekly_cap_exercises=int(os.getenv('BATCH_WEEKLY_CAP_EXERCISES', '100')),

            # Deduplication
            vocab_check_existing=os.getenv('BATCH_VOCAB_CHECK_EXISTING', 'true').lower() == 'true',
            vocab_similarity_threshold=float(os.getenv('BATCH_VOCAB_SIMILARITY_THRESHOLD', '0.85')),
            grammar_check_duplicates=os.getenv('BATCH_GRAMMAR_CHECK_DUPLICATES', 'true').lower() == 'true',

            # Execution Tracking
            execution_log_path=os.path.join(
                backend_dir,
                os.getenv('BATCH_EXECUTION_LOG_PATH', 'logs/batch_execution.json')
            ),
            history_retention_days=int(os.getenv('BATCH_HISTORY_RETENTION_DAYS', '90')),

            # Content Priority
            vocab_priority_categories=vocab_priority_list,
            cefr_distribution=cefr_distribution,
            grammar_priority_categories=grammar_priority_list,
            grammar_missing_topics=grammar_missing_list,
        )

        # Validate configuration
        config._validate()

        return config

    def _validate(self):
        """Validate configuration values"""
        errors = []

        # Check required fields
        if not self.database_url:
            errors.append("DATABASE_URL is required")

        if not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required")

        # Check positive integers
        if self.vocab_max_per_run <= 0:
            errors.append("BATCH_VOCAB_MAX_WORDS_PER_RUN must be positive")

        if self.grammar_max_per_run <= 0:
            errors.append("BATCH_GRAMMAR_MAX_EXERCISES_PER_RUN must be positive")

        if self.vocab_chunk_size <= 0 or self.vocab_chunk_size > self.vocab_max_per_run:
            errors.append("BATCH_VOCAB_CHUNK_SIZE must be positive and <= max_per_run")

        # Check similarity threshold
        if not 0.0 <= self.vocab_similarity_threshold <= 1.0:
            errors.append("BATCH_VOCAB_SIMILARITY_THRESHOLD must be between 0.0 and 1.0")

        # Check caps make sense
        if self.daily_cap_words > self.weekly_cap_words:
            errors.append("Daily word cap cannot exceed weekly cap")

        if self.daily_cap_exercises > self.weekly_cap_exercises:
            errors.append("Daily exercise cap cannot exceed weekly cap")

        if errors:
            raise ValueError(f"Configuration validation failed:\n" + "\n".join(f"  - {err}" for err in errors))

        logger.info("✅ Configuration loaded and validated successfully")

    def get_summary(self) -> str:
        """Get human-readable configuration summary"""
        return f"""
============================================================
BATCH FEEDING CONFIGURATION
============================================================

📚 VOCABULARY LIMITS:
  Max per run: {self.vocab_max_per_run} words
  Max total: {self.vocab_max_total:,} words
  Chunk size: {self.vocab_chunk_size} words/call

✏️  GRAMMAR LIMITS:
  Max per run: {self.grammar_max_per_run} exercises
  Max total: {self.grammar_max_total:,} exercises
  Target per topic: {self.grammar_target_per_topic} exercises
  Max new topics: {self.grammar_max_new_topics} topics/run

📅 DAILY/WEEKLY CAPS:
  Daily words: {self.daily_cap_words}
  Daily exercises: {self.daily_cap_exercises}
  Weekly words: {self.weekly_cap_words}
  Weekly exercises: {self.weekly_cap_exercises}

🤖 AI RATE LIMITING:
  Calls per minute: {self.ai_calls_per_minute}
  Retry delay: {self.ai_retry_delay_seconds}s
  Max retries: {self.ai_max_retries}

🔍 DEDUPLICATION:
  Check existing vocabulary: {self.vocab_check_existing}
  Similarity threshold: {self.vocab_similarity_threshold}
  Check grammar duplicates: {self.grammar_check_duplicates}

🎯 CONTENT PRIORITY:
  Vocabulary categories: {', '.join(self.vocab_priority_categories)}
  Grammar categories: {', '.join(self.grammar_priority_categories)}
  Missing topics: {', '.join(self.grammar_missing_topics)}

📊 CEFR DISTRIBUTION:
  {self._format_cefr_distribution()}

📝 EXECUTION TRACKING:
  Log path: {self.execution_log_path}
  Retention: {self.history_retention_days} days

============================================================
"""

    def _format_cefr_distribution(self) -> str:
        """Format CEFR distribution for display"""
        lines = []
        for level in ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']:
            percentage = self.cefr_distribution.get(level, 0)
            bar = '█' * (percentage // 2)  # Scale to fit display
            lines.append(f"  {level}: {percentage:2d}% {bar}")
        return '\n  '.join(lines)


if __name__ == "__main__":
    # Test configuration loading
    logging.basicConfig(level=logging.INFO)

    try:
        config = BatchConfig.load()
        print(config.get_summary())
    except Exception as e:
        print(f"❌ Configuration error: {e}")
