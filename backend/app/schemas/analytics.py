"""
Pydantic schemas for analytics and progress tracking endpoints.
"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


# ========== OVERALL PROGRESS SCHEMAS ==========

class ActivityStats(BaseModel):
    """Overall activity statistics."""
    total_study_days: int
    current_streak_days: int
    longest_streak_days: int
    average_sessions_per_week: float


class ConversationStats(BaseModel):
    """Conversation module statistics."""
    total_sessions: int
    total_messages: int
    average_session_duration_minutes: float
    unique_contexts_practiced: int
    sessions_last_7_days: int
    estimated_conversation_hours: float


class GrammarTopicSummary(BaseModel):
    """Brief summary of a grammar topic."""
    topic_id: int
    topic_name: str
    mastery: float


class GrammarStats(BaseModel):
    """Grammar module statistics."""
    topics_practiced: int
    topics_mastered: int
    total_exercises_attempted: int
    overall_accuracy_percentage: float
    average_mastery_level: float
    weak_areas: List[GrammarTopicSummary]
    strong_areas: List[GrammarTopicSummary]


class VocabularyStats(BaseModel):
    """Vocabulary module statistics."""
    total_words_learned: int
    words_mastered: int
    total_reviews: int
    overall_accuracy_percentage: float
    words_by_cefr_level: Dict[str, int]
    personal_vocabulary_lists: int
    current_streak_days: int


class WeeklyGoalProgress(BaseModel):
    """Weekly goal progress."""
    sessions_this_week: int
    goal_sessions: int
    goal_percentage: int
    goal_met: bool


class OverallProgressResponse(BaseModel):
    """Comprehensive progress across all modules."""
    user_id: int
    overall_score: int = Field(..., ge=0, le=100, description="Overall progress score 0-100")
    last_updated: datetime
    conversation: ConversationStats
    grammar: GrammarStats
    vocabulary: VocabularyStats
    activity: ActivityStats
    weekly_goal_progress: WeeklyGoalProgress


# ========== ERROR PATTERN ANALYSIS SCHEMAS ==========

class TopErrorTopic(BaseModel):
    """Top error topic summary."""
    topic: str
    count: int


class RecurringMistake(BaseModel):
    """Recurring mistake details."""
    topic_id: int
    topic_name: str
    error_count: int
    severity: str = Field(..., pattern="^(high|medium|low)$")


class ImprovementTrend(BaseModel):
    """Topic improvement trend."""
    topic_id: int
    topic_name: str
    trend: str = Field(..., pattern="^(improving|declining)$")
    improvement_percentage: float


class ErrorPatternAnalysisResponse(BaseModel):
    """Error pattern analysis."""
    analysis_period_days: int
    total_errors: int
    top_error_topics: List[TopErrorTopic]
    recurring_mistakes: List[RecurringMistake]
    improvement_trends: List[ImprovementTrend]
    recommendations: List[str]


# ========== PROGRESS SNAPSHOT SCHEMAS ==========

class MilestoneAchieved(BaseModel):
    """Milestone achievement."""
    type: str  # conversation, grammar, vocabulary, activity
    milestone: str  # e.g., "10_sessions", "100_words"


class ProgressSnapshotResponse(BaseModel):
    """Point-in-time progress snapshot."""
    snapshot_date: datetime
    user_id: int
    overall_progress: OverallProgressResponse
    error_analysis: ErrorPatternAnalysisResponse
    milestones_achieved: List[MilestoneAchieved]
    next_goals: List[str]


class CreateSnapshotRequest(BaseModel):
    """Request to create a progress snapshot."""
    snapshot_type: str = Field("weekly", pattern="^(daily|weekly|monthly)$")


# ========== ACHIEVEMENT SCHEMAS ==========

class AchievementResponse(BaseModel):
    """Achievement definition."""
    id: int
    name: str
    description: str
    category: str
    badge_icon: Optional[str]
    badge_color: Optional[str]
    criteria_type: str
    criteria_value: int
    tier: str = Field(..., pattern="^(bronze|silver|gold|platinum)$")
    points: int

    model_config = ConfigDict(from_attributes=True)


class UserAchievementResponse(BaseModel):
    """User's earned achievement."""
    id: int
    achievement: AchievementResponse
    earned_at: datetime
    progress_value: int
    is_completed: bool
    is_showcased: bool

    model_config = ConfigDict(from_attributes=True)


class AchievementProgressResponse(BaseModel):
    """Achievement with current progress."""
    achievement: AchievementResponse
    current_progress: int
    target_value: int
    progress_percentage: int
    is_completed: bool
    earned_at: Optional[datetime]


class ShowcaseAchievementRequest(BaseModel):
    """Request to showcase an achievement."""
    achievement_id: int
    is_showcased: bool


# ========== USER STATS SCHEMAS ==========

