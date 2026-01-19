import { Page, expect } from '@playwright/test';

/**
 * Vocabulary Test Helper Functions
 * Reusable utilities for vocabulary E2E tests
 */

export interface FlashcardSetup {
  category?: string;
  difficulty?: string;
  count?: number;
  types?: string[];
  spacedRepetition?: boolean;
}

export interface QuizSetup {
  type?: 'multiple_choice' | 'fill_blank' | 'matching';
  category?: string;
  difficulty?: string;
  count?: number;
}

/**
 * Starts a flashcard session with specified options
 */
export async function startFlashcardSession(page: Page, options: FlashcardSetup = {}) {
  await page.goto('/vocabulary/flashcards');
  await page.waitForSelector('text=Flashcard Session', { timeout: 10000 });

  // Configure session
  if (options.category) {
    await page.getByTestId('fc-category-select').selectOption(options.category);
  }

  if (options.difficulty) {
    await page.getByTestId('fc-difficulty-select').selectOption(options.difficulty);
  }

  if (options.count) {
    await page.getByTestId(`fc-count-${options.count}`).click();
  } else {
    // Default to 5 cards
    await page.getByTestId('fc-count-5').click();
  }

  if (options.types && options.types.length > 0) {
    // First deselect all types
    const allTypes = ['definition', 'translation', 'usage', 'synonym', 'example'];
    for (const type of allTypes) {
      const button = page.getByTestId(`fc-type-${type}`);
      if (await button.isVisible({ timeout: 1000 }).catch(() => false)) {
        const classes = await button.getAttribute('class');
        if (classes?.includes('border-primary-500')) {
          await button.click();
          await page.waitForTimeout(200);
        }
      }
    }

    // Then select specified types
    for (const type of options.types) {
      await page.getByTestId(`fc-type-${type}`).click();
      await page.waitForTimeout(200);
    }
  }

  if (options.spacedRepetition !== undefined) {
    const toggle = page.getByTestId('fc-spaced-repetition-toggle');
    const isChecked = await toggle.isChecked().catch(() => false);
    if (isChecked !== options.spacedRepetition) {
      await toggle.click();
    }
  }

  // Start session
  await page.getByTestId('fc-start-btn').click();
  await page.waitForTimeout(3000);

  // Check if session started successfully
  const hasCard = await page.getByTestId('show-answer-btn').isVisible({ timeout: 5000 }).catch(() => false);
  return hasCard;
}

/**
 * Flips the current flashcard to show the answer
 */
export async function flipCard(page: Page) {
  const showAnswerBtn = page.getByTestId('show-answer-btn');
  await showAnswerBtn.click();
  await page.waitForTimeout(500);
}

/**
 * Rates the current flashcard (1-5)
 */
