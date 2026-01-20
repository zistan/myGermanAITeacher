# BUG-022: Grammar Practice Session Restore Investigation

**Date:** 2026-01-20
**Severity:** High (P1)
**Category:** Grammar Module
**Status:** Under Investigation

## Problem Description

### Scenario 1: Cached Browser - White Page Loop
When attempting to start a grammar practice session in a cached browser (with existing localStorage), the application enters a white page loop or gets stuck in a loading state.

### Scenario 2: Private Browsing - Resume Dialog
In private browsing mode, a "Resume Previous Session?" dialog appears unexpectedly after navigating away and returning to practice.

## Root Cause Analysis

### Hypothesis
The frontend's incomplete session detection (`hasIncompleteSession()`) checks if a session exists in localStorage and is < 24 hours old, but **does NOT validate whether the backend session still exists**.

**Failure Scenario:**
1. User starts a session (e.g., sessionId: 2606) with `sessionState: 'active'`
2. User closes browser or navigates away
3. **Backend session expires** after 1-2 hours (typical backend timeout)
4. User returns within 24 hours (localStorage still valid)
5. Frontend detects "incomplete" session from localStorage
6. Shows "Resume Previous Session?" dialog
7. User clicks "Resume Session"
8. Frontend tries to load exercises from sessionId 2606
9. **Backend returns 404** (session no longer exists)
10. Frontend gets stuck in loading state or error state

### Evidence from Code Review

**File: `/frontend/src/store/grammarStore.ts` (lines 264-274)**
```typescript
hasIncompleteSession: () => {
  const state = get();
  if (!state.currentSession) return false;

  const ageHours = get().getSessionAge();
  if (ageHours !== null && ageHours > SESSION_EXPIRY_HOURS) {
    return false;
  }

  // ❌ MISSING: Backend session validation
  return state.sessionState !== 'completed' && state.sessionState !== 'idle';
}
```

**File: `/frontend/src/pages/grammar/PracticeSessionPage.tsx` (lines 110-153)**
```typescript
const loadSessionFromStore = async (restoredSessionId: number) => {
  setSessionState('loading');
  try {
    // ... tries to load exercise from backend
    await loadNextExercise(restoredSessionId);
    // ✅ Has error handling but shows warning toast only
  } catch (error) {
    const apiError = error as ApiError;
    addToast('warning', 'Could not restore session', 'Starting a new session instead');
    startSession(); // ⚠️ Called without await, may not clear stale session properly
  }
};
```

**File: `/frontend/src/pages/grammar/PracticeSessionPage.tsx` (lines 155-163)**
```typescript
const handleRestoreSession = () => {
  setShowRestoreModal(false);
  const session = restoreSession();
  if (session) {
    loadSessionFromStore(session.sessionId); // ⚠️ Called without await
  } else {
    startSession();
  }
};
```

**Issues Identified:**
1. ❌ No backend session validation before showing resume dialog
2. ⚠️ `loadSessionFromStore()` called without `await` (fire-and-forget)
3. ⚠️ Error handling relies on toast notifications instead of graceful fallback
4. ⚠️ `startSession()` in catch block not awaited, may cause race conditions
5. ⚠️ Stale localStorage not cleared before retry

## Test Plan

### Test 1: Verify localStorage State (Cached Browser)
**Goal:** Identify what's stored in localStorage

**Steps:**
1. Open cached browser where issue occurs
2. Open DevTools → Application → Local Storage → `http://192.168.178.100:5173`
3. Find key `'german-learning-grammar-store'`
4. Document:
   - `sessionState`
   - `currentSession.sessionId`
   - `currentSession.startTime` (calculate age)
   - `currentExercise`

**Expected Finding:** Old session data with sessionId that no longer exists in backend

### Test 2: Reproduce White Page Loop
**Goal:** Confirm the white page loop and capture errors

**Steps:**
1. In cached browser, navigate to `http://192.168.178.100:5173/grammar`
2. Click "Practice This Topic" on any topic
3. Open DevTools → Console & Network tabs
4. Document:
   - Does page go white?
   - Does modal appear?
   - Console errors?
   - Network 404 errors?

**Expected Finding:** API 404 error on `/api/grammar/practice/{sessionId}/next`

### Test 3: Verify Session Expiry Logic
**Goal:** Check if 24-hour expiry works correctly

