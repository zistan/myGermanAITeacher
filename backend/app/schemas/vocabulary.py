"""
Pydantic schemas for vocabulary learning endpoints.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== VOCABULARY WORD SCHEMAS ==========

class VocabularyWordBase(BaseModel):
    """Base schema for vocabulary words."""
    word: str = Field(..., description="German word with article if noun")
    translation_it: str = Field(..., description="Italian translation")
    part_of_speech: str = Field(..., description="Part of speech")
    gender: Optional[str] = Field(None, pattern="^(masculine|feminine|neuter)$")
    plural_form: Optional[str] = Field(None, description="Plural form for nouns")
    difficulty: str = Field(..., pattern="^(A1|A2|B1|B2|C1|C2)$")
    category: str = Field(..., description="Category (business, daily, verbs, etc.)")
    example_de: str = Field(..., description="Example sentence in German")
    example_it: str = Field(..., description="Example sentence in Italian")
    pronunciation: Optional[str] = Field(None, description="Pronunciation guide")


class VocabularyWordCreate(VocabularyWordBase):
    """Schema for creating a vocabulary word."""
    definition_de: Optional[str] = Field(None, description="Definition in German")
    usage_notes: Optional[str] = Field(None, description="Usage notes")
    synonyms: List[str] = Field(default_factory=list)
    antonyms: List[str] = Field(default_factory=list)
    is_idiom: bool = Field(False)
    is_compound: bool = Field(False)
    is_separable_verb: bool = Field(False)


class VocabularyWordResponse(VocabularyWordBase):
    """Schema for vocabulary word response."""
    id: int
    definition_de: Optional[str]
    usage_notes: Optional[str]
    synonyms: List[str] = Field(default_factory=list)
    antonyms: List[str] = Field(default_factory=list)
    is_idiom: bool
    is_compound: bool
    is_separable_verb: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VocabularyWordWithProgress(VocabularyWordResponse):
    """Vocabulary word with user's learning progress."""
    mastery_level: Optional[int] = Field(None, ge=0, le=5, description="0=new, 5=mastered")
    times_reviewed: int = Field(0, description="Number of times reviewed")
    last_reviewed: Optional[datetime] = None
    next_review_due: Optional[datetime] = None
    accuracy_rate: Optional[float] = Field(None, ge=0, le=100)


# ========== FLASHCARD SCHEMAS ==========

class FlashcardResponse(BaseModel):
    """Single flashcard for vocabulary practice."""
    card_id: str
    word_id: int
    word: str
    card_type: str = Field(..., description="definition, translation, usage, etc.")
    front: str = Field(..., description="Front of the flashcard")
    back: str = Field(..., description="Back of the flashcard")
    hint: Optional[str] = Field(None, description="Optional hint")
    difficulty: str


class StartFlashcardSessionRequest(BaseModel):
    """Request to start a flashcard practice session."""
    word_ids: Optional[List[int]] = Field(None, description="Specific words to practice")
    category: Optional[str] = Field(None, description="Filter by category")
    difficulty: Optional[str] = Field(None, pattern="^(A1|A2|B1|B2|C1|C2)$")
    card_count: int = Field(10, ge=1, le=50)
    use_spaced_repetition: bool = Field(True)
    card_types: Optional[List[str]] = Field(None, description="Types of cards to include")


class FlashcardSessionResponse(BaseModel):
    """Response when starting a flashcard session."""
    session_id: int
    total_cards: int
    current_card_number: int
    current_card: FlashcardResponse


class SubmitFlashcardAnswerRequest(BaseModel):
    """Request to submit a flashcard answer."""
    card_id: str
    user_answer: str
    confidence_level: int = Field(..., ge=1, le=5, description="1=hard, 5=easy")
    time_spent_seconds: Optional[int] = Field(None, ge=0)


class SubmitFlashcardAnswerResponse(BaseModel):
    """Response after submitting a flashcard answer."""
    is_correct: bool
    correct_answer: str
    feedback: str
    next_review_interval_days: int
    next_card: Optional[FlashcardResponse] = None


# ========== PERSONAL VOCABULARY LIST SCHEMAS ==========

