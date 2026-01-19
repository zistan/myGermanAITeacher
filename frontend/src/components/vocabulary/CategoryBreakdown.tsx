import type { VocabularyProgressSummary } from '../../api/types/vocabulary.types';
import { Card } from '../common';
import { CategoryBadge } from './CategoryBadge';

export interface CategoryBreakdownProps {
  progress: VocabularyProgressSummary;
}

export function CategoryBreakdown({ progress }: CategoryBreakdownProps) {
  const categories = Object.entries(progress.words_by_category)
    .map(([category, count]) => ({ category, count }))
    .sort((a, b) => b.count - a.count);

  const totalWords = categories.reduce((sum, c) => sum + c.count, 0);
  const maxCount = Math.max(...categories.map((c) => c.count), 1);

  return (
    <Card>
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Words by Category</h3>

      {categories.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">📂</div>
          <p>No categories yet</p>
        </div>
      ) : (
        <div className="space-y-3">
          {categories.map(({ category, count }) => {
            const percentage = totalWords > 0 ? (count / totalWords) * 100 : 0;
            const barWidth = (count / maxCount) * 100;

            return (
              <div key={category} className="flex items-center gap-3">
                <div className="w-28">
                  <CategoryBadge category={category} size="sm" />
                </div>
                <div className="flex-1 h-6 bg-gray-100 rounded-lg overflow-hidden">
                  <div
                    className="h-full bg-primary-400 transition-all duration-500 flex items-center justify-end pr-2"
                    style={{ width: `${barWidth}%`, minWidth: count > 0 ? '20px' : '0' }}
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
      )}
    </Card>
  );
}
