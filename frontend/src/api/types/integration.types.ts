/**
 * Integration API Types - Match backend IntegrationService responses EXACTLY
 * Source: backend/app/services/integration_service.py
 */

// Dashboard Data Types
export interface DashboardData {
  user_id: number;
  last_updated: string; // datetime
  overall_progress: OverallProgress;
  learning_path: LearningPath;
  due_items: DueItems;
  recent_activity: Activity[];
  close_achievements: CloseAchievement[];
  quick_actions: QuickAction[];
}

// Overall Progress (from AnalyticsService.get_overall_progress)
export interface OverallProgress {
  user_id: number;
  overall_score: number; // 0-100
  last_updated: string;
  conversation: ConversationStats;
  grammar: GrammarStats;
  vocabulary: VocabularyStats;
  activity: ActivityStats;
  weekly_goal_progress: WeeklyGoalProgress;
}

export interface WeeklyGoalProgress {
  sessions_this_week: number;
  goal_sessions: number;
  goal_percentage: number; // 0-100
  goal_met: boolean;
}

export interface ConversationStats {
  total_sessions: number;
  total_messages: number;
  average_session_duration_minutes: number;
  unique_contexts_practiced: number;
  sessions_last_7_days: number;
  estimated_conversation_hours: number;
}

export interface GrammarStats {
  total_sessions: number;
  topics_practiced: number;
  topics_mastered: number;
  total_exercises: number;
  overall_accuracy: number; // percentage
  average_mastery: number; // 0-5
  weak_topics: WeakTopic[];
  strong_topics: StrongTopic[];
}

export interface WeakTopic {
  topic_id: number;
  topic_name: string;
  mastery: number;
}

export interface StrongTopic {
  topic_id: number;
  topic_name: string;
  mastery: number;
}

export interface VocabularyStats {
  total_words_learned: number;
  words_mastered: number; // mastery_level >= 4
  total_reviews: number;
  overall_accuracy: number; // percentage
  average_mastery: number; // 0-5
  words_in_progress: number;
  words_due_today: number;
}

export interface ActivityStats {
  total_active_days: number;
  current_streak_days: number;
  longest_streak_days: number;
  average_daily_minutes: number;
  last_activity_date: string | null;
  days_since_last_activity: number;
}

// Learning Path (from IntegrationService.get_personalized_learning_path)
export interface LearningPath {
  focus_areas: FocusArea[];
  daily_plan: DailyPlan;
  weekly_goals: WeeklyGoals;
  recommended_contexts: RecommendedContext[];
  motivation_message: string;
}

export interface FocusArea {
  module: string; // "grammar" | "vocabulary" | "conversation"
  area: string; // Area name
  reason: string; // Why focus on this
  priority: string; // "high" | "medium" | "low"
}

export interface DailyPlan {
  total_duration_minutes: number;
  activities: DailyActivity[];
}

export interface DailyActivity {
  activity: string; // "vocabulary_review" | "grammar_practice" | "conversation"
  duration_minutes: number;
  description: string;
}

export interface WeeklyGoals {
  target_sessions: number;
  target_exercises: number;
  target_vocabulary_reviews: number;
  progress: {
    sessions_completed: number;
    exercises_completed: number;
    reviews_completed: number;
  };
}

export interface RecommendedContext {
  context_id: number;
  name: string;
  category: string;
  difficulty_level: string;
  reason: string;
}

// Due Items
export interface DueItems {
  grammar_topics: DueGrammarTopic[];
  vocabulary_words: DueVocabularyWord[];
  total_due: number;
}

export interface DueGrammarTopic {
  topic_id: number;
  topic_name: string; // name_de
  mastery_level: number;
  days_overdue: number;
}

export interface DueVocabularyWord {
  word_id: number;
  word: string;
  translation_it: string;
  mastery_level: number;
  days_overdue: number;
}

// Recent Activity
export interface Activity {
  type: 'conversation' | 'grammar' | 'vocabulary';
  timestamp: string;
  description: string;
  details: Record<string, any>;
}

// Close Achievements
export interface CloseAchievement {
  achievement_name: string;
  progress_percent: number;
  current_value: number;
  target_value: number;
  tier: string; // "bronze" | "silver" | "gold" | "platinum"
  points: number;
}

// Quick Actions
export interface QuickAction {
  action: string; // "review_due_items" | "start_daily_plan" | "start_conversation" | "practice_grammar"
  label: string;
  priority: string; // "high" | "medium" | "low"
  icon: string; // "clock" | "play" | "chat" | "book"
  context_id?: number; // For conversation actions
}
