/**
 * TypeScript type definitions for analytics and progress tracking.
 * Generated from backend/app/schemas/analytics.py
 */

// ========== OVERALL PROGRESS TYPES ==========

export interface ActivityStats {
  total_study_days: number;
  current_streak_days: number;
  longest_streak_days: number;
  average_sessions_per_week: number;
}

export interface ConversationStats {
  total_sessions: number;
  total_messages: number;
  average_session_duration_minutes: number;
  unique_contexts_practiced: number;
  sessions_last_7_days: number;
  estimated_conversation_hours: number;
}

export interface GrammarTopicSummary {
  topic_id: number;
  topic_name: string;
  mastery: number;
}

export interface GrammarStats {
  topics_practiced: number;
  topics_mastered: number;
  total_exercises_attempted: number;
  overall_accuracy_percentage: number;
  average_mastery_level: number;
  weak_areas: GrammarTopicSummary[];
  strong_areas: GrammarTopicSummary[];
}

export interface VocabularyStats {
  total_words_learned: number;
  words_mastered: number;
  total_reviews: number;
  overall_accuracy_percentage: number;
  words_by_cefr_level: Record<string, number>;
  personal_vocabulary_lists: number;
  current_streak_days: number;
}

export interface WeeklyGoalProgress {
  sessions_this_week: number;
  goal_sessions: number;
  goal_percentage: number;
  goal_met: boolean;
}

export interface OverallProgressResponse {
  user_id: number;
  overall_score: number; // 0-100
  last_updated: string; // ISO 8601
  conversation: ConversationStats;
  grammar: GrammarStats;
  vocabulary: VocabularyStats;
  activity: ActivityStats;
  weekly_goal_progress: WeeklyGoalProgress;
}

// ========== ERROR PATTERN ANALYSIS TYPES ==========

export interface TopErrorTopic {
  topic: string;
  count: number;
}

export interface RecurringMistake {
  topic_id: number;
  topic_name: string;
  error_count: number;
  severity: 'high' | 'medium' | 'low';
}

export interface ImprovementTrend {
  topic_id: number;
  topic_name: string;
  trend: 'improving' | 'declining';
  improvement_percentage: number;
}

export interface ErrorPatternAnalysisResponse {
  analysis_period_days: number;
  total_errors: number;
  top_error_topics: TopErrorTopic[];
  recurring_mistakes: RecurringMistake[];
  improvement_trends: ImprovementTrend[];
  recommendations: string[];
}

// ========== PROGRESS SNAPSHOT TYPES ==========

export interface MilestoneAchieved {
  type: string; // conversation, grammar, vocabulary, activity
  milestone: string; // e.g., "10_sessions", "100_words"
}

export interface ProgressSnapshotResponse {
  snapshot_date: string; // ISO 8601
  user_id: number;
  overall_progress: OverallProgressResponse;
  error_analysis: ErrorPatternAnalysisResponse;
  milestones_achieved: MilestoneAchieved[];
  next_goals: string[];
}

export interface CreateSnapshotRequest {
  snapshot_type: 'daily' | 'weekly' | 'monthly';
}

// ========== ACHIEVEMENT TYPES ==========

export interface AchievementResponse {
  id: number;
  name: string;
  description: string;
  category: string;
  badge_icon: string | null;
  badge_color: string | null;
  criteria_type: string;
  criteria_value: number;
  tier: 'bronze' | 'silver' | 'gold' | 'platinum';
  points: number;
}

export interface UserAchievementResponse {
  id: number;
  achievement: AchievementResponse;
  earned_at: string; // ISO 8601
  progress_value: number;
  is_completed: boolean;
  is_showcased: boolean;
}

export interface AchievementProgressResponse {
  achievement: AchievementResponse;
  current_progress: number;
  target_value: number;
  progress_percentage: number;
  is_completed: boolean;
  earned_at: string | null; // ISO 8601
}

export interface ShowcaseAchievementRequest {
  achievement_id: number;
  is_showcased: boolean;
}

// ========== USER STATS TYPES ==========

export interface UserStatsResponse {
  user_id: number;

  // Overall stats
  total_study_time_minutes: number;
  total_sessions: number;
  current_streak_days: number;
  longest_streak_days: number;
  last_activity_date: string | null; // ISO 8601

  // Conversation stats
  conversation_sessions: number;
  total_messages_sent: number;

  // Grammar stats
  grammar_sessions: number;
  grammar_exercises_completed: number;
  grammar_exercises_correct: number;
  grammar_topics_mastered: number;
  average_grammar_accuracy: number;

