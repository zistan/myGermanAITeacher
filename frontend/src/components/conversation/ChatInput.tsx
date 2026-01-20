import { useState, useRef, useEffect, KeyboardEvent } from 'react';
import { Send } from 'lucide-react';
import { GermanKeyboardHelper } from './GermanKeyboardHelper';

interface ChatInputProps {
  onSend: (message: string, requestFeedback: boolean) => void;
  disabled?: boolean;
  placeholder?: string;
}

const MAX_CHARS = 5000;
const MAX_LINES = 5;

export function ChatInput({
  onSend,
  disabled = false,
  placeholder = 'Schreiben Sie eine Nachricht auf Deutsch...',
}: ChatInputProps) {
  const [message, setMessage] = useState('');
  const [requestFeedback, setRequestFeedback] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  /**
   * Auto-resize textarea based on content
   */
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      const scrollHeight = textareaRef.current.scrollHeight;
      const lineHeight = 24; // Approximate line height in pixels
      const maxHeight = lineHeight * MAX_LINES;
      textareaRef.current.style.height = `${Math.min(scrollHeight, maxHeight)}px`;
    }
  }, [message]);

  /**
   * Handle send message
   */
  const handleSend = () => {
    const trimmedMessage = message.trim();
    if (trimmedMessage && !disabled) {
      onSend(trimmedMessage, requestFeedback);
      setMessage('');
      setRequestFeedback(false);
    }
  };

  /**
   * Handle keyboard shortcuts
   */
  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    // Alt+A -> ä
    if (e.altKey && e.key.toLowerCase() === 'a') {
      e.preventDefault();
      insertCharacter('ä');
      return;
    }

    // Alt+O -> ö
    if (e.altKey && e.key.toLowerCase() === 'o') {
      e.preventDefault();
      insertCharacter('ö');
      return;
    }

    // Alt+U -> ü
    if (e.altKey && e.key.toLowerCase() === 'u') {
      e.preventDefault();
      insertCharacter('ü');
      return;
    }

    // Alt+S -> ß
    if (e.altKey && e.key.toLowerCase() === 's') {
      e.preventDefault();
      insertCharacter('ß');
      return;
    }

    // Enter to send (Shift+Enter for newline)
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  /**
   * Insert a German character at cursor position
   */
  const insertCharacter = (char: string) => {
    if (!textareaRef.current) return;

    const start = textareaRef.current.selectionStart;
    const end = textareaRef.current.selectionEnd;
    const newMessage =
      message.substring(0, start) + char + message.substring(end);

    if (newMessage.length <= MAX_CHARS) {
      setMessage(newMessage);

      // Move cursor after inserted character
      setTimeout(() => {
        if (textareaRef.current) {
          textareaRef.current.selectionStart = start + char.length;
          textareaRef.current.selectionEnd = start + char.length;
          textareaRef.current.focus();
        }
      }, 0);
    }
  };

  const charCount = message.length;
  const isOverLimit = charCount > MAX_CHARS;
  const canSend = message.trim().length > 0 && !isOverLimit && !disabled;

  return (
    <div className="border-t border-gray-200 bg-white px-4 py-3">
      {/* German Keyboard Helper */}
      <div className="mb-2">
        <GermanKeyboardHelper onInsertChar={insertCharacter} />
      </div>

      {/* Textarea */}
      <div className="relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          className={`w-full px-4 py-3 pr-12 border rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            isOverLimit
              ? 'border-red-300 focus:ring-red-500'
              : 'border-gray-300'
          } ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}`}
          rows={1}
          style={{ minHeight: '48px', maxHeight: `${24 * MAX_LINES}px` }}
        />

        {/* Send button */}
        <button
          onClick={handleSend}
          disabled={!canSend}
          className={`absolute right-2 bottom-2 p-2 rounded-lg transition-colors ${
            canSend
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-200 text-gray-400 cursor-not-allowed'
          }`}
          title="Send message (Enter)"
        >
          <Send className="h-5 w-5" />
        </button>
      </div>

      {/* Footer with character count and grammar feedback checkbox */}
      <div className="flex items-center justify-between mt-2">
        <label className="flex items-center gap-2 text-sm text-gray-600 cursor-pointer">
          <input
            type="checkbox"
            checked={requestFeedback}
            onChange={(e) => setRequestFeedback(e.target.checked)}
            disabled={disabled}
            className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span>Request Grammar Feedback</span>
        </label>

        <div
          className={`text-sm ${
            isOverLimit
              ? 'text-red-600 font-medium'
              : charCount > MAX_CHARS * 0.9
              ? 'text-orange-600'
              : 'text-gray-500'
          }`}
        >
          {charCount} / {MAX_CHARS}
        </div>
      </div>

      {/* Help text */}
      <div className="mt-2 text-xs text-gray-500 flex items-center justify-between">
        <span>Press Enter to send, Shift+Enter for new line</span>
        <span className="hidden md:inline">
          Alt+A/O/U/S for German characters
        </span>
      </div>
    </div>
  );
}
