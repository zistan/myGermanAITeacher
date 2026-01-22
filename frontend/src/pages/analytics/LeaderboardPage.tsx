/**
 * LeaderboardPage
 * Displays rankings across different leaderboard types
 */

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import clsx from 'clsx';
import { Loading } from '../../components/common/Loading';
import { useAuthStore } from '../../store/authStore';
import analyticsService from '../../api/services/analyticsService';
import type { LeaderboardResponse } from '../../api/types/analytics.types';

type LeaderboardType = 'overall' | 'grammar' | 'vocabulary' | 'streak';

const LEADERBOARD_TABS = [
  { id: 'overall' as LeaderboardType, label: 'Overall', metric: 'Total Sessions' },
  { id: 'grammar' as LeaderboardType, label: 'Grammar', metric: 'Topics Mastered' },
  { id: 'vocabulary' as LeaderboardType, label: 'Vocabulary', metric: 'Words Learned' },
  { id: 'streak' as LeaderboardType, label: 'Streak', metric: 'Current Streak' },
];

export function LeaderboardPage() {
  const currentUser = useAuthStore((state) => state.user);
  const [activeTab, setActiveTab] = useState<LeaderboardType>('overall');
  const [leaderboardData, setLeaderboardData] = useState<LeaderboardResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadLeaderboard();
  }, [activeTab]);

  const loadLeaderboard = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getLeaderboard(activeTab, 'all_time', 100);
      setLeaderboardData(data);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const currentMetric = LEADERBOARD_TABS.find((t) => t.id === activeTab)?.metric || 'Metric';

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Leaderboards</h1>
        <p className="mt-2 text-gray-600">See how you rank against other learners</p>
      </div>

      {/* User Stats Summary (if available) */}
      {leaderboardData && leaderboardData.user_rank && (
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg shadow p-6 text-white">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <p className="text-primary-100 text-sm">Your Rank</p>
              <p className="text-4xl font-bold mt-1">#{leaderboardData.user_rank}</p>
            </div>
            <div>
              <p className="text-primary-100 text-sm">{currentMetric}</p>
              <p className="text-4xl font-bold mt-1">
                {leaderboardData.user_entry?.metric_value || 0}
              </p>
            </div>
            <div>
              <p className="text-primary-100 text-sm">Total Users</p>
              <p className="text-4xl font-bold mt-1">{leaderboardData.total_users}</p>
            </div>
          </div>
        </div>
      )}

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px overflow-x-auto">
            {LEADERBOARD_TABS.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={clsx(
                  'px-6 py-3 text-sm font-medium border-b-2 transition-colors whitespace-nowrap',
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
                )}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Leaderboard Table */}
        <div className="p-6">
          {loading ? (
            <div className="flex items-center justify-center py-12">
              <Loading />
            </div>
          ) : leaderboardData && leaderboardData.entries.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="border-b border-gray-200 text-left text-sm font-medium text-gray-600">
                    <th className="pb-3 pr-4">Rank</th>
                    <th className="pb-3 pr-4">Username</th>
                    <th className="pb-3 pr-4 text-right">{currentMetric}</th>
                    <th className="pb-3 text-right">Achievement Points</th>
                  </tr>
                </thead>
                <tbody>
                  {leaderboardData.entries.map((entry) => {
                    const isCurrentUser = entry.user_id === currentUser?.id;
                    return (
                      <tr
                        key={entry.user_id}
                        className={clsx(
                          'border-b border-gray-200 hover:bg-gray-50 transition-colors',
                          isCurrentUser &&
                            'bg-primary-50 border-l-4 border-l-primary-500 font-medium'
                        )}
                      >
                        <td className="py-3 pr-4">
                          <div className="flex items-center">
                            {entry.rank <= 3 ? (
                              <span className="text-2xl">
                                {entry.rank === 1 && '🥇'}
                                {entry.rank === 2 && '🥈'}
                                {entry.rank === 3 && '🥉'}
                              </span>
                            ) : (
                              <span className="text-gray-700">#{entry.rank}</span>
                            )}
                          </div>
                        </td>
                        <td className="py-3 pr-4 text-gray-900">{entry.username}</td>
                        <td className="py-3 pr-4 text-right text-gray-900">
                          {entry.metric_value.toLocaleString()}
                        </td>
                        <td className="py-3 text-right text-gray-900">
                          {entry.score.toLocaleString()}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-gray-600">No leaderboard data available</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
