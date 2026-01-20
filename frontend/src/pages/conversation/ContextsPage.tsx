import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, Filter } from 'lucide-react';
import { useConversationStore } from '../../store/conversationStore';
import { ContextCard } from '../../components/conversation';

export function ContextsPage() {
  const navigate = useNavigate();
  const { availableContexts, isLoadingContexts, loadContexts } = useConversationStore();

  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState<string>('');
  const [difficultyFilter, setDifficultyFilter] = useState<string>('');

  /**
   * Load contexts on mount
   */
  useEffect(() => {
    loadContexts();
  }, [loadContexts]);

  /**
   * Handle context selection
   */
  const handleSelectContext = (contextId: number) => {
    navigate(`/conversation/practice?context=${contextId}`);
  };

  /**
   * Filter contexts based on search and filters
   */
  const filteredContexts = availableContexts.filter((context) => {
    const matchesSearch =
      !searchQuery ||
      context.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      context.description.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesCategory = !categoryFilter || context.category === categoryFilter;
    const matchesDifficulty =
      !difficultyFilter || context.difficulty_level === difficultyFilter;

    return matchesSearch && matchesCategory && matchesDifficulty;
  });

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Conversation Practice
          </h1>
          <p className="mt-2 text-gray-600">
            Choose a context to start practicing your German conversation skills
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search contexts..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Category filter */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={categoryFilter}
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
              >
                <option value="">All Categories</option>
                <option value="business">Business</option>
                <option value="daily">Daily Life</option>
                <option value="custom">Custom</option>
              </select>
            </div>

            {/* Difficulty filter */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={difficultyFilter}
                onChange={(e) => setDifficultyFilter(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
              >
                <option value="">All Levels</option>
                <option value="A1">A1 - Beginner</option>
                <option value="A2">A2 - Elementary</option>
                <option value="B1">B1 - Intermediate</option>
                <option value="B2">B2 - Upper Intermediate</option>
                <option value="C1">C1 - Advanced</option>
                <option value="C2">C2 - Proficiency</option>
              </select>
            </div>
          </div>
        </div>

        {/* Contexts Grid */}
        {isLoadingContexts ? (
          <LoadingState />
        ) : filteredContexts.length === 0 ? (
          <EmptyState hasFilters={Boolean(searchQuery || categoryFilter || difficultyFilter)} />
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredContexts.map((context) => (
              <ContextCard
                key={context.id}
                context={context}
                onSelect={handleSelectContext}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function LoadingState() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {[1, 2, 3, 4, 5, 6].map((i) => (
        <div
          key={i}
          className="bg-gray-100 rounded-lg h-64 animate-pulse"
        ></div>
      ))}
    </div>
  );
}

interface EmptyStateProps {
  hasFilters: boolean;
}

function EmptyState({ hasFilters }: EmptyStateProps) {
  return (
    <div className="text-center py-12">
      <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
        <Search className="h-8 w-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {hasFilters ? 'No contexts found' : 'No contexts available'}
      </h3>
      <p className="text-gray-600 max-w-md mx-auto">
        {hasFilters
          ? 'Try adjusting your filters to see more contexts.'
          : 'There are no conversation contexts available at the moment.'}
      </p>
    </div>
  );
}
