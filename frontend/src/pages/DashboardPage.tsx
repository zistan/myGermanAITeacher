import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import integrationService from '../api/services/integrationService';
import type { DashboardData } from '../api/types/integration.types';
import { Loading } from '../components/common';
import { OverallProgressCard } from '../components/dashboard/OverallProgressCard';
import { CurrentStreakCard } from '../components/dashboard/CurrentStreakCard';
import { DueItemsCard } from '../components/dashboard/DueItemsCard';
import { QuickActionsCard } from '../components/dashboard/QuickActionsCard';
import { RecentActivityCard } from '../components/dashboard/RecentActivityCard';
import { useNotificationStore } from '../store/notificationStore';
import type { ApiError } from '../api/types/common.types';

export function DashboardPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const data = await integrationService.getDashboardData();
      setDashboardData(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load dashboard', apiError.detail);
    } finally {
      setIsLoading(false);
    }
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  if (!dashboardData) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No dashboard data available</h2>
          <p className="text-gray-600">Please try refreshing the page.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-gray-600">
            Welcome back! Here's your learning progress overview.
          </p>
        </div>

        {/* Grid Layout - 2 columns on large screens */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <OverallProgressCard progress={dashboardData.overall_progress} />
            <CurrentStreakCard activity={dashboardData.overall_progress.activity} />
            <QuickActionsCard
              actions={dashboardData.quick_actions}
              onAction={(action) => {
                // Navigate based on action type
                if (action.action === 'review_due_items') {
                  navigate('/review');
                } else if (action.action === 'start_daily_plan') {
                  navigate('/learning-path');
                } else if (action.action === 'start_conversation') {
                  navigate('/conversation');
                } else if (action.action === 'practice_grammar') {
                  navigate('/grammar');
                }
              }}
            />
          </div>

          {/* Right Column */}
          <div className="space-y-6">
            <DueItemsCard dueItems={dashboardData.due_items} />
            <RecentActivityCard activities={dashboardData.recent_activity} />
          </div>
        </div>

        {/* Close Achievements Section */}
        {dashboardData.close_achievements.length > 0 && (
          <div className="mt-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Almost There!</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {dashboardData.close_achievements.map((achievement, index) => (
                <div
                  key={index}
                  className="bg-white rounded-lg shadow p-4 border-2 border-primary-500"
                >
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-semibold text-gray-900">{achievement.achievement_name}</h3>
                    <span
                      className={`text-xs font-medium px-2 py-1 rounded ${
                        achievement.tier === 'platinum'
                          ? 'bg-gray-200 text-gray-800'
                          : achievement.tier === 'gold'
                          ? 'bg-primary-100 text-primary-800'
                          : achievement.tier === 'silver'
                          ? 'bg-gray-100 text-gray-700'
                          : 'bg-orange-100 text-orange-800'
                      }`}
                    >
                      {achievement.tier}
                    </span>
                  </div>
                  <div className="mb-2">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>
                        {achievement.current_value} / {achievement.target_value}
                      </span>
                      <span>{achievement.progress_percent}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full transition-all"
                        style={{ width: `${achievement.progress_percent}%` }}
                      />
                    </div>
                  </div>
                  <p className="text-xs text-gray-500">{achievement.points} points</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
