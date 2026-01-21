#!/usr/bin/env python3
"""
Batch vocabulary generation runner.

Processes a batch configuration file and generates all vocabulary
files using the AI generator.

Usage:
    python run_batch_generation.py business_vocabulary_batches.json
    python run_batch_generation.py business_vocabulary_batches.json --start-from 5
    python run_batch_generation.py business_vocabulary_batches.json --only 0,1,2
    python run_batch_generation.py business_vocabulary_batches.json --chunk-size 50

Features:
    - Auto-chunking: Large batches automatically split into smaller chunks (default: ON)
    - Each batch can specify any count (e.g., 80, 150, 200 words)
    - Chunks are aggregated into single output file per batch
    - Default chunk size: 40 words (configurable with --chunk-size)
"""

import os
import sys
import json
import argparse
import time
from typing import List, Dict

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from core.ai_generator import VocabularyGenerator


def load_batch_config(config_file: str) -> Dict:
    """Load batch configuration from JSON file."""
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def run_batch_generation(
    config_file: str,
    start_from: int = 0,
    only_batches: List[int] = None,
    delay_seconds: int = 2,
    verbose: bool = False,
    auto_chunk: bool = True,
    chunk_size: int = 40
):
    """
    Run batch vocabulary generation.

    Args:
        config_file: Path to batch configuration JSON
        start_from: Start from batch number (0-indexed)
        only_batches: Only generate specific batch numbers
        delay_seconds: Delay between API calls (rate limiting)
        verbose: Print detailed progress
        auto_chunk: Enable automatic batch chunking (default: True)
        chunk_size: Words per chunk when auto-chunking (default: 40)
    """
    # Load configuration
    config = load_batch_config(config_file)
    batches = config['batches']

    print(f"\n{'='*70}")
    print(f"BATCH VOCABULARY GENERATION")
    print(f"{'='*70}")
    print(f"Configuration: {config.get('description', 'No description')}")
    print(f"Total batches: {len(batches)}")
    print(f"Total words: {config.get('summary', {}).get('total_words', 'Unknown')}")
    print(f"Auto-chunking: {'ENABLED' if auto_chunk else 'DISABLED'}")
    if auto_chunk:
        print(f"Chunk size: {chunk_size} words per chunk")
    print(f"{'='*70}\n")

    # Filter batches
    if only_batches:
        batches = [batches[i] for i in only_batches if i < len(batches)]
        print(f"Processing only batches: {only_batches}")
    elif start_from > 0:
        batches = batches[start_from:]
        print(f"Starting from batch {start_from}")

    # Initialize generator
    try:
        generator = VocabularyGenerator(verbose=verbose)
    except ValueError as e:
        print(f"✗ Error initializing generator: {str(e)}")
        return

    # Process each batch
    total_words_generated = 0
    successful_batches = 0
    failed_batches = []

    for i, batch in enumerate(batches):
        batch_num = i + start_from if not only_batches else only_batches[i]

        print(f"\n{'='*70}")
        print(f"Batch {batch_num + 1}/{len(config['batches'])}: {batch['name']}")
        print(f"{'='*70}")
        print(f"Category: {batch['category']}")
        print(f"Subcategory: {batch['subcategory']}")
        print(f"Count: {batch['count']} words")
        print(f"Difficulty: {batch.get('difficulty', 'mixed')}")
        print(f"Output: {batch['output_file']}")

        try:
            # Generate vocabulary
            words = generator.generate_vocabulary(
                category=batch['category'],
                subcategory=batch['subcategory'],
                count=batch['count'],
                difficulty=batch.get('difficulty', 'mixed'),
                context=batch.get('context', ''),
                auto_chunk=auto_chunk,
                chunk_size=chunk_size
            )

            if not words:
                print(f"✗ No words generated for batch {batch['name']}")
                failed_batches.append((batch_num, batch['name'], "No words generated"))
                continue

            # Determine output path
            output_path = os.path.join(
                os.path.dirname(config_file),
                "..",
                batch['output_file']
            )

            # Save to file
            generator.save_to_file(words, output_path, format="python")

            total_words_generated += len(words)
            successful_batches += 1

            print(f"\n✓ Successfully generated {len(words)} words")
            print(f"✓ Saved to {output_path}")

        except Exception as e:
            print(f"\n✗ Error processing batch {batch['name']}: {str(e)}")
            failed_batches.append((batch_num, batch['name'], str(e)))

        # Rate limiting delay (except for last batch)
        if i < len(batches) - 1:
            if verbose:
                print(f"\nWaiting {delay_seconds} seconds before next batch...")
            time.sleep(delay_seconds)

    # Final summary
    print(f"\n{'='*70}")
    print(f"BATCH GENERATION COMPLETE")
    print(f"{'='*70}")
    print(f"Successful batches: {successful_batches}/{len(batches)}")
    print(f"Total words generated: {total_words_generated}")

    if failed_batches:
        print(f"\nFailed batches ({len(failed_batches)}):")
        for batch_num, name, error in failed_batches:
            print(f"  - Batch {batch_num}: {name}")
            print(f"    Error: {error}")

    print(f"{'='*70}\n")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Batch vocabulary generation runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all batches (auto-chunking enabled by default)
  %(prog)s business_vocabulary_batches.json

  # Start from batch 5 (if previous batches already done)
  %(prog)s business_vocabulary_batches.json --start-from 5

  # Generate only specific batches
  %(prog)s business_vocabulary_batches.json --only 0,1,2

  # Custom chunk size (larger = fewer API calls but risk truncation)
  %(prog)s business_vocabulary_batches.json --chunk-size 50

  # Disable auto-chunking (not recommended for batches with count > 50)
  %(prog)s business_vocabulary_batches.json --no-auto-chunk

  # Verbose mode with custom delay and chunk size
  %(prog)s business_vocabulary_batches.json --verbose --delay 5 --chunk-size 40

Note: Auto-chunking splits large batches (e.g., count=80) into smaller chunks
      (default: 40 words) and aggregates results. This prevents truncation errors.
        """
    )

    parser.add_argument(
        "config_file",
        help="Path to batch configuration JSON file"
    )

    parser.add_argument(
        "--start-from",
        type=int,
        default=0,
        help="Start from batch number (0-indexed)"
    )

    parser.add_argument(
        "--only",
        help="Only generate specific batches (comma-separated, e.g., '0,1,2')"
    )

    parser.add_argument(
        "--delay",
        type=int,
        default=2,
        help="Delay between API calls in seconds (default: 2)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress"
    )

    parser.add_argument(
        "--no-auto-chunk",
        action="store_true",
        help="Disable automatic batch chunking (not recommended for large batches)"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=40,
        help="Words per chunk when auto-chunking (default: 40)"
    )

    args = parser.parse_args()

    # Parse --only argument
    only_batches = None
    if args.only:
        try:
            only_batches = [int(x.strip()) for x in args.only.split(',')]
        except ValueError:
            print(f"✗ Error: Invalid --only argument. Use comma-separated numbers.")
            sys.exit(1)

    # Run batch generation
    run_batch_generation(
        config_file=args.config_file,
        start_from=args.start_from,
        only_batches=only_batches,
        delay_seconds=args.delay,
        verbose=args.verbose,
        auto_chunk=not args.no_auto_chunk,
        chunk_size=args.chunk_size
    )


if __name__ == "__main__":
    main()
