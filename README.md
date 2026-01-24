# German Learning Application (myGermanAITeacher)

**An AI-powered German language learning application for advanced learners (B2/C1 level)**

**Last Updated:** 2026-01-24
**Project Status:** 🚀 94% Complete (Phase 7 of 8)
**Live Deployment:** http://192.168.178.100:8000 (Backend) | http://192.168.178.100:5173 (Frontend)

---

## Overview

A comprehensive German language learning platform designed specifically for advanced learners (B2/C1 level) working in business environments. The application combines AI-powered conversation practice, systematic grammar drilling, spaced-repetition vocabulary learning, and detailed progress analytics.

**Built for:** Igor - Italian native speaker, fluent in English, working in payments/finance in Switzerland

---

## Features

### 🤖 AI Conversation Practice
- **12+ Pre-configured Contexts** - Business meetings, client calls, presentations, casual conversations, travel scenarios
- **Real-time Chat with Claude Sonnet 4.5** - Natural, context-aware conversations with instant grammar feedback
- **Grammar Feedback Panel** - Real-time corrections grouped by severity (high/medium/low)
- **Vocabulary Highlighting** - Inline tooltips showing translations and difficulty levels
- **Session Analysis** - Detailed post-session recommendations for grammar and vocabulary practice
- **German Keyboard Helper** - Quick input for ä, ö, ü, ß with keyboard shortcuts

### 📚 Grammar Learning System
- **50+ Grammar Topics** - Comprehensive coverage from A1 to C2 (Articles, Cases, Tenses, Subjunctive, etc.)
- **200+ Manual Exercises** - 5 exercise types: fill_blank, multiple_choice, translation, error_correction, sentence_building
- **AI-Generated Exercises** - Dynamic exercise generation using Claude AI
- **Spaced Repetition Algorithm** - Exponential backoff (1→2→4→8→16→30 days) based on mastery level
- **Diagnostic Tests** - Assess current level and identify weak areas
- **Interactive Practice Sessions** - With pause/resume, focus mode, bookmarking, notes, auto-advance
- **Text Diff Visualization** - Character-by-character comparison for translation exercises
- **Keyboard Shortcuts** - Full keyboard navigation (Enter=submit, Space=next, Esc=end, F=focus, etc.)

### 📖 Vocabulary Management
- **150+ German Words** - Business and daily life vocabulary (foundation for 1000+ expansion)
- **Flashcard System** - 5-point rating (Again/Hard/Good/Easy/Perfect) with spaced repetition
- **Personal Vocabulary Lists** - Create custom lists, organize by theme or difficulty
- **Vocabulary Quizzes** - Multiple question types (multiple_choice, fill_blank, matching)
- **Progress Tracking** - 6 mastery levels with confidence scoring
- **AI-Powered Features** - Word analysis, vocabulary detection, recommendations
- **CEFR Level Distribution** - Track vocabulary across difficulty levels (A1-C2)

### 📊 Progress Analytics
- **Overall Progress Score** - 0-100 score combining all modules
- **31 Achievements** - 4 tiers (bronze/silver/gold/platinum), 5,825 total points
- **Activity Heatmap** - GitHub-style 365-day visualization
- **Grammar Mastery Heatmap** - Visual topic mastery by category
- **Leaderboards** - 4 rankings (overall, grammar, vocabulary, streak)
- **Error Pattern Analysis** - Recurring mistakes detection with AI recommendations
- **Progress Snapshots** - Daily/weekly/monthly historical tracking
- **Streak Tracking** - Current and longest streaks with milestone celebrations

### 🎯 Personalized Learning Path
- **Daily Study Plan** - AI-generated 75-minute daily breakdown (15 vocab + 30 grammar + 30 conversation)
- **Weekly Goals** - Session targets with module distribution and milestones
- **Focus Areas** - Priority-based weak spots (critical/high/medium/low)
- **Context Recommendations** - Suggested conversation topics based on practice history
- **Motivation Messages** - Personalized encouragement from AI

---

## Technology Stack

