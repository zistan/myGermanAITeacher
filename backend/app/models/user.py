"""User model for authentication and user management."""
from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    """
    User model representing application users.
    Stores authentication credentials and user preferences.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)

    # Language settings
    native_language = Column(String(10), default="it", nullable=False)
    target_language = Column(String(10), default="de", nullable=False)
    proficiency_level = Column(String(10), default="B2", nullable=False)  # A1-C2

    # Timestamps
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    last_login = Column(TIMESTAMP, nullable=True)

    # User settings stored as JSON
    settings = Column(JSON, default={}, nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}', level='{self.proficiency_level}')>"
