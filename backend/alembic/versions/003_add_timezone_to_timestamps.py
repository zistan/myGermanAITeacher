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


def upgrade() -> None:
    """Convert all TIMESTAMP columns to TIMESTAMPTZ (timestamp with timezone)."""

    # Grammar Tables
    if table_exists('grammar_topics'):
        op.alter_column('grammar_topics', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('grammar_exercises'):
        op.alter_column('grammar_exercises', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('user_grammar_progress'):
        op.alter_column('user_grammar_progress', 'last_practiced',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

        op.alter_column('user_grammar_progress', 'next_review_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('grammar_sessions'):
        op.alter_column('grammar_sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('grammar_sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('grammar_exercise_attempts'):
        op.alter_column('grammar_exercise_attempts', 'timestamp',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('diagnostic_tests'):
        op.alter_column('diagnostic_tests', 'test_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Session Tables (Conversation)
    if table_exists('sessions'):
        op.alter_column('sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('conversation_turns'):
        op.alter_column('conversation_turns', 'timestamp',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Vocabulary Tables
    if table_exists('vocabulary'):
        op.alter_column('vocabulary', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('vocabulary', 'last_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('user_vocabulary_progress'):
        op.alter_column('user_vocabulary_progress', 'last_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

        op.alter_column('user_vocabulary_progress', 'first_reviewed',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('user_vocabulary_progress', 'next_review_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('user_vocabulary_lists'):
        op.alter_column('user_vocabulary_lists', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('user_vocabulary_lists', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('vocabulary_list_words'):
        op.alter_column('vocabulary_list_words', 'added_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('vocabulary_reviews'):
        op.alter_column('vocabulary_reviews', 'reviewed_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    if table_exists('flashcard_sessions'):
        op.alter_column('flashcard_sessions', 'started_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('flashcard_sessions', 'ended_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('vocabulary_quizzes'):
        op.alter_column('vocabulary_quizzes', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('vocabulary_quizzes', 'completed_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    # User Tables
    if table_exists('users'):
        op.alter_column('users', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('users', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Context Tables
    if table_exists('contexts'):
        op.alter_column('contexts', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('contexts', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Progress/Correction Tables
    if table_exists('grammar_corrections'):
        op.alter_column('grammar_corrections', 'timestamp',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

    # Achievement Tables
    if table_exists('achievements'):
        op.alter_column('achievements', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('user_achievements'):
        op.alter_column('user_achievements', 'earned_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('user_stats'):
        op.alter_column('user_stats', 'last_activity_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

        op.alter_column('user_stats', 'updated_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)

    if table_exists('progress_snapshots'):
        op.alter_column('progress_snapshots', 'snapshot_date',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=False)

        op.alter_column('progress_snapshots', 'created_at',
                        type_=sa.DateTime(timezone=True),
                        existing_type=sa.TIMESTAMP(),
                        existing_nullable=True)


def downgrade() -> None:
    """Revert TIMESTAMPTZ columns back to TIMESTAMP (without timezone)."""

    # Grammar Tables
    op.alter_column('grammar_topics', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('grammar_exercises', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('user_grammar_progress', 'last_practiced',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_grammar_progress', 'next_review_date',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('grammar_sessions', 'started_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('grammar_sessions', 'ended_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('grammar_exercise_attempts', 'timestamp',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('diagnostic_tests', 'test_date',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    # Session Tables (Conversation)
    op.alter_column('sessions', 'started_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('sessions', 'ended_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('conversation_turns', 'timestamp',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    # Vocabulary Tables
    op.alter_column('vocabulary', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('vocabulary', 'last_reviewed',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_vocabulary_progress', 'last_reviewed',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_vocabulary_progress', 'first_reviewed',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('user_vocabulary_progress', 'next_review_date',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_vocabulary_lists', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('user_vocabulary_lists', 'updated_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('vocabulary_list_words', 'added_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('vocabulary_reviews', 'reviewed_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('flashcard_sessions', 'started_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('flashcard_sessions', 'ended_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('vocabulary_quizzes', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('vocabulary_quizzes', 'completed_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    # User Tables
    op.alter_column('users', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('users', 'updated_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    # Context Tables
    op.alter_column('contexts', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('contexts', 'updated_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    # Progress/Correction Tables
    op.alter_column('grammar_corrections', 'timestamp',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    # Achievement Tables
    op.alter_column('achievements', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_achievements', 'earned_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_stats', 'last_activity_date',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('user_stats', 'updated_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)

    op.alter_column('progress_snapshots', 'snapshot_date',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)

    op.alter_column('progress_snapshots', 'created_at',
                    type_=sa.TIMESTAMP(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=True)
