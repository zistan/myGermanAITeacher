"""Context model for conversation scenarios."""
from sqlalchemy import Column, Integer, String, Text, Boolean, TIMESTAMP, JSON, Index
from sqlalchemy.sql import func
from app.database import Base


class Context(Base):
    """
    Conversation contexts/scenarios (e.g., business meeting, restaurant, etc.).
    Defines the setting and system prompts for AI conversations.
    """

    __tablename__ = "contexts"

    id = Column(Integer, primary_key=True, index=True)

    # Basic information
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False, index=True)  # business, daily, finance, social
    difficulty_level = Column(String(10), nullable=True, index=True)  # B1, B2, C1, C2
    description = Column(Text, nullable=True)

    # AI configuration
    system_prompt = Column(Text, nullable=False)  # System prompt for Claude

    # Suggested vocabulary (array of vocabulary IDs)
    suggested_vocab = Column(JSON, default=[], nullable=False)

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Tracking
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Context(id={self.id}, name='{self.name}', category='{self.category}')>"
