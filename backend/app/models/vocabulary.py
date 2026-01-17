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


class UserVocabulary(Base):
    """
    Tracks user's progress with individual vocabulary items.
    Implements spaced repetition algorithm.
    """

    __tablename__ = "user_vocabulary"
    __table_args__ = (
        UniqueConstraint("user_id", "vocabulary_id", name="uq_user_vocabulary"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    vocabulary_id = Column(Integer, ForeignKey("vocabulary.id", ondelete="CASCADE"), nullable=False)

    # Progress metrics
    familiarity_score = Column(Float, default=0.0, nullable=False, index=True)  # 0.0 to 1.0
    times_encountered = Column(Integer, default=0, nullable=False)
    times_correct = Column(Integer, default=0, nullable=False)
    times_incorrect = Column(Integer, default=0, nullable=False)

    # Spaced repetition
    last_encountered = Column(TIMESTAMP, nullable=True)
    first_encountered = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    next_review_date = Column(TIMESTAMP, nullable=True, index=True)

    # Notes
    notes = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<UserVocabulary(user_id={self.user_id}, vocab_id={self.vocabulary_id}, score={self.familiarity_score:.2f})>"
