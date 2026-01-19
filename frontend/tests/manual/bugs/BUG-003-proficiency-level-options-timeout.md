# BUG-003: Proficiency Level Options Timeout

**Severity:** Low
**Category:** Authentication / Test Reliability
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Fixed
**Fixed:** 2026-01-19
**Fix:** Replaced `.toBeVisible()` assertions with `evaluateAll` + functional `selectOption` tests

---

## Description

The E2E test for proficiency level options in the registration form fails intermittently due to timing issues. The test expects to verify that all 6 CEFR level options (A1-C2) are visible in the dropdown, but the assertion times out before options can be verified.

---

## Steps to Reproduce

1. Run Playwright test: `npx playwright test auth.spec.ts -g "should show proficiency level options"`
2. Observe test failure due to timeout

---

## Test Code

**File:** `/frontend/tests/e2e/auth.spec.ts`, lines 185-198

```typescript
test('should show proficiency level options', async ({ page }) => {
  await page.goto('/register');

  const select = page.locator('#proficiency_level');
  await expect(select.locator('option')).toHaveCount(6);

  // Check all CEFR levels are present
  await expect(select.locator('option[value="A1"]')).toBeVisible();
  await expect(select.locator('option[value="A2"]')).toBeVisible();
  await expect(select.locator('option[value="B1"]')).toBeVisible();
  await expect(select.locator('option[value="B2"]')).toBeVisible();
  await expect(select.locator('option[value="C1"]')).toBeVisible();
  await expect(select.locator('option[value="C2"]')).toBeVisible();
});
```

---

## Frontend Implementation

**File:** `/frontend/src/pages/auth/RegisterPage.tsx`, lines 187-200

```tsx
<select
  id="proficiency_level"
  value={formData.proficiency_level}
  onChange={(e) => handleChange('proficiency_level', e.target.value)}
  className="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
>
  <option value="A1">A1 - Beginner</option>
  <option value="A2">A2 - Elementary</option>
  <option value="B1">B1 - Intermediate</option>
  <option value="B2">B2 - Upper Intermediate</option>
  <option value="C1">C1 - Advanced</option>
  <option value="C2">C2 - Proficient</option>
</select>
```

---

## Root Cause Analysis

### Issue 1: Option Visibility in Native Select Elements

In Playwright, checking `.toBeVisible()` on `<option>` elements inside a native `<select>` can be problematic because:
- Options are only truly "visible" when the dropdown is expanded
- Native select elements render options in a system-level overlay, not in the DOM hierarchy
- The visibility check may not work as expected for unexpanded dropdowns

### Issue 2: Default Timeout May Be Insufficient

The default Playwright expect timeout (5000ms) may not be enough if:
- The page takes longer to render
- Network latency delays the page load
- The test runs on a slower CI environment

---

## Recommended Fixes

### Option A: Check Option Count Only (Recommended)

The most reliable approach is to verify option count, not visibility:

```typescript
test('should show proficiency level options', async ({ page }) => {
  await page.goto('/register');

  // Wait for page to fully load
  await page.waitForSelector('#proficiency_level');

  const select = page.locator('#proficiency_level');

  // Verify option count
  await expect(select.locator('option')).toHaveCount(6);

  // Verify options exist by their values (not visibility)
  const optionValues = await select.locator('option').evaluateAll(
    options => options.map(opt => (opt as HTMLOptionElement).value)
  );
  expect(optionValues).toEqual(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']);
});
```

### Option B: Use `toHaveValue` for Select Verification

```typescript
test('should show proficiency level options', async ({ page }) => {
  await page.goto('/register');

  const select = page.locator('#proficiency_level');

  // Verify default value
  await expect(select).toHaveValue('B2'); // Default in component

  // Select each option to verify they work
  await select.selectOption('A1');
  await expect(select).toHaveValue('A1');

  await select.selectOption('C2');
  await expect(select).toHaveValue('C2');
});
```

### Option C: Add Explicit Wait

```typescript
test('should show proficiency level options', async ({ page }) => {
  await page.goto('/register');

  // Wait for the select element to be attached and stable
  await page.waitForSelector('#proficiency_level', { state: 'attached' });
  await page.waitForTimeout(500); // Allow render to complete

  const select = page.locator('#proficiency_level');
  await expect(select.locator('option')).toHaveCount(6, { timeout: 10000 });
});
```

### Option D: Add `data-testid` for Reliability

**Frontend Change Required:**

```tsx
<select
  id="proficiency_level"
  data-testid="proficiency-level-select"
  ...
>
  <option value="A1" data-testid="option-a1">A1 - Beginner</option>
  <option value="A2" data-testid="option-a2">A2 - Elementary</option>
  ...
</select>
```

**Test Change:**

```typescript
const select = page.getByTestId('proficiency-level-select');
await expect(select.locator('[data-testid^="option-"]')).toHaveCount(6);
```

---

## Impact

| Aspect | Impact |
|--------|--------|
| **User Impact** | None - the functionality works correctly |
| **Test Impact** | Causes flaky tests, reduces CI reliability |
| **Fix Priority** | Low - test reliability improvement only |

---

## Files to Modify

| File | Change |
|------|--------|
| `/frontend/tests/e2e/auth.spec.ts` | Update test to use more reliable assertions |
| `/frontend/src/pages/auth/RegisterPage.tsx` | (Optional) Add `data-testid` attributes |

---

## Related Bugs

- BUG-004: Similar issue with CEFR level options in Grammar Topics

---

## Test Results Context

From error log `error-context.md`:
```
- combobox "Proficiency Level" [ref=e27]:
  - option "A1 - Beginner"
  - option "A2 - Elementary"
  - option "B1 - Intermediate"
  - option "B2 - Upper Intermediate" [selected]
  - option "C1 - Advanced"
```

This confirms the options exist and are correctly configured - the issue is purely with test assertion approach.

---

## Fix Applied

**Files Modified:**
- `/frontend/tests/e2e/auth.spec.ts` - Updated test assertions
- `/frontend/src/pages/auth/RegisterPage.tsx` - Added `data-testid` attributes

**Solution:**
Replaced unreliable `.toBeVisible()` assertions on `<option>` elements with:

1. **`evaluateAll`** to extract option values from the DOM directly
2. **`toHaveValue`** to verify default selection (B2)
3. **`selectOption`** to functionally verify options are selectable

**Updated Test:**
```typescript
test('should show proficiency level options', async ({ page }) => {
  await page.goto('/register');

  const select = page.locator('#proficiency_level');
  await expect(select).toBeVisible();
  await expect(select.locator('option')).toHaveCount(6);

  // Extract values instead of checking visibility
  const optionValues = await select.locator('option').evaluateAll(
    (options) => options.map((opt) => (opt as HTMLOptionElement).value)
  );
  expect(optionValues).toEqual(['A1', 'A2', 'B1', 'B2', 'C1', 'C2']);

  // Verify default and selectability
  await expect(select).toHaveValue('B2');
  await select.selectOption('A1');
  await expect(select).toHaveValue('A1');
});
```

**Why this works:**
- `evaluateAll` runs JavaScript in the browser context, bypassing Playwright's visibility checks
- Native `<option>` elements are not truly "visible" until the dropdown is expanded
- Functional `selectOption` tests prove the options work, not just exist
