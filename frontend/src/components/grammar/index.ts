// Grammar Components - Barrel Export

// Exercise rendering
export { ExerciseRenderer } from './ExerciseRenderer';

// Feedback display
export { FeedbackDisplay } from './FeedbackDisplay';

// Session header
export { SessionHeader } from './SessionHeader';

// Text diff visualization
export { TextDiff, CompactDiff } from './TextDiff';
export type { TextDiffProps, CompactDiffProps } from './TextDiff';

// Notes panel
export { NotesPanel, NotesToggleButton, InlineNotesDisplay } from './NotesPanel';
export type { NotesPanelProps, NotesToggleButtonProps, InlineNotesDisplayProps } from './NotesPanel';

// Focus mode
export { FocusMode, FocusModeToggleButton, PausedOverlay } from './FocusMode';
export type { FocusModeProps, FocusModeToggleButtonProps, PausedOverlayProps } from './FocusMode';
