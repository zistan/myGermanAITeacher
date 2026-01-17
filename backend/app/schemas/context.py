"""Pydantic schemas for context data."""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class ContextBase(BaseModel):
    """Base context schema."""
    name: str = Field(..., min_length=3, max_length=100)
    category: str = Field(..., pattern="^(business|daily|finance|social|technical|general)$")
    difficulty_level: Optional[str] = Field(None, pattern="^(A1|A2|B1|B2|C1|C2)$")
    description: Optional[str] = None


class ContextCreate(ContextBase):
    """Schema for creating a new context."""
    system_prompt: str = Field(..., min_length=20)
    suggested_vocab: List[int] = []
    is_active: bool = True


class ContextUpdate(BaseModel):
    """Schema for updating a context."""
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    description: Optional[str] = None
    system_prompt: Optional[str] = None
    suggested_vocab: Optional[List[int]] = None
    is_active: Optional[bool] = None


class ContextResponse(ContextBase):
    """Schema for context response."""
    id: int
    system_prompt: str
    suggested_vocab: List[int]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContextListItem(BaseModel):
    """Schema for context in list view."""
    id: int
    name: str
    category: str
    difficulty_level: Optional[str] = None
    description: Optional[str] = None
    times_used: int = 0
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ContextWithStats(ContextResponse):
    """Context with usage statistics."""
    times_used: int = 0
    average_score: Optional[float] = None
    last_used: Optional[datetime] = None
