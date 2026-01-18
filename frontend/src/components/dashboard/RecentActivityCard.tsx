import type { Activity } from '../../api/types/integration.types';
import { Card, Badge } from '../common';

interface RecentActivityCardProps {
  activities: Activity[];
}

export function RecentActivityCard({ activities }: RecentActivityCardProps) {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case 'conversation':
        return (
          <div className="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
            <svg
              className="w-5 h-5 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
              />
            </svg>
          </div>
        );
      case 'grammar':
        return (
          <div className="flex-shrink-0 w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
            <svg
              className="w-5 h-5 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
              />
            </svg>
          </div>
        );
      case 'vocabulary':
        return (
          <div className="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
            <svg
              className="w-5 h-5 text-purple-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z"
              />
            </svg>
          </div>
        );
      default:
        return (
          <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-full flex items-center justify-center">
            <svg
              className="w-5 h-5 text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M13 10V3L4 14h7v7l9-11h-7z"
              />
            </svg>
          </div>
        );
    }
  };

  const getActivityBadgeVariant = (
    type: string
  ): 'primary' | 'success' | 'danger' | 'warning' | 'info' | 'gray' => {
    switch (type) {
      case 'conversation':
        return 'info';
      case 'grammar':
        return 'success';
      case 'vocabulary':
        return 'primary';
      default:
        return 'gray';
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;

    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
  };

  return (
    <Card>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h2>

      {activities.length === 0 ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">📚</div>
          <p className="text-gray-600">No recent activity.</p>
          <p className="text-sm text-gray-500 mt-1">Start learning to see your progress here!</p>
        </div>
      ) : (
        <div className="space-y-4 max-h-96 overflow-y-auto">
          {activities.map((activity, index) => (
            <div key={index} className="flex items-start">
              {getActivityIcon(activity.type)}
              <div className="ml-4 flex-1">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-900">{activity.description}</p>
                    {activity.details && Object.keys(activity.details).length > 0 && (
                      <div className="mt-1 space-y-1">
                        {activity.details.score !== undefined && (
                          <p className="text-xs text-gray-600">
                            Score: {activity.details.score}%
                          </p>
                        )}
                        {activity.details.duration !== undefined && (
                          <p className="text-xs text-gray-600">
                            Duration: {activity.details.duration} min
                          </p>
                        )}
                        {activity.details.exercises_completed !== undefined && (
                          <p className="text-xs text-gray-600">
                            Exercises: {activity.details.exercises_completed}
                          </p>
                        )}
                        {activity.details.words_reviewed !== undefined && (
                          <p className="text-xs text-gray-600">
                            Words: {activity.details.words_reviewed}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                  <div className="ml-4 flex-shrink-0 flex flex-col items-end">
                    <Badge variant={getActivityBadgeVariant(activity.type)} size="sm">
                      {activity.type}
                    </Badge>
                    <span className="text-xs text-gray-500 mt-1">
                      {formatTimestamp(activity.timestamp)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {activities.length > 0 && (
        <div className="mt-4 pt-4 border-t border-gray-200 text-center">
          <button className="text-sm text-primary-600 hover:text-primary-700 font-medium">
            View All Activity →
          </button>
        </div>
      )}
    </Card>
  );
}
