/**
 * Conversation API Types
 * Matches backend schemas exactly to prevent validation errors
 */

// ============================================================================
// Core Types
// ============================================================================

export interface GrammarFeedbackItem {
  error_type: string;
  incorrect: string;
  corrected: string;
  explanation: string;
  severity: 'low' | 'medium' | 'high';
  grammar_topic_id?: number;
}

export interface VocabularyItem {
  word_id: number;
  word: string;
  translation_it: string;
  difficulty: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  category?: string;
  is_new: boolean;
}

export interface ConversationTurnResponse {
  id: number;
  session_id: number;
  user_message: string;
  ai_response: string;
  grammar_feedback: GrammarFeedbackItem[];
  vocabulary_detected: VocabularyItem[];
  timestamp: string;
  turn_number: number;
}

// ============================================================================
// Session Types
// ============================================================================

export interface SessionStart {
  context_id: number;
  user_proficiency_level?: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
}

export interface SessionResponse {
  id: number;
  user_id: number;
  context_id: number;
  start_time: string;
  end_time?: string;
  total_turns: number;
  grammar_corrections: number;
  vocabulary_used: number;
  overall_score?: number;
  session_summary?: string;
}

export interface SessionWithContext {
  id: number;
  user_id: number;
  context_id: number;
  context_name: string;
  context_description: string;
  context_category: string;
  context_difficulty: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  start_time: string;
  end_time?: string;
  total_turns: number;
  grammar_corrections: number;
  vocabulary_used: number;
  overall_score?: number;
}

export interface MessageSend {
  message: string;
  request_grammar_feedback?: boolean;
}

export interface MessageResponse {
  user_message: string;
  ai_response: string;
  grammar_feedback: GrammarFeedbackItem[];
  vocabulary_detected: VocabularyItem[];
  turn_number: number;
}

export interface SessionSummary {
  total_turns: number;
  duration_minutes: number;
  grammar_accuracy: number;
  unique_vocabulary_count: number;
  overall_score: number;
  areas_for_improvement: string[];
  grammar_topics_to_practice: Array<{
    topic_id: number;
    topic_name: string;
    error_count: number;
  }>;
}

export interface SessionEndResponse {
  session_id: number;
  summary: SessionSummary;
}

export interface SessionHistoryResponse {
  session: SessionWithContext;
  messages: ConversationTurnResponse[];
  summary: SessionSummary;
}

// ============================================================================
// Context Types
// ============================================================================

export interface ContextListItem {
  id: number;
  name: string;
  description: string;
  category: 'business' | 'daily' | 'custom';
  difficulty_level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  times_used: number;
  is_active: boolean;
  is_default: boolean;
}

export interface ContextWithStats {
  id: number;
  name: string;
  description: string;
  category: 'business' | 'daily' | 'custom';
  difficulty_level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  system_prompt: string;
  example_phrases: string[];
  times_used: number;
  is_active: boolean;
  is_default: boolean;
  created_at: string;
  last_used?: string;
  avg_session_duration?: number;
  avg_turns_per_session?: number;
}

export interface ContextCreate {
  name: string;
  description: string;
  category: 'business' | 'daily' | 'custom';
  difficulty_level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  system_prompt: string;
  example_phrases?: string[];
}

export interface ContextUpdate {
  name?: string;
  description?: string;
  category?: 'business' | 'daily' | 'custom';
  difficulty_level?: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  system_prompt?: string;
  example_phrases?: string[];
  is_active?: boolean;
}

export interface ContextResponse {
  id: number;
  name: string;
  description: string;
  category: 'business' | 'daily' | 'daily';
  difficulty_level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  system_prompt: string;
  example_phrases: string[];
  times_used: number;
  is_active: boolean;
  is_default: boolean;
  created_at: string;
}

// ============================================================================
// Filter Types
// ============================================================================

export interface ConversationFilter {
  context_id?: number;
  start_date?: string;
  end_date?: string;
  min_score?: number;
  limit?: number;
  offset?: number;
}

export interface ContextFilter {
  category?: 'business' | 'daily' | 'custom';
  difficulty?: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
  active_only?: boolean;
}

// ============================================================================
// UI State Types (Frontend-only)
// ============================================================================

export interface ConversationSessionData {
  sessionId: number;
  contextId: number;
  contextName: string;
  contextDescription: string;
  contextCategory: string;
  contextDifficulty: string;
  startTime: string;
  messageCount: number;
  grammarCorrections: number;
  vocabularyUsed: number;
}

export type SessionState = 'idle' | 'selecting' | 'active' | 'loading' | 'completed';
