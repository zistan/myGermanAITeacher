# BUG-020: Grammar Practice Stuck on Loading Page

**Date:** 2026-01-19
**Severity:** 🔴 CRITICAL
**Category:** Grammar Practice / Frontend Loading Issue
**Status:** Root Cause Identified
**Reported By:** User (Frontend behavior issue)

---

## Problem Statement

When clicking "Practice This Topic" from Grammar → Browse Topics page, the application gets stuck on a loading page and never shows exercises.

**User Flow:**
1. Navigate to Grammar → Browse Topics
2. Select any topic (e.g., "Nominative Case")
3. Click "Practice This Topic" button
4. Page shows loading spinner indefinitely
5. Never loads exercises

---

## Root Cause

### Issue: Over-Restrictive Filter Combination

The frontend sends **BOTH** `topic_ids` AND `difficulty_level` filters to the backend:

```typescript
// frontend/src/pages/grammar/PracticeSessionPage.tsx:181-186
const session = await grammarService.startPracticeSession({
  topic_ids: topicIds,                      // e.g., [1]
  difficulty_level: difficultyParam as any,  // May default to "B2" or user's profile level
  exercise_count: countParam ? parseInt(countParam) : 10,
  use_spaced_repetition: true,
});
```

**The Problem:**
- Topic 1 (Nominative Case) has exercises at **A1 difficulty only**
- If `difficulty_level="B2"` is sent (from URL param or user profile), backend finds **NO exercises** that match BOTH filters
- Backend returns: `{"detail": "No exercises found matching the criteria"}`
- Frontend gets 404 error → shows loading forever (error not handled gracefully)

---

## Empirical Test Results

### Test Server: http://192.168.178.100:8000

**Test 1: No filters**
```json
Request: {"exercise_count": 10}
Response: ✅ SUCCESS - Session started (session_id: 2603)
```

**Test 2: Topic filter only**
```json
Request: {"topic_ids": [1]}
Response: ✅ SUCCESS - Session started with "Nominativ" exercises
```

**Test 3: Difficulty filter only (B2)**
```json
Request: {"difficulty_level": "B2"}
Response: ✅ SUCCESS - Session started with B2 exercises from various topics
```

**Test 4: BOTH filters (topic=1, difficulty=B2)**
```json
Request: {"topic_ids": [1], "difficulty_level": "B2"}
Response: ❌ FAILED - "No exercises found matching the criteria"
```

**Topic 1 Exercise Availability by Difficulty:**
```
Topic 1 (Nominative Case):
  A1: ✅ Has exercises
  A2: ❌ No exercises
  B1: ❌ No exercises
  B2: ❌ No exercises  ← User trying to practice at this level
  C1: ❌ No exercises
  C2: ❌ No exercises
```

---

## Why This Happens

### Scenario 1: URL Parameter

User's profile might have `proficiency_level: "B2"`. Frontend might auto-add this to URL:
```
/grammar/practice?topics=1&difficulty=B2
```

### Scenario 2: Default Difficulty

Frontend might have a default difficulty setting that's applied when user clicks "Practice This Topic".

### Scenario 3: Previous Session State

User previously practiced at B2 level, setting saved in localStorage or store, applied to new session.

---

## Impact

### User Experience
- 🔴 **Complete blocking issue** - Cannot practice grammar topics
- 🔴 Loading spinner shows indefinitely
- 🔴 No error message displayed to user
- 🔴 User has no idea what went wrong
- 🔴 Must close page and try again (same result)

### Scope
- ✅ Backend works correctly (following API specification)
- ❌ Frontend doesn't handle "no exercises" error gracefully
- ❌ Filter combination too restrictive
- ❌ UI doesn't show helpful error message

### Workaround
- Remove difficulty parameter from URL manually
- Or: Pick a topic that has B2 exercises

---

## Solutions

### Option 1: Frontend Fix - Remove Default Difficulty (RECOMMENDED)

**Change:** Don't send `difficulty_level` when user clicks "Practice This Topic" from topics page.

**File:** `frontend/src/pages/grammar/PracticeSessionPage.tsx`

**Current Code (lines 173-186):**
```typescript
const startSession = async () => {
  setSessionState('loading');
  try {
    const topicsParam = searchParams.get('topics');
    const difficultyParam = searchParams.get('difficulty');
    const countParam = searchParams.get('count');

    const topicIds = topicsParam ? topicsParam.split(',').map(Number) : undefined;

    const session = await grammarService.startPracticeSession({
      topic_ids: topicIds,
      difficulty_level: difficultyParam as any,  // ← Problem: may send B2 when topic only has A1
      exercise_count: countParam ? parseInt(countParam) : 10,
      use_spaced_repetition: true,
    });
```

