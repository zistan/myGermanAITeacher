# Backend Test Engineer Instructions
## German Learning Application - Backend API Testing Guide

**Last Updated:** 2026-01-19
**Role:** Backend Test Engineer
**Project:** myGermanAITeacher
**Backend API:** http://192.168.178.100:8000
**API Documentation:** http://192.168.178.100:8000/docs

---

## Mission Statement

Your mission is to **thoroughly test all 74 backend API endpoints** and **report all bugs discovered** so that backend engineers can fix them. You are **NOT authorized to modify any code** in the backend or frontend, but you **ARE authorized to create and enhance test scripts** in the `/backend/tests/` directory.

---

## Quick Start Guide

**Ready to start testing immediately?**

```bash
# 1. Navigate to tests directory
cd /backend/tests

# 2. Run the comprehensive test suite (all 61+ test cases, 8 phases)
python test_api_manual.py --non-interactive

# 3. Review output for failures (marked with [FAIL])

# 4. Create bug reports for any failures in /backend/tests/bugs/
```

**Your primary testing tool**: `/backend/tests/test_api_manual.py`
- ✅ 1,616 lines of comprehensive API testing
- ✅ Tests all 74 endpoints systematically
- ✅ 8 phases covering all modules
- ✅ Automatic authentication and state management
- ✅ Detailed pass/fail reporting

---

## Critical Constraints

### ✅ ALLOWED Activities
- Create test scripts in `/backend/tests/` directory
- Enhance existing test scripts in `/backend/tests/`
- Create test documentation and reports
- Execute API tests (manual and automated)
- Document bugs with detailed API request/response data
- Create bug reports in `/backend/tests/` as `.md` files
- Update test results documentation
- Create integration test scripts
- Suggest improvements (documentation only)

### ❌ FORBIDDEN Activities
- Modify any backend source code (anything in `/backend/app/`)
- Modify any frontend code (anything in `/frontend/`)
- Modify database schema or migrations
- Modify seed scripts (unless creating test-specific seed data)
- Fix bugs directly in the codebase
- Implement new features or endpoints
- Change API contracts or models
- Modify production configuration files

---

## Reference Documentation

### Primary References
1. **Project Instructions**: `/.claude/claude.md`
   - Complete backend architecture, all 74 endpoints, database schema, modules

2. **API Documentation**: http://192.168.178.100:8000/docs
   - Interactive Swagger UI with all endpoints, request/response schemas, try-it-out functionality

3. **Backend README**: `/backend/README.md` (if exists)
   - Setup instructions, dependencies, environment variables

4. **Deployment Guide**: `/docs/DEPLOYMENT_GUIDE.md`
   - Production deployment, environment setup, troubleshooting

### Supporting References
- **BRD**: `/brd and planning documents/german_learning_app_brd.md`
  - Business requirements, feature specifications
- **Database Models**: `/backend/app/models/`
  - 18 database models with relationships
- **API Schemas**: `/backend/app/schemas/`
  - Pydantic schemas for request/response validation

---

## Backend Architecture Overview

### Technology Stack
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 12+ (15+ recommended)
- **ORM**: SQLAlchemy 2.0
- **AI Service**: Anthropic Claude Sonnet 4.5 (claude-sonnet-4-5)
- **Authentication**: JWT tokens with bcrypt password hashing
- **Migrations**: Alembic

### API Structure (74 Endpoints)

**Authentication (3 endpoints):**
- POST `/api/v1/auth/register` - User registration
- POST `/api/v1/auth/login` - User login (returns JWT token)
- GET `/api/v1/auth/me` - Get current user info

**Conversations (4 endpoints):**
- POST `/api/sessions/start` - Start conversation session
- POST `/api/sessions/{id}/message` - Send message in conversation
- POST `/api/sessions/{id}/end` - End conversation session
- GET `/api/sessions/history` - Get user's conversation history

**Contexts (5 endpoints):**
- GET `/api/contexts` - List all contexts with filters
- GET `/api/contexts/{id}` - Get context details with usage stats
- POST `/api/contexts` - Create custom context
- PUT `/api/contexts/{id}` - Update context
- DELETE `/api/contexts/{id}` - Deactivate context

**Grammar (14 endpoints):**
- GET `/api/grammar/topics` - List all grammar topics
- GET `/api/grammar/topics/{id}` - Get topic details
- POST `/api/grammar/practice/start` - Start practice session
- GET `/api/grammar/practice/{session_id}/next` - Get next exercise
- POST `/api/grammar/practice/{session_id}/answer` - Submit answer
- POST `/api/grammar/practice/{session_id}/end` - End practice session
- GET `/api/grammar/progress` - Get overall grammar progress
- GET `/api/grammar/progress/topic/{topic_id}` - Get topic-specific progress
- POST `/api/grammar/generate-exercises` - AI-generate exercises
- GET `/api/grammar/categories` - List grammar categories
- GET `/api/grammar/recommendations` - Get practice recommendations
- GET `/api/grammar/review-queue` - Get due topics for review
- POST `/api/grammar/diagnostic/start` - Start diagnostic test
- POST `/api/grammar/diagnostic/complete` - Complete diagnostic test

**Vocabulary (26 endpoints):**
- GET `/api/v1/vocabulary/words` - List words with filters
- GET `/api/v1/vocabulary/words/{id}` - Get word details with progress
- POST `/api/v1/vocabulary/words` - Create new word
- POST `/api/v1/vocabulary/flashcards/start` - Start flashcard session
- POST `/api/v1/vocabulary/flashcards/{session_id}/answer` - Submit flashcard answer
- GET `/api/v1/vocabulary/flashcards/{session_id}/current` - Get current flashcard
- POST `/api/v1/vocabulary/lists` - Create vocabulary list
- GET `/api/v1/vocabulary/lists` - Get all lists
- GET `/api/v1/vocabulary/lists/{id}` - Get list with words
- POST `/api/v1/vocabulary/lists/{id}/words` - Add word to list
- DELETE `/api/v1/vocabulary/lists/{id}/words/{word_id}` - Remove word from list
- DELETE `/api/v1/vocabulary/lists/{id}` - Delete list
- POST `/api/v1/vocabulary/quiz/generate` - Generate vocabulary quiz
- POST `/api/v1/vocabulary/quiz/{quiz_id}/answer` - Submit quiz answer
- GET `/api/v1/vocabulary/progress/summary` - Get progress summary
- GET `/api/v1/vocabulary/progress/review-queue` - Get review queue
- POST `/api/v1/vocabulary/analyze` - AI word analysis
- POST `/api/v1/vocabulary/detect` - Detect vocabulary from text
- POST `/api/v1/vocabulary/recommend` - Get word recommendations

