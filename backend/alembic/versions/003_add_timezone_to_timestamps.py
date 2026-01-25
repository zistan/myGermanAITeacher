"""Add timezone to all timestamp columns

Revision ID: 003_add_timezone_to_timestamps
Revises: 002_add_vocabulary_sessions
Create Date: 2026-01-25 15:39:38.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = '003_add_timezone_to_timestamps'
down_revision = '002_add_vocabulary_sessions'
branch_labels = None
depends_on = None


def table_exists(table_name):
    """Check if a table exists in the database."""
    conn = op.get_bind()
    inspector = inspect(conn)
    return table_name in inspector.get_table_names()


def column_exists(table_name, column_name):
    """Check if a column exists in a table."""
    conn = op.get_bind()
    inspector = inspect(conn)
    if not table_exists(table_name):
        return False
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns


def upgrade() -> None:
    """Convert all TIMESTAMP columns to TIMESTAMPTZ (timestamp with timezone)."""

    # Grammar Tables
    if column_exists('grammar_topics', 'created_at'):
        op.alter_column('grammar_topics', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('grammar_exercises', 'created_at'):
        op.alter_column('grammar_exercises', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('user_grammar_progress', 'last_practiced'):
        op.alter_column('user_grammar_progress', 'last_practiced',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('user_grammar_progress', 'next_review_date'):
        op.alter_column('user_grammar_progress', 'next_review_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('grammar_sessions', 'started_at'):
        op.alter_column('grammar_sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('grammar_sessions', 'ended_at'):
        op.alter_column('grammar_sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('grammar_exercise_attempts', 'timestamp'):
        op.alter_column('grammar_exercise_attempts', 'timestamp',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('diagnostic_tests', 'test_date'):
        op.alter_column('diagnostic_tests', 'test_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Session Tables (Conversation)
    if column_exists('sessions', 'started_at'):
        op.alter_column('sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('sessions', 'ended_at'):
        op.alter_column('sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('conversation_turns', 'timestamp'):
        op.alter_column('conversation_turns', 'timestamp',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Vocabulary Tables
    if column_exists('vocabulary', 'created_at'):
        op.alter_column('vocabulary', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('vocabulary', 'last_reviewed'):
        op.alter_column('vocabulary', 'last_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('user_vocabulary_progress', 'last_reviewed'):
        op.alter_column('user_vocabulary_progress', 'last_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('user_vocabulary_progress', 'first_reviewed'):
        op.alter_column('user_vocabulary_progress', 'first_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('user_vocabulary_progress', 'next_review_date'):
        op.alter_column('user_vocabulary_progress', 'next_review_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('user_vocabulary_lists', 'created_at'):
        op.alter_column('user_vocabulary_lists', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('user_vocabulary_lists', 'updated_at'):
        op.alter_column('user_vocabulary_lists', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('vocabulary_list_words', 'added_at'):
        op.alter_column('vocabulary_list_words', 'added_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('vocabulary_reviews', 'reviewed_at'):
        op.alter_column('vocabulary_reviews', 'reviewed_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('flashcard_sessions', 'started_at'):
        op.alter_column('flashcard_sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('flashcard_sessions', 'ended_at'):
        op.alter_column('flashcard_sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if column_exists('vocabulary_quizzes', 'created_at'):
        op.alter_column('vocabulary_quizzes', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('vocabulary_quizzes', 'completed_at'):
        op.alter_column('vocabulary_quizzes', 'completed_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    # User Tables
    if column_exists('users', 'created_at'):
        op.alter_column('users', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if column_exists('users', 'last_login'):
        op.alter_column('users', 'last_login',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    # Context Tables
    if column_exists('contexts', 'created_at'):
        op.alter_column('contexts', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Progress/Correction Tables
    if column_exists('grammar_corrections', 'created_at'):
        op.alter_column('grammar_corrections', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Achievement Tables (already DateTime, just add timezone=True)
    if column_exists('achievements', 'created_at'):
        op.alter_column('achievements', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=True)

    if column_exists('user_achievements', 'earned_at'):
        op.alter_column('user_achievements', 'earned_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=True)

    if column_exists('user_stats', 'last_activity_date'):
        op.alter_column('user_stats', 'last_activity_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=True)

    if column_exists('user_stats', 'updated_at'):
        op.alter_column('user_stats', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=True)

    if column_exists('progress_snapshots', 'snapshot_date'):
        op.alter_column('progress_snapshots', 'snapshot_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=False)

    if column_exists('progress_snapshots', 'created_at'):
        op.alter_column('progress_snapshots', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.DateTime(),
                        existing_nullable=True)


def downgrade() -> None:
    """Revert TIMESTAMPTZ columns back to TIMESTAMP (without timezone).
    Note: Only reverts columns that exist in the database."""

    # Grammar Tables
    if column_exists('grammar_topics', 'created_at'):
        op.alter_column('grammar_topics', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('grammar_exercises', 'created_at'):
        op.alter_column('grammar_exercises', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('user_grammar_progress', 'last_practiced'):
        op.alter_column('user_grammar_progress', 'last_practiced',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_grammar_progress', 'next_review_date'):
        op.alter_column('user_grammar_progress', 'next_review_date',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('grammar_sessions', 'started_at'):
        op.alter_column('grammar_sessions', 'started_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('grammar_sessions', 'ended_at'):
        op.alter_column('grammar_sessions', 'ended_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('grammar_exercise_attempts', 'timestamp'):
        op.alter_column('grammar_exercise_attempts', 'timestamp',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('diagnostic_tests', 'test_date'):
        op.alter_column('diagnostic_tests', 'test_date',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    # Session Tables (Conversation)
    if column_exists('sessions', 'started_at'):
        op.alter_column('sessions', 'started_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('sessions', 'ended_at'):
        op.alter_column('sessions', 'ended_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('conversation_turns', 'timestamp'):
        op.alter_column('conversation_turns', 'timestamp',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    # Vocabulary Tables
    if column_exists('vocabulary', 'created_at'):
        op.alter_column('vocabulary', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('vocabulary', 'last_reviewed'):
        op.alter_column('vocabulary', 'last_reviewed',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_vocabulary_progress', 'last_reviewed'):
        op.alter_column('user_vocabulary_progress', 'last_reviewed',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_vocabulary_progress', 'first_reviewed'):
        op.alter_column('user_vocabulary_progress', 'first_reviewed',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('user_vocabulary_progress', 'next_review_date'):
        op.alter_column('user_vocabulary_progress', 'next_review_date',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_vocabulary_lists', 'created_at'):
        op.alter_column('user_vocabulary_lists', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('user_vocabulary_lists', 'updated_at'):
        op.alter_column('user_vocabulary_lists', 'updated_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('vocabulary_list_words', 'added_at'):
        op.alter_column('vocabulary_list_words', 'added_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('vocabulary_reviews', 'reviewed_at'):
        op.alter_column('vocabulary_reviews', 'reviewed_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('flashcard_sessions', 'started_at'):
        op.alter_column('flashcard_sessions', 'started_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('flashcard_sessions', 'ended_at'):
        op.alter_column('flashcard_sessions', 'ended_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('vocabulary_quizzes', 'created_at'):
        op.alter_column('vocabulary_quizzes', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('vocabulary_quizzes', 'completed_at'):
        op.alter_column('vocabulary_quizzes', 'completed_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    # User Tables
    if column_exists('users', 'created_at'):
        op.alter_column('users', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('users', 'last_login'):
        op.alter_column('users', 'last_login',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    # Context Tables
    if column_exists('contexts', 'created_at'):
        op.alter_column('contexts', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    # Progress/Correction Tables
    if column_exists('grammar_corrections', 'created_at'):
        op.alter_column('grammar_corrections', 'created_at',
                        type_=sa.TIMESTAMP(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    # Achievement Tables (revert to DateTime without timezone)
    if column_exists('achievements', 'created_at'):
        op.alter_column('achievements', 'created_at',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_achievements', 'earned_at'):
        op.alter_column('user_achievements', 'earned_at',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_stats', 'last_activity_date'):
        op.alter_column('user_stats', 'last_activity_date',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('user_stats', 'updated_at'):
        op.alter_column('user_stats', 'updated_at',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)

    if column_exists('progress_snapshots', 'snapshot_date'):
        op.alter_column('progress_snapshots', 'snapshot_date',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=False)

    if column_exists('progress_snapshots', 'created_at'):
        op.alter_column('progress_snapshots', 'created_at',
                        type_=sa.DateTime(),
                        existing_type=sa.DateTime(timezone=True),
                        existing_nullable=True)
