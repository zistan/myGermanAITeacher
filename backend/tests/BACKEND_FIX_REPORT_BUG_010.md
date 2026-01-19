# Backend Fix Report: BUG-010 Session Progress Schema Mismatch

**Date:** 2026-01-19
**Priority:** 🔴 **CRITICAL**
**Issue:** API contract violation - Backend returns incorrect field names
**Impact:** Grammar Practice completely broken after first answer submission
**Reporter:** Frontend E2E Test Engineer

---

## Executive Summary

**Problem:** The `POST /api/grammar/practice/{session_id}/answer` endpoint returns a `session_progress` object with field names that don't match the frontend's expectations, causing the application to crash with a blank page.

**Root Cause:** Backend uses snake_case field names (`completed`, `correct`, `accuracy`) while frontend expects different names (`exercises_completed`, `exercises_correct`, `accuracy_percentage`) plus additional fields (`current_streak`, `total_points`).

**Solution:** Update backend to return correct field names and missing fields.

**Severity:** CRITICAL - Users cannot complete grammar exercises.

---

## Current Backend Response (INCORRECT)

**File:** `/backend/app/api/v1/grammar.py`
**Lines:** 437-443

```python
session_progress = {
    "completed": total_attempted,
    "total": session.total_exercises,
    "correct": session.exercises_correct,
    "accuracy": (session.exercises_correct / total_attempted * 100)
        if total_attempted > 0 else 0
}
```

**Actual Response Example:**
```json
{
  "feedback": {...},
  "session_progress": {
    "completed": 1,
    "total": 5,
    "correct": 1,
    "accuracy": 100.0
  },
  "next_exercise": null
}
```

---

## Required Backend Response (CORRECT)

**Frontend Expects:**
```json
{
  "feedback": {...},
  "session_progress": {
    "exercises_completed": 1,
    "exercises_correct": 1,
    "current_streak": 1,
    "total_points": 2,
    "accuracy_percentage": 100.0
  },
  "next_exercise": null
}
```

**Field Mapping:**

| Current Backend | Required Frontend | Description |
|----------------|-------------------|-------------|
| `completed` | `exercises_completed` | Number of exercises attempted |
| `correct` | `exercises_correct` | Number of correct answers |
| `accuracy` | `accuracy_percentage` | Percentage accuracy (0-100) |
| (missing) | `current_streak` | Current streak of correct answers |
| (missing) | `total_points` | Total points earned in session |
| `total` | (remove) | Not needed by frontend |

---

## Required Backend Changes

### Change 1: Update session_progress in POST /answer endpoint

**File:** `/backend/app/api/v1/grammar.py`
**Function:** `submit_exercise_answer`
**Lines to modify:** 437-443

**Current Code:**
```python
# Session progress
total_attempted = session.exercises_correct + session.exercises_incorrect
session_progress = {
    "completed": total_attempted,
    "total": session.total_exercises,
    "correct": session.exercises_correct,
    "accuracy": (session.exercises_correct / total_attempted * 100)
        if total_attempted > 0 else 0
}
```

**Replace with:**
```python
# Session progress (API contract with frontend)
total_attempted = session.exercises_correct + session.exercises_incorrect

# Calculate current streak from recent attempts
# Get last 10 attempts for this session, ordered by timestamp
recent_attempts = db.query(GrammarExerciseAttempt).filter(
    GrammarExerciseAttempt.grammar_session_id == session_id
).order_by(GrammarExerciseAttempt.timestamp.desc()).limit(10).all()

current_streak = 0
for attempt in reversed(recent_attempts):
    if attempt.is_correct:
        current_streak += 1
    else:
        break

# Calculate total points (sum points from all attempts)
# Points are awarded based on difficulty: A1/A2=1, B1/B2=2, C1/C2=3
total_points = 0
all_attempts = db.query(GrammarExerciseAttempt).join(
    GrammarExercise,
    GrammarExercise.id == GrammarExerciseAttempt.exercise_id
).filter(
    GrammarExerciseAttempt.grammar_session_id == session_id
).all()

for attempt in all_attempts:
    if attempt.is_correct:
        exercise = db.query(GrammarExercise).filter(
            GrammarExercise.id == attempt.exercise_id
        ).first()
        if exercise:
            difficulty_points = {"A1": 1, "A2": 1, "B1": 2, "B2": 2, "C1": 3, "C2": 3}
            total_points += difficulty_points.get(exercise.difficulty_level, 1)

session_progress = {
    "exercises_completed": total_attempted,
    "exercises_correct": session.exercises_correct,
    "current_streak": current_streak,
    "total_points": total_points,
    "accuracy_percentage": (session.exercises_correct / total_attempted * 100)
        if total_attempted > 0 else 0
}
```

