# BUG-011: Word Detail Modal - accuracy_rate undefined error

**Status:** FIXED
**Severity:** High
**Type:** Backend/Frontend Schema Mismatch
**Reported:** 2026-01-19
**Fixed:** 2026-01-19
**Reporter:** Test Engineer
**Fixed By:** Claude Code (Frontend Fix)

---

## Summary

Clicking on a word in the Vocabulary Browser causes a TypeError crash because `accuracy_rate` is undefined when the `WordDetailModal` tries to call `.toFixed()` on it.

---

## Error Message

```
TypeError: undefined is not an object (evaluating 'word.accuracy_rate.toFixed')
    reportError (WordDetailModal.tsx:195)
```

---

## Steps to Reproduce

1. Login to the application
2. Navigate to **Vocabulary** -> **Browse Words**
3. Click on any word card
4. **Result:** Modal fails to render, TypeError in console

---

## Expected Behavior

Word detail modal should open and display word information, showing "N/A" or hiding the accuracy field if no reviews exist.

---

## Actual Behavior

Modal crashes with TypeError because `accuracy_rate` is `undefined` (not `null`).

---

## Root Cause Analysis

### Backend API Schema Mismatch

Two different endpoints return different response schemas:

| Endpoint | Response Model | Has Progress Fields |
|----------|---------------|---------------------|
| `GET /api/v1/vocabulary/words` | `VocabularyResponse` | NO |
| `GET /api/v1/vocabulary/words/{id}` | `VocabularyWithProgress` | YES |

### Code Evidence

**Backend (`backend/app/api/v1/vocabulary.py`):**

```python
# Line 40 - List endpoint returns VocabularyResponse (NO progress)
@router.get("/v1/vocabulary/words", response_model=List[VocabularyResponse])

# Line 99 - Single word endpoint returns VocabularyWithProgress (HAS progress)
@router.get("/v1/vocabulary/words/{word_id}", response_model=VocabularyWithProgress)
```

**Frontend (`VocabularyBrowserPage.tsx`):**
- Calls `vocabularyService.getWords()` which hits the list endpoint
- Passes word data to `WordDetailModal`
- Modal expects `VocabularyWithProgress` type with `accuracy_rate` field

**Frontend (`WordDetailModal.tsx:125-127`):**
```tsx
{word.accuracy_rate !== null && (
  <span className="font-medium">{word.accuracy_rate.toFixed(0)}%</span>
)}
```

**Frontend (`WordCard.tsx:129`):**
```tsx
{word.accuracy_rate !== null && <span>{word.accuracy_rate.toFixed(0)}% accuracy</span>}
```

The check `!== null` only handles `null`, but the field is completely **missing** from the API response (making it `undefined`), so the condition evaluates to `true` and `.toFixed()` is called on `undefined`.

---

## Affected Files

| File | Line(s) | Issue |
|------|---------|-------|
| `backend/app/api/v1/vocabulary.py` | 40-96 | Returns `VocabularyResponse` without progress fields |
| `frontend/src/components/vocabulary/WordDetailModal.tsx` | 125-127 | Assumes `accuracy_rate` exists |
| `frontend/src/components/vocabulary/WordCard.tsx` | 129 | Same issue (may crash in list view) |

---

## Suggested Fixes

### Option A - Backend Fix (Recommended)

Modify `GET /api/v1/vocabulary/words` to return `VocabularyWithProgress` with user's progress data:

```python
@router.get("/v1/vocabulary/words", response_model=List[VocabularyWithProgress])
def get_vocabulary_words(...):
    # Add progress lookup for each word
    # Include mastery_level, times_reviewed, accuracy_rate, etc.
```

### Option B - Frontend Fix (Fetch on Modal Open)

When opening modal, fetch full word data via single-word endpoint:

```tsx
// In VocabularyBrowserPage.tsx
const handleWordClick = async (word: VocabularyWord) => {
  const fullWord = await vocabularyService.getWord(word.id);
  setSelectedWord(fullWord);
};
```

### Option C - Frontend Fix (Defensive Checks)

Add defensive checks for all progress fields in `WordDetailModal.tsx`:

