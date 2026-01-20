import { useState } from 'react';
import { Copy, ChevronDown, ChevronUp, AlertCircle, CheckCircle2 } from 'lucide-react';
import type {
  ConversationTurnResponse,
  GrammarFeedbackItem,
} from '../../api/types/conversation.types';

interface MessageBubbleProps {
  message: ConversationTurnResponse;
  isUser: boolean;
  showGrammarFeedback?: boolean;
  showVocabularyHighlights?: boolean;
  onVocabularyClick?: (wordId: number) => void;
}

export function MessageBubble({
  message,
  isUser,
  showGrammarFeedback = false,
  showVocabularyHighlights = false,
  onVocabularyClick,
}: MessageBubbleProps) {
  const [showFeedback, setShowFeedback] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('de-DE', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'text-red-600 bg-red-50';
      case 'medium':
        return 'text-orange-600 bg-orange-50';
      case 'low':
        return 'text-yellow-600 bg-yellow-50';
      default:
        return 'text-gray-600 bg-gray-50';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high':
      case 'medium':
        return <AlertCircle className="h-4 w-4" />;
      case 'low':
        return <CheckCircle2 className="h-4 w-4" />;
      default:
        return null;
    }
  };

  const hasFeedback = message.grammar_feedback && message.grammar_feedback.length > 0;
  const messageText = isUser ? message.user_message : message.ai_response;

  return (
    <div
      className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4 group`}
    >
      <div
        className={`max-w-[75%] md:max-w-[65%] ${
          isUser
            ? 'bg-blue-600 text-white rounded-l-2xl rounded-tr-2xl'
            : 'bg-gray-100 text-gray-900 rounded-r-2xl rounded-tl-2xl'
        } px-4 py-3 shadow-sm relative`}
      >
        {/* Message text */}
        <div className="whitespace-pre-wrap break-words">{messageText}</div>

        {/* Timestamp and copy button */}
        <div
          className={`flex items-center justify-between mt-2 pt-2 border-t ${
            isUser ? 'border-blue-500' : 'border-gray-200'
          }`}
        >
          <span
            className={`text-xs ${
              isUser ? 'text-blue-100' : 'text-gray-500'
            }`}
          >
            {formatTimestamp(message.timestamp)}
          </span>

          <button
            onClick={() => handleCopy(messageText)}
            className={`opacity-0 group-hover:opacity-100 transition-opacity p-1 rounded hover:bg-white/10 ${
              isUser ? 'text-blue-100' : 'text-gray-600'
            }`}
            title="Copy message"
          >
            {copied ? (
              <CheckCircle2 className="h-3 w-3" />
            ) : (
              <Copy className="h-3 w-3" />
            )}
          </button>
        </div>

        {/* Grammar feedback (for user messages only) */}
        {!isUser && showGrammarFeedback && hasFeedback && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <button
              onClick={() => setShowFeedback(!showFeedback)}
              className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-gray-900 transition-colors"
            >
              <AlertCircle className="h-4 w-4 text-orange-500" />
              <span>
                {message.grammar_feedback.length} Grammar{' '}
                {message.grammar_feedback.length === 1 ? 'Note' : 'Notes'}
              </span>
              {showFeedback ? (
                <ChevronUp className="h-4 w-4" />
              ) : (
                <ChevronDown className="h-4 w-4" />
              )}
            </button>

            {showFeedback && (
              <div className="mt-2 space-y-2">
                {message.grammar_feedback.map((feedback, index) => (
                  <GrammarFeedbackItem key={index} feedback={feedback} />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

interface GrammarFeedbackItemProps {
  feedback: GrammarFeedbackItem;
}

function GrammarFeedbackItem({ feedback }: GrammarFeedbackItemProps) {
  const severityColor = getSeverityColor(feedback.severity);
  const severityIcon = getSeverityIcon(feedback.severity);

  function getSeverityColor(severity: string) {
    switch (severity) {
      case 'high':
        return 'border-red-200 bg-red-50';
      case 'medium':
        return 'border-orange-200 bg-orange-50';
      case 'low':
        return 'border-yellow-200 bg-yellow-50';
      default:
        return 'border-gray-200 bg-gray-50';
    }
  }

  function getSeverityIcon(severity: string) {
    switch (severity) {
      case 'high':
      case 'medium':
        return <AlertCircle className="h-4 w-4 text-orange-600" />;
      case 'low':
        return <CheckCircle2 className="h-4 w-4 text-green-600" />;
      default:
        return null;
    }
  }

  return (
    <div className={`p-3 rounded-lg border ${severityColor}`}>
      <div className="flex items-start gap-2">
        {severityIcon}
        <div className="flex-1 text-sm">
          <div className="font-medium text-gray-900 mb-1">
            {feedback.error_type}
          </div>
          <div className="space-y-1">
            <div className="flex items-baseline gap-2">
              <span className="text-gray-600">Incorrect:</span>
              <span className="line-through text-red-600">
                {feedback.incorrect}
              </span>
            </div>
            <div className="flex items-baseline gap-2">
              <span className="text-gray-600">Corrected:</span>
              <span className="font-medium text-green-600">
                {feedback.corrected}
              </span>
            </div>
            {feedback.explanation && (
              <p className="text-gray-700 mt-1 italic">
                {feedback.explanation}
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
