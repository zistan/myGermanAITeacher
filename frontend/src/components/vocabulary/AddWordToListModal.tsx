import { useState, useEffect } from 'react';
import { Modal, Button, Loading } from '../common';
import type { PersonalVocabularyList, VocabularyWithProgress } from '../../api/types/vocabulary.types';
import vocabularyService from '../../api/services/vocabularyService';

export interface AddWordToListModalProps {
  isOpen: boolean;
  onClose: () => void;
  list: PersonalVocabularyList | null;
  onAddWord: (listId: number, wordId: number, notes?: string) => Promise<void>;
  existingWordIds?: number[];
}

export function AddWordToListModal({
  isOpen,
  onClose,
  list,
  onAddWord,
  existingWordIds = [],
}: AddWordToListModalProps) {
  const [words, setWords] = useState<VocabularyWithProgress[]>([]);
  const [filteredWords, setFilteredWords] = useState<VocabularyWithProgress[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedWordId, setSelectedWordId] = useState<number | null>(null);
  const [notes, setNotes] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  useEffect(() => {
    if (isOpen) {
      loadWords();
    }
  }, [isOpen]);

  useEffect(() => {
    filterWords();
  }, [words, searchQuery, existingWordIds]);

  const loadWords = async () => {
    setIsLoading(true);
    try {
      const data = await vocabularyService.getWords({ limit: 500 });
      setWords(data);
    } catch (error) {
      console.error('Failed to load words:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const filterWords = () => {
    let filtered = words.filter((w) => !existingWordIds.includes(w.id));

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (w) =>
          w.word.toLowerCase().includes(query) ||
          w.translation_it.toLowerCase().includes(query)
      );
    }

    setFilteredWords(filtered);
  };

  const handleAdd = async () => {
    if (!list || !selectedWordId) return;

    setIsAdding(true);
    try {
      await onAddWord(list.id, selectedWordId, notes || undefined);
      handleClose();
    } catch (error) {
      console.error('Failed to add word:', error);
    } finally {
      setIsAdding(false);
    }
  };

  const handleClose = () => {
    setSearchQuery('');
    setSelectedWordId(null);
    setNotes('');
    onClose();
  };

  const footer = (
    <div className="flex gap-3">
      <Button
        onClick={handleAdd}
        variant="primary"
        isLoading={isAdding}
        disabled={!selectedWordId}
        data-testid="add-word-submit-btn"
      >
        Add to List
      </Button>
      <Button onClick={handleClose} variant="ghost">
        Cancel
      </Button>
    </div>
  );

  return (
    <Modal
      isOpen={isOpen}
      onClose={handleClose}
      title={`Add Word to ${list?.name || 'List'}`}
      size="lg"
      footer={footer}
    >
      <div className="space-y-4">
        {/* Search */}
        <div>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search words..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            data-testid="add-word-search"
          />
        </div>

        {/* Words list */}
        <div className="max-h-64 overflow-y-auto border border-gray-200 rounded-lg">
          {isLoading ? (
            <div className="flex justify-center py-8">
              <Loading />
            </div>
          ) : filteredWords.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              {words.length === 0
                ? 'No vocabulary words available'
                : searchQuery
                ? 'No words match your search'
                : 'All words are already in this list'}
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {filteredWords.map((word) => (
                <div
                  key={word.id}
                  onClick={() => setSelectedWordId(word.id)}
                  className={`p-3 cursor-pointer transition-colors ${
                    selectedWordId === word.id
                      ? 'bg-primary-50 border-l-4 border-primary-500'
                      : 'hover:bg-gray-50'
                  }`}
                  data-testid={`word-option-${word.id}`}
                >
                  <div className="flex items-center justify-between">
                    <div>
                      <span className="font-medium text-gray-900">{word.word}</span>
                      <span className="text-gray-500 ml-2">- {word.translation_it}</span>
                    </div>
                    <span className="text-xs text-gray-400">{word.category}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Notes */}
        {selectedWordId && (
          <div>
            <label htmlFor="word-notes" className="block text-sm font-medium text-gray-700 mb-1">
              Personal Notes (optional)
            </label>
            <textarea
              id="word-notes"
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              placeholder="Add your notes about this word..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              rows={2}
              maxLength={500}
              data-testid="word-notes-input"
            />
          </div>
        )}

        {/* Info */}
        <p className="text-sm text-gray-500">
          {filteredWords.length} word{filteredWords.length !== 1 ? 's' : ''} available
          {existingWordIds.length > 0 && ` (${existingWordIds.length} already in list)`}
        </p>
      </div>
    </Modal>
  );
}
