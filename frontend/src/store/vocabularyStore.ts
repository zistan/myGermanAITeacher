import { create } from 'zustand';
import type {
  VocabularyWithProgress,
  FlashcardSessionResponse,
  FlashcardResponse,
  PersonalVocabularyList,
  VocabularyQuizResponse,
  VocabularyProgressSummary,
  VocabularyFilters,
} from '../api/types/vocabulary.types';

// ========== FLASHCARD SESSION STATE ==========

export type FlashcardSessionState =
  | 'idle'
  | 'setup'
  | 'loading'
  | 'active'
  | 'flipped'
  | 'rating'
  | 'completed'
  | 'error';

interface FlashcardSessionData {
  sessionId: number;
  totalCards: number;
  currentCardNumber: number;
  currentCard: FlashcardResponse | null;
  correctCount: number;
  incorrectCount: number;
  startTime: number;
}

// ========== QUIZ STATE ==========

export type QuizState = 'idle' | 'setup' | 'loading' | 'active' | 'answering' | 'completed' | 'error';

interface QuizSessionData {
  quiz: VocabularyQuizResponse | null;
  currentQuestionIndex: number;
  answers: Array<{
    questionId: string;
    userAnswer: string;
    isCorrect: boolean;
    correctAnswer: string;
  }>;
  score: number;
  startTime: number;
}

// ========== VOCABULARY STORE ==========

interface VocabularyState {
  // Word browsing
  words: VocabularyWithProgress[];
  selectedWord: VocabularyWithProgress | null;
  filters: VocabularyFilters;
  categories: string[];
  isLoadingWords: boolean;

  // Flashcard session
  flashcardState: FlashcardSessionState;
  flashcardSession: FlashcardSessionData | null;

  // Quiz session
  quizState: QuizState;
  quizSession: QuizSessionData | null;

  // Personal lists
  lists: PersonalVocabularyList[];
  isLoadingLists: boolean;

  // Progress
  progress: VocabularyProgressSummary | null;
  isLoadingProgress: boolean;

  // Error handling
  error: string | null;

  // ========== WORD ACTIONS ==========
  setWords: (words: VocabularyWithProgress[]) => void;
  setSelectedWord: (word: VocabularyWithProgress | null) => void;
  setFilters: (filters: Partial<VocabularyFilters>) => void;
  clearFilters: () => void;
  setCategories: (categories: string[]) => void;
  setLoadingWords: (isLoading: boolean) => void;

  // ========== FLASHCARD ACTIONS ==========
  setFlashcardState: (state: FlashcardSessionState) => void;
  startFlashcardSession: (session: FlashcardSessionResponse) => void;
  updateFlashcardCard: (card: FlashcardResponse, cardNumber: number) => void;
  flipCard: () => void;
  recordFlashcardAnswer: (isCorrect: boolean) => void;
  completeFlashcardSession: () => void;
  resetFlashcardSession: () => void;

  // ========== QUIZ ACTIONS ==========
  setQuizState: (state: QuizState) => void;
  startQuiz: (quiz: VocabularyQuizResponse) => void;
  recordQuizAnswer: (
    questionId: string,
    userAnswer: string,
    isCorrect: boolean,
    correctAnswer: string,
    points: number
  ) => void;
  nextQuizQuestion: () => void;
  completeQuiz: () => void;
  resetQuiz: () => void;

  // ========== LIST ACTIONS ==========
  setLists: (lists: PersonalVocabularyList[]) => void;
  addList: (list: PersonalVocabularyList) => void;
  removeList: (listId: number) => void;
  setLoadingLists: (isLoading: boolean) => void;

  // ========== PROGRESS ACTIONS ==========
  setProgress: (progress: VocabularyProgressSummary | null) => void;
  setLoadingProgress: (isLoading: boolean) => void;

  // ========== ERROR ACTIONS ==========
  setError: (error: string | null) => void;
  clearError: () => void;
}

const initialFilters: VocabularyFilters = {};

