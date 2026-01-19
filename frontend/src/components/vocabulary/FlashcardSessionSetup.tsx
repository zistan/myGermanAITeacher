import { useState } from 'react';
import type { DifficultyLevel } from '../../api/types/common.types';
import type { StartFlashcardSessionRequest, FlashcardType } from '../../api/types/vocabulary.types';
import { Button, Card } from '../common';

export interface FlashcardSessionSetupProps {
  categories: string[];
  onStart: (request: StartFlashcardSessionRequest) => void;
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

const cardTypeOptions: Array<{ value: FlashcardType; label: string; description: string }> = [
  { value: 'definition', label: 'Definition', description: 'German definitions' },
  { value: 'translation', label: 'Translation', description: 'German ↔ Italian' },
  { value: 'usage', label: 'Usage', description: 'How to use the word' },
  { value: 'synonym', label: 'Synonym', description: 'Similar words' },
  { value: 'example', label: 'Example', description: 'Example sentences' },
];

const cardCountOptions = [5, 10, 15, 20, 30, 50];

export function FlashcardSessionSetup({
  categories,
  onStart,
  isLoading = false,
}: FlashcardSessionSetupProps) {
  const [category, setCategory] = useState<string>('');
  const [difficulty, setDifficulty] = useState<DifficultyLevel | ''>('');
  const [cardCount, setCardCount] = useState<number>(10);
  const [selectedCardTypes, setSelectedCardTypes] = useState<FlashcardType[]>([
    'definition',
    'translation',
  ]);
  const [useSpacedRepetition, setUseSpacedRepetition] = useState(true);

  const handleCardTypeToggle = (type: FlashcardType) => {
    setSelectedCardTypes((prev) =>
      prev.includes(type) ? prev.filter((t) => t !== type) : [...prev, type]
    );
  };

  const handleStart = () => {
    const request: StartFlashcardSessionRequest = {
      category: category || undefined,
      difficulty: difficulty || undefined,
      card_count: cardCount,
      card_types: selectedCardTypes.length > 0 ? selectedCardTypes : undefined,
      use_spaced_repetition: useSpacedRepetition,
    };
    onStart(request);
  };

  return (
    <div className="max-w-2xl mx-auto">
      <Card>
        <div className="space-y-6">
          {/* Header */}
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Flashcard Session</h2>
            <p className="text-gray-600">Configure your practice session</p>
          </div>

          {/* Category */}
          <div>
            <label htmlFor="fc-category" className="block text-sm font-medium text-gray-700 mb-2">
              Category
            </label>
            <select
              id="fc-category"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              data-testid="fc-category-select"
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
            <label htmlFor="fc-difficulty" className="block text-sm font-medium text-gray-700 mb-2">
              Difficulty Level
            </label>
            <select
              id="fc-difficulty"
              value={difficulty}
              onChange={(e) => setDifficulty(e.target.value as DifficultyLevel | '')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              data-testid="fc-difficulty-select"
            >
              {difficultyOptions.map(({ value, label }) => (
                <option key={value || 'all'} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </div>

          {/* Card Count */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Cards
            </label>
            <div className="flex flex-wrap gap-2">
              {cardCountOptions.map((count) => (
                <button
                  key={count}
                  onClick={() => setCardCount(count)}
                  className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                    cardCount === count
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                  data-testid={`fc-count-${count}`}
                >
                  {count}
                </button>
              ))}
            </div>
          </div>

          {/* Card Types */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Card Types
            </label>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
              {cardTypeOptions.map(({ value, label, description }) => (
                <button
                  key={value}
                  onClick={() => handleCardTypeToggle(value)}
                  className={`p-3 rounded-lg border-2 text-left transition-colors ${
                    selectedCardTypes.includes(value)
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                  data-testid={`fc-type-${value}`}
                >
                  <div className="font-medium text-sm">{label}</div>
                  <div className="text-xs text-gray-500">{description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Spaced Repetition Toggle */}
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <div className="font-medium text-gray-900">Spaced Repetition</div>
              <div className="text-sm text-gray-500">Prioritize words due for review</div>
            </div>
            <button
              onClick={() => setUseSpacedRepetition(!useSpacedRepetition)}
              className={`relative w-14 h-7 rounded-full transition-colors ${
                useSpacedRepetition ? 'bg-primary-600' : 'bg-gray-300'
              }`}
              data-testid="fc-spaced-repetition-toggle"
            >
              <span
                className={`absolute top-0.5 left-0.5 w-6 h-6 bg-white rounded-full transition-transform ${
                  useSpacedRepetition ? 'translate-x-7' : 'translate-x-0'
                }`}
              />
            </button>
          </div>

          {/* Start Button */}
          <Button
            onClick={handleStart}
            variant="primary"
            fullWidth
            isLoading={isLoading}
            disabled={selectedCardTypes.length === 0}
            data-testid="fc-start-btn"
          >
            Start Session ({cardCount} cards)
          </Button>

          {selectedCardTypes.length === 0 && (
            <p className="text-sm text-red-600 text-center">
              Please select at least one card type
            </p>
          )}
        </div>
      </Card>
    </div>
  );
}
