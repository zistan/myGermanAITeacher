"""
Deduplication Engine

Prevent duplicate content and redundant AI calls.
Uses database queries + fuzzy text matching to detect duplicates.
"""

import re
from difflib import SequenceMatcher
from typing import List, Set, Tuple
import logging

logger = logging.getLogger(__name__)


def normalize_german_word(word: str) -> str:
    """
    Normalize German word for comparison

    Args:
        word: German word to normalize

    Returns:
        Normalized word (lowercase, articles removed)
    """
    # Convert to lowercase
    word = word.lower().strip()

    # Remove common articles (der, die, das, ein, eine)
    word = re.sub(r'^(der|die|das|ein|eine)\s+', '', word)

    # Remove parenthetical notes like "(Pl.)" or "(formal)"
    word = re.sub(r'\s*\([^)]*\)', '', word)

    # Remove extra whitespace
    word = ' '.join(word.split())

    return word


def fuzzy_match(str1: str, str2: str, threshold: float) -> bool:
    """
    Check if two strings are similar using fuzzy matching

    Args:
        str1: First string
        str2: Second string
        threshold: Similarity threshold (0.0-1.0)

    Returns:
        True if strings are similar enough
    """
    # Normalize both strings
    s1 = normalize_german_word(str1)
    s2 = normalize_german_word(str2)

    # Calculate similarity ratio
    ratio = SequenceMatcher(None, s1, s2).ratio()

    return ratio >= threshold


class VocabularyDeduplicator:
    """Deduplication for vocabulary words"""

    def __init__(self, db_session, similarity_threshold: float = 0.85):
        """
        Initialize deduplicator

        Args:
            db_session: SQLAlchemy database session
            similarity_threshold: Fuzzy match threshold (0.0-1.0)
        """
        self.db = db_session
        self.threshold = similarity_threshold
        logger.info(f"Initialized VocabularyDeduplicator with threshold={similarity_threshold}")

    def get_existing_words(self, category: str = None, difficulty: str = None) -> Set[str]:
        """
        Query existing words from database

        Args:
            category: Optional category filter
            difficulty: Optional difficulty filter

        Returns:
            Set of existing words (normalized, lowercase)
        """
        try:
            # Import here to avoid circular dependency
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.vocabulary import Vocabulary

            # Build query
            query = self.db.query(Vocabulary.word)

            if category:
                query = query.filter(Vocabulary.category == category)

            if difficulty:
                query = query.filter(Vocabulary.difficulty == difficulty)

            # Execute query
            results = query.all()

            # Extract and normalize words
            existing_words = {normalize_german_word(row[0]) for row in results}

            logger.info(f"Loaded {len(existing_words)} existing words from database")
            return existing_words

        except Exception as e:
            logger.error(f"Failed to query existing words: {e}")
            return set()

    def is_duplicate(self, word: str, existing_words: Set[str]) -> bool:
        """
        Check if word is duplicate using fuzzy matching

        Args:
            word: Word to check
            existing_words: Set of existing words (normalized)

        Returns:
            True if word is a duplicate
        """
        normalized_word = normalize_german_word(word)

        # Exact match
        if normalized_word in existing_words:
            return True

        # Fuzzy match
        for existing in existing_words:
            if fuzzy_match(word, existing, self.threshold):
                logger.debug(f"Fuzzy match found: '{word}' ≈ '{existing}'")
                return True

        return False

    def filter_duplicates(self, words: List[str], existing_words: Set[str] = None) -> Tuple[List[str], List[str]]:
        """
        Filter duplicates from word list

        Args:
            words: List of words to check
            existing_words: Optional set of existing words (will query if not provided)

        Returns:
            (unique_words, duplicate_words) tuple
        """
        if existing_words is None:
            existing_words = self.get_existing_words()

        unique_words = []
        duplicate_words = []

        # Track words we've seen in this batch to avoid duplicates within the batch itself
        batch_seen = set()

        for word in words:
            normalized = normalize_german_word(word)

            # Check if duplicate in batch
            if normalized in batch_seen:
                duplicate_words.append(word)
                continue

            # Check if duplicate in database
            if self.is_duplicate(word, existing_words):
                duplicate_words.append(word)
            else:
                unique_words.append(word)
                batch_seen.add(normalized)

        logger.info(f"Filtered {len(words)} words: {len(unique_words)} unique, {len(duplicate_words)} duplicates")

        return unique_words, duplicate_words


