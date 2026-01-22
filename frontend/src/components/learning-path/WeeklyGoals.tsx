import type { WeeklyPlan } from '../../api/types/integration.types';

interface WeeklyGoalsProps {
  plan: WeeklyPlan;
}

/**
 * WeeklyGoals component - Displays weekly study goals and focus distribution
 *
 * Shows the weekly session target, module distribution (conversation, grammar, vocabulary),
 * and key milestones to achieve. Styled with a gradient background for emphasis.
 */
export function WeeklyGoals({ plan }: WeeklyGoalsProps) {
  const { goal_sessions, focus_distribution, milestones } = plan;

  const distributionEntries = Object.entries(focus_distribution) as [string, number][];
  const total = distributionEntries.reduce((sum, [_, count]) => sum + count, 0);

  const getModuleIcon = (module: string): string => {
    switch (module) {
      case 'conversation':
        return '💬';
      case 'grammar':
        return '📖';
      case 'vocabulary':
        return '📚';
      default:
        return '📝';
    }
  };

  return (
    <div className="bg-gradient-to-br from-primary-500 via-primary-600 to-primary-700 rounded-lg shadow-lg p-6 text-white">
      {/* Header */}
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">Weekly Goals</h2>
        <p className="text-primary-100 text-sm">Your study targets for this week</p>
      </div>

      {/* Goal sessions */}
      <div className="mb-6 bg-white/10 rounded-lg p-4 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div>
            <div className="text-primary-100 text-sm font-medium mb-1">Target Sessions</div>
            <div className="text-xs text-primary-200">Complete this many practice sessions</div>
          </div>
          <div className="text-5xl font-bold">{goal_sessions}</div>
        </div>
      </div>

      {/* Focus distribution */}
      <div className="mb-6">
        <h3 className="text-sm font-semibold text-primary-100 mb-3 uppercase tracking-wide">
          Focus Distribution
        </h3>
        <div className="grid grid-cols-3 gap-3">
          {distributionEntries.map(([module, count]) => (
            <div
              key={module}
              className="bg-white/20 backdrop-blur-sm rounded-lg p-4 text-center transition-transform hover:scale-105"
            >
              <div className="text-3xl mb-1">{getModuleIcon(module)}</div>
              <div className="text-3xl font-bold mb-1">{count}</div>
              <div className="text-xs text-primary-100 capitalize font-medium">{module}</div>
            </div>
          ))}
        </div>
        {total > 0 && (
          <div className="mt-4 text-xs text-primary-200 text-center">
            {total} sessions total across all modules
          </div>
        )}
      </div>

      {/* Milestones */}
      <div>
        <h3 className="text-sm font-semibold text-primary-100 mb-3 uppercase tracking-wide">
          This Week's Milestones
        </h3>
        <ul className="space-y-2">
          {milestones.map((milestone, index) => (
            <li key={index} className="flex items-start space-x-3">
              <svg
                className="w-5 h-5 mt-0.5 flex-shrink-0"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clipRule="evenodd"
                />
              </svg>
              <span className="text-sm flex-1">{milestone}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* Motivational footer */}
      <div className="mt-6 pt-6 border-t border-white/20">
        <p className="text-center text-sm text-primary-100">
          🎯 Stay consistent and you'll achieve your weekly goals!
        </p>
      </div>
    </div>
  );
}
