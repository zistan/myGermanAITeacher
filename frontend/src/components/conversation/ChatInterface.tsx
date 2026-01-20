import { useEffect } from 'react';
import { MessageSquare } from 'lucide-react';
import { MessageBubble } from './MessageBubble';
import { TypingIndicator } from './TypingIndicator';
import { ChatInput } from './ChatInput';
import { useAutoScroll } from '../../hooks/useAutoScroll';
import type { ConversationTurnResponse } from '../../api/types/conversation.types';

interface ChatInterfaceProps {
  sessionId: number | null;
  messages: ConversationTurnResponse[];
  onSendMessage: (message: string, requestFeedback: boolean) => void;
  isTyping: boolean;
  disabled: boolean;
  showGrammarFeedback?: boolean;
  showVocabularyHighlights?: boolean;
  onVocabularyClick?: (wordId: number) => void;
}

export function ChatInterface({
  sessionId,
  messages,
  onSendMessage,
  isTyping,
  disabled,
  showGrammarFeedback = false,
  showVocabularyHighlights = false,
  onVocabularyClick,
}: ChatInterfaceProps) {
  const { containerRef, messagesEndRef, handleScroll } = useAutoScroll(
    [messages.length, isTyping],
    100
  );

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Messages container */}
      <div
        ref={containerRef}
        onScroll={handleScroll}
        className="flex-1 overflow-y-auto px-4 py-6"
      >
        {messages.length === 0 && !isTyping ? (
          <EmptyState />
        ) : (
          <>
            {messages.map((message) => (
              <div key={message.id}>
                {/* User message */}
                <MessageBubble
                  message={message}
                  isUser={true}
                  showGrammarFeedback={showGrammarFeedback}
                  showVocabularyHighlights={showVocabularyHighlights}
                  onVocabularyClick={onVocabularyClick}
                />

                {/* AI response */}
                <MessageBubble
                  message={message}
                  isUser={false}
                  showGrammarFeedback={showGrammarFeedback}
                  showVocabularyHighlights={showVocabularyHighlights}
                  onVocabularyClick={onVocabularyClick}
                />
              </div>
            ))}

            {/* Typing indicator */}
            {isTyping && <TypingIndicator />}

            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Chat input (sticky) */}
      <ChatInput onSend={onSendMessage} disabled={disabled} />
    </div>
  );
}

function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center px-4">
      <div className="bg-blue-50 rounded-full p-6 mb-4">
        <MessageSquare className="h-12 w-12 text-blue-600" />
      </div>
      <h3 className="text-lg font-semibold text-gray-900 mb-2">
        Start Your Conversation
      </h3>
      <p className="text-gray-600 max-w-md mb-6">
        Begin practicing your German! Send your first message to start the conversation.
        Don't worry about making mistakes - that's how we learn.
      </p>
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-md">
        <p className="text-sm text-blue-900 font-medium mb-2">Tips for better practice:</p>
        <ul className="text-sm text-blue-800 text-left space-y-1">
          <li>• Write complete sentences in German</li>
          <li>• Use the German character buttons (ä, ö, ü, ß)</li>
          <li>• Request grammar feedback for detailed corrections</li>
          <li>• Try to stay in character for the context</li>
        </ul>
      </div>
    </div>
  );
}
