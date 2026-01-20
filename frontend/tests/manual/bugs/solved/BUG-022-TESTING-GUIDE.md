# BUG-022: Session Restore Fix - Testing Guide

**Date:** 2026-01-20
**Bug:** Grammar Practice session restore with stale localStorage
**Status:** Fixes Implemented - Ready for Testing

## Overview

This guide provides step-by-step instructions for testing the BUG-022 fixes that address:
1. **White page loop** when resuming sessions with expired backend sessions
2. **Stale localStorage** causing incorrect "Resume Previous Session?" prompts

## Fixes Implemented

### ✅ Phase 1: Graceful Error Handling
**File:** `/frontend/src/pages/grammar/PracticeSessionPage.tsx`
- Made `handleRestoreSession()` async with proper error handling
- Errors from `loadSessionFromStore()` now trigger automatic fallback to `handleStartFresh()`
- User-friendly toast notification: "Session Expired - Starting fresh..."

### ✅ Phase 2: Backend Session Validation
**File:** `/frontend/src/hooks/useSessionPersistence.ts`
- Added `validateBackendSession()` function
- Validates backend session **before** showing "Resume Previous Session?" modal
- Automatically clears localStorage if backend session is expired/invalid
- Prevents modal from showing for non-existent sessions

## Pre-Test Setup

### 1. Build and Deploy Frontend
```bash
cd /Users/igorparis/PycharmProjects/myGermanAITeacher/frontend
npm run build
# Or for dev mode:
npm run dev
```

### 2. Ensure Backend is Running
```bash
# Check backend status
curl http://192.168.178.100:8000/api/health

# Should return: {"status": "healthy"}
```

### 3. Prepare Test Account
- Username: `igor@test.com` (or your test account)
- Password: Your test password
- Ensure account has access to Grammar Practice

---

## Test Scenarios

## Test 1: Stale localStorage with Expired Backend Session ⭐ PRIMARY TEST

**Goal:** Verify that expired backend sessions are detected and cleared automatically

### Setup:
1. **Create stale localStorage:**
   - Open browser (Chrome/Firefox)
   - Navigate to `http://192.168.178.100:5173`
   - Login with test credentials
   - Navigate to Grammar → Browse Topics
   - Click "Practice This Topic" on Topic 1 (Nominative Case)
   - Complete 2-3 exercises
   - **Important:** Do NOT complete the session - leave it incomplete
   - Note the session ID from browser console (if visible) or DevTools

2. **Expire the backend session:**
   - Option A: Wait 2-4 hours (backend timeout)
   - Option B: Manually delete session from database (faster):
     ```sql
     -- Connect to database
     psql -U german_app_user -d german_learning

     -- Find recent sessions
     SELECT id, user_id, created_at FROM grammar_sessions
     WHERE user_id = <your_user_id>
     ORDER BY created_at DESC LIMIT 5;

     -- Delete the session
     DELETE FROM grammar_sessions WHERE id = <session_id>;
     ```
   - Option C: Restart backend server (clears in-memory sessions if any)

### Test Steps:
1. **Close and reopen browser** (keep localStorage)
2. Navigate to `http://192.168.178.100:5173/grammar`
3. **Observe what happens** when you click "Practice This Topic"

### Expected Results (AFTER FIX):
- ✅ **Phase 2 validation triggers:**
  - Page loads normally
  - **NO "Resume Previous Session?" modal appears**
  - localStorage is automatically cleared
  - New session starts immediately
  - Console log: `"Session {id} not found in backend, clearing localStorage"`

