import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import vocabularyService from '../../api/services/vocabularyService';
import type {
  VocabularyReviewQueueResponse,
  WordRecommendationResponse,
  VocabularyWithProgress,
} from '../../api/types/vocabulary.types';
import type { ApiError } from '../../api/types/common.types';
import { useVocabularyStore } from '../../store/vocabularyStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card } from '../../components/common';
import {
  ProgressOverview,
  MasteryChart,
  CategoryBreakdown,
  ReviewQueue,
  WordRecommendations,
} from '../../components/vocabulary';

export function VocabularyProgressPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const { progress, setProgress, isLoadingProgress, setLoadingProgress } = useVocabularyStore();

  // Local state
  const [reviewQueue, setReviewQueue] = useState<VocabularyReviewQueueResponse | null>(null);
  const [recommendations, setRecommendations] = useState<WordRecommendationResponse | null>(null);
  const [isLoadingQueue, setIsLoadingQueue] = useState(false);
  const [isLoadingRecs, setIsLoadingRecs] = useState(false);

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    await Promise.all([loadProgress(), loadReviewQueue(), loadRecommendations()]);
  };

  const loadProgress = async () => {
    setLoadingProgress(true);
    try {
      const data = await vocabularyService.getProgressSummary();
      setProgress(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load progress', apiError.detail || 'An error occurred');
    } finally {
      setLoadingProgress(false);
    }
  };

  const loadReviewQueue = async () => {
    setIsLoadingQueue(true);
    try {
      const data = await vocabularyService.getReviewQueue();
      setReviewQueue(data);
    } catch (error) {
      console.error('Failed to load review queue:', error);
    } finally {
      setIsLoadingQueue(false);
    }
  };

  const loadRecommendations = async () => {
    setIsLoadingRecs(true);
    try {
      const data = await vocabularyService.getRecommendations({
        recommendation_type: 'next_to_learn',
        count: 10,
      });
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setIsLoadingRecs(false);
    }
  };

  const handlePracticeWord = (word: VocabularyWithProgress) => {
    navigate(`/vocabulary/flashcards?word_ids=${word.id}`);
  };

  const handleStartFlashcards = () => {
    navigate('/vocabulary/flashcards');
  };

  const handleStartQuiz = () => {
    navigate('/vocabulary/quiz');
  };

  if (isLoadingProgress && !progress) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Vocabulary Progress</h1>
          <p className="mt-2 text-gray-600">Track your vocabulary learning journey</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button onClick={handleStartFlashcards} variant="primary" data-testid="start-flashcards-btn">
            Practice Flashcards
          </Button>
          <Button onClick={handleStartQuiz} variant="secondary" data-testid="start-quiz-btn">
            Take Quiz
          </Button>
        </div>
      </div>

      {/* Progress Overview */}
      {progress && (
        <div className="mb-8">
          <ProgressOverview progress={progress} />
        </div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-6">
          {/* Mastery Chart */}
          {progress && <MasteryChart progress={progress} />}

          {/* Category Breakdown */}
          {progress && <CategoryBreakdown progress={progress} />}
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Review Queue */}
          {reviewQueue ? (
            <ReviewQueue reviewQueue={reviewQueue} onPracticeWord={handlePracticeWord} />
          ) : isLoadingQueue ? (
            <Card>
              <div className="flex justify-center py-8">
                <Loading />
              </div>
            </Card>
          ) : null}

          {/* Recommendations */}
          <WordRecommendations
            recommendations={recommendations}
            isLoading={isLoadingRecs}
            onRefresh={loadRecommendations}
            onPracticeWord={handlePracticeWord}
          />
        </div>
      </div>

      {/* Level Distribution */}
      {progress && Object.keys(progress.words_by_level).length > 0 && (
        <div className="mt-8">
          <Card>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Words by CEFR Level</h3>
            <div className="grid grid-cols-3 md:grid-cols-6 gap-4">
              {['A1', 'A2', 'B1', 'B2', 'C1', 'C2'].map((level) => {
                const count = progress.words_by_level[level as keyof typeof progress.words_by_level] || 0;
                return (
                  <div key={level} className="text-center p-4 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-900">{count}</div>
                    <div className="text-sm text-gray-600">{level}</div>
                  </div>
                );
              })}
            </div>
          </Card>
        </div>
      )}

      {/* Quick Actions */}
      <div className="mt-8">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button
              onClick={() => navigate('/vocabulary')}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
              data-testid="browse-words-btn"
            >
              <div className="text-2xl mb-2">📚</div>
              <div className="font-medium text-gray-900">Browse Words</div>
              <div className="text-sm text-gray-500">View all vocabulary</div>
            </button>
            <button
              onClick={() => navigate('/vocabulary/lists')}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
              data-testid="my-lists-btn"
            >
              <div className="text-2xl mb-2">📋</div>
              <div className="font-medium text-gray-900">My Lists</div>
              <div className="text-sm text-gray-500">Manage word lists</div>
            </button>
            <button
              onClick={handleStartFlashcards}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
            >
              <div className="text-2xl mb-2">🃏</div>
              <div className="font-medium text-gray-900">Flashcards</div>
              <div className="text-sm text-gray-500">Practice with cards</div>
            </button>
            <button
              onClick={handleStartQuiz}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
            >
              <div className="text-2xl mb-2">❓</div>
              <div className="font-medium text-gray-900">Quiz</div>
              <div className="text-sm text-gray-500">Test your knowledge</div>
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
}
