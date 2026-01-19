import type { PracticeSessionResponse, SessionProgress } from '../../api/types/grammar.types';
import { Card, Badge, Button, ProgressBar } from '../common';
import clsx from 'clsx';

interface SessionHeaderProps {
  sessionInfo: PracticeSessionResponse;
  progress: SessionProgress;
  currentStreak: number;
  onEndSession: () => void;

  // New props for enhanced functionality
  elapsedTime?: string;
  isPaused?: boolean;
  onPause?: () => void;
  onResume?: () => void;
  onToggleFocusMode?: () => void;
  isFocusMode?: boolean;
  notesCount?: number;
  onToggleNotes?: () => void;
  isNotesOpen?: boolean;
  autoAdvanceEnabled?: boolean;
  onToggleAutoAdvance?: () => void;
}

export function SessionHeader({
  sessionInfo,
  progress,
  currentStreak,
  onEndSession,
  elapsedTime,
  isPaused = false,
  onPause,
  onResume,
  onToggleFocusMode,
  isFocusMode = false,
  notesCount = 0,
  onToggleNotes,
  isNotesOpen = false,
  autoAdvanceEnabled = false,
  onToggleAutoAdvance,
}: SessionHeaderProps) {
  const progressPercentage =
    (progress.exercises_completed / sessionInfo.total_exercises) * 100;

  return (
    <Card>
      <div className="space-y-4">
        {/* Top Row: Progress, Timer, and Controls */}
        <div className="flex items-center justify-between gap-4">
          {/* Progress Section */}
          <div className="flex-1">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Question {progress.exercises_completed + 1} of {sessionInfo.total_exercises}
              </span>
              <div className="flex items-center gap-2">
                {/* Timer */}
                {elapsedTime && (
                  <span
                    className={clsx(
                      'text-sm font-mono px-2 py-1 rounded',
                      isPaused ? 'bg-yellow-100 text-yellow-700' : 'text-gray-600'
                    )}
                    data-testid="session-timer"
                  >
                    {isPaused && (
                      <span className="mr-1" title="Paused">
                        ||
                      </span>
                    )}
                    {elapsedTime}
                  </span>
                )}
              </div>
            </div>
            <ProgressBar
              value={progressPercentage}
              color="primary"
              showLabel={false}
              size="md"
            />
          </div>

          {/* Control Buttons */}
          <div className="flex items-center gap-2">
            {/* Pause/Resume Button */}
            {(onPause || onResume) && (
              <button
                onClick={isPaused ? onResume : onPause}
                className={clsx(
                  'p-2 rounded-lg border transition-colors',
                  isPaused
                    ? 'bg-yellow-50 border-yellow-300 text-yellow-700 hover:bg-yellow-100'
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                )}
                title={isPaused ? 'Resume (P)' : 'Pause (P)'}
                data-testid="pause-resume-button"
              >
                {isPaused ? (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                    />
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                ) : (
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 9v6m4-6v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                  </svg>
                )}
              </button>
            )}

            {/* Notes Toggle */}
            {onToggleNotes && (
              <button
                onClick={onToggleNotes}
                className={clsx(
                  'relative p-2 rounded-lg border transition-colors',
                  isNotesOpen
                    ? 'bg-primary-50 border-primary-300 text-primary-700'
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                )}
                title="Toggle notes (N)"
                data-testid="notes-toggle"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                  />
                </svg>
                {notesCount > 0 && (
                  <span className="absolute -top-1 -right-1 w-4 h-4 flex items-center justify-center bg-primary-600 text-white text-xs font-medium rounded-full">
                    {notesCount}
                  </span>
                )}
              </button>
            )}

            {/* Focus Mode Toggle */}
            {onToggleFocusMode && (
              <button
                onClick={onToggleFocusMode}
                className={clsx(
                  'p-2 rounded-lg border transition-colors',
                  isFocusMode
                    ? 'bg-primary-50 border-primary-300 text-primary-700'
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                )}
                title="Toggle focus mode (F)"
                data-testid="focus-mode-toggle"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {isFocusMode ? (
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
              </button>
            )}

            {/* Auto-Advance Toggle */}
            {onToggleAutoAdvance && (
              <button
                onClick={onToggleAutoAdvance}
                className={clsx(
                  'p-2 rounded-lg border transition-colors',
                  autoAdvanceEnabled
                    ? 'bg-green-50 border-green-300 text-green-700'
                    : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                )}
                title={autoAdvanceEnabled ? 'Auto-advance: ON' : 'Auto-advance: OFF'}
                data-testid="auto-advance-toggle"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M13 5l7 7-7 7M5 5l7 7-7 7"
                  />
                </svg>
              </button>
            )}

            {/* End Session Button */}
            <Button
              onClick={onEndSession}
              variant="secondary"
              size="sm"
              data-testid="end-session-button"
            >
              End
            </Button>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-4 gap-4">
          {/* Accuracy */}
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">
              {progress.accuracy_percentage.toFixed(0)}%
            </div>
            <div className="text-xs text-gray-600">Accuracy</div>
          </div>

          {/* Correct Answers */}
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {progress.exercises_correct}
            </div>
            <div className="text-xs text-gray-600">Correct</div>
          </div>

          {/* Points */}
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600">{progress.total_points}</div>
            <div className="text-xs text-gray-600">Points</div>
          </div>

          {/* Streak */}
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">
              {currentStreak > 0 ? `! ${currentStreak}` : currentStreak}
            </div>
            <div className="text-xs text-gray-600">Streak</div>
          </div>
        </div>

        {/* Topics Included */}
        {sessionInfo.topics_included.length > 0 && (
          <div className="pt-3 border-t border-gray-200">
            <div className="text-xs text-gray-600 mb-2">Topics in this session:</div>
            <div className="flex flex-wrap gap-2">
              {sessionInfo.topics_included.map((topic, index) => (
                <Badge key={index} variant="gray" size="sm">
                  {topic}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Settings Indicators */}
        <div className="pt-3 border-t border-gray-200 flex flex-wrap gap-2">
          {autoAdvanceEnabled && (
            <Badge variant="success" size="sm">
              Auto-advance ON
            </Badge>
          )}
          {notesCount > 0 && (
            <Badge variant="info" size="sm">
              {notesCount} note{notesCount !== 1 ? 's' : ''}
            </Badge>
          )}
        </div>
      </div>
    </Card>
  );
}