**Fixed Code:**
```typescript
const startSession = async () => {
  setSessionState('loading');
  try {
    const topicsParam = searchParams.get('topics');
    const difficultyParam = searchParams.get('difficulty');
    const countParam = searchParams.get('count');

    const topicIds = topicsParam ? topicsParam.split(',').map(Number) : undefined;

    const session = await grammarService.startPracticeSession({
      topic_ids: topicIds,
      // Only send difficulty_level if explicitly specified in URL
      ...(difficultyParam && { difficulty_level: difficultyParam as any }),
      exercise_count: countParam ? parseInt(countParam) : 10,
      use_spaced_repetition: true,
    });
```

**Benefit:** Topic practice will use ALL difficulty levels for that topic (not filtered)

---

### Option 2: Frontend Fix - Better Error Handling (ALSO RECOMMENDED)

**Change:** Show helpful error message when "No exercises found".

**File:** `frontend/src/pages/grammar/PracticeSessionPage.tsx`

**Current Code (lines 206-210):**
```typescript
} catch (error) {
  const apiError = error as ApiError;
  addToast('error', 'Failed to start session', apiError.detail);
  setSessionState('error');
}
```

**Enhanced Code:**
```typescript
} catch (error) {
  const apiError = error as ApiError;

  // Check for "no exercises" error
  if (apiError.detail?.includes('No exercises found')) {
    const difficultyParam = searchParams.get('difficulty');
    const topicsParam = searchParams.get('topics');

    if (difficultyParam && topicsParam) {
      // Specific message for filter mismatch
      addToast(
        'warning',
        'No exercises found',
        `This topic doesn't have ${difficultyParam} level exercises. Try without difficulty filter.`
      );

      // Offer to retry without difficulty filter
      const retryUrl = `/grammar/practice?topics=${topicsParam}&count=${searchParams.get('count') || 10}`;
      navigate(retryUrl);
      return;
    }
  }

  addToast('error', 'Failed to start session', apiError.detail);
  setSessionState('error');
}
```

**Benefit:**
- User sees helpful message
- Automatically retries without difficulty filter
- Better UX

---

### Option 3: Backend Fix - Fallback to Available Exercises (OPTIONAL)

**Change:** If no exercises match BOTH filters, relax the difficulty filter.

**File:** `backend/app/api/v1/grammar.py`

**Current Code (lines 130-156):**
```python
# Build query for exercises
query = db.query(GrammarExercise)

# Filter by topics
if request.topic_ids:
    query = query.filter(GrammarExercise.topic_id.in_(request.topic_ids))

# Filter by difficulty
if request.difficulty_level:
    query = query.filter(GrammarExercise.difficulty_level == request.difficulty_level)

# Get exercises
all_exercises = query.all()

if not all_exercises:
    raise HTTPException(
        status_code=404,
        detail="No exercises found matching the criteria"
    )
```

**Enhanced Code:**
```python
# Build query for exercises
query = db.query(GrammarExercise)

# Filter by topics
if request.topic_ids:
    query = query.filter(GrammarExercise.topic_id.in_(request.topic_ids))

# Try with difficulty filter first
difficulty_query = query
if request.difficulty_level:
    difficulty_query = query.filter(GrammarExercise.difficulty_level == request.difficulty_level)

# Get exercises
all_exercises = difficulty_query.all()

# If no exercises with difficulty filter, fallback to topic-only exercises
if not all_exercises and request.difficulty_level and request.topic_ids:
    all_exercises = query.all()  # Just topic filter, no difficulty

    if all_exercises:
        # Log fallback for monitoring
        logger.info(
            f"No {request.difficulty_level} exercises for topics {request.topic_ids}, "
            f"falling back to all difficulty levels"
        )

if not all_exercises:
    raise HTTPException(
        status_code=404,
        detail="No exercises found matching the criteria"
    )
