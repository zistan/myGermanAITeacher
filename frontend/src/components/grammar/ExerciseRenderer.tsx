import type { GrammarExercise } from '../../api/types/grammar.types';
import { Button } from '../common';

interface ExerciseRendererProps {
  exercise: GrammarExercise;
  userAnswer: string;
  onAnswerChange: (answer: string) => void;
  onSubmit: () => void;
  isSubmitting: boolean;
}

export function ExerciseRenderer({
  exercise,
  userAnswer,
  onAnswerChange,
  onSubmit,
  isSubmitting,
}: ExerciseRendererProps) {
  const renderExerciseContent = () => {
    switch (exercise.exercise_type) {
      case 'fill_blank':
        return (
          <div>
            <p className="text-lg text-gray-900 mb-6 whitespace-pre-wrap">
              {exercise.question_text}
            </p>
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Type your answer..."
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-lg"
              autoFocus
              disabled={isSubmitting}
            />
          </div>
        );

      case 'multiple_choice':
        return (
          <div>
            <p className="text-lg text-gray-900 mb-6 whitespace-pre-wrap">
              {exercise.question_text}
            </p>
            <div className="space-y-3">
              {exercise.alternative_answers.map((option, index) => (
                <label
                  key={index}
                  className={`flex items-center p-4 border-2 rounded-lg cursor-pointer transition-colors ${
                    userAnswer === option
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-300 hover:border-gray-400'
                  }`}
                >
                  <input
                    type="radio"
                    name="answer"
                    value={option}
                    checked={userAnswer === option}
                    onChange={(e) => onAnswerChange(e.target.value)}
                    className="w-5 h-5 text-primary-600"
                    disabled={isSubmitting}
                  />
                  <span className="ml-3 text-lg text-gray-900">{option}</span>
                </label>
              ))}
            </div>
          </div>
        );

      case 'translation':
        return (
          <div>
            <div className="mb-2">
              <span className="text-sm font-medium text-gray-700">Translate to German:</span>
            </div>
            <p className="text-lg text-gray-900 mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
              {exercise.question_text}
            </p>
            <textarea
              value={userAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Type your German translation..."
              rows={4}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-lg resize-none"
              autoFocus
              disabled={isSubmitting}
            />
          </div>
        );

      case 'error_correction':
        return (
          <div>
            <div className="mb-2">
              <span className="text-sm font-medium text-gray-700">
                Find and correct the error:
              </span>
            </div>
            <p className="text-lg text-gray-900 mb-6 p-4 bg-red-50 rounded-lg border border-red-200">
              {exercise.question_text}
            </p>
            <textarea
              value={userAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Type the corrected sentence..."
              rows={3}
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-lg resize-none"
              autoFocus
              disabled={isSubmitting}
            />
          </div>
        );

      case 'sentence_building':
        return (
          <div>
            <div className="mb-2">
              <span className="text-sm font-medium text-gray-700">
                Build a sentence with the given words:
              </span>
            </div>
            <p className="text-lg text-gray-900 mb-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
              {exercise.question_text}
            </p>
            <input
              type="text"
              value={userAnswer}
              onChange={(e) => onAnswerChange(e.target.value)}
              placeholder="Type your sentence..."
              className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-primary-500 text-lg"
              autoFocus
              disabled={isSubmitting}
            />
          </div>
        );

      default:
        return <p className="text-gray-600">Unknown exercise type</p>;
    }
  };

  return (
    <div>
      {renderExerciseContent()}

      {/* Hints */}
      {exercise.hints && exercise.hints.length > 0 && (
        <div className="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
          <div className="flex items-start">
            <svg
              className="w-5 h-5 text-yellow-600 mt-0.5 mr-2 flex-shrink-0"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"
              />
            </svg>
            <div>
              <div className="text-sm font-medium text-yellow-800 mb-1">Hint:</div>
              <div className="text-sm text-yellow-700">{exercise.hints[0]}</div>
            </div>
          </div>
        </div>
      )}

      {/* Submit Button */}
      <div className="mt-6 flex justify-end">
        <Button
          onClick={onSubmit}
          variant="primary"
          size="lg"
          disabled={!userAnswer.trim() || isSubmitting}
          isLoading={isSubmitting}
        >
          Check Answer
        </Button>
      </div>
    </div>
  );
}
