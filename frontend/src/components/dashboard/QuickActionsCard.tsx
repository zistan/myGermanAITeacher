import type { QuickAction } from '../../api/types/integration.types';
import { Card } from '../common';

interface QuickActionsCardProps {
  actions: QuickAction[];
  onAction: (action: QuickAction) => void;
}

export function QuickActionsCard({ actions, onAction }: QuickActionsCardProps) {
  const getIconForAction = (iconName: string) => {
    switch (iconName) {
      case 'clock':
        return (
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        );
      case 'play':
        return (
          <svg
            className="w-6 h-6"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
            />
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        );
      case 'chat':
        return (
          <svg
            className="w-6 h-6"
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
        );
      case 'book':
        return (
          <svg
            className="w-6 h-6"
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
        );
      default:
        return (
          <svg
            className="w-6 h-6"
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
        );
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'border-danger-500 bg-danger-50 hover:bg-danger-100';
      case 'medium':
        return 'border-primary-500 bg-primary-50 hover:bg-primary-100';
      case 'low':
        return 'border-gray-300 bg-gray-50 hover:bg-gray-100';
      default:
        return 'border-gray-300 bg-white hover:bg-gray-50';
    }
  };

  const getPriorityIconColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-danger-600';
      case 'medium':
        return 'text-primary-600';
      case 'low':
        return 'text-gray-600';
      default:
        return 'text-gray-500';
    }
  };

  return (
    <Card>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>

      {actions.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-600">No recommended actions at the moment.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {actions.map((action, index) => (
            <button
              key={index}
              onClick={() => onAction(action)}
              className={`w-full flex items-center p-4 border-2 rounded-lg transition-all ${getPriorityColor(
                action.priority
              )}`}
            >
              <div className={`flex-shrink-0 ${getPriorityIconColor(action.priority)}`}>
                {getIconForAction(action.icon)}
              </div>
              <div className="ml-4 flex-1 text-left">
                <div className="font-medium text-gray-900">{action.label}</div>
                {action.priority === 'high' && (
                  <div className="text-xs text-danger-600 mt-1">Recommended</div>
                )}
              </div>
              <div className="flex-shrink-0">
                <svg
                  className="w-5 h-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 5l7 7-7 7"
                  />
                </svg>
              </div>
            </button>
          ))}
        </div>
      )}
    </Card>
  );
}