### Change 2: Update GrammarSession Model (Optional Optimization)

**File:** `/backend/app/models/grammar.py`
**Model:** `GrammarSession`

**Consider adding fields to track points and streak:**
```python
class GrammarSession(Base):
    # ... existing fields ...

    total_points = Column(Integer, default=0, nullable=False)
    current_streak = Column(Integer, default=0, nullable=False)
```

This would eliminate the need to query attempts every time, but requires a database migration.

**For immediate fix:** Use the query-based approach above (no migration needed).

---

## Alternative: Simpler Fix (Recommended for Quick Deploy)

If calculating streak/points is too complex for immediate deployment, use placeholder values:

```python
session_progress = {
    "exercises_completed": total_attempted,
    "exercises_correct": session.exercises_correct,
    "current_streak": session.exercises_correct if total_attempted == session.exercises_correct else 0,  # Simple: correct = streak
    "total_points": session.exercises_correct * 2,  # Simple: 2 points per correct answer
    "accuracy_percentage": (session.exercises_correct / total_attempted * 100)
        if total_attempted > 0 else 0
}
```

**Later enhancement:** Implement proper streak and points calculation with model changes.

---

## Backend Test Cases to Add

### Test File: `/backend/tests/test_grammar.py`

Add these test cases to `TestGrammarPracticeEndpoints` class:

### Test 1: Verify session_progress schema after answer submission

```python
@patch('app.api.v1.grammar.GrammarAIService')
def test_submit_answer_session_progress_schema(
    self,
    mock_ai_service,
    client,
    auth_headers,
    db_session,
    test_user,
    test_grammar_exercises
):
    """Test that session_progress has correct field names (BUG-010 regression test)."""
    from app.models.grammar import GrammarSession

    # Create session
    session = GrammarSession(
        user_id=test_user.id,
        session_type="practice",
        total_exercises=3,
        grammar_metadata={
            "target_level": "A2",
            "exercise_ids": [ex.id for ex in test_grammar_exercises[:3]]
        }
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Mock AI evaluation
    mock_ai_instance = MagicMock()
    mock_ai_instance.evaluate_answer.return_value = {
        "is_correct": True,
        "is_partially_correct": False,
        "feedback_de": "Richtig!",
        "specific_errors": [],
        "suggestions": []
    }
    mock_ai_service.return_value = mock_ai_instance

    # Submit answer
    response = client.post(
        f"/api/grammar/practice/{session.id}/answer",
        json={
            "exercise_id": test_grammar_exercises[0].id,
            "user_answer": "den",
            "time_spent_seconds": 30
        },
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Verify session_progress has correct fields (BUG-010)
    assert "session_progress" in data
    progress = data["session_progress"]

    # Required fields with correct names
    assert "exercises_completed" in progress, "Missing 'exercises_completed' field"
    assert "exercises_correct" in progress, "Missing 'exercises_correct' field"
    assert "current_streak" in progress, "Missing 'current_streak' field"
    assert "total_points" in progress, "Missing 'total_points' field"
    assert "accuracy_percentage" in progress, "Missing 'accuracy_percentage' field"

    # Old incorrect field names should NOT be present
    assert "completed" not in progress, "Old 'completed' field still present"
    assert "correct" not in progress, "Old 'correct' field still present"
    assert "accuracy" not in progress, "Old 'accuracy' field still present"

    # Verify field types
    assert isinstance(progress["exercises_completed"], int)
    assert isinstance(progress["exercises_correct"], int)
    assert isinstance(progress["current_streak"], int)
    assert isinstance(progress["total_points"], int)
    assert isinstance(progress["accuracy_percentage"], (int, float))

    # Verify values are reasonable
    assert progress["exercises_completed"] == 1
    assert progress["exercises_correct"] == 1
    assert progress["current_streak"] >= 0
    assert progress["total_points"] >= 0
    assert 0 <= progress["accuracy_percentage"] <= 100
```

### Test 2: Verify streak calculation

