import { Button, Card } from '../common';

export interface QuizFeedbackProps {
  isCorrect: boolean;
  userAnswer: string;
  correctAnswer: string;
  explanation: string;
  pointsEarned: number;
  onNext: () => void;
}

export function QuizFeedback({
  isCorrect,
  userAnswer,
  correctAnswer,
  explanation,
  pointsEarned,
  onNext,
}: QuizFeedbackProps) {
  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <div className="text-center space-y-6">
          {/* Result icon */}
          <div className={`text-6xl ${isCorrect ? '' : 'animate-shake'}`}>
            {isCorrect ? '✅' : '❌'}
          </div>

          {/* Result message */}
          <div>
            <h2
              className={`text-2xl font-bold ${
                isCorrect ? 'text-green-600' : 'text-red-600'
              }`}
            >
              {isCorrect ? 'Correct!' : 'Incorrect'}
            </h2>
            {pointsEarned > 0 && (
              <p className="text-primary-600 font-medium mt-1">+{pointsEarned} points</p>
            )}
          </div>

          {/* Answers comparison */}
          <div className="space-y-3">
            <div className="p-4 bg-gray-50 rounded-lg">
              <p className="text-sm text-gray-500 mb-1">Your answer</p>
              <p
                className={`font-medium ${
                  isCorrect ? 'text-green-700' : 'text-red-700'
                }`}
              >
                {userAnswer}
              </p>
            </div>

            {!isCorrect && (
              <div className="p-4 bg-green-50 rounded-lg">
                <p className="text-sm text-gray-500 mb-1">Correct answer</p>
                <p className="font-medium text-green-700">{correctAnswer}</p>
              </div>
            )}
          </div>

          {/* Explanation */}
          <div className="p-4 bg-blue-50 rounded-lg text-left">
            <p className="text-sm font-medium text-blue-800 mb-1">Explanation</p>
            <p className="text-blue-700">{explanation}</p>
          </div>

          {/* Next button */}
          <Button
            onClick={onNext}
            variant="primary"
            fullWidth
            data-testid="next-question-btn quiz-continue-btn"
          >
            Next Question
          </Button>
        </div>
      </Card>

      {/* Keyboard hint */}
      <p className="text-center text-sm text-gray-400 mt-4">
        Press{' '}
        <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs">
          Space
        </kbd>{' '}
        or{' '}
        <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs">
          Enter
        </kbd>{' '}
        to continue
      </p>
    </div>
  );
}
