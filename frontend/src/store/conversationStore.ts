import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import conversationService from '../api/services/conversationService';
import contextService from '../api/services/contextService';
import type {
  ConversationSessionData,
  SessionState,
  ConversationTurnResponse,
  GrammarFeedbackItem,
  VocabularyItem,
  ContextListItem,
  SessionResponse,
  SessionSummary,
} from '../api/types/conversation.types';

// ========== STORAGE KEYS ==========

const STORAGE_KEY = 'german-learning-conversation-store';
const SESSION_EXPIRY_HOURS = 24;

// ========== CONVERSATION STORE INTERFACE ==========

interface ConversationState {
  // Session state
  sessionState: SessionState;
  currentSession: ConversationSessionData | null;

  // Messages
  messages: ConversationTurnResponse[];
  isTyping: boolean;

  // Grammar feedback panel
  showGrammarPanel: boolean;
  pendingFeedback: GrammarFeedbackItem[];

  // Vocabulary highlighting
  detectedVocabulary: VocabularyItem[];
  showVocabularyHighlights: boolean;

  // Available contexts
  availableContexts: ContextListItem[];

  // Session history
  sessionHistory: SessionResponse[];

  // Session summary (after end)
  sessionSummary: SessionSummary | null;
  grammarTopicsToPractice: Array<{
    error_type: string;
    error_count: number;
    recommendation: string;
    practice_available: boolean;
  }>;

  // Loading states
  isLoadingContexts: boolean;
  isLoadingHistory: boolean;
  isSendingMessage: boolean;

  // Error state
  error: string | null;

  // ========== SESSION ACTIONS ==========
  setSessionState: (state: SessionState) => void;
  startSession: (contextId: number, proficiencyLevel?: string) => Promise<void>;
  sendMessage: (message: string, requestFeedback?: boolean) => Promise<void>;
  endSession: () => Promise<void>;
  clearSession: () => void;

  // Session persistence
  restoreSession: () => ConversationSessionData | null;
  hasIncompleteSession: () => boolean;
  getSessionAge: () => number | null; // hours

  // ========== MESSAGE ACTIONS ==========
  addMessage: (message: ConversationTurnResponse) => void;
  clearMessages: () => void;
  setTyping: (isTyping: boolean) => void;

  // ========== GRAMMAR PANEL ACTIONS ==========
  toggleGrammarPanel: () => void;
  setGrammarPanel: (show: boolean) => void;
  addFeedback: (feedback: GrammarFeedbackItem[]) => void;
  clearFeedback: () => void;

  // ========== VOCABULARY ACTIONS ==========
  addVocabulary: (vocabulary: VocabularyItem[]) => void;
  clearVocabulary: () => void;
  toggleVocabularyHighlights: () => void;

  // ========== CONTEXT ACTIONS ==========
  loadContexts: (filters?: { category?: string; difficulty?: string }) => Promise<void>;
  setContexts: (contexts: ContextListItem[]) => void;

  // ========== HISTORY ACTIONS ==========
  loadHistory: (limit?: number, offset?: number) => Promise<void>;
  setHistory: (history: SessionResponse[]) => void;

  // ========== SUMMARY ACTIONS ==========
  setSummary: (summary: SessionSummary | null) => void;

  // ========== ERROR ACTIONS ==========
  setError: (error: string | null) => void;
  clearError: () => void;
}

// ========== CONVERSATION STORE ==========