```python
@patch('app.api.v1.grammar.GrammarAIService')
def test_session_progress_streak_calculation(
    self,
    mock_ai_service,
    client,
    auth_headers,
    db_session,
    test_user,
    test_grammar_exercises
):
    """Test that current_streak is calculated correctly."""
    from app.models.grammar import GrammarSession

    # Create session
    session = GrammarSession(
        user_id=test_user.id,
        session_type="practice",
        total_exercises=5,
        grammar_metadata={
            "target_level": "A2",
            "exercise_ids": [ex.id for ex in test_grammar_exercises[:5]]
        }
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Mock AI to return correct answers
    mock_ai_instance = MagicMock()
    mock_ai_instance.evaluate_answer.return_value = {
        "is_correct": True,
        "is_partially_correct": False,
        "feedback_de": "Richtig!",
        "specific_errors": [],
        "suggestions": []
    }
    mock_ai_service.return_value = mock_ai_instance

    # Submit 3 correct answers
    for i in range(3):
        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": test_grammar_exercises[i].id,
                "user_answer": "correct",
                "time_spent_seconds": 30
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    # Check streak after 3 correct answers
    data = response.json()
    assert data["session_progress"]["current_streak"] == 3

    # Now submit an incorrect answer
    mock_ai_instance.evaluate_answer.return_value = {
        "is_correct": False,
        "is_partially_correct": False,
        "feedback_de": "Falsch.",
        "specific_errors": [],
        "suggestions": []
    }

    response = client.post(
        f"/api/grammar/practice/{session.id}/answer",
        json={
            "exercise_id": test_grammar_exercises[3].id,
            "user_answer": "wrong",
            "time_spent_seconds": 30
        },
        headers=auth_headers
    )

    # Streak should reset to 0
    data = response.json()
    assert data["session_progress"]["current_streak"] == 0
```

### Test 3: Verify points calculation

```python
@patch('app.api.v1.grammar.GrammarAIService')
def test_session_progress_points_calculation(
    self,
    mock_ai_service,
    client,
    auth_headers,
    db_session,
    test_user,
    test_grammar_exercises
):
    """Test that total_points increases with correct answers."""
    from app.models.grammar import GrammarSession

    # Create session
    session = GrammarSession(
        user_id=test_user.id,
        session_type="practice",
        total_exercises=3,
        grammar_metadata={
            "target_level": "A2",
            "exercise_ids": [ex.id for ex in test_grammar_exercises[:3]]
        }
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Mock AI to return correct answer
    mock_ai_instance = MagicMock()
    mock_ai_instance.evaluate_answer.return_value = {
        "is_correct": True,
        "is_partially_correct": False,
        "feedback_de": "Richtig!",
        "specific_errors": [],
        "suggestions": []
    }
    mock_ai_service.return_value = mock_ai_instance

    # Submit first correct answer
    response = client.post(
        f"/api/grammar/practice/{session.id}/answer",
        json={
            "exercise_id": test_grammar_exercises[0].id,
            "user_answer": "den",
            "time_spent_seconds": 30
        },
        headers=auth_headers
    )

    data = response.json()
    points_after_first = data["session_progress"]["total_points"]
    assert points_after_first > 0, "Points should be positive after correct answer"

    # Submit second correct answer
    response = client.post(
        f"/api/grammar/practice/{session.id}/answer",
        json={
            "exercise_id": test_grammar_exercises[1].id,
            "user_answer": "einen Stift",
            "time_spent_seconds": 30
        },
        headers=auth_headers
    )

    data = response.json()
    points_after_second = data["session_progress"]["total_points"]
    assert points_after_second > points_after_first, "Points should increase after second correct answer"
```

### Test 4: Verify accuracy_percentage field