- ✅ **Alternative (if Phase 2 doesn't catch it):**
  - Modal appears briefly
  - User clicks "Resume Session"
  - Toast appears: "Session Expired - Starting a fresh session..."
  - Modal closes
  - New session starts successfully
  - No white page loop

### ❌ Expected Results (WITHOUT FIX - OLD BEHAVIOR):
- Modal appears
- User clicks "Resume Session"
- Page shows white loading spinner forever
- OR: Error page appears
- Console error: `404 GET /api/grammar/practice/{id}/next`

### Success Criteria:
- [ ] No white page loop occurs
- [ ] Stale localStorage is cleared automatically
- [ ] New session starts successfully
- [ ] User sees helpful toast message (if manual resume attempted)
- [ ] Console shows validation log

---

## Test 2: Valid Incomplete Session (Recent)

**Goal:** Verify that valid incomplete sessions can still be resumed

### Setup:
1. Open browser (private/incognito mode recommended)
2. Navigate to `http://192.168.178.100:5173`
3. Login with test credentials
4. Navigate to Grammar → Browse Topics
5. Click "Practice This Topic" on Topic 1
6. Complete 2-3 exercises
7. **Navigate away** (to /dashboard or /grammar) WITHOUT completing session

### Test Steps:
1. **Immediately** navigate back to Grammar → Browse Topics
2. Click "Practice This Topic" on same topic

### Expected Results:
- ✅ "Resume Previous Session?" modal appears
- ✅ Click "Resume Session"
- ✅ Session resumes from where you left off
- ✅ Previous answers are preserved
- ✅ Toast: "Session restored - Continuing from where you left off"
- ✅ No errors in console

### Success Criteria:
- [ ] Modal appears for valid incomplete session
- [ ] Resuming works correctly
- [ ] Session data is preserved (answers, progress)
- [ ] No console errors

---

## Test 3: "Start Fresh" Button

**Goal:** Verify "Start Fresh" clears localStorage and starts new session

### Setup:
1. Follow Test 2 setup to create an incomplete session
2. Navigate away and return to trigger modal

### Test Steps:
1. Modal appears: "Resume Previous Session?"
2. Click **"Start Fresh"** button

### Expected Results:
- ✅ Modal closes
- ✅ localStorage is cleared
- ✅ New session starts (not resuming old session)
- ✅ Previous session data is gone
- ✅ No errors in console

### Success Criteria:
- [ ] "Start Fresh" clears old session
- [ ] New session starts successfully
- [ ] No data from previous session
- [ ] No console errors

---

## Test 4: Page Refresh During Active Session

**Goal:** Verify session persistence across page refreshes

### Setup:
1. Start a new grammar practice session
2. Complete 2-3 exercises
3. Do NOT navigate away

### Test Steps:
1. **Refresh the page** (F5 or Cmd+R)
2. Observe behavior

### Expected Results:
- ✅ Modal appears: "Resume Previous Session?"
- ✅ Click "Resume Session"
- ✅ Session resumes with previous answers intact
- ✅ Continue practicing from where you left off

### Success Criteria:
- [ ] Page refresh doesn't lose session data
- [ ] Resume works correctly after refresh
- [ ] All previous answers preserved
- [ ] No console errors

---

## Test 5: Session Age > 24 Hours

**Goal:** Verify automatic expiry after 24 hours

### Setup:
1. Manually modify localStorage to simulate old session:
   - Open DevTools → Application → Local Storage
   - Find key: `german-learning-grammar-store`
   - Edit JSON:
     ```json
     {
       "state": {
         "currentSession": {
           "sessionId": 9999,
           "startTime": 1234567890000,  // Very old timestamp
           "answers": [],
           "exerciseIndex": 0,
           "isPaused": false,
           "pausedAt": null,
           "totalPausedTime": 0
         },
         "sessionState": "active",
         "currentExercise": null
       }
     }
     ```
   - Set `startTime` to: `Date.now() - (25 * 60 * 60 * 1000)` (25 hours ago)

### Test Steps:
1. Refresh page
2. Navigate to Grammar → Practice This Topic

### Expected Results:
- ✅ No modal appears (session is expired)
- ✅ localStorage is automatically cleared
- ✅ New session starts
- ✅ Console log: Session age check clears old session

### Success Criteria:
- [ ] Sessions > 24 hours old are auto-cleared
- [ ] No modal for expired sessions
- [ ] New session starts cleanly
- [ ] No console errors

---

## Test 6: Multiple Browser Windows

**Goal:** Verify behavior with multiple windows sharing localStorage

### Setup:
1. Open Window A: Start a grammar practice session
2. Complete 2-3 exercises
3. Open Window B: Same URL

### Test Steps:
1. In Window B, navigate to Grammar → Practice This Topic
2. Observe modal behavior

### Expected Results:
- ✅ Window B shows "Resume Previous Session?" modal (same session from Window A)
- ✅ Click "Resume Session" in Window B
- ✅ Backend validates session (should still exist if recent)
- ✅ Window B resumes the session

### Success Criteria:
- [ ] localStorage shared across windows
- [ ] Both windows can resume same session
- [ ] Backend validation works
- [ ] No console errors

---

## Test 7: Private Browsing Mode

**Goal:** Verify private browsing works as baseline (no regressions)

### Setup:
1. Open private/incognito window
2. Navigate to `http://192.168.178.100:5173`
3. Login with test credentials

### Test Steps:
1. Navigate to Grammar → Practice This Topic
2. Complete 2-3 exercises
3. Navigate away to /dashboard
4. Return to Grammar → Practice This Topic

### Expected Results:
- ✅ First time: No modal (fresh session starts)
- ✅ After navigate away: Modal appears
- ✅ Click "Resume": Session resumes successfully
- ✅ No console errors

### Success Criteria:
- [ ] Private browsing works correctly
- [ ] Modal behavior matches expected
- [ ] Resume works
- [ ] No regressions

---

## Test 8: Network Error During Validation

**Goal:** Verify graceful handling of network errors

### Setup:
1. Create incomplete session
2. Stop backend server OR block network in DevTools
3. Refresh page

### Test Steps:
1. Open DevTools → Network → Enable "Offline" mode
2. Refresh page
3. Navigate to Grammar

### Expected Results:
- ✅ Backend validation fails (network error)
- ✅ Session is NOT cleared (benefit of the doubt)
- ✅ Modal appears asking to resume
- ✅ Clicking "Resume" may fail (network still offline)
- ✅ Re-enable network and retry
- ✅ Works after network restored

### Success Criteria:
- [ ] Network errors don't clear valid sessions
- [ ] User can retry when network restored
- [ ] Appropriate error messages shown
- [ ] No infinite loops

---

## Debugging Tips

### Check localStorage:
```javascript
// In browser console:
const store = localStorage.getItem('german-learning-grammar-store');
console.log(JSON.parse(store));
```

### Check session age:
```javascript
const store = JSON.parse(localStorage.getItem('german-learning-grammar-store'));
const startTime = store.state.currentSession?.startTime;
const ageHours = (Date.now() - startTime) / (1000 * 60 * 60);
console.log(`Session age: ${ageHours.toFixed(2)} hours`);
```

### Clear localStorage manually:
```javascript
localStorage.removeItem('german-learning-grammar-store');
location.reload();
```

### Check backend session:
```bash
# Get JWT token from browser (DevTools → Application → Local Storage)
# Look for key containing 'auth' or 'token'

# Test session endpoint
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     http://192.168.178.100:8000/api/grammar/practice/SESSION_ID/next
```

---

## Success Criteria Summary

**Fix is considered successful if ALL these conditions are met:**

1. ✅ **No white page loops** with stale localStorage
2. ✅ **Expired backend sessions** are auto-detected and cleared
3. ✅ **Valid incomplete sessions** can be resumed successfully
4. ✅ **"Start Fresh" button** works correctly
5. ✅ **User sees helpful messages** explaining what's happening
6. ✅ **No regressions** in existing functionality
7. ✅ **Private browsing** works as before
8. ✅ **Page refresh** preserves session data
9. ✅ **24-hour expiry** automatically clears old sessions
10. ✅ **No console errors** during normal operations

---

## Test Report Template

After completing tests, document results using this template:

```markdown
# BUG-022 Test Report

**Tester:** [Your Name]
**Date:** [YYYY-MM-DD]
**Frontend Version:** [commit hash or version]
**Backend Version:** [commit hash or version]
**Browser:** [Chrome/Firefox/Safari + version]

## Test Results

| Test | Status | Notes |
|------|--------|-------|
| Test 1: Stale localStorage | ✅/❌ | [Details] |
| Test 2: Valid incomplete session | ✅/❌ | [Details] |
| Test 3: Start Fresh button | ✅/❌ | [Details] |
| Test 4: Page refresh | ✅/❌ | [Details] |
| Test 5: Session > 24h | ✅/❌ | [Details] |
| Test 6: Multiple windows | ✅/❌ | [Details] |
| Test 7: Private browsing | ✅/❌ | [Details] |
| Test 8: Network error | ✅/❌ | [Details] |

## Issues Found
[List any issues discovered during testing]

## Recommendations
[Any recommendations for improvements]

## Overall Assessment
✅ PASS / ❌ FAIL

**Reason:** [Brief explanation]
```

---

**Last Updated:** 2026-01-20
**Next Steps:** Execute all test scenarios and document results
