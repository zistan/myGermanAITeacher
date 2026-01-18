/**
 * Grammar API Types - Match backend GrammarService schemas EXACTLY
 * Source: backend/app/schemas/grammar.py
 */

import type { DifficultyLevel } from './common.types';

// ========== GRAMMAR TOPIC TYPES ==========

export interface GrammarTopic {
  id: number;
  name_de: string;
  name_en: string;
  category: string;
  subcategory: string | null;
  difficulty_level: DifficultyLevel;
  order_index: number;
  description_de: string;
  explanation_de: string;
  created_at: string;
}

export interface GrammarTopicWithStats extends GrammarTopic {
  user_accuracy: number | null; // percentage
  total_attempts: number;
  last_practiced: string | null;
}

// ========== GRAMMAR EXERCISE TYPES ==========

export type ExerciseType =
  | 'fill_blank'
  | 'multiple_choice'
  | 'translation'
  | 'error_correction'
  | 'sentence_building';

export type ContextCategory = 'business' | 'daily' | 'general';

export interface GrammarExercise {
  id: number;
  topic_id: number;
  exercise_type: ExerciseType;
  difficulty_level: DifficultyLevel;
  question_text: string;
  correct_answer: string;
  alternative_answers: string[]; // Multiple choice options or alternative correct answers
  explanation_de: string;
  hints: string[];
  context_category: ContextCategory;
  created_at: string;
}

export interface GrammarExerciseWithTopic extends GrammarExercise {
  topic: GrammarTopic;
}

// ========== PRACTICE SESSION TYPES ==========

export interface StartPracticeRequest {
  topic_ids?: number[] | null; // null or empty = all topics
  difficulty_level?: DifficultyLevel | null;
  exercise_count?: number; // default 10, min 1, max 50
  exercise_types?: ExerciseType[] | null;
  context_category?: ContextCategory | null;
  use_spaced_repetition?: boolean; // default true
}

export interface PracticeSessionResponse {
  session_id: number;
  total_exercises: number;
  current_exercise_number: number;
  estimated_duration_minutes: number;
  topics_included: string[];
}

export interface SubmitAnswerRequest {
  exercise_id: number;
  user_answer: string;
  time_spent_seconds?: number | null;
}

export interface ExerciseFeedback {
  is_correct: boolean;
  is_partially_correct: boolean;
  correct_answer: string;
  user_answer: string;
  feedback_de: string;
  specific_errors: string[];
  suggestions: string[];
  points_earned: number; // 0-3
}

export interface SessionProgress {
  exercises_completed: number;
  exercises_correct: number;
  current_streak: number;
  total_points: number;
  accuracy_percentage: number;
}

export interface SubmitAnswerResponse {
  feedback: ExerciseFeedback;
  session_progress: SessionProgress;
  next_exercise: GrammarExercise | null;
}

export interface EndSessionResponse {
  session_id: number;
  total_exercises: number;
  exercises_correct: number;
  accuracy_percentage: number;
  total_points: number;
  duration_minutes: number;
  topics_practiced: string[];
  improvements: string[];
  next_recommended_topics: number[];
}

// ========== PROGRESS TRACKING TYPES ==========

export interface GrammarProgressSummary {
  total_exercises_completed: number;
  total_practice_time_minutes: number;
  overall_accuracy: number; // percentage
  current_streak_days: number;
  topics_mastered: number;
  topics_in_progress: number;
  topics_not_started: number;
  level_progress: Record<DifficultyLevel, {
    topics_total: number;
    topics_mastered: number;
    accuracy: number;
  }>;
  recent_activity: Array<{
    date: string;
    exercises_completed: number;
    accuracy: number;
  }>;
}

export type MasteryLevel = 'beginner' | 'intermediate' | 'advanced' | 'mastered';

export interface TopicProgressDetail {
  topic: GrammarTopic;
  total_attempts: number;
  correct_attempts: number;
  accuracy: number; // percentage
  mastery_level: MasteryLevel;
  last_practiced: string | null;
  next_review_due: string | null;
  exercises_available: number;
  exercises_completed: number;
}

export interface WeakAreasResponse {
  weak_topics: TopicProgressDetail[];
  recommended_practice_plan: Array<{
    topic_id: number;
    topic_name: string;
    priority: string;
    estimated_time_minutes: number;
  }>;
  estimated_time_to_improve: number; // days
}

// ========== REVIEW QUEUE TYPES ==========

export interface ReviewQueueItem {
  topic_id: number;
  topic_name: string;
  category: string;
  difficulty_level: DifficultyLevel;
  mastery_level: number; // 0.0-5.0
  last_practiced: string;
  next_review_due: string;
  days_overdue: number;
  priority: string; // high, medium, low
}

export interface ReviewQueueResponse {
  total_due: number;
  items: ReviewQueueItem[];
  recommended_session_size: number;
}

// ========== DIAGNOSTIC TEST TYPES ==========

export interface StartDiagnosticRequest {
  target_level: DifficultyLevel;
  num_questions?: number; // default 20, min 10, max 50
  topics?: string[] | null;
}

export interface DiagnosticTestResponse {
  test_id: number;
  total_questions: number;
  estimated_duration_minutes: number;
  instructions: string;
}

export interface DiagnosticTestResults {
  test_id: number;
  total_questions: number;
  correct_answers: number;
  score_percentage: number;
  assessed_level: DifficultyLevel;
  strengths: string[];
  weaknesses: string[];
  recommended_topics: number[];
  detailed_results: Array<{
    question_number: number;
    topic: string;
    correct: boolean;
    time_spent: number;
  }>;
}

// ========== AI GENERATION TYPES ==========

export interface GenerateExercisesRequest {
  topic_id: number;
  exercise_type: ExerciseType;
  difficulty_level: DifficultyLevel;
  count: number; // min 1, max 10
  context_category?: ContextCategory;
}

export interface GenerateExercisesResponse {
  exercises_generated: number;
  exercise_ids: number[];
  topic_name: string;
}

// ========== CATEGORIES ==========

export interface GrammarCategory {
  name: string;
  description: string;
  topic_count: number;
}
