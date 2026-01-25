import apiClient from '../client';
import type {
  SessionStart,
  SessionWithContext,
  MessageSend,
  MessageResponse,
  SessionEndResponse,
  SessionResponse,
  SessionHistoryResponse,
  ConversationFilter,
} from '../types/conversation.types';

/**
 * ConversationService - Conversation practice API endpoints
 * Matches backend/app/api/v1/sessions.py
 */
class ConversationService {
  /**
   * POST /api/sessions/start
   * Start a new conversation session with a specific context
   */
  async startSession(request: SessionStart): Promise<SessionWithContext> {
    const response = await apiClient.post<SessionWithContext>(
      '/api/sessions/start',
      request
    );
    return response.data;
  }

  /**
   * POST /api/sessions/{session_id}/message
   * Send a message in an active conversation session
   */
  async sendMessage(
    sessionId: number,
    message: MessageSend
  ): Promise<MessageResponse> {
    const response = await apiClient.post<MessageResponse>(
      `/api/sessions/${sessionId}/message`,
      message
    );
    return response.data;
  }

  /**
   * POST /api/sessions/{session_id}/end
   * End a conversation session and get summary
   */
  async endSession(sessionId: number): Promise<SessionEndResponse> {
    const response = await apiClient.post<SessionEndResponse>(
      `/api/sessions/${sessionId}/end`
    );
    return response.data;
  }

  /**
   * DELETE /api/sessions/{session_id}
   * Delete an abandoned/orphaned conversation session
   */
  async deleteAbandonedSession(sessionId: number): Promise<void> {
    await apiClient.delete(`/api/sessions/${sessionId}`);
  }

  /**
   * GET /api/sessions/history
   * Get user's conversation session history with optional filtering
   */
  async getSessionHistory(
    filters?: ConversationFilter
  ): Promise<SessionResponse[]> {
    const response = await apiClient.get<SessionResponse[]>(
      '/api/sessions/history',
      { params: filters }
    );
    return response.data;
  }

  /**
   * GET /api/v1/integration/session-analysis/{session_id}
   * Get detailed session analysis including full conversation and recommendations
   */
  async getSessionDetail(sessionId: number): Promise<SessionHistoryResponse> {
    const response = await apiClient.get<SessionHistoryResponse>(
      `/api/v1/integration/session-analysis/${sessionId}`
    );
    return response.data;
  }
}

// Export singleton instance
export default new ConversationService();
