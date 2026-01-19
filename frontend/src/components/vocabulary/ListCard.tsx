import { type HTMLAttributes } from 'react';
import clsx from 'clsx';
import type { PersonalVocabularyList } from '../../api/types/vocabulary.types';

export interface ListCardProps extends HTMLAttributes<HTMLDivElement> {
  list: PersonalVocabularyList;
  onView?: (list: PersonalVocabularyList) => void;
  onDelete?: (list: PersonalVocabularyList) => void;
  onPractice?: (list: PersonalVocabularyList) => void;
  testId?: string;
}

export function ListCard({
  list,
  onView,
  onDelete,
  onPractice,
  className,
  testId,
  onClick,
  ...props
}: ListCardProps) {
  const isClickable = !!onClick || !!onView;

  const handleClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (onClick) {
      onClick(e);
    } else if (onView) {
      onView(list);
    }
  };

  return (
    <div
      className={clsx(
        'bg-white rounded-lg border border-gray-200 shadow-sm p-5 transition-all',
        isClickable && 'cursor-pointer hover:border-primary-300 hover:shadow-md',
        className
      )}
      onClick={handleClick}
      data-testid={testId}
      {...props}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <span className="text-2xl">📝</span>
          <h3 className="text-lg font-semibold text-gray-900">{list.name}</h3>
        </div>
        {list.is_public && (
          <span className="text-xs text-green-600 bg-green-50 px-2 py-1 rounded-full">
            Public
          </span>
        )}
      </div>

      {/* Description */}
      {list.description && (
        <p className="text-sm text-gray-600 mb-4 line-clamp-2">{list.description}</p>
      )}

      {/* Stats */}
      <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
        <span className="flex items-center gap-1">
          <span className="font-medium text-gray-900">{list.word_count}</span> words
        </span>
        <span>
          Created: {new Date(list.created_at).toLocaleDateString()}
        </span>
      </div>

      {/* Actions */}
      {(onPractice || onDelete) && (
        <div className="flex gap-2 pt-3 border-t border-gray-100">
          {onPractice && list.word_count > 0 && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onPractice(list);
              }}
              className="flex-1 px-3 py-2 text-sm font-medium text-white bg-primary-600 rounded-md hover:bg-primary-700 transition-colors"
              data-testid="list-practice-btn"
            >
              Practice
            </button>
          )}
          {onDelete && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onDelete(list);
              }}
              className="px-3 py-2 text-sm font-medium text-red-600 bg-red-50 rounded-md hover:bg-red-100 transition-colors"
              data-testid="list-delete-btn"
            >
              Delete
            </button>
          )}
        </div>
      )}
    </div>
  );
}
