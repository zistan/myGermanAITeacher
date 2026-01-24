# Keyboard Shortcuts Test Plan - Grammar Practice

**Date:** 2026-01-20
**Status:** Testing Required
**Issue:** Some keyboard shortcuts not behaving as expected (ESC white page, etc.)

---

## 🎹 Available Keyboard Shortcuts

### During Active Practice (sessionState = 'active')
| Key | Action | Expected Behavior | Priority |
|-----|--------|-------------------|----------|
| **Enter** | Submit answer | Submit current answer and show feedback | 10 |
| **Esc** | End session | End session gracefully and show results | 10 |
| **B** | Bookmark exercise | Toggle bookmark for current exercise | 10 |
| **N** | Toggle notes | Open/close notes panel | 10 |
| **F** | Toggle focus mode | Enter/exit focus mode | 10 |
| **P** | Pause session | Pause the session timer | 10 |

### During Feedback (sessionState = 'feedback')
| Key | Action | Expected Behavior | Priority |
|-----|--------|-------------------|----------|
| **Space** | Next exercise | Load next exercise | 10 |
| **Enter** | Next exercise | Load next exercise | 10 |
| **B** | Bookmark exercise | Toggle bookmark for current exercise | 10 |
| **N** | Toggle notes | Open/close notes panel | 10 |

### During Focus Mode (isFocusMode = true)
| Key | Action | Expected Behavior | Priority |
|-----|--------|-------------------|----------|
| **Esc** | Exit focus mode | Return to normal view | 100 (highest) |

### When Paused (sessionState = 'paused')
| Key | Action | Expected Behavior | Priority |
|-----|--------|-------------------|----------|
| **P** | Resume session | Resume the session timer | 50 |
| **Space** | Resume session | Resume the session timer | 50 |

---

## 🐛 Known Issues

### Issue 1: ESC Key White Page ⚠️ **CRITICAL**
**Reported Behavior:**
- Press ESC during active session
- Page navigates to white screen
- User stuck, cannot continue

**Expected Behavior:**
- Press ESC during active session
- API calls `endPracticeSession()`
- Navigate to `/grammar/results` with session results
- User sees results page with score, recommendations, etc.

**Potential Causes:**
1. ❌ API call fails (session incomplete, backend error)
2. ❌ Navigation happens without `results` state
3. ❌ ResultsPage receives invalid/missing data
4. ❌ Router not configured for `/grammar/results`
5. ❌ User doesn't want to "end session", wants to "exit/back to topics"

**Root Cause Analysis:**
Looking at the code:
- ESC triggers `handleEndSession()` (line 361-372 in PracticeSessionPage.tsx)
- `handleEndSession()` calls API: `grammarService.endPracticeSession(sessionId)`
- If API **fails**, shows toast but **doesn't navigate anywhere**
- User stuck on current page in broken state
- If API **succeeds** but user expected to go back to topics list, they see results page unexpectedly

**The REAL Issue:**
ESC should mean "EXIT/CANCEL" not "END SESSION AND SEE RESULTS"
- Users expect ESC to go back to topic list (like a back button)
- Not to forcefully end session and see results
- Current behavior is counter-intuitive

### Issue 2: Keyboard Shortcuts in Input Fields
**Potential Issue:**
- Some shortcuts should work in input fields (`allowInInput: true`)
- Some shouldn't (e.g., Space for next exercise when typing)

**Current Settings:**
- ESC: `allowInInput: true` ✅
- Enter: Default (blocked in inputs) ✅
- Space: `allowInInput: false` ✅
- B, N, F, P: Default (blocked in inputs) ⚠️

**Issue:** B, N, F, P might not work when focused on input

### Issue 3: Focus Mode Priority Conflict
**Potential Issue:**
- Focus mode ESC has priority 100
- Practice mode ESC has priority 10
- Should focus mode ESC override practice mode? (YES, currently correct)

---

## 🧪 Test Scenarios

