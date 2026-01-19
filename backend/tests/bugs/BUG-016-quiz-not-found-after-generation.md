# BUG-016: Quiz Not Found After Generation

**Severity:** High
**Category:** Vocabulary / Quiz
**Reported:** 2026-01-19
**Reporter:** Backend Test Engineer
**Status:** Open

## Description
After successfully generating a vocabulary quiz via POST `/api/v1/vocabulary/quiz/generate`, attempting to submit an answer with POST `/api/v1/vocabulary/quiz/{quiz_id}/answer` returns a 404 "Quiz not found" error. This is similar to BUG-015 (Flashcard Session Not Found) and indicates a pattern of session/quiz persistence issues in the vocabulary module.

## API Endpoint
**Method:** POST
**URL:** http://192.168.178.100:8000/api/v1/vocabulary/quiz/{quiz_id}/answer
**Authentication:** Required (JWT Bearer token)

## Steps to Reproduce
1. Authenticate as a valid user
2. Generate a vocabulary quiz:
   ```bash
   POST /api/v1/vocabulary/quiz/generate
   {
     "word_ids": [1, 2, 3],
     "quiz_type": "multiple_choice",
     "num_questions": 5
   }
   ```
3. Note the returned `quiz_id` from response
4. Attempt to submit an answer to first question:
   ```bash
   POST /api/v1/vocabulary/quiz/{quiz_id}/answer
   {
     "question_number": 0,
     "answer": "option_a"
   }
   ```
5. Observe 404 error

## Request Details

**Step 1: Generate Quiz (SUCCEEDS)**
```bash
curl -X POST http://192.168.178.100:8000/api/v1/vocabulary/quiz/generate \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "word_ids": [1, 2, 3, 4, 5],
    "quiz_type": "multiple_choice",
    "num_questions": 5
  }'
```

**Response:**
```json
{
  "quiz_id": "some-quiz-id",
  "questions": [...],
  "total_questions": 5,
  "estimated_duration_minutes": 5
}
```

**Step 2: Submit Answer (FAILS)**
```bash
curl -X POST http://192.168.178.100:8000/api/v1/vocabulary/quiz/{quiz_id}/answer \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "question_number": 0,
    "answer": "option_a"
  }'
```

## Expected Result
**Status Code:** 200
**Response Body:**
```json
{
  "is_correct": true,
  "correct_answer": "option_a",
  "explanation": "...",
  "points_earned": 10,
  "progress": {
    "answered": 1,
    "total": 5,
    "score": 10
  }
}
```

## Actual Result
**Status Code:** 404
**Response Body:**
```json
{
  "detail": "Quiz not found"
}
```

## Database State
Check if quiz was created:
```sql
-- Check vocabulary_quizzes table (or similar)
SELECT * FROM vocabulary_quizzes ORDER BY created_at DESC LIMIT 5;

-- Check quiz sessions
SELECT * FROM quiz_sessions WHERE user_id = [USER_ID] ORDER BY created_at DESC LIMIT 5;

-- Check all quiz-related tables
\dt *quiz*
```

## Impact Analysis
- **Users Affected:** All users attempting to use vocabulary quiz feature
- **Workaround Available:** No - quiz feature is broken
- **Data Integrity:** Unknown - quiz may not be persisted or stored only in memory

## Possible Root Cause
1. **In-memory storage** - Quiz stored in memory/cache, not database (lost between requests)
2. **Database commit issue** - Quiz not committed to database after generation
3. **Quiz ID mismatch** - ID format inconsistency (UUID string vs integer)
4. **Session management** - Quiz tied to session that expires immediately
5. **Missing database table** - Quiz persistence table may not exist
6. **Temporary storage** - Quiz stored with short TTL that expires before answer submission

## Related Code
**Generate Quiz:**
- **File:** `/backend/app/api/v1/vocabulary.py`
- **Endpoint:** `POST /api/v1/vocabulary/quiz/generate`
- **Service:** `/backend/app/services/vocabulary_ai_service.py`

**Submit Answer:**
- **File:** `/backend/app/api/v1/vocabulary.py`
- **Endpoint:** `POST /api/v1/vocabulary/quiz/{quiz_id}/answer`

**Database Models:**
- **File:** `/backend/app/models/vocabulary.py`
- **Expected Model:** `VocabularyQuiz` or `QuizSession`

## Suggested Investigation Steps
1. Check if quiz persistence is implemented or only in-memory
2. Verify quiz_id returned from generation matches what's expected by answer endpoint
3. Check server logs for both generate and answer requests
4. Verify database tables exist for quiz storage
5. Check if quiz is committed to database after generation
6. Test if adding a delay between generate and answer changes behavior
7. Verify VocabularyAIService quiz generation includes persistence

## Test Output
```
================================================================================
TEST REPORT: Generate Vocabulary Quiz
================================================================================
[PASS] Test 1: Generate multiple choice quiz - PASSED
   Expected: 200
   Actual: 200
   Response keys: ['quiz_id', 'questions', 'total_questions', 'estimated_duration_minutes']

================================================================================
TEST REPORT: Submit Quiz Answer
================================================================================
[FAIL] Test 1: Submit quiz answer - FAILED
   Expected: 200
   Actual: 404
   Error response: {
      "detail": "Quiz not found"
   }
```

## Related Bugs
- **BUG-015**: Flashcard Session Not Found - Same pattern in vocabulary module
- Suggests systemic issue with vocabulary module session/state persistence

## Additional Context
The quiz generation endpoint returns 200 with quiz_id, questions, and metadata, suggesting successful generation. However, the quiz cannot be found immediately afterward when attempting to submit an answer. This points to either:
- Quiz not being persisted to database
- In-memory storage that's not shared across requests
- Quiz ID format mismatch between generation and retrieval

This is the second vocabulary feature with this pattern (after flashcards), suggesting a common root cause in how vocabulary sessions/quizzes are stored and retrieved.
