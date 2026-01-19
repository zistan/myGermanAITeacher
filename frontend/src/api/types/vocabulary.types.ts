/**
 * Vocabulary API Types - Match backend schemas EXACTLY
 * Source: backend/app/schemas/vocabulary.py
 */

import type { DifficultyLevel, MasteryLevel } from './common.types';

// ========== VOCABULARY WORD TYPES ==========

export interface VocabularyWord {
  id: number;
  word: string;
  translation_it: string;
  part_of_speech: string;
  gender: 'masculine' | 'feminine' | 'neuter' | null;
  plural_form: string | null;
  difficulty: DifficultyLevel;
  category: string;
  example_de: string;
  example_it: string;
  pronunciation: string | null;
  definition_de: string | null;
  usage_notes: string | null;
  synonyms: string[];
  antonyms: string[];
  is_idiom: boolean;
  is_compound: boolean;
  is_separable_verb: boolean;
  created_at: string;
}

export interface VocabularyWordCreate {
  word: string;
  translation_it: string;
  part_of_speech: string;
  gender?: 'masculine' | 'feminine' | 'neuter' | null;
  plural_form?: string | null;
  difficulty: DifficultyLevel;
  category: string;
  example_de: string;
  example_it: string;
  pronunciation?: string | null;
  definition_de?: string | null;
  usage_notes?: string | null;
  synonyms?: string[];
  antonyms?: string[];
  is_idiom?: boolean;
  is_compound?: boolean;
  is_separable_verb?: boolean;
}

export interface VocabularyWithProgress extends VocabularyWord {
  mastery_level: MasteryLevel | null;
  times_reviewed: number;
  last_reviewed: string | null;
  next_review_due: string | null;
  accuracy_rate: number | null;
}

// ========== FLASHCARD TYPES ==========

export type FlashcardType = 'definition' | 'translation' | 'usage' | 'synonym' | 'example';

export interface FlashcardResponse {
  card_id: string;
  word_id: number;
  word: string;
  card_type: FlashcardType;
  front: string;
  back: string;
  hint: string | null;
  difficulty: DifficultyLevel;
}

export interface StartFlashcardSessionRequest {
  word_ids?: number[] | null;
  category?: string | null;
  difficulty?: DifficultyLevel | null;
  card_count?: number;
  use_spaced_repetition?: boolean;
  card_types?: FlashcardType[] | null;
}

export interface FlashcardSessionResponse {
  session_id: number;
  total_cards: number;
  current_card_number: number;
  current_card: FlashcardResponse;
}

export interface SubmitFlashcardAnswerRequest {
  card_id: string;
  user_answer: string;
  confidence_level: 1 | 2 | 3 | 4 | 5;
  time_spent_seconds?: number | null;
}

export interface SubmitFlashcardAnswerResponse {
  is_correct: boolean;
  correct_answer: string;
  feedback: string;
  next_review_interval_days: number;
  next_card: FlashcardResponse | null;
}

// ========== PERSONAL VOCABULARY LIST TYPES ==========

export interface PersonalVocabularyListCreate {
  name: string;
  description?: string | null;
  is_public?: boolean;
}

export interface PersonalVocabularyList {
  id: number;
  name: string;
  description: string | null;
  is_public: boolean;
  word_count: number;
  created_at: string;
  updated_at: string;
}

export interface PersonalVocabularyListWithWords extends PersonalVocabularyList {
  words: VocabularyWithProgress[];
}

export interface AddWordToListRequest {
  word_id: number;
  notes?: string | null;
}

// ========== VOCABULARY QUIZ TYPES ==========

export type QuizType = 'multiple_choice' | 'fill_blank' | 'matching';

export interface VocabularyQuizRequest {
  word_ids?: number[] | null;
  category?: string | null;
  difficulty?: DifficultyLevel | null;
  quiz_type?: QuizType;
  question_count?: number;
}

export interface VocabularyQuizQuestion {
  question_id: string;
  question: string;
  question_type: QuizType;
  options: string[] | null;
  correct_answer: string;
  word_tested: string;
  explanation: string;
}

