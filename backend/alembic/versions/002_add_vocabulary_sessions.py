"""Add vocabulary session tables for flashcards and quizzes

Revision ID: 002_add_vocabulary_sessions
Revises: 001_update_vocabulary_schema
Create Date: 2026-01-19 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision = '002_add_vocabulary_sessions'
down_revision = '001_update_vocabulary_schema'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create flashcard_sessions and vocabulary_quizzes tables."""

    # Create flashcard_sessions table
    op.create_table(
        'flashcard_sessions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('started_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False),
        sa.Column('ended_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('total_cards', sa.Integer(), nullable=False),
        sa.Column('current_index', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('cards_data', sa.Text(), nullable=False),
        sa.Column('use_spaced_repetition', sa.Integer(), nullable=False, server_default='1'),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('difficulty', sa.String(10), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create indexes for flashcard_sessions
    op.create_index('ix_flashcard_sessions_id', 'flashcard_sessions', ['id'])
    op.create_index('ix_flashcard_sessions_user_id', 'flashcard_sessions', ['user_id'])

    # Create vocabulary_quizzes table
    op.create_table(
        'vocabulary_quizzes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=func.now(), nullable=False),
        sa.Column('completed_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('quiz_type', sa.String(50), nullable=False),
        sa.Column('total_questions', sa.Integer(), nullable=False),
        sa.Column('questions_data', sa.Text(), nullable=False),
        sa.Column('category', sa.String(50), nullable=True),
        sa.Column('difficulty', sa.String(10), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )

    # Create indexes for vocabulary_quizzes
    op.create_index('ix_vocabulary_quizzes_id', 'vocabulary_quizzes', ['id'])
    op.create_index('ix_vocabulary_quizzes_user_id', 'vocabulary_quizzes', ['user_id'])


def downgrade() -> None:
    """Drop flashcard_sessions and vocabulary_quizzes tables."""

    # Drop indexes first
    op.drop_index('ix_vocabulary_quizzes_user_id', 'vocabulary_quizzes')
    op.drop_index('ix_vocabulary_quizzes_id', 'vocabulary_quizzes')
    op.drop_index('ix_flashcard_sessions_user_id', 'flashcard_sessions')
    op.drop_index('ix_flashcard_sessions_id', 'flashcard_sessions')

    # Drop tables
    op.drop_table('vocabulary_quizzes')
    op.drop_table('flashcard_sessions')
