import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  GrammarExercise,
  GrammarProgressSummary,
  ReviewQueueResponse,
  WeakAreasResponse,
  ExerciseFeedback,
} from '../api/types/grammar.types';

// ========== SESSION STATE TYPES ==========

export interface SessionAnswer {
  exerciseId: number;
  userAnswer: string;
  isCorrect: boolean;
  feedback: ExerciseFeedback | null;
  timeSpent: number;
  timestamp: number;
}

export interface GrammarSessionData {
  sessionId: number;
  exerciseIndex: number;
  answers: SessionAnswer[];
  startTime: number;
  isPaused: boolean;
  pausedAt: number | null;
  totalPausedTime: number;
}

export type GrammarSessionState =
  | 'idle'
  | 'loading'
  | 'active'
  | 'paused'
  | 'feedback'
  | 'completed'
  | 'error';

// ========== STORAGE KEYS ==========

const STORAGE_KEY = 'german-learning-grammar-store';
const SESSION_EXPIRY_HOURS = 24;

// ========== GRAMMAR STORE INTERFACE ==========

interface GrammarState {
  // Session state
  sessionState: GrammarSessionState;
  currentSession: GrammarSessionData | null;

  // Current exercise
  currentExercise: GrammarExercise | null;

  // Bookmarked exercises
  bookmarkedExercises: number[];

  // Session notes (exerciseId -> note)
  sessionNotes: Record<number, string>;

  // Focus mode
  isFocusMode: boolean;

  // Auto-advance settings
  autoAdvanceEnabled: boolean;
  autoAdvanceDelay: number; // seconds

  // Progress data (cached for quick access)
  progressSummary: GrammarProgressSummary | null;
  reviewQueue: ReviewQueueResponse | null;
  weakAreas: WeakAreasResponse | null;

  // Loading states
  isLoadingProgress: boolean;
  isLoadingReviewQueue: boolean;

  // Error state
  error: string | null;

  // ========== SESSION ACTIONS ==========
  setSessionState: (state: GrammarSessionState) => void;
  startSession: (sessionId: number) => void;
  setCurrentExercise: (exercise: GrammarExercise | null) => void;
  recordAnswer: (answer: SessionAnswer) => void;
  incrementExerciseIndex: () => void;
  pauseSession: () => void;
  resumeSession: () => void;
  endSession: () => void;
  clearSession: () => void;

  // Session persistence
  saveSessionProgress: () => void;
  restoreSession: () => GrammarSessionData | null;
  hasIncompleteSession: () => boolean;
  getSessionAge: () => number | null; // hours

  // ========== BOOKMARK ACTIONS ==========
  toggleBookmark: (exerciseId: number) => void;
  isBookmarked: (exerciseId: number) => boolean;
  clearBookmarks: () => void;

  // ========== NOTES ACTIONS ==========
  setNote: (exerciseId: number, note: string) => void;
  getNote: (exerciseId: number) => string;
  clearNotes: () => void;
  getNotesCount: () => number;

  // ========== FOCUS MODE ACTIONS ==========
  toggleFocusMode: () => void;
  setFocusMode: (enabled: boolean) => void;

  // ========== AUTO-ADVANCE ACTIONS ==========
  setAutoAdvance: (enabled: boolean, delay?: number) => void;

  // ========== PROGRESS ACTIONS ==========
  setProgressSummary: (progress: GrammarProgressSummary | null) => void;
  setReviewQueue: (queue: ReviewQueueResponse | null) => void;
  setWeakAreas: (areas: WeakAreasResponse | null) => void;
  setLoadingProgress: (isLoading: boolean) => void;
  setLoadingReviewQueue: (isLoading: boolean) => void;

  // ========== ERROR ACTIONS ==========
  setError: (error: string | null) => void;
  clearError: () => void;
}

// ========== GRAMMAR STORE ==========