### Backend
- **Python 3.10** - Core language
- **FastAPI** - Modern, fast web framework
- **PostgreSQL 12+** - Relational database (15+ recommended)
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migrations
- **Anthropic Claude Sonnet 4.5** - AI conversation and generation
- **bcrypt** - Password hashing
- **JWT** - Authentication tokens
- **Pydantic** - Data validation

### Frontend
- **React 18** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Lightning-fast build tool
- **Tailwind CSS v3** - Utility-first styling
- **Zustand** - Lightweight state management
- **Axios** - HTTP client with interceptors
- **Recharts** - Data visualization
- **Headless UI** - Accessible components
- **React Router v6** - Client-side routing

### Deployment
- **Ubuntu 20.04 LTS** - Production server
- **Uvicorn** - ASGI server (multi-worker support)
- **Nginx** - Reverse proxy
- **Systemd** - Service management
- **PostgreSQL** - Production database

---

## Project Structure

```
myGermanAITeacher/
├── backend/                           # Python FastAPI backend
│   ├── app/
│   │   ├── api/v1/                   # API endpoints (74 total)
│   │   │   ├── auth.py               # 3 endpoints
│   │   │   ├── sessions.py           # 4 endpoints
│   │   │   ├── contexts.py           # 5 endpoints
│   │   │   ├── grammar.py            # 14 endpoints
│   │   │   ├── vocabulary.py         # 26 endpoints
│   │   │   ├── analytics.py          # 14 endpoints
│   │   │   └── integration.py        # 3 endpoints
│   │   ├── models/                   # 20 SQLAlchemy models
│   │   ├── schemas/                  # Pydantic validation schemas
│   │   ├── services/                 # Business logic (AI services)
│   │   ├── utils/                    # Utilities (auth, helpers)
│   │   ├── main.py                   # FastAPI application
│   │   ├── config.py                 # Settings management
│   │   └── database.py               # Database setup
│   ├── alembic/                      # Database migrations (2 migrations)
│   ├── tests/                        # 104 tests (>80% coverage)
│   ├── scripts/                      # Seed scripts (contexts, grammar, vocabulary, achievements)
│   ├── deploy/                       # Deployment scripts and configs
│   └── requirements.txt              # Python dependencies
│
├── frontend/                         # React TypeScript frontend
│   ├── src/
│   │   ├── api/                      # API integration (7 services, 7 type files)
│   │   ├── components/               # 81 React components
│   │   │   ├── common/               # 12 shared UI components
│   │   │   ├── grammar/              # 7 grammar components
│   │   │   ├── vocabulary/           # 26 vocabulary components
│   │   │   ├── conversation/         # 13 conversation components
│   │   │   ├── analytics/            # 10 analytics components
│   │   │   ├── dashboard/            # 6 dashboard widgets
│   │   │   ├── learning-path/        # 4 learning path components
│   │   │   └── layout/               # 4 layout components
│   │   ├── pages/                    # 26 page components
│   │   ├── store/                    # 6 Zustand stores
│   │   ├── hooks/                    # 3 custom React hooks
│   │   ├── utils/                    # Utility functions
│   │   ├── App.tsx                   # Root component with routing
│   │   └── main.tsx                  # Application entry point
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                             # Comprehensive documentation
│   ├── CODEMAPS/                     # Architecture documentation (6 codemaps)
│   ├── GUIDES/                       # User guides (setup, deployment, troubleshooting)
│   └── testing/                      # Test reports and bug tracking
│
└── brd and planning documents/       # Requirements and planning
    ├── german_learning_app_brd.md
    └── plan.md
```

---

## Quick Start

### Prerequisites
- **Python 3.10 or 3.11**
- **PostgreSQL 12+** (15+ recommended)
- **Node.js 18+** (for frontend)
- **Git**
- **Anthropic API Key** (Claude access)

### Backend Setup (5 minutes)

```bash
# 1. Clone repository
git clone <repository-url>
cd myGermanAITeacher/backend

# 2. Create virtual environment (Python 3.10)
python3.10 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
nano .env  # Add DATABASE_URL, ANTHROPIC_API_KEY, SECRET_KEY

# 5. Create database
createdb german_learning

# 6. Run migrations
alembic upgrade head

# 7. Seed initial data
python scripts/seed_contexts.py
python scripts/seed_grammar_data.py
python scripts/seed_vocabulary_data.py
python scripts/seed_achievements.py

# 8. Start server
uvicorn app.main:app --reload --port 8000
```

