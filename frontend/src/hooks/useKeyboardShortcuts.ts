import { useEffect, useCallback } from 'react';

// ========== TYPES ==========

export interface KeyboardShortcut {
  key: string; // The key to listen for (e.g., 'Enter', 'Escape', 'f')
  modifiers?: {
    ctrl?: boolean;
    shift?: boolean;
    alt?: boolean;
    meta?: boolean;
  };
  action: () => void;
  description?: string; // For displaying in help
  preventDefault?: boolean;
  allowInInput?: boolean; // Allow shortcut even when focused on input
}

export interface ShortcutContext {
  id: string;
  shortcuts: KeyboardShortcut[];
  enabled?: boolean;
  priority?: number; // Higher priority contexts handle events first
}

interface UseKeyboardShortcutsOptions {
  enabled?: boolean;
  contexts?: ShortcutContext[];
}

// ========== HELPER FUNCTIONS ==========

function matchesShortcut(event: KeyboardEvent, shortcut: KeyboardShortcut): boolean {
  const { key, modifiers = {} } = shortcut;

  // Check the key (case-insensitive for letters)
  const pressedKey = event.key.toLowerCase();
  const targetKey = key.toLowerCase();

  if (pressedKey !== targetKey) {
    return false;
  }

  // Check modifiers
  const { ctrl = false, shift = false, alt = false, meta = false } = modifiers;

  if (ctrl !== (event.ctrlKey || event.metaKey)) return false;
  if (shift !== event.shiftKey) return false;
  if (alt !== event.altKey) return false;
  if (meta !== event.metaKey) return false;

  return true;
}

function isInputElement(element: EventTarget | null): boolean {
  if (!element || !(element instanceof HTMLElement)) return false;

  const tagName = element.tagName.toLowerCase();
  const isInput = tagName === 'input' || tagName === 'textarea' || tagName === 'select';
  const isEditable = element.isContentEditable;

  return isInput || isEditable;
}

// ========== MAIN HOOK ==========

/**
 * Hook for managing keyboard shortcuts with context support.
 *
 * Features:
 * - Multiple context support (e.g., 'practice', 'feedback', 'focus-mode')
 * - Modifier key support (Ctrl, Shift, Alt, Meta)
 * - Input element detection (prevent shortcuts when typing)
 * - Priority-based handling
 *
 * @example
 * ```tsx
 * useKeyboardShortcuts({
 *   contexts: [
 *     {
 *       id: 'practice',
 *       enabled: sessionState === 'active',
 *       shortcuts: [
 *         { key: 'Enter', action: handleSubmit, description: 'Submit answer' },
 *         { key: 'Escape', action: handleEndSession, description: 'End session' },
 *       ],
 *     },
 *     {
 *       id: 'feedback',
 *       enabled: sessionState === 'feedback',
 *       shortcuts: [
 *         { key: ' ', action: handleNext, description: 'Next exercise' },
 *         { key: 'Enter', action: handleNext, description: 'Next exercise' },
 *       ],
 *     },
 *   ],
 * });
 * ```
 */
