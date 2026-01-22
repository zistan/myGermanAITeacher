/**
 * ProgressOverviewPage
 * Displays comprehensive progress across all modules with trends and comparisons
 */

import { useEffect, useState } from 'react';
import toast from 'react-hot-toast';
import { StatCard } from '../../components/analytics/progress/StatCard';
import { ModuleStatsCard } from '../../components/analytics/progress/ModuleStatsCard';
import { ProgressChart } from '../../components/analytics/charts/ProgressChart';
import { Loading } from '../../components/common/Loading';
import analyticsService from '../../api/services/analyticsService';
import type {
  OverallProgressResponse,
  ProgressComparisonResponse,
} from '../../api/types/analytics.types';

export function ProgressOverviewPage() {
  const [overallProgress, setOverallProgress] = useState<OverallProgressResponse | null>(null);
  const [comparison, setComparison] = useState<ProgressComparisonResponse | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<7 | 30 | 90>(30);
  const [loading, setLoading] = useState(true);
  const [comparisonLoading, setComparisonLoading] = useState(false);

  // Load overall progress
  useEffect(() => {
    loadProgress();
  }, []);

  // Load comparison data when period changes
  useEffect(() => {
    if (overallProgress) {
      loadComparison();
    }
  }, [selectedPeriod]);

  const loadProgress = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getProgress();
      setOverallProgress(data);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load progress data');
    } finally {
      setLoading(false);
    }
  };

  const loadComparison = async () => {
    try {
      setComparisonLoading(true);
      const data = await analyticsService.getProgressComparison(selectedPeriod);
      setComparison(data);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load comparison data');
    } finally {
      setComparisonLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (!overallProgress) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No progress data available</p>
      </div>
    );
  }

  const { activity, conversation, grammar, vocabulary, weekly_goal_progress } = overallProgress;

  // Prepare chart data for comparison
  const chartData = comparison
    ? [
        {
          period: `Previous ${selectedPeriod}d`,
          sessions: comparison.previous_period.total_sessions,
          accuracy: comparison.previous_period.exercise_accuracy,
        },
        {
          period: `Current ${selectedPeriod}d`,
          sessions: comparison.current_period.total_sessions,
          accuracy: comparison.current_period.exercise_accuracy,
        },
      ]
    : [];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Progress Overview</h1>
        <p className="mt-2 text-gray-600">
          Track your learning journey across all modules
        </p>
      </div>

      {/* Overall Progress Card */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Overall Progress</h2>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-5xl font-bold text-primary-600">
              {overallProgress.overall_score}
            </div>
            <p className="text-sm text-gray-600 mt-1">Overall Score (0-100)</p>
          </div>
          <div className="w-32 h-32">
            {/* Circular progress gauge */}
            <svg className="transform -rotate-90" viewBox="0 0 120 120">
              <circle
                cx="60"
                cy="60"
                r="54"
                stroke="#e5e7eb"
                strokeWidth="8"
                fill="none"
              />
              <circle
                cx="60"
                cy="60"
                r="54"
                stroke="#3b82f6"
                strokeWidth="8"
                fill="none"
                strokeDasharray={`${(overallProgress.overall_score / 100) * 339.292} 339.292`}
                strokeLinecap="round"
              />
            </svg>
          </div>
        </div>
      </div>

      {/* Weekly Goal Progress */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Goal</h3>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm text-gray-600">
            {weekly_goal_progress.sessions_this_week} / {weekly_goal_progress.goal_sessions} sessions
          </span>
          <span className="text-sm font-medium text-gray-900">
            {weekly_goal_progress.goal_percentage}%
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className={`h-3 rounded-full transition-all ${
              weekly_goal_progress.goal_met ? 'bg-green-500' : 'bg-primary-500'
            }`}
            style={{ width: `${weekly_goal_progress.goal_percentage}%` }}
          />
        </div>
        {weekly_goal_progress.goal_met && (
          <p className="text-sm text-green-600 mt-2 font-medium">
            ✓ Weekly goal achieved!
          </p>
        )}
      </div>

      {/* Activity Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <StatCard
          label="Current Streak"
          value={`${activity.current_streak_days} days`}
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z"
                clipRule="evenodd"
              />
            </svg>
          }
          color="success"
        />
        <StatCard
          label="Longest Streak"
          value={`${activity.longest_streak_days} days`}
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
          }
          color="warning"
        />
        <StatCard
          label="Total Study Days"
          value={activity.total_study_days}
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z"
                clipRule="evenodd"
              />
            </svg>
          }
          color="primary"
        />
        <StatCard
          label="Avg Sessions/Week"
          value={activity.average_sessions_per_week.toFixed(1)}
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
          }
          color="primary"
        />
      </div>

      {/* Module Stats Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <ModuleStatsCard
          title="Conversation"
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path
                fillRule="evenodd"
                d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                clipRule="evenodd"
              />
            </svg>
          }
          stats={[
            { label: 'Sessions', value: conversation.total_sessions },
            { label: 'Messages', value: conversation.total_messages },
            { label: 'Contexts', value: conversation.unique_contexts_practiced },
            { label: 'Avg Duration', value: `${conversation.average_session_duration_minutes.toFixed(0)}m` },
          ]}
          linkTo="/conversation"
          color="blue"
        />

        <ModuleStatsCard
          title="Grammar"
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 4.804A7.968 7.968 0 005.5 4c-1.255 0-2.443.29-3.5.804v10A7.969 7.969 0 015.5 14c1.669 0 3.218.51 4.5 1.385A7.962 7.962 0 0114.5 14c1.255 0 2.443.29 3.5.804v-10A7.968 7.968 0 0014.5 4c-1.255 0-2.443.29-3.5.804V12a1 1 0 11-2 0V4.804z" />
            </svg>
          }
          stats={[
            { label: 'Topics Practiced', value: grammar.topics_practiced },
            { label: 'Topics Mastered', value: grammar.topics_mastered },
            { label: 'Exercises', value: grammar.total_exercises_attempted },
            { label: 'Accuracy', value: `${grammar.overall_accuracy_percentage.toFixed(0)}%` },
          ]}
          progressPercentage={Math.round((grammar.average_mastery_level / 5) * 100)}
          linkTo="/grammar"
          color="purple"
        />

        <ModuleStatsCard
          title="Vocabulary"
          icon={
            <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path d="M13 7H7v6h6V7z" />
              <path
                fillRule="evenodd"
                d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v2h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1H9v1a1 1 0 11-2 0v-1H5a2 2 0 01-2-2v-2H2a1 1 0 110-2h1V9H2a1 1 0 010-2h1V5a2 2 0 012-2h2V2zM5 5h10v10H5V5z"
                clipRule="evenodd"
              />
            </svg>
          }
          stats={[
            { label: 'Words Learned', value: vocabulary.total_words_learned },
            { label: 'Words Mastered', value: vocabulary.words_mastered },
            { label: 'Reviews', value: vocabulary.total_reviews },
            { label: 'Accuracy', value: `${vocabulary.overall_accuracy_percentage.toFixed(0)}%` },
          ]}
          progressPercentage={
            vocabulary.total_words_learned > 0
              ? Math.round((vocabulary.words_mastered / vocabulary.total_words_learned) * 100)
              : 0
          }
          linkTo="/vocabulary"
          color="green"
        />
      </div>

      {/* Progress Comparison */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-gray-900">Progress Trend</h2>
          <div className="flex space-x-2">
            {[7, 30, 90].map((days) => (
              <button
                key={days}
                onClick={() => setSelectedPeriod(days as 7 | 30 | 90)}
                className={`px-3 py-1 text-sm font-medium rounded-lg transition-colors ${
                  selectedPeriod === days
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {days}d
              </button>
            ))}
          </div>
        </div>

        {comparisonLoading ? (
          <div className="flex items-center justify-center h-64">
            <Loading />
          </div>
        ) : comparison && chartData.length > 0 ? (
          <div>
            <ProgressChart
              data={chartData}
              type="bar"
              xAxisKey="period"
              yAxisKey="sessions"
              color="#3b82f6"
              height={250}
            />
            <div className="grid grid-cols-3 gap-4 mt-4 pt-4 border-t border-gray-200">
              <div className="text-center">
                <p className="text-sm text-gray-600">Sessions Change</p>
                <p className={`text-lg font-bold ${
                  comparison.current_period.total_sessions >= comparison.previous_period.total_sessions
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}>
                  {comparison.current_period.total_sessions >= comparison.previous_period.total_sessions ? '+' : ''}
                  {comparison.current_period.total_sessions - comparison.previous_period.total_sessions}
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">Accuracy Change</p>
                <p className={`text-lg font-bold ${
                  comparison.current_period.exercise_accuracy >= comparison.previous_period.exercise_accuracy
                    ? 'text-green-600'
                    : 'text-red-600'
                }`}>
                  {comparison.current_period.exercise_accuracy >= comparison.previous_period.exercise_accuracy ? '+' : ''}
                  {(comparison.current_period.exercise_accuracy - comparison.previous_period.exercise_accuracy).toFixed(1)}%
                </p>
              </div>
              <div className="text-center">
                <p className="text-sm text-gray-600">Exercises Completed</p>
                <p className="text-lg font-bold text-gray-900">
                  {comparison.current_period.exercises_completed}
                </p>
              </div>
            </div>
          </div>
        ) : (
          <p className="text-center text-gray-600 py-12">No comparison data available</p>
        )}
      </div>
    </div>
  );
}
