import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import grammarService from '../../api/services/grammarService';
import type { GrammarTopic } from '../../api/types/grammar.types';
import type { DifficultyLevel } from '../../api/types/common.types';
import { Card, Badge, Button, Loading } from '../../components/common';
import { useNotificationStore } from '../../store/notificationStore';
import type { ApiError } from '../../api/types/common.types';

export function GrammarTopicsPage() {
  const navigate = useNavigate();
  const addToast = useNotificationStore((state) => state.addToast);

  const [topics, setTopics] = useState<GrammarTopic[]>([]);
  const [filteredTopics, setFilteredTopics] = useState<GrammarTopic[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Filters
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedDifficulty, setSelectedDifficulty] = useState<DifficultyLevel | 'all'>('all');
  const [searchQuery, setSearchQuery] = useState('');

  // Get unique categories
  const categories = ['all', ...Array.from(new Set(topics.map((t) => t.category)))];

  useEffect(() => {
    loadTopics();
  }, []);

  useEffect(() => {
    filterTopics();
  }, [topics, selectedCategory, selectedDifficulty, searchQuery]);

  const loadTopics = async () => {
    setIsLoading(true);
    try {
      const data = await grammarService.getTopics();
      setTopics(data);
    } catch (error) {
      const apiError = error as ApiError;
      addToast('error', 'Failed to load topics', apiError.detail);
    } finally {
      setIsLoading(false);
    }
  };

  const filterTopics = () => {
    let filtered = [...topics];

    // Category filter
    if (selectedCategory !== 'all') {
      filtered = filtered.filter((t) => t.category === selectedCategory);
    }

    // Difficulty filter
    if (selectedDifficulty !== 'all') {
      filtered = filtered.filter((t) => t.difficulty_level === selectedDifficulty);
    }

    // Search filter
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(
        (t) =>
          t.name_en.toLowerCase().includes(query) ||
          t.name_de.toLowerCase().includes(query) ||
          t.description_de.toLowerCase().includes(query)
      );
    }

    setFilteredTopics(filtered);
  };

  const handleStartPractice = (topicId: number) => {
    navigate(`/grammar/practice?topics=${topicId}`);
  };

  const handleStartMixedPractice = () => {
    navigate('/grammar/practice');
  };

  if (isLoading) {
    return <Loading fullScreen />;
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Grammar Topics</h1>
          <p className="mt-2 text-gray-600">
            {filteredTopics.length} topic{filteredTopics.length !== 1 ? 's' : ''} available
          </p>
        </div>
        <Button onClick={handleStartMixedPractice} variant="primary">
          Start Mixed Practice
        </Button>
      </div>

      {/* Filters */}
      <Card className="mb-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Search */}
          <div>
            <label htmlFor="search" className="block text-sm font-medium text-gray-700 mb-1">
              Search
            </label>
            <input
              id="search"
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search topics..."
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            />
          </div>

          {/* Category filter */}
          <div>
            <label htmlFor="category" className="block text-sm font-medium text-gray-700 mb-1">
              Category
            </label>
            <select
              id="category"
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat.charAt(0).toUpperCase() + cat.slice(1)}
                </option>
              ))}
            </select>
          </div>

          {/* Difficulty filter */}
          <div>
            <label
              htmlFor="difficulty"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Difficulty
            </label>
            <select
              id="difficulty"
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value as DifficultyLevel | 'all')}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="all">All Levels</option>
              <option value="A1">A1 - Beginner</option>
              <option value="A2">A2 - Elementary</option>
              <option value="B1">B1 - Intermediate</option>
              <option value="B2">B2 - Upper Intermediate</option>
              <option value="C1">C1 - Advanced</option>
              <option value="C2">C2 - Mastery</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Topics Grid */}
      {filteredTopics.length === 0 ? (
        <Card>
          <div className="text-center py-12">
            <div className="text-4xl mb-4">📚</div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">No topics found</h3>
            <p className="text-gray-600">Try adjusting your filters</p>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTopics.map((topic) => (
            <Card key={topic.id} className="hover:shadow-lg transition-shadow">
              {/* Header */}
              <div className="mb-4">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-lg font-semibold text-gray-900">{topic.name_en}</h3>
                  <Badge variant="info" size="sm">
                    {topic.difficulty_level}
                  </Badge>
                </div>
                <p className="text-sm text-gray-600">{topic.name_de}</p>
              </div>

              {/* Description */}
              <p className="text-sm text-gray-700 mb-4 line-clamp-3">{topic.description_de}</p>

              {/* Category */}
              <div className="mb-4">
                <Badge variant="gray" size="sm">
                  {topic.category}
                </Badge>
              </div>

              {/* Action */}
              <Button
                onClick={() => handleStartPractice(topic.id)}
                variant="primary"
                size="sm"
                fullWidth
              >
                Practice This Topic
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
