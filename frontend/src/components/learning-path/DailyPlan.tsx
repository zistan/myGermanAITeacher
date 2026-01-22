import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';
import type { DailyPlan as DailyPlanType, DailyActivity } from '../../api/types/integration.types';

interface DailyPlanProps {
  plan: DailyPlanType;
  onStartActivity?: (activity: DailyActivity) => void;
}

const MODULE_COLORS = {
  vocabulary_review: 'bg-green-100 text-green-700 border-green-200',
  grammar_practice: 'bg-blue-100 text-blue-700 border-blue-200',
  conversation: 'bg-purple-100 text-purple-700 border-purple-200',
};

const TIME_OF_DAY_EMOJI = {
  morning: '🌅',
  midday: '☀️',
  evening: '🌙',
};

/**
 * DailyPlan component - Displays today's personalized study plan
 *
 * Shows a time-boxed daily study plan with activities across all modules
 * (vocabulary, grammar, conversation). Each activity shows duration, description,
 * and a quick-start button.
 */
export function DailyPlan({ plan, onStartActivity }: DailyPlanProps) {
  const navigate = useNavigate();

  const handleStartActivity = (activity: DailyActivity) => {
    if (onStartActivity) {
      onStartActivity(activity);
    } else {
      // Default navigation based on activity type
      if (activity.activity === 'vocabulary_review') {
        navigate('/vocabulary/flashcards');
      } else if (activity.activity === 'grammar_practice') {
        navigate('/grammar/practice');
      } else if (activity.activity === 'conversation') {
        navigate('/conversation/start');
      }
    }
  };

  const getModuleColor = (activity: string): string => {
    return MODULE_COLORS[activity as keyof typeof MODULE_COLORS] || 'bg-gray-100 text-gray-700 border-gray-200';
  };

  const getTimeEmoji = (timeOfDay?: string): string => {
    if (!timeOfDay) return '📚';
    return TIME_OF_DAY_EMOJI[timeOfDay as keyof typeof TIME_OF_DAY_EMOJI] || '📚';
  };

  return (
    <div className="bg-white rounded-lg shadow-lg border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Today's Plan</h2>
          <p className="text-sm text-gray-600 mt-1">Your personalized daily study guide</p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-primary-600">{plan.total_duration_minutes}</div>
          <div className="text-xs text-gray-500 uppercase tracking-wide">minutes</div>
        </div>
      </div>

      {/* Timeline visualization */}
      <div className="space-y-4">
        {plan.activities.map((activity, index) => (
          <div key={index} className="flex items-start space-x-4">
            {/* Time badge */}
            <div className="flex-shrink-0 w-14 h-14 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex flex-col items-center justify-center shadow-sm">
              <span className="text-sm font-bold text-primary-700">
                {activity.duration_minutes}
              </span>
              <span className="text-xs text-primary-600">min</span>
            </div>

            {/* Activity card */}
            <div className="flex-1">
              <div
                className={clsx(
                  'border-l-4 rounded-lg p-4 transition-all hover:shadow-md',
                  getModuleColor(activity.activity)
                )}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center space-x-2">
                    <span className="text-lg">{getTimeEmoji(activity.time_of_day)}</span>
                    <span className="text-xs font-semibold uppercase tracking-wide">
                      {activity.time_of_day || 'Flexible'}
                    </span>
                  </div>
                  {activity.priority && (
                    <span
                      className={clsx(
                        'px-2 py-1 text-xs font-medium rounded',
                        activity.priority === 'high' && 'bg-red-100 text-red-700',
                        activity.priority === 'medium' && 'bg-yellow-100 text-yellow-700',
                        activity.priority === 'low' && 'bg-gray-100 text-gray-700'
                      )}
                    >
                      {activity.priority.toUpperCase()}
                    </span>
                  )}
                </div>
                <p className="text-sm font-medium text-gray-900 mb-3">{activity.description}</p>
                <button
                  onClick={() => handleStartActivity(activity)}
                  className="px-4 py-2 text-sm font-medium bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
                >
                  Start Now →
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Total time summary */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="font-medium text-gray-700">Total Study Time Today</span>
          <span className="font-bold text-gray-900">{plan.total_duration_minutes} minutes</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-primary-500 to-primary-600 h-3 rounded-full transition-all duration-500"
            style={{ width: '0%' }}
            data-testid="progress-bar"
          />
        </div>
        <p className="text-xs text-gray-500 mt-2 text-center">
          Progress updates as you complete activities
        </p>
      </div>
    </div>
  );
}
