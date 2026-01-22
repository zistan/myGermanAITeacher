/**
 * AchievementFilters Component
 * Filter controls for achievements page
 */


export interface AchievementFiltersProps {
  category: string;
  tier: string;
  status: string;
  onCategoryChange: (category: string) => void;
  onTierChange: (tier: string) => void;
  onStatusChange: (status: string) => void;
}

export function AchievementFilters({
  category,
  tier,
  status,
  onCategoryChange,
  onTierChange,
  onStatusChange,
}: AchievementFiltersProps) {
  return (
    <div className="bg-white rounded-lg shadow border border-gray-200 p-4">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Category Filter */}
        <div>
          <label
            htmlFor="category-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Category
          </label>
          <select
            id="category-filter"
            value={category}
            onChange={(e) => onCategoryChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Categories</option>
            <option value="conversation">Conversation</option>
            <option value="grammar">Grammar</option>
            <option value="vocabulary">Vocabulary</option>
            <option value="activity">Activity</option>
          </select>
        </div>

        {/* Tier Filter */}
        <div>
          <label
            htmlFor="tier-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Tier
          </label>
          <select
            id="tier-filter"
            value={tier}
            onChange={(e) => onTierChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Tiers</option>
            <option value="bronze">Bronze</option>
            <option value="silver">Silver</option>
            <option value="gold">Gold</option>
            <option value="platinum">Platinum</option>
          </select>
        </div>

        {/* Status Filter */}
        <div>
          <label
            htmlFor="status-filter"
            className="block text-sm font-medium text-gray-700 mb-1"
          >
            Status
          </label>
          <select
            id="status-filter"
            value={status}
            onChange={(e) => onStatusChange(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="all">All Achievements</option>
            <option value="earned">Earned</option>
            <option value="in-progress">In Progress</option>
            <option value="locked">Locked</option>
          </select>
        </div>
      </div>
    </div>
  );
}
