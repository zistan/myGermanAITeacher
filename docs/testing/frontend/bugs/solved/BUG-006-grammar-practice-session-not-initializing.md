# BUG-006: Grammar Practice Session Not Initializing Properly

**Severity:** Critical
**Category:** Grammar / API Integration
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Open - Backend Implementation Gap Identified
**Last Updated:** 2026-01-19

---

## Executive Summary

The Grammar Practice Session fails because the **frontend correctly implements the BRD specification**, but the **backend has NOT implemented the required `/api/grammar/practice/{session_id}/next` endpoint**. This is a **backend implementation gap**, not a frontend bug.

---

## Root Cause Analysis

### Evidence 1: BRD Specification (Line 2427)

The Business Requirements Document explicitly specifies:

```
*Practice Session:*
- API: `POST /api/grammar/practice/start` → `GET /api/grammar/practice/{session_id}/next`
```

**Source:** `/brd and planning documents/german_learning_app_brd.md`, line 2427

### Evidence 2: BRD Frontend Service Example (Lines 2229-2231)

The BRD provides example code for the frontend service:

```typescript
async getNextExercise(sessionId: number): Promise<GrammarExercise> {
  const response = await this.axios.get(`/grammar/practice/${sessionId}/next`);
  return response.data;
}
```

**Source:** `/brd and planning documents/german_learning_app_brd.md`, lines 2229-2231

### Evidence 3: Frontend Implementation Matches BRD

The frontend correctly implements the BRD specification:

**File:** `/frontend/src/api/services/grammarService.ts`, lines 70-75
```typescript
async getNextExercise(sessionId: number): Promise<GrammarExercise> {
  const response = await apiClient.get<GrammarExercise>(
    `/api/grammar/practice/${sessionId}/next`
  );
  return response.data;
}
```

### Evidence 4: Backend Missing Endpoint

**File:** `/backend/app/api/v1/grammar.py`

The backend grammar API has:
- ✅ `POST /api/grammar/practice/start` (line 123)
- ❌ `GET /api/grammar/practice/{session_id}/next` - **NOT IMPLEMENTED**
- ✅ `POST /api/grammar/practice/{session_id}/answer` (line 233)
- ✅ `POST /api/grammar/practice/{session_id}/end` (line 381)

**Backend Comment (lines 215-216):**
```python
# For now, we'll just return the session info and client will fetch exercises
```

This comment suggests the `/next` endpoint was planned but never implemented.

### Evidence 5: Direct API Test

```bash
# Session starts successfully
curl -X POST "http://192.168.178.100:8000/api/grammar/practice/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"topic_ids":[1],"exercise_count":5}'

# Response: {"session_id":111,"total_exercises":5,...} ✅

# Get next exercise - FAILS
curl "http://192.168.178.100:8000/api/grammar/practice/111/next" \
  -H "Authorization: Bearer $TOKEN"

# Response: {"detail":"Not Found"} ❌ (404)
```

---

## Expected vs Actual Behavior

### Expected User Flow (per BRD and Exercise Cycle Review)

```
1. User clicks "Practice This Topic"
2. Frontend: POST /api/grammar/practice/start
3. Backend returns: session_id, total_exercises
4. Frontend: GET /api/grammar/practice/{session_id}/next
5. Backend returns: first exercise
6. User answers exercise
7. Frontend: POST /api/grammar/practice/{session_id}/answer
8. Repeat steps 4-7 until session complete
9. Frontend: POST /api/grammar/practice/{session_id}/end
```

### Actual Behavior

```
1. User clicks "Practice This Topic"
2. Frontend: POST /api/grammar/practice/start ✅
3. Backend returns: session_id, total_exercises ✅
4. Frontend: GET /api/grammar/practice/{session_id}/next ❌
5. Backend returns: 404 Not Found ❌
6. Frontend shows error/blank screen
```

---

## Impact Analysis

| Aspect | Impact |
|--------|--------|
| **User Impact** | Users cannot practice grammar exercises - core learning feature is broken |
| **Feature Impact** | 90% of Grammar Practice Session tests fail (26/29) |
| **Business Impact** | Critical - grammar practice is a core feature per BRD Section 4.1 |
| **Timeline Impact** | Blocks frontend testing of entire Grammar Practice module |

---

## Verification: Frontend Expectations are Correct

### BRD Specification Check

| BRD Requirement | Frontend Implementation | Match |
|-----------------|------------------------|-------|
| `POST /api/grammar/practice/start` | grammarService.startPracticeSession() | ✅ |
| `GET /api/grammar/practice/{session_id}/next` | grammarService.getNextExercise() | ✅ |
| `POST /api/grammar/practice/{session_id}/answer` | grammarService.submitAnswer() | ✅ |
| `POST /api/grammar/practice/{session_id}/end` | grammarService.endSession() | ✅ |

### Exercise Cycle Review Check

