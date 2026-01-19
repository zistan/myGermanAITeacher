import { useState } from 'react';
import { Modal, Button } from '../common';
import type { PersonalVocabularyListCreate } from '../../api/types/vocabulary.types';

export interface CreateListModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreate: (list: PersonalVocabularyListCreate) => Promise<void>;
  isLoading?: boolean;
}

export function CreateListModal({
  isOpen,
  onClose,
  onCreate,
  isLoading = false,
}: CreateListModalProps) {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isPublic, setIsPublic] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!name.trim()) {
      setError('Please enter a list name');
      return;
    }

    try {
      await onCreate({
        name: name.trim(),
        description: description.trim() || null,
        is_public: isPublic,
      });
      handleClose();
    } catch (err) {
      setError('Failed to create list. Please try again.');
    }
  };

  const handleClose = () => {
    setName('');
    setDescription('');
    setIsPublic(false);
    setError(null);
    onClose();
  };

  const footer = (
    <div className="flex gap-3">
      <Button
        onClick={handleSubmit}
        variant="primary"
        isLoading={isLoading}
        disabled={!name.trim()}
        data-testid="create-list-submit-btn"
      >
        Create List
      </Button>
      <Button onClick={handleClose} variant="ghost">
        Cancel
      </Button>
    </div>
  );

  return (
    <Modal isOpen={isOpen} onClose={handleClose} title="Create New List" footer={footer}>
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Name */}
        <div>
          <label htmlFor="list-name" className="block text-sm font-medium text-gray-700 mb-1">
            List Name *
          </label>
          <input
            id="list-name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g., Business Terms, Travel Words"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            maxLength={100}
            autoFocus
            data-testid="list-name-input"
          />
        </div>

        {/* Description */}
        <div>
          <label htmlFor="list-description" className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            id="list-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="What is this list for?"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            rows={3}
            maxLength={500}
            data-testid="list-description-input"
          />
        </div>

        {/* Public toggle */}
        <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
          <div>
            <div className="font-medium text-gray-900">Make Public</div>
            <div className="text-sm text-gray-500">Allow others to view this list</div>
          </div>
          <button
            type="button"
            onClick={() => setIsPublic(!isPublic)}
            className={`relative w-14 h-7 rounded-full transition-colors ${
              isPublic ? 'bg-primary-600' : 'bg-gray-300'
            }`}
            data-testid="list-public-toggle"
          >
            <span
              className={`absolute top-0.5 left-0.5 w-6 h-6 bg-white rounded-full transition-transform ${
                isPublic ? 'translate-x-7' : 'translate-x-0'
              }`}
            />
          </button>
        </div>

        {/* Error */}
        {error && (
          <p className="text-sm text-red-600" data-testid="list-create-error">
            {error}
          </p>
        )}
      </form>
    </Modal>
  );
}
