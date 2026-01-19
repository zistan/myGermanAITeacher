#!/usr/bin/env python3
"""
Master vocabulary seed orchestrator.

This script provides a CLI for seeding vocabulary data from various sources
with validation, bulk insertion, and progress tracking.

Usage:
    python master_seed.py --all                    # Seed all categories
    python master_seed.py --priority               # Seed priority business vocabulary
    python master_seed.py --categories business    # Seed specific categories
    python master_seed.py --dry-run --verbose      # Validate without inserting
"""

import sys
import os
import argparse
import importlib
from typing import List, Dict
from datetime import datetime

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from core.validation import VocabularyValidator
from core.bulk_insert import bulk_insert_vocabulary, get_vocabulary_count
from core.data_format import VocabularyWord


# Category registry mapping category names to seed modules
CATEGORY_REGISTRY = {
    # Phase 2: Business vocabulary (HIGHEST PRIORITY - 3,500 words)
    "business": [
        "business.seed_finance_payments",      # 800 words - CRITICAL
        "business.seed_business_general",      # 1,500 words
        "business.seed_finance_banking",       # 400 words
        "business.seed_finance_accounting",    # 300 words
        "business.seed_business_legal",        # 300 words
        "business.seed_business_hr",           # 200 words
    ],

    # Phase 3: Core frequency vocabulary (10,000 words)
    "cefr_core": [
        "cefr_core.seed_a1_foundation",        # 800 words
        "cefr_core.seed_a2_expansion",         # 1,200 words
        "cefr_core.seed_b1_intermediate",      # 4,000 words
        "cefr_core.seed_b2_upper_intermediate",# 4,000 words
    ],

    # Phase 4: Advanced vocabulary (8,000 words)
    "advanced": [
        "advanced.seed_c1_advanced",           # 5,000 words
        "advanced.seed_c2_mastery",            # 3,000 words
    ],

    # Phase 5: Thematic vocabulary (5,000 words)
    "thematic": [
        "thematic.seed_food_drink",            # 500 words
        "thematic.seed_travel_transport",      # 500 words
        "thematic.seed_technology_digital",    # 500 words
        "thematic.seed_health_medical",        # 500 words
        "thematic.seed_sports_hobbies",        # 500 words
        "thematic.seed_home_living",           # 500 words
        "thematic.seed_education_learning",    # 500 words
        "thematic.seed_environment_nature",    # 500 words
        "thematic.seed_culture_society",       # 500 words
        "thematic.seed_politics_government",   # 500 words
    ],

    # Phase 6: Linguistic completeness (3,200 words)
    "linguistic": [
        "linguistic.seed_verbs_frequency",     # 1,500 verbs
        "linguistic.seed_adjectives_frequency",# 1,000 adjectives
        "linguistic.seed_modal_particles",     # 100 particles - CRITICAL
        "linguistic.seed_idioms_expressions",  # 500 idioms
        "linguistic.seed_prepositions_conjunctions", # 100 words
    ],
}


# Priority categories (Phase 2 - Business)
PRIORITY_CATEGORIES = ["business"]


def load_seed_module(module_path: str, verbose: bool = False):
    """
    Dynamically load a seed module and get its words.

    Args:
        module_path: Module path (e.g., "business.seed_finance_payments")
        verbose: If True, print loading messages

    Returns:
        List of VocabularyWord dictionaries, or None if module not found
    """
    try:
        # Import module dynamically
        full_path = f"vocabulary_seeds.{module_path}" if not module_path.startswith("vocabulary_seeds.") else module_path

        if verbose:
            print(f"  Loading module: {full_path}")

        module = importlib.import_module(full_path)

        # Call get_vocabulary_words() function
        if hasattr(module, "get_vocabulary_words"):
            words = module.get_vocabulary_words()

            if verbose:
                print(f"  ✓ Loaded {len(words)} words from {module_path}")

            return words
        else:
            if verbose:
                print(f"  ✗ Module {module_path} missing get_vocabulary_words() function")
            return None

    except ModuleNotFoundError:
        if verbose:
            print(f"  ⚠ Module {module_path} not found (not yet implemented)")
        return None

    except Exception as e:
        if verbose:
            print(f"  ✗ Error loading module {module_path}: {str(e)}")
        return None


