"""Vocabulary models for word management and user progress."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    TIMESTAMP,
    ForeignKey,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Vocabulary(Base):
    """
    Vocabulary items with German, Italian, and English translations.
    Categorized by difficulty and context.
    """

    __tablename__ = "vocabulary"

    id = Column(Integer, primary_key=True, index=True)

    # Translations
    word_de = Column(String(255), nullable=False, index=True)
    word_it = Column(String(255), nullable=False)
    word_en = Column(String(255), nullable=True)

    # Grammatical information
    part_of_speech = Column(String(50), nullable=True)  # noun, verb, adjective, etc.
    gender = Column(String(10), nullable=True)  # der, die, das
    plural_form = Column(String(255), nullable=True)

    # Categorization
    difficulty_level = Column(String(10), nullable=True, index=True)  # B1, B2, C1, C2
    context_category = Column(String(50), nullable=True, index=True)  # business, daily, finance

    # Examples and notes
    example_sentence_de = Column(Text, nullable=True)
    example_sentence_it = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Tracking
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    last_reviewed = Column(TIMESTAMP, nullable=True)
    review_count = Column(Integer, default=0, nullable=False)

    def __repr__(self) -> str:
        return f"<Vocabulary(id={self.id}, word_de='{self.word_de}', level='{self.difficulty_level}')>"


class UserVocabularyProgress(Base):
    """
    Tracks user's progress with individual vocabulary items.
    Implements spaced repetition algorithm (SM-2 inspired).
    """

    __tablename__ = "user_vocabulary_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "word_id", name="uq_user_vocabulary_progress"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False)

    # Progress metrics (6 mastery levels: 0-5)
    mastery_level = Column(Integer, default=0, nullable=False, index=True)  # 0=new, 1-5=increasing mastery
    confidence_score = Column(Float, default=0.0, nullable=False)  # 0.0 to 1.0
    times_reviewed = Column(Integer, default=0, nullable=False)
    times_correct = Column(Integer, default=0, nullable=False)
    times_incorrect = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)

    # Spaced repetition (SM-2 inspired)
    last_reviewed = Column(TIMESTAMP, nullable=True)
    first_reviewed = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    next_review_date = Column(TIMESTAMP, nullable=True, index=True)
    ease_factor = Column(Float, default=2.5, nullable=False)  # SM-2 algorithm ease factor
    interval_days = Column(Integer, default=1, nullable=False)  # Days until next review

    # Personal notes
    personal_note = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<UserVocabularyProgress(user_id={self.user_id}, word_id={self.word_id}, mastery={self.mastery_level})>"


class UserVocabularyList(Base):
    """
    User's custom vocabulary lists for organizing words.
    """

    __tablename__ = "user_vocabulary_lists"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # List details
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    color = Column(String(50), nullable=True)  # For UI organization

    # Tracking
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<UserVocabularyList(id={self.id}, user_id={self.user_id}, name='{self.name}')>"


class VocabularyListWord(Base):
    """
    Association table linking vocabulary words to user lists.
    """

    __tablename__ = "vocabulary_list_words"
    __table_args__ = (
        UniqueConstraint("list_id", "word_id", name="uq_list_word"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    list_id = Column(Integer, ForeignKey("user_vocabulary_lists.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False, index=True)

    # Custom notes for this word in this list
    notes = Column(Text, nullable=True)

    # Tracking
    added_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<VocabularyListWord(list_id={self.list_id}, word_id={self.word_id})>"


class VocabularyReview(Base):
    """
    Historical record of vocabulary review sessions.
    Tracks each flashcard review for analytics.
    """

    __tablename__ = "vocabulary_reviews"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    word_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False, index=True)

    # Review details
    review_type = Column(String(50), nullable=False)  # flashcard, quiz, conversation
    was_correct = Column(Integer, nullable=False)  # 0=incorrect, 1=correct
    confidence_rating = Column(Integer, nullable=True)  # 1-5, optional user rating
    time_spent_seconds = Column(Integer, nullable=True)

    # Timestamp
    reviewed_at = Column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)

    def __repr__(self) -> str:
        return f"<VocabularyReview(user_id={self.user_id}, word_id={self.word_id}, correct={self.was_correct})>"