export const useGrammarStore = create<GrammarState>()(
  persist(
    (set, get) => ({
      // Initial state
      sessionState: 'idle',
      currentSession: null,
      currentExercise: null,
      bookmarkedExercises: [],
      sessionNotes: {},
      isFocusMode: false,
      autoAdvanceEnabled: false,
      autoAdvanceDelay: 2,
      progressSummary: null,
      reviewQueue: null,
      weakAreas: null,
      isLoadingProgress: false,
      isLoadingReviewQueue: false,
      error: null,

      // ========== SESSION ACTIONS ==========

      setSessionState: (sessionState) => set({ sessionState }),

      startSession: (sessionId) =>
        set({
          sessionState: 'active',
          currentSession: {
            sessionId,
            exerciseIndex: 0,
            answers: [],
            startTime: Date.now(),
            isPaused: false,
            pausedAt: null,
            totalPausedTime: 0,
          },
          currentExercise: null,
          sessionNotes: {},
          bookmarkedExercises: [],
        }),

      setCurrentExercise: (exercise) => set({ currentExercise: exercise }),

      recordAnswer: (answer) =>
        set((state) => ({
          currentSession: state.currentSession
            ? {
                ...state.currentSession,
                answers: [...state.currentSession.answers, answer],
              }
            : null,
        })),

      incrementExerciseIndex: () =>
        set((state) => ({
          currentSession: state.currentSession
            ? {
                ...state.currentSession,
                exerciseIndex: state.currentSession.exerciseIndex + 1,
              }
            : null,
        })),

      pauseSession: () =>
        set((state) => ({
          sessionState: 'paused',
          currentSession: state.currentSession
            ? {
                ...state.currentSession,
                isPaused: true,
                pausedAt: Date.now(),
              }
            : null,
        })),

      resumeSession: () =>
        set((state) => {
          if (!state.currentSession || !state.currentSession.pausedAt) {
            return { sessionState: 'active' };
          }

          const pausedDuration = Date.now() - state.currentSession.pausedAt;
          return {
            sessionState: 'active',
            currentSession: {
              ...state.currentSession,
              isPaused: false,
              pausedAt: null,
              totalPausedTime: state.currentSession.totalPausedTime + pausedDuration,
            },
          };
        }),

      endSession: () =>
        set({
          sessionState: 'completed',
        }),

      clearSession: () =>
        set({
          sessionState: 'idle',
          currentSession: null,
          currentExercise: null,
          sessionNotes: {},
          bookmarkedExercises: [],
        }),

      // Session persistence
      saveSessionProgress: () => {
        const state = get();
        if (state.currentSession) {
          // Zustand persist middleware handles this automatically
          // This is a noop but can be used to trigger manual save if needed
        }
      },

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

        return state.sessionState !== 'completed' && state.sessionState !== 'idle';
      },

      getSessionAge: () => {
        const state = get();
        if (!state.currentSession) return null;
        return (Date.now() - state.currentSession.startTime) / (1000 * 60 * 60);
      },

      // ========== BOOKMARK ACTIONS ==========

      toggleBookmark: (exerciseId) =>
        set((state) => ({
          bookmarkedExercises: state.bookmarkedExercises.includes(exerciseId)
            ? state.bookmarkedExercises.filter((id) => id !== exerciseId)
            : [...state.bookmarkedExercises, exerciseId],
        })),

      isBookmarked: (exerciseId) => {
        return get().bookmarkedExercises.includes(exerciseId);
      },

      clearBookmarks: () => set({ bookmarkedExercises: [] }),

      // ========== NOTES ACTIONS ==========

      setNote: (exerciseId, note) =>
        set((state) => ({
          sessionNotes: {
            ...state.sessionNotes,
            [exerciseId]: note,
          },
        })),

      getNote: (exerciseId) => {
        return get().sessionNotes[exerciseId] || '';
      },

      clearNotes: () => set({ sessionNotes: {} }),

      getNotesCount: () => {
        const notes = get().sessionNotes;
        return Object.values(notes).filter((note) => note.trim().length > 0).length;
      },

      // ========== FOCUS MODE ACTIONS ==========

      toggleFocusMode: () =>
        set((state) => ({ isFocusMode: !state.isFocusMode })),

      setFocusMode: (enabled) => set({ isFocusMode: enabled }),

      // ========== AUTO-ADVANCE ACTIONS ==========

      setAutoAdvance: (enabled, delay) =>
        set((state) => ({
          autoAdvanceEnabled: enabled,
          autoAdvanceDelay: delay !== undefined ? delay : state.autoAdvanceDelay,
        })),

      // ========== PROGRESS ACTIONS ==========

      setProgressSummary: (progress) => set({ progressSummary: progress }),

      setReviewQueue: (queue) => set({ reviewQueue: queue }),

      setWeakAreas: (areas) => set({ weakAreas: areas }),

      setLoadingProgress: (isLoading) => set({ isLoadingProgress: isLoading }),

      setLoadingReviewQueue: (isLoading) => set({ isLoadingReviewQueue: isLoading }),

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
        bookmarkedExercises: state.bookmarkedExercises,
        sessionNotes: state.sessionNotes,
        autoAdvanceEnabled: state.autoAdvanceEnabled,
        autoAdvanceDelay: state.autoAdvanceDelay,
      }),
    }
  )
);
