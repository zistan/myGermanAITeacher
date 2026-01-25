import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { PracticeSessionPage } from '../PracticeSessionPage';
import grammarService from '../../../api/services/grammarService';
import { useGrammarStore } from '../../../store/grammarStore';
import { useNotificationStore } from '../../../store/notificationStore';

// Mock services
vi.mock('../../../api/services/grammarService');
vi.mock('../../../store/notificationStore');
vi.mock('../../../store/grammarStore');

// Mock useSessionPersistence hook
vi.mock('../../../hooks/useSessionPersistence', () => ({
  useSessionPersistence: () => ({
    hasIncompleteSession: false,
    restoreSession: vi.fn(),
    clearSession: vi.fn(),
  }),
  useSessionTimer: () => ({
    elapsedFormatted: '00:00',
    isPaused: false,
  }),
}));

// Mock useKeyboardShortcuts hook
vi.mock('../../../hooks/useKeyboardShortcuts', () => ({
  useKeyboardShortcuts: vi.fn(),
  createPracticeContext: vi.fn(() => ({ shortcuts: [] })),
  createFeedbackContext: vi.fn(() => ({ shortcuts: [] })),
  createPausedContext: vi.fn(() => ({ shortcuts: [] })),
  createFocusModeContext: vi.fn(() => ({ shortcuts: [] })),
  useShortcutDisplay: vi.fn(() => []),
}));

