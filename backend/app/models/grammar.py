"""Grammar learning models for topics, exercises, and progress tracking."""
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    JSON,
    UniqueConstraint,
    Index
)
from sqlalchemy.sql import func
from app.database import Base


class GrammarTopic(Base):
    """
    Grammar topics/rules (e.g., Dativ case, Perfect tense, etc.).
    Hierarchical structure with parent-child relationships.
    """

    __tablename__ = "grammar_topics"

    id = Column(Integer, primary_key=True, index=True)

    # Topic information
    name_de = Column(String(255), nullable=False)  # German name
    name_en = Column(String(255), nullable=True)  # English name
    category = Column(String(100), nullable=False, index=True)  # cases, verbs, sentence_structure, etc.
    subcategory = Column(String(100), nullable=True)

    # Difficulty and hierarchy
    difficulty_level = Column(String(10), nullable=True, index=True)  # A1, A2, B1, B2, C1, C2
    parent_topic_id = Column(Integer, ForeignKey("grammar_topics.id"), nullable=True)
    order_index = Column(Integer, nullable=True)  # For sequential learning path

    # Explanations
    description_de = Column(Text, nullable=True)
    explanation_de = Column(Text, nullable=True)  # Detailed grammar explanation in German

    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<GrammarTopic(id={self.id}, name='{self.name_de}', category='{self.category}')>"


class GrammarExercise(Base):
    """
    Grammar exercises for practice and drilling.
    Supports multiple exercise types (fill-blank, multiple choice, etc.).
    """

    __tablename__ = "grammar_exercises"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    topic_id = Column(Integer, ForeignKey("grammar_topics.id"), nullable=True, index=True)

    # Exercise type and difficulty
    exercise_type = Column(String(50), nullable=False, index=True)  # fill_blank, multiple_choice, etc.
    difficulty_level = Column(String(10), nullable=True, index=True)

    # Exercise content
    question_text = Column(Text, nullable=False)
    question_data = Column(JSON, default={}, nullable=False)  # Exercise-specific data (options, blanks, etc.)

    # Answers
    correct_answer = Column(Text, nullable=False)
    alternative_answers = Column(JSON, nullable=True)  # Array of acceptable alternatives

    # Explanations and hints
    explanation_de = Column(Text, nullable=False)
    explanation_it = Column(Text, nullable=True)  # Optional Italian explanation
    hints = Column(JSON, nullable=True)  # Array of progressive hints

    # Categorization
    context_category = Column(String(50), nullable=True)  # business, daily, general

    # Source and status
    source = Column(String(50), default="manual", nullable=False)  # manual, ai_generated
    is_active = Column(Boolean, default=True, nullable=False)

    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    exercise_metadata = Column("metadata", JSON, default={}, nullable=False)

    def __repr__(self) -> str:
        return f"<GrammarExercise(id={self.id}, topic_id={self.topic_id}, type='{self.exercise_type}')>"


class UserGrammarProgress(Base):
    """
    Tracks user's progress per grammar topic.
    Implements spaced repetition for grammar topics.
    """

    __tablename__ = "user_grammar_progress"
    __table_args__ = (
        UniqueConstraint("user_id", "topic_id", name="uq_user_grammar_topic"),
    )

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("grammar_topics.id"), nullable=False)

    # Progress metrics
    mastery_level = Column(Float, default=0.0, nullable=False, index=True)  # 0.0 to 1.0
    total_exercises_attempted = Column(Integer, default=0, nullable=False)
    total_exercises_correct = Column(Integer, default=0, nullable=False)
    total_exercises_incorrect = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)

    # Spaced repetition
    last_practiced = Column(DateTime(timezone=True), nullable=True)
    next_review_date = Column(DateTime(timezone=True), nullable=True, index=True)

    # Weak areas
    weak_subtopics = Column(JSON, nullable=True)  # Array of problematic subtopics

    # Notes
    notes = Column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<UserGrammarProgress(user_id={self.user_id}, topic_id={self.topic_id}, mastery={self.mastery_level:.2f})>"


class GrammarSession(Base):
    """
    Grammar practice/drill sessions.
    Tracks user's performance during focused grammar practice.
    """

    __tablename__ = "grammar_sessions"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("grammar_topics.id"), nullable=True, index=True)
    triggered_by_conversation_id = Column(Integer, ForeignKey("sessions.id"), nullable=True)

    # Session type
    session_type = Column(String(50), default="drill", nullable=False)  # drill, diagnostic, review, conversation_triggered

    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    ended_at = Column(DateTime(timezone=True), nullable=True)

    # Performance metrics
    total_exercises = Column(Integer, default=0, nullable=False)
    exercises_correct = Column(Integer, default=0, nullable=False)
    exercises_incorrect = Column(Integer, default=0, nullable=False)
    accuracy_rate = Column(Float, nullable=True)
    completion_rate = Column(Float, nullable=True)

    # Summary
    session_summary = Column(JSON, nullable=True)
    grammar_metadata = Column("metadata", JSON, default={}, nullable=False)

    def __repr__(self) -> str:
        return f"<GrammarSession(id={self.id}, user_id={self.user_id}, type='{self.session_type}')>"


class GrammarExerciseAttempt(Base):
    """
    Individual exercise attempts during grammar sessions.
    Stores user answers and correctness.
    """

    __tablename__ = "grammar_exercise_attempts"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign keys
    grammar_session_id = Column(Integer, ForeignKey("grammar_sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("grammar_exercises.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Attempt data
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    time_spent_seconds = Column(Integer, nullable=True)
    hints_used = Column(Integer, default=0, nullable=False)
    attempt_number = Column(Integer, default=1, nullable=False)  # If user retries

    # Feedback
    feedback_given = Column(Text, nullable=True)

    # Timestamp
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<GrammarExerciseAttempt(id={self.id}, exercise_id={self.exercise_id}, correct={self.is_correct})>"


class DiagnosticTest(Base):
    """
    Grammar diagnostic test results.
    Assesses user's overall grammar level and identifies weak areas.
    """

    __tablename__ = "diagnostic_tests"

    id = Column(Integer, primary_key=True, index=True)

    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Test date
    test_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # Overall results
    overall_level = Column(String(10), nullable=True)  # Determined level: B1, B2, C1
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    test_duration_minutes = Column(Integer, nullable=True)

    # Detailed results (stored as JSON)
    topic_scores = Column(JSON, nullable=True)  # {"cases": 0.75, "verbs": 0.60, ...}
    weak_areas = Column(JSON, nullable=True)  # Array of topics needing work
    strong_areas = Column(JSON, nullable=True)  # Array of mastered topics
    recommended_path = Column(JSON, nullable=True)  # Suggested learning sequence

    def __repr__(self) -> str:
        return f"<DiagnosticTest(id={self.id}, user_id={self.user_id}, level='{self.overall_level}')>"