**Analytics (14 endpoints):**
- GET `/api/v1/analytics/progress` - Overall progress metrics
- GET `/api/v1/analytics/progress/comparison` - Compare time periods
- GET `/api/v1/analytics/errors` - Error pattern analysis
- POST `/api/v1/analytics/snapshots` - Create progress snapshot
- GET `/api/v1/analytics/snapshots` - Get historical snapshots
- GET `/api/v1/analytics/achievements` - List all achievements
- GET `/api/v1/analytics/achievements/earned` - Get user's earned achievements
- GET `/api/v1/analytics/achievements/progress` - Get achievement progress
- POST `/api/v1/analytics/achievements/{id}/showcase` - Showcase achievement
- GET `/api/v1/analytics/stats` - User statistics
- POST `/api/v1/analytics/stats/refresh` - Refresh user stats
- GET `/api/v1/analytics/leaderboard/{type}` - Get leaderboard (overall/grammar/vocabulary/streak)
- GET `/api/v1/analytics/heatmap/activity` - Activity heatmap (365 days)
- GET `/api/v1/analytics/heatmap/grammar` - Grammar mastery heatmap

**Integration (3 endpoints):**
- GET `/api/v1/integration/session-analysis/{session_id}` - Analyze conversation session with recommendations
- GET `/api/v1/integration/learning-path` - Get personalized learning path
- GET `/api/v1/integration/dashboard` - Get unified dashboard data

**Health (2 endpoints):**
- GET `/` - Root endpoint
- GET `/api/health` - Health check

### Database Schema (18 Tables)

**Core Tables:**
- `users` - User accounts with authentication
- `contexts` - Conversation scenarios (12+ default)
- `sessions` - Conversation practice sessions
- `messages` - Individual conversation messages

**Grammar Module (6 tables):**
- `grammar_topics` - 50+ topics
- `grammar_exercises` - 200+ manual exercises
- `user_grammar_progress` - Mastery tracking with spaced repetition
- `grammar_sessions` - Practice sessions
- `grammar_exercise_attempts` - Individual answers
- `diagnostic_tests` - Assessment results

**Vocabulary Module (4 tables):**
- `vocabulary_words` - 150+ words
- `user_vocabulary_progress` - Mastery tracking (6 levels)
- `user_vocabulary_lists` - Personal vocabulary lists
- `vocabulary_list_words` - List membership association
- `vocabulary_reviews` - Review history

**Analytics Module (4 tables):**
- `achievements` - 31 achievement definitions
- `user_achievements` - Earned achievements with progress
- `user_stats` - Aggregate statistics
- `progress_snapshots` - Historical progress tracking

---

## Main Testing Script

### Primary Test Tool: `test_api_manual.py`

**Location**: `/backend/tests/test_api_manual.py`

This is your **primary testing tool** - a comprehensive 1,616-line script that tests all 74 API endpoints systematically across 8 phases:

- **Phase 1**: Health & Infrastructure (2 endpoints)
- **Phase 2**: Authentication (3 endpoints)
- **Phase 3**: Context Management (5 endpoints)
- **Phase 4**: Conversation Sessions (4 endpoints)
- **Phase 5**: Grammar Learning (11 endpoints)
- **Phase 6**: Vocabulary Learning (19 endpoints)
- **Phase 7**: Analytics & Progress Tracking (14 endpoints)
- **Phase 8**: Integration & Cross-Module (3 endpoints)

### Running the Test Script

**Run all phases**:
```bash
cd /backend/tests
python test_api_manual.py
```

**Run in non-interactive mode** (no pauses between phases):
```bash
python test_api_manual.py --non-interactive
# or
python test_api_manual.py -y
```

**Run specific phase only**:
```bash
python test_api_manual.py --phase=5  # Grammar module only
python test_api_manual.py --phase=6  # Vocabulary module only
```

**Features**:
- ✅ Automatic test user registration and authentication
- ✅ State management across test phases
- ✅ Detailed pass/fail reporting per endpoint
- ✅ Response data validation
- ✅ Database state tracking
- ✅ Error scenario testing
- ✅ Edge case validation

## Test Environment Setup

### Prerequisites
1. **Backend API running**: http://192.168.178.100:8000
   - Verify with: `curl http://192.168.178.100:8000/api/health`
   - Expected response: `{"status":"healthy"}`

2. **Database seeded** with test data:
   - 12+ conversation contexts
   - 50+ grammar topics with 200+ exercises
   - 150+ vocabulary words
   - 31 achievements

3. **Testing tools installed**:
   ```bash
   pip install pytest pytest-asyncio httpx requests
   ```

### Test Script Output

When you run `test_api_manual.py`, you'll see detailed reports like this:

```
================================================================================
TEST REPORT: User Login
================================================================================
Endpoint: POST /api/v1/auth/login
Test Cases: 4
Passed: 3/4
Failed: 1/4

DETAILS:

[PASS] Test 1: Login with valid credentials - PASSED
   Expected: 200
   Actual: 200
   Response keys: ['access_token', 'token_type']
   Note: Token type: bearer
   Note: Token length: 187

[FAIL] Test 2: Login with invalid password (should fail) - FAILED
   Expected: 401
   Actual: 200
   Error response: {...}

OBSERVATIONS:
- Successfully obtained JWT token
- Token format: JWT

DATABASE STATE:
- User authenticated successfully
================================================================================
```

**The script automatically**:
- Creates test users (`testuser1`, `testuser2`)
- Logs in and stores JWT tokens
- Maintains state (session IDs, topic IDs, etc.) across phases
- Tests both success and failure scenarios
- Reports detailed pass/fail results

### Test User Setup

**Note**: `test_api_manual.py` automatically creates test users. You only need to manually create a test user if running individual curl commands:

```bash
curl -X POST http://192.168.178.100:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "test_backend_engineer",
    "email": "backend_test@example.com",
    "password": "TestBackend123!",
    "proficiency_level": "B2"
  }'
```

Save the returned JWT token for authenticated requests.

### Environment Variables
Verify backend `.env` configuration:
- `DATABASE_URL` - PostgreSQL connection string
- `ANTHROPIC_API_KEY` - Valid Claude API key
- `SECRET_KEY` - JWT signing key
- `DEBUG` - Should be False in production

---

## Test Categories & Checklist

### 1. Authentication & Authorization Tests

#### 1.1 User Registration

**Test Case: Register with Valid Data**
- [ ] POST `/api/v1/auth/register` with valid data
- [ ] Verify 201 Created response
- [ ] Verify response includes user ID, username, email
- [ ] Verify password is NOT returned
- [ ] Verify user created in database

**Test Case: Register with Duplicate Username**
- [ ] Register user with existing username
- [ ] Verify 400 Bad Request response
- [ ] Verify error message indicates duplicate username

