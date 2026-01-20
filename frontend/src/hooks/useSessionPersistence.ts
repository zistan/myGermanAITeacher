import { useCallback, useEffect, useState } from 'react';
import { useGrammarStore, type GrammarSessionData } from '../store/grammarStore';
import grammarService from '../api/services/grammarService';

interface SessionPersistenceOptions {
  autoRestore?: boolean;
  onSessionRestored?: (session: GrammarSessionData) => void;
  onSessionExpired?: () => void;
}

interface SessionPersistenceReturn {
  // State
  hasIncompleteSession: boolean;
  sessionAge: number | null; // hours
  isRestoring: boolean;

  // Actions
  restoreSession: () => GrammarSessionData | null;
  clearSession: () => void;
  dismissRestore: () => void;

  // Prompt state
  showRestorePrompt: boolean;
}

/**
 * Hook for managing grammar session persistence.
 *
 * Features:
 * - Detects incomplete sessions on page load
 * - Shows restore prompt for sessions less than 24 hours old
 * - Handles session expiration
 * - Auto-saves session progress
 *
 * @example
 * ```tsx
 * const {
 *   hasIncompleteSession,
 *   showRestorePrompt,
 *   restoreSession,
 *   dismissRestore
 * } = useSessionPersistence({
 *   onSessionRestored: (session) => {
 *     navigate(`/grammar/practice?session=${session.sessionId}`);
 *   }
 * });
 * ```
 */
export function useSessionPersistence(
  options: SessionPersistenceOptions = {}
): SessionPersistenceReturn {
  const { autoRestore = false, onSessionRestored, onSessionExpired } = options;

  // Store access
  const storeHasIncomplete = useGrammarStore((state) => state.hasIncompleteSession);
  const storeRestoreSession = useGrammarStore((state) => state.restoreSession);
  const storeClearSession = useGrammarStore((state) => state.clearSession);
  const storeGetSessionAge = useGrammarStore((state) => state.getSessionAge);
  // Local state
  const [isRestoring, setIsRestoring] = useState(false);
  const [showRestorePrompt, setShowRestorePrompt] = useState(false);
  const [dismissed, setDismissed] = useState(false);

  // Check for incomplete session on mount
  useEffect(() => {
    const hasIncomplete = storeHasIncomplete();
    const sessionAge = storeGetSessionAge();

    if (hasIncomplete && !dismissed) {
      // Check if session is expired (> 24 hours)
      if (sessionAge !== null && sessionAge > 24) {
        storeClearSession();
        onSessionExpired?.();
        return;
      }

      // Show restore prompt immediately (don't block on validation)
      // Validation will happen when user clicks "Resume Session"
      if (autoRestore) {
        // Auto-restore the session
        const session = storeRestoreSession();
        if (session) {
          onSessionRestored?.(session);
        }
      } else {
        // Show restore prompt
        setShowRestorePrompt(true);
      }
    }
  }, [
    storeHasIncomplete,
    storeGetSessionAge,
    storeRestoreSession,
    storeClearSession,
    autoRestore,
    dismissed,
    onSessionRestored,
    onSessionExpired,
  ]);

  const restoreSession = useCallback((): GrammarSessionData | null => {
    setIsRestoring(true);
    try {
      const session = storeRestoreSession();
      if (session) {
        setShowRestorePrompt(false);
        onSessionRestored?.(session);
        return session;
      }
      return null;
    } finally {
      setIsRestoring(false);
    }
  }, [storeRestoreSession, onSessionRestored]);

  const clearSession = useCallback(() => {
    storeClearSession();
    setShowRestorePrompt(false);
    setDismissed(true);
  }, [storeClearSession]);

  const dismissRestore = useCallback(() => {
    setShowRestorePrompt(false);
    setDismissed(true);
  }, []);

  return {
    hasIncompleteSession: storeHasIncomplete() && !dismissed,
    sessionAge: storeGetSessionAge(),
    isRestoring,
    restoreSession,
    clearSession,
    dismissRestore,
    showRestorePrompt,
  };
}

/**
 * Hook for auto-saving session progress.
 *
 * This is a lighter hook that just handles the auto-save aspect,
 * useful when you want to save progress without the restore prompt logic.
 */
export function useAutoSaveSession() {
  const saveSessionProgress = useGrammarStore((state) => state.saveSessionProgress);
  const currentSession = useGrammarStore((state) => state.currentSession);

  // Auto-save on session changes
  useEffect(() => {
    if (currentSession) {
      saveSessionProgress();
    }
  }, [currentSession, saveSessionProgress]);

  return { saveSessionProgress };
}

/**
 * Hook for tracking session time, accounting for pauses.
 */
export function useSessionTimer() {
  const currentSession = useGrammarStore((state) => state.currentSession);
  const sessionState = useGrammarStore((state) => state.sessionState);
  const [elapsedTime, setElapsedTime] = useState(0);

  useEffect(() => {
    if (!currentSession || sessionState === 'paused' || sessionState === 'completed') {
      return;
    }

    const updateTime = () => {
      const now = Date.now();
      const rawElapsed = now - currentSession.startTime;
      const adjustedElapsed = rawElapsed - currentSession.totalPausedTime;
      setElapsedTime(Math.floor(adjustedElapsed / 1000));
    };

    // Update immediately
    updateTime();

    // Update every second
    const timer = setInterval(updateTime, 1000);

    return () => clearInterval(timer);
  }, [currentSession, sessionState]);

  const formatTime = (seconds: number): string => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return {
    elapsedSeconds: elapsedTime,
    elapsedFormatted: formatTime(elapsedTime),
    isPaused: sessionState === 'paused',
  };
}
