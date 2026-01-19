import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type { VocabularyWithProgress } from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useVocabularyStore } from '../../store/vocabularyStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Button, Loading, Card } from '../../components/common';
import {
  WordCard,
  WordFilters,
  WordDetailModal,
} from '../../components/vocabulary';

type ViewMode = 'grid' | 'list';

export function VocabularyBrowserPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const {
    words,
    setWords,
    filters,
    setFilters,
    clearFilters,
    categories,
    setCategories,
    isLoadingWords,
    setLoadingWords,
    selectedWord,
    setSelectedWord,
  } = useVocabularyStore();

  // Local state
  const [filteredWords, setFilteredWords] = useState<VocabularyWithProgress[]>([]);
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);

  // Load words on mount
  useEffect(() => {
    loadWords();
    loadCategories();
  }, []);

  // Filter words when filters change
  useEffect(() => {
    filterWords();
  }, [words, filters]);

  const loadWords = async () => {
    setLoadingWords(true);
    try {
      const data = await vocabularyService.getWords({ limit: 500 });
      setWords(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load words', apiError.detail || 'An error occurred');
    } finally {
      setLoadingWords(false);
    }
  };

  const loadCategories = async () => {
    try {
      const cats = await vocabularyService.getCategories();
      setCategories(cats);
    } catch (error) {
      // Silently fail, categories are optional
      console.error('Failed to load categories:', error);
    }
  };

  const filterWords = useCallback(() => {
    let filtered = [...words];

    // Search filter
    if (filters.search) {
      const query = filters.search.toLowerCase();
      filtered = filtered.filter(
        (w) =>
          w.word.toLowerCase().includes(query) ||
          w.translation_it.toLowerCase().includes(query) ||
          (w.definition_de && w.definition_de.toLowerCase().includes(query))
      );
    }

    // Category filter
    if (filters.category) {
      filtered = filtered.filter((w) => w.category === filters.category);
    }

    // Difficulty filter
    if (filters.difficulty) {
      filtered = filtered.filter((w) => w.difficulty === filters.difficulty);
    }

    // Mastery filter
    if (filters.mastery_level !== undefined) {
      filtered = filtered.filter((w) => w.mastery_level === filters.mastery_level);
    }

    setFilteredWords(filtered);
  }, [words, filters]);

  const handleWordClick = async (word: VocabularyWithProgress) => {
    // Fetch full word data with progress fields from single-word endpoint
    try {
      setLoadingWords(true);
      const fullWord = await vocabularyService.getWord(word.id);
      setSelectedWord(fullWord);
      setIsDetailModalOpen(true);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load word details', apiError.detail || 'An error occurred');
      // Fallback: use the word data from the list (may have missing progress fields)
      setSelectedWord(word);
      setIsDetailModalOpen(true);
    } finally {
      setLoadingWords(false);
    }
  };

  const handleCloseModal = () => {
    setIsDetailModalOpen(false);
    setSelectedWord(null);
  };

  const handlePracticeWord = (word: VocabularyWithProgress) => {
    navigate(`/vocabulary/flashcards?word_ids=${word.id}`);
  };

  const handleStartFlashcards = () => {
    navigate('/vocabulary/flashcards');
  };

  const handleStartQuiz = () => {
    navigate('/vocabulary/quiz');
  };

  if (isLoadingWords && words.length === 0) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Vocabulary</h1>
          <p className="mt-2 text-gray-600">
            {filteredWords.length} word{filteredWords.length !== 1 ? 's' : ''} available
            {filters.search || filters.category || filters.difficulty || filters.mastery_level !== undefined
              ? ' (filtered)'
              : ''}
          </p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button onClick={handleStartFlashcards} variant="primary" data-testid="start-flashcards-btn">
            Start Flashcards
          </Button>
          <Button onClick={handleStartQuiz} variant="secondary" data-testid="start-quiz-btn">
            Take Quiz
          </Button>
        </div>
      </div>

      {/* Filters */}
      <div className="mb-6">
        <WordFilters
          filters={filters}
          categories={categories}
          onFilterChange={setFilters}
          onClearFilters={clearFilters}
        />
      </div>

      {/* View toggle */}
      <div className="flex items-center justify-between mb-4">
        <p className="text-sm text-gray-500">
          Showing {filteredWords.length} of {words.length} words
        </p>
        <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-1">
          <button
            onClick={() => setViewMode('grid')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
              viewMode === 'grid'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
            data-testid="view-grid-btn"
          >
            Grid
          </button>
          <button
            onClick={() => setViewMode('list')}
            className={`px-3 py-1.5 text-sm font-medium rounded-md transition-colors ${
              viewMode === 'list'
                ? 'bg-white text-gray-900 shadow-sm'
                : 'text-gray-600 hover:text-gray-900'
            }`}
            data-testid="view-list-btn"
          >
            List
          </button>
        </div>
      </div>

      {/* Words display */}
      {filteredWords.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No words found</h3>
            <p className="text-gray-600 mb-4">
              {words.length === 0
                ? 'No vocabulary words have been added yet.'
                : 'Try adjusting your filters to see more words.'}
            </p>
            {words.length > 0 && (
              <Button onClick={clearFilters} variant="secondary">
                Clear Filters
              </Button>
            )}
          </div>
        </Card>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredWords.map((word) => (
            <WordCard
              key={word.id}
              word={word}
              variant="default"
              showExamples={false}
              onClick={() => handleWordClick(word)}
              testId={`word-card-${word.id}`}
            />
          ))}
        </div>
      ) : (
        <div className="space-y-2">
          {filteredWords.map((word) => (
            <WordCard
              key={word.id}
              word={word}
              variant="compact"
              onClick={() => handleWordClick(word)}
              testId={`word-card-${word.id}`}
            />
          ))}
        </div>
      )}

      {/* Load more indicator */}
      {isLoadingWords && words.length > 0 && (
        <div className="flex justify-center py-8">
          <Loading />
        </div>
      )}

      {/* Word Detail Modal */}
      <WordDetailModal
        word={selectedWord}
        isOpen={isDetailModalOpen}
        onClose={handleCloseModal}
        onPractice={handlePracticeWord}
      />
    </div>
  );
}
