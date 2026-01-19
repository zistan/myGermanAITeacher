import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type { StartFlashcardSessionRequest } from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useVocabularyStore } from '../../store/vocabularyStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card } from '../../components/common';
import {
  FlashcardDisplay,
  FlashcardControls,
  FlashcardSessionSetup,
  FlashcardSessionSummary,
} from '../../components/vocabulary';

export function FlashcardSessionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const {
    flashcardState,
    setFlashcardState,
    flashcardSession,
    startFlashcardSession,
    updateFlashcardCard,
    flipCard,
    recordFlashcardAnswer,
    completeFlashcardSession,
    resetFlashcardSession,
    categories,
    setCategories,
  } = useVocabularyStore();

  // Local state
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [cardStartTime, setCardStartTime] = useState<number>(Date.now());

  // Load categories on mount
  useEffect(() => {
    loadCategories();

    // Check for URL params (e.g., word_ids)
    const wordIdsParam = searchParams.get('word_ids');
    if (wordIdsParam) {
      // Auto-start session with specific words
      const wordIds = wordIdsParam.split(',').map(Number);
      handleStartSession({ word_ids: wordIds, card_count: wordIds.length });
    } else {
      // Show setup screen
      setFlashcardState('setup');
    }

    // Cleanup on unmount
    return () => {
      resetFlashcardSession();
    };
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Don't intercept if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      if (flashcardState === 'active') {
        // Space to flip
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          flipCard();
        }
        // Escape to end session
        if (e.key === 'Escape') {
          handleEndSession();
        }
      }

      if (flashcardState === 'flipped') {
        // Number keys 1-5 to rate
        const num = parseInt(e.key);
        if (num >= 1 && num <= 5) {
          e.preventDefault();
          handleRate(num as 1 | 2 | 3 | 4 | 5);
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [flashcardState, flashcardSession]);

  const loadCategories = async () => {
    try {
      const cats = await vocabularyService.getCategories();
      setCategories(cats);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handleStartSession = async (request: StartFlashcardSessionRequest) => {
    setFlashcardState('loading');
    try {
      const session = await vocabularyService.startFlashcardSession(request);
      setSessionId(session.session_id);
      startFlashcardSession(session);
      setCardStartTime(Date.now());
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to start session', apiError.detail || 'An error occurred');
      setFlashcardState('error');
    }
  };

  const handleRate = async (confidence: 1 | 2 | 3 | 4 | 5) => {
    if (!sessionId || !flashcardSession?.currentCard || isSubmitting) return;

    setIsSubmitting(true);
    try {
      const timeSpent = Math.floor((Date.now() - cardStartTime) / 1000);

      const result = await vocabularyService.submitFlashcardAnswer(sessionId, {
        card_id: flashcardSession.currentCard.card_id,
        user_answer: '', // User self-rated, no explicit answer
        confidence_level: confidence,
        time_spent_seconds: timeSpent,
      });

      // Record answer (confidence >= 3 is considered "correct" for stats)
      recordFlashcardAnswer(confidence >= 3);

      // Check for streak milestone
      if (confidence >= 3 && flashcardSession.correctCount + 1 >= 5 && (flashcardSession.correctCount + 1) % 5 === 0) {
        addToast('success', 'Great streak!', `${flashcardSession.correctCount + 1} cards mastered!`);
      }

      if (result.next_card) {
        // Move to next card
        updateFlashcardCard(result.next_card, flashcardSession.currentCardNumber + 1);
        setCardStartTime(Date.now());
      } else {
        // Session complete
        completeFlashcardSession();
      }
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to submit answer', apiError.detail || 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleEndSession = () => {
    if (flashcardSession) {
      completeFlashcardSession();
    } else {
      navigate('/vocabulary');
    }
  };

  const handleStartNewSession = () => {
    resetFlashcardSession();
    setSessionId(null);
    setFlashcardState('setup');
  };

  const handleViewProgress = () => {
    navigate('/vocabulary/progress');
  };

  const handleBackToBrowser = () => {
    resetFlashcardSession();
    navigate('/vocabulary');
  };

  // Render based on state
  if (flashcardState === 'loading') {
    return <Loading fullScreen />;
  }

  if (flashcardState === 'error') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Failed to start session</h2>
            <p className="text-gray-600 mb-4">Please try again or check your connection</p>
            <div className="flex gap-3 justify-center">
              <Button onClick={handleStartNewSession} variant="primary">
                Try Again
              </Button>
              <Button onClick={() => navigate('/vocabulary')} variant="secondary">
                Back to Vocabulary
              </Button>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  if (flashcardState === 'setup' || flashcardState === 'idle') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <FlashcardSessionSetup
          categories={categories}
          onStart={handleStartSession}
          isLoading={false}
        />
      </div>
    );
  }

  if (flashcardState === 'completed' && flashcardSession) {
    const sessionDuration = Math.floor((Date.now() - flashcardSession.startTime) / 1000);

    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <FlashcardSessionSummary
          totalCards={flashcardSession.totalCards}
          correctCount={flashcardSession.correctCount}
          incorrectCount={flashcardSession.incorrectCount}
          sessionDuration={sessionDuration}
          onStartNew={handleStartNewSession}
          onViewProgress={handleViewProgress}
          onBackToBrowser={handleBackToBrowser}
        />
      </div>
    );
  }

  // Active session states: 'active', 'flipped', 'rating'
  if (!flashcardSession?.currentCard) {
    return <Loading fullScreen />;
  }

  const isFlipped = flashcardState === 'flipped' || flashcardState === 'rating';

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Session Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Flashcard Session</h1>
          <p className="text-sm text-gray-500">
            Card {flashcardSession.currentCardNumber} of {flashcardSession.totalCards}
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm text-gray-600">
            <span className="text-green-600 font-medium">{flashcardSession.correctCount}</span>
            {' / '}
            <span className="text-red-600 font-medium">{flashcardSession.incorrectCount}</span>
          </div>
          <Button onClick={handleEndSession} variant="ghost" size="sm" data-testid="end-session-btn">
            End Session
          </Button>
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-2 mb-8">
        <div
          className="bg-primary-600 h-2 rounded-full transition-all duration-300"
          style={{
            width: `${(flashcardSession.currentCardNumber / flashcardSession.totalCards) * 100}%`,
          }}
        />
      </div>

      {/* Flashcard */}
      <div className="mb-8">
        <FlashcardDisplay
          card={flashcardSession.currentCard}
          isFlipped={isFlipped}
          onFlip={flipCard}
        />
      </div>

      {/* Controls */}
      {isFlipped ? (
        <FlashcardControls onRate={handleRate} disabled={isSubmitting} />
      ) : (
        <div className="text-center">
          <Button
            onClick={flipCard}
            variant="primary"
            size="lg"
            data-testid="show-answer-btn"
          >
            Show Answer
          </Button>
          <p className="text-sm text-gray-400 mt-3">
            Or press <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs">Space</kbd> to flip
          </p>
        </div>
      )}
    </div>
  );
}
