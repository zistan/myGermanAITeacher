import { Page, expect } from '@playwright/test';

/**
 * Grammar Test Helper Functions
 * Reusable utilities for grammar practice E2E tests
 */

/**
 * Starts a grammar practice session
 * @param page - Playwright page object
 * @param topicId - Optional topic ID to practice specific topic
 */
export async function startGrammarSession(page: Page, topicId?: number) {
  if (topicId) {
    await page.goto(`/grammar/practice?topicId=${topicId}`);
  } else {
    await page.goto('/grammar/practice');
  }

  // Wait for session to initialize
  await page.waitForSelector('text=/Check Answer|error|Failed/i', { timeout: 20000 });

  // Return true if session started successfully
  const hasCheckButton = await page.locator('text=Check Answer').isVisible({ timeout: 3000 }).catch(() => false);
  return hasCheckButton;
}

/**
 * Submits an answer to the current exercise
 * @param page - Playwright page object
 * @param answer - Answer text (if input/textarea type)
 */
export async function submitAnswer(page: Page, answer?: string) {
  // Find the input type
  const textInput = page.locator('input[type="text"]').first();
  const textarea = page.locator('textarea').first();
  const radio = page.locator('input[type="radio"]').first();

  // Fill in answer based on input type
  if (answer) {
    if (await textInput.isVisible({ timeout: 1000 }).catch(() => false)) {
      await textInput.fill(answer);
    } else if (await textarea.isVisible({ timeout: 1000 }).catch(() => false)) {
      await textarea.fill(answer);
    }
  } else {
    // If no answer provided, select first radio if available
    if (await radio.isVisible({ timeout: 1000 }).catch(() => false)) {
      await radio.click();
    }
  }

  // Submit the answer
  const submitButton = page.locator('button:has-text("Check Answer")');
  await expect(submitButton).toBeEnabled({ timeout: 5000 });
  await submitButton.click();

  // Wait for feedback
  await page.waitForSelector('text=/Richtig|Falsch|correct|incorrect|Continue|Next/i', { timeout: 10000 });
}

/**
 * Waits for feedback to be displayed after answer submission
 */
export async function waitForFeedback(page: Page) {
  await expect(page.locator('text=/Richtig|Falsch|correct|incorrect|Feedback/i').first()).toBeVisible({ timeout: 10000 });
}

/**
 * Clicks Continue button to proceed to next exercise
 */
export async function continueToNextExercise(page: Page) {
  await page.getByTestId('continue-button').click();
  await page.waitForTimeout(500);
}

/**
 * Pauses the current practice session
 */
export async function pauseSession(page: Page) {
  // Try button first
  const pauseButton = page.getByTestId('pause-button');
  if (await pauseButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await pauseButton.click();
  } else {
    // Use P key shortcut
    await page.keyboard.press('p');
  }

  // Wait for paused state
  await page.waitForTimeout(500);
}

/**
 * Resumes a paused practice session
 */
export async function resumeSession(page: Page) {
  // Try button first
  const resumeButton = page.getByTestId('resume-button');
  if (await resumeButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await resumeButton.click();
  } else {
    // Use P or Space key
    await page.keyboard.press('p');
  }

  await page.waitForTimeout(500);
}

/**
 * Bookmarks the current exercise
 */
export async function bookmarkExercise(page: Page) {
  // Try button first
  const bookmarkButton = page.getByTestId('bookmark-button');
  if (await bookmarkButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await bookmarkButton.click();
  } else {
    // Use B key shortcut
    await page.keyboard.press('b');
  }

  await page.waitForTimeout(300);
}

/**
 * Opens the notes panel
 */
export async function openNotesPanel(page: Page) {
  // Try button first
  const notesButton = page.getByTestId('notes-button');
  if (await notesButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await notesButton.click();
  } else {
    // Use N key shortcut
    await page.keyboard.press('n');
  }

  // Wait for panel to open
  await page.waitForTimeout(500);
}

/**
 * Closes the notes panel
 */
export async function closeNotesPanel(page: Page) {
  // Try close button first
  const closeButton = page.getByTestId('notes-close-button');
  if (await closeButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await closeButton.click();
  } else {
    // Use N key shortcut again or Escape
    await page.keyboard.press('Escape');
  }

  await page.waitForTimeout(500);
}

/**
 * Enters focus mode
 */
export async function enterFocusMode(page: Page) {
  // Try button first
  const focusButton = page.getByTestId('focus-mode-button');
  if (await focusButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await focusButton.click();
  } else {
    // Use F key shortcut
    await page.keyboard.press('f');
  }

  // Wait for focus mode to activate
  await page.waitForTimeout(500);
}

/**
 * Exits focus mode
 */
export async function exitFocusMode(page: Page) {
  // Try exit button first
  const exitButton = page.getByTestId('exit-focus-mode-button');
  if (await exitButton.isVisible({ timeout: 1000 }).catch(() => false)) {
    await exitButton.click();
  } else {
    // Use F or Escape key
    await page.keyboard.press('Escape');
  }

  await page.waitForTimeout(500);
}

/**
 * Ends the current practice session
 */
