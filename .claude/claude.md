# Claude Code Project Context

## Project: German Learning Application (myGermanAITeacher)

### Overview
An AI-powered German language learning application designed for advanced learners (B2/C1 level) with a focus on:
- Business vocabulary (payments/finance sector)
- Conversational fluency (business & everyday contexts)
- Comprehensive grammar mastery through systematic drilling

**User Profile**: Igor - Italian native speaker, fluent in English, works in payments/finance in Switzerland

### Core Features
1. **AI Conversation Practice**: Interactive conversations with Anthropic Claude in 12+ contexts (business + daily)
2. **Grammar Learning System**: 50+ topics, 200+ manual exercises, AI-generated exercises, spaced repetition
3. **Vocabulary Management**: 150+ words (foundation for 1000+) with flashcards and spaced repetition
4. **Progress Analytics**: Comprehensive tracking with 31 achievements, heatmaps, leaderboards
5. **Cross-Module Integration**: Seamless workflows with personalized learning paths

### Technology Stack

**Backend:**
- Python 3.10+ (3.10 or 3.11+ supported)
- FastAPI (REST API)
- PostgreSQL 12+ (15+ recommended)
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Anthropic Claude Sonnet 4.5 (AI - auto-updating)

**Frontend (Planned):**
- React 18 + TypeScript
- Vite (build tool)
- Tailwind CSS (styling)
- Zustand (state management)
- Axios (HTTP client)

**Deployment:**
- Local Ubuntu server or development machine
- Uvicorn (ASGI server)
- Nginx (reverse proxy, optional)

### Project Status
**Current Phase**: 🚀 Phase 6.5 - Production Deployment (In Progress)
**Previous Phase**: ✅ Phase 6 Complete - Backend Fully Implemented!
**Next Phase**: Phase 7 - Frontend Development
**Timeline**: 10-week development plan
**Deployment Target**: Ubuntu 20.04 LTS server

### Completed Phases

#### ✅ Phase 1: Core Infrastructure (Complete)
- FastAPI backend with 20 database models
- JWT authentication with bcrypt
- PostgreSQL database setup
- Alembic migrations (2 migrations: 001, 002)
- All core models: User, Context, Session, Message, Grammar (6 tables), Vocabulary (7 tables), Achievement (4 tables)

#### ✅ Phase 2: AI Integration & Conversation Engine (Complete)
- ConversationAI service with Claude 3.5 Sonnet
- Session management (start, message, end, history)
- 12+ pre-configured contexts (6 business, 6 daily)
- Grammar and vocabulary detection in conversations
- Context management API (5 endpoints)

#### ✅ Phase 3: Grammar Learning System (Complete)
- 50+ grammar topics with German explanations
- 200+ manual exercises (5 types: fill_blank, multiple_choice, translation, error_correction, sentence_building)
- GrammarAIService for dynamic exercise generation
- Spaced repetition algorithm (exponential backoff)
- 14 grammar API endpoints
- Diagnostic tests
- 25 comprehensive tests

#### ✅ Phase 4: Vocabulary Management System (Complete)
- 150+ vocabulary words (foundation for 1000+)
- VocabularyAIService with 7 AI-powered methods
- Flashcard system with multiple types (definition, translation, usage, synonym, example)
- Personal vocabulary lists with notes
- Spaced repetition (SM-2 inspired, 6 mastery levels)
- Vocabulary quiz generation (multiple choice, fill blank, matching)
- 26 vocabulary API endpoints
- 30 comprehensive tests

#### ✅ Phase 5: Progress Tracking & Analytics (Complete)
- AnalyticsService with 15+ analysis methods
- Achievement system: 31 achievements, 4 tiers (bronze/silver/gold/platinum), 5,825 points
- Error pattern analysis with recurring mistake detection
- Improvement trend analysis
- Activity and grammar mastery heatmaps
- Leaderboard rankings
- Progress snapshots (daily/weekly/monthly)
- 14 analytics API endpoints
- 18 comprehensive tests