**Test Case: Register with Duplicate Email**
- [ ] Register user with existing email
- [ ] Verify 400 Bad Request response
- [ ] Verify error message indicates duplicate email

**Test Case: Register with Invalid Email Format**
- [ ] POST with invalid email (e.g., "notanemail")
- [ ] Verify 422 Unprocessable Entity response
- [ ] Verify validation error details

**Test Case: Register with Short Password**
- [ ] POST with password less than 8 characters
- [ ] Verify 422 Unprocessable Entity response
- [ ] Verify validation error for password length

**Test Case: Register with Invalid Proficiency Level**
- [ ] POST with proficiency_level not in [A1, A2, B1, B2, C1, C2]
- [ ] Verify 422 Unprocessable Entity response

**Test Case: Register with Missing Required Fields**
- [ ] POST without username
- [ ] POST without email
- [ ] POST without password
- [ ] Verify 422 errors for each missing field

#### 1.2 User Login

**Test Case: Login with Valid Credentials**
- [ ] POST `/api/v1/auth/login` with correct username/password
- [ ] Verify 200 OK response
- [ ] Verify response includes access_token
- [ ] Verify token_type is "bearer"
- [ ] Verify token is valid JWT

**Test Case: Login with Invalid Username**
- [ ] POST with non-existent username
- [ ] Verify 401 Unauthorized response
- [ ] Verify error message

**Test Case: Login with Invalid Password**
- [ ] POST with correct username but wrong password
- [ ] Verify 401 Unauthorized response
- [ ] Verify error message

**Test Case: Login with Missing Credentials**
- [ ] POST without username
- [ ] POST without password
- [ ] Verify 422 Unprocessable Entity responses

#### 1.3 Protected Endpoints

**Test Case: Access Protected Endpoint Without Token**
- [ ] GET `/api/v1/auth/me` without Authorization header
- [ ] Verify 401 Unauthorized response

**Test Case: Access Protected Endpoint With Invalid Token**
- [ ] GET `/api/v1/auth/me` with invalid token
- [ ] Verify 401 Unauthorized response

**Test Case: Access Protected Endpoint With Expired Token**
- [ ] Use expired JWT token
- [ ] Verify 401 Unauthorized response

**Test Case: Access Protected Endpoint With Valid Token**
- [ ] GET `/api/v1/auth/me` with valid token
- [ ] Verify 200 OK response
- [ ] Verify user details returned

### 2. Conversation Module Tests

#### 2.1 Start Conversation Session

**Test Case: Start Session with Valid Context**
- [ ] POST `/api/sessions/start` with context_id
- [ ] Verify 201 Created response
- [ ] Verify session_id returned
- [ ] Verify initial_message returned
- [ ] Verify session created in database

**Test Case: Start Session with Invalid Context**
- [ ] POST with non-existent context_id
- [ ] Verify 404 Not Found response

**Test Case: Start Session Without Authentication**
- [ ] POST without JWT token
- [ ] Verify 401 Unauthorized response

#### 2.2 Send Message in Session

**Test Case: Send Message with Valid Session**
- [ ] POST `/api/sessions/{id}/message` with message text
- [ ] Verify 200 OK response
- [ ] Verify AI response returned
- [ ] Verify message saved in database

**Test Case: Send Message to Invalid Session**
- [ ] POST with non-existent session_id
- [ ] Verify 404 Not Found response

**Test Case: Send Empty Message**
- [ ] POST with empty message text
- [ ] Verify appropriate error response

**Test Case: Send Message to Ended Session**
- [ ] End a session, then try to send message
- [ ] Verify 400 Bad Request or similar error

#### 2.3 End Session

**Test Case: End Active Session**
- [ ] POST `/api/sessions/{id}/end`
- [ ] Verify 200 OK response
- [ ] Verify summary returned (message_count, duration, etc.)
- [ ] Verify session marked as ended in database

**Test Case: End Already Ended Session**
- [ ] POST `/api/sessions/{id}/end` on ended session
- [ ] Verify appropriate error response

**Test Case: End Invalid Session**
- [ ] POST with non-existent session_id
- [ ] Verify 404 Not Found response

#### 2.4 Session History

**Test Case: Get User's Session History**
- [ ] GET `/api/sessions/history`
- [ ] Verify 200 OK response
- [ ] Verify list of sessions returned
- [ ] Verify sessions belong to authenticated user
- [ ] Verify sessions include context information

**Test Case: Session History Pagination**
- [ ] Create 20+ sessions
- [ ] GET with limit and offset parameters
- [ ] Verify pagination works correctly

### 3. Grammar Module Tests

#### 3.1 Grammar Topics

**Test Case: List All Grammar Topics**
- [ ] GET `/api/grammar/topics`
- [ ] Verify 200 OK response
- [ ] Verify 50+ topics returned
- [ ] Verify each topic has required fields (id, name_de, name_en, category, difficulty)

**Test Case: Filter Topics by Category**
- [ ] GET `/api/grammar/topics?category=verbs`
- [ ] Verify only verb topics returned

**Test Case: Filter Topics by Difficulty**
- [ ] GET `/api/grammar/topics?difficulty=B2`
- [ ] Verify only B2 topics returned

**Test Case: Search Topics**
- [ ] GET `/api/grammar/topics?search=Präsens`
- [ ] Verify matching topics returned

**Test Case: Get Single Topic Details**
- [ ] GET `/api/grammar/topics/{id}`
- [ ] Verify 200 OK response
- [ ] Verify topic details returned
- [ ] Verify explanation in German included

**Test Case: Get Non-Existent Topic**
- [ ] GET `/api/grammar/topics/99999`
- [ ] Verify 404 Not Found response

#### 3.2 Grammar Practice Session

**Test Case: Start Practice Session with Topic**
- [ ] POST `/api/grammar/practice/start` with topic_id
- [ ] Verify 201 Created response
- [ ] Verify session_id returned
- [ ] Verify session configuration returned

**Test Case: Start Practice with Multiple Topics**
- [ ] POST with topic_ids array [1, 2, 3]
- [ ] Verify session includes exercises from all topics

**Test Case: Start Practice with Invalid Topic**
- [ ] POST with non-existent topic_id
- [ ] Verify 404 Not Found response

**Test Case: Get Next Exercise**
- [ ] GET `/api/grammar/practice/{session_id}/next`
- [ ] Verify 200 OK response
- [ ] Verify exercise returned with all required fields
- [ ] Verify exercise type is one of: fill_blank, multiple_choice, translation, error_correction, sentence_building

**Test Case: Get Next Exercise from Empty Session**
- [ ] Complete all exercises in session
- [ ] GET next exercise
- [ ] Verify appropriate response (no more exercises)

