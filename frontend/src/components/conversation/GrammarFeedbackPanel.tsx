import { useState } from 'react';
import { X, ChevronRight, AlertCircle, CheckCircle2, BookOpen } from 'lucide-react';
import type { GrammarFeedbackItem } from '../../api/types/conversation.types';

interface GrammarFeedbackPanelProps {
  feedback: GrammarFeedbackItem[];
  isVisible: boolean;
  onToggle: () => void;
}

export function GrammarFeedbackPanel({
  feedback,
  isVisible,
  onToggle,
}: GrammarFeedbackPanelProps) {
  // Group feedback by severity
  const groupedFeedback = {
    high: feedback.filter((f) => f.severity === 'high'),
    medium: feedback.filter((f) => f.severity === 'medium'),
    low: feedback.filter((f) => f.severity === 'low'),
  };

  const totalCount = feedback.length;

  if (!isVisible) return null;

  return (
    <div className="h-full bg-white border-l border-gray-200 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-gray-50">
        <div className="flex items-center gap-2">
          <BookOpen className="h-5 w-5 text-blue-600" />
          <h3 className="font-semibold text-gray-900">Grammar Feedback</h3>
          {totalCount > 0 && (
            <span className="px-2 py-0.5 text-xs font-medium bg-blue-100 text-blue-700 rounded-full">
              {totalCount}
            </span>
          )}
        </div>
        <button
          onClick={onToggle}
          className="p-1 hover:bg-gray-200 rounded transition-colors"
          title="Close panel"
        >
          <X className="h-5 w-5 text-gray-600" />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {totalCount === 0 ? (
          <div className="text-center py-8">
            <CheckCircle2 className="h-12 w-12 text-green-500 mx-auto mb-3" />
            <p className="text-gray-600">No grammar issues detected!</p>
            <p className="text-sm text-gray-500 mt-1">
              Keep practicing to maintain your accuracy.
            </p>
          </div>
        ) : (
          <>
            {/* High severity */}
            {groupedFeedback.high.length > 0 && (
              <FeedbackSection
                title="Critical Issues"
                severity="high"
                items={groupedFeedback.high}
                color="red"
              />
            )}

            {/* Medium severity */}
            {groupedFeedback.medium.length > 0 && (
              <FeedbackSection
                title="Important Notes"
                severity="medium"
                items={groupedFeedback.medium}
                color="orange"
              />
            )}

            {/* Low severity */}
            {groupedFeedback.low.length > 0 && (
              <FeedbackSection
                title="Suggestions"
                severity="low"
                items={groupedFeedback.low}
                color="yellow"
              />
            )}
          </>
        )}
      </div>
    </div>
  );
}

interface FeedbackSectionProps {
  title: string;
  severity: 'high' | 'medium' | 'low';
  items: GrammarFeedbackItem[];
  color: 'red' | 'orange' | 'yellow';
}

function FeedbackSection({ title, severity, items, color }: FeedbackSectionProps) {
  const [isExpanded, setIsExpanded] = useState(true);

  const colorClasses = {
    red: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      text: 'text-red-700',
      icon: 'text-red-600',
    },
    orange: {
      bg: 'bg-orange-50',
      border: 'border-orange-200',
      text: 'text-orange-700',
      icon: 'text-orange-600',
    },
    yellow: {
      bg: 'bg-yellow-50',
      border: 'border-yellow-200',
      text: 'text-yellow-700',
      icon: 'text-yellow-600',
    },
  };

  const colors = colorClasses[color];

  return (
    <div className="space-y-2">
      {/* Section header */}
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="w-full flex items-center justify-between text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
      >
        <span className="flex items-center gap-2">
          <AlertCircle className={`h-4 w-4 ${colors.icon}`} />
          {title}
          <span className={`px-2 py-0.5 text-xs ${colors.bg} ${colors.text} rounded-full`}>
            {items.length}
          </span>
        </span>
        <ChevronRight
          className={`h-4 w-4 transition-transform ${
            isExpanded ? 'rotate-90' : ''
          }`}
        />
      </button>

      {/* Section items */}
      {isExpanded && (
        <div className="space-y-2 pl-4">
          {items.map((item, index) => (
            <FeedbackItem key={index} item={item} color={color} />
          ))}
        </div>
      )}
    </div>
  );
}

interface FeedbackItemProps {
  item: GrammarFeedbackItem;
  color: 'red' | 'orange' | 'yellow';
}

function FeedbackItem({ item, color }: FeedbackItemProps) {
  const colorClasses = {
    red: 'border-red-200 bg-red-50',
    orange: 'border-orange-200 bg-orange-50',
    yellow: 'border-yellow-200 bg-yellow-50',
  };

  return (
    <div className={`p-3 rounded-lg border ${colorClasses[color]}`}>
      <div className="space-y-2 text-sm">
        <div className="font-medium text-gray-900">{item.error_type}</div>
        <div className="space-y-1">
          <div className="flex items-baseline gap-2">
            <span className="text-gray-600 text-xs">Incorrect:</span>
            <span className="line-through text-red-600">{item.incorrect}</span>
          </div>
          <div className="flex items-baseline gap-2">
            <span className="text-gray-600 text-xs">Corrected:</span>
            <span className="font-medium text-green-600">{item.corrected}</span>
          </div>
        </div>
        {item.explanation && (
          <p className="text-gray-700 text-xs italic mt-2">
            {item.explanation}
          </p>
        )}
        {item.grammar_topic_id && (
          <button className="text-xs text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1">
            <BookOpen className="h-3 w-3" />
            Practice this topic
          </button>
        )}
      </div>
    </div>
  );
}