export const useVocabularyStore = create<VocabularyState>((set) => ({
  // Initial state
  words: [],
  selectedWord: null,
  filters: initialFilters,
  categories: [],
  isLoadingWords: false,

  flashcardState: 'idle',
  flashcardSession: null,

  quizState: 'idle',
  quizSession: null,

  lists: [],
  isLoadingLists: false,

  progress: null,
  isLoadingProgress: false,

  error: null,

  // ========== WORD ACTIONS ==========
  setWords: (words) => set({ words }),

  setSelectedWord: (word) => set({ selectedWord: word }),

  setFilters: (newFilters) =>
    set((state) => ({
      filters: { ...state.filters, ...newFilters },
    })),

  clearFilters: () => set({ filters: initialFilters }),

  setCategories: (categories) => set({ categories }),

  setLoadingWords: (isLoading) => set({ isLoadingWords: isLoading }),

  // ========== FLASHCARD ACTIONS ==========
  setFlashcardState: (flashcardState) => set({ flashcardState }),

  startFlashcardSession: (session) =>
    set({
      flashcardState: 'active',
      flashcardSession: {
        sessionId: session.session_id,
        totalCards: session.total_cards,
        currentCardNumber: session.current_card_number,
        currentCard: session.current_card,
        correctCount: 0,
        incorrectCount: 0,
        startTime: Date.now(),
      },
    }),

  updateFlashcardCard: (card, cardNumber) =>
    set((state) => ({
      flashcardState: 'active',
      flashcardSession: state.flashcardSession
        ? {
            ...state.flashcardSession,
            currentCard: card,
            currentCardNumber: cardNumber,
          }
        : null,
    })),

  flipCard: () =>
    set((state) => ({
      flashcardState: state.flashcardState === 'active' ? 'flipped' : state.flashcardState,
    })),

  recordFlashcardAnswer: (isCorrect) =>
    set((state) => ({
      flashcardState: 'rating',
      flashcardSession: state.flashcardSession
        ? {
            ...state.flashcardSession,
            correctCount: isCorrect
              ? state.flashcardSession.correctCount + 1
              : state.flashcardSession.correctCount,
            incorrectCount: !isCorrect
              ? state.flashcardSession.incorrectCount + 1
              : state.flashcardSession.incorrectCount,
          }
        : null,
    })),

  completeFlashcardSession: () => set({ flashcardState: 'completed' }),

  resetFlashcardSession: () =>
    set({
      flashcardState: 'idle',
      flashcardSession: null,
    }),

  // ========== QUIZ ACTIONS ==========
  setQuizState: (quizState) => set({ quizState }),

  startQuiz: (quiz) =>
    set({
      quizState: 'active',
      quizSession: {
        quiz,
        currentQuestionIndex: 0,
        answers: [],
        score: 0,
        startTime: Date.now(),
      },
    }),

  recordQuizAnswer: (questionId, userAnswer, isCorrect, correctAnswer, points) =>
    set((state) => ({
      quizState: 'answering',
      quizSession: state.quizSession
        ? {
            ...state.quizSession,
            answers: [
              ...state.quizSession.answers,
              { questionId, userAnswer, isCorrect, correctAnswer },
            ],
            score: state.quizSession.score + points,
          }
        : null,
    })),

  nextQuizQuestion: () =>
    set((state) => {
      if (!state.quizSession || !state.quizSession.quiz) return state;

      const nextIndex = state.quizSession.currentQuestionIndex + 1;
      const isComplete = nextIndex >= state.quizSession.quiz.total_questions;

      return {
        quizState: isComplete ? 'completed' : 'active',
        quizSession: {
          ...state.quizSession,
          currentQuestionIndex: nextIndex,
        },
      };
    }),

  completeQuiz: () => set({ quizState: 'completed' }),

  resetQuiz: () =>
    set({
      quizState: 'idle',
      quizSession: null,
    }),

  // ========== LIST ACTIONS ==========
  setLists: (lists) => set({ lists }),

  addList: (list) => set((state) => ({ lists: [...state.lists, list] })),

  removeList: (listId) =>
    set((state) => ({
      lists: state.lists.filter((l) => l.id !== listId),
    })),

  setLoadingLists: (isLoading) => set({ isLoadingLists: isLoading }),

  // ========== PROGRESS ACTIONS ==========
  setProgress: (progress) => set({ progress }),

  setLoadingProgress: (isLoading) => set({ isLoadingProgress: isLoading }),

  // ========== ERROR ACTIONS ==========
  setError: (error) => set({ error }),

  clearError: () => set({ error: null }),
}));