**Test Case: Submit Correct Answer**
- [ ] POST `/api/grammar/practice/{session_id}/answer` with correct answer
- [ ] Verify 200 OK response
- [ ] Verify is_correct: true
- [ ] Verify positive feedback returned
- [ ] Verify points awarded

**Test Case: Submit Incorrect Answer**
- [ ] POST with incorrect answer
- [ ] Verify is_correct: false
- [ ] Verify detailed feedback explaining error
- [ ] Verify suggestions provided
- [ ] Verify correct answer revealed

**Test Case: Submit Answer to Invalid Session**
- [ ] POST with non-existent session_id
- [ ] Verify 404 Not Found response

**Test Case: End Practice Session**
- [ ] POST `/api/grammar/practice/{session_id}/end`
- [ ] Verify 200 OK response
- [ ] Verify summary returned (total_exercises, correct_count, accuracy, points, duration)
- [ ] Verify progress updated in database

#### 3.3 Grammar Progress

**Test Case: Get Overall Grammar Progress**
- [ ] GET `/api/grammar/progress`
- [ ] Verify 200 OK response
- [ ] Verify progress data for all topics
- [ ] Verify mastery_level field (0.0-1.0)
- [ ] Verify last_practiced timestamp

**Test Case: Get Topic-Specific Progress**
- [ ] GET `/api/grammar/progress/topic/{topic_id}`
- [ ] Verify 200 OK response
- [ ] Verify detailed progress for topic
- [ ] Verify attempt history

**Test Case: Get Progress for Unpracticed Topic**
- [ ] GET progress for topic never practiced
- [ ] Verify 200 OK with default values (mastery_level: 0.0)

#### 3.4 Grammar Recommendations & Review Queue

**Test Case: Get Practice Recommendations**
- [ ] GET `/api/grammar/recommendations`
- [ ] Verify 200 OK response
- [ ] Verify recommended topics returned
- [ ] Verify recommendations prioritize weak areas

**Test Case: Get Review Queue**
- [ ] GET `/api/grammar/review-queue`
- [ ] Verify 200 OK response
- [ ] Verify due topics returned based on spaced repetition

**Test Case: Get Categories**
- [ ] GET `/api/grammar/categories`
- [ ] Verify list of categories (verbs, nouns, adjectives, etc.)

#### 3.5 AI Exercise Generation

**Test Case: Generate AI Exercises**
- [ ] POST `/api/grammar/generate-exercises` with topic_id and count
- [ ] Verify 200 OK response
- [ ] Verify requested number of exercises generated
- [ ] Verify exercises valid and match topic

**Test Case: Generate with Invalid Topic**
- [ ] POST with non-existent topic_id
- [ ] Verify 404 Not Found response

### 4. Vocabulary Module Tests

#### 4.1 Vocabulary Words

**Test Case: List All Words**
- [ ] GET `/api/v1/vocabulary/words`
- [ ] Verify 200 OK response
- [ ] Verify 150+ words returned
- [ ] Verify each word has required fields (word, translation_it, difficulty, category)

**Test Case: Filter Words by Category**
- [ ] GET `/api/v1/vocabulary/words?category=business`
- [ ] Verify only business words returned

**Test Case: Filter Words by Difficulty**
- [ ] GET `/api/v1/vocabulary/words?difficulty=B2`
- [ ] Verify only B2 words returned

**Test Case: Search Words**
- [ ] GET `/api/v1/vocabulary/words?search=Zahlung`
- [ ] Verify matching words returned

**Test Case: Get Single Word**
- [ ] GET `/api/v1/vocabulary/words/{id}`
- [ ] Verify 200 OK response
- [ ] Verify word details with user progress

**Test Case: Create New Word**
- [ ] POST `/api/v1/vocabulary/words` with word data
- [ ] Verify 201 Created response
- [ ] Verify word created in database

**Test Case: Create Word with Missing Required Fields**
- [ ] POST without required fields
- [ ] Verify 422 Unprocessable Entity response

#### 4.2 Flashcard System

**Test Case: Start Flashcard Session**
- [ ] POST `/api/v1/vocabulary/flashcards/start` with word_ids
- [ ] Verify 201 Created response
- [ ] Verify session_id returned

**Test Case: Get Current Flashcard**
- [ ] GET `/api/v1/vocabulary/flashcards/{session_id}/current`
- [ ] Verify 200 OK response
- [ ] Verify flashcard details returned

**Test Case: Submit Flashcard Answer**
- [ ] POST `/api/v1/vocabulary/flashcards/{session_id}/answer`
- [ ] Verify 200 OK response
- [ ] Verify feedback returned
- [ ] Verify progress updated

#### 4.3 Vocabulary Lists

**Test Case: Create Vocabulary List**
- [ ] POST `/api/v1/vocabulary/lists` with list name
- [ ] Verify 201 Created response
- [ ] Verify list_id returned

**Test Case: Get All User Lists**
- [ ] GET `/api/v1/vocabulary/lists`
- [ ] Verify 200 OK response
- [ ] Verify user's lists returned

**Test Case: Get List with Words**
- [ ] GET `/api/v1/vocabulary/lists/{id}`
- [ ] Verify 200 OK response
- [ ] Verify list details and words returned

**Test Case: Add Word to List**
- [ ] POST `/api/v1/vocabulary/lists/{id}/words` with word_id
- [ ] Verify 200 OK response
- [ ] Verify word added to list

**Test Case: Remove Word from List**
- [ ] DELETE `/api/v1/vocabulary/lists/{id}/words/{word_id}`
- [ ] Verify 200 OK response
- [ ] Verify word removed from list

**Test Case: Delete List**
- [ ] DELETE `/api/v1/vocabulary/lists/{id}`
- [ ] Verify 200 OK response
- [ ] Verify list deleted from database

#### 4.4 Vocabulary Quiz

**Test Case: Generate Quiz**
- [ ] POST `/api/v1/vocabulary/quiz/generate` with word_ids
- [ ] Verify 200 OK response
- [ ] Verify quiz_id returned
- [ ] Verify quiz questions generated

**Test Case: Submit Quiz Answer**
- [ ] POST `/api/v1/vocabulary/quiz/{quiz_id}/answer`
- [ ] Verify 200 OK response
- [ ] Verify answer evaluation returned

#### 4.5 Vocabulary Progress

**Test Case: Get Progress Summary**
- [ ] GET `/api/v1/vocabulary/progress/summary`
- [ ] Verify 200 OK response
- [ ] Verify summary includes total words, mastery levels, accuracy

**Test Case: Get Review Queue**
- [ ] GET `/api/v1/vocabulary/progress/review-queue`
- [ ] Verify 200 OK response
- [ ] Verify due words returned based on spaced repetition

#### 4.6 AI Vocabulary Services

