/**
 * Analytics Service
 * Provides methods for all analytics and progress tracking endpoints.
 * Includes progress tracking, achievements, leaderboards, heatmaps, and error analysis.
 */

import apiClient from '../client';
import type {
  OverallProgressResponse,
  ProgressComparisonResponse,
  ErrorPatternAnalysisResponse,
  CreateSnapshotRequest,
  ProgressSnapshotResponse,
  AchievementResponse,
  UserAchievementResponse,
  AchievementProgressResponse,
  ShowcaseAchievementRequest,
  UserStatsResponse,
  LeaderboardResponse,
  ActivityHeatmapResponse,
  GrammarHeatmapResponse,
} from '../types/analytics.types';

class AnalyticsService {
  // ========== PROGRESS ENDPOINTS ==========

  /**
   * Get comprehensive progress across all modules
   * @returns Overall progress data
   */
  async getProgress(): Promise<OverallProgressResponse> {
    const response = await apiClient.get<OverallProgressResponse>('/api/v1/analytics/progress');
    return response.data;
  }

  /**
   * Compare progress between current and previous period
   * @param periodDays - Number of days to compare (7-90)
   * @returns Progress comparison data
   */
  async getProgressComparison(periodDays: number = 30): Promise<ProgressComparisonResponse> {
    const response = await apiClient.get<ProgressComparisonResponse>(
      '/api/v1/analytics/progress/comparison',
      { params: { period_days: periodDays } }
    );
    return response.data;
  }

  // ========== ERROR ANALYSIS ENDPOINTS ==========

  /**
   * Analyze common error patterns across grammar and conversation
   * @param days - Analysis period in days (7-90)
   * @returns Error pattern analysis
   */
  async getErrorAnalysis(days: number = 30): Promise<ErrorPatternAnalysisResponse> {
    const response = await apiClient.get<ErrorPatternAnalysisResponse>(
      '/api/v1/analytics/errors',
      { params: { days } }
    );
    return response.data;
  }

  // ========== SNAPSHOT ENDPOINTS ==========

  /**
   * Create a point-in-time snapshot of user progress
   * @param request - Snapshot creation request
   * @returns Created snapshot data
   */
  async createSnapshot(request: CreateSnapshotRequest): Promise<ProgressSnapshotResponse> {
    const response = await apiClient.post<ProgressSnapshotResponse>(
      '/api/v1/analytics/snapshots',
      request
    );
    return response.data;
  }

  /**
   * Get historical progress snapshots
   * @param limit - Maximum number of snapshots to return (1-50)
   * @param snapshotType - Optional filter by type (daily, weekly, monthly)
   * @returns Array of progress snapshots
   */
  async getSnapshots(
    limit: number = 10,
    snapshotType?: string
  ): Promise<ProgressSnapshotResponse[]> {
    const params: any = { limit };
    if (snapshotType) {
      params.snapshot_type = snapshotType;
    }

    const response = await apiClient.get<ProgressSnapshotResponse[]>(
      '/api/v1/analytics/snapshots',
      { params }
    );
    return response.data;
  }

  // ========== ACHIEVEMENT ENDPOINTS ==========

  /**
   * Get all available achievements
   * @param category - Optional filter by category
   * @param tier - Optional filter by tier (bronze, silver, gold, platinum)
   * @returns Array of achievements
   */
  async getAllAchievements(
    category?: string,
    tier?: string
  ): Promise<AchievementResponse[]> {
    const params: any = {};
    if (category) params.category = category;
    if (tier) params.tier = tier;

    const response = await apiClient.get<AchievementResponse[]>(
      '/api/v1/analytics/achievements',
      { params }
    );
    return response.data;
  }

  /**
   * Get user's earned achievements
   * @returns Array of earned achievements
   */
  async getEarnedAchievements(): Promise<UserAchievementResponse[]> {
    const response = await apiClient.get<UserAchievementResponse[]>(
      '/api/v1/analytics/achievements/earned'
    );
    return response.data;
  }

  /**
   * Get progress toward all achievements
   * @returns Array of achievement progress
   */
  async getAchievementProgress(): Promise<AchievementProgressResponse[]> {
    const response = await apiClient.get<AchievementProgressResponse[]>(
      '/api/v1/analytics/achievements/progress'
    );
    return response.data;
  }

  /**
   * Toggle achievement showcase status
   * @param achievementId - ID of the achievement
   * @param isShowcased - Whether to showcase the achievement
   * @returns Updated achievement data (message only per backend)
   */
  async toggleShowcase(
    achievementId: number,
    isShowcased: boolean
  ): Promise<{ message: string }> {
    const request: ShowcaseAchievementRequest = {
      achievement_id: achievementId,
      is_showcased: isShowcased,
    };

    const response = await apiClient.post<{ message: string }>(
      `/api/v1/analytics/achievements/${achievementId}/showcase`,
      request
    );
    return response.data;
  }

  // ========== STATS & LEADERBOARDS ENDPOINTS ==========

  /**
   * Get aggregate user statistics
   * @returns User statistics
   */
  async getUserStats(): Promise<UserStatsResponse> {
    const response = await apiClient.get<UserStatsResponse>('/api/v1/analytics/stats');
    return response.data;
  }

  /**
   * Manually refresh user statistics
   * @returns Refresh confirmation message
   */
  async refreshStats(): Promise<{ message: string }> {
    const response = await apiClient.post<{ message: string }>(
      '/api/v1/analytics/stats/refresh'
    );
    return response.data;
  }

  /**
   * Get leaderboard rankings
   * @param type - Leaderboard type (overall, grammar, vocabulary, streak)
   * @param period - Time period (all_time, monthly, weekly)
   * @param limit - Maximum number of entries (10-500)
   * @returns Leaderboard data
   */
  async getLeaderboard(
    type: 'overall' | 'grammar' | 'vocabulary' | 'streak',
    period: string = 'all_time',
    limit: number = 100
  ): Promise<LeaderboardResponse> {
    const response = await apiClient.get<LeaderboardResponse>(
      `/api/v1/analytics/leaderboard/${type}`,
      { params: { period, limit } }
    );
    return response.data;
  }

  // ========== HEATMAP ENDPOINTS ==========

  /**
   * Get activity heatmap for calendar display
   * @param days - Number of days to include (30-730)
   * @returns Activity heatmap data
   */
  async getActivityHeatmap(days: number = 365): Promise<ActivityHeatmapResponse> {
    const response = await apiClient.get<ActivityHeatmapResponse>(
      '/api/v1/analytics/heatmap/activity',
      { params: { days } }
    );
    return response.data;
  }

  /**
   * Get grammar topic mastery heatmap
   * @returns Grammar heatmap data
   */
  async getGrammarHeatmap(): Promise<GrammarHeatmapResponse> {
    const response = await apiClient.get<GrammarHeatmapResponse>(
      '/api/v1/analytics/heatmap/grammar'
    );
    return response.data;
  }
}

export default new AnalyticsService();
