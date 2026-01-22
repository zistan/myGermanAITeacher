/**
 * HeatmapPage
 * Displays activity and grammar mastery heatmaps with tab navigation
 */

import { useEffect, useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { format, addDays } from 'date-fns';
import clsx from 'clsx';
import { Loading } from '../../components/common/Loading';
import analyticsService from '../../api/services/analyticsService';
import type {
  ActivityHeatmapResponse,
  GrammarHeatmapResponse,
  HeatmapCell,
} from '../../api/types/analytics.types';

type TabType = 'activity' | 'grammar';

// Activity intensity colors
const INTENSITY_COLORS = [
  'fill-gray-100',   // 0
  'fill-green-200',  // 1
  'fill-green-300',  // 2
  'fill-green-500',  // 3
  'fill-green-700',  // 4
];

// Grammar mastery colors
const MASTERY_COLORS = [
  'bg-gray-200',   // < 1.0
  'bg-red-300',    // 1.0-1.9
  'bg-yellow-300', // 2.0-2.9
  'bg-blue-400',   // 3.0-3.9
  'bg-green-500',  // 4.0+
];

export function HeatmapPage() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<TabType>('activity');
  const [activityData, setActivityData] = useState<ActivityHeatmapResponse | null>(null);
  const [grammarData, setGrammarData] = useState<GrammarHeatmapResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [activity, grammar] = await Promise.all([
        analyticsService.getActivityHeatmap(365),
        analyticsService.getGrammarHeatmap(),
      ]);
      setActivityData(activity);
      setGrammarData(grammar);
    } catch (error: any) {
      toast.error(error.detail || 'Failed to load heatmap data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <Loading />;
  }

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Heatmaps</h1>
        <p className="mt-2 text-gray-600">Visualize your learning activity and mastery</p>
      </div>

      {/* Tab Selector */}
      <div className="bg-white rounded-lg shadow border border-gray-200">
        <div className="border-b border-gray-200">
          <nav className="flex -mb-px">
            <button
              onClick={() => setActiveTab('activity')}
              className={clsx(
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'activity'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
              )}
            >
              Activity Heatmap
            </button>
            <button
              onClick={() => setActiveTab('grammar')}
              className={clsx(
                'px-6 py-3 text-sm font-medium border-b-2 transition-colors',
                activeTab === 'grammar'
                  ? 'border-primary-500 text-primary-600'
                  : 'border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300'
              )}
            >
              Grammar Mastery
            </button>
          </nav>
        </div>

        <div className="p-6">
          {activeTab === 'activity' && activityData && (
            <ActivityHeatmapView data={activityData} />
          )}
          {activeTab === 'grammar' && grammarData && (
            <GrammarHeatmapView data={grammarData} navigate={navigate} />
          )}
        </div>
      </div>
    </div>
  );
}