export const useConversationStore = create<ConversationState>()(
  persist(
    (set, get) => ({
      // Initial state
      sessionState: 'idle',
      currentSession: null,
      messages: [],
      isTyping: false,
      showGrammarPanel: false,
      pendingFeedback: [],
      detectedVocabulary: [],
      showVocabularyHighlights: true,
      availableContexts: [],
      sessionHistory: [],
      sessionSummary: null,
      grammarTopicsToPractice: [],
      isLoadingContexts: false,
      isLoadingHistory: false,
      isSendingMessage: false,
      error: null,

      // ========== SESSION ACTIONS ==========

      setSessionState: (sessionState) => set({ sessionState }),

      startSession: async (contextId, proficiencyLevel) => {
        try {
          set({ sessionState: 'loading', error: null });

          const response = await conversationService.startSession({
            context_id: contextId,
            user_proficiency_level: proficiencyLevel as any,
          });

          set({
            sessionState: 'active',
            currentSession: {
              sessionId: response.id,
              contextId: response.context_id,
              contextName: response.context_name,
              contextDescription: response.context_description,
              contextCategory: response.context_category,
              contextDifficulty: response.context_difficulty,
              startTime: response.start_time,
              messageCount: 0,
              grammarCorrections: 0,
              vocabularyUsed: 0,
            },
            messages: [],
            pendingFeedback: [],
            detectedVocabulary: [],
          });
        } catch (error: any) {
          set({
            sessionState: 'idle',
            error: error.message || 'Failed to start conversation session',
          });
          throw error;
        }
      },

      sendMessage: async (message, requestFeedback = false) => {
        const { currentSession } = get();
        if (!currentSession) {
          set({ error: 'No active session' });
          return;
        }

        try {
          set({ isSendingMessage: true, isTyping: true, error: null });

          const response = await conversationService.sendMessage(
            currentSession.sessionId,
            { message, request_grammar_feedback: requestFeedback }
          );

          // Create message object
          const newMessage: ConversationTurnResponse = {
            id: Date.now(), // Temporary ID
            session_id: currentSession.sessionId,
            user_message: response.user_message,
            ai_response: response.ai_response,
            grammar_feedback: response.grammar_feedback,
            vocabulary_detected: response.vocabulary_detected,
            timestamp: new Date().toISOString(),
            turn_number: response.turn_number,
          };

          // Update state
          set((state) => ({
            messages: [...state.messages, newMessage],
            pendingFeedback: [
              ...state.pendingFeedback,
              ...response.grammar_feedback,
            ],
            detectedVocabulary: [
              ...state.detectedVocabulary,
              ...response.vocabulary_detected,
            ],
            currentSession: state.currentSession
              ? {
                  ...state.currentSession,
                  messageCount: state.currentSession.messageCount + 1,
                  grammarCorrections:
                    state.currentSession.grammarCorrections +
                    response.grammar_feedback.length,
                  vocabularyUsed:
                    state.currentSession.vocabularyUsed +
                    response.vocabulary_detected.length,
                }
              : null,
            isSendingMessage: false,
            isTyping: false,
          }));
        } catch (error: any) {
          set({
            isSendingMessage: false,
            isTyping: false,
            error: error.message || 'Failed to send message',
          });
          throw error;
        }
      },

      endSession: async () => {
        const { currentSession } = get();
        if (!currentSession) {
          set({ error: 'No active session to end' });
          return;
        }

        try {
          set({ sessionState: 'loading', error: null });

          const response = await conversationService.endSession(
            currentSession.sessionId
          );

          set({
            sessionState: 'completed',
            sessionSummary: response.summary,
            grammarTopicsToPractice: response.grammar_topics_to_practice || [],
            // Clear session data (similar to Grammar BUG-021 fix)
            currentSession: null,
            messages: [],
            pendingFeedback: [],
            detectedVocabulary: [],
          });
        } catch (error: any) {
          set({
            sessionState: 'active',
            error: error.message || 'Failed to end session',
          });
          throw error;
        }
      },

      clearSession: () =>
        set({
          sessionState: 'idle',
          currentSession: null,
          messages: [],
          pendingFeedback: [],
          detectedVocabulary: [],
          sessionSummary: null,
          grammarTopicsToPractice: [],
          error: null,
        }),

      // Session persistence
      restoreSession: () => {
        const state = get();
        if (!state.currentSession) return null;

        // Check if session is expired
        const ageHours = get().getSessionAge();
        if (ageHours !== null && ageHours > SESSION_EXPIRY_HOURS) {
          get().clearSession();
          return null;
        }

        return state.currentSession;
      },

      hasIncompleteSession: () => {
        const state = get();
        if (!state.currentSession) return false;

        const ageHours = get().getSessionAge();
        if (ageHours !== null && ageHours > SESSION_EXPIRY_HOURS) {
          return false;
        }

        return state.sessionState === 'active' || state.sessionState === 'loading';
      },

      getSessionAge: () => {
        const state = get();
        if (!state.currentSession) return null;
        const startTime = new Date(state.currentSession.startTime).getTime();
        return (Date.now() - startTime) / (1000 * 60 * 60);
      },

      // ========== MESSAGE ACTIONS ==========

      addMessage: (message) =>
        set((state) => ({
          messages: [...state.messages, message],
        })),

      clearMessages: () => set({ messages: [] }),

      setTyping: (isTyping) => set({ isTyping }),

      // ========== GRAMMAR PANEL ACTIONS ==========

      toggleGrammarPanel: () =>
        set((state) => ({ showGrammarPanel: !state.showGrammarPanel })),

      setGrammarPanel: (show) => set({ showGrammarPanel: show }),

      addFeedback: (feedback) =>
        set((state) => ({
          pendingFeedback: [...state.pendingFeedback, ...feedback],
        })),

      clearFeedback: () => set({ pendingFeedback: [] }),

      // ========== VOCABULARY ACTIONS ==========

      addVocabulary: (vocabulary) =>
        set((state) => ({
          detectedVocabulary: [...state.detectedVocabulary, ...vocabulary],
        })),

      clearVocabulary: () => set({ detectedVocabulary: [] }),

      toggleVocabularyHighlights: () =>
        set((state) => ({
          showVocabularyHighlights: !state.showVocabularyHighlights,
        })),

      // ========== CONTEXT ACTIONS ==========

      loadContexts: async (filters) => {
        try {
          set({ isLoadingContexts: true, error: null });

          const contexts = await contextService.getContexts(filters);

          set({
            availableContexts: contexts,
            isLoadingContexts: false,
          });
        } catch (error: any) {
          set({
            isLoadingContexts: false,
            error: error.message || 'Failed to load contexts',
          });
        }
      },

      setContexts: (contexts) => set({ availableContexts: contexts }),

      // ========== HISTORY ACTIONS ==========

      loadHistory: async (limit, offset) => {
        try {
          set({ isLoadingHistory: true, error: null });

          const history = await conversationService.getSessionHistory({
            limit,
            offset,
          });

          set({
            sessionHistory: history,
            isLoadingHistory: false,
          });
        } catch (error: any) {
          set({
            isLoadingHistory: false,
            error: error.message || 'Failed to load session history',
          });
        }
      },

      setHistory: (history) => set({ sessionHistory: history }),

      // ========== SUMMARY ACTIONS ==========

      setSummary: (summary) => set({ sessionSummary: summary }),

      // ========== ERROR ACTIONS ==========

      setError: (error) => set({ error }),

      clearError: () => set({ error: null }),
    }),
    {
      name: STORAGE_KEY,
      partialize: (state) => ({
        // Only persist these fields
        currentSession: state.currentSession,
        sessionState: state.sessionState,
        messages: state.messages,
        showGrammarPanel: state.showGrammarPanel,
        pendingFeedback: state.pendingFeedback,
        detectedVocabulary: state.detectedVocabulary,
        showVocabularyHighlights: state.showVocabularyHighlights,
      }),
    }
  )
);
