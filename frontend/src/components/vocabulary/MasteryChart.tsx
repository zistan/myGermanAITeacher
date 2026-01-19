import type { VocabularyProgressSummary } from '../../api/types/vocabulary.types';
import { Card } from '../common';

export interface MasteryChartProps {
  progress: VocabularyProgressSummary;
}

const masteryLevels = [
  { level: '0', label: 'New', color: 'bg-gray-400' },
  { level: '1', label: 'Learning', color: 'bg-red-400' },
  { level: '2', label: 'Familiar', color: 'bg-orange-400' },
  { level: '3', label: 'Comfortable', color: 'bg-yellow-400' },
  { level: '4', label: 'Confident', color: 'bg-blue-400' },
  { level: '5', label: 'Mastered', color: 'bg-green-400' },
];

export function MasteryChart({ progress }: MasteryChartProps) {
  const totalWords = Object.values(progress.mastery_breakdown).reduce((sum, count) => sum + count, 0);
  const maxCount = Math.max(...Object.values(progress.mastery_breakdown), 1);

  return (
    <Card>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Mastery Distribution</h3>

      {totalWords === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">📊</div>
          <p>No vocabulary data yet</p>
          <p className="text-sm">Start learning words to see your progress</p>
        </div>
      ) : (
        <>
          {/* Bar Chart */}
          <div className="space-y-3">
            {masteryLevels.map(({ level, label, color }) => {
              const count = progress.mastery_breakdown[level] || 0;
              const percentage = totalWords > 0 ? (count / totalWords) * 100 : 0;
              const barWidth = (count / maxCount) * 100;

              return (
                <div key={level} className="flex items-center gap-3">
                  <div className="w-24 text-sm text-gray-600">{label}</div>
                  <div className="flex-1 h-8 bg-gray-100 rounded-lg overflow-hidden">
                    <div
                      className={`h-full ${color} transition-all duration-500 flex items-center justify-end pr-2`}
                      style={{ width: `${barWidth}%`, minWidth: count > 0 ? '24px' : '0' }}
                    >
                      {count > 0 && (
                        <span className="text-xs font-medium text-white">{count}</span>
                      )}
                    </div>
                  </div>
                  <div className="w-12 text-sm text-gray-500 text-right">
                    {percentage.toFixed(0)}%
                  </div>
                </div>
              );
            })}
          </div>

          {/* Summary */}
          <div className="mt-6 pt-4 border-t border-gray-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Total words in progress</span>
              <span className="font-semibold text-gray-900">{totalWords}</span>
            </div>
          </div>
        </>
      )}
    </Card>
  );
}
