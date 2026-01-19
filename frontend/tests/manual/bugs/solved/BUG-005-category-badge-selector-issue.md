# BUG-005: Category Badge Selector Issue

**Severity:** Low
**Category:** Grammar Topics / Test Reliability
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Fixed
**Fixed:** 2026-01-19
**Fix:** Added `testId` prop to Badge component + updated tests to use `data-testid`

---

## Description

The E2E test for category badge display on Grammar Topics page fails because the CSS selector `[class*="Badge"]` does not match the actual Badge component implementation. The Badge component uses Tailwind CSS utility classes, not a class containing "Badge".

---

## Steps to Reproduce

1. Navigate to `/grammar` page while authenticated
2. Run Playwright test: `npx playwright test grammar-topics.spec.ts -g "should display category badge"`
3. Observe test failure - no element matches `[class*="Badge"]`

---

## Test Code (Current - Failing)

**File:** `/frontend/tests/e2e/grammar-topics.spec.ts`, lines 274-282

```typescript
test('should display category badge', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Topics should have category badges
  // The categories are dynamic from the API
  const categoryBadges = page.locator('[class*="Badge"]').first();
  await expect(categoryBadges).toBeVisible();
});
```

---

## Frontend Implementation

### Badge Component

**File:** `/frontend/src/components/common/Badge.tsx`

```tsx
export function Badge({
  children,
  variant = 'gray',
  size = 'md',
  className,
  ...props
}: BadgeProps) {
  const baseStyles = 'inline-flex items-center justify-center font-medium rounded-full';

  const variantStyles = {
    primary: 'bg-primary-100 text-primary-800',
    success: 'bg-green-100 text-green-800',
    danger: 'bg-red-100 text-red-800',
    warning: 'bg-yellow-100 text-yellow-800',
    info: 'bg-blue-100 text-blue-800',
    gray: 'bg-gray-100 text-gray-800',
  };

  // ... renders <span> with these classes
  return (
    <span className={clsx(baseStyles, variantStyles[variant], sizeStyles[size], className)} {...props}>
      {children}
    </span>
  );
}
```

### Usage in GrammarTopicsPage

**File:** `/frontend/src/pages/grammar/GrammarTopicsPage.tsx`, lines 193-195

```tsx
{/* Category */}
<div className="mb-4">
  <Badge variant="gray" size="sm">
    {topic.category}
  </Badge>
</div>
```

---

## Root Cause Analysis

### The Problem

The selector `[class*="Badge"]` looks for elements with a CSS class containing the string "Badge". However:

1. The `Badge` component is a **React component**, not a CSS class
2. The actual rendered HTML has classes like:
   ```html
   <span class="inline-flex items-center justify-center font-medium rounded-full bg-gray-100 text-gray-800 px-2.5 py-0.5 text-xs">
     cases
   </span>
   ```
3. None of these Tailwind CSS classes contain "Badge"

### Why the Selector Fails

| What Test Expects | What Actually Renders |
|-------------------|----------------------|
| `<span class="...Badge...">` | `<span class="inline-flex items-center... bg-gray-100...">` |

---

## Recommended Fixes

### Option A: Add `data-testid` to Badge Component (Recommended)

**Frontend Change:**

**File:** `/frontend/src/components/common/Badge.tsx`

```tsx
export function Badge({
  children,
  variant = 'gray',
  size = 'md',
  className,
  testId,  // Add this prop
  ...props
}: BadgeProps) {
  return (
    <span
      className={clsx(...)}
      data-testid={testId}  // Add this
      {...props}
    >
      {children}
    </span>
  );
}
```

**Usage:**

```tsx
<Badge variant="gray" size="sm" testId="topic-category-badge">
  {topic.category}
</Badge>
```

**Test Change:**

```typescript
test('should display category badge', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
  await page.waitForTimeout(2000);

  const categoryBadge = page.getByTestId('topic-category-badge').first();
  await expect(categoryBadge).toBeVisible();
});
```

### Option B: Use CSS Class Pattern

Since Badge uses consistent Tailwind classes, target those:

