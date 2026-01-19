import { Button, Card } from '../common';

export interface QuizResultsProps {
  totalQuestions: number;
  correctAnswers: number;
  totalPoints: number;
  answers: Array<{
    questionId: string;
    userAnswer: string;
    isCorrect: boolean;
    correctAnswer: string;
  }>;
  onStartNew: () => void;
  onViewProgress: () => void;
  onBackToBrowser: () => void;
}

export function QuizResults({
  totalQuestions,
  correctAnswers,
  totalPoints,
  answers,
  onStartNew,
  onViewProgress,
  onBackToBrowser,
}: QuizResultsProps) {
  const accuracy = totalQuestions > 0 ? Math.round((correctAnswers / totalQuestions) * 100) : 0;
  const incorrectAnswers = totalQuestions - correctAnswers;

  // Determine performance level and message
  const getPerformanceInfo = () => {
    if (accuracy >= 90) {
      return { emoji: '🏆', message: 'Outstanding!', color: 'text-yellow-600', bgColor: 'bg-yellow-50' };
    } else if (accuracy >= 75) {
      return { emoji: '🎉', message: 'Great job!', color: 'text-green-600', bgColor: 'bg-green-50' };
    } else if (accuracy >= 60) {
      return { emoji: '👍', message: 'Good progress!', color: 'text-blue-600', bgColor: 'bg-blue-50' };
    } else if (accuracy >= 40) {
      return { emoji: '💪', message: 'Keep practicing!', color: 'text-orange-600', bgColor: 'bg-orange-50' };
    } else {
      return { emoji: '📚', message: 'More study needed', color: 'text-red-600', bgColor: 'bg-red-50' };
    }
  };

  const performanceInfo = getPerformanceInfo();

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      {/* Main Results Card */}
      <Card>
        <div className="text-center space-y-6">
          {/* Header */}
          <div className={`p-6 -mx-6 -mt-6 ${performanceInfo.bgColor}`}>
            <div className="text-6xl mb-4">{performanceInfo.emoji}</div>
            <h2 className="text-2xl font-bold text-gray-900">Quiz Complete!</h2>
            <p className={`text-lg font-medium ${performanceInfo.color}`}>
              {performanceInfo.message}
            </p>
          </div>

          {/* Score */}
          <div>
            <div className="text-5xl font-bold text-primary-600">{accuracy}%</div>
            <div className="text-gray-600 mt-1">Overall Score</div>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-gray-900">{totalQuestions}</div>
              <div className="text-sm text-gray-600">Questions</div>
            </div>
            <div className="bg-green-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-green-600">{correctAnswers}</div>
              <div className="text-sm text-gray-600">Correct</div>
            </div>
            <div className="bg-red-50 rounded-lg p-4">
              <div className="text-2xl font-bold text-red-600">{incorrectAnswers}</div>
              <div className="text-sm text-gray-600">Incorrect</div>
            </div>
          </div>

          {/* Points */}
          <div className="flex items-center justify-center gap-2 text-lg">
            <span className="text-yellow-500">⭐</span>
            <span className="font-semibold text-gray-900">{totalPoints}</span>
            <span className="text-gray-600">points earned</span>
          </div>

          {/* Progress bar */}
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-1000"
              style={{ width: `${accuracy}%` }}
            />
          </div>

          {/* Actions */}
          <div className="flex flex-col sm:flex-row gap-3 pt-4">
            <Button
              onClick={onStartNew}
              variant="primary"
              fullWidth
              data-testid="start-new-quiz-btn"
            >
              Take Another Quiz
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
            data-testid="back-to-vocabulary-btn"
          >
            Back to Vocabulary
          </Button>
        </div>
      </Card>

      {/* Incorrect Answers Review */}
      {incorrectAnswers > 0 && (
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Review Mistakes</h3>
          <div className="space-y-3">
            {answers
              .filter((a) => !a.isCorrect)
              .map((answer) => (
                <div
                  key={answer.questionId}
                  className="p-4 bg-red-50 rounded-lg border border-red-100"
                >
                  <div className="flex items-start gap-3">
                    <span className="text-red-500 text-lg">❌</span>
                    <div className="flex-1">
                      <div className="text-sm text-gray-600 mb-1">
                        Your answer:{' '}
                        <span className="text-red-700 font-medium">{answer.userAnswer}</span>
                      </div>
                      <div className="text-sm text-gray-600">
                        Correct:{' '}
                        <span className="text-green-700 font-medium">{answer.correctAnswer}</span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
          </div>
        </Card>
      )}
    </div>
  );
}