**Test Case: Analyze Word**
- [ ] POST `/api/v1/vocabulary/analyze` with German word
- [ ] Verify 200 OK response
- [ ] Verify analysis includes definition, usage examples, synonyms

**Test Case: Detect Vocabulary**
- [ ] POST `/api/v1/vocabulary/detect` with German text
- [ ] Verify 200 OK response
- [ ] Verify vocabulary words detected from text

**Test Case: Get Recommendations**
- [ ] POST `/api/v1/vocabulary/recommend`
- [ ] Verify 200 OK response
- [ ] Verify word recommendations based on user level

### 5. Analytics Module Tests

#### 5.1 Progress Tracking

**Test Case: Get Overall Progress**
- [ ] GET `/api/v1/analytics/progress`
- [ ] Verify 200 OK response
- [ ] Verify progress score (0-100)
- [ ] Verify module-specific metrics

**Test Case: Compare Progress Periods**
- [ ] GET `/api/v1/analytics/progress/comparison?start_date=X&end_date=Y`
- [ ] Verify 200 OK response
- [ ] Verify comparison data for specified period

**Test Case: Get Error Analysis**
- [ ] GET `/api/v1/analytics/errors`
- [ ] Verify 200 OK response
- [ ] Verify error patterns identified
- [ ] Verify recurring mistakes highlighted

#### 5.2 Progress Snapshots

**Test Case: Create Progress Snapshot**
- [ ] POST `/api/v1/analytics/snapshots`
- [ ] Verify 201 Created response
- [ ] Verify snapshot saved with timestamp

**Test Case: Get Historical Snapshots**
- [ ] GET `/api/v1/analytics/snapshots?period=weekly`
- [ ] Verify 200 OK response
- [ ] Verify snapshots returned for specified period

#### 5.3 Achievements

**Test Case: List All Achievements**
- [ ] GET `/api/v1/analytics/achievements`
- [ ] Verify 200 OK response
- [ ] Verify 31 achievements returned
- [ ] Verify achievements have tiers (bronze, silver, gold, platinum)

**Test Case: Get Earned Achievements**
- [ ] GET `/api/v1/analytics/achievements/earned`
- [ ] Verify 200 OK response
- [ ] Verify user's earned achievements returned
- [ ] Verify timestamps included

**Test Case: Get Achievement Progress**
- [ ] GET `/api/v1/analytics/achievements/progress`
- [ ] Verify 200 OK response
- [ ] Verify progress toward unearned achievements

**Test Case: Showcase Achievement**
- [ ] POST `/api/v1/analytics/achievements/{id}/showcase`
- [ ] Verify 200 OK response
- [ ] Verify achievement marked as showcased

#### 5.4 User Statistics

**Test Case: Get User Stats**
- [ ] GET `/api/v1/analytics/stats`
- [ ] Verify 200 OK response
- [ ] Verify stats include total_sessions, total_exercises, current_streak, etc.

**Test Case: Refresh Stats**
- [ ] POST `/api/v1/analytics/stats/refresh`
- [ ] Verify 200 OK response
- [ ] Verify stats recalculated

#### 5.5 Leaderboards

**Test Case: Get Overall Leaderboard**
- [ ] GET `/api/v1/analytics/leaderboard/overall`
- [ ] Verify 200 OK response
- [ ] Verify top users ranked by overall score

**Test Case: Get Grammar Leaderboard**
- [ ] GET `/api/v1/analytics/leaderboard/grammar`
- [ ] Verify top users ranked by grammar mastery

**Test Case: Get Vocabulary Leaderboard**
- [ ] GET `/api/v1/analytics/leaderboard/vocabulary`
- [ ] Verify top users ranked by vocabulary mastery

**Test Case: Get Streak Leaderboard**
- [ ] GET `/api/v1/analytics/leaderboard/streak`
- [ ] Verify top users ranked by current streak

**Test Case: Invalid Leaderboard Type**
- [ ] GET `/api/v1/analytics/leaderboard/invalid_type`
- [ ] Verify 400 Bad Request or 422 error

#### 5.6 Heatmaps

**Test Case: Get Activity Heatmap**
- [ ] GET `/api/v1/analytics/heatmap/activity`
- [ ] Verify 200 OK response
- [ ] Verify 365 days of activity data returned

**Test Case: Get Grammar Mastery Heatmap**
- [ ] GET `/api/v1/analytics/heatmap/grammar`
- [ ] Verify 200 OK response
- [ ] Verify grammar mastery data per topic

### 6. Integration Module Tests

#### 6.1 Session Analysis

**Test Case: Analyze Conversation Session**
- [ ] GET `/api/v1/integration/session-analysis/{session_id}`
- [ ] Verify 200 OK response
- [ ] Verify grammar recommendations returned
- [ ] Verify vocabulary recommendations returned
- [ ] Verify analysis includes detected errors

**Test Case: Analyze Invalid Session**
- [ ] GET with non-existent session_id
- [ ] Verify 404 Not Found response

#### 6.2 Learning Path

**Test Case: Get Personalized Learning Path**
- [ ] GET `/api/v1/integration/learning-path`
- [ ] Verify 200 OK response
- [ ] Verify daily plan returned (75 min breakdown)
- [ ] Verify weekly goals returned
- [ ] Verify recommendations prioritize weak areas

**Test Case: Get Learning Path for New User**
- [ ] GET with new user account (no history)
- [ ] Verify default learning path returned

#### 6.3 Dashboard Data

**Test Case: Get Unified Dashboard**
- [ ] GET `/api/v1/integration/dashboard`
- [ ] Verify 200 OK response
- [ ] Verify all dashboard sections included:
  - Overall progress
  - Weekly goals
  - Module statistics
  - Current streak
  - Due items (grammar + vocabulary)
  - Quick actions
  - Recent activity
  - Close achievements

**Test Case: Dashboard Performance**
- [ ] Measure response time for dashboard endpoint
- [ ] Target: <2 seconds
- [ ] Verify single API call provides all data

### 7. Context Management Tests

**Test Case: List All Contexts**
- [ ] GET `/api/contexts`
- [ ] Verify 200 OK response
- [ ] Verify 12+ contexts returned (6 business, 6 daily)

**Test Case: Filter Contexts by Type**
- [ ] GET `/api/contexts?context_type=business`
- [ ] Verify only business contexts returned

**Test Case: Get Context Details**
- [ ] GET `/api/contexts/{id}`
- [ ] Verify 200 OK response
- [ ] Verify context details with usage statistics

**Test Case: Create Custom Context**
- [ ] POST `/api/contexts` with custom context data
- [ ] Verify 201 Created response
- [ ] Verify context created with user as owner

**Test Case: Update Context**
- [ ] PUT `/api/contexts/{id}` with updated data
- [ ] Verify 200 OK response
- [ ] Verify context updated in database