#### ✅ Phase 6: Context Library & Integration (Complete)
- IntegrationService for cross-module workflows
- Conversation → Grammar/Vocabulary flow (session analysis with recommendations)
- Personalized learning paths (daily/weekly plans)
- Unified dashboard endpoint
- Due items tracking (grammar + vocabulary)
- Recent activity timeline
- Quick action recommendations
- 3 integration API endpoints
- 11 comprehensive tests

#### 🚀 Phase 6.5: Production Deployment (In Progress)
**Target Environment:** Ubuntu 20.04 LTS server with Python 3.10

**Deployment Components:**
- ✅ Comprehensive deployment documentation (DEPLOYMENT_GUIDE.md)
- ✅ Automated setup script (setup-server.sh)
- ✅ Systemd service configuration
- ✅ Nginx reverse proxy configuration
- ✅ Production environment template (.env.production)
- ✅ Step-by-step deployment checklist
- 🔄 Database migration execution
- 🔄 Initial data seeding
- ⏳ Service startup and verification
- ⏳ SSL/HTTPS configuration
- ⏳ Firewall and security hardening

**Production Fixes Applied (Phase 6.5):**

**Initial Deployment Issues (Resolved):**
1. **Python 3.11 Availability** - Added deadsnakes PPA for Python 3.10/3.11 installation on Ubuntu 20.04
2. **SQLAlchemy Reserved Keywords** - Fixed `metadata` column conflicts in models
3. **Model Import Issues** - Added missing Achievement model imports
4. **Duplicate Model Definitions** - Removed duplicate ProgressSnapshot
5. **PostgreSQL Configuration** - Configured pg_hba.conf for local md5 authentication

**Production Testing Fixes (2026-01-17):**
6. **bcrypt Compatibility** - Pinned bcrypt==4.2.0 for passlib 1.7.4 compatibility (fixed user registration)
7. **JWT Specification** - Convert user.id to string in JWT "sub" claim per RFC 7519
8. **Session History Endpoint** - Added missing GET /api/sessions/history endpoint for listing user sessions
9. **Claude Model Update** - Upgraded to Claude Sonnet 4.5 (claude-sonnet-4-5) with auto-updating alias
10. **Grammar Topic Schema** - Removed non-existent updated_at field from GrammarTopicResponse
11. **Grammar Practice Session** - Store target_level in grammar_metadata JSON field
12. **GrammarSession Field Names** - Fixed total_attempted → total_exercises, total_correct → exercises_correct
13. **GrammarExerciseAttempt** - Fixed session_id → grammar_session_id, added user_id field
14. **SessionWithContext** - Fixed SQLAlchemy metadata conflict using explicit field assignment
15. **UserGrammarProgress Fields** - Fixed all field names and mastery_level type (float 0.0-1.0)
16. **Grammar Progress Endpoints** - Fixed field names and mastery level conversions in progress/weak-areas/summary
17. **Vocabulary Model/Schema Alignment** - Fixed 550 validation errors by aligning Vocabulary model field names with schemas
18. **Vocabulary Database Migration** - Created comprehensive migration (001_update_vocabulary_schema) to update existing database schema

**Multi-Worker Session Persistence Fix (2026-01-19 - BUG-015, BUG-016):**
19. **Vocabulary Session Persistence** - Replaced in-memory dictionaries with database persistence for flashcard sessions and vocabulary quizzes

**Root Cause:** In-memory dictionaries (`flashcard_sessions = {}`, `vocabulary_quizzes = {}`) caused 404 errors in multi-worker deployments. Sessions created on Worker A were not accessible on Worker B due to isolated process memory. All sessions were also lost on server restart.

**Frontend Grammar Practice Fixes (2026-01-20 - BUG-020, BUG-021):**
20. **Grammar Practice Loading Issue (BUG-020)** - Fixed infinite loading when clicking "Practice This Topic"
21. **Second Session Loading Issue (BUG-021)** - Fixed second grammar session getting stuck after completing first session

**BUG-020 Root Cause:** Frontend sent both `topic_ids` and `difficulty_level` filters. When topic had no exercises at requested difficulty (e.g., Topic 1 "Nominative Case" has only A1 exercises but B2 was requested), backend returned 404. Frontend didn't handle this gracefully, showing loading spinner forever.

