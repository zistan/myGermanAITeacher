#!/usr/bin/env python3
"""
Batch Content Feeding System - CLI Entry Point

Command-line interface for batch vocabulary and grammar content generation.

Usage:
    # Execute batches
    python batch_feed.py --vocabulary --verbose
    python batch_feed.py --grammar --verbose
    python batch_feed.py --both --verbose
    python batch_feed.py --both --force  # Bypass caps

    # Monitoring
    python batch_feed.py --status        # Show current progress
    python batch_feed.py --gaps          # Show gap analysis
    python batch_feed.py --history       # Show execution history
    python batch_feed.py --config        # Show current configuration
"""

import argparse
import sys
import os
import logging

# Add backend to path
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, backend_dir)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def show_status(db, config):
    """Show current batch feeding status"""
    from core.batch_tracker import BatchExecutionTracker
    from gap_analysis.vocabulary_gaps import VocabularyGapAnalyzer
    from gap_analysis.grammar_gaps import GrammarGapAnalyzer
    from app.models.vocabulary import Vocabulary
    from app.models.grammar import GrammarExercise
    from sqlalchemy import func

    tracker = BatchExecutionTracker(config.execution_log_path, config.history_retention_days)
    vocab_analyzer = VocabularyGapAnalyzer(db, config)
    grammar_analyzer = GrammarGapAnalyzer(db, config)

    # Get current totals from database
    total_vocab = db.query(func.count(Vocabulary.id)).scalar() or 0
    total_exercises = grammar_analyzer.get_total_exercises()
    total_topics = grammar_analyzer.get_total_topics()

    # Get daily/weekly totals from tracker
    daily_totals = tracker.get_daily_totals()
    weekly_totals = tracker.get_weekly_totals()

    # Calculate percentages
    vocab_progress = (total_vocab / config.vocab_max_total * 100) if config.vocab_max_total > 0 else 0
    grammar_progress = (total_exercises / config.grammar_max_total * 100) if config.grammar_max_total > 0 else 0

    # Check if next batch can run
    can_vocab, vocab_reason = tracker.can_execute_vocabulary(
        config.vocab_max_per_run,
        config.daily_cap_words,
        config.weekly_cap_words,
        config.vocab_max_total
    )
    can_grammar, grammar_reason = tracker.can_execute_grammar(
        config.grammar_max_per_run,
        config.daily_cap_exercises,
        config.weekly_cap_exercises,
        config.grammar_max_total
    )

    print("============================================================")
    print("BATCH FEEDING STATUS")
    print("============================================================")
    print()
    print("📅 Today's Progress:")
    print(f"  Vocabulary: {daily_totals['words']}/{config.daily_cap_words} words " +
          f"({daily_totals['words']/config.daily_cap_words*100:.1f}% of daily cap)")
    print(f"  Grammar: {daily_totals['exercises']}/{config.daily_cap_exercises} exercises " +
          f"({daily_totals['exercises']/config.daily_cap_exercises*100:.1f}% of daily cap)")
    print()
    print("📆 This Week's Progress:")
    print(f"  Vocabulary: {weekly_totals['words']}/{config.weekly_cap_words} words " +
          f"({weekly_totals['words']/config.weekly_cap_words*100:.1f}% of weekly cap)")
    print(f"  Grammar: {weekly_totals['exercises']}/{config.weekly_cap_exercises} exercises " +
          f"({weekly_totals['exercises']/config.weekly_cap_exercises*100:.1f}% of weekly cap)")
    print()
    print("🎯 Global Progress:")
    print(f"  Vocabulary: {total_vocab:,}/{config.vocab_max_total:,} words ({vocab_progress:.1f}%)")
    print(f"  Grammar: {total_exercises:,}/{config.grammar_max_total:,} exercises ({grammar_progress:.1f}%)")
    print(f"  Grammar Topics: {total_topics}")
    print()
    print("✅ Next Batch Execution:")
    print(f"  Vocabulary: {'YES' if can_vocab else 'NO'}" + (f" - {vocab_reason}" if not can_vocab else ""))
    print(f"  Grammar: {'YES' if can_grammar else 'NO'}" + (f" - {grammar_reason}" if not can_grammar else ""))
    print("============================================================")


def show_gaps(db, config):
    """Show gap analysis for both vocabulary and grammar"""
    from gap_analysis.vocabulary_gaps import VocabularyGapAnalyzer
    from gap_analysis.grammar_gaps import GrammarGapAnalyzer

    vocab_analyzer = VocabularyGapAnalyzer(db, config)
    grammar_analyzer = GrammarGapAnalyzer(db, config)

    print(vocab_analyzer.get_gap_summary())
    print()
    print(grammar_analyzer.get_gap_summary())


def show_history(config):
    """Show execution history"""
    from core.batch_tracker import BatchExecutionTracker

    tracker = BatchExecutionTracker(config.execution_log_path, config.history_retention_days)

    print(tracker.get_history_display(limit=10))


def show_config(config):
    """Show current configuration"""
    print(config.get_summary())


