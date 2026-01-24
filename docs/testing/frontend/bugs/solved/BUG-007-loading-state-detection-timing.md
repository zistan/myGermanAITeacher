# BUG-007: Loading State Detection Timing Issue

**Severity:** Low
**Category:** Grammar Practice / Test Reliability
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Open - Secondary to BUG-006

---

## Description

The E2E test for loading state detection in Grammar Practice Session fails because:
1. The loading state may be too brief to capture reliably
2. More significantly, this test is blocked by BUG-006 (missing `/next` endpoint) - the session fails before proper loading/exercise cycle can occur

---

## Steps to Reproduce

1. Navigate to `/grammar/practice` while authenticated
2. Run Playwright test: `npx playwright test grammar-practice.spec.ts -g "should show loading state"`
3. Observe test failure

---

## Test Code

**File:** `/frontend/tests/e2e/grammar-practice.spec.ts`, lines 70-79

```typescript
test('should show loading state while starting', async ({ page }) => {
  await page.goto('/grammar/practice');

  // Should show loading initially
  // The loading state may be brief
  const hasLoading = await page.locator('[class*="loading"], text=/loading/i').isVisible({ timeout: 3000 }).catch(() => false);

  // Eventually should show content
  await page.waitForSelector('text=/exercise|Check Answer|Failed to start/i', { timeout: 20000 });
});
```

---

## Root Cause Analysis

### Primary Issue: Blocked by BUG-006

The Grammar Practice Session cannot properly function because:
1. Session starts successfully via `POST /api/grammar/practice/start`
2. Frontend calls `GET /api/grammar/practice/{session_id}/next` to get exercise
3. Backend returns 404 (endpoint doesn't exist)
4. Session fails, showing error state instead of normal loading → exercise flow

**Until BUG-006 is fixed, this test cannot properly validate loading behavior.**

### Secondary Issue: Loading State Detection

Even when BUG-006 is fixed, the test has reliability issues:

1. **Brief Loading Window**: The loading state between session start and exercise display may be very short (< 100ms) on fast networks
2. **Fragile Selector**: `[class*="loading"]` depends on CSS class names which may change
3. **Race Condition**: By the time the test checks for loading, it may have already completed

---

## Frontend Loading Implementation

**File:** `/frontend/src/pages/grammar/PracticeSessionPage.tsx`

```tsx
const [isLoading, setIsLoading] = useState(true);

// ... in useEffect
try {
  setIsLoading(true);
  const session = await grammarService.startPracticeSession({...});
  setSessionInfo(session);
  await loadNextExercise(session.session_id); // This fails due to BUG-006
} catch (error) {
  setError('Failed to start practice session');
} finally {
  setIsLoading(false);
}

// Render
if (isLoading) {
  return <Loading message="Starting practice session..." />;
}
```

---

## Recommended Fixes

### Step 1: Wait for BUG-006 Fix

This test cannot be reliably fixed until the backend implements the `/next` endpoint. Once BUG-006 is resolved, the normal flow will be:

```
1. Page loads → Shows loading
2. Session starts → Loading continues
3. Exercise fetched → Loading ends, exercise displays
```

### Step 2: Update Test After BUG-006

Once BUG-006 is fixed, update the test:

```typescript
test('should show loading state while starting', async ({ page }) => {
  // Intercept API calls to slow them down for testing
  await page.route('**/api/grammar/practice/start', async route => {
    // Add small delay to make loading visible
    await new Promise(r => setTimeout(r, 500));
    await route.continue();
  });

  await page.goto('/grammar/practice');

  // Now loading should be visible
  await expect(page.getByTestId('loading-indicator')).toBeVisible({ timeout: 3000 });

  // Wait for content to load
  await expect(page.getByText(/Check Answer/i)).toBeVisible({ timeout: 20000 });
});
```

### Step 3: Add `data-testid` to Loading Component

**Frontend Change:**

**File:** `/frontend/src/components/common/Loading.tsx`

```tsx
export function Loading({ message, testId = 'loading-indicator' }: LoadingProps) {
  return (
    <div data-testid={testId} className="...">
      {/* ... spinner and message ... */}
    </div>
  );
}
```

**Usage in PracticeSessionPage:**

```tsx
if (isLoading) {
  return <Loading message="Starting practice session..." testId="practice-loading" />;
}
```

### Alternative: Remove Loading State Test

If loading state timing is consistently unreliable, consider removing this specific test and instead verifying:

```typescript
test('should eventually show exercise or error', async ({ page }) => {
  await page.goto('/grammar/practice');

  // Don't test loading specifically, just verify end state
  await page.waitForSelector(
    'text=/Check Answer|Failed to start|exercise/i',
    { timeout: 30000 }
  );
});
```

---

## Impact

| Aspect | Impact |
|--------|--------|
| **User Impact** | None - loading behavior works correctly |
| **Test Impact** | Test fails; however, this is secondary to BUG-006 |
| **Fix Priority** | Low - blocked by BUG-006; will be easier to fix after that |

---

## Dependencies

| Bug | Relationship |
|-----|-------------|
| **BUG-006** | **Blocks this bug** - must be fixed first for meaningful loading test |

---

## Files to Modify (After BUG-006 Fix)

| File | Change |
|------|--------|
| `/frontend/src/components/common/Loading.tsx` | Add `testId` prop support |
| `/frontend/src/pages/grammar/PracticeSessionPage.tsx` | Add `testId` to Loading usage |
| `/frontend/tests/e2e/grammar-practice.spec.ts` | Update test with API interception or better selectors |

---

## Test Status

| Condition | Test Result |
|-----------|-------------|
| BUG-006 unfixed | Always fails (no exercises load) |
| BUG-006 fixed, fast network | May fail (loading too brief) |
| BUG-006 fixed, with API delay | Should pass |
| BUG-006 fixed, with `data-testid` | Should pass reliably |

---

## Recommendation

1. **Wait for BUG-006 fix** before addressing this bug
2. After BUG-006 is fixed, add `data-testid` to Loading component
3. Update test to use network interception for reliable loading visibility
4. Re-run tests to verify fix
