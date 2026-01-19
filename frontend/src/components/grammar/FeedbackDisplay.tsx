import type { ExerciseFeedback } from '../../api/types/grammar.types';
import { Button, Badge } from '../common';

interface FeedbackDisplayProps {
  feedback: ExerciseFeedback;
  onNext: () => void;
}

export function FeedbackDisplay({ feedback, onNext }: FeedbackDisplayProps) {
  const isCorrect = feedback.is_correct;
  const isPartial = feedback.is_partially_correct;

  return (
    <div className="space-y-6">
      {/* Result Header */}
      <div
        className={`p-6 rounded-lg border-2 ${
          isCorrect
            ? 'bg-green-50 border-green-500'
            : isPartial
            ? 'bg-yellow-50 border-yellow-500'
            : 'bg-red-50 border-red-500'
        }`}
      >
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center">
            <div className="text-3xl mr-3">
              {isCorrect ? '✅' : isPartial ? '⚠️' : '❌'}
            </div>
            <div>
              <h3
                className={`text-xl font-bold ${
                  isCorrect
                    ? 'text-green-800'
                    : isPartial
                    ? 'text-yellow-800'
                    : 'text-red-800'
                }`}
              >
                {isCorrect
                  ? 'Correct!'
                  : isPartial
                  ? 'Partially Correct'
                  : 'Incorrect'}
              </h3>
              <p
                className={`text-sm ${
                  isCorrect
                    ? 'text-green-700'
                    : isPartial
                    ? 'text-yellow-700'
                    : 'text-red-700'
                }`}
              >
                {feedback.points_earned} {feedback.points_earned === 1 ? 'point' : 'points'}{' '}
                earned
              </p>
            </div>
          </div>
          <Badge variant={isCorrect ? 'success' : isPartial ? 'warning' : 'danger'} size="lg">
            +{feedback.points_earned}
          </Badge>
        </div>
      </div>

      {/* Answers Comparison */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Your Answer */}
        <div
          className={`p-4 rounded-lg border ${
            isCorrect ? 'bg-green-50 border-green-200' : 'bg-gray-50 border-gray-200'
          }`}
        >
          <div className="text-sm font-medium text-gray-700 mb-2">Your Answer:</div>
          <div className="text-lg font-mono">{feedback.user_answer}</div>
        </div>

        {/* Correct Answer */}
        {!isCorrect && (
          <div className="p-4 rounded-lg border bg-green-50 border-green-200">
            <div className="text-sm font-medium text-gray-700 mb-2">Correct Answer:</div>
            <div className="text-lg font-mono text-green-800">{feedback.correct_answer}</div>
          </div>
        )}
      </div>

      {/* Feedback Text */}
      <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex items-start">
          <svg
            className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <div className="text-sm font-medium text-blue-800 mb-1">Explanation:</div>
            <p className="text-sm text-blue-900">{feedback.feedback_de}</p>
          </div>
        </div>
      </div>

      {/* Specific Errors */}
      {feedback.specific_errors && feedback.specific_errors.length > 0 && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="text-sm font-medium text-red-800 mb-2">Errors Found:</div>
          <ul className="list-disc list-inside space-y-1">
            {feedback.specific_errors.map((error, index) => (
              <li key={index} className="text-sm text-red-700">
                {error}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Suggestions */}
      {feedback.suggestions && feedback.suggestions.length > 0 && (
        <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
          <div className="text-sm font-medium text-purple-800 mb-2">Tips:</div>
          <ul className="list-disc list-inside space-y-1">
            {feedback.suggestions.map((suggestion, index) => (
              <li key={index} className="text-sm text-purple-700">
                {suggestion}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Self-Assessment (UX G5) */}
      <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg">
        <div className="text-sm font-medium text-gray-700 mb-3">
          How well do you understand this now?
        </div>
        <div className="flex gap-3 justify-center">
          <button
            className="flex-1 p-3 border-2 border-gray-300 rounded-lg hover:border-green-500 hover:bg-green-50 transition-colors"
            onClick={() => {
              /* TODO: Track understanding */
            }}
          >
            <div className="text-2xl mb-1">👍</div>
            <div className="text-xs text-gray-600">I understand</div>
          </button>
          <button
            className="flex-1 p-3 border-2 border-gray-300 rounded-lg hover:border-yellow-500 hover:bg-yellow-50 transition-colors"
            onClick={() => {
              /* TODO: Track understanding */
            }}
          >
            <div className="text-2xl mb-1">🤔</div>
            <div className="text-xs text-gray-600">Not sure</div>
          </button>
          <button
            className="flex-1 p-3 border-2 border-gray-300 rounded-lg hover:border-red-500 hover:bg-red-50 transition-colors"
            onClick={() => {
              /* TODO: Track understanding */
            }}
          >
            <div className="text-2xl mb-1">👎</div>
            <div className="text-xs text-gray-600">Still confused</div>
          </button>
        </div>
      </div>

      {/* Continue Button */}
      <div className="flex justify-center">
        <Button
          onClick={onNext}
          variant="primary"
          size="lg"
          className="min-w-[200px]"
          data-testid="continue-button"
        >
          Next Exercise →
        </Button>
      </div>
    </div>
  );
}
