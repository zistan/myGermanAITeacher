"""Progress tracking models for analytics and corrections."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Date,
    TIMESTAMP,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from app.database import Base


class ProgressSnapshot(Base):
    """
    Daily/periodic snapshots of user progress.
    Tracks metrics across all learning modules.
    """

    __tablename__ = "progress_snapshots"
    __table_args__ = (
        UniqueConstraint("user_id", "snapshot_date", name="uq_user_snapshot_date"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Snapshot date
    snapshot_date = Column(Date, server_default=func.current_date(), nullable=False, index=True)

    # Session metrics
    total_sessions = Column(Integer, default=0, nullable=False)
    total_practice_minutes = Column(Integer, default=0, nullable=False)

    # Vocabulary metrics
    vocabulary_learned = Column(Integer, default=0, nullable=False)
    vocabulary_mastered = Column(Integer, default=0, nullable=False)  # familiarity_score > 0.8

    # Grammar metrics
    grammar_topics_mastered = Column(Integer, default=0, nullable=False)  # mastery_level > 0.8
    grammar_topics_learning = Column(Integer, default=0, nullable=False)
    grammar_drill_sessions = Column(Integer, default=0, nullable=False)

    # Accuracy metrics
    avg_grammar_accuracy = Column(Float, nullable=True)
    avg_fluency_score = Column(Float, nullable=True)

    # Common errors (stored as JSON)
    common_errors = Column(JSON, nullable=True)  # Top grammar errors this period

    # Achievements
    achievements = Column(JSON, nullable=True)  # Milestones reached

    def __repr__(self) -> str:
        return f"<ProgressSnapshot(user_id={self.user_id}, date={self.snapshot_date})>"


class GrammarCorrection(Base):
    """
    Individual grammar corrections from conversations.
    Links errors to grammar topics for targeted practice.
    """

    __tablename__ = "grammar_corrections"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    turn_id = Column(Integer, ForeignKey("conversation_turns.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    grammar_topic_id = Column(Integer, ForeignKey("grammar_topics.id"), nullable=True, index=True)

    # Error details
    error_type = Column(String(100), nullable=False, index=True)  # case, gender, verb_conjugation, etc.
    incorrect_text = Column(Text, nullable=False)
    corrected_text = Column(Text, nullable=False)

    # Explanation and reference
    explanation = Column(Text, nullable=True)
    rule_reference = Column(Text, nullable=True)

    # Severity
    severity = Column(String(20), nullable=True)  # minor, moderate, major

    # Timestamp
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<GrammarCorrection(id={self.id}, user_id={self.user_id}, type='{self.error_type}', severity='{self.severity}')>"