export async function rateCard(page: Page, rating: 1 | 2 | 3 | 4 | 5) {
  // First flip the card if not already flipped
  const showAnswerBtn = page.getByTestId('show-answer-btn');
  if (await showAnswerBtn.isVisible({ timeout: 1000 }).catch(() => false)) {
    await flipCard(page);
  }

  // Submit rating
  const rateButton = page.getByTestId(`rate-${rating}-btn`);
  await rateButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Rates a card using keyboard shortcut (1-5)
 */
export async function rateCardWithKeyboard(page: Page, rating: 1 | 2 | 3 | 4 | 5) {
  // First flip the card if not already flipped
  const showAnswerBtn = page.getByTestId('show-answer-btn');
  if (await showAnswerBtn.isVisible({ timeout: 1000 }).catch(() => false)) {
    await flipCard(page);
  }

  // Press rating key
  await page.keyboard.press(rating.toString());
  await page.waitForTimeout(1000);
}

/**
 * Ends the current flashcard session
 */
export async function endFlashcardSession(page: Page) {
  const endButton = page.getByTestId('end-session-btn');
  await endButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Creates a new vocabulary list
 */
export async function createList(page: Page, name: string, description?: string, isPublic?: boolean) {
  await page.goto('/vocabulary/lists');
  await page.waitForSelector('text=/My Vocabulary Lists|lists/i', { timeout: 10000 });
  await page.waitForTimeout(1000);

  // Open create modal
  const createBtn = page.getByTestId('create-list-btn');
  await createBtn.click();
  await page.waitForTimeout(500);

  // Wait for modal
  await expect(page.getByTestId('list-name-input')).toBeVisible({ timeout: 5000 });

  // Fill in details
  await page.getByTestId('list-name-input').fill(name);

  if (description) {
    await page.getByTestId('list-description-input').fill(description);
  }

  if (isPublic !== undefined) {
    const toggle = page.getByTestId('list-public-toggle');
    const isChecked = await toggle.isChecked().catch(() => false);
    if (isChecked !== isPublic) {
      await toggle.click();
    }
  }

  // Submit
  await page.getByTestId('create-list-submit-btn').click();
  await page.waitForTimeout(3000);

  // Return true if list was created successfully
  const hasNewList = await page.locator(`h3:has-text("${name}")`).isVisible({ timeout: 5000 }).catch(() => false);
  return hasNewList;
}

/**
 * Adds a word to a list
 */
export async function addWordToList(page: Page, wordId: number, listId: number) {
  // Navigate to word browser
  await page.goto('/vocabulary');
  await page.waitForSelector('text=Vocabulary', { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Find the word card
  const wordCard = page.locator(`[data-testid="word-card-${wordId}"]`);

  // Click add to list button
  const addButton = wordCard.locator('[data-testid="add-to-list-btn"]');
  await addButton.click();
  await page.waitForTimeout(500);

  // Select list from dropdown
  const listSelect = page.getByTestId('list-select-dropdown');
  await listSelect.selectOption(listId.toString());

  // Confirm
  const confirmButton = page.getByTestId('add-to-list-confirm-btn');
  await confirmButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Removes a word from a list
 */
export async function removeWordFromList(page: Page, wordId: number, listId: number) {
  // Navigate to list detail page
  await page.goto(`/vocabulary/lists/${listId}`);
  await page.waitForTimeout(2000);

  // Find the word card
  const wordCard = page.locator(`[data-testid="list-word-${wordId}"]`);

  // Click remove button
  const removeButton = wordCard.locator('[data-testid="remove-from-list-btn"]');
  await removeButton.click();
  await page.waitForTimeout(500);

  // Confirm removal
  const confirmButton = page.getByTestId('remove-word-confirm-btn');
  await confirmButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Deletes a vocabulary list
 */
export async function deleteList(page: Page, listId: number) {
  // Navigate to list detail page
  await page.goto(`/vocabulary/lists/${listId}`);
  await page.waitForTimeout(2000);

  // Click delete button
  const deleteButton = page.getByTestId('delete-list-btn');
  await deleteButton.click();
  await page.waitForTimeout(500);

  // Confirm deletion
  const confirmButton = page.getByTestId('delete-list-confirm-btn');
  await confirmButton.click();
  await page.waitForTimeout(1000);

  // Should redirect to lists page
  await expect(page).toHaveURL(/vocabulary\/lists$/, { timeout: 5000 });
}

/**
 * Starts a quiz with specified options
 */
export async function startQuiz(page: Page, options: QuizSetup = {}) {
  await page.goto('/vocabulary/quiz');
  await page.waitForSelector('text=Vocabulary Quiz', { timeout: 10000 });

  // Select quiz type
  if (options.type) {
    await page.getByTestId(`quiz-type-${options.type}`).click();
    await page.waitForTimeout(300);
  }

  // Configure options
  if (options.category) {
    await page.getByTestId('quiz-category-select').selectOption(options.category);
  }

  if (options.difficulty) {
    await page.getByTestId('quiz-difficulty-select').selectOption(options.difficulty);
  }

  if (options.count) {
    await page.getByTestId(`quiz-count-${options.count}`).click();
  } else {
    // Default to 5 questions
    await page.getByTestId('quiz-count-5').click();
  }

  // Start quiz
  await page.getByTestId('quiz-start-btn').click();
  await page.waitForTimeout(8000);

  // Check if quiz started
  const hasQuiz = await page.locator('text=Question').isVisible({ timeout: 5000 }).catch(() => false);
  return hasQuiz;
}

/**
 * Submits an answer to a quiz question
 */
export async function submitQuizAnswer(page: Page, answer: string | number) {
  // Determine question type and submit answer
  const multipleChoiceRadio = page.locator('input[type="radio"]').first();
  const fillBlankInput = page.locator('input[type="text"]').first();

  if (await multipleChoiceRadio.isVisible({ timeout: 1000 }).catch(() => false)) {
    // Multiple choice - click radio button
    if (typeof answer === 'number') {
      await page.locator(`input[type="radio"][value="${answer}"]`).click();
    } else {
      await multipleChoiceRadio.click();
    }
  } else if (await fillBlankInput.isVisible({ timeout: 1000 }).catch(() => false)) {
    // Fill in the blank
    await fillBlankInput.fill(answer.toString());
  }

  // Submit answer
  const submitButton = page.getByTestId('quiz-submit-answer-btn');
  await submitButton.click();
  await page.waitForTimeout(2000);
}

/**
 * Continues to the next quiz question
 */
export async function continueQuiz(page: Page) {
  const continueButton = page.getByTestId('quiz-continue-btn');
  await continueButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Ends the current quiz
 */
export async function endQuiz(page: Page) {
  const endButton = page.getByTestId('end-quiz-btn');
  await endButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Opens the word detail modal
 */
export async function openWordDetailModal(page: Page, wordId: number) {
  // Navigate to vocabulary browser
  await page.goto('/vocabulary');
  await page.waitForSelector('text=Vocabulary', { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Click on word card
  const wordCard = page.locator(`[data-testid="word-card-${wordId}"]`);
  await wordCard.click();
  await page.waitForTimeout(1000);

  // Check if modal opened
  const hasModal = await page.getByTestId('word-detail-modal').isVisible({ timeout: 3000 }).catch(() => false);
  return hasModal;
}

/**
 * Closes the word detail modal
 */
export async function closeWordDetailModal(page: Page) {
  const closeButton = page.getByTestId('word-detail-modal-close-btn');
  await closeButton.click();
  await page.waitForTimeout(500);
}

/**
 * Gets the flashcard session state from localStorage
 */
export async function getFlashcardSessionFromLocalStorage(page: Page) {
  const stored = await page.evaluate(() =>
    localStorage.getItem('german-learning-vocabulary-store')
  );

  if (!stored) {
    return null;
  }

  try {
    const data = JSON.parse(stored);
    return data.flashcardSession || null;
  } catch {
    return null;
  }
}

/**
 * Gets the current card number
 */
export async function getCurrentCardNumber(page: Page): Promise<number> {
  const cardText = await page.locator('[data-testid="card-progress"]').textContent().catch(() => '1 / 5');
  const match = cardText?.match(/(\d+)\s*\/\s*\d+/);
  return match ? parseInt(match[1], 10) : 1;
}

/**
 * Gets the total number of cards
 */
export async function getTotalCards(page: Page): Promise<number> {
  const cardText = await page.locator('[data-testid="card-progress"]').textContent().catch(() => '1 / 5');
  const match = cardText?.match(/\d+\s*\/\s*(\d+)/);
  return match ? parseInt(match[1], 10) : 5;
}

/**
 * Gets the current streak from flashcard session
 */
export async function getFlashcardStreak(page: Page): Promise<number> {
  const streakText = await page.locator('[data-testid="flashcard-streak"]').textContent().catch(() => '0');
  return parseInt(streakText || '0', 10);
}

/**
 * Checks if a streak milestone notification is visible
 */
export async function hasStreakMilestoneNotification(page: Page): Promise<boolean> {
  return await page.locator('text=/streak milestone|consecutive/i').isVisible({ timeout: 2000 }).catch(() => false);
}

/**
 * Gets the current quiz score
 */
export async function getQuizScore(page: Page): Promise<{ correct: number; total: number }> {
  const scoreText = await page.locator('[data-testid="quiz-score"]').textContent().catch(() => '0 / 5');
  const match = scoreText?.match(/(\d+)\s*\/\s*(\d+)/);

  return {
    correct: match ? parseInt(match[1], 10) : 0,
    total: match ? parseInt(match[2], 10) : 5,
  };
}

/**
 * Checks if the flashcard session is paused
 */
export async function isFlashcardSessionPaused(page: Page): Promise<boolean> {
  return await page.locator('[data-testid="flashcard-paused-overlay"]').isVisible({ timeout: 1000 }).catch(() => false);
}

/**
 * Pauses the flashcard session
 */
export async function pauseFlashcardSession(page: Page) {
  const pauseButton = page.getByTestId('pause-flashcard-btn');
  await pauseButton.click();
  await page.waitForTimeout(500);
}

/**
 * Resumes the flashcard session
 */
export async function resumeFlashcardSession(page: Page) {
  const resumeButton = page.getByTestId('resume-flashcard-btn');
  await resumeButton.click();
  await page.waitForTimeout(500);
}

/**
 * Gets the thinking time (time to flip card)
 */
export async function getFlipTime(page: Page): Promise<number> {
  const timeText = await page.locator('[data-testid="flip-time"]').textContent().catch(() => '0s');
  const match = timeText?.match(/(\d+)s/);
  return match ? parseInt(match[1], 10) : 0;
}

/**
 * Checks if undo rating button is visible
 */
export async function hasUndoRatingButton(page: Page): Promise<boolean> {
  return await page.getByTestId('undo-rating-btn').isVisible({ timeout: 1000 }).catch(() => false);
}

/**
 * Undos the last rating
 */
export async function undoLastRating(page: Page) {
  const undoButton = page.getByTestId('undo-rating-btn');
  await undoButton.click();
  await page.waitForTimeout(1000);
}

/**
 * Gets word lists count
 */
export async function getListsCount(page: Page): Promise<number> {
  await page.goto('/vocabulary/lists');
  await page.waitForTimeout(2000);

  const listCards = await page.locator('[data-testid^="list-card-"]').count();
  return listCards;
}

/**
 * Searches for a word in the browser
 */
export async function searchWord(page: Page, searchTerm: string) {
  await page.goto('/vocabulary');
  await page.waitForSelector('text=Vocabulary', { timeout: 10000 });

  const searchInput = page.getByTestId('word-search-input');
  await searchInput.fill(searchTerm);
  await page.waitForTimeout(500);
}

/**
 * Filters words by category
 */
export async function filterByCategory(page: Page, category: string) {
  const categoryFilter = page.getByTestId('word-category-filter');
  await categoryFilter.selectOption(category);
  await page.waitForTimeout(500);
}

/**
 * Filters words by difficulty
 */
export async function filterByDifficulty(page: Page, difficulty: string) {
  const difficultyFilter = page.getByTestId('word-difficulty-filter');
  await difficultyFilter.selectOption(difficulty);
  await page.waitForTimeout(500);
}
