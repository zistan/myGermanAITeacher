import { useState } from 'react';
import type { DifficultyLevel } from '../../api/types/common.types';
import type { VocabularyQuizRequest, QuizType } from '../../api/types/vocabulary.types';
import { Button, Card } from '../common';

export interface QuizSetupProps {
  categories: string[];
  onStart: (request: VocabularyQuizRequest) => void;
  isLoading?: boolean;
}

const difficultyOptions: Array<{ value: DifficultyLevel | ''; label: string }> = [
  { value: '', label: 'All Levels' },
  { value: 'A1', label: 'A1 - Beginner' },
  { value: 'A2', label: 'A2 - Elementary' },
  { value: 'B1', label: 'B1 - Intermediate' },
  { value: 'B2', label: 'B2 - Upper Intermediate' },
  { value: 'C1', label: 'C1 - Advanced' },
  { value: 'C2', label: 'C2 - Mastery' },
];

const quizTypeOptions: Array<{ value: QuizType; label: string; description: string; icon: string }> = [
  {
    value: 'multiple_choice',
    label: 'Multiple Choice',
    description: 'Select the correct answer',
    icon: '🔘',
  },
  {
    value: 'fill_blank',
    label: 'Fill in the Blank',
    description: 'Type the missing word',
    icon: '✍️',
  },
  {
    value: 'matching',
    label: 'Matching',
    description: 'Match words with translations',
    icon: '🔗',
  },
];

const questionCountOptions = [5, 10, 15, 20, 30];

export function QuizSetup({
  categories,
  onStart,
  isLoading = false,
}: QuizSetupProps) {
  const [category, setCategory] = useState<string>('');
  const [difficulty, setDifficulty] = useState<DifficultyLevel | ''>('');
  const [quizType, setQuizType] = useState<QuizType>('multiple_choice');
  const [questionCount, setQuestionCount] = useState<number>(10);

  const handleStart = () => {
    const request: VocabularyQuizRequest = {
      category: category || undefined,
      difficulty: difficulty || undefined,
      quiz_type: quizType,
      question_count: questionCount,
    };
    onStart(request);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Vocabulary Quiz</h2>
            <p className="text-gray-600">Test your vocabulary knowledge</p>
          </div>

          {/* Quiz Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Quiz Type
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {quizTypeOptions.map(({ value, label, description, icon }) => (
                <button
                  key={value}
                  onClick={() => setQuizType(value)}
                  className={`p-4 rounded-lg border-2 text-left transition-colors ${
                    quizType === value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  data-testid={`quiz-type-${value}`}
                >
                  <div className="text-2xl mb-2">{icon}</div>
                  <div className="font-medium text-gray-900">{label}</div>
                  <div className="text-xs text-gray-500 mt-1">{description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Category */}
          <div>
            <label htmlFor="quiz-category" className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              id="quiz-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              data-testid="quiz-category-select"
            >
              <option value="">All Categories</option>
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty */}
          <div>
            <label htmlFor="quiz-difficulty" className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              id="quiz-difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value as DifficultyLevel | '')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              data-testid="quiz-difficulty-select"
            >
              {difficultyOptions.map(({ value, label }) => (
                <option key={value || 'all'} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          {/* Question Count */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Questions
            </label>
            <div className="flex flex-wrap gap-2">
              {questionCountOptions.map((count) => (
                <button
                  key={count}
                  onClick={() => setQuestionCount(count)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    questionCount === count
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                  data-testid={`quiz-count-${count}`}
                >
                  {count}
                </button>
              ))}
            </div>
          </div>

          {/* Start Button */}
          <Button
            onClick={handleStart}
            variant="primary"
            fullWidth
            isLoading={isLoading}
            data-testid="quiz-start-btn"
          >
            Start Quiz ({questionCount} questions)
          </Button>
        </div>
      </Card>
    </div>
  );
}