class UserStatsResponse(BaseModel):
    """Aggregate user statistics."""
    user_id: int

    # Overall stats
    total_study_time_minutes: int
    total_sessions: int
    current_streak_days: int
    longest_streak_days: int
    last_activity_date: Optional[datetime]

    # Conversation stats
    conversation_sessions: int
    total_messages_sent: int

    # Grammar stats
    grammar_sessions: int
    grammar_exercises_completed: int
    grammar_exercises_correct: int
    grammar_topics_mastered: int
    average_grammar_accuracy: int

    # Vocabulary stats
    vocabulary_words_learned: int
    vocabulary_words_mastered: int
    vocabulary_reviews_completed: int
    vocabulary_reviews_correct: int
    average_vocabulary_accuracy: int

    # Achievement stats
    total_achievement_points: int
    achievements_earned: int

    # Rankings
    overall_rank: Optional[int]
    grammar_rank: Optional[int]
    vocabulary_rank: Optional[int]

    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ========== COMPARATIVE ANALYTICS SCHEMAS ==========

class PeriodStats(BaseModel):
    """Statistics for a specific time period."""
    total_sessions: int
    conversation_sessions: int
    grammar_sessions: int
    exercises_completed: int
    exercise_accuracy: float
    vocabulary_reviews: int


class StatChange(BaseModel):
    """Change in a statistic."""
    value: float
    change_percent: float
    trend: str = Field(..., pattern="^(up|down|stable)$")


class ProgressComparisonResponse(BaseModel):
    """Comparison between two time periods."""
    period_days: int
    current_period: PeriodStats
    previous_period: PeriodStats
    changes: Dict[str, Any]


# ========== LEADERBOARD SCHEMAS ==========

class LeaderboardEntry(BaseModel):
    """Single leaderboard entry."""
    rank: int
    user_id: int
    username: str
    score: int
    metric_value: int  # Specific metric for this leaderboard


class LeaderboardResponse(BaseModel):
    """Leaderboard response."""
    leaderboard_type: str  # overall, grammar, vocabulary, streak
    period: str  # all_time, monthly, weekly
    entries: List[LeaderboardEntry]
    user_rank: Optional[int]
    user_entry: Optional[LeaderboardEntry]
    total_users: int


# ========== HEATMAP SCHEMAS ==========

class HeatmapCell(BaseModel):
    """Single cell in a heatmap."""
    date: str  # YYYY-MM-DD
    value: int
    level: int  # 0-4 for intensity


class ActivityHeatmapResponse(BaseModel):
    """Activity heatmap data."""
    start_date: str
    end_date: str
    cells: List[HeatmapCell]
    total_days: int
    active_days: int


class GrammarTopicHeatmap(BaseModel):
    """Grammar topic mastery heatmap."""
    topic_id: int
    topic_name: str
    category: str
    mastery_level: float
    last_practiced: Optional[datetime]
    color_intensity: int  # 0-4


class GrammarHeatmapResponse(BaseModel):
    """Grammar mastery heatmap."""
    topics: List[GrammarTopicHeatmap]
    categories: List[str]
    overall_mastery: float


# ========== DETAILED ANALYTICS SCHEMAS ==========

class SessionDetail(BaseModel):
    """Detailed session information."""
    session_id: int
    session_type: str  # conversation, grammar, vocabulary
    started_at: datetime
    ended_at: Optional[datetime]
    duration_minutes: Optional[int]
    performance_score: Optional[float]


class DailyActivity(BaseModel):
    """Daily activity summary."""
    date: str  # YYYY-MM-DD
    sessions: List[SessionDetail]
    total_sessions: int
    total_minutes: int
    exercises_completed: int
    accuracy_rate: Optional[float]


class WeeklyReport(BaseModel):
    """Weekly progress report."""
    week_start: str  # YYYY-MM-DD
    week_end: str  # YYYY-MM-DD
    total_sessions: int
    total_study_minutes: int
    days_active: int
    average_accuracy: float
    top_achievements: List[AchievementResponse]
    improvement_areas: List[str]
    daily_breakdown: List[DailyActivity]


class MonthlyReport(BaseModel):
    """Monthly progress report."""
    month: str  # YYYY-MM
    total_sessions: int
    total_study_hours: float
    days_active: int
    conversation_sessions: int
    grammar_sessions: int
    vocabulary_reviews: int
    new_words_learned: int
    grammar_topics_mastered: int
    achievements_earned: int
    overall_progress_change: float


# ========== RECOMMENDATION SCHEMAS ==========

class StudyRecommendation(BaseModel):
    """Study recommendation."""
    type: str  # grammar_topic, vocabulary_category, conversation_context
    item_id: int
    item_name: str
    reason: str
    priority: str = Field(..., pattern="^(high|medium|low)$")
    estimated_duration_minutes: int


class PersonalizedRecommendationsResponse(BaseModel):
    """Personalized study recommendations."""
    recommendations: List[StudyRecommendation]
    next_review_due: List[Dict[str, Any]]  # Items due for review
    suggested_session_plan: List[Dict[str, Any]]  # Suggested study plan
    motivation_message: str


# ========== EXPORT SCHEMAS ==========

class ExportProgressRequest(BaseModel):
    """Request to export progress data."""
    format: str = Field("json", pattern="^(json|csv)$")
    include_sessions: bool = True
    include_exercises: bool = True
    include_achievements: bool = True
    start_date: Optional[datetime]
    end_date: Optional[datetime]


class ProgressExportResponse(BaseModel):
    """Progress data export."""
    export_date: datetime
    user_id: int
    data_format: str
    data: Dict[str, Any]  # Exported data