```python
@patch('app.api.v1.grammar.GrammarAIService')
def test_session_progress_accuracy_percentage(
    self,
    mock_ai_service,
    client,
    auth_headers,
    db_session,
    test_user,
    test_grammar_exercises
):
    """Test that accuracy_percentage is calculated correctly."""
    from app.models.grammar import GrammarSession

    # Create session
    session = GrammarSession(
        user_id=test_user.id,
        session_type="practice",
        total_exercises=4,
        grammar_metadata={
            "target_level": "A2",
            "exercise_ids": [ex.id for ex in test_grammar_exercises[:4]]
        }
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Mock AI to alternate correct/incorrect
    mock_ai_instance = MagicMock()
    mock_ai_service.return_value = mock_ai_instance

    # Submit 2 correct, 2 incorrect (50% accuracy)
    correct_responses = [True, False, True, False]

    for i, is_correct in enumerate(correct_responses):
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": is_correct,
            "is_partially_correct": False,
            "feedback_de": "Feedback",
            "specific_errors": [],
            "suggestions": []
        }

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": test_grammar_exercises[i].id,
                "user_answer": "answer",
                "time_spent_seconds": 30
            },
            headers=auth_headers
        )
        assert response.status_code == status.HTTP_200_OK

    # Final accuracy should be 50%
    data = response.json()
    accuracy = data["session_progress"]["accuracy_percentage"]
    assert 49 <= accuracy <= 51, f"Expected ~50% accuracy, got {accuracy}%"
```

### Test 5: Verify zero accuracy edge case

```python
@patch('app.api.v1.grammar.GrammarAIService')
def test_session_progress_zero_accuracy(
    self,
    mock_ai_service,
    client,
    auth_headers,
    db_session,
    test_user,
    test_grammar_exercises
):
    """Test that accuracy_percentage handles 0% correctly (BUG-010 edge case)."""
    from app.models.grammar import GrammarSession

    # Create session
    session = GrammarSession(
        user_id=test_user.id,
        session_type="practice",
        total_exercises=2,
        grammar_metadata={
            "target_level": "A2",
            "exercise_ids": [ex.id for ex in test_grammar_exercises[:2]]
        }
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)

    # Mock AI to return incorrect answer
    mock_ai_instance = MagicMock()
    mock_ai_instance.evaluate_answer.return_value = {
        "is_correct": False,
        "is_partially_correct": False,
        "feedback_de": "Falsch.",
        "specific_errors": [],
        "suggestions": []
    }
    mock_ai_service.return_value = mock_ai_instance

    # Submit incorrect answer
    response = client.post(
        f"/api/grammar/practice/{session.id}/answer",
        json={
            "exercise_id": test_grammar_exercises[0].id,
            "user_answer": "wrong",
            "time_spent_seconds": 30
        },
        headers=auth_headers
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Verify 0% accuracy doesn't cause NaN or undefined
    accuracy = data["session_progress"]["accuracy_percentage"]
    assert accuracy == 0.0, f"Expected 0% accuracy, got {accuracy}%"
    assert data["session_progress"]["exercises_completed"] == 1
    assert data["session_progress"]["exercises_correct"] == 0
    assert data["session_progress"]["current_streak"] == 0
```

---

## Manual API Testing

After implementing the fix, verify with curl:

### Setup
```bash
# Login and get token
TOKEN=$(curl -X POST "http://192.168.178.100:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}' \
  -s | jq -r '.access_token')

# Start practice session
SESSION_RESPONSE=$(curl -X POST "http://192.168.178.100:8000/api/grammar/practice/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exercise_count": 3}' \
  -s)

SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')

# Get first exercise
EXERCISE=$(curl "http://192.168.178.100:8000/api/grammar/practice/$SESSION_ID/next" \
  -H "Authorization: Bearer $TOKEN" \
  -s)

EXERCISE_ID=$(echo $EXERCISE | jq -r '.id')
```

### Test Answer Submission
```bash
# Submit answer and check session_progress schema
curl -X POST "http://192.168.178.100:8000/api/grammar/practice/$SESSION_ID/answer" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"exercise_id\": $EXERCISE_ID,
    \"user_answer\": \"test\",
    \"time_spent_seconds\": 30
  }" \
  -s | jq '.session_progress'
```

### Expected Output (AFTER FIX)
```json
{
  "exercises_completed": 1,
  "exercises_correct": 1,
  "current_streak": 1,
  "total_points": 2,
  "accuracy_percentage": 100.0
}
```

### Current Output (BEFORE FIX - INCORRECT)
```json
{
  "completed": 1,
  "total": 3,
  "correct": 1,
  "accuracy": 100.0
}
```

---

## Verification Checklist

After implementing the fix:

### Backend Code Changes
- [ ] Updated `session_progress` dict in grammar.py (lines 437-443)
- [ ] Changed `completed` → `exercises_completed`
- [ ] Changed `correct` → `exercises_correct`
- [ ] Changed `accuracy` → `accuracy_percentage`
- [ ] Added `current_streak` field
- [ ] Added `total_points` field
- [ ] Removed `total` field

