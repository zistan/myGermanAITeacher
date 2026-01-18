import { useNavigate } from 'react-router-dom';
import type { DueItems } from '../../api/types/integration.types';
import { Card, Badge, Button } from '../common';

interface DueItemsCardProps {
  dueItems: DueItems;
}

export function DueItemsCard({ dueItems }: DueItemsCardProps) {
  const navigate = useNavigate();
  const hasDueItems = dueItems.total_due > 0;

  return (
    <Card>
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Items Due for Review</h2>
        {hasDueItems && (
          <Badge variant="danger">{dueItems.total_due} due</Badge>
        )}
      </div>

      {!hasDueItems ? (
        <div className="text-center py-8">
          <div className="text-4xl mb-2">✅</div>
          <p className="text-gray-600">All caught up! No items due for review.</p>
        </div>
      ) : (
        <>
          {/* Grammar Topics Due */}
          {dueItems.grammar_topics.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-700">Grammar Topics</h3>
                <span className="text-xs text-gray-500">
                  {dueItems.grammar_topics.length} topic{dueItems.grammar_topics.length !== 1 ? 's' : ''}
                </span>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {dueItems.grammar_topics.slice(0, 5).map((topic) => (
                  <div
                    key={topic.topic_id}
                    className="flex items-center justify-between p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors cursor-pointer"
                    onClick={() => navigate(`/grammar/practice?topic=${topic.topic_id}`)}
                  >
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{topic.topic_name}</div>
                      <div className="text-xs text-gray-500">
                        Mastery: {(topic.mastery_level * 100).toFixed(0)}%
                      </div>
                    </div>
                    {topic.days_overdue > 0 && (
                      <Badge variant="danger" size="sm">
                        {topic.days_overdue}d overdue
                      </Badge>
                    )}
                  </div>
                ))}
                {dueItems.grammar_topics.length > 5 && (
                  <div className="text-center pt-2">
                    <button
                      onClick={() => navigate('/grammar/review-queue')}
                      className="text-xs text-primary-600 hover:text-primary-700 font-medium"
                    >
                      View all {dueItems.grammar_topics.length} topics →
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Vocabulary Words Due */}
          {dueItems.vocabulary_words.length > 0 && (
            <div className="mb-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-gray-700">Vocabulary Words</h3>
                <span className="text-xs text-gray-500">
                  {dueItems.vocabulary_words.length} word{dueItems.vocabulary_words.length !== 1 ? 's' : ''}
                </span>
              </div>
              <div className="space-y-2 max-h-48 overflow-y-auto">
                {dueItems.vocabulary_words.slice(0, 5).map((word) => (
                  <div
                    key={word.word_id}
                    className="flex items-center justify-between p-2 bg-gray-50 rounded hover:bg-gray-100 transition-colors cursor-pointer"
                    onClick={() => navigate(`/vocabulary/flashcards?word=${word.word_id}`)}
                  >
                    <div className="flex-1">
                      <div className="text-sm font-medium text-gray-900">{word.word}</div>
                      <div className="text-xs text-gray-500">{word.translation_it}</div>
                    </div>
                    {word.days_overdue > 0 && (
                      <Badge color="danger" size="sm">
                        {word.days_overdue}d overdue
                      </Badge>
                    )}
                  </div>
                ))}
                {dueItems.vocabulary_words.length > 5 && (
                  <div className="text-center pt-2">
                    <button
                      onClick={() => navigate('/vocabulary/review-queue')}
                      className="text-xs text-primary-600 hover:text-primary-700 font-medium"
                    >
                      View all {dueItems.vocabulary_words.length} words →
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* Review Button */}
          <div className="mt-4 pt-4 border-t border-gray-200">
            <Button
              onClick={() => navigate('/review')}
              variant="primary"
              fullWidth
            >
              Start Review Session
            </Button>
          </div>
        </>
      )}
    </Card>
  );
}