**BUG-020 Solution:**
- Only send `difficulty_level` if explicitly specified in URL (conditional parameter)
- Add error handling that detects "No exercises found" and retries without difficulty filter
- User sees helpful warning: "This topic doesn't have B2 level exercises. Trying with all available difficulties..."
- File: `frontend/src/pages/grammar/PracticeSessionPage.tsx`

**BUG-021 Root Cause:** After completing a session, `endSession()` only set `sessionState` to 'completed' but did NOT clear `currentSession`, `sessionNotes`, or `bookmarkedExercises`. Stale data persisted in localStorage via Zustand, causing race condition when starting second session.

**BUG-021 Solution:**
- Clear all session data in `endSession()`: currentSession, currentExercise, sessionNotes, bookmarkedExercises
- Add defensive clear before starting new session (safety net for edge cases)
- Files: `frontend/src/store/grammarStore.ts`, `frontend/src/pages/grammar/PracticeSessionPage.tsx`

**Benefits:**
- ✅ Grammar practice works smoothly for all topics
- ✅ Can start multiple sessions in succession without hangs
- ✅ Better error messages guide users when filters don't match
- ✅ Clean localStorage state between sessions
- ✅ Fully tested with comprehensive test verification documents

**Vocabulary Session Persistence (BUG-015, BUG-016) - Continued from above:**

**Solution:** Database persistence using PostgreSQL (matching Grammar module pattern)

**Changes Made:**
- Added `FlashcardSession` model - Stores flashcard practice session state (cards, current_index, user_id)
- Added `VocabularyQuiz` model - Stores quiz questions and metadata (questions, quiz_type, user_id)
- Created migration `002_add_vocabulary_sessions.py` - Creates both tables with proper indexes
- Updated 5 API endpoints to use database queries instead of dict lookups:
  - `POST /api/v1/vocabulary/flashcards/start` - Stores session in DB
  - `GET /api/v1/vocabulary/flashcards/{session_id}/current` - Queries session from DB
  - `POST /api/v1/vocabulary/flashcards/{session_id}/answer` - Updates session in DB
  - `POST /api/v1/vocabulary/quiz/generate` - Stores quiz in DB
  - `POST /api/v1/vocabulary/quiz/{quiz_id}/answer` - Queries quiz from DB
- Removed in-memory dictionaries: `flashcard_sessions = {}` and `vocabulary_quizzes = {}`
- Updated test fixtures to mock database models instead of dictionaries
- Sessions stored as JSON strings in `cards_data` and `questions_data` TEXT columns

**Benefits:**
- ✅ Works with multiple workers (`uvicorn --workers 3+`)
- ✅ Sessions persist across server restarts
- ✅ No more 404 "Session not found" or "Quiz not found" errors
- ✅ Matches proven Grammar module architecture
- ✅ Fully tested with database-backed fixtures

