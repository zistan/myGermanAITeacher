"""
Pydantic schemas for grammar learning endpoints.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import datetime


# ========== GRAMMAR TOPIC SCHEMAS ==========

class GrammarTopicBase(BaseModel):
    """Base schema for grammar topics."""
    name_de: str = Field(..., description="German name of the topic")
    name_en: str = Field(..., description="English name of the topic")
    category: str = Field(..., description="Category (cases, verbs, etc.)")
    subcategory: Optional[str] = Field(None, description="Subcategory for finer grouping")
    difficulty_level: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2)$", description="CEFR level")
    order_index: int = Field(..., description="Order for sequential learning")
    description_de: str = Field(..., description="Brief description in German")
    explanation_de: str = Field(..., description="Detailed explanation in German")


class GrammarTopicCreate(GrammarTopicBase):
    """Schema for creating a grammar topic."""
    pass


class GrammarTopicResponse(GrammarTopicBase):
    """Schema for grammar topic response."""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GrammarTopicWithStats(GrammarTopicResponse):
    """Grammar topic with user progress stats."""
    user_accuracy: Optional[float] = Field(None, description="User's accuracy % on this topic")
    total_attempts: int = Field(0, description="Total exercises attempted")
    last_practiced: Optional[datetime] = Field(None, description="Last practice date")


# ========== GRAMMAR EXERCISE SCHEMAS ==========

class GrammarExerciseBase(BaseModel):
    """Base schema for grammar exercises."""
    exercise_type: str = Field(
        ...,
        pattern="^(fill_blank|multiple_choice|translation|error_correction|sentence_building)$",
        description="Type of exercise"
    )
    difficulty_level: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2)$")
    question_text: str = Field(..., description="The exercise question")
    correct_answer: str = Field(..., description="The correct answer")
    alternative_answers: List[str] = Field(default_factory=list, description="Alternative correct answers or distractors")
    explanation_de: str = Field(..., description="Explanation in German")
    hints: List[str] = Field(default_factory=list, description="Helpful hints")
    context_category: str = Field("general", pattern="^(business|daily|general)$")


class GrammarExerciseCreate(GrammarExerciseBase):
    """Schema for creating a grammar exercise."""
    topic_id: int = Field(..., description="Associated grammar topic ID")


class GrammarExerciseResponse(GrammarExerciseBase):
    """Schema for grammar exercise response."""
    id: int
    topic_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class GrammarExerciseWithTopic(GrammarExerciseResponse):
    """Grammar exercise with topic information."""
    topic: GrammarTopicResponse


# ========== GRAMMAR PRACTICE SCHEMAS ==========

class StartGrammarPracticeRequest(BaseModel):
    """Request to start a grammar practice session."""
    topic_ids: Optional[List[int]] = Field(None, description="Specific topics to practice (empty = all)")
    difficulty_level: Optional[str] = Field(None, pattern="^(A1|A2|B1|B2|C1|C2)$", description="Filter by level")
    exercise_count: int = Field(10, ge=1, le=50, description="Number of exercises")
    exercise_types: Optional[List[str]] = Field(None, description="Specific exercise types")
    context_category: Optional[str] = Field(None, pattern="^(business|daily|general)$")
    use_spaced_repetition: bool = Field(True, description="Use spaced repetition algorithm")


class GrammarPracticeSessionResponse(BaseModel):
    """Response when starting a grammar practice session."""
    session_id: int
    total_exercises: int
    current_exercise_number: int
    estimated_duration_minutes: int
    topics_included: List[str]

    model_config = ConfigDict(from_attributes=True)


class SubmitExerciseAnswerRequest(BaseModel):
    """Request to submit an answer to an exercise."""
    exercise_id: int
    user_answer: str = Field(..., min_length=1, description="User's answer")
    time_spent_seconds: Optional[int] = Field(None, ge=0, description="Time spent on exercise")


class ExerciseFeedback(BaseModel):
    """Feedback on a submitted exercise answer."""
    is_correct: bool
    is_partially_correct: bool = False
    correct_answer: str
    user_answer: str
    feedback_de: str = Field(..., description="Detailed feedback in German")
    specific_errors: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    points_earned: int = Field(..., ge=0, le=3)


class SubmitExerciseAnswerResponse(BaseModel):
    """Response after submitting an exercise answer."""
    feedback: ExerciseFeedback
    session_progress: dict = Field(..., description="Current session progress")
    next_exercise: Optional[GrammarExerciseResponse] = None


# ========== DIAGNOSTIC TEST SCHEMAS ==========

class StartDiagnosticTestRequest(BaseModel):
    """Request to start a diagnostic test."""
    target_level: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2)$", description="Level to assess")
    num_questions: int = Field(20, ge=10, le=50, description="Number of questions")
    topics: Optional[List[str]] = Field(None, description="Specific topics to test")


class DiagnosticTestResponse(BaseModel):
    """Response when starting a diagnostic test."""
    test_id: int
    total_questions: int
    estimated_duration_minutes: int
    instructions: str

    model_config = ConfigDict(from_attributes=True)


class DiagnosticTestResults(BaseModel):
    """Results of a completed diagnostic test."""
    test_id: int
    total_questions: int
    correct_answers: int
    score_percentage: float
    assessed_level: str = Field(..., description="Determined CEFR level based on results")
    strengths: List[str] = Field(..., description="Grammar topics user is strong in")
    weaknesses: List[str] = Field(..., description="Grammar topics needing improvement")
    recommended_topics: List[int] = Field(..., description="Topic IDs to focus on")
    detailed_results: List[dict] = Field(..., description="Question-by-question breakdown")


# ========== PROGRESS TRACKING SCHEMAS ==========

class GrammarProgressSummary(BaseModel):
    """Summary of user's grammar progress."""
    total_exercises_completed: int
    total_practice_time_minutes: int
    overall_accuracy: float = Field(..., ge=0, le=100, description="Overall accuracy percentage")
    current_streak_days: int
    topics_mastered: int
    topics_in_progress: int
    topics_not_started: int
    level_progress: dict = Field(..., description="Progress by CEFR level")
    recent_activity: List[dict]


