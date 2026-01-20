import apiClient from '../client';
import type {
  ContextListItem,
  ContextWithStats,
  ContextCreate,
  ContextUpdate,
  ContextResponse,
  ContextFilter,
} from '../types/conversation.types';

/**
 * ContextService - Conversation context management API endpoints
 * Matches backend/app/api/v1/contexts.py
 */
class ContextService {
  /**
   * GET /api/contexts
   * List all available conversation contexts with optional filtering
   */
  async getContexts(filters?: ContextFilter): Promise<ContextListItem[]> {
    const response = await apiClient.get<ContextListItem[]>('/api/contexts', {
      params: filters,
    });
    return response.data;
  }

  /**
   * GET /api/contexts/{context_id}
   * Get a specific context with detailed stats
   */
  async getContext(contextId: number): Promise<ContextWithStats> {
    const response = await apiClient.get<ContextWithStats>(
      `/api/contexts/${contextId}`
    );
    return response.data;
  }

  /**
   * POST /api/contexts
   * Create a custom conversation context
   */
  async createContext(data: ContextCreate): Promise<ContextResponse> {
    const response = await apiClient.post<ContextResponse>('/api/contexts', data);
    return response.data;
  }

  /**
   * PUT /api/contexts/{context_id}
   * Update an existing context
   */
  async updateContext(
    contextId: number,
    data: ContextUpdate
  ): Promise<ContextResponse> {
    const response = await apiClient.put<ContextResponse>(
      `/api/contexts/${contextId}`,
      data
    );
    return response.data;
  }

  /**
   * DELETE /api/contexts/{context_id}
   * Deactivate a context (soft delete)
   */
  async deleteContext(contextId: number): Promise<void> {
    await apiClient.delete(`/api/contexts/${contextId}`);
  }
}

// Export singleton instance
export default new ContextService();
