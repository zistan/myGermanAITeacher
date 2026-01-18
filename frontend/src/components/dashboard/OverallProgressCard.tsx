import type { OverallProgress } from '../../api/types/integration.types';
import { Card, ProgressBar } from '../common';

interface OverallProgressCardProps {
  progress: OverallProgress;
}

export function OverallProgressCard({ progress }: OverallProgressCardProps) {
  return (
    <Card>
      <h2 className="text-lg font-semibold text-gray-900 mb-4">Overall Progress</h2>

      {/* Overall Score */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Overall Score</span>
          <span className="text-2xl font-bold text-primary-600">{progress.overall_score}%</span>
        </div>
        <ProgressBar value={progress.overall_score} color="primary" showLabel={false} />
      </div>

      {/* Weekly Goal Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Weekly Goal</span>
          <span className="text-lg font-semibold text-gray-900">
            {progress.weekly_goal_progress}%
          </span>
        </div>
        <ProgressBar
          value={progress.weekly_goal_progress}
          color="success"
          showLabel={false}
        />
      </div>

      {/* Module Stats Grid */}
      <div className="grid grid-cols-3 gap-4">
        {/* Conversation Stats */}
        <div className="text-center p-3 bg-blue-50 rounded-lg">
          <div className="text-2xl font-bold text-blue-600">
            {progress.conversation.total_sessions}
          </div>
          <div className="text-xs text-gray-600 mt-1">Conversations</div>
          <div className="text-xs text-gray-500 mt-1">
            {progress.conversation.sessions_last_7_days} this week
          </div>
        </div>

        {/* Grammar Stats */}
        <div className="text-center p-3 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">
            {progress.grammar.topics_mastered}
          </div>
          <div className="text-xs text-gray-600 mt-1">Topics Mastered</div>
          <div className="text-xs text-gray-500 mt-1">
            {progress.grammar.overall_accuracy.toFixed(0)}% accuracy
          </div>
        </div>

        {/* Vocabulary Stats */}
        <div className="text-center p-3 bg-purple-50 rounded-lg">
          <div className="text-2xl font-bold text-purple-600">
            {progress.vocabulary.words_mastered}
          </div>
          <div className="text-xs text-gray-600 mt-1">Words Mastered</div>
          <div className="text-xs text-gray-500 mt-1">
            {progress.vocabulary.total_words_learned} total learned
          </div>
        </div>
      </div>

      {/* Activity Stats */}
      <div className="mt-4 pt-4 border-t border-gray-200">
        <div className="grid grid-cols-2 gap-4 text-center">
          <div>
            <div className="text-sm text-gray-600">Total Active Days</div>
            <div className="text-lg font-semibold text-gray-900">
              {progress.activity.total_active_days}
            </div>
          </div>
          <div>
            <div className="text-sm text-gray-600">Avg. Daily Minutes</div>
            <div className="text-lg font-semibold text-gray-900">
              {progress.activity.average_daily_minutes.toFixed(0)}
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
