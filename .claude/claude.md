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
- Anthropic Claude 3.5 Sonnet (AI)

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
- FastAPI backend with 14 database models
- JWT authentication with bcrypt
- PostgreSQL database setup
- Alembic migrations
- All core models: User, Context, Session, Message, Grammar (6 tables), Vocabulary (4 tables), Achievement (4 tables)

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

**Production Fixes Applied:**
1. **Python 3.11 Availability** - Added deadsnakes PPA for Python 3.10/3.11 installation on Ubuntu 20.04
2. **SQLAlchemy Reserved Keywords** - Fixed `metadata` column conflicts in models:
   - Session.metadata → session_metadata
   - ConversationTurn.metadata → turn_metadata
   - GrammarExercise.metadata → exercise_metadata
   - GrammarSession.metadata → grammar_metadata
3. **Model Import Issues** - Added missing Achievement model imports (UserAchievement, UserStats, Achievement)
4. **Duplicate Model Definitions** - Removed duplicate ProgressSnapshot from progress.py (kept version in achievement.py)
5. **PostgreSQL Configuration** - Configured pg_hba.conf for local md5 authentication

**Deployment Documentation:**
- `/docs/DEPLOYMENT_GUIDE.md` - Complete deployment walkthrough
- `/backend/deploy/DEPLOYMENT_CHECKLIST.md` - Step-by-step checklist
- `/backend/deploy/README.md` - Deploy directory overview
- `/backend/deploy/setup-server.sh` - Automated server setup
- `/backend/deploy/german-learning.service` - Systemd service file
- `/backend/deploy/nginx-german-learning.conf` - Nginx configuration
- `/backend/deploy/.env.production` - Production environment template

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

### Database Schema (18 Tables)

**Core Tables (4):**
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
- `vocabulary_words` - 150+ words (foundation for 1000+)
- `user_vocabulary_progress` - Mastery tracking (6 levels)
- `user_vocabulary_lists` - Personal lists
- `vocabulary_list_words` - List membership
- `vocabulary_reviews` - Review history

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
│   │   ├── models/                           # 18 database models
│   │   │   ├── user.py                       # User model
│   │   │   ├── context.py                    # Context model
│   │   │   ├── session.py                    # Session, Message models
│   │   │   ├── grammar.py                    # 6 grammar models
│   │   │   ├── vocabulary.py                 # 4 vocabulary models
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
- ✅ 18 database models with relationships
- ✅ 104 comprehensive tests (>80% coverage)
- ✅ 12+ conversation contexts (6 business, 6 daily)
- ✅ 50+ grammar topics with 200+ exercises
- ✅ 150+ vocabulary words (foundation for 1000+)
- ✅ 31 achievements with gamification
- ✅ Cross-module integration with learning paths
- ✅ All AI services functional (conversation, grammar, vocabulary)
- ✅ Spaced repetition algorithms implemented
- ✅ Error tracking and improvement analysis

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
- 🚀 **Deployment**: In progress on Ubuntu 20.04 server with Python 3.10
- 🔄 **Frontend**: Not started (Phase 7)
- 📊 **Progress**: 6/10 phases complete (backend complete, deployment in progress, frontend pending)

---

## Known Issues & Solutions

### Deployment Issues (Resolved)
1. **Python 3.11 not available on Ubuntu 20.04**
   - Solution: Use Python 3.10 (fully compatible) or add deadsnakes PPA

2. **SQLAlchemy "metadata" reserved keyword error**
   - Solution: Renamed model attributes with Column("metadata", ...) syntax
   - Affects: Session, ConversationTurn, GrammarExercise, GrammarSession models

3. **Missing Achievement model imports**
   - Solution: Added imports in models/__init__.py

4. **Duplicate ProgressSnapshot model**
   - Solution: Removed from progress.py, kept in achievement.py

5. **PostgreSQL authentication failed**
   - Solution: Configure pg_hba.conf with md5 authentication for localhost

### Python Version Compatibility
- **Recommended**: Python 3.10 or 3.11
- **Tested**: Python 3.10 on Ubuntu 20.04 LTS
- **Not Required**: HOST and PORT in .env file (handled by systemd/uvicorn)

---

Last Updated: 2026-01-17
Project Version: 1.0 (Phase 6 Complete - Backend Implemented, Phase 6.5 Deployment In Progress)