class TopicProgressDetail(BaseModel):
    """Detailed progress for a specific topic."""
    topic: GrammarTopicResponse
    total_attempts: int
    correct_attempts: int
    accuracy: float = Field(..., ge=0, le=100)
    mastery_level: str = Field(..., description="beginner, intermediate, advanced, mastered")
    last_practiced: Optional[datetime]
    next_review_due: Optional[datetime]
    exercises_available: int
    exercises_completed: int


class WeakAreasResponse(BaseModel):
    """User's weak areas with recommendations."""
    weak_topics: List[TopicProgressDetail]
    recommended_practice_plan: List[dict] = Field(..., description="Suggested practice schedule")
    estimated_time_to_improve: int = Field(..., description="Estimated days to improvement")


# ========== AI GENERATION SCHEMAS ==========

class GenerateExercisesRequest(BaseModel):
    """Request to generate new exercises using AI."""
    topic_id: int
    count: int = Field(5, ge=1, le=20, description="Number of exercises to generate")
    exercise_type: str = Field(
        ...,
        pattern="^(fill_blank|multiple_choice|translation|error_correction|sentence_building)$"
    )
    context_category: str = Field("general", pattern="^(business|daily|general)$")


class GenerateExercisesResponse(BaseModel):
    """Response after generating exercises."""
    generated_count: int
    exercises: List[GrammarExerciseResponse]


# ========== STATISTICS SCHEMAS ==========

class GrammarStatistics(BaseModel):
    """Overall grammar learning statistics."""
    total_sessions: int
    total_exercises: int
    total_time_minutes: int
    average_session_duration: float
    accuracy_by_level: dict = Field(..., description="Accuracy for each CEFR level")
    accuracy_by_type: dict = Field(..., description="Accuracy for each exercise type")
    progress_over_time: List[dict] = Field(..., description="Daily/weekly progress data")
    most_practiced_topics: List[dict]
    least_practiced_topics: List[dict]


# ========== SPACED REPETITION SCHEMAS ==========

class ReviewQueueItem(BaseModel):
    """Item in the spaced repetition review queue."""
    topic_id: int
    topic_name: str
    due_date: datetime
    priority: int = Field(..., ge=1, le=5, description="1=low, 5=urgent")
    days_overdue: int


class ReviewQueueResponse(BaseModel):
    """User's review queue based on spaced repetition."""
    overdue_count: int
    due_today_count: int
    upcoming_count: int
    overdue_items: List[ReviewQueueItem]
    due_today_items: List[ReviewQueueItem]
    upcoming_items: List[ReviewQueueItem]