### Test 1: ESC During Active Practice ⭐ **PRIMARY ISSUE**
**Setup:**
1. Start a grammar practice session
2. Answer 2-3 exercises
3. Stop in middle of session (don't complete)

**Test Steps:**
1. While on an active exercise (before submitting answer)
2. Press **ESC** key
3. Observe what happens

**Current Behavior (BROKEN):**
- [ ] White page appears
- [ ] Stuck, cannot navigate
- [ ] OR: Results page shows unexpectedly

**Expected Behavior (SHOULD BE):**
- [ ] User asked: "Are you sure you want to exit?" (confirmation modal)
- [ ] If confirm: Navigate to `/grammar` (topic list)
- [ ] Session remains **incomplete** in localStorage (can resume later)
- [ ] OR: Navigate to `/grammar/results` with partial results

**Alternative Expected Behavior:**
- [ ] Navigate to `/grammar/results` immediately
- [ ] Show results for completed exercises so far
- [ ] Clear success message, no errors

### Test 2: ESC After Submitting Answer (Feedback State)
**Setup:**
1. Start practice session
2. Submit an answer (now in feedback state)

**Test Steps:**
1. Press **ESC** while viewing feedback
2. Observe what happens

**Expected Behavior:**
- [ ] Should ESC work in feedback state? (Currently NO - feedback context doesn't have ESC)
- [ ] OR: Should it be ignored?

### Test 3: ESC in Focus Mode
**Setup:**
1. Start practice session
2. Press **F** to enter focus mode

**Test Steps:**
1. Press **ESC** while in focus mode
2. Observe what happens

**Expected Behavior:**
- [ ] Exits focus mode
- [ ] Returns to normal practice view
- [ ] Does NOT end session

### Test 4: Enter to Submit Answer
**Setup:**
1. Start practice session
2. Type an answer in the input field

**Test Steps:**
1. Type answer: "Das Haus"
2. Press **Enter**
3. Observe what happens

**Expected Behavior:**
- [ ] Answer is submitted
- [ ] Feedback is shown
- [ ] No errors

### Test 5: Space/Enter for Next Exercise (Feedback State)
**Setup:**
1. Start practice session
2. Submit an answer (see feedback)

**Test Steps:**
1. Press **Space** (or **Enter**)
2. Observe what happens

**Expected Behavior:**
- [ ] Loads next exercise
- [ ] Clears previous feedback
- [ ] Shows new exercise form

### Test 6: B for Bookmark
**Setup:**
1. Start practice session
2. On an active exercise

**Test Steps:**
1. Press **B** key
2. Check bookmark icon (should fill/unfill)
3. Press **B** again
4. Check bookmark icon (should toggle back)

**Expected Behavior:**
- [ ] Bookmark icon toggles
- [ ] Toast shows: "Bookmarked" or "Bookmark removed"
- [ ] No errors

### Test 7: N for Notes Panel
**Setup:**
1. Start practice session

**Test Steps:**
1. Press **N** key
2. Notes panel should open
3. Press **N** again
4. Notes panel should close

**Expected Behavior:**
- [ ] Notes panel toggles open/close
- [ ] No errors
- [ ] Works in both active and feedback states

### Test 8: F for Focus Mode
**Setup:**
1. Start practice session

**Test Steps:**
1. Press **F** key
2. Focus mode should activate
3. Press **ESC** (not F) to exit
4. Returns to normal view

**Expected Behavior:**
- [ ] Focus mode activates (minimal UI)
- [ ] ESC exits focus mode
- [ ] F key toggles focus mode

### Test 9: P for Pause/Resume
**Setup:**
1. Start practice session

**Test Steps:**
1. Press **P** key
2. Session should pause (overlay appears)
3. Press **P** or **Space**
4. Session should resume

**Expected Behavior:**
- [ ] Pause overlay appears
- [ ] Timer stops
- [ ] P or Space resumes
- [ ] Timer continues

### Test 10: Shortcuts While Typing in Input
**Setup:**
1. Start practice session
2. Focus on answer input field

**Test Steps:**
1. Start typing: "Das ist ein Buch"
2. While typing, try pressing:
   - **B** (should type 'b', not bookmark)
   - **N** (should type 'n', not open notes)
   - **F** (should type 'f', not focus mode)
   - **P** (should type 'p', not pause)
   - **ESC** (should work - exit session)
   - **Enter** (should submit answer)

**Expected Behavior:**
- [ ] Regular letters (B, N, F, P) should type normally
- [ ] ESC should work (allowInInput: true)
- [ ] Enter should submit answer

---

## 🔧 Proposed Fixes

### Fix 1: Change ESC Behavior (Recommended) ⭐
**Problem:** ESC should not "end session", it should "exit/go back"

**Solution Options:**

**Option A: ESC = Back to Topics (No Confirmation)**
```typescript
const handleExit = useCallback(() => {
  // Don't end session, just navigate back
  // Session stays in localStorage for resumption
  navigate('/grammar');
}, [navigate]);

// In practiceContext:
onExit: handleExit, // Instead of onEndSession
```

**Option B: ESC = Confirmation Modal → Exit**
```typescript
const handleExit = useCallback(() => {
  // Show confirmation modal
  setShowExitModal(true);
}, []);

const handleConfirmExit = useCallback(() => {
  // User confirmed, navigate back (session stays incomplete)
  navigate('/grammar');
}, [navigate]);
```

**Option C: ESC = End Session Gracefully**
```typescript
const handleEndSession = useCallback(async () => {
  if (!sessionId) {
    // No session, just navigate back
    navigate('/grammar');
    return;
  }

  try {
    const results = await grammarService.endPracticeSession(sessionId);
    storeEndSession();
    navigate('/grammar/results', { state: { results } });
  } catch (error) {
    // API failed, show error and navigate back to topics
    const apiError = error as ApiError;
    addToast('error', 'Failed to end session', apiError.detail);
    navigate('/grammar'); // Go back instead of staying stuck
  }
}, [sessionId, navigate, addToast, storeEndSession]);
```

**Recommendation:** **Option C** - End session gracefully, fallback to /grammar on error

### Fix 2: Add Confirmation Modal for ESC
```typescript
// Add state
const [showExitModal, setShowExitModal] = useState(false);

// Handler
const handleExitRequest = useCallback(() => {
  setShowExitModal(true);
}, []);

const handleConfirmExit = useCallback(async () => {
  setShowExitModal(false);
  await handleEndSession();
}, [handleEndSession]);

const handleCancelExit = useCallback(() => {
  setShowExitModal(false);
}, []);

// In practiceContext:
onEndSession: handleExitRequest,
```

### Fix 3: Add "Exit Session" Button in UI
Instead of relying only on ESC, add a visible button:
```tsx
<Button onClick={handleEndSession} variant="ghost" size="sm">
  Exit Session
</Button>
```

### Fix 4: Handle API Errors in handleEndSession
**Current code doesn't navigate on error:**
```typescript
} catch (error) {
  addToast('error', 'Failed to end session', apiError.detail);
  // ❌ User stuck here!
}
```

**Fix: Navigate back on error:**
```typescript
} catch (error) {
  addToast('error', 'Failed to end session', apiError.detail);
  navigate('/grammar'); // ✅ Go back to topics
}
```

---

## 📊 Test Checklist

After fixes are implemented:

- [ ] ESC during active practice navigates somewhere (not stuck)
- [ ] ESC in focus mode exits focus mode only (doesn't end session)
- [ ] Enter submits answer correctly
- [ ] Space/Enter in feedback state loads next exercise
- [ ] B toggles bookmark
- [ ] N toggles notes panel
- [ ] F toggles focus mode
- [ ] P pauses/resumes session
- [ ] All shortcuts work correctly when NOT in input fields
- [ ] Shortcuts don't interfere when typing in input fields
- [ ] No white page issues
- [ ] Clear user feedback for all actions

---

## 🎯 Priority Issues

1. **HIGH:** ESC key white page issue → Fix handleEndSession error handling
2. **MEDIUM:** ESC behavior clarification → Should it exit or end session?
3. **LOW:** Shortcut visibility → Add keyboard shortcut hints in UI

---

**Last Updated:** 2026-01-20
**Status:** Analysis complete, fixes ready to implement