**Test Case: Delete Context**
- [ ] DELETE `/api/contexts/{id}`
- [ ] Verify 200 OK response
- [ ] Verify context deactivated (not hard deleted)

---

## Edge Cases & Error Scenarios

### 8.1 Data Validation Tests

**Test Case: Invalid Data Types**
- [ ] Send string where integer expected
- [ ] Send integer where string expected
- [ ] Verify 422 Unprocessable Entity with field-level errors

**Test Case: Out of Range Values**
- [ ] Send mastery_level > 1.0
- [ ] Send difficulty not in [A1-C2]
- [ ] Verify validation errors

**Test Case: Very Long Text Input**
- [ ] Send 10,000+ character message
- [ ] Verify appropriate handling (truncation or error)

**Test Case: Special Characters**
- [ ] Send German special characters (ä, ö, ü, ß)
- [ ] Verify proper Unicode handling

**Test Case: SQL Injection Attempt**
- [ ] Send `'; DROP TABLE users; --` in input fields
- [ ] Verify parameterized queries prevent injection

**Test Case: XSS Attempt**
- [ ] Send `<script>alert('XSS')</script>` in text fields
- [ ] Verify sanitization/escaping

### 8.2 Spaced Repetition Algorithm Tests

**Test Case: Initial Mastery Level**
- [ ] Practice topic for first time
- [ ] Verify mastery_level starts at 0.0

**Test Case: Mastery Level Increase**
- [ ] Answer 5 exercises correctly
- [ ] Verify mastery_level increases appropriately

**Test Case: Mastery Level Decrease**
- [ ] Answer exercises incorrectly
- [ ] Verify mastery_level decreases or increases slower

**Test Case: Review Interval Calculation**
- [ ] Complete topic with high mastery
- [ ] Verify next_review_date calculated correctly (exponential backoff)

**Test Case: Due Items Calculation**
- [ ] Verify review queue only includes items past next_review_date

### 8.3 Concurrent Request Tests

**Test Case: Concurrent Session Creation**
- [ ] Create multiple sessions simultaneously
- [ ] Verify all sessions created correctly
- [ ] Verify no race conditions

**Test Case: Concurrent Exercise Submission**
- [ ] Submit multiple answers rapidly
- [ ] Verify all recorded correctly
- [ ] Verify progress updates atomic

### 8.4 Performance & Load Tests

**Test Case: Response Time - Simple GET**
- [ ] GET `/api/health`
- [ ] Measure response time
- [ ] Target: <100ms

**Test Case: Response Time - Complex Dashboard**
- [ ] GET `/api/v1/integration/dashboard`
- [ ] Measure response time
- [ ] Target: <2 seconds

**Test Case: Response Time - AI-Powered Endpoints**
- [ ] POST `/api/sessions/{id}/message` (calls Claude API)
- [ ] Measure response time
- [ ] Target: <5 seconds (depends on Claude API)

**Test Case: Large Dataset Query**
- [ ] GET grammar progress with 50+ topics
- [ ] Verify query optimized (N+1 queries avoided)

**Test Case: Pagination Performance**
- [ ] GET endpoints with limit=100
- [ ] Verify performance acceptable

---

## Bug Reporting Guidelines

### Bug Report Template

Create a file: `/backend/tests/bugs/BUG-XXX-short-title.md`

```markdown
# BUG-XXX: [Short Descriptive Title]

**Severity:** [Critical | High | Medium | Low]
**Category:** [Authentication | Conversation | Grammar | Vocabulary | Analytics | Integration | Database | Performance]
**Reported:** [Date]
**Reporter:** [Your name]
**Status:** [Open | In Progress | Fixed | Closed | Wont Fix]

## Description
[Brief description of the bug]

## API Endpoint
**Method:** [GET | POST | PUT | DELETE]
**URL:** [Full endpoint URL]
**Authentication:** [Required | Not Required]

## Steps to Reproduce
1. [First step with exact API call]
2. [Second step]
3. [Third step]
...

## Request Details
```bash
# Example curl command
curl -X POST http://192.168.178.100:8000/api/endpoint \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"field": "value"}'
```

**Request Headers:**
```
Authorization: Bearer eyJ...
Content-Type: application/json
```

**Request Body:**
```json
{
  "field1": "value1",
  "field2": "value2"
}
```

## Expected Result
**Status Code:** [200 | 201 | 204]
**Response Body:**
```json
{
  "expected": "response"
}
```

## Actual Result
**Status Code:** [Actual status code]
**Response Body:**
```json
{
  "actual": "response",
  "error": "error message"
}
```

## Server Logs
```
[Paste relevant server logs from journalctl -u german-learning -f]
```

## Database State
[If relevant, show database query results]
```sql
SELECT * FROM table WHERE condition;
```

## Environment
- **Backend URL:** http://192.168.178.100:8000
- **Python Version:** 3.10
- **PostgreSQL Version:** 15
- **FastAPI Version:** [Check requirements.txt]

## Impact Analysis
- **Users Affected:** [All users | Specific user types]
- **Workaround Available:** [Yes | No] [If yes, describe]
- **Data Integrity:** [At Risk | Safe]

## Possible Root Cause
[Your analysis of what might be causing the bug]

## Related Code
**File:** `/backend/app/path/to/file.py`
**Function:** `function_name`
**Line:** [Line number if known]

## Related Bugs
[Links to related bug reports, if any]

## Additional Context
[Any other relevant information]
```

### Severity Classification

**Critical (P0):**
- API completely down or unreachable
- Data loss or corruption
- Security vulnerabilities (authentication bypass, SQL injection successful)
- Database connection failures
- 500 errors on core endpoints (auth, sessions, practice)