**Steps:**
1. Check `currentSession.startTime` in localStorage
2. Calculate age: `(Date.now() - startTime) / (1000 * 60 * 60)` hours
3. If age > 24 hours: Should auto-clear
4. If age < 24 hours: Should show resume dialog

**Expected Finding:** If age > 24 hours, expiry logic might not be running

### Test 4: Test "Start Fresh" Functionality
**Goal:** Verify clearing stale session works

**Steps:**
1. Navigate to `/grammar/practice?topics=1`
2. If modal appears, click "Start Fresh"
3. Verify new session starts successfully
4. Check localStorage is cleared

**Expected Finding:** "Start Fresh" should work correctly

### Test 5: Private Browsing Baseline
**Goal:** Confirm private browsing works correctly

**Steps:**
1. Open private/incognito window
2. Login and navigate to `/grammar`
3. Click "Practice This Topic"
4. Verify new session starts (no modal)
5. Navigate away and return
6. Verify modal appears for incomplete session
7. Click "Resume" and verify it works

**Expected Finding:** Private browsing works correctly (this is the baseline)

### Test 6: Backend Session Validation
**Goal:** Verify backend session state

**Steps:**
1. Get sessionId from localStorage
2. Try to fetch from backend:
   ```bash
   curl -H "Authorization: Bearer <token>" \
        http://192.168.178.100:8000/api/grammar/practice/{sessionId}/next
   ```
3. Document response (200 OK vs 404 Not Found)

**Expected Finding:** 404 error confirming backend session expired

## Proposed Fix

### Phase 1: Quick Fix (Graceful Error Handling) ✅ Implemented
**File:** `/frontend/src/pages/grammar/PracticeSessionPage.tsx`

**Changes:**
1. ✅ Make `handleRestoreSession` async and await `loadSessionFromStore`
2. ✅ Catch errors and automatically call `handleStartFresh()`
3. ✅ Show helpful toast: "Your previous session expired. Starting fresh..."
4. ✅ Ensure stale localStorage is cleared before starting new session

### Phase 2: Comprehensive Fix (Backend Validation) ✅ Implemented
**File:** `/frontend/src/hooks/useSessionPersistence.ts`

**Changes:**
1. ✅ Add `validateBackendSession()` helper function
2. ✅ Validate backend session before showing restore dialog
3. ✅ If validation fails (404), clear localStorage and call `onSessionExpired`
4. ✅ Only show resume dialog if backend session exists

## Implementation Status

### ✅ Phase 1: Graceful Error Handling (COMPLETE)
- Fixed `handleRestoreSession` to be async with proper error handling
- Added automatic fallback to `handleStartFresh()` on restore failure
- Added user-friendly toast notifications
- Ensures localStorage is cleared before retry

### ✅ Phase 2: Backend Validation (COMPLETE)
- Added `validateBackendSession()` to useSessionPersistence hook
- Validates session with backend before showing modal
- Auto-clears expired sessions on mount
- Prevents modal from showing for invalid sessions

## Verification Checklist

After implementing fixes, verify:

- [ ] **Test 1:** Stale localStorage with old sessionId doesn't cause white page loop
- [ ] **Test 2:** "Resume Session" with expired backend session shows toast and starts fresh
- [ ] **Test 3:** Valid incomplete session (< 2 hours) shows modal and resumes correctly
- [ ] **Test 4:** "Start Fresh" clears localStorage and starts new session
- [ ] **Test 5:** Private browsing works as before (no regression)
- [ ] **Test 6:** Backend validation prevents modal for expired sessions
- [ ] **Test 7:** Page refresh during active session resumes correctly
- [ ] **Test 8:** Navigating away and back shows modal for valid sessions only

## Related Issues

- **BUG-020:** Grammar practice stuck loading (fixed - different issue, difficulty filter)
- **BUG-021:** Second session stuck loading (fixed - different issue, stale completed session)
- **BUG-022:** THIS ISSUE - localStorage persistence vs. backend session lifecycle mismatch

## Success Criteria

✅ **Fix is successful when:**
1. No white page loops occur with stale localStorage
2. Expired backend sessions are detected and cleared automatically
3. Valid incomplete sessions can be resumed without errors
4. User sees helpful messages explaining what's happening
5. No regression in existing session persistence functionality

---

**Last Updated:** 2026-01-20
**Next Steps:** Execute test plan and verify fixes
