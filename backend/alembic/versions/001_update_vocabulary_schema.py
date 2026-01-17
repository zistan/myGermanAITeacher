"""Update vocabulary table schema to match model

Revision ID: 001_update_vocabulary_schema
Revises:
Create Date: 2026-01-17 23:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001_update_vocabulary_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Rename columns in vocabulary table
    op.alter_column('vocabulary', 'word_de', new_column_name='word')
    op.alter_column('vocabulary', 'word_it', new_column_name='translation_it')
    op.alter_column('vocabulary', 'difficulty_level', new_column_name='difficulty')
    op.alter_column('vocabulary', 'context_category', new_column_name='category')
    op.alter_column('vocabulary', 'example_sentence_de', new_column_name='example_de')
    op.alter_column('vocabulary', 'example_sentence_it', new_column_name='example_it')
    op.alter_column('vocabulary', 'notes', new_column_name='usage_notes')

    # Add new columns
    op.add_column('vocabulary', sa.Column('definition_de', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('pronunciation', sa.String(255), nullable=True))
    op.add_column('vocabulary', sa.Column('synonyms', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('antonyms', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('is_idiom', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('vocabulary', sa.Column('is_compound', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('vocabulary', sa.Column('is_separable_verb', sa.Integer(), nullable=False, server_default='0'))

    # Add is_public to user_vocabulary_lists
    op.add_column('user_vocabulary_lists', sa.Column('is_public', sa.Integer(), nullable=False, server_default='0'))


def downgrade() -> None:
    # Remove added columns
    op.drop_column('user_vocabulary_lists', 'is_public')
    op.drop_column('vocabulary', 'is_separable_verb')
    op.drop_column('vocabulary', 'is_compound')
    op.drop_column('vocabulary', 'is_idiom')
    op.drop_column('vocabulary', 'antonyms')
    op.drop_column('vocabulary', 'synonyms')
    op.drop_column('vocabulary', 'pronunciation')
    op.drop_column('vocabulary', 'definition_de')

    # Rename columns back
    op.alter_column('vocabulary', 'usage_notes', new_column_name='notes')
    op.alter_column('vocabulary', 'example_it', new_column_name='example_sentence_it')
    op.alter_column('vocabulary', 'example_de', new_column_name='example_sentence_de')
    op.alter_column('vocabulary', 'category', new_column_name='context_category')
    op.alter_column('vocabulary', 'difficulty', new_column_name='difficulty_level')
    op.alter_column('vocabulary', 'translation_it', new_column_name='word_it')
    op.alter_column('vocabulary', 'word', new_column_name='word_de')