describe('PracticeSessionPage - Session Duplication Fix', () => {
  const mockAddToast = vi.fn();
  const mockNavigate = vi.fn();

  // Mock store state
  const mockStoreState = {
    sessionState: 'idle' as const,
    setSessionState: vi.fn(),
    startSession: vi.fn(),
    setCurrentExercise: vi.fn(),
    recordAnswer: vi.fn(),
    pauseSession: vi.fn(),
    resumeSession: vi.fn(),
    endSession: vi.fn(),
    clearSession: vi.fn(),
    isFocusMode: false,
    toggleFocusMode: vi.fn(),
    autoAdvanceEnabled: false,
    autoAdvanceDelay: 2,
    setAutoAdvance: vi.fn(),
    toggleBookmark: vi.fn(),
    isBookmarked: vi.fn(() => false),
    getNotesCount: vi.fn(() => 0),
    currentSession: null,
    currentExercise: null,
  };

  beforeEach(() => {
    // Reset mocks
    vi.clearAllMocks();

    // Mock store
    vi.mocked(useGrammarStore).mockReturnValue(mockStoreState as any);
    vi.mocked(useNotificationStore).mockReturnValue({ addToast: mockAddToast } as any);

    // Mock useNavigate
    vi.mock('react-router-dom', async () => {
      const actual = await vi.importActual('react-router-dom');
      return {
        ...actual,
        useNavigate: () => mockNavigate,
        useSearchParams: () => [new URLSearchParams(), vi.fn()],
      };
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('should show setup modal on mount (no auto-create)', async () => {
    render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Wait for setup modal to appear
    await waitFor(() => {
      expect(screen.getByText('Start Grammar Practice')).toBeInTheDocument();
    });

    // Verify setup modal is shown
    expect(screen.getByText(/Ready to practice grammar/i)).toBeInTheDocument();
    expect(screen.getByTestId('confirm-start-button')).toBeInTheDocument();

    // Verify NO automatic API call (only called when user clicks button)
    expect(grammarService.startPracticeSession).not.toHaveBeenCalled();
  });

  it('should handle 409 conflict without infinite loop', async () => {
    const mockConflictError = {
      response: {
        status: 409,
        data: {
          detail: {
            message: 'Active grammar session already exists',
            session_id: 123,
            started_at: '2026-01-25T10:00:00Z',
            age_hours: 0.5,
          },
        },
      },
      status: 409,
      detail: {
        message: 'Active grammar session already exists',
        session_id: 123,
        started_at: '2026-01-25T10:00:00Z',
        age_hours: 0.5,
      },
    };

    vi.mocked(grammarService.startPracticeSession).mockRejectedValue(mockConflictError);

    render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Wait for setup modal
    await waitFor(() => {
      expect(screen.getByTestId('confirm-start-button')).toBeInTheDocument();
    });

    // Click start button
    fireEvent.click(screen.getByTestId('confirm-start-button'));

    // Wait for conflict modal (NOT infinite loop)
    await waitFor(() => {
      expect(screen.getByText('Active Session Detected')).toBeInTheDocument();
    });

    // Verify conflict modal content
    expect(screen.getByText(/active grammar session/i)).toBeInTheDocument();
    expect(screen.getByText(/ID: 123/)).toBeInTheDocument();

    // Verify only 1 API call was made (no loop)
    expect(grammarService.startPracticeSession).toHaveBeenCalledTimes(1);

    // Wait 5 seconds to ensure no additional calls (would indicate loop)
    await new Promise(resolve => setTimeout(resolve, 5000));
    expect(grammarService.startPracticeSession).toHaveBeenCalledTimes(1);
  });

  it('should show setup modal after conflict cleanup (no auto-retry)', async () => {
    const mockConflictError = {
      response: {
        status: 409,
        data: {
          detail: {
            message: 'Active grammar session already exists',
            session_id: 456,
            started_at: '2026-01-25T10:00:00Z',
            age_hours: 1.2,
          },
        },
      },
      status: 409,
      detail: {
        message: 'Active grammar session already exists',
        session_id: 456,
        started_at: '2026-01-25T10:00:00Z',
        age_hours: 1.2,
      },
    };

    vi.mocked(grammarService.startPracticeSession).mockRejectedValueOnce(mockConflictError);
    vi.mocked(grammarService.deleteAbandonedSession).mockResolvedValue(undefined);

    render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Wait for setup modal
    await waitFor(() => {
      expect(screen.getByTestId('confirm-start-button')).toBeInTheDocument();
    });

    // Start session (triggers 409)
    fireEvent.click(screen.getByTestId('confirm-start-button'));

    // Wait for conflict modal
    await waitFor(() => {
      expect(screen.getByText('Active Session Detected')).toBeInTheDocument();
    });

    // Click "Clean Up & Start Fresh"
    fireEvent.click(screen.getByText('Clean Up & Start Fresh'));

    // Wait for cleanup to complete
    await waitFor(() => {
      expect(grammarService.deleteAbandonedSession).toHaveBeenCalledWith(456);
    });

    // Verify setup modal is shown again (NO AUTO-RETRY)
    await waitFor(() => {
      expect(screen.getByText('Start Grammar Practice')).toBeInTheDocument();
    });

    // Verify only 1 API call to startPracticeSession (no automatic retry)
    expect(grammarService.startPracticeSession).toHaveBeenCalledTimes(1);
  });

  it('should create session only when user clicks Start button', async () => {
    const mockSession = {
      session_id: 789,
      total_exercises: 10,
      current_exercise: {
        id: 1,
        exercise_type: 'fill_blank',
        difficulty_level: 'B2',
        prompt: 'Test prompt',
        instruction: 'Fill the blank',
        correct_answer: 'test',
        topic_id: 1,
      },
    };

    vi.mocked(grammarService.startPracticeSession).mockResolvedValue(mockSession as any);

    render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Wait for setup modal
    await waitFor(() => {
      expect(screen.getByTestId('confirm-start-button')).toBeInTheDocument();
    });

    // Verify NO API call yet (user hasn't clicked button)
    expect(grammarService.startPracticeSession).not.toHaveBeenCalled();

    // Click start button
    fireEvent.click(screen.getByTestId('confirm-start-button'));

    // Now API should be called
    await waitFor(() => {
      expect(grammarService.startPracticeSession).toHaveBeenCalledTimes(1);
    });

    // Verify session creation in store
    expect(mockStoreState.startSession).toHaveBeenCalledWith(789);
  });

  it('should not trigger useEffect on state changes (empty deps)', async () => {
    let renderCount = 0;

    const TestWrapper = () => {
      renderCount++;
      return (
        <BrowserRouter>
          <PracticeSessionPage />
        </BrowserRouter>
      );
    };

    const { rerender } = render(<TestWrapper />);

    // Wait for initial mount
    await waitFor(() => {
      expect(screen.getByText('Start Grammar Practice')).toBeInTheDocument();
    });

    const initialRenderCount = renderCount;

    // Simulate state change in store
    mockStoreState.sessionState = 'loading';
    rerender(<TestWrapper />);

    // Wait a bit
    await new Promise(resolve => setTimeout(resolve, 500));

    // Verify useEffect didn't run again (no additional setup modal toggles)
    // Only the state change should cause a rerender, not a useEffect rerun
    expect(screen.queryByText('Start Grammar Practice')).toBeInTheDocument();

    // Verify no additional API calls (would indicate useEffect rerun)
    expect(grammarService.startPracticeSession).not.toHaveBeenCalled();
  });
});

describe('PracticeSessionPage - React StrictMode Compatibility', () => {
  it('should handle StrictMode double-invoke without duplicates', async () => {
    // Simulate StrictMode by calling useEffect twice
    const { unmount } = render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Unmount and remount (simulates StrictMode)
    unmount();

    render(
      <BrowserRouter>
        <PracticeSessionPage />
      </BrowserRouter>
    );

    // Wait for setup modal
    await waitFor(() => {
      expect(screen.getByText('Start Grammar Practice')).toBeInTheDocument();
    });

    // Verify only 1 modal shown (no duplicates)
    const modals = screen.getAllByText('Start Grammar Practice');
    expect(modals).toHaveLength(1);

    // Verify no API calls (user hasn't clicked button)
    expect(grammarService.startPracticeSession).not.toHaveBeenCalled();
  });
});
