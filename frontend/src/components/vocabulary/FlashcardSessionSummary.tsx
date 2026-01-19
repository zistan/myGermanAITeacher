import { Button, Card } from '../common';

export interface FlashcardSessionSummaryProps {
  totalCards: number;
  correctCount: number;
  incorrectCount: number;
  sessionDuration: number; // in seconds
  onStartNew: () => void;
  onViewProgress: () => void;
  onBackToBrowser: () => void;
}

export function FlashcardSessionSummary({
  totalCards,
  correctCount,
  incorrectCount,
  sessionDuration,
  onStartNew,
  onViewProgress,
  onBackToBrowser,
}: FlashcardSessionSummaryProps) {
  const accuracy = totalCards > 0 ? Math.round((correctCount / totalCards) * 100) : 0;
  const minutes = Math.floor(sessionDuration / 60);
  const seconds = sessionDuration % 60;

  // Determine performance level and message
  const getPerformanceInfo = () => {
    if (accuracy >= 90) {
      return { emoji: '🏆', message: 'Outstanding!', color: 'text-yellow-600' };
    } else if (accuracy >= 75) {
      return { emoji: '🎉', message: 'Great job!', color: 'text-green-600' };
    } else if (accuracy >= 60) {
      return { emoji: '👍', message: 'Good progress!', color: 'text-blue-600' };
    } else if (accuracy >= 40) {
      return { emoji: '💪', message: 'Keep practicing!', color: 'text-orange-600' };
    } else {
      return { emoji: '📚', message: 'More practice needed', color: 'text-red-600' };
    }
  };

  const performanceInfo = getPerformanceInfo();

  return (
    <div className="max-w-xl mx-auto">
      <Card>
        <div className="text-center space-y-6">
          {/* Header */}
          <div>
            <div className="text-6xl mb-4">{performanceInfo.emoji}</div>
            <h2 className="text-2xl font-bold text-gray-900">Session Complete!</h2>
            <p className={`text-lg font-medium ${performanceInfo.color}`}>
              {performanceInfo.message}
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            {/* Accuracy */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-3xl font-bold text-primary-600">{accuracy}%</div>
              <div className="text-sm text-gray-600">Accuracy</div>
            </div>

            {/* Cards Reviewed */}
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-3xl font-bold text-gray-900">{totalCards}</div>
              <div className="text-sm text-gray-600">Cards Reviewed</div>
            </div>

            {/* Correct */}
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-3xl font-bold text-green-600">{correctCount}</div>
              <div className="text-sm text-gray-600">Correct</div>
            </div>

            {/* Needs Review */}
            <div className="bg-red-50 rounded-lg p-4">
              <div className="text-3xl font-bold text-red-600">{incorrectCount}</div>
              <div className="text-sm text-gray-600">Needs Review</div>
            </div>
          </div>

          {/* Time */}
          <div className="text-gray-600">
            <span className="font-medium">Time spent:</span>{' '}
            {minutes > 0 ? `${minutes}m ${seconds}s` : `${seconds}s`}
          </div>

          {/* Progress visualization */}
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500"
              style={{ width: `${accuracy}%` }}
            />
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3">
            <Button
              onClick={onStartNew}
              variant="primary"
              fullWidth
              data-testid="start-new-session-btn"
            >
              Start New Session
            </Button>
            <Button
              onClick={onViewProgress}
              variant="secondary"
              fullWidth
              data-testid="view-progress-btn"
            >
              View Progress
            </Button>
          </div>
          <Button
            onClick={onBackToBrowser}
            variant="ghost"
            fullWidth
            data-testid="back-to-browser-btn"
          >
            Back to Vocabulary
          </Button>
        </div>
      </Card>
    </div>
  );
}
