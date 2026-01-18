import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type {
  GrammarExercise,
  PracticeSessionResponse,
  ExerciseFeedback,
  SessionProgress,
} from '../../api/types/grammar.types';
import { Loading, Button, Card, Badge } from '../../components/common';
import { useNotificationStore } from '../../store/notificationStore';
import type { ApiError } from '../../api/types/common.types';
import { ExerciseRenderer } from '../../components/grammar/ExerciseRenderer';
import { FeedbackDisplay } from '../../components/grammar/FeedbackDisplay';
import { SessionHeader } from '../../components/grammar/SessionHeader';

type SessionState = 'loading' | 'active' | 'feedback' | 'completed' | 'error';

export function PracticeSessionPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const addToast = useNotificationStore((state) => state.addToast);

  // Session data
  const [sessionState, setSessionState] = useState<SessionState>('loading');
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [sessionInfo, setSessionInfo] = useState<PracticeSessionResponse | null>(null);
  const [currentExercise, setCurrentExercise] = useState<GrammarExercise | null>(null);
  const [feedback, setFeedback] = useState<ExerciseFeedback | null>(null);
  const [progress, setProgress] = useState<SessionProgress | null>(null);

  // User input
  const [userAnswer, setUserAnswer] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Session metrics
  const [exerciseStartTime, setExerciseStartTime] = useState<number>(Date.now());
  const [currentStreak, setCurrentStreak] = useState(0);

  useEffect(() => {
    startSession();
  }, []);

  const startSession = async () => {
    setSessionState('loading');
    try {
      // Parse URL params
      const topicsParam = searchParams.get('topics');
      const difficultyParam = searchParams.get('difficulty');
      const countParam = searchParams.get('count');

      const topicIds = topicsParam ? topicsParam.split(',').map(Number) : undefined;

      // Start session
      const session = await grammarService.startPracticeSession({
        topic_ids: topicIds,
        difficulty_level: difficultyParam as any,
        exercise_count: countParam ? parseInt(countParam) : 10,
        use_spaced_repetition: true,
      });

      setSessionId(session.session_id);
      setSessionInfo(session);

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
      setCurrentExercise(exercise);
      setUserAnswer('');
      setFeedback(null);
      setSessionState('active');
      setExerciseStartTime(Date.now());
    } catch (error) {
      // No more exercises - session complete
      setSessionState('completed');
    }
  };

  const handleSubmitAnswer = async () => {
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

      // Update streak
      if (result.feedback.is_correct) {
        setCurrentStreak((prev) => prev + 1);
        if (currentStreak + 1 >= 5) {
          addToast('success', 'Amazing streak!', `${currentStreak + 1} correct answers in a row! 🔥`);
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
  };

  const handleNext = async () => {
    if (!sessionId) return;
    await loadNextExercise(sessionId);
  };

  const handleEndSession = async () => {
    if (!sessionId) return;

    try {
      const results = await grammarService.endPracticeSession(sessionId);
      navigate('/grammar/results', { state: { results } });
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to end session', apiError.detail);
    }
  };

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (sessionState === 'active') {
        // Enter to submit
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          handleSubmitAnswer();
        }
        // Esc to end session
        if (e.key === 'Escape') {
          handleEndSession();
        }
      }

      if (sessionState === 'feedback') {
        // Space or Enter to continue
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          handleNext();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [sessionState, userAnswer, sessionId]);

  if (sessionState === 'loading') {
    return <Loading fullScreen />;
  }

  if (sessionState === 'error') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Failed to start session</h2>
            <p className="text-gray-600 mb-4">Please try again</p>
            <Button onClick={() => navigate('/grammar')}>Back to Topics</Button>
          </div>
        </Card>
      </div>
    );
  }

  if (sessionState === 'completed') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">🎉</div>
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

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Session Header */}
      {sessionInfo && progress && (
        <SessionHeader
          sessionInfo={sessionInfo}
          progress={progress}
          currentStreak={currentStreak}
          onEndSession={handleEndSession}
        />
      )}

      {/* Exercise Card */}
      {currentExercise && (
        <Card className="mt-6">
          {/* Exercise Type Badge */}
          <div className="flex items-center justify-between mb-4">
            <Badge variant="info">{currentExercise.exercise_type.replace('_', ' ')}</Badge>
            <Badge variant="gray">{currentExercise.difficulty_level}</Badge>
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
            <FeedbackDisplay feedback={feedback} onNext={handleNext} />
          )}
        </Card>
      )}

      {/* Keyboard Shortcuts Helper */}
      <div className="mt-4 text-center text-sm text-gray-500">
        <span className="inline-flex items-center">
          {sessionState === 'active' && (
            <>
              <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs mr-2">
                Enter
              </kbd>
              Submit •
              <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs mx-2">
                Esc
              </kbd>
              End Session
            </>
          )}
          {sessionState === 'feedback' && (
            <>
              <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs mr-2">
                Space
              </kbd>
              or
              <kbd className="px-2 py-1 bg-gray-100 border border-gray-300 rounded text-xs mx-2">
                Enter
              </kbd>
              Continue
            </>
          )}
        </span>
      </div>
    </div>
  );
}
