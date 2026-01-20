import { X, MessageSquare, Clock, Target, BookOpen, Award, TrendingUp } from 'lucide-react';
import type { SessionSummary as SessionSummaryType } from '../../api/types/conversation.types';

interface SessionSummaryProps {
  summary: SessionSummaryType;
  onClose: () => void;
  onViewDetails: () => void;
  onStartNew: () => void;
}

export function SessionSummary({
  summary,
  onClose,
  onViewDetails,
  onStartNew,
}: SessionSummaryProps) {
  /**
   * Get score color
   */
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-orange-600';
    return 'text-red-600';
  };

  /**
   * Get score badge color
   */
  const getScoreBadgeColor = (score: number) => {
    if (score >= 80) return 'bg-green-100 text-green-700 border-green-300';
    if (score >= 60) return 'bg-blue-100 text-blue-700 border-blue-300';
    if (score >= 40) return 'bg-orange-100 text-orange-700 border-orange-300';
    return 'bg-red-100 text-red-700 border-red-300';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <div className="flex items-center gap-3">
            <div className="bg-blue-100 rounded-full p-2">
              <Award className="h-6 w-6 text-blue-600" />
            </div>
            <h2 className="text-xl font-bold text-gray-900">Session Complete!</h2>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Close"
          >
            <X className="h-5 w-5 text-gray-600" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Overall Score */}
          <div className="text-center">
            <div
              className={`inline-flex items-center justify-center w-32 h-32 rounded-full border-4 ${getScoreBadgeColor(
                summary.overall_score
              )}`}
            >
              <div>
                <div className={`text-4xl font-bold ${getScoreColor(summary.overall_score)}`}>
                  {summary.overall_score}
                </div>
                <div className="text-sm text-gray-600">Overall Score</div>
              </div>
            </div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <StatCard
              icon={<MessageSquare className="h-5 w-5" />}
              label="Total Turns"
              value={summary.total_turns.toString()}
              color="blue"
            />
            <StatCard
              icon={<Clock className="h-5 w-5" />}
              label="Duration"
              value={`${summary.duration_minutes} min`}
              color="green"
            />
            <StatCard
              icon={<Target className="h-5 w-5" />}
              label="Grammar Accuracy"
              value={`${summary.grammar_accuracy}%`}
              color="purple"
            />
            <StatCard
              icon={<BookOpen className="h-5 w-5" />}
              label="Vocabulary Used"
              value={summary.unique_vocabulary_count.toString()}
              color="orange"
            />
          </div>

          {/* Areas for Improvement */}
          {summary.areas_for_improvement && summary.areas_for_improvement.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-blue-600" />
                Areas for Improvement
              </h3>
              <ul className="space-y-2">
                {summary.areas_for_improvement.slice(0, 3).map((area, index) => (
                  <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                    <span className="text-blue-600 font-medium">{index + 1}.</span>
                    <span>{area}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Grammar Topics to Practice */}
          {summary.grammar_topics_to_practice &&
            summary.grammar_topics_to_practice.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-900 mb-3 flex items-center gap-2">
                  <BookOpen className="h-4 w-4 text-green-600" />
                  Recommended Grammar Topics
                </h3>
                <div className="space-y-2">
                  {summary.grammar_topics_to_practice.map((topic) => (
                    <div
                      key={topic.topic_id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <div className="font-medium text-gray-900">{topic.topic_name}</div>
                        <div className="text-sm text-gray-600">
                          {topic.error_count} error{topic.error_count !== 1 ? 's' : ''}
                        </div>
                      </div>
                      <span className="px-3 py-1 text-xs font-medium bg-blue-100 text-blue-700 rounded">
                        Practice
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
        </div>

        {/* Footer */}
        <div className="flex items-center justify-between gap-3 px-6 py-4 border-t border-gray-200 bg-gray-50">
          <button
            onClick={onViewDetails}
            className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 hover:bg-gray-50 rounded-lg transition-colors"
          >
            View Full Analysis
          </button>
          <button
            onClick={onStartNew}
            className="px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            Start New Conversation
          </button>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

function StatCard({ icon, label, value, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
    orange: 'bg-orange-50 text-orange-600',
  };

  return (
    <div className="bg-gray-50 rounded-lg p-4 text-center">
      <div className={`inline-flex p-2 rounded-lg mb-2 ${colorClasses[color]}`}>
        {icon}
      </div>
      <div className="text-2xl font-bold text-gray-900 mb-1">{value}</div>
      <div className="text-xs text-gray-600">{label}</div>
    </div>
  );
}
