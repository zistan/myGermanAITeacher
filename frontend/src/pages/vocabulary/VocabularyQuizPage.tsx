import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type {
  VocabularyQuizRequest,
  VocabularyQuizResponse,
} from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useVocabularyStore } from '../../store/vocabularyStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card } from '../../components/common';
import { QuizSetup, QuizQuestion, QuizFeedback, QuizResults } from '../../components/vocabulary';

interface QuizAnswer {
  questionId: string;
  userAnswer: string;
  isCorrect: boolean;
  correctAnswer: string;
  explanation: string;
  points: number;
}

export function VocabularyQuizPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const { quizState, setQuizState, categories, setCategories } = useVocabularyStore();

  // Local state
  const [quiz, setQuiz] = useState<VocabularyQuizResponse | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswer[]>([]);
  const [totalPoints, setTotalPoints] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [currentFeedback, setCurrentFeedback] = useState<QuizAnswer | null>(null);
  const [localState, setLocalState] = useState<'setup' | 'active' | 'feedback' | 'completed' | 'error'>('setup');

  // Load categories on mount
  useEffect(() => {
    loadCategories();

    // Cleanup on unmount
    return () => {
      setQuizState('idle');
    };
  }, []);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Don't intercept if user is typing in an input
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) {
        return;
      }

      if (localState === 'feedback') {
        // Space or Enter to continue
        if (e.key === ' ' || e.key === 'Enter') {
          e.preventDefault();
          handleNextQuestion();
        }
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [localState, currentQuestionIndex, quiz]);

  const loadCategories = async () => {
    try {
      const cats = await vocabularyService.getCategories();
      setCategories(cats);
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handleStartQuiz = async (request: VocabularyQuizRequest) => {
    setQuizState('loading');
    setLocalState('active');
    try {
      const quizData = await vocabularyService.generateQuiz(request);
      setQuiz(quizData);
      setCurrentQuestionIndex(0);
      setAnswers([]);
      setTotalPoints(0);
      setCurrentFeedback(null);
      setQuizState('active');
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to generate quiz', apiError.detail || 'An error occurred');
      setQuizState('error');
      setLocalState('error');
    }
  };

  const handleSubmitAnswer = async (userAnswer: string) => {
    if (!quiz || isSubmitting) return;

    const currentQuestion = quiz.questions[currentQuestionIndex];
    setIsSubmitting(true);

    try {
      const result = await vocabularyService.submitQuizAnswer(quiz.quiz_id, {
        question_id: currentQuestion.question_id,
        user_answer: userAnswer,
      });

      const answer: QuizAnswer = {
        questionId: currentQuestion.question_id,
        userAnswer,
        isCorrect: result.is_correct,
        correctAnswer: result.correct_answer,
        explanation: result.explanation,
        points: result.points_earned,
      };

      setAnswers((prev) => [...prev, answer]);
      setTotalPoints((prev) => prev + result.points_earned);
      setCurrentFeedback(answer);
      setLocalState('feedback');

      // Show streak notification
      if (result.is_correct) {
        const correctCount = answers.filter((a) => a.isCorrect).length + 1;
        if (correctCount >= 5 && correctCount % 5 === 0) {
          addToast('success', 'Great streak!', `${correctCount} correct answers!`);
        }
      }
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to submit answer', apiError.detail || 'An error occurred');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleNextQuestion = async () => {
    if (!quiz) return;

    const nextIndex = currentQuestionIndex + 1;
    if (nextIndex >= quiz.questions.length) {
      // Quiz is complete - mark it as completed in the database
      try {
        await vocabularyService.completeQuiz(quiz.quiz_id);
        console.log('[Quiz] Marked quiz as completed in database');
      } catch (error) {
        const apiError = error as ApiError;
        console.error('[Quiz] Failed to mark quiz as completed:', apiError);
        // Don't block UI - show warning but still display results
        addToast('warning', 'Quiz completed', 'Unable to save completion status');
      }

      setLocalState('completed');
      setQuizState('completed');
    } else {
      setCurrentQuestionIndex(nextIndex);
      setCurrentFeedback(null);
      setLocalState('active');
    }
  };

  const handleStartNewQuiz = () => {
    setQuiz(null);
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setTotalPoints(0);
    setCurrentFeedback(null);
    setLocalState('setup');
    setQuizState('idle');
  };

  const handleViewProgress = () => {
    navigate('/vocabulary/progress');
  };

  const handleBackToBrowser = () => {
    navigate('/vocabulary');
  };

  // Render based on state
  if (localState === 'active' && !quiz) {
    return <Loading fullScreen />;
  }

  if (localState === 'error') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">⚠️</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">Failed to generate quiz</h2>
            <p className="text-gray-600 mb-4">Please try again or check your connection</p>
            <div className="flex gap-3 justify-center">
              <Button onClick={handleStartNewQuiz} variant="primary">
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

  if (localState === 'setup') {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <QuizSetup
          categories={categories}
          onStart={handleStartQuiz}
          isLoading={quizState === 'loading'}
        />
      </div>
    );
  }

  if (localState === 'completed' && quiz) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <QuizResults
          totalQuestions={quiz.questions.length}
          correctAnswers={answers.filter((a) => a.isCorrect).length}
          totalPoints={totalPoints}
          answers={answers}
          onStartNew={handleStartNewQuiz}
          onViewProgress={handleViewProgress}
          onBackToBrowser={handleBackToBrowser}
        />
      </div>
    );
  }

  if (localState === 'feedback' && currentFeedback) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-8">
        <QuizFeedback
          isCorrect={currentFeedback.isCorrect}
          userAnswer={currentFeedback.userAnswer}
          correctAnswer={currentFeedback.correctAnswer}
          explanation={currentFeedback.explanation}
          pointsEarned={currentFeedback.points}
          onNext={handleNextQuestion}
        />
      </div>
    );
  }

  // Active quiz state
  if (!quiz || !quiz.questions[currentQuestionIndex]) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Header with end button */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-gray-900">Vocabulary Quiz</h1>
          <p className="text-sm text-gray-500">
            {answers.filter((a) => a.isCorrect).length} correct • {totalPoints} points
          </p>
        </div>
        <Button
          onClick={async () => {
            if (confirm('Are you sure you want to end this quiz?')) {
              // Mark quiz as completed in database
              try {
                await vocabularyService.completeQuiz(quiz.quiz_id);
                console.log('[Quiz] Marked quiz as completed in database (early end)');
              } catch (error) {
                const apiError = error as ApiError;
                console.error('[Quiz] Failed to mark quiz as completed:', apiError);
              }

              setLocalState('completed');
              setQuizState('completed');
            }
          }}
          variant="ghost"
          size="sm"
          data-testid="end-quiz-btn"
        >
          End Quiz
        </Button>
      </div>

      <QuizQuestion
        question={quiz.questions[currentQuestionIndex]}
        questionNumber={currentQuestionIndex + 1}
        totalQuestions={quiz.questions.length}
        onSubmit={handleSubmitAnswer}
        isSubmitting={isSubmitting}
      />
    </div>
  );
}