def execute_batch(db, config, mode, force, verbose):
    """Execute batch feeding"""
    from batch_jobs.unified_feeder import UnifiedBatchFeeder

    # Set logging level based on verbose flag
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        for handler in logging.getLogger().handlers:
            handler.setLevel(logging.DEBUG)

    # Create unified feeder
    feeder = UnifiedBatchFeeder(db, config)

    # Execute
    print("\n🚀 Starting batch execution...")
    print(f"   Mode: {mode}")
    print(f"   Force: {force}")
    print()

    results = feeder.execute(mode=mode, force=force)

    # Print results
    print("\n" + "="*60)
    print("EXECUTION SUMMARY")
    print("="*60)
    print()

    # Vocabulary results
    if 'vocabulary' in results:
        vocab = results['vocabulary']
        print("📚 VOCABULARY:")
        print(f"   Status: {vocab.get('status', 'N/A')}")

        if vocab.get('status') == 'completed':
            vocab_results = vocab.get('results', {})
            print(f"   ✅ Generated: {vocab_results.get('generated', 0)} words")
            print(f"   ✅ Inserted: {vocab_results.get('inserted', 0)} words")
            print(f"   ⏭️  Skipped (duplicates): {vocab_results.get('skipped_duplicates', 0)} words")
            print(f"   🤖 AI Calls: {vocab_results.get('ai_calls', 0)}")
            print(f"   ⏱️  Duration: {vocab_results.get('duration_seconds', 0):.1f}s")
        elif vocab.get('status') == 'skipped':
            print(f"   ⏭️  Reason: {vocab.get('reason', 'N/A')}")
        else:
            print(f"   ❌ Reason: {vocab.get('reason', 'N/A')}")
            errors = vocab.get('results', {}).get('errors', [])
            if errors:
                print(f"   ❌ Errors: {len(errors)}")
                for error in errors[:3]:
                    print(f"      - {error}")

        print()

    # Grammar results
    if 'grammar' in results:
        grammar = results['grammar']
        print("✏️  GRAMMAR:")
        print(f"   Status: {grammar.get('status', 'N/A')}")

        if grammar.get('status') == 'completed':
            grammar_results = grammar.get('results', {})
            print(f"   Action: {grammar.get('action', 'N/A')}")
            print(f"   ✅ Exercises Generated: {grammar_results.get('exercises_generated', 0)}")
            print(f"   ✅ Exercises Inserted: {grammar_results.get('exercises_inserted', 0)}")
            print(f"   ⏭️  Skipped (duplicates): {grammar_results.get('skipped_duplicates', 0)}")

            if grammar_results.get('new_topics_created', 0) > 0:
                print(f"   🆕 New Topics Created: {grammar_results['new_topics_created']}")

            print(f"   🤖 AI Calls: {grammar_results.get('ai_calls', 0)}")
            print(f"   ⏱️  Duration: {grammar_results.get('duration_seconds', 0):.1f}s")
        elif grammar.get('status') == 'skipped':
            print(f"   ⏭️  Reason: {grammar.get('reason', 'N/A')}")
        else:
            print(f"   ❌ Reason: {grammar.get('reason', 'N/A')}")
            errors = grammar.get('results', {}).get('errors', [])
            if errors:
                print(f"   ❌ Errors: {len(errors)}")
                for error in errors[:3]:
                    print(f"      - {error}")

        print()

    print(f"⏱️  Total Duration: {results.get('total_duration', 0):.1f}s")
    print("="*60)

    # Show updated status
    print("\n📊 Updated Status:")
    show_status(db, config)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Batch Content Feeding System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Execute batches
  python batch_feed.py --vocabulary --verbose
  python batch_feed.py --grammar --verbose
  python batch_feed.py --both --verbose
  python batch_feed.py --both --force

  # Monitoring
  python batch_feed.py --status
  python batch_feed.py --gaps
  python batch_feed.py --history
  python batch_feed.py --config
        """
    )

    # Execution modes
    execution_group = parser.add_argument_group('Execution modes')
    execution_group.add_argument("--vocabulary", action="store_true", help="Run vocabulary batch")
    execution_group.add_argument("--grammar", action="store_true", help="Run grammar batch")
    execution_group.add_argument("--both", action="store_true", help="Run both batches (default)")
    execution_group.add_argument("--force", action="store_true", help="Bypass caps (use with caution)")

    # Monitoring modes
    monitoring_group = parser.add_argument_group('Monitoring modes')
    monitoring_group.add_argument("--status", action="store_true", help="Show current status")
    monitoring_group.add_argument("--gaps", action="store_true", help="Show gap analysis")
    monitoring_group.add_argument("--history", action="store_true", help="Show execution history (last 10)")
    monitoring_group.add_argument("--config", action="store_true", help="Show configuration")

    # Options
    parser.add_argument("--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        # Load configuration
        from core.batch_config import BatchConfig
        config = BatchConfig.load()

        # Setup database session
        from app.database import SessionLocal
        db = SessionLocal()

        try:
            # Handle monitoring commands
            if args.status:
                show_status(db, config)
            elif args.gaps:
                show_gaps(db, config)
            elif args.history:
                show_history(config)
            elif args.config:
                show_config(config)
            else:
                # Execute batch
                mode = "both"
                if args.vocabulary and not args.grammar:
                    mode = "vocabulary"
                elif args.grammar and not args.vocabulary:
                    mode = "grammar"

                execute_batch(db, config, mode, args.force, args.verbose)

        finally:
            db.close()

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
