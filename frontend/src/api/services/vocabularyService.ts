import apiClient from '../client';
import type {
  VocabularyWord,
  VocabularyWordCreate,
  VocabularyWithProgress,
  FlashcardSessionResponse,
  StartFlashcardSessionRequest,
  SubmitFlashcardAnswerRequest,
  SubmitFlashcardAnswerResponse,
  FlashcardResponse,
  PersonalVocabularyList,
  PersonalVocabularyListCreate,
  PersonalVocabularyListWithWords,
  AddWordToListRequest,
  VocabularyQuizRequest,
  VocabularyQuizResponse,
  SubmitQuizAnswerRequest,
  SubmitQuizAnswerResponse,
  VocabularyProgressSummary,
  VocabularyReviewQueueResponse,
  AnalyzeWordRequest,
  WordAnalysisResponse,
  DetectVocabularyRequest,
  DetectVocabularyResponse,
  WordRecommendationRequest,
  WordRecommendationResponse,
  VocabularyFilters,
} from '../types/vocabulary.types';
import type { DifficultyLevel, MasteryLevel } from '../types/common.types';

/**
 * VocabularyService - Vocabulary learning API endpoints
 * Matches backend/app/api/v1/vocabulary.py
 */
class VocabularyService {
  // ========== WORD ENDPOINTS ==========

  /**
   * GET /api/v1/vocabulary/words
   * List vocabulary words with optional filtering
   */
  async getWords(filters?: VocabularyFilters): Promise<VocabularyWithProgress[]> {
    const response = await apiClient.get<VocabularyWithProgress[]>(
      '/api/v1/vocabulary/words',
      { params: filters }
    );
    return response.data;
  }