### Backend Tests
- [ ] Added Test 1: Schema validation test
- [ ] Added Test 2: Streak calculation test
- [ ] Added Test 3: Points calculation test
- [ ] Added Test 4: Accuracy percentage test
- [ ] Added Test 5: Zero accuracy edge case test
- [ ] All 5 new tests pass
- [ ] All existing grammar tests still pass

### Manual Testing
- [ ] POST /answer returns correct field names
- [ ] Frontend doesn't crash after answer submission
- [ ] SessionHeader displays accuracy without error
- [ ] Multiple answers update progress correctly
- [ ] Zero accuracy edge case works

### Integration Testing
- [ ] Run frontend E2E tests
- [ ] Grammar practice session completes successfully
- [ ] 5 new frontend regression tests pass

---

## Schema Documentation

### Update API Documentation

**File:** `/backend/app/schemas/grammar.py`
**Location:** Line 122-127 (SubmitExerciseAnswerResponse)

**Current:**
```python
class SubmitExerciseAnswerResponse(BaseModel):
    """Response after submitting an exercise answer."""
    feedback: ExerciseFeedback
    session_progress: dict = Field(..., description="Current session progress")
    next_exercise: Optional[GrammarExerciseResponse] = None
```

**Should add explicit schema:**
```python
class SessionProgress(BaseModel):
    """Session progress tracking."""
    exercises_completed: int = Field(..., description="Number of exercises attempted")
    exercises_correct: int = Field(..., description="Number of correct answers")
    current_streak: int = Field(..., description="Current streak of correct answers")
    total_points: int = Field(..., description="Total points earned in session")
    accuracy_percentage: float = Field(..., ge=0, le=100, description="Accuracy percentage (0-100)")

class SubmitExerciseAnswerResponse(BaseModel):
    """Response after submitting an exercise answer."""
    feedback: ExerciseFeedback
    session_progress: SessionProgress  # Changed from dict to SessionProgress
    next_exercise: Optional[GrammarExerciseResponse] = None
```

This provides:
- ✅ Type safety
- ✅ API documentation in Swagger UI
- ✅ Validation
- ✅ Clear contract

---

## Impact Assessment

### Before Fix
- ❌ Grammar Practice crashes after first answer
- ❌ Users cannot complete exercises
- ❌ Frontend tests fail (5 tests)
- ❌ Feature completely unusable

### After Fix
- ✅ Grammar Practice works end-to-end
- ✅ Users can complete full sessions
- ✅ Frontend tests pass
- ✅ Feature fully functional
- ✅ Proper API contract established

---

## Deployment Steps

1. **Implement Backend Fix**
   - Update grammar.py with correct field names
   - Add SessionProgress schema
   - Add 5 new test cases

2. **Run Backend Tests**
   ```bash
   pytest tests/test_grammar.py::TestGrammarPracticeEndpoints -v
   ```

3. **Deploy to Remote Server**
   ```bash
   cd /opt/german-learning-app
   git pull origin master
   sudo systemctl restart german-learning
   ```

4. **Manual Verification**
   - Use curl commands above
   - Verify correct field names in response

5. **Frontend Verification**
   - Run frontend E2E tests
   - Test Grammar Practice manually
   - Verify no crashes

---

## Priority and Timeline

**Priority:** 🔴 **CRITICAL P0**
**Estimated Fix Time:** 30-60 minutes
**Testing Time:** 30 minutes
**Total:** 1-1.5 hours

**Blocks:**
- Grammar Practice feature (complete blocker)
- 5 frontend E2E tests
- User acceptance testing

---

## Related Issues

- **BUG-006:** GET /next endpoint (fixed, deployed)
- **BUG-010:** Session progress schema (THIS ISSUE)

Both issues must be resolved for Grammar Practice to work.

---

## Contact

**Bug Reporter:** Frontend E2E Test Engineer
**Bug File:** `/backend/tests/BUG-010-session-progress-schema-mismatch.md`
**Frontend Tests:** `/frontend/tests/e2e/grammar-practice.spec.ts` (lines with BUG-010)

**Questions:** Review bug file for full frontend context and error screenshots.

---

**Report Generated:** 2026-01-19
**Status:** 🔴 **CRITICAL - IMMEDIATE FIX REQUIRED**
**Next Action:** Implement backend fix in grammar.py
