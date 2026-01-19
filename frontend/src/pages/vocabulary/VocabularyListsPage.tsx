import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type { PersonalVocabularyList, PersonalVocabularyListCreate } from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useVocabularyStore } from '../../store/vocabularyStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Button, Loading, Card } from '../../components/common';
import { ListCard, CreateListModal } from '../../components/vocabulary';

export function VocabularyListsPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const { lists, setLists, addList, removeList, isLoadingLists, setLoadingLists } =
    useVocabularyStore();

  // Local state
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [deleteConfirmList, setDeleteConfirmList] = useState<PersonalVocabularyList | null>(null);

  useEffect(() => {
    loadLists();
  }, []);

  const loadLists = async () => {
    setLoadingLists(true);
    try {
      const data = await vocabularyService.getLists();
      setLists(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load lists', apiError.detail || 'An error occurred');
    } finally {
      setLoadingLists(false);
    }
  };

  const handleCreateList = async (listData: PersonalVocabularyListCreate) => {
    setIsCreating(true);
    try {
      const newList = await vocabularyService.createList(listData);
      addList(newList);
      setIsCreateModalOpen(false);
      addToast('success', 'List created', `"${newList.name}" has been created`);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to create list', apiError.detail || 'An error occurred');
      throw error;
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteList = async (list: PersonalVocabularyList) => {
    try {
      await vocabularyService.deleteList(list.id);
      removeList(list.id);
      setDeleteConfirmList(null);
      addToast('success', 'List deleted', `"${list.name}" has been deleted`);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to delete list', apiError.detail || 'An error occurred');
    }
  };

  const handleViewList = (list: PersonalVocabularyList) => {
    navigate(`/vocabulary/lists/${list.id}`);
  };

  const handlePracticeList = (list: PersonalVocabularyList) => {
    navigate(`/vocabulary/flashcards?list_id=${list.id}`);
  };

  if (isLoadingLists && lists.length === 0) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">My Vocabulary Lists</h1>
          <p className="mt-2 text-gray-600">
            {lists.length} list{lists.length !== 1 ? 's' : ''}
          </p>
        </div>
        <Button
          onClick={() => setIsCreateModalOpen(true)}
          variant="primary"
          data-testid="create-list-btn"
        >
          Create New List
        </Button>
      </div>

      {/* Lists Grid */}
      {lists.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📋</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No lists yet</h3>
            <p className="text-gray-600 mb-4">
              Create your first vocabulary list to organize words for study
            </p>
            <Button
              onClick={() => setIsCreateModalOpen(true)}
              variant="primary"
              data-testid="create-first-list-btn"
            >
              Create Your First List
            </Button>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {lists.map((list) => (
            <ListCard
              key={list.id}
              list={list}
              onView={handleViewList}
              onPractice={handlePracticeList}
              onDelete={() => setDeleteConfirmList(list)}
              testId={`list-card-${list.id}`}
            />
          ))}
        </div>
      )}

      {/* Create List Modal */}
      <CreateListModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onCreate={handleCreateList}
        isLoading={isCreating}
      />

      {/* Delete Confirmation Modal */}
      {deleteConfirmList && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <Card className="max-w-md w-full">
            <div className="text-center">
              <div className="text-4xl mb-4">⚠️</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete List?</h3>
              <p className="text-gray-600 mb-6">
                Are you sure you want to delete "{deleteConfirmList.name}"? This action cannot be
                undone.
              </p>
              <div className="flex gap-3">
                <Button
                  onClick={() => handleDeleteList(deleteConfirmList)}
                  variant="danger"
                  fullWidth
                  data-testid="confirm-delete-btn"
                >
                  Delete
                </Button>
                <Button
                  onClick={() => setDeleteConfirmList(null)}
                  variant="ghost"
                  fullWidth
                  data-testid="cancel-delete-btn"
                >
                  Cancel
                </Button>
              </div>
            </div>
          </Card>
        </div>
      )}
    </div>
  );
}