**High (P1):**
- Major features broken (can't start practice, progress not saving)
- Incorrect data returned (wrong user data, wrong exercises)
- AI service failures
- Significant performance degradation (>10s response times)
- Authorization bypass allowing access to other users' data

**Medium (P2):**
- Minor features broken (statistics incorrect, recommendations suboptimal)
- Validation errors not user-friendly
- Slow performance (2-5s on simple endpoints)
- Non-critical data inconsistencies
- Misleading error messages

**Low (P3):**
- Cosmetic API response issues
- Minor optimization opportunities
- Documentation inconsistencies
- Non-critical validation edge cases
- Typos in error messages

### Bug Summary Document

Create a file: `/backend/tests/bug-summary.md`

```markdown
# Backend API Bug Summary

**Last Updated:** [Date]
**Total Bugs:** XX
**Critical:** X | **High:** X | **Medium:** X | **Low:** X

## Critical Bugs (P0)

### BUG-001: [Title]
- **Status:** Open
- **Category:** Authentication
- **Link:** [./bugs/BUG-001-title.md](./bugs/BUG-001-title.md)
- **Impact:** All users unable to login

## High Bugs (P1)

### BUG-002: [Title]
- **Status:** Open
- **Category:** Grammar
- **Link:** [./bugs/BUG-002-title.md](./bugs/BUG-002-title.md)
- **Impact:** Practice sessions not saving progress

## Medium Bugs (P2)
...

## Low Bugs (P3)
...

## Fixed Bugs
### BUG-XXX: [Title]
- **Fixed Date:** [Date]
- **Fixed In:** [Git commit hash]
- **Verified:** [Yes | No]

## Statistics
- **Open:** XX
- **In Progress:** XX
- **Fixed:** XX
- **Closed:** XX

## Trends
[Analysis of common bug patterns, frequently problematic modules, etc.]
```

---

## Understanding test_api_manual.py Structure

### Key Components

**1. TestState Class** (Lines 18-31)
- Stores state across test phases (auth tokens, IDs)
- Automatically populated as tests run
- Used by subsequent tests (e.g., session_id from Phase 4 used in Phase 8)

**2. TestResult Class** (Lines 34-59)
- Records individual test case results
- Tracks expected vs actual status codes
- Stores response data and errors
- Adds contextual notes

**3. EndpointTestReport Class** (Lines 61-143)
- Groups multiple test cases for one endpoint
- Generates formatted reports
- Tracks database changes and observations
- Calculates pass/fail statistics

**4. make_request() Function** (Lines 145-193)
- Centralized HTTP request handler
- Automatically adds authentication headers
- Handles both JSON and form data
- Returns TestResult objects

**5. Phase Test Functions** (Lines 196-1489)
- `test_phase1_health()` - Health & infrastructure
- `test_phase2_authentication()` - Auth flow
- `test_phase3_contexts()` - Context management
- `test_phase4_conversations()` - Conversation sessions
- `test_phase5_grammar()` - Grammar module
- `test_phase6_vocabulary()` - Vocabulary module
- `test_phase7_analytics()` - Analytics & progress
- `test_phase8_integration()` - Cross-module workflows

### Extending test_api_manual.py

**To add a new test case** to an existing phase:

```python
# Inside test_phaseX_module():
report = EndpointTestReport("Test Name", "METHOD", "/api/endpoint")

# Test case 1: Success scenario
result = make_request("GET", "/api/endpoint", use_auth=True, expected_status=200)
result.name = "Description of what this tests"
report.add_test(result)

if result.passed:
    # Store any IDs or data for later tests
    some_id = result.response_data.get('id')
    state.some_ids.append(some_id)
    report.add_db_change(f"Created resource with ID: {some_id}")

# Test case 2: Error scenario
result2 = make_request("GET", "/api/endpoint/99999", use_auth=True, expected_status=404)
result2.name = "Test with invalid ID (should fail)"
report.add_test(result2)

report.print_report()
```

**To add a new endpoint not yet covered**:

1. Identify which phase it belongs to (or create Phase 9 if cross-cutting)
2. Add test function following the pattern above
3. Call it from `main()` function
4. Update total endpoint count in documentation

### Analyzing Test Failures

When `test_api_manual.py` reports a failure:

1. **Check the report output**:
   - Expected status vs Actual status
   - Response data (first 500 chars shown)
   - Error message if exception occurred

2. **Review server logs**:
   ```bash
   sudo journalctl -u german-learning -f -n 100
   ```

3. **Reproduce with curl**:
   ```bash
   # Copy endpoint details from test
   curl -X POST http://192.168.178.100:8000/api/endpoint \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"field": "value"}'
   ```

4. **Create bug report**: Use template in bug reporting section

## Test Automation Scripts

### Additional Testing Tools

Beyond `test_api_manual.py`, you can create supplementary test scripts.

Create file: `/backend/tests/api_test_helper.py`

```python
import httpx
import pytest
from typing import Dict, Optional

BASE_URL = "http://192.168.178.100:8000"

class APITestHelper:
    def __init__(self):
        self.base_url = BASE_URL
        self.token: Optional[str] = None
        self.client = httpx.Client(base_url=self.base_url, timeout=10.0)

    def register_user(self, username: str, email: str, password: str, proficiency_level: str = "B2") -> Dict:
        """Register a new user"""
        response = self.client.post("/api/v1/auth/register", json={
            "username": username,
            "email": email,
            "password": password,
            "proficiency_level": proficiency_level
        })
        return response.json()

    def login(self, username: str, password: str) -> str:
        """Login and return JWT token"""
        response = self.client.post("/api/v1/auth/login", data={
            "username": username,
            "password": password
        })
        data = response.json()
        self.token = data["access_token"]
        return self.token

    def get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if not self.token:
            raise ValueError("Not authenticated. Call login() first.")
        return {"Authorization": f"Bearer {self.token}"}

    def get(self, endpoint: str, **kwargs) -> httpx.Response:
        """Authenticated GET request"""
        return self.client.get(endpoint, headers=self.get_headers(), **kwargs)

    def post(self, endpoint: str, **kwargs) -> httpx.Response:
        """Authenticated POST request"""
        return self.client.post(endpoint, headers=self.get_headers(), **kwargs)

    def put(self, endpoint: str, **kwargs) -> httpx.Response:
        """Authenticated PUT request"""
        return self.client.put(endpoint, headers=self.get_headers(), **kwargs)

    def delete(self, endpoint: str, **kwargs) -> httpx.Response:
        """Authenticated DELETE request"""
        return self.client.delete(endpoint, headers=self.get_headers(), **kwargs)

    def close(self):
        """Close HTTP client"""
        self.client.close()
```

### Sample Test Script

Create file: `/backend/tests/test_api_authentication.py`

```python
import pytest
from api_test_helper import APITestHelper
import time

def test_register_and_login():
    """Test user registration and login flow"""
    helper = APITestHelper()

    # Generate unique username
    timestamp = int(time.time())
    username = f"test_user_{timestamp}"
    email = f"test_{timestamp}@example.com"
    password = "TestPass123!"

    try:
        # Test registration
        register_response = helper.register_user(username, email, password)
        assert "id" in register_response
        assert register_response["username"] == username
        assert register_response["email"] == email
        assert "password" not in register_response  # Password should not be returned

        print(f"✅ Registration successful: User ID {register_response['id']}")

        # Test login
        token = helper.login(username, password)
        assert token is not None
        assert len(token) > 0

        print(f"✅ Login successful: Token received")

        # Test /me endpoint
        me_response = helper.get("/api/v1/auth/me")
        assert me_response.status_code == 200
        me_data = me_response.json()
        assert me_data["username"] == username

        print(f"✅ /me endpoint working: {me_data['username']}")

    finally:
        helper.close()

def test_login_with_invalid_credentials():
    """Test login with wrong password"""
    helper = APITestHelper()

    try:
        response = helper.client.post("/api/v1/auth/login", data={
            "username": "nonexistent_user",
            "password": "wrongpassword"
        })
        assert response.status_code == 401
        print(f"✅ Invalid login correctly rejected with 401")

    finally:
        helper.close()

def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without authentication"""
    helper = APITestHelper()

    try:
        response = helper.client.get("/api/v1/auth/me")
        assert response.status_code == 401
        print(f"✅ Protected endpoint correctly requires authentication")

    finally:
        helper.close()

if __name__ == "__main__":
    print("Running authentication tests...\n")
    test_register_and_login()
    test_login_with_invalid_credentials()
    test_protected_endpoint_without_token()
    print("\n✅ All authentication tests passed!")
```

### Run Tests

```bash
cd /backend/tests
python test_api_authentication.py
```

---

## Test Results Documentation

Create file: `/backend/tests/test-results.md`

```markdown
# Backend API Test Results

**Test Date:** [Date]
**Tester:** [Your name]
**Backend Version:** [Git commit hash]
**API Base URL:** http://192.168.178.100:8000

## Test Execution Summary

**Total Test Cases:** XXX
**Passed:** XXX (XX%)
**Failed:** XX (XX%)
**Blocked:** XX (XX%)
**Not Tested:** XX (XX%)

## Results by Module

### Authentication (X/X passed)
- ✅ User registration
- ✅ User login
- ✅ Protected endpoints
- ❌ Token expiration handling

### Conversations (X/X passed)
- ✅ Start session
- ✅ Send message
- ✅ End session
- ✅ Session history

### Grammar (X/X passed)
- ✅ List topics
- ✅ Start practice
- ✅ Submit answers
- ❌ Progress tracking

### Vocabulary (X/X passed)
- ✅ List words
- ✅ Flashcards
- ✅ Lists management
- ✅ Quizzes

### Analytics (X/X passed)
- ✅ Progress metrics
- ✅ Achievements
- ✅ Leaderboards
- ✅ Heatmaps

### Integration (X/X passed)
- ✅ Session analysis
- ✅ Learning path
- ✅ Dashboard

## Performance Metrics

| Endpoint | Target | Actual | Status |
|----------|--------|--------|--------|
| GET /api/health | <100ms | XXms | ✅/❌ |
| POST /api/v1/auth/login | <1s | XXms | ✅/❌ |
| GET /api/v1/integration/dashboard | <2s | XXms | ✅/❌ |
| POST /api/sessions/{id}/message | <5s | XXms | ✅/❌ |
| GET /api/grammar/topics | <500ms | XXms | ✅/❌ |

## Detailed Test Results

### Authentication Module

#### TEST-AUTH-001: Register with valid data
- **Status:** ✅ PASS
- **Response Time:** XXXms
- **Notes:** [Any notes]

#### TEST-AUTH-002: Login with valid credentials
- **Status:** ❌ FAIL
- **Response Time:** XXXms
- **Bug:** [Link to BUG-XXX]
- **Notes:** Returns 500 error instead of 200

[Continue for all test cases...]

## Bug Summary
**Total Bugs Found:** XX
- **Critical:** X
- **High:** X
- **Medium:** X
- **Low:** X

See [bug-summary.md](./bug-summary.md) for complete bug list.

## Coverage Analysis

**Endpoints Tested:** XX/74 (XX%)
**Endpoints Not Tested:** [List endpoints not yet tested]

## Recommendations

### High Priority
1. [Critical fix needed]
2. [Important improvement]

### Medium Priority
3. [Moderate improvement]
4. [Performance optimization]

### Low Priority
5. [Nice-to-have enhancement]

## Next Steps
- [ ] Fix and retest failed test cases
- [ ] Complete untested endpoints
- [ ] Load testing with 100+ concurrent requests
- [ ] Security audit (penetration testing)
- [ ] Integration testing with frontend
```

---

## Daily Testing Workflow

### Morning Routine
1. **Check backend status**
   ```bash
   curl http://192.168.178.100:8000/api/health
   ```

2. **Review recent changes**
   ```bash
   cd /opt/german-learning-app
   git log --oneline -10
   ```

3. **Check for new migrations**
   ```bash
   cd backend
   alembic history
   ```

### Testing Session

**Option 1: Full Comprehensive Test** (Recommended for major changes or weekly regression)
```bash
cd /backend/tests
python test_api_manual.py --non-interactive 2>&1 | tee test_output_$(date +%Y%m%d).log
```
This runs all 61+ test cases across 8 phases and saves output to a log file.

**Option 2: Targeted Module Test** (For specific feature changes)
```bash
# Test only grammar module
python test_api_manual.py --phase=5 --non-interactive

# Test only vocabulary module
python test_api_manual.py --phase=6 --non-interactive

# Test only analytics module
python test_api_manual.py --phase=7 --non-interactive
```

**Option 3: Manual Specific Endpoint Test** (For quick verification)
```bash
# Use curl or custom test script for specific endpoint
curl -X GET http://192.168.178.100:8000/api/grammar/topics \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Workflow Steps**:
1. Run `test_api_manual.py` with appropriate phase/flags
2. Review output for PASS/FAIL status
3. Document failures immediately in bug reports
4. For each failure:
   - Check actual vs expected status codes
   - Review error response
   - Check server logs: `sudo journalctl -u german-learning -f`
   - Create bug report in `/backend/tests/bugs/`
5. Update test results summary

### End of Day
1. Update test results document (`/backend/tests/test-results.md`)
2. Update bug summary (`/backend/tests/bug-summary.md`)
3. Generate summary report with statistics
4. Communicate findings to backend engineers
5. Plan next day's testing focus

---

## Tools & Resources

### Command Line Tools
- `curl` - HTTP requests
- `jq` - JSON parsing
- `psql` - PostgreSQL client
- `python` - Test scripts

### Python Libraries
- `httpx` - HTTP client
- `pytest` - Testing framework
- `pytest-asyncio` - Async testing

### Monitoring
- Server logs: `sudo journalctl -u german-learning -f`
- PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-*.log`

---

## Success Criteria

Your testing is successful when:

- ✅ All 74 endpoints tested comprehensively
- ✅ 200+ test cases executed
- ✅ All bugs documented with reproduction steps
- ✅ Bug reports include curl commands and responses
- ✅ Test results documented and up-to-date
- ✅ Automated test suite created
- ✅ Performance metrics collected
- ✅ Edge cases and error scenarios tested
- ✅ Security vulnerabilities checked (SQL injection, XSS, auth bypass)
- ✅ Spaced repetition algorithm verified

---

**Remember: Your goal is to find bugs so backend engineers can fix them and deliver a high-quality API. Be thorough, be detailed, and test like a user trying to break the system!**