**API Documentation:** http://localhost:8000/docs

### Frontend Setup (3 minutes)

```bash
cd frontend

# 1. Install dependencies
npm install

# 2. Configure environment
cp .env.example .env
nano .env  # Set VITE_API_URL=http://localhost:8000

# 3. Start development server
npm run dev
```

**Frontend:** http://localhost:5173

### Running Tests

```bash
# Backend tests (104 tests, >80% coverage)
cd backend
pytest -v

# With coverage report
pytest --cov=app --cov-report=html
```

---

## API Endpoints (74 Total)

### Authentication (3)
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login with OAuth2 password flow
- `GET /api/v1/auth/me` - Get current user

### Conversations (4)
- `POST /api/sessions/start` - Start conversation session
- `POST /api/sessions/{id}/message` - Send message
- `POST /api/sessions/{id}/end` - End session
- `GET /api/sessions/history` - List past sessions

### Contexts (5)
- `GET /api/contexts` - List contexts with filters
- `GET /api/contexts/{id}` - Get context details
- `POST /api/contexts` - Create custom context
- `PUT /api/contexts/{id}` - Update context
- `DELETE /api/contexts/{id}` - Deactivate context

### Grammar (14)
- `GET /api/grammar/topics` - List all topics
- `GET /api/grammar/topics/{id}` - Get topic details
- `POST /api/grammar/practice/start` - Start practice session
- `GET /api/grammar/practice/{id}/next` - Get next exercise
- `POST /api/grammar/practice/{id}/answer` - Submit answer
- `POST /api/grammar/practice/{id}/end` - End session
- `GET /api/grammar/progress` - Overall progress
- `GET /api/grammar/progress/topic/{id}` - Topic progress
- `GET /api/grammar/categories` - List categories
- `POST /api/grammar/generate-exercises` - AI exercise generation
- `POST /api/grammar/diagnostic/start` - Start diagnostic test
- `POST /api/grammar/diagnostic/complete` - Complete diagnostic
- `GET /api/grammar/review-queue` - Get due topics
- (+ 1 more)

### Vocabulary (26)
- `GET /api/v1/vocabulary/words` - List words with filters
- `GET /api/v1/vocabulary/words/{id}` - Get word details
- `POST /api/v1/vocabulary/words` - Create word
- `POST /api/v1/vocabulary/flashcards/start` - Start flashcard session
- `POST /api/v1/vocabulary/flashcards/{id}/answer` - Submit answer
- `GET /api/v1/vocabulary/flashcards/{id}/current` - Get current card
- `POST /api/v1/vocabulary/lists` - Create list
- `GET /api/v1/vocabulary/lists` - Get all lists
- `GET /api/v1/vocabulary/lists/{id}` - Get list details
- `POST /api/v1/vocabulary/lists/{id}/words` - Add word to list
- `DELETE /api/v1/vocabulary/lists/{id}/words/{word_id}` - Remove word
- `POST /api/v1/vocabulary/quiz/generate` - Generate quiz
- `POST /api/v1/vocabulary/quiz/{id}/answer` - Submit quiz answer
- `GET /api/v1/vocabulary/progress/summary` - Progress summary
- `GET /api/v1/vocabulary/progress/review-queue` - Review queue
- `POST /api/v1/vocabulary/analyze` - AI word analysis
- `POST /api/v1/vocabulary/detect` - Detect vocabulary from text
- `POST /api/v1/vocabulary/recommend` - Get recommendations
- (+ 8 more)

### Analytics (14)
- `GET /api/v1/analytics/progress` - Overall progress
- `GET /api/v1/analytics/progress/comparison` - Compare periods
- `GET /api/v1/analytics/errors` - Error pattern analysis
- `POST /api/v1/analytics/snapshots` - Create snapshot
- `GET /api/v1/analytics/snapshots` - Get snapshots
- `GET /api/v1/analytics/achievements` - List achievements
- `GET /api/v1/analytics/achievements/earned` - User achievements
- `GET /api/v1/analytics/achievements/progress` - Achievement progress
- `POST /api/v1/analytics/achievements/{id}/showcase` - Showcase achievement
- `GET /api/v1/analytics/stats` - User statistics
- `POST /api/v1/analytics/stats/refresh` - Refresh stats
- `GET /api/v1/analytics/leaderboard/{type}` - Leaderboard rankings
- `GET /api/v1/analytics/heatmap/activity` - Activity heatmap
- `GET /api/v1/analytics/heatmap/grammar` - Grammar mastery heatmap

