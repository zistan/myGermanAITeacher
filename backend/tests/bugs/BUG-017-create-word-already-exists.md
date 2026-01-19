# BUG-017: Create Custom Word Fails with "Word already exists"

**Severity:** Medium
**Category:** Vocabulary / Word Management
**Reported:** 2026-01-19
**Reporter:** Backend Test Engineer
**Status:** Open

## Description
The POST `/api/v1/vocabulary/words` endpoint returns a 400 "Word already exists" error when attempting to create a custom vocabulary word. This test failure could indicate:
1. Environmental issue - Word from previous test run still exists
2. Test data issue - Using a common word that's already in seed data
3. Business logic issue - Overly strict duplicate detection

## API Endpoint
**Method:** POST
**URL:** http://192.168.178.100:8000/api/v1/vocabulary/words
**Authentication:** Required (JWT Bearer token)

## Steps to Reproduce
1. Authenticate as a valid user
2. Attempt to create a custom vocabulary word:
   ```bash
   POST /api/v1/vocabulary/words
   {
     "word": "TestWort",
     "translation_it": "parola di prova",
     "difficulty": "B2",
     "category": "general"
   }
   ```
3. Observe 400 error "Word already exists"

## Request Details
```bash
curl -X POST http://192.168.178.100:8000/api/v1/vocabulary/words \
  -H "Authorization: Bearer <JWT_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "word": "TestWort",
    "translation_it": "parola di prova",
    "part_of_speech": "noun",
    "difficulty": "B2",
    "category": "general",
    "definition_de": "Ein Testwort für Demonstrationszwecke"
  }'
```

**Request Headers:**
```
Authorization: Bearer eyJ...
Content-Type: application/json
```

**Request Body:**
```json
{
  "word": "TestWort",
  "translation_it": "parola di prova",
  "part_of_speech": "noun",
  "difficulty": "B2",
  "category": "general",
  "definition_de": "Ein Testwort für Demonstrationszwecke"
}
```

## Expected Result
**Status Code:** 200 (or 201)
**Response Body:**
```json
{
  "id": 151,
  "word": "TestWort",
  "translation_it": "parola di prova",
  "part_of_speech": "noun",
  "difficulty": "B2",
  "category": "general",
  "definition_de": "Ein Testwort für Demonstrationszwecke",
  "created_at": "2026-01-19T...",
  "user_id": 1
}
```

## Actual Result
**Status Code:** 400
**Response Body:**
```json
{
  "detail": "Word already exists"
}
```

## Database State
Check if word exists:
```sql
-- Check for exact word match
SELECT * FROM vocabulary_words WHERE word = 'TestWort';

-- Check for case-insensitive match
SELECT * FROM vocabulary_words WHERE LOWER(word) = LOWER('TestWort');

-- Check all custom words created by test user
SELECT * FROM vocabulary_words WHERE user_id = [TEST_USER_ID];

-- Check if there's a unique constraint
\d vocabulary_words
```

## Impact Analysis
- **Users Affected:** Users attempting to create custom vocabulary words
- **Workaround Available:** Possibly - use a different word if it's truly a duplicate
- **Data Integrity:** Safe - prevents duplicate words (may be intended behavior)
- **Severity Justification:** Medium - May be environmental issue or by-design validation

## Possible Root Cause
1. **Environmental contamination** - Word exists from previous test run
2. **Insufficient uniqueness** - Need to use timestamp/UUID in test word
3. **Case-insensitive duplicate check** - "TestWort" matches existing "testwort"
4. **By-design validation** - System prevents duplicate words globally
5. **Test cleanup issue** - Previous test didn't clean up created words

## Related Code
**File:** `/backend/app/api/v1/vocabulary.py`
**Endpoint:** `POST /api/v1/vocabulary/words`
**Function:** `create_word()`

**File:** `/backend/app/models/vocabulary.py`
**Model:** `Vocabulary`

## Suggested Investigation Steps
1. Query database to check if "TestWort" already exists
2. Check if duplicate validation is case-sensitive or case-insensitive
3. Determine if validation checks global duplicates or per-user duplicates
4. Review business requirements - should users be able to create words that already exist?
5. If environmental issue, clean up test data and retry
6. If by-design, update test to use guaranteed unique word (with timestamp)

## Test Improvement Suggestions
If this is environmental contamination, the test should be updated to:
```python
# Generate unique test word using timestamp
import time
timestamp = int(time.time())
test_word = f"TestWort{timestamp}"

# Create word with unique identifier
create_word_response = make_request(
    "POST",
    "/api/v1/vocabulary/words",
    json_data={
        "word": test_word,
        "translation_it": "parola di prova",
        ...
    }
)
```

Alternatively, add teardown to delete created test words:
```python
# At end of test
if created_word_id:
    delete_test_word(created_word_id)
```

## Test Output
```
================================================================================
TEST REPORT: Create Custom Word
================================================================================
[FAIL] Test 1: Create custom vocabulary word - FAILED
   Expected: 200
   Actual: 400
   Error response: {
      "detail": "Word already exists"
   }
```

## Related Bugs
None

## Additional Context
This could be expected behavior if the system enforces global word uniqueness to prevent duplicate entries in the vocabulary database. However, it could also be:
- A test isolation issue where previous runs contaminated the database
- A case-sensitivity issue in duplicate detection
- A user-scoping issue (should users be able to add their own version of existing words?)

**Priority:** This should be investigated to determine if it's a:
1. **Bug** - Word shouldn't be marked as duplicate
2. **Test Issue** - Test needs better cleanup or unique word generation
3. **Expected Behavior** - Test expectations need to be updated
