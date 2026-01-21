"""Add unique constraint to vocabulary.word

Revision ID: 003_add_vocabulary_word_unique
Revises: 002_add_vocabulary_sessions
Create Date: 2026-01-21

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003_add_vocabulary_word_unique'
down_revision = '002_add_vocabulary_sessions'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add unique constraint to vocabulary.word column
    # This allows ON CONFLICT (word) DO NOTHING in bulk insert
    op.create_unique_constraint('uq_vocabulary_word', 'vocabulary', ['word'])


def downgrade() -> None:
    # Remove unique constraint
    op.drop_constraint('uq_vocabulary_word', 'vocabulary', type_='unique')
