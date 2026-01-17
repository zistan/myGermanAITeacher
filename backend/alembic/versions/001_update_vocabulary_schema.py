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
    # === Update vocabulary table ===
    # Rename columns to match model
    op.alter_column('vocabulary', 'word_de', new_column_name='word')
    op.alter_column('vocabulary', 'word_it', new_column_name='translation_it')
    op.alter_column('vocabulary', 'difficulty_level', new_column_name='difficulty')
    op.alter_column('vocabulary', 'context_category', new_column_name='category')
    op.alter_column('vocabulary', 'example_sentence_de', new_column_name='example_de')
    op.alter_column('vocabulary', 'example_sentence_it', new_column_name='example_it')
    op.alter_column('vocabulary', 'notes', new_column_name='usage_notes')

    # Add new columns to vocabulary
    op.add_column('vocabulary', sa.Column('definition_de', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('pronunciation', sa.String(255), nullable=True))
    op.add_column('vocabulary', sa.Column('synonyms', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('antonyms', sa.Text(), nullable=True))
    op.add_column('vocabulary', sa.Column('is_idiom', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('vocabulary', sa.Column('is_compound', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('vocabulary', sa.Column('is_separable_verb', sa.Integer(), nullable=False, server_default='0'))

    # === Update user_vocabulary table to match UserVocabularyProgress model ===
    # Rename table
    op.rename_table('user_vocabulary', 'user_vocabulary_progress')

    # Rename columns
    op.alter_column('user_vocabulary_progress', 'vocabulary_id', new_column_name='word_id')
    op.alter_column('user_vocabulary_progress', 'familiarity_score', new_column_name='confidence_score')
    op.alter_column('user_vocabulary_progress', 'times_encountered', new_column_name='times_reviewed')
    op.alter_column('user_vocabulary_progress', 'last_encountered', new_column_name='last_reviewed')
    op.alter_column('user_vocabulary_progress', 'notes', new_column_name='personal_note')

    # Add new columns
    op.add_column('user_vocabulary_progress', sa.Column('mastery_level', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user_vocabulary_progress', sa.Column('current_streak', sa.Integer(), nullable=False, server_default='0'))
    op.add_column('user_vocabulary_progress', sa.Column('ease_factor', sa.Float(), nullable=False, server_default='2.5'))
    op.add_column('user_vocabulary_progress', sa.Column('interval_days', sa.Integer(), nullable=False, server_default='1'))

    # === Create new tables ===
    # user_vocabulary_lists
    op.create_table(
        'user_vocabulary_lists',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_public', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('color', sa.String(50), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE')
    )
    op.create_index('ix_user_vocabulary_lists_user_id', 'user_vocabulary_lists', ['user_id'])

    # vocabulary_list_words
    op.create_table(
        'vocabulary_list_words',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('list_id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('added_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['list_id'], ['user_vocabulary_lists.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['word_id'], ['vocabulary.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('list_id', 'word_id', name='uq_list_word')
    )
    op.create_index('ix_vocabulary_list_words_list_id', 'vocabulary_list_words', ['list_id'])
    op.create_index('ix_vocabulary_list_words_word_id', 'vocabulary_list_words', ['word_id'])

    # vocabulary_reviews
    op.create_table(
        'vocabulary_reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('word_id', sa.Integer(), nullable=False),
        sa.Column('review_type', sa.String(50), nullable=False),
        sa.Column('was_correct', sa.Integer(), nullable=False),
        sa.Column('confidence_rating', sa.Integer(), nullable=True),
        sa.Column('time_spent_seconds', sa.Integer(), nullable=True),
        sa.Column('reviewed_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['word_id'], ['vocabulary.id'], ondelete='CASCADE')
    )
    op.create_index('ix_vocabulary_reviews_user_id', 'vocabulary_reviews', ['user_id'])
    op.create_index('ix_vocabulary_reviews_word_id', 'vocabulary_reviews', ['word_id'])
    op.create_index('ix_vocabulary_reviews_reviewed_at', 'vocabulary_reviews', ['reviewed_at'])


def downgrade() -> None:
    # Drop new tables
    op.drop_index('ix_vocabulary_reviews_reviewed_at', 'vocabulary_reviews')
    op.drop_index('ix_vocabulary_reviews_word_id', 'vocabulary_reviews')
    op.drop_index('ix_vocabulary_reviews_user_id', 'vocabulary_reviews')
    op.drop_table('vocabulary_reviews')

    op.drop_index('ix_vocabulary_list_words_word_id', 'vocabulary_list_words')
    op.drop_index('ix_vocabulary_list_words_list_id', 'vocabulary_list_words')
    op.drop_table('vocabulary_list_words')

    op.drop_index('ix_user_vocabulary_lists_user_id', 'user_vocabulary_lists')
    op.drop_table('user_vocabulary_lists')

    # Remove added columns from user_vocabulary_progress
    op.drop_column('user_vocabulary_progress', 'interval_days')
    op.drop_column('user_vocabulary_progress', 'ease_factor')
    op.drop_column('user_vocabulary_progress', 'current_streak')
    op.drop_column('user_vocabulary_progress', 'mastery_level')

    # Rename columns back in user_vocabulary_progress
    op.alter_column('user_vocabulary_progress', 'personal_note', new_column_name='notes')
    op.alter_column('user_vocabulary_progress', 'last_reviewed', new_column_name='last_encountered')
    op.alter_column('user_vocabulary_progress', 'times_reviewed', new_column_name='times_encountered')
    op.alter_column('user_vocabulary_progress', 'confidence_score', new_column_name='familiarity_score')
    op.alter_column('user_vocabulary_progress', 'word_id', new_column_name='vocabulary_id')

    # Rename table back
    op.rename_table('user_vocabulary_progress', 'user_vocabulary')

    # Remove added columns from vocabulary
    op.drop_column('vocabulary', 'is_separable_verb')
    op.drop_column('vocabulary', 'is_compound')
    op.drop_column('vocabulary', 'is_idiom')
    op.drop_column('vocabulary', 'antonyms')
    op.drop_column('vocabulary', 'synonyms')
    op.drop_column('vocabulary', 'pronunciation')
    op.drop_column('vocabulary', 'definition_de')

    # Rename columns back in vocabulary
    op.alter_column('vocabulary', 'usage_notes', new_column_name='notes')
    op.alter_column('vocabulary', 'example_it', new_column_name='example_sentence_it')
    op.alter_column('vocabulary', 'example_de', new_column_name='example_sentence_de')
    op.alter_column('vocabulary', 'category', new_column_name='context_category')
    op.alter_column('vocabulary', 'difficulty', new_column_name='difficulty_level')
    op.alter_column('vocabulary', 'translation_it', new_column_name='word_it')
    op.alter_column('vocabulary', 'word', new_column_name='word_de')