**Deployment Documentation:**
- `/docs/DEPLOYMENT_GUIDE.md` - Complete deployment walkthrough
- `/backend/deploy/DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `/backend/deploy/README.md` - Deploy directory overview
- `/backend/deploy/setup-server.sh` - Automated server setup
- `/backend/deploy/german-learning.service` - Systemd service file
- `/backend/deploy/nginx-german-learning.conf` - Nginx configuration
- `/backend/deploy/.env.production` - Production environment template

**Vocabulary Module Database Migration (Fix #17-18):**

The Vocabulary module required extensive database schema updates to align with the SQLAlchemy models. Migration `001_update_vocabulary_schema.py` performs:

**Vocabulary Table Updates:**
- Renamed columns: word_de→word, word_it→translation_it, difficulty_level→difficulty, context_category→category
- Renamed columns: example_sentence_de→example_de, example_sentence_it→example_it, notes→usage_notes
- Added columns: definition_de, pronunciation, synonyms, antonyms, is_idiom, is_compound, is_separable_verb

**User Vocabulary Progress Table Transformation:**
- Renamed table: user_vocabulary → user_vocabulary_progress
- Renamed columns: vocabulary_id→word_id, familiarity_score→confidence_score, times_encountered→times_reviewed
- Renamed columns: last_encountered→last_reviewed, first_encountered→first_reviewed, notes→personal_note
- Added columns: mastery_level, current_streak, ease_factor, interval_days

**New Tables Created:**
- `user_vocabulary_lists` - Personal vocabulary lists with is_public field
- `vocabulary_list_words` - Many-to-many association for list membership
- `vocabulary_reviews` - Review history tracking with confidence ratings

**API Fixes (backend/app/api/v1/vocabulary.py):**
- Fixed all 8 word dictionary constructions to convert integer booleans (0/1) to Python booleans
- Calculate accuracy_rate dynamically: `(times_correct / times_reviewed * 100)`
- Initialize all UserVocabularyProgress fields explicitly (times_incorrect, current_streak, confidence_score)
- Track streaks correctly (increment on correct, reset on incorrect)
- Fixed VocabularyReview field: confidence_level→confidence_rating
- Convert boolean to integer for was_correct field

**Migration Command:**
```bash
alembic upgrade 001_update_vocabulary_schema
```

This migration preserves all existing vocabulary and user progress data while updating the schema to match the models.

### API Structure (74 Total Endpoints)

**Authentication (3 endpoints):**
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- GET `/api/v1/auth/me`

**Conversations (4 endpoints):**
- POST `/api/sessions/start`
- POST `/api/sessions/{id}/message`
- POST `/api/sessions/{id}/end`
- GET `/api/sessions/history`

**Contexts (5 endpoints):**
- GET `/api/contexts` - List contexts with filters
- GET `/api/contexts/{id}` - Get context with usage stats
- POST `/api/contexts` - Create custom context
- PUT `/api/contexts/{id}` - Update context
- DELETE `/api/contexts/{id}` - Deactivate context

**Grammar (14 endpoints):**
- GET `/api/grammar/topics` - List all topics
- GET `/api/grammar/topics/{id}` - Get topic details
- POST `/api/grammar/practice/start` - Start practice session
- GET `/api/grammar/practice/{session_id}/next` - Get next exercise
- POST `/api/grammar/practice/{session_id}/answer` - Submit answer
- POST `/api/grammar/practice/{session_id}/end` - End session
- GET `/api/grammar/progress` - Get overall progress
- GET `/api/grammar/progress/topic/{topic_id}` - Topic-specific progress
- POST `/api/grammar/generate-exercises` - AI-generate exercises
- GET `/api/grammar/categories` - List categories
- GET `/api/grammar/recommendations` - Get practice recommendations
- GET `/api/grammar/review-queue` - Get due topics
- POST `/api/grammar/diagnostic/start` - Start diagnostic test
- POST `/api/grammar/diagnostic/complete` - Complete diagnostic

**Vocabulary (26 endpoints):**
- GET `/api/v1/vocabulary/words` - List words with filters
- GET `/api/v1/vocabulary/words/{id}` - Get word with progress
- POST `/api/v1/vocabulary/words` - Create word
- POST `/api/v1/vocabulary/flashcards/start` - Start flashcard session
- POST `/api/v1/vocabulary/flashcards/{session_id}/answer` - Submit answer
- GET `/api/v1/vocabulary/flashcards/{session_id}/current` - Get current card
- POST `/api/v1/vocabulary/lists` - Create vocabulary list
- GET `/api/v1/vocabulary/lists` - Get all lists
- GET `/api/v1/vocabulary/lists/{id}` - Get list with words
- POST `/api/v1/vocabulary/lists/{id}/words` - Add word to list
- DELETE `/api/v1/vocabulary/lists/{id}/words/{word_id}` - Remove word
- DELETE `/api/v1/vocabulary/lists/{id}` - Delete list
- POST `/api/v1/vocabulary/quiz/generate` - Generate quiz
- POST `/api/v1/vocabulary/quiz/{quiz_id}/answer` - Submit quiz answer
- GET `/api/v1/vocabulary/progress/summary` - Get progress summary
- GET `/api/v1/vocabulary/progress/review-queue` - Get review queue
- POST `/api/v1/vocabulary/analyze` - AI word analysis
- POST `/api/v1/vocabulary/detect` - Detect vocabulary from text
- POST `/api/v1/vocabulary/recommend` - Get word recommendations

**Analytics (14 endpoints):**
- GET `/api/v1/analytics/progress` - Overall progress
- GET `/api/v1/analytics/progress/comparison` - Compare periods
- GET `/api/v1/analytics/errors` - Error pattern analysis
- POST `/api/v1/analytics/snapshots` - Create snapshot
- GET `/api/v1/analytics/snapshots` - Get snapshots
- GET `/api/v1/analytics/achievements` - List achievements
- GET `/api/v1/analytics/achievements/earned` - User's achievements
- GET `/api/v1/analytics/achievements/progress` - Achievement progress
- POST `/api/v1/analytics/achievements/{id}/showcase` - Showcase achievement
- GET `/api/v1/analytics/stats` - User statistics
- POST `/api/v1/analytics/stats/refresh` - Refresh stats
- GET `/api/v1/analytics/leaderboard/{type}` - Leaderboard rankings
- GET `/api/v1/analytics/heatmap/activity` - Activity heatmap (365 days)
- GET `/api/v1/analytics/heatmap/grammar` - Grammar mastery heatmap

**Integration (3 endpoints):**
- GET `/api/v1/integration/session-analysis/{session_id}` - Analyze conversation with recommendations
- GET `/api/v1/integration/learning-path` - Personalized learning path
- GET `/api/v1/integration/dashboard` - Unified dashboard data

**Health (2 endpoints):**
- GET `/` - Root endpoint
- GET `/api/health` - Health check

### Database Schema (20 Tables)

**Core Tables (4):**
- `users` - User accounts with authentication
- `contexts` - Conversation scenarios (12+ default)
- `sessions` - Conversation practice sessions
- `messages` - Individual conversation messages

**Grammar Module (6 tables):**
- `grammar_topics` - 50+ topics
- `grammar_exercises` - 200+ manual exercises
- `user_grammar_progress` - Mastery tracking with spaced repetition
- `grammar_sessions` - Practice sessions (database-persisted)
- `grammar_exercise_attempts` - Individual answers
- `diagnostic_tests` - Assessment results

**Vocabulary Module (7 tables):**
- `vocabulary` - 150+ words (foundation for 1000+)
- `user_vocabulary_progress` - Mastery tracking (6 levels)
- `user_vocabulary_lists` - Personal lists
- `vocabulary_list_words` - List membership
- `vocabulary_reviews` - Review history
- `flashcard_sessions` - Flashcard practice sessions (database-persisted, multi-worker safe) **NEW**
- `vocabulary_quizzes` - Quiz sessions (database-persisted, multi-worker safe) **NEW**

**Analytics Module (4 tables):**
- `achievements` - 31 achievement definitions
- `user_achievements` - Earned achievements with progress
- `user_stats` - Aggregate statistics for leaderboards
- `progress_snapshots` - Historical progress tracking

### Project Structure
```
myGermanAITeacher/
├── backend/
│   ├── app/
│   │   ├── main.py                           # FastAPI app with 74 endpoints
│   │   ├── config.py                         # Settings
│   │   ├── database.py                       # SQLAlchemy setup
│   │   ├── models/                           # 20 database models
│   │   │   ├── user.py                       # User model
│   │   │   ├── context.py                    # Context model
│   │   │   ├── session.py                    # Session, Message models
│   │   │   ├── grammar.py                    # 6 grammar models
│   │   │   ├── vocabulary.py                 # 7 vocabulary models (includes FlashcardSession, VocabularyQuiz)
│   │   │   └── achievement.py                # 4 analytics models
│   │   ├── schemas/                          # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── context.py
│   │   │   ├── session.py
│   │   │   ├── grammar.py                    # 20+ grammar schemas
│   │   │   ├── vocabulary.py                 # 22 vocabulary schemas
│   │   │   └── analytics.py                  # 30+ analytics schemas
│   │   ├── api/v1/                           # API endpoints
│   │   │   ├── auth.py                       # 3 endpoints
│   │   │   ├── sessions.py                   # 4 endpoints
│   │   │   ├── contexts.py                   # 5 endpoints
│   │   │   ├── grammar.py                    # 14 endpoints
│   │   │   ├── vocabulary.py                 # 26 endpoints
│   │   │   ├── analytics.py                  # 14 endpoints
│   │   │   └── integration.py                # 3 endpoints
│   │   ├── services/                         # Business logic
│   │   │   ├── ai_service.py                 # Conversation AI
│   │   │   ├── grammar_ai_service.py         # Exercise generation
│   │   │   ├── vocabulary_ai_service.py      # Word analysis
│   │   │   ├── analytics_service.py          # Progress tracking
│   │   │   └── integration_service.py        # Cross-module workflows
│   │   └── utils/                            # Utilities
│   │       └── auth.py                       # JWT & password hashing
│   ├── scripts/                              # Seed scripts
│   │   ├── seed_contexts.py                  # 12+ contexts
│   │   ├── seed_grammar_data.py              # 50+ topics, 200+ exercises
│   │   ├── seed_vocabulary_data.py           # 150+ words
│   │   └── seed_achievements.py              # 31 achievements
│   ├── tests/                                # 104 tests total
│   │   ├── test_grammar.py                   # 25 tests
│   │   ├── test_vocabulary.py                # 30 tests
│   │   ├── test_analytics.py                 # 18 tests
│   │   ├── test_integration.py               # 11 tests
│   │   └── ... (other test files)
│   ├── alembic/                              # Database migrations
│   ├── requirements.txt                      # Python dependencies
│   └── .env.example                          # Environment template
├── frontend/ (Planned - Phase 7)
├── docs/
├── logs/
└── brd and planning documents/
    ├── german_learning_app_brd.md
    └── plan.md