The `/brd and planning documents/EXERCISE_CYCLE_REVIEW.md` document (lines 38-47) describes the expected flow:

```
│ 4. Practice Session Loop (repeat 10-20 times)               │
│    ┌──────────────────────────────────────────┐            │
│    │ a. Display Exercise (1 of 5 types)       │            │
│    │ b. User inputs answer                    │            │
│    │ c. User clicks "Submit Answer"           │            │
│    │ d. API call to check answer              │            │
│    │ e. Display feedback (correct/incorrect)  │            │
│    │ f. Show explanation + examples           │            │
│    │ g. User clicks "Next Exercise"           │            │
│    └──────────────────────────────────────────┘            │
```

This requires:
1. ✅ A way to GET exercises (the `/next` endpoint)
2. ✅ A way to submit answers (the `/answer` endpoint)

**Conclusion:** Frontend implementation correctly follows BRD specifications.

---

## Recommendations for Backend Team

### Option 1: Implement the Missing `/next` Endpoint (Recommended)

Add `GET /api/grammar/practice/{session_id}/next` endpoint to `/backend/app/api/v1/grammar.py`:

**Expected Response Schema:**
```json
{
  "exercise_id": 123,
  "exercise_type": "fill_blank",
  "difficulty": "B2",
  "question": "Der Kunde ___ (haben) die Rechnung bereits bezahlt.",
  "options": null,
  "hint": "Think about Perfekt tense with haben",
  "topic_id": 1,
  "topic_name": "Perfekt"
}
```

**Implementation Approach:**
1. Check if session exists and belongs to user
2. Get next unanswered exercise for the session
3. Return exercise data or indicate session complete

### Option 2: Return Exercises with Session Start

Modify `POST /api/grammar/practice/start` to return the first exercise inline with session data:

```json
{
  "session_id": 111,
  "total_exercises": 5,
  "current_exercise": {
    "exercise_id": 123,
    "exercise_type": "fill_blank",
    ...
  }
}
```

This would require frontend changes.

### Option 3: Return All Exercises at Once

Return all exercises when session starts, let frontend manage progression locally.

**Note:** This changes the architecture from server-managed to client-managed exercise sequence, which may not align with spaced repetition goals.

---

## Files Affected

### Backend Files (Need Implementation)
- `/backend/app/api/v1/grammar.py` - Add `/next` endpoint

### Frontend Files (Correctly Implemented per BRD)
- `/frontend/src/api/services/grammarService.ts` - getNextExercise() method
- `/frontend/src/pages/grammar/PracticeSessionPage.tsx` - loadNextExercise() call

---

## Test Impact

| Test Suite | Total | Pass | Fail | Blocked by BUG-006 |
|------------|-------|------|------|-------------------|
| Grammar Practice | 29 | 3 | 26 | 26 (90%) |

**Blocked Tests:**
- Exercise type badge display
- Difficulty badge display
- Exercise question rendering
- Fill-blank exercise interaction
- Multiple choice exercise interaction
- Hint display
- Answer submission
- Loading state during submit
- Empty submission validation
- Feedback display
- Correct/incorrect indicators
- Continue button functionality
- Progress header
- End session button
- Keyboard shortcut tests
- Completion screen
- Session navigation
- Streak counter
- Mobile/tablet layouts

---

## Related Documentation

- **BRD:** `/brd and planning documents/german_learning_app_brd.md`
- **Exercise Cycle Review:** `/brd and planning documents/EXERCISE_CYCLE_REVIEW.md`
- **CLAUDE.md:** Phase 6 Complete notes mention 14 grammar endpoints, but `/next` is missing

---

## Related Bugs

- BUG-007: Loading state detection timing issue (secondary symptom of this bug)

---

## Conclusion

**The frontend implementation is CORRECT according to the BRD specification.**

The root cause is a **backend implementation gap** - the `GET /api/grammar/practice/{session_id}/next` endpoint was specified in the BRD but never implemented. The backend comment "For now, we'll just return the session info and client will fetch exercises" confirms this was intentional deferral that was never completed.

**Recommended Action:** Backend team should implement the missing `/next` endpoint to match the BRD specification.

---

## Appendix: API Specification (per BRD)

### GET /api/grammar/practice/{session_id}/next

**Purpose:** Return the next exercise for the current practice session

**Request:**
- Method: GET
- Path: `/api/grammar/practice/{session_id}/next`
- Headers: `Authorization: Bearer {token}`

**Response (200 OK):**
```json
{
  "exercise_id": 123,
  "exercise_type": "fill_blank" | "multiple_choice" | "translation" | "error_correction" | "sentence_building",
  "difficulty": "A1" | "A2" | "B1" | "B2" | "C1" | "C2",
  "question": "string",
  "options": ["string"] | null,
  "hint": "string" | null,
  "topic_id": 1,
  "topic_name": "string"
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Session not found or session complete"
}
```
