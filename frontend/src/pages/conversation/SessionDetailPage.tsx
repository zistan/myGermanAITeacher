import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  ArrowLeft,
  Calendar,
  Clock,
  MessageSquare,
  Target,
  BookOpen,
  Award,
  TrendingUp,
  ExternalLink,
} from 'lucide-react';
import conversationService from '../../api/services/conversationService';
import { MessageBubble } from '../../components/conversation';
import type { SessionHistoryResponse } from '../../api/types/conversation.types';

export function SessionDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [data, setData] = useState<SessionHistoryResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  /**
   * Load session details
   */
  useEffect(() => {
    const loadSession = async () => {
      if (!id) {
        setError('Invalid session ID');
        setIsLoading(false);
        return;
      }

      try {
        setIsLoading(true);
        const sessionData = await conversationService.getSessionDetail(parseInt(id, 10));
        setData(sessionData);
      } catch (err: any) {
        setError(err.message || 'Failed to load session details');
      } finally {
        setIsLoading(false);
      }
    };

    loadSession();
  }, [id]);

  /**
   * Navigate to grammar practice with detected topics
   */
  const handlePracticeGrammar = () => {
    if (!data?.summary.grammar_topics_to_practice) return;

    const topicIds = data.summary.grammar_topics_to_practice
      .map((t) => t.topic_id)
      .join(',');
    navigate(`/grammar/practice?topics=${topicIds}`);
  };

  /**
   * Start similar conversation
   */
  const handleStartSimilar = () => {
    if (!data?.session.context_id) return;
    navigate(`/conversation/practice?context=${data.session.context_id}`);
  };

  /**
   * Format date
   */
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading session details...</p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Session not found'}</p>
          <button
            onClick={() => navigate('/conversation/history')}
            className="px-4 py-2 text-white bg-blue-600 hover:bg-blue-700 rounded-lg"
          >
            Back to History
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-6">
          <button
            onClick={() => navigate('/conversation/history')}
            className="flex items-center gap-2 text-gray-600 hover:text-gray-900 mb-4"
          >
            <ArrowLeft className="h-4 w-4" />
            <span>Back to History</span>
          </button>

          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
            <div className="flex items-start justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900 mb-2">
                  {data.session.context_name}
                </h1>
                <p className="text-gray-600 mb-4">
                  {data.session.context_description}
                </p>
                <div className="flex items-center gap-4 text-sm text-gray-600">
                  <div className="flex items-center gap-2">
                    <Calendar className="h-4 w-4" />
                    <span>{formatDate(data.session.start_time)}</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span>{data.summary.duration_minutes} minutes</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <MessageSquare className="h-4 w-4" />
                    <span>{data.summary.total_turns} turns</span>
                  </div>
                </div>
              </div>

              {data.summary.overall_score !== undefined && (
                <div className="text-center">
                  <div className="text-3xl font-bold text-blue-600 mb-1">
                    {data.summary.overall_score}
                  </div>
                  <div className="text-sm text-gray-600">Overall Score</div>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            icon={<Target className="h-6 w-6" />}
            label="Grammar Accuracy"
            value={`${data.summary.grammar_accuracy}%`}
            color="purple"
          />
          <StatCard
            icon={<BookOpen className="h-6 w-6" />}
            label="Vocabulary Used"
            value={data.summary.unique_vocabulary_count.toString()}
            color="green"
          />
          <StatCard
            icon={<Award className="h-6 w-6" />}
            label="Session Score"
            value={data.summary.overall_score?.toString() || 'N/A'}
            color="blue"
          />
        </div>

        {/* Analysis Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Areas for Improvement */}
          {data.summary.areas_for_improvement &&
            data.summary.areas_for_improvement.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-orange-600" />
                  Areas for Improvement
                </h2>
                <ul className="space-y-2">
                  {data.summary.areas_for_improvement.map((area, index) => (
                    <li key={index} className="flex items-start gap-2 text-sm text-gray-700">
                      <span className="text-orange-600 font-medium">{index + 1}.</span>
                      <span>{area}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

          {/* Grammar Topics to Practice */}
          {data.summary.grammar_topics_to_practice &&
            data.summary.grammar_topics_to_practice.length > 0 && (
              <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-green-600" />
                  Recommended Grammar Topics
                </h2>
                <div className="space-y-2 mb-4">
                  {data.summary.grammar_topics_to_practice.map((topic) => (
                    <div
                      key={topic.topic_id}
                      className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                    >
                      <div>
                        <div className="font-medium text-gray-900">{topic.topic_name}</div>
                        <div className="text-sm text-gray-600">
                          {topic.error_count} error{topic.error_count !== 1 ? 's' : ''}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <button
                  onClick={handlePracticeGrammar}
                  className="w-full px-4 py-2 text-sm font-medium text-white bg-green-600 hover:bg-green-700 rounded-lg transition-colors flex items-center justify-center gap-2"
                >
                  <BookOpen className="h-4 w-4" />
                  Practice These Topics
                  <ExternalLink className="h-4 w-4" />
                </button>
              </div>
            )}
        </div>

        {/* Conversation Replay */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-6 flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-blue-600" />
            Full Conversation
          </h2>
          <div className="space-y-4">
            {data.messages.map((message) => (
              <div key={message.id} className="space-y-2">
                <MessageBubble
                  message={message}
                  isUser={true}
                  showGrammarFeedback={true}
                  showVocabularyHighlights={false}
                />
                <MessageBubble
                  message={message}
                  isUser={false}
                  showGrammarFeedback={true}
                  showVocabularyHighlights={false}
                />
              </div>
            ))}
          </div>
        </div>

        {/* Actions */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Next Steps</h2>
          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleStartSimilar}
              className="flex-1 px-6 py-3 text-white bg-blue-600 hover:bg-blue-700 rounded-lg font-medium transition-colors"
            >
              Practice Similar Context
            </button>
            <button
              onClick={() => navigate('/conversation')}
              className="flex-1 px-6 py-3 text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg font-medium transition-colors"
            >
              Choose Different Context
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string;
  color: 'blue' | 'green' | 'purple';
}

function StatCard({ icon, label, value, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    purple: 'bg-purple-50 text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 text-center">
      <div className={`inline-flex p-3 rounded-lg mb-3 ${colorClasses[color]}`}>
        {icon}
      </div>
      <div className="text-3xl font-bold text-gray-900 mb-2">{value}</div>
      <div className="text-sm text-gray-600">{label}</div>
    </div>
  );
}
