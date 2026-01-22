import { useNavigate } from 'react-router-dom';
import clsx from 'clsx';
import type { RecommendedContext as RecommendedContextType } from '../../api/types/integration.types';

interface RecommendedContextProps {
  context: RecommendedContextType;
  onStartConversation?: () => void;
}

const PRIORITY_COLORS = {
  high: {
    border: 'border-orange-500',
    badge: 'bg-orange-100 text-orange-700',
  },
  medium: {
    border: 'border-yellow-500',
    badge: 'bg-yellow-100 text-yellow-700',
  },
  low: {
    border: 'border-blue-500',
    badge: 'bg-blue-100 text-blue-700',
  },
};

const CATEGORY_ICONS: Record<string, string> = {
  business: '💼',
  daily: '🏠',
  social: '🤝',
  travel: '✈️',
  shopping: '🛍️',
  restaurant: '🍽️',
  medical: '🏥',
  education: '🎓',
  hobbies: '🎨',
};

/**
 * RecommendedContext component - Displays a conversation context recommendation
 *
 * Shows conversation contexts the user should practice based on their learning history.
 * Prioritizes unpracticed or rarely practiced contexts to ensure variety.
 */
export function RecommendedContext({ context, onStartConversation }: RecommendedContextProps) {
  const navigate = useNavigate();
  const colors = PRIORITY_COLORS[context.priority];

  const handleStartConversation = () => {
    if (onStartConversation) {
      onStartConversation();
    } else {
      // Default navigation to conversation start with context ID
      navigate(`/conversation/start?context=${context.context_id}`);
    }
  };

  const getCategoryIcon = (category: string): string => {
    return CATEGORY_ICONS[category.toLowerCase()] || '💬';
  };

  return (
    <div
      className={clsx(
        'border-2 rounded-lg p-4 bg-white shadow transition-all hover:shadow-lg cursor-pointer',
        colors.border
      )}
      onClick={handleStartConversation}
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-3">
        <span className={clsx('px-2 py-1 text-xs font-semibold rounded', colors.badge)}>
          {context.priority.toUpperCase()}
        </span>
        <div className="flex items-center space-x-2">
          <span className="text-lg">{getCategoryIcon(context.category)}</span>
          <span className="text-xs text-gray-500 capitalize font-medium">{context.category}</span>
        </div>
      </div>

      {/* Context name */}
      <h3 className="font-bold text-gray-900 mb-2 text-lg">{context.name}</h3>

      {/* Stats */}
      <div className="flex items-center space-x-4 mb-3 text-xs text-gray-600">
        <div className="flex items-center space-x-1">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
            <path
              fillRule="evenodd"
              d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z"
              clipRule="evenodd"
            />
          </svg>
          <span>Level: {context.difficulty_level}</span>
        </div>
        <div className="flex items-center space-x-1">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path
              fillRule="evenodd"
              d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z"
              clipRule="evenodd"
            />
          </svg>
          <span>Practiced: {context.times_practiced}x</span>
        </div>
      </div>

      {/* Reason */}
      <p className="text-sm text-gray-600 mb-4">{context.reason}</p>

      {/* Action button */}
      <button
        onClick={(e) => {
          e.stopPropagation();
          handleStartConversation();
        }}
        className="w-full px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors font-medium"
      >
        Start Conversation →
      </button>
    </div>
  );
}