```

### Key Implementation Highlights

**AI Services:**
- **ConversationAI**: Context-aware conversations with grammar/vocabulary detection
- **GrammarAIService**: Dynamic exercise generation, answer evaluation, error explanations
- **VocabularyAIService**: Word analysis, vocabulary detection, flashcard generation, quiz creation
- **AnalyticsService**: 15+ analysis methods for comprehensive progress tracking
- **IntegrationService**: Cross-module workflows and personalized learning paths

**Spaced Repetition:**
- **Grammar**: 5-level mastery (0.0-5.0), exponential backoff (1→2→4→8→16→30 days)
- **Vocabulary**: 6-level mastery (0-5), SM-2 inspired algorithm, confidence-based intervals

**Gamification:**
- 31 achievements across 4 categories (conversation, grammar, vocabulary, activity)
- 4 tiers: bronze (7), silver (7), gold (10), platinum (7)
- Leaderboard rankings (overall, grammar, vocabulary, streak)
- Progress score (0-100) combining all modules
- Streak tracking with milestone achievements

**Smart Features:**
- Session analysis with grammar/vocabulary recommendations
- Personalized daily plans (75 min: 15 vocab + 30 grammar + 30 conversation)
- Weekly goals (5+ sessions with module distribution)
- Error pattern analysis with recurring mistake detection
- Improvement trend analysis
- Context recommendations (prioritize unpracticed)
- Quick actions for immediate engagement

### Environment Variables (.env)

**Development:**
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/german_learning

# AI Services
ANTHROPIC_API_KEY=sk-ant-...

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=German Learning App
DEBUG=True
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

**Production:**
```bash
# Database
DATABASE_URL=postgresql://german_app_user:strong_password@localhost/german_learning

