"""Session and conversation models for practice sessions."""
from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ForeignKey, JSON, Index
from sqlalchemy.sql import func
from app.database import Base


class Session(Base):
    """
    Practice sessions (conversation, vocabulary review, etc.).
    Tracks session progress and scores.
    """

    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    context_id = Column(Integer, ForeignKey("contexts.id"), nullable=True, index=True)

    # Session type
    session_type = Column(String(50), default="conversation", nullable=False)  # conversation, vocab_review, mixed

    # Timing
    started_at = Column(TIMESTAMP, server_default=func.now(), nullable=False, index=True)
    ended_at = Column(TIMESTAMP, nullable=True)
    duration_minutes = Column(Integer, nullable=True)

    # Metrics
    total_turns = Column(Integer, default=0, nullable=False)
    grammar_errors = Column(Integer, default=0, nullable=False)
    vocab_score = Column(Float, nullable=True)  # 0.0 to 1.0
    fluency_score = Column(Float, nullable=True)  # 0.0 to 1.0
    overall_score = Column(Float, nullable=True)  # 0.0 to 1.0

    # AI model tracking
    ai_model_used = Column(String(50), nullable=True)

    # Summary and metadata
    session_summary = Column(Text, nullable=True)
    metadata = Column(JSON, default={}, nullable=False)

    def __repr__(self) -> str:
        return f"<Session(id={self.id}, user_id={self.user_id}, type='{self.session_type}')>"


class ConversationTurn(Base):
    """
    Individual messages/turns in a conversation session.
    Stores user and AI messages with feedback.
    """

    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)

    # Turn information
    turn_number = Column(Integer, nullable=False)
    speaker = Column(String(20), nullable=False)  # 'user' or 'ai'
    message_text = Column(Text, nullable=False)

    # Timestamp
    timestamp = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    # Feedback and analysis (stored as JSON)
    grammar_feedback = Column(JSON, nullable=True)  # Array of grammar corrections
    vocabulary_used = Column(JSON, nullable=True)  # Array of vocabulary IDs detected
    ai_evaluation = Column(JSON, nullable=True)  # AI's assessment of the turn

    # Metadata
    metadata = Column(JSON, default={}, nullable=False)

    def __repr__(self) -> str:
        return f"<ConversationTurn(id={self.id}, session_id={self.session_id}, turn={self.turn_number}, speaker='{self.speaker}')>"


# Create composite index for efficient querying
Index("idx_conversation_turns_session_turn", ConversationTurn.session_id, ConversationTurn.turn_number)
