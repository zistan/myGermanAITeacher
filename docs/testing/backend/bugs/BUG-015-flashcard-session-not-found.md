# BUG-015: Flashcard Session Not Found After Creation

**Severity:** High
**Category:** Vocabulary / Flashcards
**Reported:** 2026-01-19
**Reporter:** Backend Test Engineer
**Status:** Open

## Description
After successfully creating a flashcard session via POST `/api/v1/vocabulary/flashcards/start`, attempting to retrieve the current flashcard with GET `/api/v1/vocabulary/flashcards/{session_id}/current` returns a 404 "Session not found" error. This indicates that either:
1. The session is not being persisted to the database
2. The session_id returned doesn't match what's stored
3. The GET endpoint is looking in the wrong place

## API Endpoint
**Method:** GET
**URL:** http://192.168.178.100:8000/api/v1/vocabulary/flashcards/{session_id}/current
**Authentication:** Required (JWT Bearer token)

## Steps to Reproduce
1. Authenticate as a valid user
2. Create a flashcard session:
   ```bash
   POST /api/v1/vocabulary/flashcards/start
   {
     "mode": "spaced_repetition",
     "max_cards": 10
   }
   ```
3. Note the returned `session_id` (e.g., 1)
4. Immediately attempt to get current flashcard:
   ```bash
   GET /api/v1/vocabulary/flashcards/1/current
   ```
5. Observe 404 error

## Request Details

**Step 1: Create Session (SUCCEEDS)**
```bash
curl -X POST http://192.168.178.100:8000/api/v1/vocabulary/flashcards/start \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "spaced_repetition",
    "max_cards": 10
  }'
```

**Step 2: Get Current Card (FAILS)**
```bash
curl -X GET http://192.168.178.100:8000/api/v1/vocabulary/flashcards/1/current \
  -H "Authorization: Bearer <JWT_TOKEN>"
```

## Expected Result
**Status Code:** 200
**Response Body:**
```json
{
  "session_id": 1,
  "total_cards": 10,
  "current_card_number": 1,
  "current_card": {
    "word_id": 1,
    "word": "die Arbeit",
    "card_type": "definition",
    ...
  }
}
```

## Actual Result
**Status Code:** 404
**Response Body:**
```json
{
  "detail": "Session not found"
}
```

## Database State
Check if session was created:
```sql
-- Check flashcard_sessions table (or similar)
SELECT * FROM flashcard_sessions WHERE id = 1;

-- Check if there's a vocabulary_sessions table
SELECT * FROM vocabulary_sessions WHERE id = 1;

-- Check all sessions for the user
SELECT * FROM flashcard_sessions WHERE user_id = [USER_ID] ORDER BY created_at DESC LIMIT 5;
```

## Impact Analysis
- **Users Affected:** All users attempting to use flashcard feature
- **Workaround Available:** No - flashcard feature is broken
- **Data Integrity:** Unknown - session may not be persisted

## Possible Root Cause
1. **Database commit issue** - Session not committed to database after creation
2. **Table mismatch** - POST creates in one table, GET reads from another
3. **Session ID mismatch** - Different ID format expected (string vs int)
4. **User ID filter** - GET endpoint may be filtering by wrong user_id
5. **Missing database table** - Flashcard session table may not exist

## Related Code
**Create Session:**
- **File:** `/backend/app/api/v1/vocabulary.py`
- **Endpoint:** `POST /api/v1/vocabulary/flashcards/start`

**Get Current Card:**
- **File:** `/backend/app/api/v1/vocabulary.py`
- **Endpoint:** `GET /api/v1/vocabulary/flashcards/{session_id}/current`

**Database Models:**
- **File:** `/backend/app/models/vocabulary.py`
- **Expected Model:** `FlashcardSession` or similar

## Suggested Investigation Steps
1. Check server logs for both POST and GET requests
2. Verify database tables exist for flashcard sessions
3. Check if session is committed to database after creation
4. Verify session_id type consistency (int vs string)
5. Check if GET endpoint queries the correct table with correct filters
6. Verify user_id is correctly associated with session

## Test Output
```
================================================================================
TEST REPORT: Start Flashcard Session
================================================================================
[PASS] Test 1: Start flashcard session with spaced repetition - PASSED
   Expected: 200
   Actual: 200
   Response keys: ['session_id', 'total_cards', 'current_card_number', 'current_card']

DATABASE STATE:
- Created flashcard session ID: 1

================================================================================
TEST REPORT: Get Current Flashcard
================================================================================
[FAIL] Test 1: Get current flashcard - FAILED
   Expected: 200
   Actual: 404
   Error response: {
      "detail": "Session not found"
   }
```

## Related Bugs
- BUG-016 (Quiz not found after generation) - Similar pattern

## Additional Context
The POST endpoint returns 200 and includes session_id in response, suggesting creation appears successful. However, the immediate GET request fails to find the session, indicating a persistence or query issue.
