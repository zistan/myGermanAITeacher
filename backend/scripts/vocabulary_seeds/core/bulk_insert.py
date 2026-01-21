"""
Bulk insertion utilities for vocabulary seed data.

This module provides efficient batch insertion into the database.
"""

import sys
import os
from typing import List, Dict
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session

# Add parent directories to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

from app.database import SessionLocal
from .data_format import VocabularyWord


class BulkInsertResult:
    """Result of bulk insertion operation."""

    def __init__(self):
        self.inserted_count: int = 0
        self.skipped_count: int = 0
        self.error_count: int = 0
        self.duration_seconds: float = 0.0
        self.errors: List[str] = []

    def summary(self) -> str:
        """Get a summary of insertion results."""
        lines = [
            f"\n{'='*60}",
            f"BULK INSERT SUMMARY",
            f"{'='*60}",
            f"Inserted:  {self.inserted_count} words",
            f"Skipped:   {self.skipped_count} words (duplicates)",
            f"Errors:    {self.error_count}",
            f"Duration:  {self.duration_seconds:.2f} seconds",
            f"{'='*60}"
        ]

        if self.errors:
            lines.append("\nERRORS:")
            for error in self.errors[:10]:  # Show first 10 errors
                lines.append(f"  - {error}")
            if len(self.errors) > 10:
                lines.append(f"  ... and {len(self.errors) - 10} more errors")

        return "\n".join(lines)


def bulk_insert_vocabulary(
    words: List[VocabularyWord],
    batch_size: int = 1000,
    verbose: bool = False
) -> BulkInsertResult:
    """
    Bulk insert vocabulary words into the database.

    Uses PostgreSQL INSERT ... ON CONFLICT DO NOTHING for efficient insertion
    with automatic duplicate handling.

    Args:
        words: List of vocabulary word dictionaries
        batch_size: Number of words to insert per batch (default: 1000)
        verbose: If True, print progress messages

    Returns:
        BulkInsertResult with insertion statistics
    """
    result = BulkInsertResult()
    start_time = datetime.now()

    if not words:
        if verbose:
            print("No words to insert")
        return result

    db = SessionLocal()

    try:
        # Process words in batches
        total_batches = (len(words) + batch_size - 1) // batch_size

        for batch_num in range(total_batches):
            start_idx = batch_num * batch_size
            end_idx = min(start_idx + batch_size, len(words))
            batch = words[start_idx:end_idx]

            if verbose:
                print(f"Processing batch {batch_num + 1}/{total_batches} "
                      f"({len(batch)} words)...")

            # Insert batch
            batch_result = _insert_batch(db, batch, verbose)
            result.inserted_count += batch_result["inserted"]
            result.skipped_count += batch_result["skipped"]
            result.error_count += batch_result["errors"]

            if batch_result["error_messages"]:
                result.errors.extend(batch_result["error_messages"])

        # Commit all changes
        db.commit()

        if verbose:
            print(f"✓ Successfully committed {result.inserted_count} words to database")

    except Exception as e:
        db.rollback()
        error_msg = f"Database error during bulk insert: {str(e)}"
        result.errors.append(error_msg)
        result.error_count += 1

        if verbose:
            print(f"✗ Error: {error_msg}")

    finally:
        db.close()

    # Calculate duration
    end_time = datetime.now()
    result.duration_seconds = (end_time - start_time).total_seconds()

    return result