export async function endSession(page: Page) {
  const endButton = page.getByTestId('end-session-button');
  await endButton.click();

  // Wait for navigation or completion screen
  await page.waitForSelector('text=/Complete|Results|Topics|grammar/i', { timeout: 10000 });
}

/**
 * Gets the current session state from localStorage
 */
export async function getSessionFromLocalStorage(page: Page) {
  const stored = await page.evaluate(() =>
    localStorage.getItem('german-learning-grammar-store')
  );

  if (!stored) {
    return null;
  }

  try {
    return JSON.parse(stored);
  } catch {
    return null;
  }
}

/**
 * Clears session data from localStorage
 */
export async function clearSessionFromLocalStorage(page: Page) {
  await page.evaluate(() => {
    localStorage.removeItem('german-learning-grammar-store');
  });
}

/**
 * Checks if a session restore prompt is visible
 */
export async function hasRestorePrompt(page: Page): Promise<boolean> {
  return await page.locator('text=/restore|resume|continue/i').first().isVisible({ timeout: 3000 }).catch(() => false);
}

/**
 * Clicks the restore session button
 */
export async function restoreSession(page: Page) {
  const restoreButton = page.getByTestId('restore-session-button');
  await restoreButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Clicks the clear session button (discard saved session)
 */
export async function clearSavedSession(page: Page) {
  const clearButton = page.getByTestId('clear-session-button');
  await clearButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Gets the current streak count from the UI
 */
export async function getCurrentStreak(page: Page): Promise<number> {
  const streakText = await page.locator('[data-testid="streak-count"]').textContent().catch(() => '0');
  return parseInt(streakText || '0', 10);
}

/**
 * Gets the current accuracy percentage from the UI
 */
export async function getCurrentAccuracy(page: Page): Promise<number> {
  const accuracyText = await page.locator('[data-testid="accuracy-value"]').textContent().catch(() => '0%');
  const match = accuracyText?.match(/(\d+)%/);
  return match ? parseInt(match[1], 10) : 0;
}

/**
 * Gets the current points from the UI
 */
export async function getCurrentPoints(page: Page): Promise<number> {
  const pointsText = await page.locator('[data-testid="points-value"]').textContent().catch(() => '0');
  return parseInt(pointsText || '0', 10);
}

/**
 * Checks if a hint is visible for the current exercise
 */
export async function hasHint(page: Page): Promise<boolean> {
  return await page.locator('text=Hint').isVisible({ timeout: 2000 }).catch(() => false);
}

/**
 * Clicks the hint toggle button
 */
export async function toggleHint(page: Page) {
  const hintButton = page.getByTestId('hint-toggle-button');
  await hintButton.click();
  await page.waitForTimeout(300);
}

/**
 * Submits a self-assessment rating (1-3: understand, not-sure, confused)
 */
export async function submitSelfAssessment(page: Page, rating: 'understand' | 'not-sure' | 'confused') {
  const button = page.getByTestId(`self-assessment-${rating}`);
  await button.click();
  await page.waitForTimeout(500);
}

/**
 * Gets elapsed time in seconds from the UI
 */
export async function getElapsedTime(page: Page): Promise<number> {
  const timeText = await page.locator('[data-testid="elapsed-time"]').textContent().catch(() => '0:00');

  // Parse time format MM:SS or HH:MM:SS
  const parts = timeText?.split(':').map(p => parseInt(p, 10)) || [0, 0];

  if (parts.length === 2) {
    // MM:SS
    return parts[0] * 60 + parts[1];
  } else if (parts.length === 3) {
    // HH:MM:SS
    return parts[0] * 3600 + parts[1] * 60 + parts[2];
  }

  return 0;
}

/**
 * Checks if the session is currently paused
 */
export async function isSessionPaused(page: Page): Promise<boolean> {
  return await page.locator('[data-testid="paused-overlay"]').isVisible({ timeout: 1000 }).catch(() => false);
}

/**
 * Checks if focus mode is active
 */
export async function isFocusModeActive(page: Page): Promise<boolean> {
  // Check if sidebar is hidden (focus mode indicator)
  const sidebarHidden = await page.locator('[data-testid="sidebar"]').isHidden().catch(() => false);
  return sidebarHidden;
}

/**
 * Checks if an exercise is bookmarked
 */
export async function isExerciseBookmarked(page: Page): Promise<boolean> {
  return await page.getByTestId('bookmark-icon-filled').isVisible({ timeout: 1000 }).catch(() => false);
}

/**
 * Types notes in the notes panel
 */
export async function typeNotes(page: Page, notes: string) {
  const notesTextarea = page.getByTestId('notes-textarea');
  await notesTextarea.fill(notes);

  // Wait for auto-save (500ms debounce)
  await page.waitForTimeout(700);
}

/**
 * Gets the notes for the current exercise
 */
export async function getCurrentNotes(page: Page): Promise<string> {
  const notesTextarea = page.getByTestId('notes-textarea');
  return await notesTextarea.inputValue().catch(() => '');
}

/**
 * Gets the character count for notes
 */
export async function getNotesCharacterCount(page: Page): Promise<number> {
  const countText = await page.getByTestId('notes-char-count').textContent().catch(() => '0');
  const match = countText?.match(/(\d+)/);
  return match ? parseInt(match[1], 10) : 0;
}
