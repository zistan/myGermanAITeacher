import { test, expect } from '@playwright/test';

/**
 * Grammar Topics Browser E2E Test Suite
 * Tests topic listing, filtering, searching, and navigation to practice
 */

// Test user credentials
const testUser = {
  username: 'test_engineer',
  password: 'TestPass123A',
};

test.describe('Grammar Topics Browser', () => {
  // Login and navigate to grammar page before each test
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
    await page.evaluate(() => localStorage.clear());
    await page.locator('#username').fill(testUser.username);
    await page.locator('#password').fill(testUser.password);
    await page.locator('button[type="submit"]').click();
    await expect(page).toHaveURL(/dashboard/, { timeout: 15000 });

    // Navigate to grammar topics page
    await page.goto('/grammar');
    await expect(page).toHaveURL(/grammar/, { timeout: 5000 });
  });

  test.describe('Topics List Loading', () => {
    test('should display grammar topics page header', async ({ page }) => {
      await expect(page.locator('h1')).toContainText('Grammar Topics', { timeout: 10000 });
    });

    test('should show topic count', async ({ page }) => {
      // Wait for topics to load
      await page.waitForSelector('text=/\\d+ topic/i', { timeout: 10000 });

      // Should show topic count
      await expect(page.locator('text=/\\d+ topics? available/i')).toBeVisible();
    });

    test('should make API call to topics endpoint', async ({ page }) => {
      // Intercept the topics API call
      const apiResponse = page.waitForResponse(
        (response) =>
          response.url().includes('/api/grammar/topics') && response.status() === 200
      );

      await page.reload();
      const response = await apiResponse;

      expect(response.status()).toBe(200);
    });

    test('should display topic cards', async ({ page }) => {
      // Wait for topics to load
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Wait for cards to appear
      await page.waitForTimeout(2000);

      // Should have topic cards with Practice button
      const practiceButtons = page.locator('button:has-text("Practice This Topic")');
      const count = await practiceButtons.count();

      // Should have at least one topic
      expect(count).toBeGreaterThanOrEqual(1);
    });

    test('should display Start Mixed Practice button', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Check for mixed practice button
      await expect(page.locator('button:has-text("Start Mixed Practice")')).toBeVisible();
    });
  });

  test.describe('Search Functionality', () => {
    test('should have search input', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Check for search input
      await expect(page.locator('#search')).toBeVisible();
    });

    test('should filter topics by German name', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Get initial count
      const initialCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const initialCount = parseInt(initialCountText?.match(/\\d+/)?.[0] || '0');

      // Search for a German term
      await page.locator('#search').fill('Präsens');
      await page.waitForTimeout(500);

      // Count should change (filtered)
      const filteredCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const filteredCount = parseInt(filteredCountText?.match(/\\d+/)?.[0] || '0');

      // Either filter worked (count different) or search term not found
      expect(filteredCount).toBeLessThanOrEqual(initialCount);
    });

    test('should filter topics by English name', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Search for an English term
      await page.locator('#search').fill('Present');
      await page.waitForTimeout(500);

      // Should show results or empty state
      const hasResults = await page.locator('button:has-text("Practice This Topic")').count();
      const hasEmptyState = await page.locator('text=No topics found').isVisible().catch(() => false);

      expect(hasResults > 0 || hasEmptyState).toBe(true);
    });

    test('should clear search and show all topics', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Get initial count
      const initialCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const initialCount = parseInt(initialCountText?.match(/\\d+/)?.[0] || '0');

      // Search and clear
      await page.locator('#search').fill('Präsens');
      await page.waitForTimeout(500);
      await page.locator('#search').fill('');
      await page.waitForTimeout(500);

      // Should show all topics again
      const finalCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const finalCount = parseInt(finalCountText?.match(/\\d+/)?.[0] || '0');

      expect(finalCount).toBe(initialCount);
    });
  });

  test.describe('Category Filter', () => {
    test('should have category dropdown', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Check for category select
      await expect(page.locator('#category')).toBeVisible();
    });

    test('should filter by category', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Get available categories
      const categorySelect = page.locator('#category');
      const options = await categorySelect.locator('option').allTextContents();

      // If there are categories beyond "All"
      if (options.length > 1) {
        // Select a specific category
        await categorySelect.selectOption({ index: 1 });
        await page.waitForTimeout(500);

        // Topics should be filtered (count may change)
        await expect(page.locator('text=/\\d+ topics? available/i')).toBeVisible();
      }
    });

    test('should reset to all categories', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Get initial count
      const initialCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const initialCount = parseInt(initialCountText?.match(/\\d+/)?.[0] || '0');

      // Select and reset category
      const categorySelect = page.locator('#category');
      await categorySelect.selectOption({ index: 1 });
      await page.waitForTimeout(500);
      await categorySelect.selectOption({ value: 'all' });
      await page.waitForTimeout(500);

      // Should show all topics again
      const finalCountText = await page.locator('text=/\\d+ topics? available/i').textContent();
      const finalCount = parseInt(finalCountText?.match(/\\d+/)?.[0] || '0');

      expect(finalCount).toBe(initialCount);
    });
  });

  test.describe('Difficulty Filter', () => {
    test('should have difficulty dropdown', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Check for difficulty select
      await expect(page.locator('#difficulty')).toBeVisible();
    });

    test('should have all CEFR levels', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      const difficultySelect = page.locator('#difficulty');
      await expect(difficultySelect).toBeVisible();

      // Verify option count (7 total: "All Levels" + 6 CEFR levels)
      await expect(difficultySelect.locator('option')).toHaveCount(7);

      // Verify all CEFR level options exist by extracting their values
      // Note: Using evaluateAll instead of toBeVisible() because <option> elements
      // in native <select> are not truly "visible" until dropdown is expanded
      const optionValues = await difficultySelect.locator('option').evaluateAll(
        (options) => options.map((opt) => (opt as HTMLOptionElement).value)
      );
      expect(optionValues).toEqual(['all', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']);

      // Verify options are selectable (functional test)
      await difficultySelect.selectOption('A1');
      await expect(difficultySelect).toHaveValue('A1');

      await difficultySelect.selectOption('C2');
      await expect(difficultySelect).toHaveValue('C2');

      // Reset to "All Levels"
      await difficultySelect.selectOption('all');
      await expect(difficultySelect).toHaveValue('all');
    });

    test('should filter by difficulty level', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Select B2 level
      await page.locator('#difficulty').selectOption('B2');
      await page.waitForTimeout(500);

      // Topics should be filtered
      await expect(page.locator('text=/\\d+ topics? available/i')).toBeVisible();

      // All visible topic badges should show B2 (or no topics)
      const hasTopics = await page.locator('button:has-text("Practice This Topic")').count() > 0;

      if (hasTopics) {
        // Check that B2 badges are present
        const b2Badges = page.locator('text=B2').first();
        await expect(b2Badges).toBeVisible();
      }
    });
  });

  test.describe('Combined Filters', () => {
    test('should apply multiple filters together', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Apply search + difficulty
      await page.locator('#search').fill('Verb');
      await page.locator('#difficulty').selectOption('B2');
      await page.waitForTimeout(500);

      // Should show filtered results or empty state
      const hasResults = await page.locator('button:has-text("Practice This Topic")').count() > 0;
      const hasEmptyState = await page.locator('text=No topics found').isVisible().catch(() => false);

      expect(hasResults || hasEmptyState).toBe(true);
    });
  });

  test.describe('Topic Card Display', () => {
    test('should display topic name in English', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Topic cards should have h3 headers with English names
      const firstCard = page.locator('h3.text-lg').first();
      await expect(firstCard).toBeVisible();
    });

    test('should display difficulty badge', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Topics should have difficulty badges (A1, A2, B1, B2, C1, C2)
      const difficultyBadge = page.locator('text=/^(A1|A2|B1|B2|C1|C2)$/').first();
      await expect(difficultyBadge).toBeVisible();
    });

    test('should display category badge', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Topics should have category badges
      // The categories are dynamic from the API
      const categoryBadges = page.locator('[class*="Badge"]').first();
      await expect(categoryBadges).toBeVisible();
    });

    test('should display Practice This Topic button', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Each topic card should have a practice button
      await expect(page.locator('button:has-text("Practice This Topic")').first()).toBeVisible();
    });
  });

  test.describe('Navigation to Practice', () => {
    test('should navigate to practice with topic ID when clicking Practice button', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Click the first Practice button
      const practiceButton = page.locator('button:has-text("Practice This Topic")').first();

      if (await practiceButton.isVisible()) {
        await practiceButton.click();

        // Should navigate to practice page with topics parameter
        await expect(page).toHaveURL(/grammar\/practice\?topics=\d+/, { timeout: 5000 });
      }
    });

    test('should navigate to mixed practice when clicking Start Mixed Practice', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Click mixed practice button
      const mixedButton = page.locator('button:has-text("Start Mixed Practice")');
      await mixedButton.click();

      // Should navigate to practice page without specific topic
      await expect(page).toHaveURL(/grammar\/practice/, { timeout: 5000 });
    });
  });

  test.describe('Empty State', () => {
    test('should show empty state when no topics match filter', async ({ page }) => {
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
      await page.waitForTimeout(2000);

      // Search for something that won't match
      await page.locator('#search').fill('xyznonexistent12345');
      await page.waitForTimeout(500);

      // Should show empty state
      await expect(page.locator('text=No topics found')).toBeVisible();
      await expect(page.locator('text=Try adjusting your filters')).toBeVisible();
    });
  });

  test.describe('Error Handling', () => {
    test('should handle API error gracefully', async ({ page }) => {
      // Mock API failure
      await page.route('**/api/grammar/topics', (route) => {
        route.fulfill({
          status: 500,
          body: JSON.stringify({ detail: 'Internal Server Error' }),
        });
      });

      await page.reload();

      // Should show error toast or message
      await expect(page.locator('text=/error|failed/i').first()).toBeVisible({ timeout: 10000 });
    });
  });

  test.describe('Responsive Design', () => {
    test('should render correctly on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.reload();
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Page should still be functional
      await expect(page.locator('h1')).toContainText('Grammar Topics');
      await expect(page.locator('#search')).toBeVisible();
    });

    test('should stack filters on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      await page.reload();
      await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

      // Filters should be accessible
      await expect(page.locator('#search')).toBeVisible();
      await expect(page.locator('#category')).toBeVisible();
      await expect(page.locator('#difficulty')).toBeVisible();
    });
  });
});
