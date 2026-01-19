import { useState } from 'react';
import type { VocabularyQuizQuestion as QuizQuestionType } from '../../api/types/vocabulary.types';
import { Button, Card } from '../common';

export interface QuizQuestionProps {
  question: QuizQuestionType;
  questionNumber: number;
  totalQuestions: number;
  onSubmit: (answer: string) => void;
  isSubmitting?: boolean;
}

export function QuizQuestion({
  question,
  questionNumber,
  totalQuestions,
  onSubmit,
  isSubmitting = false,
}: QuizQuestionProps) {
  const [selectedAnswer, setSelectedAnswer] = useState<string>('');
  const [textAnswer, setTextAnswer] = useState('');

  const handleSubmit = () => {
    const answer = question.question_type === 'multiple_choice' ? selectedAnswer : textAnswer;
    if (answer.trim()) {
      onSubmit(answer);
    }
  };

  // Render based on question type
  const renderQuestionInput = () => {
    switch (question.question_type) {
      case 'multiple_choice':
        return (
          <div className="space-y-3">
            {question.options?.map((option, index) => (
              <button
                key={index}
                onClick={() => setSelectedAnswer(option)}
                className={`w-full p-4 text-left rounded-lg border-2 transition-all ${
                  selectedAnswer === option
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300 bg-white'
                }`}
                data-testid={`option-${index}`}
              >
                <span className="flex items-center gap-3">
                  <span
                    className={`w-6 h-6 rounded-full border-2 flex items-center justify-center ${
                      selectedAnswer === option
                        ? 'border-primary-500 bg-primary-500'
                        : 'border-gray-300'
                    }`}
                  >
                    {selectedAnswer === option && (
                      <span className="w-3 h-3 bg-white rounded-full" />
                    )}
                  </span>
                  <span className="text-gray-900">{option}</span>
                </span>
              </button>
            ))}
          </div>
        );

      case 'fill_blank':
        return (
          <div>
            <input
              type="text"
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Type your answer..."
              className="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              autoFocus
              data-testid="fill-blank-input"
            />
          </div>
        );

      case 'matching':
        // For matching, we'll use a simple text input
        // A full matching UI would require more complex state management
        return (
          <div>
            <p className="text-sm text-gray-600 mb-3">
              Enter the matching translation for: <strong>{question.word_tested}</strong>
            </p>
            <input
              type="text"
              value={textAnswer}
              onChange={(e) => setTextAnswer(e.target.value)}
              placeholder="Type the translation..."
              className="w-full px-4 py-3 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
              autoFocus
              data-testid="matching-input"
            />
          </div>
        );

      default:
        return null;
    }
  };

  const canSubmit =
    question.question_type === 'multiple_choice'
      ? selectedAnswer.length > 0
      : textAnswer.trim().length > 0;

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
          <span>Question {questionNumber} of {totalQuestions}</span>
          <span>{Math.round((questionNumber / totalQuestions) * 100)}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div
            className="bg-primary-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${(questionNumber / totalQuestions) * 100}%` }}
          />
        </div>
      </div>

      <Card>
        {/* Question Type Badge */}
        <div className="flex items-center justify-between mb-4">
          <span className="text-sm font-medium text-primary-700 bg-primary-100 px-3 py-1 rounded-full">
            {question.question_type.replace('_', ' ')}
          </span>
          <span className="text-sm text-gray-500">Word: {question.word_tested}</span>
        </div>

        {/* Question */}
        <h2 className="text-xl font-semibold text-gray-900 mb-6">{question.question}</h2>

        {/* Input */}
        <div className="mb-6">{renderQuestionInput()}</div>

        {/* Submit */}
        <Button
          onClick={handleSubmit}
          variant="primary"
          fullWidth
          disabled={!canSubmit}
          isLoading={isSubmitting}
          data-testid="submit-answer-btn"
        >
          Submit Answer
        </Button>
      </Card>

      {/* Keyboard hint */}
      <p className="text-center text-sm text-gray-400 mt-4">
        Press <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs">Enter</kbd> to submit
      </p>
    </div>
  );
}
