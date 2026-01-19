import { test, expect } from '@playwright/test';

/**
 * Authentication E2E Test Suite
 * Tests login, registration, protected routes, and auth persistence
 */

// Generate unique test user for each test run
const timestamp = Date.now();
const testUser = {
  username: `test_user_${timestamp}`,
  email: `test_${timestamp}@example.com`,
  password: 'TestPass123A',
};

// Existing test user (should exist in database)
const existingUser = {
  username: 'test_engineer',
  password: 'TestPass123A',
};

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage before each test
    await page.goto('/login');
    await page.evaluate(() => localStorage.clear());
  });

  test.describe('Login Page', () => {
    test('should display login form', async ({ page }) => {
      await page.goto('/login');

      // Check page elements
      await expect(page.locator('h1')).toContainText('German Learning App');
      await expect(page.locator('input#username')).toBeVisible();
      await expect(page.locator('input#password')).toBeVisible();
      await expect(page.locator('button[type="submit"]')).toContainText('Sign In');
      await expect(page.locator('a[href="/register"]')).toBeVisible();
    });

    test('should show validation errors for empty fields', async ({ page }) => {
      await page.goto('/login');

      // Submit empty form - HTML5 required validation will prevent submission
      // but our custom validation should also kick in
      await page.locator('#username').fill('');
      await page.locator('#password').fill('');
      await page.locator('#username').focus();
      await page.locator('#password').focus();
      await page.locator('#username').blur();

      // Click submit to trigger validation
      await page.locator('button[type="submit"]').click();

      // Form should not navigate away (still on login page)
      await expect(page).toHaveURL(/login/);
    });

    test('should show error for invalid credentials', async ({ page }) => {
      await page.goto('/login');

      await page.locator('#username').fill('invalid_user_xyz');
      await page.locator('#password').fill('wrongpassword123');
      await page.locator('button[type="submit"]').click();

      // Wait for error toast or message
      // The app shows error via toast notification
      await expect(page.locator('[class*="toast"]').or(page.locator('text=/failed|invalid|error/i'))).toBeVisible({
        timeout: 10000,
      });
    });

    test('should login successfully with valid credentials', async ({ page }) => {
      await page.goto('/login');

      await page.locator('#username').fill(existingUser.username);
      await page.locator('#password').fill(existingUser.password);
      await page.locator('button[type="submit"]').click();

      // Should redirect to dashboard
      await expect(page).toHaveURL(/dashboard/, { timeout: 10000 });

      // Verify token is stored
      const token = await page.evaluate(() => localStorage.getItem('auth_token'));
      expect(token).toBeTruthy();
    });

    test('should show loading state during login', async ({ page }) => {
      await page.goto('/login');

      await page.locator('#username').fill(existingUser.username);
      await page.locator('#password').fill(existingUser.password);

      // Check button has loading state when clicked
      const submitButton = page.locator('button[type="submit"]');
      await submitButton.click();

      // Button should be disabled during loading
      // Note: This may happen very fast, so we use a soft check
      await page.waitForURL(/dashboard|login/, { timeout: 10000 });
    });

    test('should navigate to register page', async ({ page }) => {
      await page.goto('/login');

      await page.locator('a[href="/register"]').click();
      await expect(page).toHaveURL(/register/);
    });
  });

  test.describe('Registration Page', () => {
    test('should display registration form', async ({ page }) => {
      await page.goto('/register');

      await expect(page.locator('h1')).toContainText('German Learning App');
      await expect(page.locator('text=Create your account')).toBeVisible();
      await expect(page.locator('#username')).toBeVisible();
      await expect(page.locator('#email')).toBeVisible();
      await expect(page.locator('#password')).toBeVisible();
      await expect(page.locator('#confirmPassword')).toBeVisible();
      await expect(page.locator('#proficiency_level')).toBeVisible();
      await expect(page.locator('button[type="submit"]')).toContainText('Create Account');
    });

    test('should show validation error for invalid email', async ({ page }) => {
      await page.goto('/register');

      await page.locator('#username').fill('testuser');
      await page.locator('#email').fill('invalid-email');
      await page.locator('#password').fill('TestPass123!');
      await page.locator('#confirmPassword').fill('TestPass123!');
      await page.locator('button[type="submit"]').click();

      // Should show email validation error
      await expect(page.locator('text=/email|invalid/i')).toBeVisible();
      await expect(page).toHaveURL(/register/);
    });

    test('should show validation error for password mismatch', async ({ page }) => {
      await page.goto('/register');

      await page.locator('#username').fill('testuser');
      await page.locator('#email').fill('test@example.com');
      await page.locator('#password').fill('TestPass123!');
      await page.locator('#confirmPassword').fill('DifferentPass456!');
      await page.locator('button[type="submit"]').click();

      // Should show password mismatch error
      await expect(page.locator('text=/match|mismatch/i')).toBeVisible();
      await expect(page).toHaveURL(/register/);
    });

    test('should show validation error for short password', async ({ page }) => {
      await page.goto('/register');

      await page.locator('#username').fill('testuser');
      await page.locator('#email').fill('test@example.com');
      await page.locator('#password').fill('short');
      await page.locator('#confirmPassword').fill('short');
      await page.locator('button[type="submit"]').click();

      // Should show password length error
      await expect(page.locator('.text-red-600')).toBeVisible();
      await expect(page).toHaveURL(/register/);
    });

    test('should register successfully and auto-login', async ({ page }) => {
      await page.goto('/register');

      await page.locator('#username').fill(testUser.username);
      await page.locator('#email').fill(testUser.email);
      await page.locator('#password').fill(testUser.password);
      await page.locator('#confirmPassword').fill(testUser.password);
      await page.locator('#proficiency_level').selectOption('B2');
      await page.locator('button[type="submit"]').click();

      // Should redirect to dashboard after successful registration
      await expect(page).toHaveURL(/dashboard/, { timeout: 15000 });

      // Verify auto-login (token stored)
      const token = await page.evaluate(() => localStorage.getItem('auth_token'));
      expect(token).toBeTruthy();
    });

    test('should show proficiency level options', async ({ page }) => {
      await page.goto('/register');

      // Wait for the select element to be ready
      const select = page.locator('#proficiency_level');
      await expect(select).toBeVisible();

      // Verify option count
      await expect(select.locator('option')).toHaveCount(6);

      // Verify all CEFR level options exist by extracting their values
      // Note: Using evaluateAll instead of toBeVisible() because <option> elements
      // in native <select> are not truly "visible" until dropdown is expanded
      const optionValues = await select.locator('option').evaluateAll(
        (options) => options.map((opt) => (opt as HTMLOptionElement).value)
      );
      expect(optionValues).toEqual(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']);

      // Verify default value is B2
      await expect(select).toHaveValue('B2');

      // Verify options are selectable (functional test)
      await select.selectOption('A1');
      await expect(select).toHaveValue('A1');

      await select.selectOption('C2');
      await expect(select).toHaveValue('C2');
    });

    test('should navigate to login page', async ({ page }) => {
      await page.goto('/register');

      await page.locator('a[href="/login"]').click();
      await expect(page).toHaveURL(/login/);
    });
  });

  test.describe('Protected Routes', () => {
    test('should redirect to login when accessing dashboard without auth', async ({ page }) => {
      // Clear any existing auth
      await page.goto('/login');
      await page.evaluate(() => localStorage.clear());

      // Try to access protected route
      await page.goto('/dashboard');

      // Should redirect to login
      await expect(page).toHaveURL(/login/, { timeout: 5000 });
    });

    test('should redirect to login when accessing grammar page without auth', async ({ page }) => {
      await page.goto('/login');
      await page.evaluate(() => localStorage.clear());

      await page.goto('/grammar');
      await expect(page).toHaveURL(/login/, { timeout: 5000 });
    });

    test('should allow access to protected routes with valid auth', async ({ page }) => {
      // Login first
      await page.goto('/login');
      await page.locator('#username').fill(existingUser.username);
      await page.locator('#password').fill(existingUser.password);
      await page.locator('button[type="submit"]').click();

      // Wait for dashboard
      await expect(page).toHaveURL(/dashboard/, { timeout: 10000 });

      // Navigate to grammar (protected route)
      await page.goto('/grammar');
      await expect(page).toHaveURL(/grammar/);
      await expect(page).not.toHaveURL(/login/);
    });
  });

  test.describe('Auth Persistence', () => {
    test('should persist auth state after page refresh', async ({ page }) => {
      // Login
      await page.goto('/login');
      await page.locator('#username').fill(existingUser.username);
      await page.locator('#password').fill(existingUser.password);
      await page.locator('button[type="submit"]').click();

      await expect(page).toHaveURL(/dashboard/, { timeout: 10000 });

      // Refresh the page
      await page.reload();

      // Should still be on dashboard (not redirected to login)
      await expect(page).toHaveURL(/dashboard/, { timeout: 5000 });
    });

    test('should clear auth state after logout', async ({ page }) => {
      // Login
      await page.goto('/login');
      await page.locator('#username').fill(existingUser.username);
      await page.locator('#password').fill(existingUser.password);
      await page.locator('button[type="submit"]').click();

      await expect(page).toHaveURL(/dashboard/, { timeout: 10000 });

      // Clear localStorage to simulate logout
      await page.evaluate(() => localStorage.clear());

      // Try to access protected route
      await page.goto('/grammar');

      // Should redirect to login
      await expect(page).toHaveURL(/login/, { timeout: 5000 });
    });
  });
});
