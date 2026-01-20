import { MessageSquare, Briefcase, Coffee, Star } from 'lucide-react';
import type { ContextListItem } from '../../api/types/conversation.types';

interface ContextCardProps {
  context: ContextListItem;
  onSelect: (contextId: number) => void;
}

export function ContextCard({ context, onSelect }: ContextCardProps) {
  /**
   * Get category icon
   */
  const getCategoryIcon = () => {
    switch (context.category) {
      case 'business':
        return <Briefcase className="h-5 w-5" />;
      case 'daily':
        return <Coffee className="h-5 w-5" />;
      case 'custom':
        return <Star className="h-5 w-5" />;
      default:
        return <MessageSquare className="h-5 w-5" />;
    }
  };

  /**
   * Get category color scheme
   */
  const getCategoryColors = () => {
    switch (context.category) {
      case 'business':
        return {
          gradient: 'from-blue-50 to-blue-100',
          border: 'border-blue-200',
          badge: 'bg-blue-100 text-blue-700',
          icon: 'text-blue-600',
        };
      case 'daily':
        return {
          gradient: 'from-green-50 to-green-100',
          border: 'border-green-200',
          badge: 'bg-green-100 text-green-700',
          icon: 'text-green-600',
        };
      case 'custom':
        return {
          gradient: 'from-purple-50 to-purple-100',
          border: 'border-purple-200',
          badge: 'bg-purple-100 text-purple-700',
          icon: 'text-purple-600',
        };
      default:
        return {
          gradient: 'from-gray-50 to-gray-100',
          border: 'border-gray-200',
          badge: 'bg-gray-100 text-gray-700',
          icon: 'text-gray-600',
        };
    }
  };

  /**
   * Get difficulty badge color
   */
  const getDifficultyColor = () => {
    switch (context.difficulty_level) {
      case 'A1':
      case 'A2':
        return 'bg-green-100 text-green-700';
      case 'B1':
      case 'B2':
        return 'bg-blue-100 text-blue-700';
      case 'C1':
      case 'C2':
        return 'bg-purple-100 text-purple-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  const colors = getCategoryColors();

  return (
    <div
      className={`bg-gradient-to-br ${colors.gradient} border ${colors.border} rounded-lg p-5 shadow-sm hover:shadow-md transition-shadow cursor-pointer group`}
      onClick={() => onSelect(context.id)}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2 rounded-lg bg-white ${colors.icon}`}>
          {getCategoryIcon()}
        </div>
        <div className="flex items-center gap-2">
          <span
            className={`px-2 py-1 text-xs font-medium rounded ${colors.badge}`}
          >
            {context.category.charAt(0).toUpperCase() + context.category.slice(1)}
          </span>
          <span
            className={`px-2 py-1 text-xs font-medium rounded ${getDifficultyColor()}`}
          >
            {context.difficulty_level}
          </span>
        </div>
      </div>

      {/* Content */}
      <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
        {context.name}
      </h3>
      <p className="text-sm text-gray-600 mb-4 line-clamp-2">
        {context.description}
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between pt-3 border-t border-gray-200">
        <div className="flex items-center gap-2 text-sm text-gray-500">
          <MessageSquare className="h-4 w-4" />
          <span>{context.times_used} session{context.times_used !== 1 ? 's' : ''}</span>
        </div>
        <button
          className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          onClick={(e) => {
            e.stopPropagation();
            onSelect(context.id);
          }}
        >
          Start Conversation
        </button>
      </div>
    </div>
  );
}
