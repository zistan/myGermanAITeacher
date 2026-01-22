/**
 * Analytics Store (Zustand)
 * Minimal store for SHARED analytics state only.
 * Page-specific data should remain local to each page.
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type {
  OverallProgressResponse,
  UserStatsResponse,
  UserAchievementResponse,
} from '../api/types/analytics.types';

interface AnalyticsState {
  // Shared data (used by Dashboard + Analytics pages)
  overallProgress: OverallProgressResponse | null;
  userStats: UserStatsResponse | null;
  earnedAchievements: UserAchievementResponse[] | null;

  // Loading states
  isLoadingProgress: boolean;
  isLoadingStats: boolean;
  isLoadingAchievements: boolean;

  // Actions
  setOverallProgress: (progress: OverallProgressResponse) => void;
  setUserStats: (stats: UserStatsResponse) => void;
  setEarnedAchievements: (achievements: UserAchievementResponse[]) => void;
  setLoadingProgress: (loading: boolean) => void;
  setLoadingStats: (loading: boolean) => void;
  setLoadingAchievements: (loading: boolean) => void;
  clearAnalytics: () => void;
}

export const useAnalyticsStore = create<AnalyticsState>()(
  persist(
    (set) => ({
      // Initial state
      overallProgress: null,
      userStats: null,
      earnedAchievements: null,
      isLoadingProgress: false,
      isLoadingStats: false,
      isLoadingAchievements: false,

      // Actions
      setOverallProgress: (progress) => set({ overallProgress: progress }),
      setUserStats: (stats) => set({ userStats: stats }),
      setEarnedAchievements: (achievements) => set({ earnedAchievements: achievements }),
      setLoadingProgress: (loading) => set({ isLoadingProgress: loading }),
      setLoadingStats: (loading) => set({ isLoadingStats: loading }),
      setLoadingAchievements: (loading) => set({ isLoadingAchievements: loading }),
      clearAnalytics: () =>
        set({
          overallProgress: null,
          userStats: null,
          earnedAchievements: null,
          isLoadingProgress: false,
          isLoadingStats: false,
          isLoadingAchievements: false,
        }),
    }),
    {
      name: 'analytics-storage',
      // Only persist non-loading states
      partialize: (state) => ({
        overallProgress: state.overallProgress,
        userStats: state.userStats,
        earnedAchievements: state.earnedAchievements,
      }),
    }
  )
);
