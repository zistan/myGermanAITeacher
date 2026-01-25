import apiClient from '../client';
import type {
  GrammarTopic,
  GrammarTopicWithStats,
  GrammarExercise,
  StartPracticeRequest,
  PracticeSessionResponse,
  SubmitAnswerRequest,
  SubmitAnswerResponse,
  EndSessionResponse,
  GrammarProgressSummary,
  TopicProgressDetail,
  WeakAreasResponse,
  ReviewQueueResponse,
  StartDiagnosticRequest,
  DiagnosticTestResponse,
  DiagnosticTestResults,
  GenerateExercisesRequest,
  GenerateExercisesResponse,
  GrammarCategory,
} from '../types/grammar.types';
import type { DifficultyLevel } from '../types/common.types';

/**
 * GrammarService - Grammar learning API endpoints
 * Matches backend/app/api/v1/grammar.py
 */
class GrammarService {
  /**
   * GET /api/grammar/topics
   * List all grammar topics with optional filtering
   */
  async getTopics(params?: {
    category?: string;
    difficulty?: DifficultyLevel;
  }): Promise<GrammarTopic[]> {
    const response = await apiClient.get<GrammarTopic[]>('/api/grammar/topics', { params });
    return response.data;
  }

  /**
   * GET /api/grammar/topics/{topic_id}
   * Get a specific grammar topic with user's progress stats
   */
  async getTopic(topicId: number): Promise<GrammarTopicWithStats> {
    const response = await apiClient.get<GrammarTopicWithStats>(
      `/api/grammar/topics/${topicId}`
    );
    return response.data;
  }

  /**
   * POST /api/grammar/practice/start
   * Start a new grammar practice session
   */
  async startPracticeSession(
    request: StartPracticeRequest
  ): Promise<PracticeSessionResponse> {
    const response = await apiClient.post<PracticeSessionResponse>(
      '/api/grammar/practice/start',
      request
    );
    return response.data;
  }

  /**
   * GET /api/grammar/practice/{session_id}/next
   * Get the next exercise in the practice session
   */
  async getNextExercise(sessionId: number): Promise<GrammarExercise> {
    const response = await apiClient.get<GrammarExercise>(
      `/api/grammar/practice/${sessionId}/next`
    );
    return response.data;
  }

  /**
   * POST /api/grammar/practice/{session_id}/answer
   * Submit an answer to the current exercise
   */
  async submitAnswer(
    sessionId: number,
    request: SubmitAnswerRequest
  ): Promise<SubmitAnswerResponse> {
    const response = await apiClient.post<SubmitAnswerResponse>(
      `/api/grammar/practice/${sessionId}/answer`,
      request
    );
    return response.data;
  }

  /**
   * POST /api/grammar/practice/{session_id}/end
   * End the practice session and get results
   */
  async endPracticeSession(sessionId: number): Promise<EndSessionResponse> {
    const response = await apiClient.post<EndSessionResponse>(
      `/api/grammar/practice/${sessionId}/end`
    );
    return response.data;
  }

  /**
   * DELETE /api/grammar/practice/{session_id}
   * Delete an abandoned/orphaned grammar session
   */
  async deleteAbandonedSession(sessionId: number): Promise<void> {
    await apiClient.delete(`/api/grammar/practice/${sessionId}`);
  }

  /**
   * GET /api/grammar/progress
   * Get overall grammar progress summary
   */
  async getProgressSummary(): Promise<GrammarProgressSummary> {
    const response = await apiClient.get<GrammarProgressSummary>('/api/grammar/progress');
    return response.data;
  }

  /**
   * GET /api/grammar/progress/topic/{topic_id}
   * Get detailed progress for a specific topic
   */
  async getTopicProgress(topicId: number): Promise<TopicProgressDetail> {
    const response = await apiClient.get<TopicProgressDetail>(
      `/api/grammar/progress/topic/${topicId}`
    );
    return response.data;
  }

  /**
   * GET /api/grammar/progress/weak-areas
   * Get user's weak areas with recommendations
   */
  async getWeakAreas(): Promise<WeakAreasResponse> {
    const response = await apiClient.get<WeakAreasResponse>(
      '/api/grammar/progress/weak-areas'
    );
    return response.data;
  }

  /**
   * GET /api/grammar/review-queue
   * Get topics due for review (spaced repetition)
   */
  async getReviewQueue(): Promise<ReviewQueueResponse> {
    const response = await apiClient.get<ReviewQueueResponse>('/api/grammar/review-queue');
    return response.data;
  }

  /**
   * POST /api/grammar/diagnostic/start
   * Start a diagnostic test
   */
  async startDiagnosticTest(
    request: StartDiagnosticRequest
  ): Promise<DiagnosticTestResponse> {
    const response = await apiClient.post<DiagnosticTestResponse>(
      '/api/grammar/diagnostic/start',
      request
    );
    return response.data;
  }

  /**
   * POST /api/grammar/diagnostic/complete
   * Complete diagnostic test and get results
   */
  async completeDiagnosticTest(testId: number): Promise<DiagnosticTestResults> {
    const response = await apiClient.post<DiagnosticTestResults>(
      '/api/grammar/diagnostic/complete',
      { test_id: testId }
    );
    return response.data;
  }

  /**
   * POST /api/grammar/generate-exercises
   * AI-generate new exercises for a topic
   */
  async generateExercises(
    request: GenerateExercisesRequest
  ): Promise<GenerateExercisesResponse> {
    const response = await apiClient.post<GenerateExercisesResponse>(
      '/api/grammar/generate-exercises',
      request
    );
    return response.data;
  }

  /**
   * GET /api/grammar/categories
   * Get list of grammar categories with topic counts
   */
  async getCategories(): Promise<GrammarCategory[]> {
    const response = await apiClient.get<GrammarCategory[]>('/api/grammar/categories');
    return response.data;
  }

  /**
   * GET /api/grammar/recommendations
   * Get personalized practice recommendations
   */
  async getRecommendations(): Promise<{
    recommended_topics: Array<{
      topic_id: number;
      topic_name: string;
      reason: string;
      priority: string;
    }>;
    next_session_suggestion: {
      topic_ids: number[];
      difficulty_level: DifficultyLevel;
      exercise_count: number;
      estimated_duration_minutes: number;
    };
  }> {
    const response = await apiClient.get('/api/grammar/recommendations');
    return response.data;
  }
}

export default new GrammarService();