```typescript
test('should display category badge', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Badge uses "rounded-full" and "bg-gray-100" for category
  const categoryBadge = page.locator('.rounded-full.bg-gray-100').first();
  await expect(categoryBadge).toBeVisible();
});
```

**Note:** This is fragile and will break if styling changes.

### Option C: Target by Content Pattern

Categories are specific values from the API:

```typescript
test('should display category badge', async ({ page }) => {
  await page.waitForSelector('text=Grammar Topics', { timeout: 10000 });
  await page.waitForTimeout(2000);

  // Look for known category values
  const categoryText = page.locator('text=/^(cases|verbs|sentence_structure|vocabulary|advanced)$/i').first();
  await expect(categoryText).toBeVisible();
});
```

### Option D: Add Role Attribute

**Frontend Change:**

```tsx
<Badge variant="gray" size="sm" role="status" aria-label="category">
  {topic.category}
</Badge>
```

**Test Change:**

```typescript
const categoryBadge = page.locator('[role="status"][aria-label="category"]').first();
await expect(categoryBadge).toBeVisible();
```

---

## Best Practice Recommendation

The most reliable approach is **Option A** - adding `data-testid` attributes. This is a standard E2E testing practice because:

1. **Decoupled from styling**: Tests don't break when CSS changes
2. **Explicit intent**: Makes test targets clear in code
3. **Stable**: IDs don't change with refactoring
4. **Recommended by Playwright**: Official docs recommend `data-testid` for reliable element selection

---

## Impact

| Aspect | Impact |
|--------|--------|
| **User Impact** | None - the functionality works correctly |
| **Test Impact** | Test fails, cannot verify badge rendering |
| **Fix Priority** | Low - requires small frontend change for test reliability |

---

## Files to Modify

| File | Change |
|------|--------|
| `/frontend/src/components/common/Badge.tsx` | Add `testId` prop support |
| `/frontend/src/pages/grammar/GrammarTopicsPage.tsx` | Add `testId` to Badge usage |
| `/frontend/tests/e2e/grammar-topics.spec.ts` | Update selector to use `data-testid` |

---

## Additional Context

The Badge component is used extensively throughout the application:

| Location | Usage |
|----------|-------|
| GrammarTopicsPage | Category and difficulty badges |
| PracticeSessionPage | Exercise type and difficulty badges |
| DashboardCards | Various status badges |
| Header | Proficiency level badge |

Adding `data-testid` support to Badge will improve testability across all these areas.

---

## Fix Applied

**Files Modified:**
- `/frontend/src/components/common/Badge.tsx` - Added `testId` prop that renders as `data-testid`
- `/frontend/src/pages/grammar/GrammarTopicsPage.tsx` - Added `testId` to category and difficulty badges
- `/frontend/tests/e2e/grammar-topics.spec.ts` - Updated tests to use `getByTestId()` selector

**Solution:**
Implemented Option A from recommendations - added explicit `testId` prop support to the Badge component:

**Badge Component Change:**
```tsx
export interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  variant?: 'primary' | 'success' | 'danger' | 'warning' | 'info' | 'gray';
  size?: 'sm' | 'md' | 'lg';
  /** Test ID for E2E testing - renders as data-testid attribute */
  testId?: string;
}

// In render:
<span ... data-testid={testId} ...>
```

**Usage in GrammarTopicsPage:**
```tsx
<Badge variant="info" size="sm" testId="topic-difficulty-badge">
  {topic.difficulty_level}
</Badge>

<Badge variant="gray" size="sm" testId="topic-category-badge">
  {topic.category}
</Badge>
```

**Updated Tests:**
```typescript
test('should display category badge', async ({ page }) => {
  const categoryBadge = page.getByTestId('topic-category-badge').first();
  await expect(categoryBadge).toBeVisible();
});
```

**Benefits:**
- Tests are decoupled from CSS styling
- Stable selectors that won't break with refactoring
- Follows Playwright best practices for element selection
- Reusable `testId` prop can be used across all Badge instances in the app