# AI Services
ANTHROPIC_API_KEY=sk-ant-your-production-key

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=generated-secure-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=German Learning App
DEBUG=False
ENVIRONMENT=production
CORS_ORIGINS=http://your-server-ip,https://your-domain.com
```

**Important Notes:**
- `HOST` and `PORT` are NOT included in .env (not defined in Settings class)
- Uvicorn will use default `--host 0.0.0.0 --port 8000` from systemd service or command line
- Generate SECRET_KEY with: `openssl rand -hex 32`
- Set DEBUG=False in production
- Update CORS_ORIGINS with actual server IP/domain

### Development Commands

**Backend:**
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run migrations
cd backend && alembic upgrade head

# Seed data
python backend/scripts/seed_contexts.py
python backend/scripts/seed_grammar_data.py
python backend/scripts/seed_vocabulary_data.py
python backend/scripts/seed_achievements.py

# Start server
cd backend && uvicorn app.main:app --reload --port 8000

# Run tests (104 tests)
cd backend && pytest tests/ -v
```

**API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Production Deployment Commands

**Quick Deployment (Ubuntu 20.04):**
```bash
# 1. Transfer deployment files to server
scp -r backend/deploy/* user@server-ip:~/deploy/

# 2. Run automated setup script
ssh user@server-ip
cd ~/deploy
chmod +x setup-server.sh
./setup-server.sh

# 3. Transfer application code
cd /opt/german-learning-app
git clone https://github.com/zistan/myGermanAITeacher.git .

# 4. Setup Python environment (Python 3.10)
cd backend
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 5. Configure environment
cp deploy/.env.production .env
nano .env  # Update with actual values
chmod 600 .env

# 6. Run migrations and seed data
alembic upgrade head
python scripts/seed_contexts.py
python scripts/seed_grammar_data.py
python scripts/seed_vocabulary_data.py
python scripts/seed_achievements.py

# 7. Setup systemd service
sudo cp deploy/german-learning.service /etc/systemd/system/
sudo nano /etc/systemd/system/german-learning.service  # Update username
sudo systemctl daemon-reload
sudo systemctl enable german-learning
sudo systemctl start german-learning

# 8. Setup Nginx
sudo cp deploy/nginx-german-learning.conf /etc/nginx/sites-available/german-learning
sudo nano /etc/nginx/sites-available/german-learning  # Update domain
sudo ln -s /etc/nginx/sites-available/german-learning /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# 9. Configure firewall
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

**Service Management:**
```bash
# Check status
sudo systemctl status german-learning