  // Vocabulary stats
  vocabulary_words_learned: number;
  vocabulary_words_mastered: number;
  vocabulary_reviews_completed: number;
  vocabulary_reviews_correct: number;
  average_vocabulary_accuracy: number;

  // Achievement stats
  total_achievement_points: number;
  achievements_earned: number;

  // Rankings
  overall_rank: number | null;
  grammar_rank: number | null;
  vocabulary_rank: number | null;

  updated_at: string; // ISO 8601
}

// ========== COMPARATIVE ANALYTICS TYPES ==========

export interface PeriodStats {
  total_sessions: number;
  conversation_sessions: number;
  grammar_sessions: number;
  exercises_completed: number;
  exercise_accuracy: number;
  vocabulary_reviews: number;
}

export interface StatChange {
  value: number;
  change_percent: number;
  trend: 'up' | 'down' | 'stable';
}

export interface ProgressComparisonResponse {
  period_days: number;
  current_period: PeriodStats;
  previous_period: PeriodStats;
  changes: Record<string, any>;
}

// ========== LEADERBOARD TYPES ==========

export interface LeaderboardEntry {
  rank: number;
  user_id: number;
  username: string;
  score: number;
  metric_value: number; // Specific metric for this leaderboard
}

export interface LeaderboardResponse {
  leaderboard_type: string; // overall, grammar, vocabulary, streak
  period: string; // all_time, monthly, weekly
  entries: LeaderboardEntry[];
  user_rank: number | null;
  user_entry: LeaderboardEntry | null;
  total_users: number;
}

// ========== HEATMAP TYPES ==========

export interface HeatmapCell {
  date: string; // YYYY-MM-DD
  value: number;
  level: number; // 0-4 for intensity
}

export interface ActivityHeatmapResponse {
  start_date: string;
  end_date: string;
  cells: HeatmapCell[];
  total_days: number;
  active_days: number;
}

export interface GrammarTopicHeatmap {
  topic_id: number;
  topic_name: string;
  category: string;
  mastery_level: number;
  last_practiced: string | null; // ISO 8601
  color_intensity: number; // 0-4
}

export interface GrammarHeatmapResponse {
  topics: GrammarTopicHeatmap[];
  categories: string[];
  overall_mastery: number;
}

// ========== DETAILED ANALYTICS TYPES ==========

export interface SessionDetail {
  session_id: number;
  session_type: string; // conversation, grammar, vocabulary
  started_at: string; // ISO 8601
  ended_at: string | null; // ISO 8601
  duration_minutes: number | null;
  performance_score: number | null;
}

export interface DailyActivity {
  date: string; // YYYY-MM-DD
  sessions: SessionDetail[];
  total_sessions: number;
  total_minutes: number;
  exercises_completed: number;
  accuracy_rate: number | null;
}

export interface WeeklyReport {
  week_start: string; // YYYY-MM-DD
  week_end: string; // YYYY-MM-DD
  total_sessions: number;
  total_study_minutes: number;
  days_active: number;
  average_accuracy: number;
  top_achievements: AchievementResponse[];
  improvement_areas: string[];
  daily_breakdown: DailyActivity[];
}

export interface MonthlyReport {
  month: string; // YYYY-MM
  total_sessions: number;
  total_study_hours: number;
  days_active: number;
  conversation_sessions: number;
  grammar_sessions: number;
  vocabulary_reviews: number;
  new_words_learned: number;
  grammar_topics_mastered: number;
  achievements_earned: number;
  overall_progress_change: number;
}

// ========== RECOMMENDATION TYPES ==========

export interface StudyRecommendation {
  type: string; // grammar_topic, vocabulary_category, conversation_context
  item_id: number;
  item_name: string;
  reason: string;
  priority: 'high' | 'medium' | 'low';
  estimated_duration_minutes: number;
}

export interface PersonalizedRecommendationsResponse {
  recommendations: StudyRecommendation[];
  next_review_due: Record<string, any>[];
  suggested_session_plan: Record<string, any>[];
  motivation_message: string;
}

// ========== EXPORT TYPES ==========

export interface ExportProgressRequest {
  format: 'json' | 'csv';
  include_sessions: boolean;
  include_exercises: boolean;
  include_achievements: boolean;
  start_date: string | null; // ISO 8601
  end_date: string | null; // ISO 8601
}

export interface ProgressExportResponse {
  export_date: string; // ISO 8601
  user_id: number;
  data_format: string;
  data: Record<string, any>;
}
