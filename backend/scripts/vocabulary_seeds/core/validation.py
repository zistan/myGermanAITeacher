"""
Validation utilities for vocabulary seed data.

This module provides the VocabularyValidator class for validating vocabulary words.
"""

from typing import List, Dict, Set, Tuple
from collections import defaultdict
import re

from .data_format import (
    VocabularyWord,
    CEFR_LEVELS,
    VALID_CATEGORIES,
    VALID_POS,
    VALID_GENDERS,
    ARTICLES,
    get_quality_tier,
    validate_article_gender_match
)


class ValidationResult:
    """Result of validation with errors and warnings."""

    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.valid_count: int = 0
        self.invalid_count: int = 0

    def add_error(self, message: str):
        """Add an error message."""
        self.errors.append(message)
        self.invalid_count += 1

    def add_warning(self, message: str):
        """Add a warning message."""
        self.warnings.append(message)

    def is_valid(self) -> bool:
        """Check if validation passed (no errors)."""
        return len(self.errors) == 0

    def summary(self) -> str:
        """Get a summary of validation results."""
        lines = [
            f"Valid words: {self.valid_count}",
            f"Invalid words: {self.invalid_count}",
            f"Errors: {len(self.errors)}",
            f"Warnings: {len(self.warnings)}"
        ]
        return "\n".join(lines)