class GrammarDeduplicator:
    """Deduplication for grammar exercises"""

    def __init__(self, db_session, similarity_threshold: float = 0.90):
        """
        Initialize deduplicator

        Args:
            db_session: SQLAlchemy database session
            similarity_threshold: Fuzzy match threshold (stricter for grammar, 0.90)
        """
        self.db = db_session
        self.threshold = similarity_threshold
        logger.info(f"Initialized GrammarDeduplicator with threshold={similarity_threshold}")

    def get_existing_exercises(self, topic_id: int) -> List[str]:
        """
        Query existing exercises for topic

        Args:
            topic_id: Grammar topic ID

        Returns:
            List of existing exercise questions
        """
        try:
            # Import here to avoid circular dependency
            import sys
            import os
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            sys.path.insert(0, backend_dir)

            from app.models.grammar import GrammarExercise

            # Query exercises for this topic
            results = self.db.query(GrammarExercise.question).filter(
                GrammarExercise.topic_id == topic_id
            ).all()

            # Extract questions
            existing_questions = [row[0] for row in results]

            logger.info(f"Loaded {len(existing_questions)} existing exercises for topic {topic_id}")
            return existing_questions

        except Exception as e:
            logger.error(f"Failed to query existing exercises: {e}")
            return []

    def is_duplicate_question(self, question: str, existing_questions: List[str]) -> bool:
        """
        Check if question text is too similar to existing exercises

        Args:
            question: Question to check
            existing_questions: List of existing questions

        Returns:
            True if question is a duplicate
        """
        # Normalize question
        normalized_question = question.lower().strip()

        for existing in existing_questions:
            normalized_existing = existing.lower().strip()

            # Calculate similarity
            ratio = SequenceMatcher(None, normalized_question, normalized_existing).ratio()

            if ratio >= self.threshold:
                logger.debug(f"Duplicate exercise found: '{question}' ≈ '{existing}'")
                return True

        return False

    def filter_duplicate_exercises(self, exercises: List[dict], existing: List[str] = None, topic_id: int = None) -> Tuple[List[dict], List[dict]]:
        """
        Filter duplicate exercises

        Args:
            exercises: List of exercise dictionaries (must have 'question' field)
            existing: Optional list of existing questions (will query if not provided)
            topic_id: Topic ID (required if existing not provided)

        Returns:
            (unique_exercises, duplicate_exercises) tuple
        """
        if existing is None:
            if topic_id is None:
                raise ValueError("Must provide either 'existing' or 'topic_id'")
            existing = self.get_existing_exercises(topic_id)

        unique_exercises = []
        duplicate_exercises = []

        # Track questions we've seen in this batch
        batch_questions = []

        for exercise in exercises:
            question = exercise.get('question', '')

            if not question:
                logger.warning(f"Exercise missing question field: {exercise}")
                duplicate_exercises.append(exercise)
                continue

            # Check if duplicate in batch
            if self.is_duplicate_question(question, batch_questions):
                duplicate_exercises.append(exercise)
                continue

            # Check if duplicate in database
            if self.is_duplicate_question(question, existing):
                duplicate_exercises.append(exercise)
            else:
                unique_exercises.append(exercise)
                batch_questions.append(question)

        logger.info(f"Filtered {len(exercises)} exercises: {len(unique_exercises)} unique, {len(duplicate_exercises)} duplicates")

        return unique_exercises, duplicate_exercises


if __name__ == "__main__":
    # Test normalization and fuzzy matching
    logging.basicConfig(level=logging.DEBUG)

    print("Testing word normalization:")
    test_words = [
        "der Hund",
        "die Katze",
        "das Auto",
        "ein Haus",
        "eine Wohnung",
        "Büro (n.)",
        "  Zahlung  "
    ]

    for word in test_words:
        normalized = normalize_german_word(word)
        print(f"  '{word}' → '{normalized}'")

    print("\nTesting fuzzy matching:")
    test_pairs = [
        ("der Hund", "Hund", 0.85),
        ("Zahlung", "Zahlungen", 0.85),
        ("Rechnung", "Rechnungen", 0.85),
        ("Auto", "Autobahn", 0.85),
    ]

    for word1, word2, threshold in test_pairs:
        is_match = fuzzy_match(word1, word2, threshold)
        print(f"  '{word1}' vs '{word2}' (threshold={threshold}): {'MATCH' if is_match else 'NO MATCH'}")