def collect_words_from_categories(
    categories: List[str],
    verbose: bool = False
) -> List[VocabularyWord]:
    """
    Collect words from specified categories.

    Args:
        categories: List of category names
        verbose: If True, print progress messages

    Returns:
        Combined list of VocabularyWord dictionaries
    """
    all_words = []

    for category in categories:
        if category not in CATEGORY_REGISTRY:
            if verbose:
                print(f"⚠ Unknown category: {category}")
            continue

        if verbose:
            print(f"\n{'='*60}")
            print(f"Category: {category.upper()}")
            print(f"{'='*60}")

        # Load all modules for this category
        for module_path in CATEGORY_REGISTRY[category]:
            words = load_seed_module(module_path, verbose)

            if words:
                all_words.extend(words)

    return all_words


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Vocabulary seed orchestrator - Load vocabulary data into database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --all                           # Seed all 25,000 words
  %(prog)s --priority                      # Seed priority business vocabulary (3,500 words)
  %(prog)s --categories business cefr_core # Seed specific categories
  %(prog)s --dry-run --verbose             # Validate without inserting
  %(prog)s --all --skip-validation         # Skip validation (use with caution)
        """
    )

    # Category selection
    parser.add_argument(
        "--all",
        action="store_true",
        help="Seed all categories (25,000 words)"
    )

    parser.add_argument(
        "--priority",
        action="store_true",
        help="Seed priority business vocabulary only (3,500 words)"
    )

    parser.add_argument(
        "--categories",
        nargs="+",
        choices=list(CATEGORY_REGISTRY.keys()),
        help="Seed specific categories"
    )

    # Options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate words without inserting into database"
    )

    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation step (use with caution)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress messages"
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Batch size for bulk insertion (default: 1000)"
    )

    args = parser.parse_args()

    # Determine which categories to load
    if args.all:
        categories = list(CATEGORY_REGISTRY.keys())
        print("Seeding ALL categories (target: 25,000 words)")
    elif args.priority:
        categories = PRIORITY_CATEGORIES
        print("Seeding PRIORITY categories (business - target: 3,500 words)")
    elif args.categories:
        categories = args.categories
        print(f"Seeding categories: {', '.join(categories)}")
    else:
        parser.print_help()
        print("\nError: Must specify --all, --priority, or --categories")
        sys.exit(1)

    start_time = datetime.now()

    # Step 1: Collect words from all modules
    print(f"\n{'='*60}")
    print("STEP 1: COLLECTING WORDS")
    print(f"{'='*60}")

    words = collect_words_from_categories(categories, args.verbose)

    print(f"\n✓ Collected {len(words)} words from {len(categories)} categories")

    if len(words) == 0:
        print("⚠ No words collected. Modules may not be implemented yet.")
        sys.exit(0)

    # Step 2: Validation (unless skipped)
    if not args.skip_validation:
        print(f"\n{'='*60}")
        print("STEP 2: VALIDATION")
        print(f"{'='*60}")

        validator = VocabularyValidator(verbose=args.verbose)
        validation_result = validator.validate_words(words)

        print(validation_result.summary())

        if not validation_result.is_valid():
            print(f"\n✗ VALIDATION FAILED - {len(validation_result.errors)} errors found")
            print("\nFirst 10 errors:")
            for error in validation_result.errors[:10]:
                print(f"  - {error}")

            if len(validation_result.errors) > 10:
                print(f"  ... and {len(validation_result.errors) - 10} more errors")

            sys.exit(1)

        print("\n✓ VALIDATION PASSED")

        # Show statistics
        if args.verbose:
            stats = validator.get_statistics(words)
            print(f"\n{'='*60}")
            print("STATISTICS")
            print(f"{'='*60}")
            print(f"Total words: {stats['total_words']}")
            print(f"Duplicates: {stats['duplicates']}")
            print(f"\nCEFR Distribution:")
            for level, count in sorted(stats['cefr_distribution'].items()):
                percentage = stats['cefr_percentages'].get(level, 0)
                print(f"  {level}: {count} ({percentage:.1f}%)")
            print(f"\nQuality Distribution:")
            for tier, count in stats['quality_distribution'].items():
                percentage = stats['quality_percentages'].get(tier, 0)
                print(f"  {tier}: {count} ({percentage:.1f}%)")

    else:
        print("\n⚠ Skipping validation (--skip-validation)")

    # Step 3: Database insertion (unless dry-run)
    if args.dry_run:
        print(f"\n{'='*60}")
        print("DRY RUN - Not inserting into database")
        print(f"{'='*60}")
        print(f"Would insert {len(words)} words")

    else:
        print(f"\n{'='*60}")
        print("STEP 3: DATABASE INSERTION")
        print(f"{'='*60}")

        # Get current count
        current_count = get_vocabulary_count()
        print(f"Current vocabulary count: {current_count}")

        # Bulk insert
        insert_result = bulk_insert_vocabulary(
            words,
            batch_size=args.batch_size,
            verbose=args.verbose
        )

        print(insert_result.summary())

        # Get new count
        new_count = get_vocabulary_count()
        print(f"\nNew vocabulary count: {new_count} (added {new_count - current_count})")

    # Final summary
    end_time = datetime.now()
    total_duration = (end_time - start_time).total_seconds()

    print(f"\n{'='*60}")
    print("COMPLETED")
    print(f"{'='*60}")
    print(f"Total duration: {total_duration:.2f} seconds")

    if args.dry_run:
        print("✓ Dry run completed successfully")
    else:
        print("✓ Vocabulary seeding completed successfully")


if __name__ == "__main__":
    main()
