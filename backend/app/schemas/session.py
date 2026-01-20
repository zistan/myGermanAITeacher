"""Pydantic schemas for session and conversation data."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime


# ============ Session Schemas ============

class SessionStart(BaseModel):
    """Schema for starting a new session."""
    context_id: Optional[int] = None
    session_type: str = Field(default="conversation", pattern="^(conversation|vocab_review|mixed)$")


class SessionResponse(BaseModel):
    """Schema for session response."""
    id: int
    user_id: int
    context_id: Optional[int] = None
    session_type: str
    start_time: datetime = Field(alias="started_at")  # Frontend expects start_time
    end_time: Optional[datetime] = Field(default=None, alias="ended_at")  # Frontend expects end_time
    duration_minutes: Optional[int] = None
    total_turns: int = 0
    grammar_errors: int = 0
    vocab_score: Optional[float] = None
    fluency_score: Optional[float] = None
    overall_score: Optional[float] = None
    ai_model_used: Optional[str] = None
    session_summary: Optional[str] = None
    session_metadata: Dict[str, Any] = Field(default_factory=dict, alias="metadata")

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class SessionWithContext(SessionResponse):
    """Session response with context details - matches frontend expectations."""
    context_name: str = ""
    context_description: str = ""
    context_category: str = ""
    context_difficulty: str = ""
    grammar_corrections: int = Field(default=0, description="Alias for grammar_errors")
    vocabulary_used: int = Field(default=0, description="Count of vocabulary items detected")


# ============ Conversation Turn Schemas ============

class MessageSend(BaseModel):
    """Schema for sending a message in conversation."""
    message: str = Field(..., min_length=1, max_length=5000)
    request_feedback: bool = True


class GrammarFeedbackItem(BaseModel):
    """Schema for individual grammar correction."""
    error_type: str
    incorrect_text: str
    corrected_text: str
    explanation: str
    severity: str
    rule: Optional[str] = None
    grammar_topic_hint: Optional[str] = None


class VocabularyItem(BaseModel):
    """Schema for detected vocabulary item."""
    word: str
    familiarity_score: float = 0.0
    is_new: bool = False


class MessageResponse(BaseModel):
    """Schema for AI response to user message."""
    turn_id: int
    user_message: str  # Echo back the user's message for frontend display
    ai_response: str
    turn_number: int  # Current turn number in the conversation
    grammar_feedback: List[GrammarFeedbackItem] = []
    vocabulary_detected: List[VocabularyItem] = []
    suggestions: List[str] = []


class ConversationTurnResponse(BaseModel):
    """Schema for conversation turn details."""
    id: int
    session_id: int
    turn_number: int
    speaker: str
    message_text: str
    timestamp: datetime
    grammar_feedback: Optional[List[Dict]] = None
    vocabulary_used: Optional[List[int]] = None
    ai_evaluation: Optional[Dict] = None

    model_config = ConfigDict(from_attributes=True)


# ============ Session Summary Schemas ============

class SessionSummary(BaseModel):
    """Schema for session summary after completion."""
    duration_minutes: int
    total_turns: int
    grammar_accuracy: float
    vocabulary_used_count: int
    new_vocabulary_count: int
    overall_score: float
    achievements: List[str] = []
    areas_for_improvement: List[Dict[str, Any]] = []


class SessionEndResponse(BaseModel):
    """Schema for session end response."""
    session_summary: SessionSummary
    grammar_topics_to_practice: List[Dict[str, Any]] = []


# ============ Session History Schemas ============

class SessionHistoryResponse(BaseModel):
    """Schema for retrieving session history."""
    session: SessionResponse
    conversation: List[ConversationTurnResponse]
