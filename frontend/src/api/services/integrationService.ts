import apiClient from '../client';
import type { DashboardData, LearningPath } from '../types/integration.types';

/**
 * IntegrationService - Cross-module integration endpoints
 * Matches backend/app/api/v1/integration.py
 */
class IntegrationService {
  /**
   * GET /api/v1/integration/dashboard
   * Get comprehensive dashboard data combining all modules
   *
   * Backend returns:
   * - Overall progress across all modules
   * - Personalized learning path
   * - Items due for review today (grammar + vocabulary)
   * - Recent activity (last 7 days)
   * - Achievements close to completion
   * - Quick action recommendations
   */
  async getDashboardData(): Promise<DashboardData> {
    const response = await apiClient.get<DashboardData>('/api/v1/integration/dashboard');
    return response.data;
  }

  /**
   * GET /api/v1/integration/learning-path
   * Get personalized learning path across all modules
   *
   * Backend returns:
   * - Focus areas based on current progress and errors
   * - Daily study plan (60-90 minutes)
   * - Weekly study goals
   * - Recommended conversation contexts
   * - Motivation message
   */
  async getLearningPath(): Promise<LearningPath> {
    const response = await apiClient.get<LearningPath>('/api/v1/integration/learning-path');
    return response.data;
  }

  /**
   * GET /api/v1/integration/session-analysis/{session_id}
   * Analyze a conversation session and get grammar/vocabulary recommendations
   *
   * Backend returns:
   * - Session summary (duration, message count, context)
   * - Detected grammar topics and vocabulary words
   * - Personalized recommendations for practice
   * - Next steps for learning
   */
  async analyzeConversationSession(sessionId: number): Promise<any> {
    const response = await apiClient.get(`/api/v1/integration/session-analysis/${sessionId}`);
    return response.data;
  }
}

export default new IntegrationService();