// Activity Heatmap Component
function ActivityHeatmapView({ data }: { data: ActivityHeatmapResponse }) {
  const CELL_SIZE = 12;
  const CELL_GAP = 3;

  // Build cells map
  const cellsMap = useMemo(() => {
    const map = new Map<string, HeatmapCell>();
    data.cells.forEach((cell) => map.set(cell.date, cell));
    return map;
  }, [data.cells]);

  // Calculate grid
  const startDate = new Date(data.start_date);
  const weeks = 52;
  const days = 7;

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600">
            {data.active_days} active days in the last {data.total_days} days
          </p>
        </div>
        <div className="flex items-center space-x-2 text-xs text-gray-600">
          <span>Less</span>
          {INTENSITY_COLORS.map((color, i) => (
            <div
              key={i}
              className={clsx('w-3 h-3 rounded-sm', color)}
            />
          ))}
          <span>More</span>
        </div>
      </div>

      <div className="overflow-x-auto">
        <svg width={weeks * (CELL_SIZE + CELL_GAP) + 40} height={days * (CELL_SIZE + CELL_GAP) + 20}>
          {/* Day labels */}
          <text x="0" y="20" fontSize="10" fill="#6b7280">M</text>
          <text x="0" y="32" fontSize="10" fill="#6b7280">W</text>
          <text x="0" y="44" fontSize="10" fill="#6b7280">F</text>

          {/* Grid cells */}
          {Array.from({ length: weeks }).map((_, weekIndex) =>
            Array.from({ length: days }).map((_, dayIndex) => {
              const date = addDays(startDate, weekIndex * 7 + dayIndex);
              const dateStr = format(date, 'yyyy-MM-dd');
              const cell = cellsMap.get(dateStr);

              return (
                <rect
                  key={`${weekIndex}-${dayIndex}`}
                  x={weekIndex * (CELL_SIZE + CELL_GAP) + 20}
                  y={dayIndex * (CELL_SIZE + CELL_GAP) + 10}
                  width={CELL_SIZE}
                  height={CELL_SIZE}
                  className={clsx(
                    'transition-opacity hover:opacity-80',
                    INTENSITY_COLORS[cell?.level || 0]
                  )}
                  rx="2"
                >
                  <title>{`${format(date, 'MMM d, yyyy')}: ${cell?.value || 0} sessions`}</title>
                </rect>
              );
            })
          )}
        </svg>
      </div>
    </div>
  );
}

// Grammar Heatmap Component
function GrammarHeatmapView({
  data,
  navigate,
}: {
  data: GrammarHeatmapResponse;
  navigate: (path: string) => void;
}) {
  // Group topics by category
  const topicsByCategory = useMemo(() => {
    const grouped = new Map<string, typeof data.topics>();
    data.topics.forEach((topic) => {
      const existing = grouped.get(topic.category) || [];
      grouped.set(topic.category, [...existing, topic]);
    });
    return grouped;
  }, [data.topics]);

  const getMasteryColor = (mastery: number): string => {
    if (mastery < 1.0) return MASTERY_COLORS[0];
    if (mastery < 2.0) return MASTERY_COLORS[1];
    if (mastery < 3.0) return MASTERY_COLORS[2];
    if (mastery < 4.0) return MASTERY_COLORS[3];
    return MASTERY_COLORS[4];
  };

  const getMasteryLabel = (mastery: number): string => {
    if (mastery < 1.0) return 'Not started';
    if (mastery < 2.0) return 'Learning';
    if (mastery < 3.0) return 'Familiar';
    if (mastery < 4.0) return 'Comfortable';
    return 'Mastered';
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-gray-600">
          Overall Mastery: <span className="font-medium">{data.overall_mastery.toFixed(1)}</span> / 5.0
        </p>
        <div className="flex items-center space-x-2 text-xs text-gray-600">
          {['Not started', 'Learning', 'Familiar', 'Comfortable', 'Mastered'].map((label, i) => (
            <div key={i} className="flex items-center space-x-1">
              <div className={clsx('w-3 h-3 rounded', MASTERY_COLORS[i])} />
              <span>{label}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="space-y-4">
        {data.categories.sort().map((category) => {
          const topics = topicsByCategory.get(category) || [];
          return (
            <div key={category}>
              <h3 className="font-medium text-sm text-gray-700 mb-2">{category}</h3>
              <div className="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-10 gap-2">
                {topics.map((topic) => (
                  <button
                    key={topic.topic_id}
                    onClick={() => navigate(`/grammar/practice?topics=${topic.topic_id}`)}
                    className={clsx(
                      'aspect-square rounded p-1 text-xs font-medium text-gray-700 hover:ring-2 hover:ring-primary-500 transition-all',
                      getMasteryColor(topic.mastery_level)
                    )}
                    title={`${topic.topic_name}\nMastery: ${topic.mastery_level.toFixed(1)} (${getMasteryLabel(topic.mastery_level)})`}
                  >
                    <span className="sr-only">{topic.topic_name}</span>
                  </button>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
