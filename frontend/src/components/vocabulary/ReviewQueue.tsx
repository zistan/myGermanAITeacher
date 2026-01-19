import { useNavigate } from 'react-router-dom';
import type { VocabularyReviewQueueResponse, VocabularyWithProgress } from '../../api/types/vocabulary.types';
import { Card, Button } from '../common';
import { WordCard } from './WordCard';

export interface ReviewQueueProps {
  reviewQueue: VocabularyReviewQueueResponse;
  onPracticeWord?: (word: VocabularyWithProgress) => void;
}

export function ReviewQueue({ reviewQueue, onPracticeWord }: ReviewQueueProps) {
  const navigate = useNavigate();

  const totalDue = reviewQueue.overdue_count + reviewQueue.due_today_count;

  const handlePracticeAll = () => {
    const allWords = [
      ...reviewQueue.overdue_words,
      ...reviewQueue.due_today_words,
    ];
    if (allWords.length > 0) {
      const wordIds = allWords.map((w) => w.id).join(',');
      navigate(`/vocabulary/flashcards?word_ids=${wordIds}`);
    }
  };

  const handlePracticeOverdue = () => {
    if (reviewQueue.overdue_words.length > 0) {
      const wordIds = reviewQueue.overdue_words.map((w) => w.id).join(',');
      navigate(`/vocabulary/flashcards?word_ids=${wordIds}`);
    }
  };

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Review Queue</h3>
        {totalDue > 0 && (
          <Button
            onClick={handlePracticeAll}
            variant="primary"
            size="sm"
            data-testid="practice-all-due-btn"
          >
            Practice All ({totalDue})
          </Button>
        )}
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="text-center p-3 bg-red-50 rounded-lg">
          <div className="text-2xl font-bold text-red-600">{reviewQueue.overdue_count}</div>
          <div className="text-xs text-gray-600">Overdue</div>
        </div>
        <div className="text-center p-3 bg-yellow-50 rounded-lg">
          <div className="text-2xl font-bold text-yellow-600">{reviewQueue.due_today_count}</div>
          <div className="text-xs text-gray-600">Due Today</div>
        </div>
        <div className="text-center p-3 bg-green-50 rounded-lg">
          <div className="text-2xl font-bold text-green-600">{reviewQueue.upcoming_count}</div>
          <div className="text-xs text-gray-600">Upcoming</div>
        </div>
      </div>

      {totalDue === 0 ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">🎉</div>
          <p className="text-gray-600">No words due for review!</p>
          <p className="text-sm text-gray-500 mt-1">Great job staying on top of your reviews</p>
        </div>
      ) : (
        <div className="space-y-4">
          {/* Overdue words */}
          {reviewQueue.overdue_words.length > 0 && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <h4 className="text-sm font-medium text-red-700">Overdue ({reviewQueue.overdue_count})</h4>
                <button
                  onClick={handlePracticeOverdue}
                  className="text-xs text-red-600 hover:text-red-700"
                >
                  Practice overdue →
                </button>
              </div>
              <div className="space-y-2">
                {reviewQueue.overdue_words.slice(0, 3).map((word) => (
                  <WordCard
                    key={word.id}
                    word={word}
                    variant="compact"
                    onClick={() => onPracticeWord?.(word)}
                    testId={`overdue-word-${word.id}`}
                  />
                ))}
                {reviewQueue.overdue_words.length > 3 && (
                  <p className="text-sm text-gray-500 text-center">
                    +{reviewQueue.overdue_words.length - 3} more overdue
                  </p>
                )}
              </div>
            </div>
          )}

          {/* Due today */}
          {reviewQueue.due_today_words.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-yellow-700 mb-2">
                Due Today ({reviewQueue.due_today_count})
              </h4>
              <div className="space-y-2">
                {reviewQueue.due_today_words.slice(0, 3).map((word) => (
                  <WordCard
                    key={word.id}
                    word={word}
                    variant="compact"
                    onClick={() => onPracticeWord?.(word)}
                    testId={`due-today-word-${word.id}`}
                  />
                ))}
                {reviewQueue.due_today_words.length > 3 && (
                  <p className="text-sm text-gray-500 text-center">
                    +{reviewQueue.due_today_words.length - 3} more due today
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </Card>
  );
}
