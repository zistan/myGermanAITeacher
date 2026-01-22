/**
 * AchievementsPage
 * Displays all achievements with filtering and showcase functionality
 */

import { useEffect, useState, useMemo } from 'react';
import toast from 'react-hot-toast';
import { AchievementCard } from '../../components/analytics/achievements/AchievementCard';
import { AchievementFilters } from '../../components/analytics/achievements/AchievementFilters';
import { Loading } from '../../components/common/Loading';
import analyticsService from '../../api/services/analyticsService';
import type {
  AchievementResponse,
  UserAchievementResponse,
  AchievementProgressResponse,
} from '../../api/types/analytics.types';

export function AchievementsPage() {
  const [allAchievements, setAllAchievements] = useState<AchievementResponse[]>([]);
  const [earned, setEarned] = useState<UserAchievementResponse[]>([]);
  const [progress, setProgress] = useState<AchievementProgressResponse[]>([]);
  const [loading, setLoading] = useState(true);

  // Filters
  const [category, setCategory] = useState('all');
  const [tier, setTier] = useState('all');
  const [status, setStatus] = useState('all');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [achievementsData, earnedData, progressData] = await Promise.all([
        analyticsService.getAllAchievements(),
        analyticsService.getEarnedAchievements(),
        analyticsService.getAchievementProgress(),
      ]);

      setAllAchievements(achievementsData);
      setEarned(earnedData);
      setProgress(progressData);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load achievements');
    } finally {
      setLoading(false);
    }
  };

  const handleToggleShowcase = async (achievementId: number, showcased: boolean) => {
    try {
      await analyticsService.toggleShowcase(achievementId, showcased);

      // Update local state
      setEarned((prev) =>
        prev.map((a) =>
          a.achievement.id === achievementId ? { ...a, is_showcased: showcased } : a
        )
      );

      toast.success(showcased ? 'Added to showcase' : 'Removed from showcase');
    } catch (error: any) {
      toast.error(error.detail || 'Failed to update showcase');
    }
  };

  // Build maps for efficient lookups
  const earnedMap = useMemo(() => {
    const map = new Map<number, UserAchievementResponse>();
    earned.forEach((e) => map.set(e.achievement.id, e));
    return map;
  }, [earned]);

  const progressMap = useMemo(() => {
    const map = new Map<number, AchievementProgressResponse>();
    progress.forEach((p) => map.set(p.achievement.id, p));
    return map;
  }, [progress]);

  // Filter achievements
  const filteredAchievements = useMemo(() => {
    return allAchievements.filter((achievement) => {
      // Category filter
      if (category !== 'all' && achievement.category !== category) {
        return false;
      }

      // Tier filter
      if (tier !== 'all' && achievement.tier !== tier) {
        return false;
      }

      // Status filter
      if (status !== 'all') {
        const prog = progressMap.get(achievement.id);
        const isEarned = prog?.is_completed || false;
        const inProgress =
          !isEarned && prog && prog.current_progress > 0 && prog.current_progress < prog.target_value;

        if (status === 'earned' && !isEarned) return false;
        if (status === 'in-progress' && !inProgress) return false;
        if (status === 'locked' && (isEarned || inProgress)) return false;
      }

      return true;
    });
  }, [allAchievements, category, tier, status, progressMap]);

  // Calculate statistics
  const totalPoints = allAchievements.reduce((sum, a) => sum + a.points, 0);
  const earnedPoints = earned.reduce((sum, e) => sum + e.achievement.points, 0);
  const earnedCount = earned.length;
  const totalCount = allAchievements.length;

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Achievements</h1>
        <p className="mt-2 text-gray-600">
          Earn achievements and showcase your progress
        </p>
      </div>

      {/* Summary Card */}
      <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg shadow p-6 text-white">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <p className="text-primary-100 text-sm">Total Points</p>
            <p className="text-4xl font-bold mt-1">
              {earnedPoints.toLocaleString()} / {totalPoints.toLocaleString()}
            </p>
          </div>
          <div>
            <p className="text-primary-100 text-sm">Achievements Earned</p>
            <p className="text-4xl font-bold mt-1">
              {earnedCount} / {totalCount}
            </p>
          </div>
          <div>
            <p className="text-primary-100 text-sm">Tier Distribution</p>
            <div className="flex space-x-2 mt-2">
              {['bronze', 'silver', 'gold', 'platinum'].map((t) => {
                const count = earned.filter((e) => e.achievement.tier === t).length;
                return (
                  <div key={t} className="bg-white/20 px-3 py-1 rounded-lg text-sm">
                    <span className="capitalize">{t}</span>: {count}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>

      {/* Filters */}
      <AchievementFilters
        category={category}
        tier={tier}
        status={status}
        onCategoryChange={setCategory}
        onTierChange={setTier}
        onStatusChange={setStatus}
      />

      {/* Achievements Grid */}
      {filteredAchievements.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredAchievements.map((achievement) => {
            const prog = progressMap.get(achievement.id);
            const earnedAchievement = earnedMap.get(achievement.id);
            const isEarned = prog?.is_completed || false;
            const inProgress =
              !isEarned &&
              prog &&
              prog.current_progress > 0 &&
              prog.current_progress < prog.target_value;

            const variant = isEarned ? 'earned' : inProgress ? 'in-progress' : 'locked';

            return (
              <AchievementCard
                key={achievement.id}
                achievement={achievement}
                variant={variant}
                earnedDate={isEarned ? prog?.earned_at : null}
                currentProgress={prog?.current_progress}
                targetValue={prog?.target_value}
                progressPercentage={prog?.progress_percentage}
                isShowcased={earnedAchievement?.is_showcased || false}
                onToggleShowcase={isEarned ? handleToggleShowcase : undefined}
              />
            );
          })}
        </div>
      ) : (
        <div className="text-center py-12 bg-white rounded-lg shadow border border-gray-200">
          <p className="text-gray-600">No achievements match the selected filters</p>
        </div>
      )}
    </div>
  );
}
