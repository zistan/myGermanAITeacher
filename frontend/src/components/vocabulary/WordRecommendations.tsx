import { useState } from 'react';
import type { WordRecommendationResponse, VocabularyWithProgress } from '../../api/types/vocabulary.types';
import { Card, Button, Loading } from '../common';
import { WordCard } from './WordCard';

export interface WordRecommendationsProps {
  recommendations: WordRecommendationResponse | null;
  isLoading?: boolean;
  onRefresh?: () => void;
  onPracticeWord?: (word: VocabularyWithProgress) => void;
  onAddToList?: (word: VocabularyWithProgress) => void;
}

export function WordRecommendations({
  recommendations,
  isLoading = false,
  onRefresh,
  onPracticeWord,
  onAddToList,
}: WordRecommendationsProps) {
  const [showAll, setShowAll] = useState(false);

  if (isLoading) {
    return (
      <Card>
        <div className="flex justify-center py-8">
          <Loading />
        </div>
      </Card>
    );
  }

  if (!recommendations || recommendations.recommended_words.length === 0) {
    return (
      <Card>
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Recommended Words</h3>
          {onRefresh && (
            <Button onClick={onRefresh} variant="ghost" size="sm">
              Refresh
            </Button>
          )}
        </div>
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-2">💡</div>
          <p>No recommendations available</p>
          <p className="text-sm mt-1">Keep learning to get personalized suggestions</p>
        </div>
      </Card>
    );
  }

  const displayedWords = showAll
    ? recommendations.recommended_words
    : recommendations.recommended_words.slice(0, 5);

  return (
    <Card>
      <div className="flex items-center justify-between mb-2">
        <h3 className="text-lg font-semibold text-gray-900">Recommended Words</h3>
        {onRefresh && (
          <Button onClick={onRefresh} variant="ghost" size="sm" data-testid="refresh-recommendations-btn">
            Refresh
          </Button>
        )}
      </div>

      {/* Reason */}
      <p className="text-sm text-gray-600 mb-4">{recommendations.reason}</p>

      {/* Words list */}
      <div className="space-y-3">
        {displayedWords.map((word) => (
          <div key={word.id} className="relative group">
            <WordCard
              word={word}
              variant="compact"
              onClick={() => onPracticeWord?.(word)}
              testId={`recommended-word-${word.id}`}
            />
            {onAddToList && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onAddToList(word);
                }}
                className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-2 text-primary-600 hover:bg-primary-50 rounded-md"
                title="Add to list"
                data-testid={`add-recommended-${word.id}-btn`}
              >
                +
              </button>
            )}
          </div>
        ))}
      </div>

      {/* Show more button */}
      {recommendations.recommended_words.length > 5 && (
        <button
          onClick={() => setShowAll(!showAll)}
          className="w-full mt-4 py-2 text-sm text-primary-600 hover:text-primary-700 font-medium"
          data-testid="show-more-recommendations-btn"
        >
          {showAll
            ? 'Show less'
            : `Show ${recommendations.recommended_words.length - 5} more`}
        </button>
      )}
    </Card>
  );
}
