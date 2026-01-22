import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';
import type { FocusArea as FocusAreaType } from '../../api/types/integration.types';

interface FocusAreaProps {
  area: FocusAreaType;
  onStartPractice?: () => void;
}

const PRIORITY_COLORS = {
  critical: {
    bg: 'bg-red-50',
    border: 'border-red-500',
    badge: 'bg-red-100 text-red-700',
  },
  high: {
    bg: 'bg-orange-50',
    border: 'border-orange-500',
    badge: 'bg-orange-100 text-orange-700',
  },
  medium: {
    bg: 'bg-yellow-50',
    border: 'border-yellow-500',
    badge: 'bg-yellow-100 text-yellow-700',
  },
  low: {
    bg: 'bg-blue-50',
    border: 'border-blue-500',
    badge: 'bg-blue-100 text-blue-700',
  },
};

const MODULE_COLORS = {
  grammar: 'bg-blue-100 text-blue-700',
  vocabulary: 'bg-green-100 text-green-700',
  conversation: 'bg-purple-100 text-purple-700',
};

/**
 * FocusArea component - Displays a priority-based learning focus area
 *
 * Shows modules the user should focus on based on their current progress
 * and error patterns. Each area has a priority level (critical/high/medium/low)
 * and provides a quick action button to start practice.
 */
export function FocusArea({ area, onStartPractice }: FocusAreaProps) {
  const navigate = useNavigate();
  const colors = PRIORITY_COLORS[area.priority];

  const handleStartPractice = () => {
    if (onStartPractice) {
      onStartPractice();
    } else {
      // Default navigation based on module
      if (area.module === 'grammar') {
        navigate('/grammar/practice');
      } else if (area.module === 'vocabulary') {
        navigate('/vocabulary/flashcards');
      } else if (area.module === 'conversation') {
        navigate('/conversation/start');
      }
    }
  };

  return (
    <div
      className={clsx(
        'border-l-4 rounded-lg p-4 shadow transition-shadow hover:shadow-md',
        colors.bg,
        colors.border
      )}
    >
      {/* Header: Module badge + priority badge */}
      <div className="flex items-center justify-between mb-2">
        <span
          className={clsx(
            'px-2 py-1 text-xs font-medium rounded capitalize',
            MODULE_COLORS[area.module]
          )}
        >
          {area.module}
        </span>
        <span className={clsx('px-2 py-1 text-xs font-semibold rounded', colors.badge)}>
          {area.priority.toUpperCase()}
        </span>
      </div>

      {/* Area name */}
      <h3 className="font-semibold text-gray-900 mb-1">{area.area}</h3>

      {/* Reason */}
      <p className="text-sm text-gray-600 mb-3">{area.reason}</p>

      {/* Action button */}
      <button
        onClick={handleStartPractice}
        className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
      >
        Start Practice
      </button>
    </div>
  );
}
