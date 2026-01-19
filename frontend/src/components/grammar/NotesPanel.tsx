import { useState, useEffect, useRef } from 'react';
import { useGrammarStore } from '../../store/grammarStore';
import clsx from 'clsx';

// ========== TYPES ==========

export interface NotesPanelProps {
  /** Current exercise ID for exercise-specific notes */
  exerciseId?: number;
  /** Whether the panel is visible */
  isOpen: boolean;
  /** Callback when the panel should close */
  onClose: () => void;
  /** Position of the panel */
  position?: 'right' | 'bottom';
  /** Maximum character count for notes */
  maxLength?: number;
  /** Placeholder text */
  placeholder?: string;
}

// ========== COMPONENT ==========

export function NotesPanel({
  exerciseId,
  isOpen,
  onClose,
  position = 'right',
  maxLength = 500,
  placeholder = 'Add your notes here...',
}: NotesPanelProps) {
  const { sessionNotes, setNote, getNotesCount } = useGrammarStore();
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Local state for current note
  const [localNote, setLocalNote] = useState('');
  const [isSaving, setIsSaving] = useState(false);

  // Sync local note with store when exerciseId changes
  useEffect(() => {
    if (exerciseId !== undefined) {
      setLocalNote(sessionNotes[exerciseId] || '');
    }
  }, [exerciseId, sessionNotes]);

  // Auto-save when local note changes (debounced)
  useEffect(() => {
    if (exerciseId === undefined) return;

    const timeoutId = setTimeout(() => {
      if (localNote !== sessionNotes[exerciseId]) {
        setIsSaving(true);
        setNote(exerciseId, localNote);
        setTimeout(() => setIsSaving(false), 300);
      }
    }, 500);

    return () => clearTimeout(timeoutId);
  }, [localNote, exerciseId, sessionNotes, setNote]);

  // Focus textarea when panel opens
  useEffect(() => {
    if (isOpen && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [isOpen]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setLocalNote(value);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Prevent shortcuts from triggering when typing
    e.stopPropagation();

    // Escape to close panel
    if (e.key === 'Escape') {
      onClose();
    }
  };

  const characterCount = localNote.length;
  const isNearLimit = characterCount > maxLength * 0.8;
  const notesCount = getNotesCount();

  if (!isOpen) return null;

  const panelClasses = clsx(
    'bg-white shadow-lg border-l border-gray-200 flex flex-col',
    position === 'right' ? 'fixed top-0 right-0 h-full w-80 z-40' : 'w-full h-64'
  );

  return (
    <>
      {/* Backdrop for mobile */}
      {position === 'right' && (
        <div
          className="fixed inset-0 bg-black bg-opacity-25 z-30 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Panel */}
      <div className={panelClasses}>
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-gray-50">
          <div>
            <h3 className="font-semibold text-gray-900">Notes</h3>
            {notesCount > 0 && (
              <span className="text-xs text-gray-500">{notesCount} notes in session</span>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-1 text-gray-500 hover:text-gray-700 rounded-lg hover:bg-gray-200"
            aria-label="Close notes panel"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 p-4 flex flex-col">
          {exerciseId !== undefined ? (
            <>
              <div className="text-xs text-gray-500 mb-2">
                Exercise #{exerciseId}
              </div>
              <textarea
                ref={textareaRef}
                value={localNote}
                onChange={handleChange}
                onKeyDown={handleKeyDown}
                placeholder={placeholder}
                className={clsx(
                  'flex-1 w-full p-3 border rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500',
                  isNearLimit ? 'border-yellow-400' : 'border-gray-300'
                )}
                data-testid="notes-textarea"
              />
              <div className="flex items-center justify-between mt-2">
                <span
                  className={clsx(
                    'text-xs',
                    characterCount >= maxLength
                      ? 'text-red-600'
                      : isNearLimit
                      ? 'text-yellow-600'
                      : 'text-gray-500'
                  )}
                >
                  {characterCount}/{maxLength}
                </span>
                {isSaving && (
                  <span className="text-xs text-gray-500 flex items-center">
                    <svg
                      className="w-3 h-3 mr-1 animate-spin"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                      />
                    </svg>
                    Saving...
                  </span>
                )}
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center text-gray-500 text-sm">
              Select an exercise to add notes
            </div>
          )}
        </div>

        {/* Footer with all session notes summary */}
        {notesCount > 0 && (
          <div className="px-4 py-3 border-t border-gray-200 bg-gray-50">
            <div className="text-xs text-gray-600">
              <span className="font-medium">{notesCount}</span> notes will be saved to your
              session results
            </div>
          </div>
        )}

        {/* Keyboard shortcut hint */}
        <div className="px-4 py-2 border-t border-gray-200 bg-gray-100">
          <div className="text-xs text-gray-500 flex items-center justify-center">
            <kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs mr-1">
              N
            </kbd>
            <span>Toggle notes</span>
            <span className="mx-2">|</span>
            <kbd className="px-1.5 py-0.5 bg-white border border-gray-300 rounded text-xs mr-1">
              Esc
            </kbd>
            <span>Close</span>
          </div>
        </div>
      </div>
    </>
  );
}

// ========== NOTES TOGGLE BUTTON ==========

export interface NotesToggleButtonProps {
  /** Number of notes in the session */
  notesCount?: number;
  /** Whether the notes panel is open */
  isOpen: boolean;
  /** Callback to toggle the panel */
  onToggle: () => void;
  /** Additional class names */
  className?: string;
}

export function NotesToggleButton({
  notesCount = 0,
  isOpen,
  onToggle,
  className,
}: NotesToggleButtonProps) {
  return (
    <button
      onClick={onToggle}
      className={clsx(
        'relative flex items-center gap-1 px-3 py-2 rounded-lg border transition-colors',
        isOpen
          ? 'bg-primary-50 border-primary-300 text-primary-700'
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50',
        className
      )}
      title="Toggle notes (N)"
      data-testid="notes-toggle"
    >
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth={2}
          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
        />
      </svg>
      <span className="text-sm">Notes</span>
      {notesCount > 0 && (
        <span className="absolute -top-1 -right-1 w-5 h-5 flex items-center justify-center bg-primary-600 text-white text-xs font-medium rounded-full">
          {notesCount}
        </span>
      )}
    </button>
  );
}

// ========== INLINE NOTES DISPLAY ==========

export interface InlineNotesDisplayProps {
  notes: Record<number, string>;
  className?: string;
}

/**
 * Display all session notes inline (for results page)
 */
export function InlineNotesDisplay({ notes, className }: InlineNotesDisplayProps) {
  const nonEmptyNotes = Object.entries(notes).filter(
    ([_, note]) => note.trim().length > 0
  );

  if (nonEmptyNotes.length === 0) return null;

  return (
    <div className={clsx('space-y-3', className)}>
      {nonEmptyNotes.map(([exerciseId, note]) => (
        <div
          key={exerciseId}
          className="p-3 bg-blue-50 rounded-lg border border-blue-200"
        >
          <div className="text-xs text-blue-600 mb-1 font-medium">
            Exercise #{exerciseId}
          </div>
          <div className="text-sm text-gray-800 whitespace-pre-wrap">{note}</div>
        </div>
      ))}
    </div>
  );
}
