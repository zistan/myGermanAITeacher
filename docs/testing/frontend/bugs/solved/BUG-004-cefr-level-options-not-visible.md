# BUG-004: CEFR Level Options Not Visible in Time

**Severity:** Low
**Category:** Grammar Topics / Test Reliability
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Fixed
**Fixed:** 2026-01-19
**Fix:** Replaced `.toBeVisible()` assertions with `evaluateAll` + functional `selectOption` tests

---

## Description

The E2E test for CEFR level difficulty filter options in the Grammar Topics page fails due to timing issues. The test expects to verify that all 6 CEFR levels (A1-C2) are available as filter options, but the assertion times out.

---

## Steps to Reproduce

1. Navigate to `/grammar` page while authenticated
2. Run Playwright test: `npx playwright test grammar-topics.spec.ts -g "should have all CEFR levels"`
3. Observe test failure due to timeout on option visibility check

---

## Test Code

**File:** `/frontend/tests/e2e/grammar-topics.spec.ts`, lines 201-212

```typescript
test('should have all CEFR levels', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

  const difficultySelect = page.locator('#difficulty');

  // Check for all CEFR levels
  await expect(difficultySelect.locator('option[value="A1"]')).toBeVisible();
  await expect(difficultySelect.locator('option[value="A2"]')).toBeVisible();
  await expect(difficultySelect.locator('option[value="B1"]')).toBeVisible();
  await expect(difficultySelect.locator('option[value="B2"]')).toBeVisible();
  await expect(difficultySelect.locator('option[value="C1"]')).toBeVisible();
  await expect(difficultySelect.locator('option[value="C2"]')).toBeVisible();
});
```

---

## Frontend Implementation

**File:** `/frontend/src/pages/grammar/GrammarTopicsPage.tsx`

The difficulty filter select element:

```tsx
<select
  id="difficulty"
  value={filters.difficulty}
  onChange={(e) => setFilters({ ...filters, difficulty: e.target.value as DifficultyLevel | '' })}
  className="..."
>
  <option value="">All Levels</option>
  <option value="A1">A1</option>
  <option value="A2">A2</option>
  <option value="B1">B1</option>
  <option value="B2">B2</option>
  <option value="C1">C1</option>
  <option value="C2">C2</option>
</select>
```

---

## Root Cause Analysis

### Same Issue as BUG-003

This is the same root cause as BUG-003:
1. **Native `<option>` visibility**: Options inside a native `<select>` element are not "visible" in the DOM until the dropdown is expanded
2. **Playwright limitation**: `.toBeVisible()` doesn't work reliably for unexpanded select options

### Additional Factor: Page Load Time

The Grammar Topics page makes an API call to load topics before rendering:
```
GET /api/grammar/topics
```
The test waits for "Grammar Topics" text but the select element may not be fully rendered yet.

---

## Recommended Fixes

### Option A: Check Option Existence, Not Visibility (Recommended)

```typescript
test('should have all CEFR levels', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

  const difficultySelect = page.locator('#difficulty');
  await expect(difficultySelect).toBeVisible();

  // Verify option count (7 total: "All Levels" + 6 CEFR levels)
  await expect(difficultySelect.locator('option')).toHaveCount(7);

  // Verify options by value using evaluate
  const optionValues = await difficultySelect.locator('option').evaluateAll(
    options => options.map(opt => (opt as HTMLOptionElement).value)
  );
  expect(optionValues).toContain('A1');
  expect(optionValues).toContain('A2');
  expect(optionValues).toContain('B1');
  expect(optionValues).toContain('B2');
  expect(optionValues).toContain('C1');
  expect(optionValues).toContain('C2');
});
```

### Option B: Test by Selecting Each Option

```typescript
test('should have all CEFR levels', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

  const difficultySelect = page.locator('#difficulty');

  // Test each CEFR level can be selected
  const cefrLevels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2'];
  for (const level of cefrLevels) {
    await difficultySelect.selectOption(level);
    await expect(difficultySelect).toHaveValue(level);
  }

  // Reset to "All Levels"
  await difficultySelect.selectOption('');
  await expect(difficultySelect).toHaveValue('');
});
```

### Option C: Add `data-testid` Attributes

**Frontend Change:**

```tsx
<select
  id="difficulty"
  data-testid="difficulty-filter"
  ...
>
  <option value="" data-testid="difficulty-all">All Levels</option>
  <option value="A1" data-testid="difficulty-a1">A1</option>
  <option value="A2" data-testid="difficulty-a2">A2</option>
  <option value="B1" data-testid="difficulty-b1">B1</option>
  <option value="B2" data-testid="difficulty-b2">B2</option>
  <option value="C1" data-testid="difficulty-c1">C1</option>
  <option value="C2" data-testid="difficulty-c2">C2</option>
</select>
```

**Test Change:**

```typescript
const difficultySelect = page.getByTestId('difficulty-filter');
await expect(difficultySelect.locator('[data-testid^="difficulty-"]')).toHaveCount(7);
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
| `/frontend/tests/e2e/grammar-topics.spec.ts` | Update test assertions |
| `/frontend/src/pages/grammar/GrammarTopicsPage.tsx` | (Optional) Add `data-testid` attributes |

---

## Related Bugs

- BUG-003: Same issue with proficiency level options in Registration (Fixed)

---

## Fix Applied

**Files Modified:**
- `/frontend/tests/e2e/grammar-topics.spec.ts` - Updated test assertions
- `/frontend/src/pages/grammar/GrammarTopicsPage.tsx` - Added `data-testid` attributes

**Solution:**
Same approach as BUG-003 - replaced unreliable `.toBeVisible()` assertions on `<option>` elements with:

1. **`evaluateAll`** to extract option values directly from the DOM
2. **`toHaveCount`** to verify 7 options ("All Levels" + 6 CEFR levels)
3. **`selectOption`** to functionally verify options are selectable

**Updated Test:**
```typescript
test('should have all CEFR levels', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });

  const difficultySelect = page.locator('#difficulty');
  await expect(difficultySelect).toBeVisible();
  await expect(difficultySelect.locator('option')).toHaveCount(7);

  // Extract values instead of checking visibility
  const optionValues = await difficultySelect.locator('option').evaluateAll(
    (options) => options.map((opt) => (opt as HTMLOptionElement).value)
  );
  expect(optionValues).toEqual(['all', 'A1', 'A2', 'B1', 'B2', 'C1', 'C2']);

  // Verify options are selectable
  await difficultySelect.selectOption('A1');
  await expect(difficultySelect).toHaveValue('A1');
});
```