class VocabularyValidator:
    """Validator for vocabulary word data."""

    def __init__(self, verbose: bool = False):
        """
        Initialize validator.

        Args:
            verbose: If True, print detailed validation messages
        """
        self.verbose = verbose
        self.seen_words: Set[str] = set()  # Track for duplicate detection

    def validate_words(self, words: List[VocabularyWord]) -> ValidationResult:
        """
        Validate a list of vocabulary words.

        Args:
            words: List of vocabulary word dictionaries

        Returns:
            ValidationResult with errors and warnings
        """
        result = ValidationResult()

        for i, word in enumerate(words):
            word_errors = self._validate_single_word(word, i)

            if word_errors:
                for error in word_errors:
                    result.add_error(error)
            else:
                result.valid_count += 1

            # Check for duplicates (case-insensitive)
            word_text = word.get("word", "").strip().lower()
            if word_text in self.seen_words:
                result.add_warning(
                    f"Word #{i + 1}: Duplicate word '{word.get('word')}' (case-insensitive)"
                )
            else:
                self.seen_words.add(word_text)

        # Add distribution analysis as warnings
        distribution = self._analyze_distribution(words)
        if self.verbose:
            result.add_warning("\n=== Distribution Analysis ===")
            result.add_warning(f"CEFR: {distribution['cefr']}")
            result.add_warning(f"Categories: {distribution['categories']}")
            result.add_warning(f"Quality tiers: {distribution['quality']}")

        return result

    def _validate_single_word(self, word: VocabularyWord, index: int) -> List[str]:
        """
        Validate a single vocabulary word.

        Args:
            word: Vocabulary word dictionary
            index: Index of word in list (for error messages)

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        word_id = f"Word #{index + 1}"

        # Required fields
        required_fields = [
            "word", "translation_it", "part_of_speech",
            "difficulty", "category", "example_de", "example_it"
        ]

        for field in required_fields:
            if not word.get(field):
                errors.append(f"{word_id}: Missing required field '{field}'")

        # If missing required fields, skip further validation
        if errors:
            return errors

        # Validate CEFR level
        difficulty = word.get("difficulty", "").upper()
        if difficulty not in CEFR_LEVELS:
            errors.append(
                f"{word_id} '{word['word']}': Invalid difficulty '{difficulty}'. "
                f"Must be one of: {', '.join(CEFR_LEVELS)}"
            )

        # Validate category
        category = word.get("category", "")
        if category not in VALID_CATEGORIES:
            errors.append(
                f"{word_id} '{word['word']}': Invalid category '{category}'. "
                f"Must be one of: {', '.join(VALID_CATEGORIES)}"
            )

        # Validate part of speech
        pos = word.get("part_of_speech", "")
        if pos not in VALID_POS:
            errors.append(
                f"{word_id} '{word['word']}': Invalid part_of_speech '{pos}'. "
                f"Must be one of: {', '.join(VALID_POS)}"
            )

        # Validate noun-specific fields
        if pos == "noun":
            errors.extend(self._validate_noun(word, word_id))

        # Validate boolean fields (should be 0 or 1)
        boolean_fields = ["is_idiom", "is_compound", "is_separable_verb"]
        for field in boolean_fields:
            value = word.get(field)
            if value is not None and value not in [0, 1, True, False]:
                errors.append(
                    f"{word_id} '{word['word']}': Field '{field}' must be 0, 1, "
                    f"True, or False, got: {value}"
                )

        # Validate JSON array fields (synonyms, antonyms)
        for field in ["synonyms", "antonyms"]:
            value = word.get(field)
            if value and not self._is_valid_json_array(value):
                errors.append(
                    f"{word_id} '{word['word']}': Field '{field}' must be a JSON array "
                    f"string like '[\"word1\", \"word2\"]'"
                )

        return errors

    def _validate_noun(self, word: VocabularyWord, word_id: str) -> List[str]:
        """
        Validate noun-specific fields (gender, article).

        Args:
            word: Vocabulary word dictionary
            word_id: Word identifier for error messages

        Returns:
            List of error messages
        """
        errors = []
        word_text = word.get("word", "")
        gender = word.get("gender")

        # Check if noun has article
        has_article = any(
            word_text.lower().startswith(article + " ")
            for articles in ARTICLES.values()
            for article in articles
        )

        if not has_article:
            errors.append(
                f"{word_id} '{word_text}': Noun should include article "
                f"(der/die/das)"
            )

        # Validate gender if provided
        if gender:
            if gender not in VALID_GENDERS:
                errors.append(
                    f"{word_id} '{word_text}': Invalid gender '{gender}'. "
                    f"Must be one of: {', '.join(VALID_GENDERS)}"
                )
            elif not validate_article_gender_match(word_text, gender):
                errors.append(
                    f"{word_id} '{word_text}': Article doesn't match gender '{gender}'"
                )

        return errors

    def _is_valid_json_array(self, value: str) -> bool:
        """
        Check if a string is a valid JSON array format.

        Args:
            value: String to validate

        Returns:
            True if valid JSON array format
        """
        # Simple regex check for JSON array format
        # Proper validation would parse JSON, but this is sufficient for seed data
        pattern = r'^\[(".*?")(,\s*".*?")*\]$'
        return bool(re.match(pattern, value))

    def _analyze_distribution(self, words: List[VocabularyWord]) -> Dict[str, Dict[str, int]]:
        """
        Analyze distribution of words across CEFR levels, categories, and quality tiers.

        Args:
            words: List of vocabulary words

        Returns:
            Dictionary with distribution statistics
        """
        cefr_dist = defaultdict(int)
        category_dist = defaultdict(int)
        quality_dist = defaultdict(int)

        for word in words:
            # CEFR distribution
            difficulty = word.get("difficulty", "Unknown").upper()
            cefr_dist[difficulty] += 1

            # Category distribution
            category = word.get("category", "Unknown")
            category_dist[category] += 1

            # Quality tier distribution
            tier = get_quality_tier(word)
            quality_dist[tier] += 1

        return {
            "cefr": dict(cefr_dist),
            "categories": dict(category_dist),
            "quality": dict(quality_dist)
        }

    def check_duplicates(self, words: List[VocabularyWord]) -> List[Tuple[str, List[int]]]:
        """
        Find duplicate words (case-insensitive).

        Args:
            words: List of vocabulary words

        Returns:
            List of tuples (word, [indices]) for duplicates
        """
        word_indices = defaultdict(list)

        for i, word in enumerate(words):
            word_text = word.get("word", "").strip().lower()
            word_indices[word_text].append(i)

        # Return only words that appear more than once
        duplicates = [
            (word, indices)
            for word, indices in word_indices.items()
            if len(indices) > 1
        ]

        return duplicates

    def get_statistics(self, words: List[VocabularyWord]) -> Dict:
        """
        Get comprehensive statistics about vocabulary words.

        Args:
            words: List of vocabulary words

        Returns:
            Dictionary with statistics
        """
        distribution = self._analyze_distribution(words)
        duplicates = self.check_duplicates(words)

        # Calculate quality metrics
        total_words = len(words)
        premium_count = distribution["quality"].get("premium", 0)
        standard_count = distribution["quality"].get("standard", 0)
        basic_count = distribution["quality"].get("basic", 0)

        # Calculate CEFR percentages
        cefr_percentages = {
            level: (count / total_words * 100) if total_words > 0 else 0
            for level, count in distribution["cefr"].items()
        }

        return {
            "total_words": total_words,
            "duplicates": len(duplicates),
            "cefr_distribution": distribution["cefr"],
            "cefr_percentages": cefr_percentages,
            "category_distribution": distribution["categories"],
            "quality_distribution": {
                "premium": premium_count,
                "standard": standard_count,
                "basic": basic_count
            },
            "quality_percentages": {
                "premium": (premium_count / total_words * 100) if total_words > 0 else 0,
                "standard": (standard_count / total_words * 100) if total_words > 0 else 0,
                "basic": (basic_count / total_words * 100) if total_words > 0 else 0
            }
        }
