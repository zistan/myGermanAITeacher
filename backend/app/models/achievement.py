"""
Achievement and badge models for gamification.
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database import Base


class Achievement(Base):
    """Achievement definitions."""
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)  # conversation, grammar, vocabulary, activity
    badge_icon = Column(String(50))  # Icon identifier
    badge_color = Column(String(20))  # Color for badge display

    # Achievement criteria
    criteria_type = Column(String(50), nullable=False)  # sessions_count, words_learned, streak, mastery, etc.
    criteria_value = Column(Integer, nullable=False)  # Threshold value
    criteria_metadata = Column(JSON, nullable=True)  # Additional criteria details

    # Difficulty/rarity
    tier = Column(String(20), nullable=False)  # bronze, silver, gold, platinum
    points = Column(Integer, default=0)  # Achievement points awarded

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")


class UserAchievement(Base):
    """User's earned achievements."""
    __tablename__ = "user_achievements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False)

    earned_at = Column(DateTime, default=datetime.utcnow)
    progress_value = Column(Integer, default=0)  # Current progress toward achievement
    is_completed = Column(Boolean, default=False)

    # Display settings
    is_showcased = Column(Boolean, default=False)  # Display on profile
    showcase_order = Column(Integer, default=0)

    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")


class UserStats(Base):
    """Aggregate user statistics for leaderboards and comparisons."""
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)

    # Overall stats
    total_study_time_minutes = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    current_streak_days = Column(Integer, default=0)
    longest_streak_days = Column(Integer, default=0)
    last_activity_date = Column(DateTime)

    # Conversation stats
    conversation_sessions = Column(Integer, default=0)
    total_messages_sent = Column(Integer, default=0)

    # Grammar stats
    grammar_sessions = Column(Integer, default=0)
    grammar_exercises_completed = Column(Integer, default=0)
    grammar_exercises_correct = Column(Integer, default=0)
    grammar_topics_mastered = Column(Integer, default=0)
    average_grammar_accuracy = Column(Integer, default=0)  # Percentage

    # Vocabulary stats
    vocabulary_words_learned = Column(Integer, default=0)
    vocabulary_words_mastered = Column(Integer, default=0)
    vocabulary_reviews_completed = Column(Integer, default=0)
    vocabulary_reviews_correct = Column(Integer, default=0)
    average_vocabulary_accuracy = Column(Integer, default=0)  # Percentage

    # Achievement stats
    total_achievement_points = Column(Integer, default=0)
    achievements_earned = Column(Integer, default=0)

    # Rankings (updated periodically)
    overall_rank = Column(Integer)
    grammar_rank = Column(Integer)
    vocabulary_rank = Column(Integer)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="stats")


class ProgressSnapshot(Base):
    """Point-in-time snapshots of user progress."""
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    snapshot_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    snapshot_type = Column(String(50), default="weekly")  # daily, weekly, monthly

    # Snapshot data (JSON)
    overall_progress = Column(JSON, nullable=False)
    conversation_stats = Column(JSON)
    grammar_stats = Column(JSON)
    vocabulary_stats = Column(JSON)
    activity_stats = Column(JSON)
    error_analysis = Column(JSON)

    # Summary metrics
    overall_score = Column(Integer)  # 0-100
    total_sessions = Column(Integer)
    study_time_minutes = Column(Integer)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="progress_snapshots")