  /**
   * GET /api/v1/vocabulary/words/{word_id}
   * Get a specific vocabulary word with progress
   */
  async getWord(wordId: number): Promise<VocabularyWithProgress> {
    const response = await apiClient.get<VocabularyWithProgress>(
      `/api/v1/vocabulary/words/${wordId}`
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/words
   * Create a new vocabulary word
   */
  async createWord(word: VocabularyWordCreate): Promise<VocabularyWord> {
    const response = await apiClient.post<VocabularyWord>(
      '/api/v1/vocabulary/words',
      word
    );
    return response.data;
  }

  // ========== FLASHCARD ENDPOINTS ==========

  /**
   * POST /api/v1/vocabulary/flashcards/start
   * Start a flashcard practice session
   */
  async startFlashcardSession(
    request: StartFlashcardSessionRequest
  ): Promise<FlashcardSessionResponse> {
    const response = await apiClient.post<FlashcardSessionResponse>(
      '/api/v1/vocabulary/flashcards/start',
      request
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/flashcards/{session_id}/answer
   * Submit an answer for the current flashcard
   */
  async submitFlashcardAnswer(
    sessionId: number,
    request: SubmitFlashcardAnswerRequest
  ): Promise<SubmitFlashcardAnswerResponse> {
    const response = await apiClient.post<SubmitFlashcardAnswerResponse>(
      `/api/v1/vocabulary/flashcards/${sessionId}/answer`,
      request
    );
    return response.data;
  }

  /**
   * GET /api/v1/vocabulary/flashcards/{session_id}/current
   * Get the current flashcard in the session
   */
  async getCurrentCard(sessionId: number): Promise<FlashcardResponse> {
    const response = await apiClient.get<FlashcardResponse>(
      `/api/v1/vocabulary/flashcards/${sessionId}/current`
    );
    return response.data;
  }

  // ========== PERSONAL LIST ENDPOINTS ==========

  /**
   * POST /api/v1/vocabulary/lists
   * Create a new personal vocabulary list
   */
  async createList(list: PersonalVocabularyListCreate): Promise<PersonalVocabularyList> {
    const response = await apiClient.post<PersonalVocabularyList>(
      '/api/v1/vocabulary/lists',
      list
    );
    return response.data;
  }

  /**
   * GET /api/v1/vocabulary/lists
   * Get all personal vocabulary lists
   */
  async getLists(): Promise<PersonalVocabularyList[]> {
    const response = await apiClient.get<PersonalVocabularyList[]>(
      '/api/v1/vocabulary/lists'
    );
    return response.data;
  }

  /**
   * GET /api/v1/vocabulary/lists/{list_id}
   * Get a specific list with all words
   */
  async getList(listId: number): Promise<PersonalVocabularyListWithWords> {
    const response = await apiClient.get<PersonalVocabularyListWithWords>(
      `/api/v1/vocabulary/lists/${listId}`
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/lists/{list_id}/words
   * Add a word to a personal list
   */
  async addWordToList(listId: number, request: AddWordToListRequest): Promise<void> {
    await apiClient.post(`/api/v1/vocabulary/lists/${listId}/words`, request);
  }

  /**
   * DELETE /api/v1/vocabulary/lists/{list_id}/words/{word_id}
   * Remove a word from a personal list
   */
  async removeWordFromList(listId: number, wordId: number): Promise<void> {
    await apiClient.delete(`/api/v1/vocabulary/lists/${listId}/words/${wordId}`);
  }

  /**
   * DELETE /api/v1/vocabulary/lists/{list_id}
   * Delete a personal vocabulary list
   */
  async deleteList(listId: number): Promise<void> {
    await apiClient.delete(`/api/v1/vocabulary/lists/${listId}`);
  }

  // ========== QUIZ ENDPOINTS ==========

  /**
   * POST /api/v1/vocabulary/quiz/generate
   * Generate a vocabulary quiz
   */
  async generateQuiz(request: VocabularyQuizRequest): Promise<VocabularyQuizResponse> {
    const response = await apiClient.post<VocabularyQuizResponse>(
      '/api/v1/vocabulary/quiz/generate',
      request
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/quiz/{quiz_id}/answer
   * Submit an answer to a quiz question
   */
  async submitQuizAnswer(
    quizId: number,
    request: SubmitQuizAnswerRequest
  ): Promise<SubmitQuizAnswerResponse> {
    const response = await apiClient.post<SubmitQuizAnswerResponse>(
      `/api/v1/vocabulary/quiz/${quizId}/answer`,
      request
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/quiz/{quiz_id}/complete
   * Mark a vocabulary quiz as completed
   */
  async completeQuiz(quizId: number): Promise<{ quiz_id: number; completed_at: string; message: string }> {
    const response = await apiClient.post<{ quiz_id: number; completed_at: string; message: string }>(
      `/api/v1/vocabulary/quiz/${quizId}/complete`
    );
    return response.data;
  }

  // ========== PROGRESS ENDPOINTS ==========

  /**
   * GET /api/v1/vocabulary/progress/summary
   * Get overall vocabulary progress summary
   */
  async getProgressSummary(): Promise<VocabularyProgressSummary> {
    const response = await apiClient.get<VocabularyProgressSummary>(
      '/api/v1/vocabulary/progress/summary'
    );
    return response.data;
  }

  /**
   * GET /api/v1/vocabulary/progress/review-queue
   * Get words due for review
   */
  async getReviewQueue(): Promise<VocabularyReviewQueueResponse> {
    const response = await apiClient.get<VocabularyReviewQueueResponse>(
      '/api/v1/vocabulary/progress/review-queue'
    );
    return response.data;
  }

  // ========== AI ENDPOINTS ==========

  /**
   * POST /api/v1/vocabulary/analyze
   * AI-powered word analysis
   */
  async analyzeWord(request: AnalyzeWordRequest): Promise<WordAnalysisResponse> {
    const response = await apiClient.post<WordAnalysisResponse>(
      '/api/v1/vocabulary/analyze',
      request
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/detect
   * Detect vocabulary from text
   */
  async detectVocabulary(request: DetectVocabularyRequest): Promise<DetectVocabularyResponse> {
    const response = await apiClient.post<DetectVocabularyResponse>(
      '/api/v1/vocabulary/detect',
      request
    );
    return response.data;
  }

  /**
   * POST /api/v1/vocabulary/recommend
   * Get word recommendations
   */
  async getRecommendations(
    request: WordRecommendationRequest
  ): Promise<WordRecommendationResponse> {
    const response = await apiClient.post<WordRecommendationResponse>(
      '/api/v1/vocabulary/recommend',
      request
    );
    return response.data;
  }

  // ========== UTILITY METHODS ==========

  /**
   * Get categories from existing words
   */
  async getCategories(): Promise<string[]> {
    const words = await this.getWords({ limit: 1000 });
    const categories = new Set(words.map((w) => w.category));
    return Array.from(categories).sort();
  }

  /**
   * Get mastery level label
   */
  getMasteryLabel(level: MasteryLevel | null): string {
    const labels: Record<number, string> = {
      0: 'New',
      1: 'Learning',
      2: 'Familiar',
      3: 'Comfortable',
      4: 'Confident',
      5: 'Mastered',
    };
    return level !== null ? labels[level] || 'Unknown' : 'Not Started';
  }

  /**
   * Get mastery level color class
   */
  getMasteryColor(level: MasteryLevel | null): string {
    const colors: Record<number, string> = {
      0: 'gray',
      1: 'red',
      2: 'orange',
      3: 'yellow',
      4: 'blue',
      5: 'green',
    };
    return level !== null ? colors[level] || 'gray' : 'gray';
  }

  /**
   * Get difficulty label in German
   */
  getDifficultyLabel(level: DifficultyLevel): string {
    const labels: Record<DifficultyLevel, string> = {
      A1: 'Anfänger (A1)',
      A2: 'Grundkenntnisse (A2)',
      B1: 'Mittelstufe (B1)',
      B2: 'Obere Mittelstufe (B2)',
      C1: 'Fortgeschritten (C1)',
      C2: 'Proficient (C2)',
    };
    return labels[level];
  }
}

export default new VocabularyService();