### Integration (3)
- `GET /api/v1/integration/dashboard` - Unified dashboard data
- `GET /api/v1/integration/learning-path` - Personalized learning path
- `GET /api/v1/integration/session-analysis/{id}` - Analyze conversation session

### Health (2)
- `GET /` - API information
- `GET /api/health` - Health check

---

## Database Schema (20 Models)

### Core Tables (4)
- **users** - User accounts with authentication
- **contexts** - Conversation scenarios (12+ default)
- **sessions** - Conversation practice sessions
- **messages** - Individual conversation messages

### Grammar Module (6)
- **grammar_topics** - 50+ topics (A1-C2)
- **grammar_exercises** - 200+ manual exercises
- **user_grammar_progress** - Mastery tracking with spaced repetition
- **grammar_sessions** - Practice sessions (database-persisted)
- **grammar_exercise_attempts** - Individual exercise answers
- **diagnostic_tests** - Assessment results

### Vocabulary Module (7)
- **vocabulary** - 150+ words (foundation for 1000+)
- **user_vocabulary_progress** - Mastery tracking (6 levels)
- **user_vocabulary_lists** - Personal vocabulary lists
- **vocabulary_list_words** - List membership (many-to-many)
- **vocabulary_reviews** - Review history with confidence ratings
- **flashcard_sessions** - Flashcard practice sessions (database-persisted)
- **vocabulary_quizzes** - Quiz sessions (database-persisted)

### Analytics Module (4)
- **achievements** - 31 achievement definitions (4 tiers)
- **user_achievements** - Earned achievements with progress
- **user_stats** - Aggregate statistics for leaderboards
- **progress_snapshots** - Historical progress tracking

---

## Development Status

### ✅ Completed Phases (7 of 8 - 94%)

#### Phase 0: Project Setup (Week 1) - Complete ✅
- Vite + React 18 + TypeScript initialized
- Tailwind CSS v3 configured
- 10 common components (Button, Card, Loading, Badge, etc.)
- ESLint + Prettier + React Router v6

#### Phase 1: Authentication (Week 2) - Complete ✅
- JWT authentication with bcrypt
- Login/Register pages with validation
- Protected routes with auth guards
- OAuth2 password flow

#### Phase 2: Dashboard & Layout (Week 3) - Complete ✅
- Unified dashboard with 6 widgets
- Sidebar navigation with 7 sections
- Header with user menu
- Mobile responsive layout

#### Phase 3: Grammar Module (Weeks 4-5) - Complete ✅
- 50+ topics, 200+ exercises, 5 exercise types
- Practice session with 12 UX improvements
- Progress dashboard with CEFR breakdown
- Review queue with spaced repetition
- Results page with recommendations

#### Phase 4: Vocabulary Module (Week 6) - Complete ✅
- 150+ words across 6 categories
- Flashcard system with 5-point rating
- Personal vocabulary lists
- Quiz system (3 question types)
- Progress dashboard with charts

#### Phase 5: Conversation Practice (Week 7) - Complete ✅
- 12+ pre-configured contexts
- Real-time chat with Claude Sonnet 4.5
- German keyboard helper (ä, ö, ü, ß)
- Grammar feedback panel
- Vocabulary highlighting
- Session history and analysis

#### Phase 6: Analytics & Progress (Week 8) - Complete ✅
- Progress overview with trend comparison
- 31 achievements with showcase feature
- Activity heatmap (365 days, GitHub-style)
- Grammar mastery heatmap
- 4 leaderboards (overall, grammar, vocabulary, streak)
- Error analysis with AI recommendations

#### Phase 7: Learning Path (Week 9) - Complete ✅
- Personalized daily plan (75-minute breakdown)
- Focus areas with priority coding
- Weekly goals with milestones
- Context recommendations
- Motivation messages

