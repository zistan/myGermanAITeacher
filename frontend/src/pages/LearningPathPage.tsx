import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Loading } from '../components/common';
import { FocusArea, DailyPlan, WeeklyGoals, RecommendedContext } from '../components/learning-path';
import integrationService from '../api/services/integrationService';
import { useNotificationStore } from '../store/notificationStore';
import type {
  LearningPath,
  DailyActivity,
  FocusArea as FocusAreaType,
  RecommendedContext as RecommendedContextType,
} from '../api/types/integration.types';
import type { ApiError } from '../api/types/common.types';

/**
 * LearningPathPage - Personalized learning recommendations and daily plan
 *
 * Displays a comprehensive learning path including:
 * - Daily study plan (75 minutes across all modules)
 * - Focus areas based on weak spots and error patterns
 * - Weekly goals with module distribution
 * - Recommended conversation contexts
 * - Motivational message
 */
export function LearningPathPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);
  const [learningPath, setLearningPath] = useState<LearningPath | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadLearningPath();
  }, []);

  const loadLearningPath = async () => {
    try {
      setIsLoading(true);
      const data = await integrationService.getLearningPath();
      setLearningPath(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load learning path', apiError.detail);
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartActivity = (activity: DailyActivity) => {
    // Navigate based on activity type
    if (activity.activity === 'vocabulary_review') {
      navigate('/vocabulary/flashcards');
    } else if (activity.activity === 'grammar_practice') {
      navigate('/grammar/practice');
    } else if (activity.activity === 'conversation') {
      navigate('/conversation/start');
    }
  };

  const handleStartFocusArea = (area: FocusAreaType) => {
    // Navigate based on module type
    if (area.module === 'grammar') {
      navigate('/grammar/practice');
    } else if (area.module === 'vocabulary') {
      navigate('/vocabulary/flashcards');
    } else if (area.module === 'conversation') {
      navigate('/conversation/start');
    }
  };

  const handleStartContext = (context: RecommendedContextType) => {
    navigate(`/conversation/start?context=${context.context_id}`);
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  if (!learningPath) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-xl font-semibold text-gray-900 mb-2">No learning path data available</h2>
          <p className="text-gray-600 mb-4">Please try refreshing the page.</p>
          <button
            onClick={loadLearningPath}
            className="px-6 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  // Sort focus areas by priority (critical > high > medium > low)
  const priorityOrder = { critical: 0, high: 1, medium: 2, low: 3 };
  const sortedFocusAreas = [...learningPath.focus_areas].sort(
    (a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]
  );

  // Format the generated_at timestamp
  const formattedDate = new Date(learningPath.generated_at).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Your Learning Path</h1>
        <div className="mt-3">
          <p className="text-lg text-gray-700 font-medium">{learningPath.motivation_message}</p>
          <p className="text-xs text-gray-500 mt-2">Last updated: {formattedDate}</p>
        </div>
      </div>

      {/* Daily Plan (Primary CTA) */}
      <div className="mb-8">
        <DailyPlan plan={learningPath.daily_plan} onStartActivity={handleStartActivity} />
      </div>

      {/* Two-column layout for focus areas and weekly goals */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
        {/* Focus Areas - Takes 2 columns */}
        {sortedFocusAreas.length > 0 && (
          <div className="lg:col-span-2">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Focus Areas</h2>
            <p className="text-sm text-gray-600 mb-4">
              Priority areas based on your progress and error patterns
            </p>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {sortedFocusAreas.map((area, index) => (
                <FocusArea key={index} area={area} onStartPractice={() => handleStartFocusArea(area)} />
              ))}
            </div>
          </div>
        )}

        {/* Weekly Goals - Takes 1 column */}
        <div className={sortedFocusAreas.length === 0 ? 'lg:col-span-3' : 'lg:col-span-1'}>
          <h2 className="text-xl font-bold text-gray-900 mb-4">Weekly Goals</h2>
          <WeeklyGoals plan={learningPath.weekly_plan} />
        </div>
      </div>

      {/* Recommended Contexts */}
      {learningPath.recommended_contexts.length > 0 && (
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Recommended Contexts</h2>
          <p className="text-sm text-gray-600 mb-4">
            Conversation scenarios to practice for well-rounded fluency
          </p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {learningPath.recommended_contexts.slice(0, 6).map((context) => (
              <RecommendedContext
                key={context.context_id}
                context={context}
                onStartConversation={() => handleStartContext(context)}
              />
            ))}
          </div>
          {learningPath.recommended_contexts.length > 6 && (
            <div className="mt-4 text-center">
              <button
                onClick={() => navigate('/conversation')}
                className="text-primary-600 hover:text-primary-700 font-medium text-sm"
              >
                View all {learningPath.recommended_contexts.length} contexts →
              </button>
            </div>
          )}
        </div>
      )}

      {/* Refresh Button */}
      <div className="text-center pt-4 border-t border-gray-200">
        <button
          onClick={loadLearningPath}
          disabled={isLoading}
          className="px-6 py-2 text-sm text-gray-600 hover:text-gray-900 border border-gray-300 rounded-lg hover:border-gray-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isLoading ? 'Refreshing...' : 'Refresh Learning Path'}
        </button>
        <p className="text-xs text-gray-500 mt-2">
          Your learning path adapts based on your latest progress
        </p>
      </div>
    </div>
  );
}
