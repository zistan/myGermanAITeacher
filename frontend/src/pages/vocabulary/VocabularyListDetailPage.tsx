import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type { PersonalVocabularyListWithWords, VocabularyWithProgress } from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useNotificationStore } from '../../store/notificationStore';
import { Button, Loading, Card } from '../../components/common';
import { WordCard, AddWordToListModal, WordDetailModal } from '../../components/vocabulary';

export function VocabularyListDetailPage() {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const addToast = useNotificationStore((state) => state.addToast);

  // State
  const [list, setList] = useState<PersonalVocabularyListWithWords | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [selectedWord, setSelectedWord] = useState<VocabularyWithProgress | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState(false);
  const [removingWordId, setRemovingWordId] = useState<number | null>(null);

  useEffect(() => {
    if (id) {
      loadList(parseInt(id));
    }
  }, [id]);

  const loadList = async (listId: number) => {
    setIsLoading(true);
    try {
      const data = await vocabularyService.getList(listId);
      setList(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load list', apiError.detail || 'An error occurred');
      navigate('/vocabulary/lists');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddWord = async (listId: number, wordId: number, notes?: string) => {
    try {
      await vocabularyService.addWordToList(listId, { word_id: wordId, notes });
      // Reload list to get updated word list
      await loadList(listId);
      setIsAddModalOpen(false);
      addToast('success', 'Word added', 'Word has been added to the list');
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to add word', apiError.detail || 'An error occurred');
      throw error;
    }
  };

  const handleRemoveWord = async (wordId: number) => {
    if (!list) return;

    setRemovingWordId(wordId);
    try {
      await vocabularyService.removeWordFromList(list.id, wordId);
      setList({
        ...list,
        words: list.words.filter((w) => w.id !== wordId),
        word_count: list.word_count - 1,
      });
      addToast('success', 'Word removed', 'Word has been removed from the list');
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to remove word', apiError.detail || 'An error occurred');
    } finally {
      setRemovingWordId(null);
    }
  };

  const handleWordClick = (word: VocabularyWithProgress) => {
    setSelectedWord(word);
    setIsDetailModalOpen(true);
  };

  const handlePracticeWord = (word: VocabularyWithProgress) => {
    navigate(`/vocabulary/flashcards?word_ids=${word.id}`);
  };

  const handlePracticeAll = () => {
    if (!list || list.words.length === 0) return;
    const wordIds = list.words.map((w) => w.id).join(',');
    navigate(`/vocabulary/flashcards?word_ids=${wordIds}`);
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  if (!list) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">❌</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">List not found</h2>
            <Button onClick={() => navigate('/vocabulary/lists')}>Back to Lists</Button>
          </div>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 text-sm text-gray-500 mb-4">
          <button
            onClick={() => navigate('/vocabulary/lists')}
            className="hover:text-primary-600"
            data-testid="back-to-lists-link"
          >
            My Lists
          </button>
          <span>/</span>
          <span className="text-gray-900">{list.name}</span>
        </nav>

        <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold text-gray-900">{list.name}</h1>
              {list.is_public && (
                <span className="text-sm text-green-600 bg-green-50 px-2 py-1 rounded-full">
                  Public
                </span>
              )}
            </div>
            {list.description && <p className="text-gray-600 mb-2">{list.description}</p>}
            <p className="text-sm text-gray-500">
              {list.word_count} word{list.word_count !== 1 ? 's' : ''} •
              Created {new Date(list.created_at).toLocaleDateString()}
            </p>
          </div>
          <div className="flex flex-wrap gap-3">
            {list.words.length > 0 && (
              <Button
                onClick={handlePracticeAll}
                variant="primary"
                data-testid="practice-all-btn"
              >
                Practice All ({list.words.length})
              </Button>
            )}
            <Button
              onClick={() => setIsAddModalOpen(true)}
              variant="secondary"
              data-testid="add-word-btn"
            >
              Add Word
            </Button>
          </div>
        </div>
      </div>

      {/* Words */}
      {list.words.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📝</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No words yet</h3>
            <p className="text-gray-600 mb-4">
              Add words to this list to start practicing
            </p>
            <Button
              onClick={() => setIsAddModalOpen(true)}
              variant="primary"
              data-testid="add-first-word-btn"
            >
              Add Your First Word
            </Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-3">
          {list.words.map((word) => (
            <div key={word.id} className="relative group">
              <WordCard
                word={word}
                variant="compact"
                onClick={() => handleWordClick(word)}
                testId={`word-${word.id}`}
              />
              {/* Remove button */}
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  handleRemoveWord(word.id);
                }}
                disabled={removingWordId === word.id}
                className="absolute right-2 top-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity p-2 text-red-600 hover:bg-red-50 rounded-md"
                data-testid={`remove-word-${word.id}-btn`}
              >
                {removingWordId === word.id ? (
                  <span className="animate-spin">⟳</span>
                ) : (
                  <span>✕</span>
                )}
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Add Word Modal */}
      <AddWordToListModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        list={list}
        onAddWord={handleAddWord}
        existingWordIds={list.words.map((w) => w.id)}
      />

      {/* Word Detail Modal */}
      <WordDetailModal
        word={selectedWord}
        isOpen={isDetailModalOpen}
        onClose={() => {
          setIsDetailModalOpen(false);
          setSelectedWord(null);
        }}
        onPractice={handlePracticeWord}
      />
    </div>
  );
}