### ⏳ Remaining Phase (1 of 8 - 6%)

#### Phase 8: Testing & Documentation (Week 10) - Not Started
- Unit tests for utilities and hooks (>90% coverage)
- Component tests with React Testing Library (75% coverage)
- Integration tests with MSW (15%)
- E2E tests with Playwright/Cypress (5%)
- Update README, CONTRIBUTING, API_INTEGRATION docs

---

## Production Deployment

**Server:** Ubuntu 20.04 LTS
**Backend URL:** http://192.168.178.100:8000
**Frontend URL:** http://192.168.178.100:5173
**API Docs:** http://192.168.178.100:8000/docs

### Deployment Resources
- **[Deployment Guide](docs/GUIDES/deployment/DEPLOYMENT_GUIDE.md)** - Complete walkthrough
- **[Deployment Checklist](docs/GUIDES/deployment/DEPLOYMENT_CHECKLIST.md)** - Step-by-step tasks
- **[Ubuntu Quickstart](docs/GUIDES/setup/QUICKSTART_UBUNTU.md)** - Quick setup guide

### Key Fixes Applied
- ✅ Multi-worker session persistence (BUG-015, BUG-016)
- ✅ Frontend grammar practice loading (BUG-020, BUG-021)
- ✅ Authentication with bcrypt 4.2.0 compatibility
- ✅ JWT specification compliance (RFC 7519)
- ✅ Database field mappings (all 20 models aligned)
- ✅ Vocabulary schema migration (comprehensive update)
- ✅ Claude Sonnet 4.5 integration

---

## Documentation

### Architecture Documentation
- **[CODEMAPS](docs/CODEMAPS/)** - System architecture and code structure
  - [Frontend Architecture](docs/CODEMAPS/frontend.md)
  - [Frontend Components](docs/CODEMAPS/frontend-components.md)
  - [Frontend State Management](docs/CODEMAPS/frontend-state.md)
  - [Backend Architecture](docs/CODEMAPS/backend.md)
  - [Backend Database](docs/CODEMAPS/backend-database.md)
  - [Backend API](docs/CODEMAPS/backend-api.md)

### User Guides
- **[Setup Guides](docs/GUIDES/setup/)** - Installation instructions
- **[Deployment Guides](docs/GUIDES/deployment/)** - Production deployment
- **[Troubleshooting](docs/GUIDES/troubleshooting/)** - Common issues
- **[Content Expansion](docs/GUIDES/content/)** - Adding vocabulary and grammar

### Testing Documentation
- **[Backend Testing](docs/testing/backend/)** - 104 tests, bug reports
- **[Frontend Testing](docs/testing/frontend/)** - Manual test plans, bug tracking

---

## Development Workflow

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Revert last migration
alembic downgrade -1

# View history
alembic history
```

### Code Quality

```bash
# Backend
black app/ tests/           # Format code
flake8 app/ tests/          # Lint
mypy app/                   # Type checking
pytest -v                   # Run tests

# Frontend
npm run lint                # ESLint
npm run format              # Prettier
npm run type-check          # TypeScript
npm run test                # Vitest
```

---

## Contributing

This is a personal learning project developed by Igor for mastering German language skills in a business context. See `.claude/CLAUDE.md` for AI agent development guidelines.

### Key Principles
1. **User-centric** - Tailored for advanced learners in business environments
2. **Immediate feedback** - Real-time corrections and explanations
3. **Adaptive learning** - Spaced repetition based on performance
4. **Comprehensive tracking** - Detailed analytics across all modules
5. **Context-rich** - Business scenarios aligned with payments/finance

---

## License

Private project - All rights reserved

---

## Contact

**Igor** - German language learner and developer
**Project Goal:** Achieve C1 fluency in business German
**Focus Areas:** Payments/Finance vocabulary, Grammar mastery, Conversational confidence

---

**For documentation updates, see:** [Documentation README](docs/README.md)
**For architecture details, see:** [Codemaps](docs/CODEMAPS/)
**For deployment help, see:** [Deployment Guide](docs/GUIDES/deployment/DEPLOYMENT_GUIDE.md)
