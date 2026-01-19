import clsx from 'clsx';
import type { FlashcardResponse } from '../../api/types/vocabulary.types';
import { DifficultyBadge } from './DifficultyBadge';

export interface FlashcardDisplayProps {
  card: FlashcardResponse;
  isFlipped: boolean;
  onFlip: () => void;
  showHint?: boolean;
}

const cardTypeLabels: Record<string, string> = {
  definition: 'Definition',
  translation: 'Translation',
  usage: 'Usage',
  synonym: 'Synonym',
  example: 'Example',
};

const cardTypeInstructions: Record<string, { front: string; back: string }> = {
  definition: {
    front: 'What is the definition?',
    back: 'Definition',
  },
  translation: {
    front: 'How do you translate this?',
    back: 'Translation',
  },
  usage: {
    front: 'How is this word used?',
    back: 'Usage',
  },
  synonym: {
    front: 'What are the synonyms?',
    back: 'Synonyms',
  },
  example: {
    front: 'Complete the example',
    back: 'Example',
  },
};

export function FlashcardDisplay({ card, isFlipped, onFlip, showHint = true }: FlashcardDisplayProps) {

  const instructions = cardTypeInstructions[card.card_type] || {
    front: 'Think about this word',
    back: 'Answer',
  };

  return (
    <div className="perspective-1000" style={{ perspective: '1000px' }}>
      {/* Card container */}
      <div
        onClick={onFlip}
        className={clsx(
          'relative w-full min-h-[320px] md:min-h-[400px] cursor-pointer transition-transform duration-500 transform-style-preserve-3d',
          isFlipped && 'rotate-y-180'
        )}
        style={{
          transformStyle: 'preserve-3d',
          transform: isFlipped ? 'rotateY(180deg)' : 'rotateY(0deg)',
        }}
        data-testid="flashcard"
      >
        {/* Front of card */}
        <div
          className={clsx(
            'absolute inset-0 w-full h-full backface-hidden',
            'bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl shadow-lg p-6 md:p-8',
            'flex flex-col'
          )}
          style={{ backfaceVisibility: 'hidden' }}
        >
          {/* Card type badge */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-primary-700 bg-primary-200 px-3 py-1 rounded-full">
              {cardTypeLabels[card.card_type] || card.card_type}
            </span>
            <DifficultyBadge level={card.difficulty} size="sm" />
          </div>

          {/* Instruction */}
          <p className="text-sm text-primary-600 mb-4">{instructions.front}</p>

          {/* Main word */}
          <div className="flex-1 flex flex-col items-center justify-center text-center">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">{card.word}</h2>
            <p className="text-xl text-gray-700">{card.front}</p>
          </div>

          {/* Hint */}
          {showHint && card.hint && (
            <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
              <p className="text-sm text-yellow-800">
                <span className="font-medium">Hint:</span> {card.hint}
              </p>
            </div>
          )}

          {/* Flip instruction */}
          <p className="text-center text-sm text-gray-400 mt-4">
            Click to reveal answer
          </p>
        </div>

        {/* Back of card */}
        <div
          className={clsx(
            'absolute inset-0 w-full h-full backface-hidden',
            'bg-gradient-to-br from-green-50 to-green-100 rounded-2xl shadow-lg p-6 md:p-8',
            'flex flex-col'
          )}
          style={{
            backfaceVisibility: 'hidden',
            transform: 'rotateY(180deg)',
          }}
        >
          {/* Card type badge */}
          <div className="flex items-center justify-between mb-4">
            <span className="text-sm font-medium text-green-700 bg-green-200 px-3 py-1 rounded-full">
              {instructions.back}
            </span>
            <DifficultyBadge level={card.difficulty} size="sm" />
          </div>

          {/* Word reminder */}
          <p className="text-lg text-gray-600 mb-2">{card.word}</p>

          {/* Answer */}
          <div className="flex-1 flex flex-col items-center justify-center text-center">
            <div className="text-2xl md:text-3xl font-semibold text-gray-900 leading-relaxed">
              {card.back}
            </div>
          </div>

          {/* Rate instruction */}
          <p className="text-center text-sm text-gray-400 mt-4">
            How well did you know this?
          </p>
        </div>
      </div>
    </div>
  );
}
