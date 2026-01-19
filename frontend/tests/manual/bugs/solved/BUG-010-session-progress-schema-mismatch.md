# BUG-010: Session Progress Schema Mismatch

**Severity:** Critical
**Category:** Grammar Practice / API Contract
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Fixed
**Fixed:** 2026-01-19
**Fix:** Backend updated field names in session_progress response

---

## Description

When submitting an answer during a grammar practice session, the application crashes with a blank page and JavaScript error. The backend returns a `session_progress` object with field names that don't match what the frontend expects.

---

## Error Message

```
TypeError: undefined is not an object (evaluating 'progress.accuracy_percentage.toFixed')
    reportError (SessionHeader.tsx:98)
```

---

## Root Cause

**Schema mismatch between backend and frontend:**

### Backend Response (grammar.py:437-443)

```python
session_progress = {
    "completed": total_attempted,
    "total": session.total_exercises,
    "correct": session.exercises_correct,
    "accuracy": (session.exercises_correct / total_attempted * 100) if total_attempted > 0 else 0
}
```

### Frontend Expected (grammar.types.ts:94-99)

```typescript
interface SessionProgress {
  exercises_completed: number;
  exercises_correct: number;
  current_streak: number;
  total_points: number;
  accuracy_percentage: number;
}
```

### Field Mapping Issues

| Backend Field | Frontend Expected | Status |
|---------------|-------------------|--------|
| `completed` | `exercises_completed` | Name mismatch |
| `correct` | `exercises_correct` | Name mismatch |
| `accuracy` | `accuracy_percentage` | Name mismatch |
| (missing) | `current_streak` | Missing |
| (missing) | `total_points` | Missing |
| `total` | (unused) | Extra field |

---

## Reproduction Steps

1. Navigate to Grammar Topics (`/grammar`)
2. Select any topic and click "Start Practice"
3. Session starts, first exercise loads correctly
4. Enter any answer and click "Check Answer"
5. **CRASH**: Blank page with console error

---

## Files Involved

### Backend
- `/backend/app/api/v1/grammar.py` - Lines 437-443 (session_progress construction)
- `/backend/app/schemas/grammar.py` - Line 125 (SubmitExerciseAnswerResponse)

### Frontend
- `/frontend/src/api/types/grammar.types.ts` - Lines 94-99 (SessionProgress interface)
- `/frontend/src/components/grammar/SessionHeader.tsx` - Line 73 (accesses accuracy_percentage)
- `/frontend/src/pages/grammar/PracticeSessionPage.tsx` - Line 114 (sets progress from response)

---

## Recommended Fix

### Option A: Update Backend (Recommended)

Update `/backend/app/api/v1/grammar.py` lines 437-443:

```python
session_progress = {
    "exercises_completed": total_attempted,
    "exercises_correct": session.exercises_correct,
    "current_streak": 0,  # Track in session or calculate
    "total_points": session.total_points if hasattr(session, 'total_points') else 0,
    "accuracy_percentage": (session.exercises_correct / total_attempted * 100) if total_attempted > 0 else 0
}
```

### Option B: Update Frontend

Update `/frontend/src/api/types/grammar.types.ts` and all consuming components to match backend field names. Would require changes in multiple frontend files.

### Option C: Add Transformation Layer

Add a transformation in the grammar service to map backend response to frontend types:

```typescript
// In grammarService.ts
const response = await api.post<BackendSubmitResponse>(...);
return {
  ...response,
  session_progress: {
    exercises_completed: response.session_progress.completed,
    exercises_correct: response.session_progress.correct,
    accuracy_percentage: response.session_progress.accuracy,
    current_streak: 0,
    total_points: 0,
  }
};
```

---

## Impact

| Aspect | Impact |
|--------|--------|
| **User Impact** | Critical - Grammar Practice completely unusable after first answer |
| **Feature Impact** | Grammar Practice Session broken |
| **Test Impact** | All exercise submission tests fail |

---

## Priority

**CRITICAL** - This bug completely blocks the Grammar Practice feature. Users cannot complete any exercises.

---

## Related Files

| File | Line | Purpose |
|------|------|---------|
| `/backend/app/api/v1/grammar.py` | 437-443 | Constructs session_progress dict |
| `/backend/app/schemas/grammar.py` | 125 | Schema defines dict type |
| `/frontend/src/api/types/grammar.types.ts` | 94-99 | SessionProgress interface |
| `/frontend/src/components/grammar/SessionHeader.tsx` | 73 | Crashes on .toFixed() |

---

## Notes

This is a critical API contract mismatch. The backend and frontend were developed with different assumptions about the session_progress structure. This needs to be fixed before Grammar Practice can be used.

The initial session (startPracticeSession) works correctly because PracticeSessionPage.tsx initializes progress locally (lines 66-72). The crash occurs when the backend returns session_progress after answer submission.

---

## Test Coverage Added

**File:** `/frontend/tests/e2e/grammar-practice.spec.ts`

**New test section:** "Session Progress Update (BUG-010 Regression)"

5 new tests added to catch this bug in future:

1. **should display session stats in header** - Verifies Accuracy, Correct, Points are visible
2. **should update progress stats after answer submission without crashing** - Submits answer and verifies page doesn't crash
3. **should verify API response has correct session_progress schema** - Intercepts API and validates required fields exist
4. **should increment exercises_completed after each submission** - Verifies progress tracking works
5. **should not crash when displaying zero accuracy** - Edge case for 0% accuracy handling

These tests will fail until BUG-010 is fixed, providing clear regression coverage.