```

**Benefit:**
- More forgiving behavior
- User gets exercises even if difficulty doesn't match perfectly
- Backend doesn't strictly enforce filter combinations

---

## Recommended Solution

**Implement BOTH Option 1 and Option 2:**

1. **Option 1 (Frontend):** Don't send default difficulty when practicing specific topic
   - Quick fix (5 minutes)
   - Solves immediate problem
   - Better UX (let topic determine difficulty)

2. **Option 2 (Frontend):** Add better error handling
   - Graceful degradation (10 minutes)
   - Helpful error messages
   - Auto-retry without filters

**Optional:** Option 3 (Backend) for even more forgiving behavior

---

## Testing Plan

### Before Fix

**Test Case:** Click "Practice This Topic" for Nominative Case
- [ ] User sees loading spinner
- [ ] Loading spinner shows indefinitely
- [ ] Browser console shows 404 error
- [ ] No error message displayed to user

### After Fix (Option 1)

**Test Case:** Click "Practice This Topic" for Nominative Case
- [ ] User sees loading spinner (brief)
- [ ] Practice session starts with A1 exercises (available for topic)
- [ ] Exercises display correctly
- [ ] No errors

### After Fix (Option 1 + Option 2)

**Test Case 1:** Click "Practice This Topic" for Nominative Case
- [ ] Practice session starts with appropriate exercises
- [ ] No errors

**Test Case 2:** Manually add `?difficulty=B2` to URL for Topic 1
- [ ] Shows warning toast: "This topic doesn't have B2 level exercises..."
- [ ] Automatically retries without difficulty filter
- [ ] Practice session starts successfully
- [ ] Exercises display correctly

---

## Files to Modify

### Frontend (Option 1 + Option 2)
- `frontend/src/pages/grammar/PracticeSessionPage.tsx`
  - Line 184: Change `difficulty_level` to conditional
  - Lines 206-210: Add better error handling with retry

### Backend (Option 3 - Optional)
- `backend/app/api/v1/grammar.py`
  - Lines 130-156: Add fallback logic for difficulty filter

---

## Related Issues

- User expects clicking "Practice This Topic" to just work
- Other topics may have same issue if they lack higher-level exercises
- Mixed practice (no topic filter) works fine

---

## Priority & Assignment

**Priority:** P0 - CRITICAL (blocking feature)

**Frontend Team:**
- Option 1: 5 minutes - Remove default difficulty
- Option 2: 10 minutes - Better error handling
- **Total:** 15 minutes

**Backend Team (Optional):**
- Option 3: 20 minutes - Add fallback logic

**QA Team:**
- Test all grammar topics with various difficulty levels
- Verify error messages are helpful
- Test retry behavior

---

## Verification Checklist

**Before deploying fix:**
- [ ] Test clicking "Practice This Topic" for Topic 1 (Nominative)
- [ ] Test clicking "Practice This Topic" for Topic 2, 3, 4, 5
- [ ] Test "Start Mixed Practice" (no topic filter)
- [ ] Test with URL param `?difficulty=B2`
- [ ] Test with URL param `?difficulty=A1`
- [ ] Check browser console for errors
- [ ] Verify toast notifications are helpful

**After deploying fix:**
- [ ] All above tests pass
- [ ] No console errors
- [ ] Loading spinner disappears quickly
- [ ] Exercises display correctly
- [ ] Error messages helpful (if testing edge cases)

---

## Additional Notes

### Why This Wasn't Caught Earlier

1. The BUG-016 fix for quiz persistence was unrelated
2. Frontend E2E tests may use mock data (all difficulty levels available)
3. Backend unit tests don't test filter combinations
4. QA testing may have tested topics that have exercises at all levels

### Why User Profile Difficulty Matters

Users have `proficiency_level` in their profile (e.g., "B2"). Frontend might use this as a default for:
- Recommended practice sessions
- Auto-filtering exercises
- Personalizing difficulty

But when user explicitly selects a topic, they want to practice THAT TOPIC regardless of difficulty.

---

## Summary

✅ **Root Cause:** Frontend sends topic_ids=[1] + difficulty_level="B2", but Topic 1 only has A1 exercises
✅ **Backend Behavior:** Correctly returns 404 (no exercises match both filters)
✅ **Frontend Issue:** Doesn't handle 404 gracefully, shows loading forever
✅ **Solution:** Don't send default difficulty when practicing specific topic + add error handling
✅ **Effort:** 15 minutes (frontend changes)

---

**Report Generated:** 2026-01-19
**Investigated By:** Claude Code (Frontend + Backend Analysis)
**Test Results:** /tmp/test-grammar-practice.sh, /tmp/diagnose-grammar-issue.sh

---

**END OF REPORT**
