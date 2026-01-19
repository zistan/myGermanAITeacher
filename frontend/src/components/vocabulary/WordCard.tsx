import { type HTMLAttributes } from 'react';
import clsx from 'clsx';
import type { VocabularyWithProgress } from '../../api/types/vocabulary.types';
import { MasteryIndicator } from './MasteryIndicator';
import { DifficultyBadge } from './DifficultyBadge';
import { CategoryBadge } from './CategoryBadge';

export interface WordCardProps extends HTMLAttributes<HTMLDivElement> {
  word: VocabularyWithProgress;
  variant?: 'compact' | 'default' | 'expanded';
  showProgress?: boolean;
  showExamples?: boolean;
  onPractice?: (word: VocabularyWithProgress) => void;
  onAddToList?: (word: VocabularyWithProgress) => void;
  testId?: string;
}

export function WordCard({
  word,
  variant = 'default',
  showProgress = true,
  showExamples = false,
  onPractice,
  onAddToList,
  className,
  testId,
  onClick,
  ...props
}: WordCardProps) {
  const isClickable = !!onClick;

  // Render gender indicator for nouns
  const renderGender = () => {
    if (!word.gender) return null;
    const genderMap: Record<string, { label: string; color: string }> = {
      masculine: { label: 'der', color: 'text-blue-600' },
      feminine: { label: 'die', color: 'text-pink-600' },
      neuter: { label: 'das', color: 'text-green-600' },
    };
    const config = genderMap[word.gender];
    return config ? <span className={clsx('font-medium', config.color)}>{config.label}</span> : null;
  };

  // Compact variant - minimal info, good for lists
  if (variant === 'compact') {
    return (
      <div
        className={clsx(
          'flex items-center justify-between p-3 bg-white rounded-lg border border-gray-200',
          isClickable && 'cursor-pointer hover:border-primary-300 hover:shadow-sm transition-all',
          className
        )}
        data-testid={testId}
        onClick={onClick}
        {...props}
      >
        <div className="flex items-center gap-3 min-w-0">
          <div className="min-w-0">
            <div className="flex items-center gap-1.5">
              {renderGender()}
              <span className="font-medium text-gray-900 truncate">{word.word}</span>
            </div>
            <p className="text-sm text-gray-500 truncate">{word.translation_it}</p>
          </div>
        </div>
        <div className="flex items-center gap-2 flex-shrink-0">
          <DifficultyBadge level={word.difficulty} size="sm" />
          {showProgress && <MasteryIndicator level={word.mastery_level} size="sm" showLabel={false} />}
        </div>
      </div>
    );
  }

  // Expanded variant - full details
  if (variant === 'expanded') {
    return (
      <div
        className={clsx(
          'bg-white rounded-lg border border-gray-200 shadow-sm overflow-hidden',
          isClickable && 'cursor-pointer hover:border-primary-300 hover:shadow-md transition-all',
          className
        )}
        data-testid={testId}
        onClick={onClick}
        {...props}
      >
        {/* Header */}
        <div className="p-4 border-b border-gray-100">
          <div className="flex items-start justify-between mb-2">
            <div>
              <div className="flex items-center gap-2">
                {renderGender()}
                <h3 className="text-xl font-semibold text-gray-900">{word.word}</h3>
                {word.pronunciation && (
                  <span className="text-gray-400 text-sm">[{word.pronunciation}]</span>
                )}
              </div>
              <p className="text-gray-600 mt-1">{word.translation_it}</p>
            </div>
            <DifficultyBadge level={word.difficulty} />
          </div>

          <div className="flex flex-wrap gap-2 mt-3">
            <CategoryBadge category={word.category} size="sm" />
            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
              {word.part_of_speech}
            </span>
            {word.is_idiom && (
              <span className="text-sm text-purple-600 bg-purple-50 px-2 py-0.5 rounded">Idiom</span>
            )}
            {word.is_compound && (
              <span className="text-sm text-blue-600 bg-blue-50 px-2 py-0.5 rounded">Compound</span>
            )}
            {word.is_separable_verb && (
              <span className="text-sm text-orange-600 bg-orange-50 px-2 py-0.5 rounded">
                Separable
              </span>
            )}
          </div>
        </div>

        {/* Progress */}
        {showProgress && (
          <div className="px-4 py-3 bg-gray-50 border-b border-gray-100">
            <div className="flex items-center justify-between">
              <MasteryIndicator level={word.mastery_level} />
              <div className="flex items-center gap-4 text-sm text-gray-500">
                <span>{word.times_reviewed ?? 0} reviews</span>
                {typeof word.accuracy_rate === 'number' && <span>{word.accuracy_rate.toFixed(0)}% accuracy</span>}
              </div>
            </div>
          </div>
        )}

        {/* Content */}
        <div className="p-4 space-y-4">
          {/* Definition */}
          {word.definition_de && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-1">Definition (DE)</h4>
              <p className="text-gray-600">{word.definition_de}</p>
            </div>
          )}

          {/* Examples */}
          {showExamples && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-1">Example</h4>
              <div className="bg-gray-50 rounded-md p-3">
                <p className="text-gray-800 italic">{word.example_de}</p>
                <p className="text-gray-500 text-sm mt-1">{word.example_it}</p>
              </div>
            </div>
          )}

          {/* Synonyms/Antonyms */}
          {(word.synonyms.length > 0 || word.antonyms.length > 0) && (
            <div className="flex gap-6">
              {word.synonyms.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Synonyms</h4>
                  <div className="flex flex-wrap gap-1">
                    {word.synonyms.map((syn, i) => (
                      <span key={i} className="text-sm text-green-700 bg-green-50 px-2 py-0.5 rounded">
                        {syn}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              {word.antonyms.length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Antonyms</h4>
                  <div className="flex flex-wrap gap-1">
                    {word.antonyms.map((ant, i) => (
                      <span key={i} className="text-sm text-red-700 bg-red-50 px-2 py-0.5 rounded">
                        {ant}
                      </span>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}

          {/* Usage notes */}
          {word.usage_notes && (
            <div>
              <h4 className="text-sm font-medium text-gray-700 mb-1">Usage Notes</h4>
              <p className="text-sm text-gray-600">{word.usage_notes}</p>
            </div>
          )}
        </div>

        {/* Actions */}
        {(onPractice || onAddToList) && (
          <div className="px-4 py-3 bg-gray-50 border-t border-gray-100 flex gap-2">
            {onPractice && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onPractice(word);
                }}
                className="flex-1 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 transition-colors"
                data-testid="word-card-practice-btn"
              >
                Practice
              </button>
            )}
            {onAddToList && (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  onAddToList(word);
                }}
                className="flex-1 px-3 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 transition-colors"
                data-testid="word-card-add-to-list-btn"
              >
                Add to List
              </button>
            )}
          </div>
        )}
      </div>
    );
  }

  // Default variant - balanced info
  return (
    <div
      className={clsx(
        'bg-white rounded-lg border border-gray-200 shadow-sm p-4',
        isClickable && 'cursor-pointer hover:border-primary-300 hover:shadow-md transition-all',
        className
      )}
      data-testid={testId}
      onClick={onClick}
      {...props}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="flex items-center gap-2">
            {renderGender()}
            <h3 className="text-lg font-semibold text-gray-900">{word.word}</h3>
            {word.plural_form && (
              <span className="text-sm text-gray-400">({word.plural_form})</span>
            )}
          </div>
          <p className="text-gray-600">{word.translation_it}</p>
        </div>
        <DifficultyBadge level={word.difficulty} size="sm" />
      </div>

      {/* Tags */}
      <div className="flex flex-wrap gap-2 mb-3">
        <CategoryBadge category={word.category} size="sm" testId="category-badge" />
        <span className="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded">
          {word.part_of_speech}
        </span>
      </div>

      {/* Example */}
      {showExamples && word.example_de && (
        <div className="mb-3 text-sm">
          <p className="text-gray-700 italic">"{word.example_de}"</p>
        </div>
      )}

      {/* Progress */}
      {showProgress && (
        <div className="pt-3 border-t border-gray-100">
          <MasteryIndicator level={word.mastery_level} size="sm" />
        </div>
      )}
    </div>
  );
}