export function useKeyboardShortcuts(options: UseKeyboardShortcutsOptions = {}) {
  const { enabled = true, contexts = [] } = options;

  const handleKeyDown = useCallback(
    (event: KeyboardEvent) => {
      if (!enabled) return;

      // Sort contexts by priority (higher first)
      const sortedContexts = [...contexts]
        .filter((ctx) => ctx.enabled !== false)
        .sort((a, b) => (b.priority || 0) - (a.priority || 0));

      // Check if we're in an input element
      const inInput = isInputElement(event.target);

      for (const context of sortedContexts) {
        for (const shortcut of context.shortcuts) {
          if (matchesShortcut(event, shortcut)) {
            // Skip if in input and not allowed
            if (inInput && !shortcut.allowInInput) {
              continue;
            }

            // Prevent default if specified (default true)
            if (shortcut.preventDefault !== false) {
              event.preventDefault();
            }

            // Execute action
            shortcut.action();
            return; // Stop after first match
          }
        }
      }
    },
    [enabled, contexts]
  );

  useEffect(() => {
    if (!enabled) return;

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [enabled, handleKeyDown]);
}

// ========== PRESET CONTEXTS ==========

/**
 * Create a practice session context for grammar practice.
 */
export function createPracticeContext(handlers: {
  onSubmit: () => void;
  onEndSession: () => void;
  onHint?: () => void;
  onToggleBookmark?: () => void;
  onToggleNotes?: () => void;
  onToggleFocusMode?: () => void;
  onPause?: () => void;
}): ShortcutContext {
  const shortcuts: KeyboardShortcut[] = [
    {
      key: 'Enter',
      action: handlers.onSubmit,
      description: 'Submit answer',
    },
    {
      key: 'Escape',
      action: handlers.onEndSession,
      description: 'End session',
      allowInInput: true,
    },
  ];

  if (handlers.onHint) {
    shortcuts.push({
      key: 'h',
      action: handlers.onHint,
      description: 'Show hint',
    });
  }

  if (handlers.onToggleBookmark) {
    shortcuts.push({
      key: 'b',
      action: handlers.onToggleBookmark,
      description: 'Bookmark exercise',
    });
  }

  if (handlers.onToggleNotes) {
    shortcuts.push({
      key: 'n',
      action: handlers.onToggleNotes,
      description: 'Toggle notes panel',
    });
  }

  if (handlers.onToggleFocusMode) {
    shortcuts.push({
      key: 'f',
      action: handlers.onToggleFocusMode,
      description: 'Toggle focus mode',
    });
  }

  if (handlers.onPause) {
    shortcuts.push({
      key: 'p',
      action: handlers.onPause,
      description: 'Pause session',
    });
  }

  return {
    id: 'practice',
    shortcuts,
    priority: 10,
  };
}

/**
 * Create a feedback context for viewing exercise feedback.
 */
export function createFeedbackContext(handlers: {
  onNext: () => void;
  onEndSession?: () => void;
  onToggleBookmark?: () => void;
  onToggleNotes?: () => void;
}): ShortcutContext {
  const shortcuts: KeyboardShortcut[] = [
    {
      key: ' ',
      action: handlers.onNext,
      description: 'Next exercise',
      allowInInput: false,
    },
    {
      key: 'Enter',
      action: handlers.onNext,
      description: 'Next exercise',
      allowInInput: false,
    },
  ];

  // Add ESC to end session from feedback state
  if (handlers.onEndSession) {
    shortcuts.push({
      key: 'Escape',
      action: handlers.onEndSession,
      description: 'End session',
      allowInInput: true,
    });
  }

  if (handlers.onToggleBookmark) {
    shortcuts.push({
      key: 'b',
      action: handlers.onToggleBookmark,
      description: 'Bookmark exercise',
    });
  }

  if (handlers.onToggleNotes) {
    shortcuts.push({
      key: 'n',
      action: handlers.onToggleNotes,
      description: 'Toggle notes panel',
    });
  }

  return {
    id: 'feedback',
    shortcuts,
    priority: 10,
  };
}

/**
 * Create a focus mode context with exit shortcut.
 */
export function createFocusModeContext(handlers: {
  onExit: () => void;
}): ShortcutContext {
  return {
    id: 'focus-mode',
    shortcuts: [
      {
        key: 'Escape',
        action: handlers.onExit,
        description: 'Exit focus mode',
        allowInInput: true,
      },
    ],
    priority: 100, // High priority to override other contexts
  };
}

/**
 * Create a paused state context.
 */
export function createPausedContext(handlers: {
  onResume: () => void;
}): ShortcutContext {
  return {
    id: 'paused',
    shortcuts: [
      {
        key: 'p',
        action: handlers.onResume,
        description: 'Resume session',
      },
      {
        key: ' ',
        action: handlers.onResume,
        description: 'Resume session',
      },
    ],
    priority: 50,
  };
}

// ========== SHORTCUT DISPLAY HOOK ==========

interface ShortcutDisplay {
  key: string;
  description: string;
}

/**
 * Hook to get displayable shortcuts for the current context.
 */
export function useShortcutDisplay(contexts: ShortcutContext[]): ShortcutDisplay[] {
  const enabledContexts = contexts.filter((ctx) => ctx.enabled !== false);
  const shortcuts: ShortcutDisplay[] = [];
  const seenKeys = new Set<string>();

  for (const context of enabledContexts) {
    for (const shortcut of context.shortcuts) {
      if (!seenKeys.has(shortcut.key) && shortcut.description) {
        shortcuts.push({
          key: formatKeyDisplay(shortcut.key, shortcut.modifiers),
          description: shortcut.description,
        });
        seenKeys.add(shortcut.key);
      }
    }
  }

  return shortcuts;
}

function formatKeyDisplay(
  key: string,
  modifiers?: KeyboardShortcut['modifiers']
): string {
  const parts: string[] = [];

  if (modifiers?.ctrl) parts.push('Ctrl');
  if (modifiers?.shift) parts.push('Shift');
  if (modifiers?.alt) parts.push('Alt');
  if (modifiers?.meta) parts.push('Cmd');

  // Format special keys
  const keyDisplay =
    key === ' '
      ? 'Space'
      : key === 'Escape'
      ? 'Esc'
      : key.length === 1
      ? key.toUpperCase()
      : key;

  parts.push(keyDisplay);

  return parts.join('+');
}