export interface VocabularyQuizResponse {
  quiz_id: number;
  questions: VocabularyQuizQuestion[];
  total_questions: number;
  estimated_duration_minutes: number;
}

export interface SubmitQuizAnswerRequest {
  question_id: string;
  user_answer: string;
}

export interface SubmitQuizAnswerResponse {
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
  points_earned: number;
}

// ========== VOCABULARY PROGRESS TYPES ==========

export interface VocabularyProgressSummary {
  total_words_learned: number;
  words_by_level: Record<DifficultyLevel, number>;
  words_by_category: Record<string, number>;
  mastery_breakdown: Record<string, number>;
  total_review_time_minutes: number;
  current_streak_days: number;
  words_due_today: number;
  words_due_this_week: number;
}

export interface WordMasteryDetail {
  word: VocabularyWord;
  mastery_level: MasteryLevel;
  times_reviewed: number;
  times_correct: number;
  accuracy_rate: number;
  last_reviewed: string | null;
  next_review_due: string | null;
  review_history: Array<{
    date: string;
    was_correct: boolean;
    confidence: number;
  }>;
}

export interface VocabularyReviewQueueResponse {
  overdue_count: number;
  due_today_count: number;
  upcoming_count: number;
  overdue_words: VocabularyWithProgress[];
  due_today_words: VocabularyWithProgress[];
  upcoming_words: VocabularyWithProgress[];
}

// ========== WORD ANALYSIS TYPES ==========

export interface AnalyzeWordRequest {
  word: string;
  include_examples?: boolean;
  include_synonyms?: boolean;
}

export interface WordAnalysisResponse {
  word: string;
  translation_it: string;
  part_of_speech: string;
  gender: string | null;
  plural_form: string | null;
  difficulty_level: DifficultyLevel;
  pronunciation: string;
  definition_de: string;
  usage_notes: string | null;
  synonyms: string[];
  antonyms: string[];
  examples: Array<{ de: string; it: string }>;
  collocations: string[];
  is_compound: boolean;
  compound_parts: string[] | null;
  is_separable: boolean;
  separable_prefix: string | null;
  register: 'formal' | 'informal' | 'neutral';
  frequency: 'very_common' | 'common' | 'uncommon' | 'rare';
}

// ========== VOCABULARY DETECTION TYPES ==========

export interface DetectVocabularyRequest {
  text: string;
  min_difficulty?: DifficultyLevel;
  max_words?: number;
}

export interface DetectedVocabularyItem {
  word: string;
  lemma: string;
  translation_it: string;
  part_of_speech: string;
  difficulty: DifficultyLevel;
  context_in_text: string;
  why_important: string;
}

export interface DetectVocabularyResponse {
  detected_words: DetectedVocabularyItem[];
  total_detected: number;
}

// ========== WORD RECOMMENDATION TYPES ==========

export type RecommendationType = 'next_to_learn' | 'similar' | 'related' | 'review_priority';

export interface WordRecommendationRequest {
  based_on_word?: string | null;
  category?: string | null;
  difficulty?: DifficultyLevel | null;
  count?: number;
  recommendation_type?: RecommendationType;
}

export interface WordRecommendationResponse {
  recommended_words: VocabularyWithProgress[];
  reason: string;
}

// ========== VOCABULARY STATISTICS TYPES ==========

export interface VocabularyStatistics {
  total_words_in_database: number;
  user_words_learned: number;
  learning_rate_words_per_week: number;
  average_mastery_level: number;
  strongest_categories: Array<{ category: string; mastery: number; count: number }>;
  weakest_categories: Array<{ category: string; mastery: number; count: number }>;
  retention_rate: number;
  review_accuracy: number;
  estimated_vocabulary_size: number;
  progress_by_level: Record<DifficultyLevel, { total: number; learned: number; mastered: number }>;
}

// ========== FILTER TYPES ==========

export interface VocabularyFilters {
  difficulty?: DifficultyLevel;
  category?: string;
  mastery_level?: MasteryLevel;
  search?: string;
  limit?: number;
  offset?: number;
}