def _insert_batch(
    db: Session,
    batch: List[VocabularyWord],
    verbose: bool
) -> Dict[str, int]:
    """
    Insert a single batch of words.

    Args:
        db: Database session
        batch: List of vocabulary words to insert
        verbose: If True, print progress messages

    Returns:
        Dictionary with counts: inserted, skipped, errors
    """
    inserted = 0
    skipped = 0
    errors = 0
    error_messages = []

    # Build SQL INSERT statement with ON CONFLICT
    sql = text("""
        INSERT INTO vocabulary (
            word, translation_it, part_of_speech, gender, plural_form,
            difficulty, category, example_de, example_it,
            pronunciation, definition_de, synonyms, antonyms, usage_notes,
            is_idiom, is_compound, is_separable_verb
        ) VALUES (
            :word, :translation_it, :part_of_speech, :gender, :plural_form,
            :difficulty, :category, :example_de, :example_it,
            :pronunciation, :definition_de, :synonyms, :antonyms, :usage_notes,
            :is_idiom, :is_compound, :is_separable_verb
        )
        ON CONFLICT (word) DO NOTHING
        RETURNING id
    """)

    for word in batch:
        try:
            # Prepare word data - convert boolean fields to integers
            word_data = _prepare_word_for_insert(word)

            # Execute insert
            result = db.execute(sql, word_data)
            row = result.fetchone()

            if row:
                inserted += 1
            else:
                skipped += 1  # Duplicate, skipped by ON CONFLICT

            # Commit after each successful insert to prevent transaction abort cascade
            db.commit()

        except Exception as e:
            errors += 1
            # Rollback the failed transaction so subsequent inserts can continue
            db.rollback()
            error_msg = f"Error inserting word '{word.get('word', 'UNKNOWN')}': {str(e)}"
            error_messages.append(error_msg)

            if verbose:
                print(f"  ✗ {error_msg}")

    return {
        "inserted": inserted,
        "skipped": skipped,
        "errors": errors,
        "error_messages": error_messages
    }


def _prepare_word_for_insert(word: VocabularyWord) -> Dict:
    """
    Prepare a vocabulary word for database insertion.

    Handles:
    - Boolean field conversion (Python bool → Integer 0/1)
    - None value handling
    - Field mapping

    Args:
        word: Vocabulary word dictionary

    Returns:
        Dictionary ready for database insertion
    """
    # Convert boolean fields to integers (0 or 1)
    def bool_to_int(value) -> int:
        if value is None:
            return 0
        if isinstance(value, bool):
            return 1 if value else 0
        if isinstance(value, int):
            return 1 if value else 0
        return 0

    return {
        # Required fields
        "word": word.get("word", ""),
        "translation_it": word.get("translation_it", ""),
        "part_of_speech": word.get("part_of_speech", ""),
        "difficulty": word.get("difficulty", ""),
        "category": word.get("category", ""),
        "example_de": word.get("example_de", ""),
        "example_it": word.get("example_it", ""),

        # Optional fields (None if not provided)
        "pronunciation": word.get("pronunciation"),
        "definition_de": word.get("definition_de"),
        "synonyms": word.get("synonyms"),
        "antonyms": word.get("antonyms"),
        "usage_notes": word.get("usage_notes"),
        "gender": word.get("gender"),
        "plural_form": word.get("plural_form"),

        # Boolean fields (convert to 0/1)
        "is_idiom": bool_to_int(word.get("is_idiom")),
        "is_compound": bool_to_int(word.get("is_compound")),
        "is_separable_verb": bool_to_int(word.get("is_separable_verb"))
    }


def get_vocabulary_count(category: str = None, difficulty: str = None) -> int:
    """
    Get count of vocabulary words in database.

    Args:
        category: Optional category filter
        difficulty: Optional difficulty filter

    Returns:
        Count of matching words
    """
    db = SessionLocal()

    try:
        sql = "SELECT COUNT(*) FROM vocabulary WHERE 1=1"
        params = {}

        if category:
            sql += " AND category = :category"
            params["category"] = category

        if difficulty:
            sql += " AND difficulty = :difficulty"
            params["difficulty"] = difficulty

        result = db.execute(text(sql), params)
        count = result.scalar()

        return count or 0

    finally:
        db.close()


def clear_vocabulary_table():
    """
    Clear all vocabulary words from database.

    WARNING: This is destructive and cannot be undone!
    Use with extreme caution.
    """
    db = SessionLocal()

    try:
        # Delete all vocabulary words
        db.execute(text("DELETE FROM vocabulary"))
        db.commit()
        print("✓ Vocabulary table cleared")

    except Exception as e:
        db.rollback()
        print(f"✗ Error clearing vocabulary table: {str(e)}")
        raise

    finally:
        db.close()
