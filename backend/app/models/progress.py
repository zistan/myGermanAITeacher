"""Progress tracking models for analytics and corrections."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    TIMESTAMP,
    ForeignKey
)
from sqlalchemy.sql import func
from app.database import Base


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
