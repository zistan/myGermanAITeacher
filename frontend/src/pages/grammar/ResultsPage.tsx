import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type { EndSessionResponse } from '../../api/types/grammar.types';
import { useGrammarStore } from '../../store/grammarStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card, Badge, ProgressBar } from '../../components/common';

interface LocationState {
  results?: EndSessionResponse;
}

export function ResultsPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const addToast = useNotificationStore((state) => state.addToast);

  // Get results from navigation state
  const locationState = location.state as LocationState | null;
  const results = locationState?.results;

  // Store state
  const { bookmarkedExercises, sessionNotes, clearSession } = useGrammarStore();

  // Local state
  const [recommendations, setRecommendations] = useState<any>(null);
  const [isLoadingRecs, setIsLoadingRecs] = useState(false);

  useEffect(() => {
    // If no results or invalid results structure, redirect to grammar page
    if (!results || typeof results.accuracy_percentage === 'undefined') {
      console.error('Invalid results structure:', results);
      addToast('error', 'Invalid session results', 'Unable to display results. Please try again.');
      navigate('/grammar');
      return;
    }

    // Load recommendations (commented out - endpoint doesn't exist)
    // loadRecommendations();

    // Clear session from store after results are shown
    return () => {
      clearSession();
    };
  }, [results, navigate, clearSession, addToast]);

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

  const handlePracticeAgain = () => {
    navigate('/grammar/practice');
  };

  const handlePracticeTopics = (topicIds: number[]) => {
    if (topicIds.length === 0) return;
    const params = topicIds.join(',');
    navigate(`/grammar/practice?topics=${params}`);
  };

  const handleViewProgress = () => {
    navigate('/grammar/progress');
  };

  const handleBrowseTopics = () => {
    navigate('/grammar');
  };

  const getScoreColor = (accuracy: number): string => {
    if (accuracy >= 80) return 'text-green-600';
    if (accuracy >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreEmoji = (accuracy: number): string => {
    if (accuracy >= 90) return '🏆';
    if (accuracy >= 80) return '🌟';
    if (accuracy >= 70) return '👍';
    if (accuracy >= 60) return '📚';
    return '💪';
  };

  const getScoreMessage = (accuracy: number): string => {
    if (accuracy >= 90) return 'Outstanding! You really know this material!';
    if (accuracy >= 80) return 'Great job! Keep up the excellent work!';
    if (accuracy >= 70) return 'Good progress! A bit more practice will help.';
    if (accuracy >= 60) return 'Nice effort! Review the topics you missed.';
    return "Keep practicing! Every session makes you stronger.";
  };

  // Get notes count
  const notesCount = Object.values(sessionNotes).filter(
    (note) => note.trim().length > 0
  ).length;

  if (!results) {
    return <Loading fullScreen />;
  }

  // Provide safe defaults for missing fields
  const safeResults = {
    session_id: results.session_id || 0,
    total_exercises: results.total_exercises || 0,
    exercises_correct: results.exercises_correct || 0,
    accuracy_percentage: results.accuracy_percentage ?? 0,
    total_points: results.total_points || 0,
    duration_minutes: results.duration_minutes || 0,
    topics_practiced: results.topics_practiced || [],
    improvements: results.improvements || [],
    next_recommended_topics: results.next_recommended_topics || [],
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      {/* Results Header */}
      <Card className="mb-6">
        <div className="text-center">
          <div className="text-6xl mb-4">{getScoreEmoji(safeResults.accuracy_percentage)}</div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Session Complete!</h1>
          <p className="text-lg text-gray-600">{getScoreMessage(safeResults.accuracy_percentage)}</p>
        </div>
      </Card>

      {/* Score Overview */}
      <Card className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Your Score</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {/* Accuracy */}
          <div className="text-center">
            <div className={`text-4xl font-bold ${getScoreColor(safeResults.accuracy_percentage)}`}>
              {safeResults.accuracy_percentage.toFixed(0)}%
            </div>
            <div className="text-sm text-gray-600">Accuracy</div>
          </div>

          {/* Correct */}
          <div className="text-center">
            <div className="text-4xl font-bold text-green-600">
              {safeResults.exercises_correct}
            </div>
            <div className="text-sm text-gray-600">Correct</div>
          </div>

          {/* Total */}
          <div className="text-center">
            <div className="text-4xl font-bold text-gray-700">
              {safeResults.total_exercises}
            </div>
            <div className="text-sm text-gray-600">Total</div>
          </div>

          {/* Points */}
          <div className="text-center">
            <div className="text-4xl font-bold text-primary-600">
              {safeResults.total_points}
            </div>
            <div className="text-sm text-gray-600">Points</div>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="mt-6">
          <ProgressBar
            value={safeResults.accuracy_percentage}
            color={
              safeResults.accuracy_percentage >= 80
                ? 'success'
                : safeResults.accuracy_percentage >= 60
                ? 'warning'
                : 'danger'
            }
            size="lg"
            showLabel
          />
        </div>
      </Card>

      {/* Session Details */}
      <Card className="mb-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Session Details</h2>
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">Duration</div>
            <div className="text-xl font-semibold text-gray-900">
              {safeResults.duration_minutes} minutes
            </div>
          </div>
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">Topics Practiced</div>
            <div className="text-xl font-semibold text-gray-900">
              {safeResults.topics_practiced.length}
            </div>
          </div>
        </div>

        {/* Topics List */}
        {safeResults.topics_practiced.length > 0 && (
          <div className="mt-4">
            <div className="text-sm font-medium text-gray-700 mb-2">Topics covered:</div>
            <div className="flex flex-wrap gap-2">
              {safeResults.topics_practiced.map((topic, index) => (
                <Badge key={index} variant="gray" size="sm">
                  {topic}
                </Badge>
              ))}
            </div>
          </div>
        )}
      </Card>

      {/* Improvements */}
      {safeResults.improvements && safeResults.improvements.length > 0 && (
        <Card className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">What You Improved</h2>
          <ul className="space-y-2">
            {safeResults.improvements.map((improvement, index) => (
              <li
                key={index}
                className="flex items-start p-3 bg-green-50 rounded-lg text-green-800"
              >
                <svg
                  className="w-5 h-5 mr-2 flex-shrink-0 text-green-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                {improvement}
              </li>
            ))}
          </ul>
        </Card>
      )}

      {/* Bookmarked Exercises */}
      {bookmarkedExercises.length > 0 && (
        <Card className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Bookmarked Exercises ({bookmarkedExercises.length})
          </h2>
          <p className="text-sm text-gray-600 mb-4">
            You bookmarked {bookmarkedExercises.length} exercises for later review.
          </p>
          <div className="flex flex-wrap gap-2">
            {bookmarkedExercises.map((exerciseId) => (
              <Badge key={exerciseId} variant="warning" size="sm">
                Exercise #{exerciseId}
              </Badge>
            ))}
          </div>
        </Card>
      )}

      {/* Session Notes */}
      {notesCount > 0 && (
        <Card className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Your Notes ({notesCount})
          </h2>
          <div className="space-y-3">
            {Object.entries(sessionNotes).map(([exerciseId, note]) => {
              if (!note.trim()) return null;
              return (
                <div
                  key={exerciseId}
                  className="p-3 bg-blue-50 rounded-lg border border-blue-200"
                >
                  <div className="text-xs text-blue-600 mb-1">Exercise #{exerciseId}</div>
                  <div className="text-sm text-gray-800 whitespace-pre-wrap">{note}</div>
                </div>
              );
            })}
          </div>
        </Card>
      )}

      {/* Recommendations */}
      {safeResults.next_recommended_topics && safeResults.next_recommended_topics.length > 0 && (
        <Card className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recommended Next</h2>
          <p className="text-sm text-gray-600 mb-4">
            Based on your performance, we recommend practicing these topics:
          </p>
          <div className="flex flex-wrap gap-3">
            {safeResults.next_recommended_topics.slice(0, 5).map((topicId) => (
              <Button
                key={topicId}
                onClick={() => handlePracticeTopics([topicId])}
                variant="secondary"
                size="sm"
              >
                Topic #{topicId}
              </Button>
            ))}
          </div>
          {safeResults.next_recommended_topics.length > 0 && (
            <div className="mt-4">
              <Button
                onClick={() => handlePracticeTopics(safeResults.next_recommended_topics)}
                variant="primary"
              >
                Practice All Recommended
              </Button>
            </div>
          )}
        </Card>
      )}

      {/* More Recommendations from API */}
      {recommendations && recommendations.recommended_topics && (
        <Card className="mb-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Keep Learning</h2>
          {isLoadingRecs ? (
            <div className="flex justify-center py-4">
              <Loading />
            </div>
          ) : (
            <div className="space-y-3">
              {recommendations.recommended_topics.slice(0, 3).map((topic: any, index: number) => (
                <div
                  key={topic.id || index}
                  className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                >
                  <div>
                    <div className="font-medium text-gray-900">
                      {topic.name_en || topic.name}
                    </div>
                    {topic.reason && (
                      <div className="text-xs text-gray-500">{topic.reason}</div>
                    )}
                  </div>
                  <Button
                    onClick={() => handlePracticeTopics([topic.id])}
                    variant="ghost"
                    size="sm"
                  >
                    Practice
                  </Button>
                </div>
              ))}
            </div>
          )}
        </Card>
      )}

      {/* Action Buttons */}
      <Card>
        <div className="flex flex-wrap gap-4 justify-center">
          <Button onClick={handlePracticeAgain} variant="primary" size="lg">
            Practice Again
          </Button>
          <Button onClick={handleViewProgress} variant="secondary" size="lg">
            View Progress
          </Button>
          <Button onClick={handleBrowseTopics} variant="ghost" size="lg">
            Browse Topics
          </Button>
        </div>
      </Card>
    </div>
  );
}
