import type { VocabularyProgressSummary } from '../../api/types/vocabulary.types';
import { Card } from '../common';

export interface ProgressOverviewProps {
  progress: VocabularyProgressSummary;
}

export function ProgressOverview({ progress }: ProgressOverviewProps) {
  const stats = [
    {
      label: 'Words Learned',
      value: progress.total_words_learned,
      icon: '📚',
      color: 'text-blue-600',
      bgColor: 'bg-blue-50',
    },
    {
      label: 'Current Streak',
      value: `${progress.current_streak_days} days`,
      icon: '🔥',
      color: 'text-orange-600',
      bgColor: 'bg-orange-50',
    },
    {
      label: 'Due Today',
      value: progress.words_due_today,
      icon: '📅',
      color: 'text-purple-600',
      bgColor: 'bg-purple-50',
    },
    {
      label: 'Due This Week',
      value: progress.words_due_this_week,
      icon: '📆',
      color: 'text-green-600',
      bgColor: 'bg-green-50',
    },
    {
      label: 'Total Review Time',
      value: `${progress.total_review_time_minutes} min`,
      icon: '⏱️',
      color: 'text-indigo-600',
      bgColor: 'bg-indigo-50',
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {stats.map((stat) => (
        <Card key={stat.label} className={`${stat.bgColor} border-none`}>
          <div className="text-center">
            <div className="text-3xl mb-2">{stat.icon}</div>
            <div className={`text-2xl font-bold ${stat.color}`}>{stat.value}</div>
            <div className="text-sm text-gray-600 mt-1">{stat.label}</div>
          </div>
        </Card>
      ))}
    </div>
  );
}
