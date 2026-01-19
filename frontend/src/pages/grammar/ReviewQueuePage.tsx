import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type { ReviewQueueItem } from '../../api/types/grammar.types';
import type { DifficultyLevel } from '../../api/types/common.types';
import type { ApiError } from '../../api/types/common.types';
import { useGrammarStore } from '../../store/grammarStore';
import { useNotificationStore } from '../../store/notificationStore';
import { Loading, Button, Card, Badge } from '../../components/common';
import clsx from 'clsx';

// Filter options
type PriorityFilter = 'all' | 'high' | 'medium' | 'low';
type CategoryFilter = 'all' | string;

export function ReviewQueuePage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  // Store state
  const {
    reviewQueue,
    setReviewQueue,
    isLoadingReviewQueue,
    setLoadingReviewQueue,
  } = useGrammarStore();

  // Local state
  const [categories, setCategories] = useState<string[]>([]);
  const [priorityFilter, setPriorityFilter] = useState<PriorityFilter>('all');
  const [categoryFilter, setCategoryFilter] = useState<CategoryFilter>('all');
  const [difficultyFilter, setDifficultyFilter] = useState<DifficultyLevel | 'all'>('all');

  useEffect(() => {
    loadReviewQueue();
    loadCategories();
  }, []);

  const loadReviewQueue = async () => {
    setLoadingReviewQueue(true);
    try {
      const data = await grammarService.getReviewQueue();
      setReviewQueue(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load review queue', apiError.detail || 'An error occurred');
    } finally {
      setLoadingReviewQueue(false);
    }
  };

  const loadCategories = async () => {
    try {
      const data = await grammarService.getCategories();
      setCategories(data.map((c) => c.name));
    } catch (error) {
      console.error('Failed to load categories:', error);
    }
  };

  const handlePracticeTopic = (topicId: number) => {
    navigate(`/grammar/practice?topics=${topicId}`);
  };

  const handlePracticeAllDue = () => {
    if (!reviewQueue || reviewQueue.items.length === 0) return;

    // Get filtered topic IDs
    const filteredItems = getFilteredItems();
    const topicIds = filteredItems.map((item) => item.topic_id).join(',');

    navigate(`/grammar/practice?topics=${topicIds}`);
  };

  const handlePracticeRecommended = () => {
    if (!reviewQueue) return;

    // Practice recommended session size
    const count = reviewQueue.recommended_session_size || 10;
    const items = getFilteredItems().slice(0, count);
    const topicIds = items.map((item) => item.topic_id).join(',');

    navigate(`/grammar/practice?topics=${topicIds}`);
  };

  const getFilteredItems = (): ReviewQueueItem[] => {
    if (!reviewQueue) return [];

    return reviewQueue.items.filter((item) => {
      // Priority filter
      if (priorityFilter !== 'all' && item.priority !== priorityFilter) {
        return false;
      }

      // Category filter
      if (categoryFilter !== 'all' && item.category !== categoryFilter) {
        return false;
      }

      // Difficulty filter
      if (difficultyFilter !== 'all' && item.difficulty_level !== difficultyFilter) {
        return false;
      }

      return true;
    });
  };

  const filteredItems = getFilteredItems();

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'danger';
      case 'medium':
        return 'warning';
      case 'low':
        return 'success';
      default:
        return 'gray';
    }
  };

  const formatDaysOverdue = (days: number): string => {
    if (days === 0) return 'Due today';
    if (days === 1) return '1 day overdue';
    if (days < 0) return `Due in ${Math.abs(days)} days`;
    return `${days} days overdue`;
  };

  if (isLoadingReviewQueue && !reviewQueue) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Review Queue</h1>
          <p className="mt-2 text-gray-600">Topics due for spaced repetition review</p>
        </div>
        <div className="flex flex-wrap gap-3">
          {reviewQueue && reviewQueue.items.length > 0 && (
            <>
              <Button
                onClick={handlePracticeRecommended}
                variant="primary"
                data-testid="practice-recommended-btn"
              >
                Practice ({reviewQueue.recommended_session_size || 10} topics)
              </Button>
              <Button
                onClick={handlePracticeAllDue}
                variant="secondary"
                data-testid="practice-all-btn"
              >
                Practice All Due ({filteredItems.length})
              </Button>
            </>
          )}
        </div>
      </div>

      {/* Stats Summary */}
      {reviewQueue && (
        <div className="mb-6">
          <Card>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary-600">
                  {reviewQueue.total_due}
                </div>
                <div className="text-sm text-gray-600">Total Due</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-red-600">
                  {reviewQueue.items.filter((i) => i.priority === 'high').length}
                </div>
                <div className="text-sm text-gray-600">High Priority</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">
                  {reviewQueue.items.filter((i) => i.priority === 'medium').length}
                </div>
                <div className="text-sm text-gray-600">Medium Priority</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">
                  {reviewQueue.items.filter((i) => i.priority === 'low').length}
                </div>
                <div className="text-sm text-gray-600">Low Priority</div>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Filters */}
      <div className="mb-6">
        <Card>
          <div className="flex flex-wrap gap-4">
            {/* Priority Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Priority
              </label>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value as PriorityFilter)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg bg-white focus:ring-primary-500 focus:border-primary-500"
                data-testid="priority-filter"
              >
                <option value="all">All Priorities</option>
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
              </select>
            </div>

            {/* Category Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Category
              </label>
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg bg-white focus:ring-primary-500 focus:border-primary-500"
                data-testid="category-filter"
              >
                <option value="all">All Categories</option>
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>

            {/* Difficulty Filter */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Difficulty
              </label>
              <select
                value={difficultyFilter}
                onChange={(e) =>
                  setDifficultyFilter(e.target.value as DifficultyLevel | 'all')
                }
                className="block w-full px-3 py-2 border border-gray-300 rounded-lg bg-white focus:ring-primary-500 focus:border-primary-500"
                data-testid="difficulty-filter"
              >
                <option value="all">All Levels</option>
                <option value="A1">A1</option>
                <option value="A2">A2</option>
                <option value="B1">B1</option>
                <option value="B2">B2</option>
                <option value="C1">C1</option>
                <option value="C2">C2</option>
              </select>
            </div>

            {/* Results Count */}
            <div className="flex items-end">
              <span className="text-sm text-gray-600">
                Showing {filteredItems.length} of {reviewQueue?.total_due || 0} topics
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Review Queue List */}
      {filteredItems.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">🎉</div>
            <h2 className="text-xl font-semibold text-gray-900 mb-2">
              {reviewQueue && reviewQueue.total_due === 0
                ? "You're all caught up!"
                : 'No matching topics'}
            </h2>
            <p className="text-gray-600 mb-6">
              {reviewQueue && reviewQueue.total_due === 0
                ? 'No topics are due for review right now. Great job staying on top of your practice!'
                : 'Try adjusting your filters to see more topics.'}
            </p>
            <div className="flex gap-3 justify-center">
              <Button onClick={() => navigate('/grammar')} variant="primary">
                Browse Topics
              </Button>
              <Button onClick={() => navigate('/grammar/progress')} variant="secondary">
                View Progress
              </Button>
            </div>
          </div>
        </Card>
      ) : (
        <div className="space-y-4">
          {filteredItems.map((item) => (
            <Card key={item.topic_id}>
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="font-semibold text-gray-900 truncate">
                      {item.topic_name}
                    </h3>
                    <Badge variant={getPriorityColor(item.priority)} size="sm">
                      {item.priority}
                    </Badge>
                  </div>
                  <div className="flex flex-wrap items-center gap-3 text-sm text-gray-600">
                    <span className="flex items-center gap-1">
                      <Badge variant="gray" size="sm">
                        {item.difficulty_level}
                      </Badge>
                    </span>
                    <span>{item.category}</span>
                    <span className="text-gray-400">|</span>
                    <span
                      className={clsx(
                        item.days_overdue > 0 ? 'text-red-600 font-medium' : 'text-gray-600'
                      )}
                    >
                      {formatDaysOverdue(item.days_overdue)}
                    </span>
                    <span className="text-gray-400">|</span>
                    <span>
                      Mastery: {((item.mastery_level / 5) * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="mt-2 text-xs text-gray-500">
                    Last practiced:{' '}
                    {new Date(item.last_practiced).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                    })}
                  </div>
                </div>
                <div className="ml-4">
                  <Button
                    onClick={() => handlePracticeTopic(item.topic_id)}
                    variant="primary"
                    size="sm"
                    data-testid={`practice-topic-${item.topic_id}`}
                  >
                    Practice
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Navigation */}
      <div className="mt-8">
        <Card>
          <div className="flex flex-wrap gap-4 justify-center">
            <Button onClick={() => navigate('/grammar')} variant="secondary">
              Browse All Topics
            </Button>
            <Button onClick={() => navigate('/grammar/progress')} variant="secondary">
              View Progress
            </Button>
            <Button onClick={loadReviewQueue} variant="ghost">
              Refresh Queue
            </Button>
          </div>
        </Card>
      </div>
    </div>
  );
}
