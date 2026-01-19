import { Modal } from '../common';
import { Button } from '../common';
import type { VocabularyWithProgress } from '../../api/types/vocabulary.types';
import { MasteryIndicator } from './MasteryIndicator';
import { DifficultyBadge } from './DifficultyBadge';
import { CategoryBadge } from './CategoryBadge';

export interface WordDetailModalProps {
  word: VocabularyWithProgress | null;
  isOpen: boolean;
  onClose: () => void;
  onPractice?: (word: VocabularyWithProgress) => void;
  onAddToList?: (word: VocabularyWithProgress) => void;
}

export function WordDetailModal({
  word,
  isOpen,
  onClose,
  onPractice,
  onAddToList,
}: WordDetailModalProps) {
  if (!word) return null;

  // Render gender indicator for nouns
  const renderGender = () => {
    if (!word.gender) return null;
    const genderMap: Record<string, { label: string; color: string }> = {
      masculine: { label: 'der', color: 'text-blue-600' },
      feminine: { label: 'die', color: 'text-pink-600' },
      neuter: { label: 'das', color: 'text-green-600' },
    };
    const config = genderMap[word.gender];
    return config ? (
      <span className={`font-medium ${config.color}`}>{config.label}</span>
    ) : null;
  };

  const footer = (
    <div className="flex gap-3">
      {onPractice && (
        <Button
          onClick={() => {
            onPractice(word);
            onClose();
          }}
          variant="primary"
          data-testid="modal-practice-btn"
        >
          Practice This Word
        </Button>
      )}
      {onAddToList && (
        <Button
          onClick={() => {
            onAddToList(word);
          }}
          variant="secondary"
          data-testid="modal-add-to-list-btn"
        >
          Add to List
        </Button>
      )}
      <Button onClick={onClose} variant="ghost">
        Close
      </Button>
    </div>
  );

  return (
    <Modal isOpen={isOpen} onClose={onClose} title="Word Details" size="lg" footer={footer}>
      <div className="space-y-6">
        {/* Header */}
        <div className="border-b border-gray-200 pb-4">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2 mb-1">
                {renderGender()}
                <h2 className="text-2xl font-bold text-gray-900">{word.word}</h2>
                {word.pronunciation && (
                  <span className="text-gray-400 text-lg">[{word.pronunciation}]</span>
                )}
              </div>
              <p className="text-xl text-gray-600">{word.translation_it}</p>
              {word.plural_form && (
                <p className="text-sm text-gray-500 mt-1">Plural: {word.plural_form}</p>
              )}
            </div>
            <DifficultyBadge level={word.difficulty} size="lg" />
          </div>

          {/* Tags */}
          <div className="flex flex-wrap gap-2 mt-4">
            <CategoryBadge category={word.category} data-testid="modal-category-badge" />
            <span className="text-sm text-gray-500 bg-gray-100 px-2 py-1 rounded">
              {word.part_of_speech}
            </span>
            {word.is_idiom && (
              <span className="text-sm text-purple-600 bg-purple-50 px-2 py-1 rounded">
                Idiom
              </span>
            )}
            {word.is_compound && (
              <span className="text-sm text-blue-600 bg-blue-50 px-2 py-1 rounded">
                Compound Word
              </span>
            )}
            {word.is_separable_verb && (
              <span className="text-sm text-orange-600 bg-orange-50 px-2 py-1 rounded">
                Separable Verb
              </span>
            )}
          </div>
        </div>

        {/* Progress Section */}
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-3">Learning Progress</h3>
          <div className="flex items-center justify-between">
            <MasteryIndicator level={word.mastery_level} size="lg" />
            <div className="flex items-center gap-6 text-sm text-gray-600">
              <div>
                <span className="font-medium">{word.times_reviewed ?? 0}</span> reviews
              </div>
              {typeof word.accuracy_rate === 'number' && (
                <div>
                  <span className="font-medium">{word.accuracy_rate.toFixed(0)}%</span> accuracy
                </div>
              )}
              {word.last_reviewed && (
                <div>
                  Last: <span className="font-medium">{new Date(word.last_reviewed).toLocaleDateString()}</span>
                </div>
              )}
            </div>
          </div>
          {word.next_review_due && (
            <p className="text-sm text-gray-500 mt-2">
              Next review: {new Date(word.next_review_due).toLocaleDateString()}
            </p>
          )}
        </div>

        {/* Definition */}
        {word.definition_de && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Definition (German)</h3>
            <p className="text-gray-800">{word.definition_de}</p>
          </div>
        )}

        {/* Example */}
        <div>
          <h3 className="text-sm font-semibold text-gray-700 mb-2">Example</h3>
          <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-400">
            <p className="text-gray-800 italic mb-2">"{word.example_de}"</p>
            <p className="text-gray-600 text-sm">{word.example_it}</p>
          </div>
        </div>

        {/* Synonyms & Antonyms */}
        {(word.synonyms.length > 0 || word.antonyms.length > 0) && (
          <div className="grid grid-cols-2 gap-6">
            {word.synonyms.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Synonyms</h3>
                <div className="flex flex-wrap gap-2">
                  {word.synonyms.map((syn, i) => (
                    <span
                      key={i}
                      className="text-sm text-green-700 bg-green-50 px-2 py-1 rounded-full"
                    >
                      {syn}
                    </span>
                  ))}
                </div>
              </div>
            )}
            {word.antonyms.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-gray-700 mb-2">Antonyms</h3>
                <div className="flex flex-wrap gap-2">
                  {word.antonyms.map((ant, i) => (
                    <span
                      key={i}
                      className="text-sm text-red-700 bg-red-50 px-2 py-1 rounded-full"
                    >
                      {ant}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Usage Notes */}
        {word.usage_notes && (
          <div>
            <h3 className="text-sm font-semibold text-gray-700 mb-2">Usage Notes</h3>
            <p className="text-gray-600 text-sm bg-yellow-50 p-3 rounded-lg border-l-4 border-yellow-400">
              {word.usage_notes}
            </p>
          </div>
        )}

        {/* Metadata */}
        <div className="text-xs text-gray-400 pt-4 border-t border-gray-100">
          Added: {new Date(word.created_at).toLocaleDateString()}
        </div>
      </div>
    </Modal>
  );
}
