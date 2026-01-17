"""Pydantic schemas for user data validation."""
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema with common fields."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    native_language: str = Field(default="it", max_length=10)
    target_language: str = Field(default="de", max_length=10)
    proficiency_level: str = Field(default="B2", max_length=10)


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(..., min_length=8, max_length=100)


class UserUpdate(BaseModel):
    """Schema for updating user information."""

    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    proficiency_level: Optional[str] = Field(None, max_length=10)
    settings: Optional[dict] = None


class UserResponse(UserBase):
    """Schema for user response (without password)."""

    id: int
    created_at: datetime
    last_login: Optional[datetime] = None
    settings: dict = {}

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token payload data."""

    user_id: Optional[int] = None
    username: Optional[str] = None
