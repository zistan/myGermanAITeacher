import type { ActivityStats } from '../../api/types/integration.types';
import { Card, Badge } from '../common';

interface CurrentStreakCardProps {
  activity: ActivityStats;
}

export function CurrentStreakCard({ activity }: CurrentStreakCardProps) {
  const isActiveToday = (activity.days_since_last_activity ?? 999) === 0;
  const currentStreak = activity.current_streak_days ?? 0;

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Activity Streak</h2>
        {isActiveToday && <Badge variant="success">Active Today</Badge>}
      </div>

      {/* Current Streak */}
      <div className="text-center py-6 bg-gradient-to-br from-primary-50 to-primary-100 rounded-lg mb-4">
        <div className="text-5xl font-bold text-primary-600 mb-2">
          {currentStreak}
        </div>
        <div className="text-sm font-medium text-gray-700">Day Streak</div>
        {currentStreak > 0 && (
          <div className="text-xs text-gray-600 mt-1">Keep it going!</div>
        )}
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">{activity.longest_streak_days ?? 0}</div>
          <div className="text-xs text-gray-600 mt-1">Longest Streak</div>
        </div>
        <div className="text-center p-3 bg-gray-50 rounded-lg">
          <div className="text-2xl font-bold text-gray-900">{activity.total_active_days ?? 0}</div>
          <div className="text-xs text-gray-600 mt-1">Total Active Days</div>
        </div>
      </div>

      {/* Last Activity */}
      {activity.last_activity_date && (
        <div className="mt-4 pt-4 border-t border-gray-200 text-center">
          <div className="text-xs text-gray-600">Last Activity</div>
          <div className="text-sm font-medium text-gray-900">
            {(activity.days_since_last_activity ?? 999) === 0
              ? 'Today'
              : (activity.days_since_last_activity ?? 999) === 1
              ? 'Yesterday'
              : `${activity.days_since_last_activity ?? 0} days ago`}
          </div>
        </div>
      )}

      {/* Motivation Message */}
      {currentStreak === 0 && (activity.days_since_last_activity ?? 999) > 0 && (
        <div className="mt-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
          <p className="text-sm text-orange-800 text-center">
            Start learning today to begin a new streak!
          </p>
        </div>
      )}
    </Card>
  );
}
