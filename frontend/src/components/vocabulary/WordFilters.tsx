import type { DifficultyLevel, MasteryLevel } from '../../api/types/common.types';
import type { VocabularyFilters } from '../../api/types/vocabulary.types';

export interface WordFiltersProps {
  filters: VocabularyFilters;
  categories: string[];
  onFilterChange: (filters: Partial<VocabularyFilters>) => void;
  onClearFilters: () => void;
}

const difficultyLevels: Array<{ value: DifficultyLevel | ''; label: string }> = [
  { value: '', label: 'All Levels' },
  { value: 'A1', label: 'A1 - Beginner' },
  { value: 'A2', label: 'A2 - Elementary' },
  { value: 'B1', label: 'B1 - Intermediate' },
  { value: 'B2', label: 'B2 - Upper Intermediate' },
  { value: 'C1', label: 'C1 - Advanced' },
  { value: 'C2', label: 'C2 - Mastery' },
];

const masteryLevels: Array<{ value: MasteryLevel | -1; label: string }> = [
  { value: -1, label: 'All Mastery' },
  { value: 0, label: '0 - New' },
  { value: 1, label: '1 - Learning' },
  { value: 2, label: '2 - Familiar' },
  { value: 3, label: '3 - Comfortable' },
  { value: 4, label: '4 - Confident' },
  { value: 5, label: '5 - Mastered' },
];

export function WordFilters({
  filters,
  categories,
  onFilterChange,
  onClearFilters,
}: WordFiltersProps) {
  const hasActiveFilters =
    filters.search ||
    filters.difficulty ||
    filters.category ||
    filters.mastery_level !== undefined;

  return (
    <div className="bg-white rounded-lg border border-gray-200 shadow-sm p-4 md:p-6">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search */}
        <div>
          <label htmlFor="word-search" className="block text-sm font-medium text-gray-700 mb-1">
            Search
          </label>
          <input
            id="word-search"
            type="text"
            value={filters.search || ''}
            onChange={(e) => onFilterChange({ search: e.target.value || undefined })}
            placeholder="Search words..."
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            data-testid="word-search-input"
          />
        </div>

        {/* Category filter */}
        <div>
          <label htmlFor="word-category" className="block text-sm font-medium text-gray-700 mb-1">
            Category
          </label>
          <select
            id="word-category"
            value={filters.category || ''}
            onChange={(e) => onFilterChange({ category: e.target.value || undefined })}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            data-testid="word-category-filter"
          >
            <option value="">All Categories</option>
            {categories.map((cat) => (
              <option key={cat} value={cat}>
                {cat.charAt(0).toUpperCase() + cat.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Difficulty filter */}
        <div>
          <label htmlFor="word-difficulty" className="block text-sm font-medium text-gray-700 mb-1">
            Difficulty
          </label>
          <select
            id="word-difficulty"
            value={filters.difficulty || ''}
            onChange={(e) =>
              onFilterChange({ difficulty: (e.target.value as DifficultyLevel) || undefined })
            }
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            data-testid="word-difficulty-filter"
          >
            {difficultyLevels.map(({ value, label }) => (
              <option key={value || 'all'} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>

        {/* Mastery filter */}
        <div>
          <label htmlFor="word-mastery" className="block text-sm font-medium text-gray-700 mb-1">
            Mastery Level
          </label>
          <select
            id="word-mastery"
            value={filters.mastery_level !== undefined ? filters.mastery_level : -1}
            onChange={(e) => {
              const value = parseInt(e.target.value);
              onFilterChange({ mastery_level: value === -1 ? undefined : (value as MasteryLevel) });
            }}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            data-testid="word-mastery-filter"
          >
            {masteryLevels.map(({ value, label }) => (
              <option key={value} value={value}>
                {label}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Clear filters button */}
      {hasActiveFilters && (
        <div className="mt-4 flex justify-end">
          <button
            onClick={onClearFilters}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            data-testid="clear-filters-btn"
          >
            Clear all filters
          </button>
        </div>
      )}
    </div>
  );
}