# View logs
sudo journalctl -u german-learning -f

# Restart service
sudo systemctl restart german-learning

# Update application
cd /opt/german-learning-app/backend
git pull origin master
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
sudo systemctl restart german-learning
```

**Deployment Documentation:**
- Full guide: `/docs/DEPLOYMENT_GUIDE.md`
- Checklist: `/backend/deploy/DEPLOYMENT_CHECKLIST.md`
- Deploy README: `/backend/deploy/README.md`

### Testing Coverage
- **Total Tests**: 104 comprehensive tests
- **Coverage**: >80% across all modules
- **Grammar Tests**: 25 tests covering all endpoints and workflows
- **Vocabulary Tests**: 30 tests for flashcards, lists, quizzes, progress
- **Analytics Tests**: 18 tests for achievements, stats, heatmaps
- **Integration Tests**: 11 tests for cross-module workflows
- All tests use mocked AI services for reliability

### Design Principles
1. **User-centric**: Tailored for Igor's business German and grammar mastery goals
2. **Immediate feedback**: Real-time grammar corrections and exercise feedback
3. **Adaptive learning**: Spaced repetition + conversation-triggered practice
4. **Comprehensive tracking**: Progress across all modules with detailed analytics
5. **Context-rich**: Business scenarios aligned with payments/finance domain
6. **Seamless integration**: Smart workflows connecting conversation → grammar → vocabulary

### Success Metrics (Backend Complete ✅)
- ✅ 74 REST API endpoints fully implemented
- ✅ 20 database models with relationships
- ✅ 104 comprehensive tests (>80% coverage)
- ✅ 12+ conversation contexts (6 business, 6 daily)
- ✅ 50+ grammar topics with 200+ exercises
- ✅ 150+ vocabulary words (foundation for 1000+)
- ✅ 31 achievements with gamification
- ✅ Cross-module integration with learning paths
- ✅ All AI services functional (conversation, grammar, vocabulary)
- ✅ Spaced repetition algorithms implemented
- ✅ Error tracking and improvement analysis
- ✅ Multi-worker safe session persistence (database-backed)

### Next Steps: Phase 7 - Frontend Development
- Initialize React 18 + TypeScript + Vite project
- Set up Tailwind CSS and component library
- Implement authentication flow (login/register)
- Build dashboard with unified data view
- Create conversation interface with context selection
- Build grammar practice UI with exercise types
- Create flashcard interface for vocabulary
- Implement progress visualizations (heatmaps, charts)
- Add achievement showcase and leaderboards
- Integrate all 74 backend endpoints

---

**For Claude Code Developers:**

**CRITICAL REQUIREMENTS:**

1. **Testing is MANDATORY**
   - Write tests for ALL code you create
   - Tests must be written alongside the implementation
   - Every service function MUST have corresponding unit tests
   - Every API endpoint MUST have integration tests
   - Test both success and failure paths
   - Mock external dependencies (AI API, database in unit tests)
   - Use pytest for backend, React Testing Library for frontend
   - Aim for >80% code coverage minimum

2. **Git Commits are MANDATORY**
   - Commit ALL changes to the Git repository
   - Commit after completing each logical unit of work
   - Write clear, descriptive commit messages
   - Always commit AND push to remote repository
   - Include both implementation AND test files in commits

**Development Workflow:**
1. Write code for feature/function
2. Write tests for the code (unit + integration as applicable)
3. Run tests and ensure they pass
4. Commit code + tests to Git with descriptive message
5. Push to remote repository
6. Move to next task

**Current Status:**
- ✅ **Backend**: Fully implemented with 74 endpoints, 104 tests, all core features
- ✅ **Deployment**: Complete on Ubuntu 20.04 server with Python 3.10
- 🚀 **Frontend**: 60% complete (5 of 8 phases done)
  - ✅ Phase 0-4: Setup, Auth, Dashboard, Grammar, Vocabulary modules
  - ⏳ Phase 5-7: Conversation, Analytics, Learning Path (pending)
- 📊 **Progress**: 6/10 backend phases + 5/8 frontend phases complete

---

## Known Issues & Solutions

### All Production Issues (Resolved ✅)

All 21 production deployment and testing issues have been identified and fixed during Phase 6.5 and Phase 7. The application is now fully functional on the production server and frontend.

**Key Fixes:**
- ✅ Authentication (bcrypt, JWT)
- ✅ API endpoints (session history, grammar practice)
- ✅ AI model (upgraded to Claude Sonnet 4.5)
- ✅ Database field mappings (all models aligned)
- ✅ Schema validation (metadata conflicts, field types)
- ✅ Spaced repetition (mastery levels, progress tracking)
- ✅ Multi-worker session persistence (BUG-015, BUG-016 fixed)
- ✅ Frontend grammar practice loading (BUG-020, BUG-021 fixed)

See "Production Fixes Applied" section above for complete list of all 21 fixes.

### Technical Notes

**Python Version:**
- **Recommended**: Python 3.10 or 3.11
- **Tested**: Python 3.10 on Ubuntu 20.04 LTS
- **Environment**: HOST and PORT handled by systemd/uvicorn (not in .env)

**Claude AI Model:**
- **Current**: claude-sonnet-4-5 (auto-updating alias)
- **Alternative**: claude-sonnet-4-5-20250929 (fixed snapshot)
- **Pricing**: $3/M input tokens, $15/M output tokens

**Database:**
- **Reserved Keywords**: All metadata columns use Column("metadata", ...) syntax
- **Field Naming**: Model attributes use full names (e.g., total_exercises_attempted)
- **Mastery Levels**: Stored as float 0.0-1.0, converted to strings in schemas

---

Last Updated: 2026-01-20
Project Version: 1.0 (Phase 7 - Frontend Development In Progress - 60% Complete)
Next Phase: Phase 7.5 - Conversation Practice Module

**Recent Changes (2026-01-20):**
- **Frontend Bug Fixes:**
  - Fixed BUG-020: Grammar practice stuck on loading (conditional difficulty parameter)
  - Fixed BUG-021: Second grammar session stuck loading (cleared completed session data)
  - Both fixes improve multi-session UX with better error handling

**Recent Changes (2026-01-19):**
- **Backend Bug Fixes:**
  - Fixed BUG-015 and BUG-016: Replaced in-memory session storage with database persistence
  - Added 2 new database tables: flashcard_sessions, vocabulary_quizzes
  - Created migration 002_add_vocabulary_sessions.py
  - All vocabulary sessions now persist across multiple workers and server restarts