class PersonalVocabularyListCreate(BaseModel):
    """Create a personal vocabulary list."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    is_public: bool = Field(False, description="Share with other users")


class PersonalVocabularyListResponse(BaseModel):
    """Personal vocabulary list response."""
    id: int
    name: str
    description: Optional[str]
    is_public: bool
    word_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AddWordToListRequest(BaseModel):
    """Add a word to a personal list."""
    word_id: int
    notes: Optional[str] = Field(None, max_length=500, description="Personal notes about this word")


class PersonalVocabularyListWithWords(PersonalVocabularyListResponse):
    """Vocabulary list with all words."""
    words: List[VocabularyWordWithProgress]


# ========== VOCABULARY QUIZ SCHEMAS ==========

class VocabularyQuizRequest(BaseModel):
    """Request to generate a vocabulary quiz."""
    word_ids: Optional[List[int]] = Field(None, description="Specific words to quiz on")
    category: Optional[str] = Field(None)
    difficulty: Optional[str] = Field(None, pattern="^(A1|A2|B1|B2|C1|C2)$")
    quiz_type: str = Field("multiple_choice", pattern="^(multiple_choice|fill_blank|matching)$")
    question_count: int = Field(10, ge=1, le=30)


class VocabularyQuizQuestion(BaseModel):
    """Single quiz question."""
    question_id: str
    question: str
    question_type: str
    options: Optional[List[str]] = Field(None, description="For multiple choice")
    correct_answer: str
    word_tested: str
    explanation: str


class VocabularyQuizResponse(BaseModel):
    """Vocabulary quiz response."""
    quiz_id: int
    questions: List[VocabularyQuizQuestion]
    total_questions: int
    estimated_duration_minutes: int


class SubmitQuizAnswerRequest(BaseModel):
    """Submit answer to a quiz question."""
    question_id: str
    user_answer: str


class SubmitQuizAnswerResponse(BaseModel):
    """Response after submitting a quiz answer."""
    is_correct: bool
    correct_answer: str
    explanation: str
    points_earned: int


# ========== VOCABULARY PROGRESS SCHEMAS ==========

class VocabularyProgressSummary(BaseModel):
    """Overall vocabulary learning progress."""
    total_words_learned: int
    words_by_level: Dict[str, int] = Field(..., description="Count per CEFR level")
    words_by_category: Dict[str, int] = Field(..., description="Count per category")
    mastery_breakdown: Dict[str, int] = Field(..., description="Count per mastery level")
    total_review_time_minutes: int
    current_streak_days: int
    words_due_today: int
    words_due_this_week: int


class WordMasteryDetail(BaseModel):
    """Detailed mastery info for a specific word."""
    word: VocabularyWordResponse
    mastery_level: int = Field(..., ge=0, le=5)
    times_reviewed: int
    times_correct: int
    accuracy_rate: float
    last_reviewed: Optional[datetime]
    next_review_due: Optional[datetime]
    review_history: List[Dict] = Field(..., description="Recent review attempts")


class VocabularyReviewQueueResponse(BaseModel):
    """Words due for review based on spaced repetition."""
    overdue_count: int
    due_today_count: int
    upcoming_count: int
    overdue_words: List[VocabularyWordWithProgress]
    due_today_words: List[VocabularyWordWithProgress]
    upcoming_words: List[VocabularyWordWithProgress]


# ========== WORD ANALYSIS SCHEMAS ==========

class AnalyzeWordRequest(BaseModel):
    """Request to analyze a German word."""
    word: str = Field(..., min_length=1)
    include_examples: bool = Field(True)
    include_synonyms: bool = Field(True)


class WordAnalysisResponse(BaseModel):
    """Detailed word analysis response."""
    word: str
    translation_it: str
    part_of_speech: str
    gender: Optional[str]
    plural_form: Optional[str]
    difficulty_level: str
    pronunciation: str
    definition_de: str
    usage_notes: Optional[str]
    synonyms: List[str]
    antonyms: List[str]
    examples: List[Dict[str, str]]
    collocations: List[str]
    is_compound: bool
    compound_parts: Optional[List[str]]
    is_separable: bool
    separable_prefix: Optional[str]
    language_register: str = Field(..., description="formal, informal, or neutral", alias="register")
    frequency: str = Field(..., description="very_common, common, uncommon, rare")

    model_config = ConfigDict(populate_by_name=True)


class DetectVocabularyRequest(BaseModel):
    """Request to detect vocabulary from text."""
    text: str = Field(..., min_length=1)
    min_difficulty: str = Field("B1", pattern="^(A1|A2|B1|B2|C1|C2)$")
    max_words: int = Field(10, ge=1, le=20)


class DetectedVocabularyItem(BaseModel):
    """Single detected vocabulary item from text."""
    word: str
    lemma: str
    translation_it: str
    part_of_speech: str
    difficulty: str
    context_in_text: str
    why_important: str


class DetectVocabularyResponse(BaseModel):
    """Response with detected vocabulary."""
    detected_words: List[DetectedVocabularyItem]
    total_detected: int


# ========== VOCABULARY STATISTICS SCHEMAS ==========

class VocabularyStatistics(BaseModel):
    """Comprehensive vocabulary statistics."""
    total_words_in_database: int
    user_words_learned: int
    learning_rate_words_per_week: float
    average_mastery_level: float
    strongest_categories: List[Dict[str, Any]]
    weakest_categories: List[Dict[str, Any]]
    retention_rate: float = Field(..., ge=0, le=100, description="Percentage retained")
    review_accuracy: float = Field(..., ge=0, le=100)
    estimated_vocabulary_size: int = Field(..., description="Estimated active vocabulary")
    progress_by_level: Dict[str, Dict[str, int]]


# ========== WORD RECOMMENDATION SCHEMAS ==========

class WordRecommendationRequest(BaseModel):
    """Request word recommendations."""
    based_on_word: Optional[str] = Field(None, description="Base word for similarity")
    category: Optional[str] = Field(None)
    difficulty: Optional[str] = Field(None, pattern="^(A1|A2|B1|B2|C1|C2)$")
    count: int = Field(10, ge=1, le=50)
    recommendation_type: str = Field("next_to_learn", pattern="^(next_to_learn|similar|related|review_priority)$")


class WordRecommendationResponse(BaseModel):
    """Recommended words for learning."""
    recommended_words: List[VocabularyWordWithProgress]
    reason: str = Field(..., description="Why these words are recommended")
