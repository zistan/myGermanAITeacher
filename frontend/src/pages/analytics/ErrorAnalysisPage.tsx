/**
 * ErrorAnalysisPage
 * Displays error patterns, recurring mistakes, and improvement recommendations
 */

import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import clsx from 'clsx';
import { PieChart } from '../../components/analytics/charts/PieChart';
import { Loading } from '../../components/common/Loading';
import analyticsService from '../../api/services/analyticsService';
import type { ErrorPatternAnalysisResponse } from '../../api/types/analytics.types';

const SEVERITY_COLORS = {
  high: 'bg-red-50 border-red-500 text-red-700',
  medium: 'bg-yellow-50 border-yellow-500 text-yellow-700',
  low: 'bg-blue-50 border-blue-500 text-blue-700',
};

export function ErrorAnalysisPage() {
  const navigate = useNavigate();
  const [errorData, setErrorData] = useState<ErrorPatternAnalysisResponse | null>(null);
  const [selectedPeriod, setSelectedPeriod] = useState<7 | 30 | 90>(30);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadErrorAnalysis();
  }, [selectedPeriod]);

  const loadErrorAnalysis = async () => {
    try {
      setLoading(true);
      const data = await analyticsService.getErrorAnalysis(selectedPeriod);
      setErrorData(data);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load error analysis');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  if (!errorData) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No error analysis data available</p>
      </div>
    );
  }

  // Prepare chart data
  const chartData = errorData.top_error_topics.slice(0, 5).map((topic) => ({
    name: topic.topic,
    value: topic.count,
  }));

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Error Analysis</h1>
          <p className="mt-2 text-gray-600">
            Identify patterns and improve your weak areas
          </p>
        </div>
        <div className="flex space-x-2">
          {[7, 30, 90].map((days) => (
            <button
              key={days}
              onClick={() => setSelectedPeriod(days as 7 | 30 | 90)}
              className={clsx(
                'px-4 py-2 text-sm font-medium rounded-lg transition-colors',
                selectedPeriod === days
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              )}
            >
              {days} Days
            </button>
          ))}
        </div>
      </div>

      {/* Summary Card */}
      <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Summary</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <p className="text-sm text-gray-600">Total Errors</p>
            <p className="text-3xl font-bold text-gray-900 mt-1">{errorData.total_errors}</p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Most Common Topic</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {errorData.top_error_topics[0]?.topic || 'N/A'}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Improvement Trends</p>
            <p className="text-lg font-semibold text-gray-900 mt-1">
              {errorData.improvement_trends.filter((t) => t.trend === 'improving').length} improving
            </p>
          </div>
        </div>
      </div>

      {/* Error Distribution Chart */}
      {chartData.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Error Topics</h2>
          <PieChart data={chartData} height={300} showLegend />
        </div>
      )}

      {/* Recurring Mistakes */}
      {errorData.recurring_mistakes.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Recurring Mistakes</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {errorData.recurring_mistakes.map((mistake, index) => (
              <div
                key={index}
                className={clsx(
                  'border-2 rounded-lg p-4',
                  SEVERITY_COLORS[mistake.severity]
                )}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-medium">{mistake.topic_name}</h3>
                  <span className="px-2 py-1 text-xs font-medium rounded capitalize">
                    {mistake.severity}
                  </span>
                </div>
                <p className="text-sm mb-3">
                  <span className="font-semibold">{mistake.error_count}</span> errors in the last{' '}
                  {selectedPeriod} days
                </p>
                <button
                  onClick={() => navigate(`/grammar/practice?topics=${mistake.topic_id}`)}
                  className="w-full px-3 py-2 bg-white border border-current rounded-lg text-sm font-medium hover:bg-opacity-10 transition-colors"
                >
                  Practice This Topic
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Improvement Trends */}
      {errorData.improvement_trends.length > 0 && (
        <div className="bg-white rounded-lg shadow border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Improvement Trends</h2>
          <div className="space-y-3">
            {errorData.improvement_trends.map((trend, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
              >
                <div className="flex items-center space-x-3">
                  <span
                    className={clsx(
                      'text-2xl',
                      trend.trend === 'improving' ? 'text-green-600' : 'text-red-600'
                    )}
                  >
                    {trend.trend === 'improving' ? '↗' : '↘'}
                  </span>
                  <div>
                    <p className="font-medium text-gray-900">{trend.topic_name}</p>
                    <p className="text-sm text-gray-600">
                      {trend.improvement_percentage > 0 ? '+' : ''}
                      {trend.improvement_percentage.toFixed(0)}% change
                    </p>
                  </div>
                </div>
                <span
                  className={clsx(
                    'px-3 py-1 rounded-lg text-sm font-medium',
                    trend.trend === 'improving'
                      ? 'bg-green-100 text-green-700'
                      : 'bg-red-100 text-red-700'
                  )}
                >
                  {trend.trend}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* AI Recommendations */}
      {errorData.recommendations.length > 0 && (
        <div className="bg-gradient-to-r from-primary-500 to-primary-600 rounded-lg shadow p-6 text-white">
          <h2 className="text-lg font-semibold mb-4">AI Recommendations</h2>
          <ul className="space-y-2">
            {errorData.recommendations.map((recommendation, index) => (
              <li key={index} className="flex items-start space-x-2">
                <svg
                  className="w-5 h-5 mt-0.5 flex-shrink-0"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
                <span>{recommendation}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
