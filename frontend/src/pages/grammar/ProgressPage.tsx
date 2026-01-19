import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type { DifficultyLevel, ApiError } from '../../api/types/common.types';
import { useGrammarStore } from '../../store/grammarStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card, Badge, ProgressBar } from '../../components/common';

// CEFR levels for display
const CEFR_LEVELS: DifficultyLevel[] = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];

export function ProgressPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const {
    progressSummary,
    setProgressSummary,
    weakAreas,
    setWeakAreas,
    isLoadingProgress,
    setLoadingProgress,
  } = useGrammarStore();

  // Local state
  const [recommendations, setRecommendations] = useState<any>(null);
  const [isLoadingRecs, setIsLoadingRecs] = useState(false);

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    await Promise.all([loadProgress(), loadWeakAreas(), loadRecommendations()]);
  };

  const loadProgress = async () => {
    setLoadingProgress(true);
    try {
      const data = await grammarService.getProgressSummary();
      setProgressSummary(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load progress', apiError.detail || 'An error occurred');
    } finally {
      setLoadingProgress(false);
    }
  };

  const loadWeakAreas = async () => {
    try {
      const data = await grammarService.getWeakAreas();
      setWeakAreas(data);
    } catch (error) {
      console.error('Failed to load weak areas:', error);
    }
  };

  const loadRecommendations = async () => {
    setIsLoadingRecs(true);
    try {
      const data = await grammarService.getRecommendations();
      setRecommendations(data);
    } catch (error) {
      console.error('Failed to load recommendations:', error);
    } finally {
      setIsLoadingRecs(false);
    }
  };

  const handleStartPractice = (topicId?: number) => {
    const params = topicId ? `?topics=${topicId}` : '';
    navigate(`/grammar/practice${params}`);
  };

  const handleViewReviewQueue = () => {
    navigate('/grammar/review-queue');
  };

  if (isLoadingProgress && !progressSummary) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Grammar Progress</h1>
          <p className="mt-2 text-gray-600">Track your grammar mastery journey</p>
        </div>
        <div className="flex flex-wrap gap-3">
          <Button
            onClick={() => handleStartPractice()}
            variant="primary"
            data-testid="start-practice-btn"
          >
            Start Practice
          </Button>
          <Button
            onClick={handleViewReviewQueue}
            variant="secondary"
            data-testid="review-queue-btn"
          >
            Review Queue
          </Button>
        </div>
      </div>

      {/* Overview Stats */}
      {progressSummary && (
        <div className="mb-8">
          <Card>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Overview</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
              {/* Total Exercises */}
              <div className="text-center">
                <div className="text-3xl font-bold text-primary-600">
                  {progressSummary.total_exercises_completed}
                </div>
                <div className="text-sm text-gray-600">Exercises Completed</div>
              </div>

              {/* Overall Accuracy */}
              <div className="text-center">
                <div className="text-3xl font-bold text-green-600">
                  {progressSummary.overall_accuracy.toFixed(0)}%
                </div>
                <div className="text-sm text-gray-600">Overall Accuracy</div>
              </div>

              {/* Practice Time */}
              <div className="text-center">
                <div className="text-3xl font-bold text-blue-600">
                  {progressSummary.total_practice_time_minutes}
                </div>
                <div className="text-sm text-gray-600">Minutes Practiced</div>
              </div>

              {/* Current Streak */}
              <div className="text-center">
                <div className="text-3xl font-bold text-orange-600">
                  {progressSummary.current_streak_days > 0
                    ? `${progressSummary.current_streak_days}`
                    : '0'}
                </div>
                <div className="text-sm text-gray-600">Day Streak</div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Topic Mastery Overview */}
      {progressSummary && (
        <div className="mb-8">
          <Card>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Topic Mastery</h3>
            <div className="grid grid-cols-3 gap-4 mb-6">
              <div className="bg-green-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-700">
                  {progressSummary.topics_mastered}
                </div>
                <div className="text-sm text-green-600">Mastered</div>
              </div>
              <div className="bg-yellow-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-yellow-700">
                  {progressSummary.topics_in_progress}
                </div>
                <div className="text-sm text-yellow-600">In Progress</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-gray-700">
                  {progressSummary.topics_not_started}
                </div>
                <div className="text-sm text-gray-600">Not Started</div>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Overall Progress</span>
                <span className="font-medium">
                  {progressSummary.topics_mastered} /{' '}
                  {progressSummary.topics_mastered +
                    progressSummary.topics_in_progress +
                    progressSummary.topics_not_started}{' '}
                  topics
                </span>
              </div>
              <ProgressBar
                value={
                  (progressSummary.topics_mastered /
                    (progressSummary.topics_mastered +
                      progressSummary.topics_in_progress +
                      progressSummary.topics_not_started)) *
                  100
                }
                color="success"
                size="md"
              />
            </div>
          </Card>
        </div>
      )}

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-6">
          {/* CEFR Level Progress */}
          {progressSummary && progressSummary.level_progress && (
            <Card>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Progress by Level</h3>
              <div className="space-y-4">
                {CEFR_LEVELS.map((level) => {
                  const levelData = progressSummary.level_progress[level];
                  if (!levelData) return null;

                  const progress =
                    levelData.topics_total > 0
                      ? (levelData.topics_mastered / levelData.topics_total) * 100
                      : 0;

                  return (
                    <div key={level} className="space-y-2">
                      <div className="flex justify-between items-center">
                        <div className="flex items-center gap-2">
                          <Badge
                            variant={
                              level.startsWith('A')
                                ? 'success'
                                : level.startsWith('B')
                                ? 'warning'
                                : 'danger'
                            }
                            size="sm"
                          >
                            {level}
                          </Badge>
                          <span className="text-sm text-gray-600">
                            {levelData.topics_mastered}/{levelData.topics_total} topics
                          </span>
                        </div>
                        <span className="text-sm font-medium text-gray-900">
                          {levelData.accuracy.toFixed(0)}% accuracy
                        </span>
                      </div>
                      <ProgressBar
                        value={progress}
                        color={
                          progress >= 80 ? 'success' : progress >= 50 ? 'warning' : 'primary'
                        }
                        size="sm"
                      />
                    </div>
                  );
                })}
              </div>
            </Card>
          )}

          {/* Recent Activity */}
          {progressSummary && progressSummary.recent_activity && progressSummary.recent_activity.length > 0 && (
            <Card>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
              <div className="space-y-3">
                {progressSummary.recent_activity.slice(0, 7).map((activity, index) => (
                  <div
                    key={index}
                    className="flex justify-between items-center py-2 border-b border-gray-100 last:border-0"
                  >
                    <div className="text-sm text-gray-600">
                      {new Date(activity.date).toLocaleDateString('en-US', {
                        weekday: 'short',
                        month: 'short',
                        day: 'numeric',
                      })}
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-sm">
                        <span className="font-medium">{activity.exercises_completed}</span> exercises
                      </span>
                      <Badge
                        variant={
                          activity.accuracy >= 80
                            ? 'success'
                            : activity.accuracy >= 60
                            ? 'warning'
                            : 'danger'
                        }
                        size="sm"
                      >
                        {activity.accuracy.toFixed(0)}%
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          {/* Weak Areas */}
          {weakAreas && weakAreas.weak_topics && weakAreas.weak_topics.length > 0 && (
            <Card>
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-lg font-semibold text-gray-900">Areas to Improve</h3>
                <Badge variant="warning" size="sm">
                  {weakAreas.weak_topics.length} topics
                </Badge>
              </div>
              <div className="space-y-3">
                {weakAreas.weak_topics.slice(0, 5).map((topic) => (
                  <div
                    key={topic.topic.id}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                  >
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-gray-900 truncate">
                        {topic.topic.name_en}
                      </div>
                      <div className="flex items-center gap-2 mt-1">
                        <Badge variant="gray" size="sm">
                          {topic.topic.difficulty_level}
                        </Badge>
                        <span className="text-xs text-gray-500">
                          {topic.accuracy.toFixed(0)}% accuracy
                        </span>
                      </div>
                    </div>
                    <Button
                      onClick={() => handleStartPractice(topic.topic.id)}
                      variant="ghost"
                      size="sm"
                    >
                      Practice
                    </Button>
                  </div>
                ))}
              </div>
              {weakAreas.recommended_practice_plan && weakAreas.recommended_practice_plan.length > 0 && (
                <div className="mt-4 pt-4 border-t border-gray-200">
                  <div className="text-sm text-gray-600">
                    Estimated time to improve:{' '}
                    <span className="font-medium">{weakAreas.estimated_time_to_improve} days</span>
                  </div>
                </div>
              )}
            </Card>
          )}

          {/* Recommendations */}
          {recommendations && (
            <Card>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommendations</h3>
              {isLoadingRecs ? (
                <div className="flex justify-center py-4">
                  <Loading />
                </div>
              ) : recommendations.recommended_topics && recommendations.recommended_topics.length > 0 ? (
                <div className="space-y-3">
                  {recommendations.recommended_topics.slice(0, 5).map((topic: any, index: number) => (
                    <div
                      key={topic.id || index}
                      className="flex items-center justify-between p-3 bg-blue-50 rounded-lg"
                    >
                      <div className="flex-1">
                        <div className="font-medium text-gray-900">
                          {topic.name_en || topic.name}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">
                          {topic.reason || 'Suggested based on your progress'}
                        </div>
                      </div>
                      <Button
                        onClick={() => handleStartPractice(topic.id)}
                        variant="ghost"
                        size="sm"
                      >
                        Start
                      </Button>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-4 text-gray-500">
                  Complete more exercises to get personalized recommendations
                </div>
              )}
            </Card>
          )}
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8">
        <Card>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button
              onClick={() => navigate('/grammar')}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
              data-testid="browse-topics-btn"
            >
              <div className="text-2xl mb-2">📚</div>
              <div className="font-medium text-gray-900">Browse Topics</div>
              <div className="text-sm text-gray-500">View all topics</div>
            </button>
            <button
              onClick={handleViewReviewQueue}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
              data-testid="due-reviews-btn"
            >
              <div className="text-2xl mb-2">📋</div>
              <div className="font-medium text-gray-900">Due Reviews</div>
              <div className="text-sm text-gray-500">Spaced repetition</div>
            </button>
            <button
              onClick={() => handleStartPractice()}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
            >
              <div className="text-2xl mb-2">🎯</div>
              <div className="font-medium text-gray-900">Practice</div>
              <div className="text-sm text-gray-500">Start a session</div>
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors text-center"
            >
              <div className="text-2xl mb-2">📊</div>
              <div className="font-medium text-gray-900">Dashboard</div>
              <div className="text-sm text-gray-500">Overall progress</div>
            </button>
          </div>
        </Card>
      </div>
    </div>
  );
}
