import { useEffect, useState, useCallback } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type {
  GrammarExercise,
  PracticeSessionResponse,
  ExerciseFeedback,
  SessionProgress,
} from '../../api/types/grammar.types';
import { Loading, Button, Card, Badge, Modal } from '../../components/common';
import { useNotificationStore } from '../../store/notificationStore';
import { useGrammarStore, type SessionAnswer } from '../../store/grammarStore';
import type { ApiError } from '../../api/types/common.types';
import { ExerciseRenderer } from '../../components/grammar/ExerciseRenderer';
import { FeedbackDisplay } from '../../components/grammar/FeedbackDisplay';
import { SessionHeader } from '../../components/grammar/SessionHeader';
import {
  NotesPanel,
  FocusMode,
  PausedOverlay,
} from '../../components/grammar';
import {
  useKeyboardShortcuts,
  createPracticeContext,
  createFeedbackContext,
  createPausedContext,
  createFocusModeContext,
  useShortcutDisplay,
} from '../../hooks/useKeyboardShortcuts';
import { useSessionPersistence, useSessionTimer } from '../../hooks/useSessionPersistence';

type SessionState = 'loading' | 'active' | 'feedback' | 'completed' | 'error';

export function PracticeSessionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const addToast = useNotificationStore((state) => state.addToast);

  // Grammar store
  const {
    setSessionState: setStoreSessionState,
    startSession: storeStartSession,
    setCurrentExercise,
    recordAnswer,
    pauseSession,
    resumeSession,
    endSession: storeEndSession,
    isFocusMode,
    toggleFocusMode,
    autoAdvanceEnabled,
    autoAdvanceDelay,
    setAutoAdvance,
    toggleBookmark,
    isBookmarked,
    getNotesCount,
  } = useGrammarStore();

  // Session timer
  const { elapsedFormatted, isPaused } = useSessionTimer();

  // Local session data
  const [sessionState, setSessionState] = useState<SessionState>('loading');
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [sessionInfo, setSessionInfo] = useState<PracticeSessionResponse | null>(null);
  const [currentExercise, setLocalCurrentExercise] = useState<GrammarExercise | null>(null);
  const [feedback, setFeedback] = useState<ExerciseFeedback | null>(null);
  const [progress, setProgress] = useState<SessionProgress | null>(null);

  // User input
  const [userAnswer, setUserAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // UI state
  const [isNotesOpen, setIsNotesOpen] = useState(false);
  const [showRestoreModal, setShowRestoreModal] = useState(false);
  const [autoAdvanceTimer, setAutoAdvanceTimer] = useState<number | null>(null);
  const [autoAdvanceCountdown, setAutoAdvanceCountdown] = useState(0);

  // Session metrics
  const [exerciseStartTime, setExerciseStartTime] = useState<number>(Date.now());
  const [currentStreak, setCurrentStreak] = useState(0);

  // Session persistence
  const { hasIncompleteSession, restoreSession, clearSession: clearPersistedSession } =
    useSessionPersistence({
      onSessionRestored: (session) => {
        // Handle restored session
        setSessionId(session.sessionId);
        // We'll need to refetch the session info
        loadSessionFromStore(session.sessionId);
      },
    });

  // Check for incomplete session on mount
  useEffect(() => {
    if (hasIncompleteSession) {
      setShowRestoreModal(true);
    } else {
      startSession();
    }
  }, []);

  const loadSessionFromStore = async (restoredSessionId: number) => {
    setSessionState('loading');
    try {
      // Set the restored session ID
      setSessionId(restoredSessionId);

      // Restore current exercise from store (for immediate display)
      const storedExercise = useGrammarStore.getState().currentExercise;
      if (storedExercise) {
        setLocalCurrentExercise(storedExercise);
      }

      // Initialize progress from store data
      const grammarSession = useGrammarStore.getState().currentSession;
      if (grammarSession) {
        setProgress({
          exercises_completed: grammarSession.answers.length,
          exercises_correct: grammarSession.answers.filter((a) => a.isCorrect).length,
          current_streak: 0, // Will be updated
          total_points: 0, // Will be updated
          accuracy_percentage:
            grammarSession.answers.length > 0
              ? Math.round(
                  (grammarSession.answers.filter((a) => a.isCorrect).length /
                    grammarSession.answers.length) *
                    100
                )
              : 0,
        });
      }

      // Try to load the next exercise from the restored session
      await loadNextExercise(restoredSessionId);

      addToast('success', 'Session restored', 'Continuing from where you left off');
    } catch (error) {
      // If the backend session no longer exists, start a new one
      const apiError = error as ApiError;
      addToast('warning', 'Could not restore session', 'Starting a new session instead');
      console.error('Session restore failed:', apiError);
      storeStartSession(0); // Temporary until we start new session
      startSession();
    }
  };

  const handleRestoreSession = () => {
    setShowRestoreModal(false);
    const session = restoreSession();
    if (session) {
      loadSessionFromStore(session.sessionId);
    } else {
      startSession();
    }
  };

  const handleStartFresh = () => {
    setShowRestoreModal(false);
    clearPersistedSession();
    startSession();
  };

  const startSession = async () => {
    setSessionState('loading');
    try {
      // Parse URL params
      const topicsParam = searchParams.get('topics');
      const difficultyParam = searchParams.get('difficulty');
      const countParam = searchParams.get('count');

      const topicIds = topicsParam ? topicsParam.split(',').map(Number) : undefined;

      // Start session via API
      const session = await grammarService.startPracticeSession({
        topic_ids: topicIds,
        difficulty_level: difficultyParam as any,
        exercise_count: countParam ? parseInt(countParam) : 10,
        use_spaced_repetition: true,
      });

      setSessionId(session.session_id);
      setSessionInfo(session);

      // Initialize store session
      storeStartSession(session.session_id);
      setStoreSessionState('active');

      // Initialize progress
      setProgress({
        exercises_completed: 0,
        exercises_correct: 0,
        current_streak: 0,
        total_points: 0,
        accuracy_percentage: 0,
      });

      // Get first exercise
      await loadNextExercise(session.session_id);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to start session', apiError.detail);
      setSessionState('error');
    }
  };

  const loadNextExercise = async (sid: number) => {
    try {
      const exercise = await grammarService.getNextExercise(sid);
      setLocalCurrentExercise(exercise);
      setCurrentExercise(exercise);
      setUserAnswer('');
      setFeedback(null);
      setSessionState('active');
      setStoreSessionState('active');
      setExerciseStartTime(Date.now());

      // Clear any auto-advance timer
      if (autoAdvanceTimer) {
        clearInterval(autoAdvanceTimer);
        setAutoAdvanceTimer(null);
      }
      setAutoAdvanceCountdown(0);
    } catch (error) {
      // No more exercises - session complete
      setSessionState('completed');
      setStoreSessionState('completed');
    }
  };

  const handleSubmitAnswer = useCallback(async () => {
    if (!sessionId || !currentExercise || !userAnswer.trim()) {
      addToast('warning', 'Please provide an answer', 'Enter your answer before submitting');
      return;
    }

    setIsSubmitting(true);
    try {
      const timeSpent = Math.floor((Date.now() - exerciseStartTime) / 1000);

      const result = await grammarService.submitAnswer(sessionId, {
        exercise_id: currentExercise.id,
        user_answer: userAnswer.trim(),
        time_spent_seconds: timeSpent,
      });

      setFeedback(result.feedback);
      setProgress(result.session_progress);
      setSessionState('feedback');
      setStoreSessionState('feedback');

      // Record answer in store
      const answer: SessionAnswer = {
        exerciseId: currentExercise.id,
        userAnswer: userAnswer.trim(),
        isCorrect: result.feedback.is_correct,
        feedback: result.feedback,
        timeSpent,
        timestamp: Date.now(),
      };
      recordAnswer(answer);

      // Update streak
      if (result.feedback.is_correct) {
        setCurrentStreak((prev) => prev + 1);
        if (currentStreak + 1 >= 5) {
          addToast('success', 'Amazing streak!', `${currentStreak + 1} correct answers in a row!`);
        }

        // Start auto-advance timer if enabled
        if (autoAdvanceEnabled) {
          startAutoAdvance();
        }
      } else {
        setCurrentStreak(0);
      }
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to submit answer', apiError.detail);
    } finally {
      setIsSubmitting(false);
    }
  }, [sessionId, currentExercise, userAnswer, exerciseStartTime, currentStreak, autoAdvanceEnabled]);

  const startAutoAdvance = () => {
    setAutoAdvanceCountdown(autoAdvanceDelay);

    const timer = window.setInterval(() => {
      setAutoAdvanceCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          handleNext();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    setAutoAdvanceTimer(timer);
  };

  const cancelAutoAdvance = () => {
    if (autoAdvanceTimer) {
      clearInterval(autoAdvanceTimer);
      setAutoAdvanceTimer(null);
    }
    setAutoAdvanceCountdown(0);
  };

  const handleNext = useCallback(async () => {
    cancelAutoAdvance();
    if (!sessionId) return;
    await loadNextExercise(sessionId);
  }, [sessionId]);

  const handleEndSession = useCallback(async () => {
    if (!sessionId) return;

    try {
      const results = await grammarService.endPracticeSession(sessionId);
      storeEndSession();
      navigate('/grammar/results', { state: { results } });
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to end session', apiError.detail);
    }
  }, [sessionId, navigate, addToast, storeEndSession]);

  const handlePause = useCallback(() => {
    pauseSession();
    cancelAutoAdvance();
  }, [pauseSession]);

  const handleResume = useCallback(() => {
    resumeSession();
  }, [resumeSession]);

  const handleToggleBookmark = useCallback(() => {
    if (currentExercise) {
      toggleBookmark(currentExercise.id);
      const isNowBookmarked = !isBookmarked(currentExercise.id);
      addToast(
        'info',
        isNowBookmarked ? 'Bookmarked' : 'Bookmark removed',
        isNowBookmarked ? 'Exercise saved for review' : 'Bookmark removed'
      );
    }
  }, [currentExercise, toggleBookmark, isBookmarked, addToast]);

  const handleToggleNotes = useCallback(() => {
    setIsNotesOpen((prev) => !prev);
  }, []);

  const handleToggleFocusMode = useCallback(() => {
    toggleFocusMode();
  }, [toggleFocusMode]);

  // Keyboard shortcuts
  const practiceContext = createPracticeContext({
    onSubmit: handleSubmitAnswer,
    onEndSession: handleEndSession,
    onToggleBookmark: handleToggleBookmark,
    onToggleNotes: handleToggleNotes,
    onToggleFocusMode: handleToggleFocusMode,
    onPause: handlePause,
  });

  const feedbackContext = createFeedbackContext({
    onNext: handleNext,
    onToggleBookmark: handleToggleBookmark,
    onToggleNotes: handleToggleNotes,
  });

  const pausedContext = createPausedContext({
    onResume: handleResume,
  });

  const focusModeContext = createFocusModeContext({
    onExit: handleToggleFocusMode,
  });

  const contexts = [
    { ...practiceContext, enabled: sessionState === 'active' && !isPaused && !isFocusMode },
    { ...feedbackContext, enabled: sessionState === 'feedback' && !isPaused && !isFocusMode },
    { ...pausedContext, enabled: isPaused },
    { ...focusModeContext, enabled: isFocusMode },
  ];

  useKeyboardShortcuts({ contexts });

  const displayShortcuts = useShortcutDisplay(contexts);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (autoAdvanceTimer) {
        clearInterval(autoAdvanceTimer);
      }
    };
  }, [autoAdvanceTimer]);

  // Render loading state
  if (sessionState === 'loading') {
    return <Loading fullScreen />;
  }

  // Render error state
  if (sessionState === 'error') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">!</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Failed to start session</h2>
            <p className="text-gray-600 mb-4">Please try again</p>
            <Button onClick={() => navigate('/grammar')}>Back to Topics</Button>
          </div>
        </Card>
      </div>
    );
  }

  // Render completed state
  if (sessionState === 'completed') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">!</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Session Complete!</h2>
            <p className="text-gray-600 mb-6">Great work! Let's review your results.</p>
            <div className="flex gap-4 justify-center">
              <Button onClick={handleEndSession} variant="primary">
                View Results
              </Button>
              <Button onClick={() => navigate('/grammar')} variant="secondary">
                Back to Topics
              </Button>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  // Main exercise content
  const exerciseContent = currentExercise && (
    <>
      {/* Exercise Type Badge */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Badge variant="info">{currentExercise.exercise_type.replace('_', ' ')}</Badge>
          <Badge variant="gray">{currentExercise.difficulty_level}</Badge>
        </div>
        <div className="flex items-center gap-2">
          {/* Bookmark button */}
          <button
            onClick={handleToggleBookmark}
            className={`p-2 rounded-lg transition-colors ${
              isBookmarked(currentExercise.id)
                ? 'text-yellow-500 bg-yellow-50'
                : 'text-gray-400 hover:text-yellow-500 hover:bg-yellow-50'
            }`}
            title="Bookmark exercise (B)"
          >
            <svg className="w-5 h-5" fill={isBookmarked(currentExercise.id) ? 'currentColor' : 'none'} stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
            </svg>
          </button>
        </div>
      </div>

      {/* Exercise Content */}
      {sessionState === 'active' && (
        <ExerciseRenderer
          exercise={currentExercise}
          userAnswer={userAnswer}
          onAnswerChange={setUserAnswer}
          onSubmit={handleSubmitAnswer}
          isSubmitting={isSubmitting}
        />
      )}

      {/* Feedback */}
      {sessionState === 'feedback' && feedback && (
        <>
          <FeedbackDisplay
            feedback={feedback}
            onNext={handleNext}
            userAnswer={userAnswer}
            exerciseType={currentExercise.exercise_type}
          />

          {/* Auto-advance indicator */}
          {autoAdvanceEnabled && autoAdvanceCountdown > 0 && (
            <div className="mt-4 text-center">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-lg">
                <span>Auto-advancing in {autoAdvanceCountdown}s</span>
                <button
                  onClick={cancelAutoAdvance}
                  className="text-blue-600 hover:text-blue-800"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </>
  );

  return (
    <>
      {/* Session Restore Modal */}
      <Modal
        isOpen={showRestoreModal}
        onClose={() => {}}
        title="Resume Previous Session?"
      >
        <div className="space-y-4">
          <p className="text-gray-600">
            You have an incomplete practice session. Would you like to resume where you left off?
          </p>
          <div className="flex gap-3 justify-end">
            <Button onClick={handleStartFresh} variant="secondary">
              Start Fresh
            </Button>
            <Button onClick={handleRestoreSession} variant="primary">
              Resume Session
            </Button>
          </div>
        </div>
      </Modal>

      {/* Paused Overlay */}
      <PausedOverlay
        isPaused={isPaused}
        onResume={handleResume}
        elapsedTime={elapsedFormatted}
      />

      {/* Focus Mode */}
      <FocusMode
        isActive={isFocusMode}
        onExit={handleToggleFocusMode}
        sessionInfo={sessionInfo}
        progress={progress}
        elapsedTime={elapsedFormatted}
      >
        <Card>{exerciseContent}</Card>
      </FocusMode>

      {/* Notes Panel */}
      <NotesPanel
        exerciseId={currentExercise?.id}
        isOpen={isNotesOpen}
        onClose={() => setIsNotesOpen(false)}
      />

      {/* Main Content (hidden in focus mode) */}
      {!isFocusMode && (
        <div className="max-w-4xl mx-auto px-4 py-8">
          {/* Session Header */}
          {sessionInfo && progress && (
            <SessionHeader
              sessionInfo={sessionInfo}
              progress={progress}
              currentStreak={currentStreak}
              elapsedTime={elapsedFormatted}
              isPaused={isPaused}
              onEndSession={handleEndSession}
              onPause={handlePause}
              onResume={handleResume}
              onToggleFocusMode={handleToggleFocusMode}
              isFocusMode={isFocusMode}
              notesCount={getNotesCount()}
              onToggleNotes={handleToggleNotes}
              isNotesOpen={isNotesOpen}
              autoAdvanceEnabled={autoAdvanceEnabled}
              onToggleAutoAdvance={() => setAutoAdvance(!autoAdvanceEnabled)}
            />
          )}

          {/* Exercise Card */}
          {currentExercise && (
            <Card className="mt-6">
              {exerciseContent}
            </Card>
          )}

          {/* Keyboard Shortcuts Helper */}
          <div className="mt-4 text-center text-sm text-gray-500" data-testid="keyboard-shortcuts-hint">
            <span className="inline-flex items-center flex-wrap justify-center gap-2">
              {displayShortcuts.slice(0, 4).map((shortcut, index) => (
                <span key={index} className="inline-flex items-center">
                  <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs mr-1">
                    {shortcut.key}
                  </kbd>
                  <span className="text-xs">{shortcut.description}</span>
                  {index < Math.min(displayShortcuts.length - 1, 3) && (
                    <span className="mx-2">|</span>
                  )}
                </span>
              ))}
            </span>
          </div>
        </div>
      )}
    </>
  );
}
