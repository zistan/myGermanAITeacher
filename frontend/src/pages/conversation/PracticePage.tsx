import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import {
  Clock,
  MessageSquare,
  X,
  BookOpen,
  ChevronLeft,
  ChevronRight,
} from 'lucide-react';
import { useConversationStore } from '../../store/conversationStore';
import {
  ChatInterface,
  GrammarFeedbackPanel,
  SessionSummary,
} from '../../components/conversation';

export function PracticePage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const contextId = searchParams.get('context');

  const {
    sessionState,
    currentSession,
    messages,
    isTyping,
    isSendingMessage,
    showGrammarPanel,
    pendingFeedback,
    sessionSummary,
    startSession,
    sendMessage,
    endSession,
    clearSession,
    toggleGrammarPanel,
    hasIncompleteSession,
    restoreSession,
  } = useConversationStore();

  const [sessionTimer, setSessionTimer] = useState(0);
  const [showEndConfirmation, setShowEndConfirmation] = useState(false);
  const [showRestorePrompt, setShowRestorePrompt] = useState(false);
  const [showSummaryModal, setShowSummaryModal] = useState(false);

  /**
   * Check for incomplete session on mount
   */
  useEffect(() => {
    if (hasIncompleteSession()) {
      setShowRestorePrompt(true);
    } else if (contextId) {
      handleStartSession(parseInt(contextId, 10));
    } else {
      navigate('/conversation');
    }
  }, []);

  /**
   * Session timer
   */
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    if (sessionState === 'active' && currentSession) {
      interval = setInterval(() => {
        const elapsed = Math.floor(
          (Date.now() - new Date(currentSession.startTime).getTime()) / 1000
        );
        setSessionTimer(elapsed);
      }, 1000);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [sessionState, currentSession]);

  /**
   * Keyboard shortcuts
   */
  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      // Escape: End session (with confirmation)
      if (e.key === 'Escape' && sessionState === 'active') {
        setShowEndConfirmation(true);
      }

      // Ctrl+/: Toggle grammar panel
      if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        toggleGrammarPanel();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, [sessionState, toggleGrammarPanel]);

  /**
   * Show summary modal when session completes
   */
  useEffect(() => {
    if (sessionState === 'completed' && sessionSummary) {
      setShowSummaryModal(true);
    }
  }, [sessionState, sessionSummary]);

  /**
   * Start a new session
   */
  const handleStartSession = async (ctxId: number) => {
    try {
      await startSession(ctxId);
      setShowRestorePrompt(false);
    } catch (error) {
      console.error('Failed to start session:', error);
      navigate('/conversation');
    }
  };

  /**
   * Restore incomplete session
   */
  const handleRestoreSession = () => {
    const restored = restoreSession();
    if (restored) {
      setShowRestorePrompt(false);
    } else {
      if (contextId) {
        handleStartSession(parseInt(contextId, 10));
      }
    }
  };

  /**
   * Discard incomplete session and start new
   */
  const handleDiscardSession = () => {
    clearSession();
    setShowRestorePrompt(false);
    if (contextId) {
      handleStartSession(parseInt(contextId, 10));
    } else {
      navigate('/conversation');
    }
  };

  /**
   * Send a message
   */
  const handleSendMessage = async (message: string, requestFeedback: boolean) => {
    try {
      await sendMessage(message, requestFeedback);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  /**
   * End the session
   */
  const handleEndSession = async () => {
    try {
      await endSession();
      setShowEndConfirmation(false);
    } catch (error) {
      console.error('Failed to end session:', error);
    }
  };

  /**
   * Close summary modal and navigate
   */
  const handleCloseSummary = () => {
    setShowSummaryModal(false);
    clearSession();
    navigate('/conversation');
  };

  /**
   * View session details
   */
  const handleViewDetails = () => {
    if (currentSession) {
      navigate(`/conversation/session/${currentSession.sessionId}`);
    }
  };

  /**
   * Start a new conversation
   */
  const handleStartNew = () => {
    setShowSummaryModal(false);
    clearSession();
    navigate('/conversation');
  };

  /**
   * Format timer
   */
  const formatTimer = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!currentSession && !showRestorePrompt) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-center">
          <p className="text-gray-600">Loading session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      {/* Session Header */}
      {currentSession && (
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/conversation')}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Back to contexts"
              >
                <ChevronLeft className="h-5 w-5 text-gray-600" />
              </button>
              <div>
                <h1 className="text-lg font-semibold text-gray-900">
                  {currentSession.contextName}
                </h1>
                <p className="text-sm text-gray-600">
                  {currentSession.contextDescription}
                </p>
              </div>
            </div>

            <div className="flex items-center gap-4">
              {/* Session Stats */}
              <div className="flex items-center gap-6 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  <span>{formatTimer(sessionTimer)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <MessageSquare className="h-4 w-4" />
                  <span>{currentSession.messageCount} messages</span>
                </div>
              </div>

              {/* Grammar Panel Toggle */}
              <button
                onClick={toggleGrammarPanel}
                className={`px-3 py-2 text-sm font-medium rounded-lg transition-colors flex items-center gap-2 ${
                  showGrammarPanel
                    ? 'bg-blue-100 text-blue-700'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
                title="Toggle grammar feedback panel (Ctrl+/)"
              >
                <BookOpen className="h-4 w-4" />
                <span className="hidden md:inline">Grammar</span>
                {pendingFeedback.length > 0 && (
                  <span className="bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                    {pendingFeedback.length}
                  </span>
                )}
                {showGrammarPanel ? (
                  <ChevronRight className="h-4 w-4" />
                ) : (
                  <ChevronLeft className="h-4 w-4" />
                )}
              </button>

              {/* End Session Button */}
              <button
                onClick={() => setShowEndConfirmation(true)}
                className="px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors"
                title="End session (Esc)"
              >
                End Session
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="flex flex-1 overflow-hidden">
        {/* Chat Interface */}
        <div className={`flex-1 ${showGrammarPanel ? 'md:w-[70%]' : 'w-full'}`}>
          {currentSession && (
            <ChatInterface
              sessionId={currentSession.sessionId}
              messages={messages}
              onSendMessage={handleSendMessage}
              isTyping={isTyping}
              disabled={isSendingMessage || sessionState === 'loading'}
              showGrammarFeedback={true}
              showVocabularyHighlights={true}
            />
          )}
        </div>

        {/* Grammar Feedback Panel (Desktop) */}
        {showGrammarPanel && (
          <div className="hidden md:block w-[30%] border-l border-gray-200">
            <GrammarFeedbackPanel
              feedback={pendingFeedback}
              isVisible={showGrammarPanel}
              onToggle={toggleGrammarPanel}
            />
          </div>
        )}
      </div>

      {/* Restore Session Modal */}
      {showRestorePrompt && (
        <RestoreSessionModal
          onRestore={handleRestoreSession}
          onDiscard={handleDiscardSession}
        />
      )}

      {/* End Session Confirmation */}
      {showEndConfirmation && (
        <ConfirmationModal
          title="End Conversation Session?"
          message="Are you sure you want to end this conversation? You'll receive a summary of your session."
          onConfirm={handleEndSession}
          onCancel={() => setShowEndConfirmation(false)}
        />
      )}

      {/* Session Summary Modal */}
      {showSummaryModal && sessionSummary && (
        <SessionSummary
          summary={sessionSummary}
          onClose={handleCloseSummary}
          onViewDetails={handleViewDetails}
          onStartNew={handleStartNew}
        />
      )}
    </div>
  );
}

interface RestoreSessionModalProps {
  onRestore: () => void;
  onDiscard: () => void;
}

function RestoreSessionModal({ onRestore, onDiscard }: RestoreSessionModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          Resume Previous Session?
        </h3>
        <p className="text-gray-600 mb-6">
          You have an incomplete conversation session. Would you like to continue where
          you left off?
        </p>
        <div className="flex gap-3">
          <button
            onClick={onDiscard}
            className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Start Fresh
          </button>
          <button
            onClick={onRestore}
            className="flex-1 px-4 py-2 text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors"
          >
            Resume Session
          </button>
        </div>
      </div>
    </div>
  );
}

interface ConfirmationModalProps {
  title: string;
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

function ConfirmationModal({
  title,
  message,
  onConfirm,
  onCancel,
}: ConfirmationModalProps) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50 p-4">
      <div className="bg-white rounded-lg shadow-xl max-w-md w-full p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <button
            onClick={onCancel}
            className="p-1 hover:bg-gray-100 rounded transition-colors"
          >
            <X className="h-5 w-5 text-gray-600" />
          </button>
        </div>
        <p className="text-gray-600 mb-6">{message}</p>
        <div className="flex gap-3">
          <button
            onClick={onCancel}
            className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            className="flex-1 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
          >
            End Session
          </button>
        </div>
      </div>
    </div>
  );
}
