import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Clock,
  MessageSquare,
  Calendar,
  ChevronRight,
  Award,
  Filter,
} from 'lucide-react';
import { useConversationStore } from '../../store/conversationStore';
import type { SessionResponse } from '../../api/types/conversation.types';

export function HistoryPage() {
  const navigate = useNavigate();
  const { sessionHistory, isLoadingHistory, loadHistory, availableContexts, loadContexts } =
    useConversationStore();

  const [contextFilter, setContextFilter] = useState<string>('');
  const [sortBy, setSortBy] = useState<'date' | 'score' | 'duration'>('date');

  /**
   * Load data on mount
   */
  useEffect(() => {
    loadHistory();
    loadContexts();
  }, [loadHistory, loadContexts]);

  /**
   * Filter and sort sessions
   */
  const filteredSessions = sessionHistory
    .filter((session) => {
      if (!contextFilter) return true;
      return session.context_id === parseInt(contextFilter, 10);
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'date':
          return (
            new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
          );
        case 'score':
          return (b.overall_score || 0) - (a.overall_score || 0);
        case 'duration': {
          const durationA = a.end_time
            ? new Date(a.end_time).getTime() - new Date(a.start_time).getTime()
            : 0;
          const durationB = b.end_time
            ? new Date(b.end_time).getTime() - new Date(b.start_time).getTime()
            : 0;
          return durationB - durationA;
        }
        default:
          return 0;
      }
    });

  return (
    <div className="flex-1 overflow-y-auto">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Conversation History
          </h1>
          <p className="mt-2 text-gray-600">
            Review your past conversation sessions and track your progress
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Context filter */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={contextFilter}
                onChange={(e) => setContextFilter(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
              >
                <option value="">All Contexts</option>
                {availableContexts.map((context) => (
                  <option key={context.id} value={context.id.toString()}>
                    {context.name}
                  </option>
                ))}
              </select>
            </div>

            {/* Sort by */}
            <div className="relative">
              <Filter className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" />
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none bg-white"
              >
                <option value="date">Sort by Date (Newest First)</option>
                <option value="score">Sort by Score (Highest First)</option>
                <option value="duration">Sort by Duration (Longest First)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Sessions List */}
        {isLoadingHistory ? (
          <LoadingState />
        ) : filteredSessions.length === 0 ? (
          <EmptyState hasFilter={Boolean(contextFilter)} />
        ) : (
          <div className="space-y-4">
            {filteredSessions.map((session) => (
              <SessionCard
                key={session.id}
                session={session}
                onViewDetails={() =>
                  navigate(`/conversation/session/${session.id}`)
                }
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

interface SessionCardProps {
  session: SessionResponse;
  onViewDetails: () => void;
}

function SessionCard({ session, onViewDetails }: SessionCardProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const calculateDuration = () => {
    if (!session.end_time) return 'In progress';
    const start = new Date(session.start_time);
    const end = new Date(session.end_time);
    const minutes = Math.floor((end.getTime() - start.getTime()) / 60000);
    return `${minutes} min`;
  };

  const getScoreColor = (score: number | undefined) => {
    if (!score) return 'bg-gray-100 text-gray-700';
    if (score >= 80) return 'bg-green-100 text-green-700';
    if (score >= 60) return 'bg-blue-100 text-blue-700';
    if (score >= 40) return 'bg-orange-100 text-orange-700';
    return 'bg-red-100 text-red-700';
  };

  const grammarAccuracy = session.total_turns > 0
    ? Math.round(
        ((session.total_turns - session.grammar_corrections) /
          session.total_turns) *
          100
      )
    : 0;

  return (
    <div
      className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
      onClick={onViewDetails}
    >
      <div className="flex items-start justify-between">
        {/* Left: Context info */}
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <span className="text-sm text-gray-600">{formatDate(session.start_time)}</span>
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">
            Context #{session.context_id}
          </h3>
        </div>

        {/* Right: Stats */}
        <div className="flex items-center gap-6 text-sm">
          <div className="flex items-center gap-2 text-gray-600">
            <Clock className="h-4 w-4" />
            <span>{calculateDuration()}</span>
          </div>
          <div className="flex items-center gap-2 text-gray-600">
            <MessageSquare className="h-4 w-4" />
            <span>{session.total_turns} turns</span>
          </div>
          {session.overall_score !== undefined && session.overall_score !== null && (
            <div
              className={`flex items-center gap-2 px-3 py-1 rounded-full font-medium ${getScoreColor(
                session.overall_score
              )}`}
            >
              <Award className="h-4 w-4" />
              <span>{session.overall_score}</span>
            </div>
          )}
          <ChevronRight className="h-5 w-5 text-gray-400" />
        </div>
      </div>

      {/* Grammar accuracy progress bar */}
      {session.grammar_corrections > 0 && (
        <div className="mt-4">
          <div className="flex items-center justify-between text-sm mb-1">
            <span className="text-gray-600">Grammar Accuracy</span>
            <span className="font-medium text-gray-900">{grammarAccuracy}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all ${
                grammarAccuracy >= 80
                  ? 'bg-green-600'
                  : grammarAccuracy >= 60
                  ? 'bg-blue-600'
                  : grammarAccuracy >= 40
                  ? 'bg-orange-600'
                  : 'bg-red-600'
              }`}
              style={{ width: `${grammarAccuracy}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Session metadata */}
      <div className="mt-4 flex items-center gap-4 text-sm text-gray-600">
        {session.vocabulary_used > 0 && (
          <span>{session.vocabulary_used} vocabulary words</span>
        )}
        {session.grammar_corrections > 0 && (
          <span>{session.grammar_corrections} grammar notes</span>
        )}
      </div>
    </div>
  );
}

function LoadingState() {
  return (
    <div className="space-y-4">
      {[1, 2, 3, 4, 5].map((i) => (
        <div key={i} className="bg-gray-100 rounded-lg h-32 animate-pulse"></div>
      ))}
    </div>
  );
}

interface EmptyStateProps {
  hasFilter: boolean;
}

function EmptyState({ hasFilter }: EmptyStateProps) {
  const navigate = useNavigate();

  return (
    <div className="text-center py-12">
      <div className="bg-gray-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
        <MessageSquare className="h-8 w-8 text-gray-400" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        {hasFilter ? 'No sessions found' : 'No conversation history yet'}
      </h3>
      <p className="text-gray-600 max-w-md mx-auto mb-6">
        {hasFilter
          ? 'Try changing your filters to see more sessions.'
          : 'Start your first conversation to begin building your practice history.'}
      </p>
      {!hasFilter && (
        <button
          onClick={() => navigate('/conversation')}
          className="px-6 py-3 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
        >
          Start First Conversation
        </button>
      )}
    </div>
  );
}