```tsx
{typeof word.accuracy_rate === 'number' && (
  <span className="font-medium">{word.accuracy_rate.toFixed(0)}%</span>
)}
```

And ensure default values:
```tsx
<span className="font-medium">{word.times_reviewed ?? 0}</span> reviews
```

---

## Fix Applied (2026-01-19)

**Solution:** Combined approach using **Option B** (fetch on modal open) + **Option C** (defensive checks)

### Changes Made

#### 1. VocabularyBrowserPage.tsx (Line 107)
**Modified:** `handleWordClick()` function to fetch full word data

```tsx
const handleWordClick = async (word: VocabularyWithProgress) => {
  // Fetch full word data with progress fields from single-word endpoint
  try {
    setLoadingWords(true);
    const fullWord = await vocabularyService.getWord(word.id);
    setSelectedWord(fullWord);
    setIsDetailModalOpen(true);
  } catch (error) {
    const apiError = error as ApiError;
    addToast('error', 'Failed to load word details', apiError.detail || 'An error occurred');
    // Fallback: use the word data from the list (may have missing progress fields)
    setSelectedWord(word);
    setIsDetailModalOpen(true);
  } finally {
    setLoadingWords(false);
  }
};
```

**Benefit:** Modal now receives `VocabularyWithProgress` with all progress fields populated from the backend's single-word endpoint.

#### 2. WordDetailModal.tsx (Lines 123, 125)
**Modified:** Added defensive checks for progress fields

```tsx
// Before:
<span className="font-medium">{word.times_reviewed}</span> reviews
{word.accuracy_rate !== null && (

// After:
<span className="font-medium">{word.times_reviewed ?? 0}</span> reviews
{typeof word.accuracy_rate === 'number' && (
```

**Benefit:** Handles `undefined` values gracefully. If API call fails and fallback data is used, modal displays "0 reviews" instead of crashing.

#### 3. WordCard.tsx (Lines 128-129)
**Modified:** Same defensive checks for expanded card variant

```tsx
// Before:
<span>{word.times_reviewed} reviews</span>
{word.accuracy_rate !== null && <span>{word.accuracy_rate.toFixed(0)}% accuracy</span>}

// After:
<span>{word.times_reviewed ?? 0} reviews</span>
{typeof word.accuracy_rate === 'number' && <span>{word.accuracy_rate.toFixed(0)}% accuracy</span>}
```

**Benefit:** Prevents crashes in list view with expanded cards.

### Why This Approach?

1. **Option A (Backend Fix) Not Possible:** Cannot modify backend (production-ready, no changes allowed)
2. **Option B (Fetch on Open):** Best solution - ensures modal always has complete data
3. **Option C (Defensive Checks):** Safety net for edge cases (API failures, network issues)

### Testing Verification

**Manual Test Steps:**
1. ✅ Login to application
2. ✅ Navigate to Vocabulary → Browse Words
3. ✅ Click on any word card
4. ✅ **Expected:** Modal opens without errors, showing word details and progress
5. ✅ **Expected:** If progress data missing, display "0 reviews" and hide accuracy (no crash)

**Network Error Test:**
1. ✅ Disconnect network
2. ✅ Click word card (fetch will fail)
3. ✅ **Expected:** Toast error shown, modal still opens with list data, displays "0 reviews"

---

## Impact

- **User Impact (Before Fix):** Cannot view word details from vocabulary browser
- **Functionality Blocked (Before Fix):** Word detail modal completely broken
- **Workaround (Before Fix):** None available
- **Status After Fix:** ✅ RESOLVED - Modal now works correctly with all progress fields

---

## Related Issues

- Similar to BUG-010 (Session Progress Schema Mismatch)
- Pattern: Backend/Frontend schema alignment issues

---

## Test Coverage

Add E2E test to `vocabulary.spec.ts`:

```typescript
test('should open word detail modal without errors', async ({ page }) => {
  await page.goto('/vocabulary');
  await page.waitForSelector('[data-testid^="word-card-"]');

  // Click first word card
  await page.locator('[data-testid^="word-card-"]').first().click();

  // Modal should open without errors
  await expect(page.locator('text=Word Details')).toBeVisible();
  await expect(page.locator('text=Learning Progress')).toBeVisible();
});
```
