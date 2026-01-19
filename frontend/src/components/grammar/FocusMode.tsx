import { useEffect, useCallback, type ReactNode } from 'react';
import { createPortal } from 'react-dom';
import clsx from 'clsx';
import type { PracticeSessionResponse, SessionProgress } from '../../api/types/grammar.types';
import { ProgressBar } from '../common';

// ========== TYPES ==========

export interface FocusModeProps {
  /** Whether focus mode is active */
  isActive: boolean;
  /** Callback when focus mode should be exited */
  onExit: () => void;
  /** The main content to display (exercise) */
  children: ReactNode;
  /** Optional session info for progress display */
  sessionInfo?: PracticeSessionResponse | null;
  /** Optional progress info */
  progress?: SessionProgress | null;
  /** Elapsed time in formatted string */
  elapsedTime?: string;
  /** Whether to use dark background */
  darkMode?: boolean;
}

// ========== COMPONENT ==========

export function FocusMode({
  isActive,
  onExit,
  children,
  sessionInfo,
  progress,
  elapsedTime,
  darkMode = false,
}: FocusModeProps) {
  // Handle escape key
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        onExit();
      }
    },
    [onExit]
  );

  // Set up escape key listener
  useEffect(() => {
    if (isActive) {
      document.addEventListener('keydown', handleKeyDown);
      // Prevent body scroll
      document.body.style.overflow = 'hidden';

      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        document.body.style.overflow = '';
      };
    }
  }, [isActive, handleKeyDown]);

  if (!isActive) return null;

  const progressPercentage =
    sessionInfo && progress
      ? (progress.exercises_completed / sessionInfo.total_exercises) * 100
      : 0;

  return createPortal(
    <div
      className={clsx(
        'fixed inset-0 z-50 flex flex-col',
        darkMode ? 'bg-gray-900' : 'bg-gray-100'
      )}
      data-testid="focus-mode-overlay"
    >
      {/* Top Bar - Minimal */}
      <div
        className={clsx(
          'flex items-center justify-between px-6 py-3',
          darkMode ? 'bg-gray-800 text-gray-200' : 'bg-white border-b border-gray-200'
        )}
      >
        {/* Progress indicator */}
        <div className="flex items-center gap-4 flex-1 max-w-md">
          {sessionInfo && progress && (
            <>
              <span className={clsx('text-sm', darkMode ? 'text-gray-400' : 'text-gray-600')}>
                {progress.exercises_completed + 1}/{sessionInfo.total_exercises}
              </span>
              <div className="flex-1">
                <ProgressBar
                  value={progressPercentage}
                  color="primary"
                  size="sm"
                  showLabel={false}
                />
              </div>
            </>
          )}
        </div>

        {/* Timer */}
        {elapsedTime && (
          <div
            className={clsx(
              'text-sm font-mono',
              darkMode ? 'text-gray-400' : 'text-gray-600'
            )}
          >
            {elapsedTime}
          </div>
        )}

        {/* Exit button */}
        <button
          onClick={onExit}
          className={clsx(
            'ml-4 p-2 rounded-lg transition-colors',
            darkMode
              ? 'text-gray-400 hover:text-gray-200 hover:bg-gray-700'
              : 'text-gray-500 hover:text-gray-700 hover:bg-gray-100'
          )}
          aria-label="Exit focus mode (Esc)"
          title="Exit focus mode (Esc)"
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

      {/* Main Content Area */}
      <div className="flex-1 flex items-center justify-center p-6 overflow-auto">
        <div className={clsx('w-full max-w-3xl', darkMode ? 'text-gray-100' : '')}>
          {children}
        </div>
      </div>

      {/* Bottom hint */}
      <div
        className={clsx(
          'text-center py-3 text-xs',
          darkMode ? 'text-gray-500' : 'text-gray-400'
        )}
      >
        Press{' '}
        <kbd
          className={clsx(
            'px-1.5 py-0.5 rounded border',
            darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-300'
          )}
        >
          Esc
        </kbd>{' '}
        or{' '}
        <kbd
          className={clsx(
            'px-1.5 py-0.5 rounded border',
            darkMode ? 'bg-gray-800 border-gray-700' : 'bg-white border-gray-300'
          )}
        >
          F
        </kbd>{' '}
        to exit focus mode
      </div>
    </div>,
    document.body
  );
}

// ========== FOCUS MODE TOGGLE BUTTON ==========

export interface FocusModeToggleButtonProps {
  /** Whether focus mode is active */
  isActive: boolean;
  /** Callback to toggle focus mode */
  onToggle: () => void;
  /** Additional class names */
  className?: string;
}

export function FocusModeToggleButton({
  isActive,
  onToggle,
  className,
}: FocusModeToggleButtonProps) {
  return (
    <button
      onClick={onToggle}
      className={clsx(
        'flex items-center gap-1 px-3 py-2 rounded-lg border transition-colors',
        isActive
          ? 'bg-primary-50 border-primary-300 text-primary-700'
          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50',
        className
      )}
      title="Toggle focus mode (F)"
      data-testid="focus-mode-toggle"
    >
      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        {isActive ? (
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 9V4.5M9 9H4.5M9 9L3.75 3.75M9 15v4.5M9 15H4.5M9 15l-5.25 5.25M15 9h4.5M15 9V4.5M15 9l5.25-5.25M15 15h4.5M15 15v4.5m0-4.5l5.25 5.25"
          />
        ) : (
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4"
          />
        )}
      </svg>
      <span className="text-sm hidden sm:inline">Focus</span>
    </button>
  );
}

// ========== PAUSED OVERLAY ==========

export interface PausedOverlayProps {
  /** Whether the session is paused */
  isPaused: boolean;
  /** Callback to resume the session */
  onResume: () => void;
  /** Elapsed time when paused */
  elapsedTime?: string;
}

export function PausedOverlay({ isPaused, onResume, elapsedTime }: PausedOverlayProps) {
  // Handle keyboard events
  useEffect(() => {
    if (!isPaused) return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'p' || e.key === ' ' || e.key === 'Enter') {
        e.preventDefault();
        onResume();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [isPaused, onResume]);

  if (!isPaused) return null;

  return createPortal(
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-75"
      data-testid="paused-overlay"
    >
      <div className="text-center text-white">
        <div className="text-6xl mb-4">⏸️</div>
        <h2 className="text-3xl font-bold mb-2">Paused</h2>
        {elapsedTime && (
          <p className="text-xl text-gray-300 mb-6 font-mono">{elapsedTime}</p>
        )}
        <button
          onClick={onResume}
          className="px-8 py-4 bg-primary-600 hover:bg-primary-700 text-white rounded-lg text-lg font-semibold transition-colors"
          data-testid="resume-button"
        >
          Resume
        </button>
        <div className="mt-4 text-gray-400 text-sm">
          Press{' '}
          <kbd className="px-1.5 py-0.5 bg-gray-800 border border-gray-600 rounded">P</kbd>{' '}
          or{' '}
          <kbd className="px-1.5 py-0.5 bg-gray-800 border border-gray-600 rounded">
            Space
          </kbd>{' '}
          to resume
        </div>
      </div>
    </div>,
    document.body
  );
}
