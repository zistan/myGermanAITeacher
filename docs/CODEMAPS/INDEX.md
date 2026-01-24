# Architecture Overview - German Learning Application

**Last Updated:** 2026-01-24
**Project Status:** 94% Complete (Phase 7 of 8)
**Backend:** FastAPI + PostgreSQL | **Frontend:** React 18 + TypeScript

---

## System Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                         User (Browser)                                │
│                    http://192.168.178.100:5173                       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼─────────────────────────────────────────┐
│                    Frontend (React 18 + TypeScript)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────────┐  │
│  │ 26 Pages     │  │ 81 Components│  │ 6 Zustand Stores          │  │
│  │ (React       │→ │ (Common +    │→ │ (State Management)        │  │
│  │  Router)     │  │  Feature)    │  │                           │  │
│  └──────────────┘  └──────────────┘  └──────────┬────────────────┘  │
│                                                   │                   │
│  ┌────────────────────────────────────────────────▼────────────────┐ │
│  │             7 API Services (Axios Client)                       │ │
│  │  auth • grammar • vocabulary • conversation • context           │ │
│  │  analytics • integration                                        │ │
│  └────────────────────────────────────────────────┬────────────────┘ │
└────────────────────────────────────────────────────┼──────────────────┘
                                                     │
                                                     │ JWT Auth
                                                     │ 74 REST Endpoints
                                                     │
┌────────────────────────────────────────────────────▼──────────────────┐
│                    Backend (FastAPI + Python 3.10)                     │
│                    http://192.168.178.100:8000                        │
│  ┌────────────────────────────────────────────────────────────────┐  │
│  │ API Layer: 7 Modules, 74 Endpoints                            │  │
│  │ auth(3) • sessions(4) • contexts(5) • grammar(14) •           │  │
│  │ vocabulary(26) • analytics(14) • integration(3) • health(2)   │  │
│  └──────────────────────────┬─────────────────────────────────────┘  │
│                             │                                         │
│  ┌──────────────────────────▼─────────────────────────────────────┐  │
│  │ Business Logic: 5 Services                                     │  │
│  │ ConversationAI • GrammarAIService • VocabularyAIService        │  │
│  │ AnalyticsService • IntegrationService                          │  │
│  └──────────────────────────┬─────────────────────────────────────┘  │
│                             │                                         │
│  ┌──────────────────────────▼─────────────────────────────────────┐  │
│  │ Data Access: SQLAlchemy 2.0 (20 Models)                        │  │
│  │ Core(4) • Grammar(6) • Vocabulary(7) • Analytics(4)            │  │
│  └──────────────────────────┬─────────────────────────────────────┘  │
└─────────────────────────────┼───────────────────────────────────────┘
                              │
                              │ SQL
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│              PostgreSQL 15 Database (20 Tables)                      │
│  users • contexts • sessions • messages • grammar_topics •          │
│  grammar_exercises • user_grammar_progress • vocabulary •           │
│  user_vocabulary_progress • achievements • user_achievements •      │
│  ... (and 9 more tables)                                            │
└─────────────────────────────┬───────────────────────────────────────┘
                              │
                              │ AI API Calls
                              │
┌─────────────────────────────▼───────────────────────────────────────┐
│                    Anthropic Claude Sonnet 4.5                       │
│  ConversationAI • Exercise Generation • Word Analysis •             │
│  Error Explanations • Personalized Recommendations                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Available Codemaps

### Frontend Architecture (3 Codemaps)

#### 1. [Frontend Architecture](./frontend.md)
**Purpose:** Overall React application structure, build configuration, and module organization

**Coverage:**
- Application entry points (main.tsx, App.tsx, vite.config.ts)
- Directory structure (135 files, 22,000 LOC)
- 30 routes with React Router v6
- Build system (Vite 5.x, Tailwind CSS v3)
- Development workflow

**Key Insights:**
- 26 page components organized by module
- 81 reusable components across 7 categories
- Hot module replacement for instant feedback
- Code splitting for optimal bundle size

---

#### 2. [Frontend Components](./frontend-components.md)
**Purpose:** Detailed component architecture, design patterns, and UI organization

**Coverage:**
- **Common Components (12):** Button, Card, Badge, Modal, Loading, Toast, etc.
- **Grammar Components (7):** ExerciseRenderer, FeedbackDisplay, SessionHeader, TextDiff, etc.
- **Vocabulary Components (26):** WordCard, FlashcardDisplay, QuizSetup, MasteryIndicator, etc.
- **Conversation Components (13):** MessageBubble, ChatInput, GrammarFeedbackPanel, etc.
- **Dashboard Components (6):** OverallProgressCard, CurrentStreakCard, QuickActionsCard, etc.
- **Analytics Components (10):** AchievementCard, ProgressChart, HeatmapGrid, etc.
- **Learning Path Components (4):** DailyPlan, FocusArea, WeeklyGoals, RecommendedContext
- **Layout Components (4):** Layout, Sidebar, Header, ProtectedRoute

**Design Patterns:**
- Atomic Design: Common → Feature-Specific → Pages
- Compound Components: ExerciseRenderer with 5 exercise types
- Higher-Order Components: ProtectedRoute, Layout wrapper
- Render Props: Modal, Dropdown (Headless UI)

**Key Features:**
- TypeScript for type safety
- Tailwind CSS utility classes
- Headless UI for accessibility
- Barrel exports for clean imports

---

#### 3. [Frontend State Management](./frontend-state.md)
**Purpose:** Zustand stores, API integration layer, and data flow

**Coverage:**
- **Zustand Stores (6):**
  - `authStore` - Authentication, JWT token, user profile
  - `grammarStore` - Session state, bookmarks, notes, focus mode
  - `vocabularyStore` - Flashcards, quizzes, word lists
  - `conversationStore` - Chat messages, grammar feedback, session persistence
  - `analyticsStore` - Progress cache, achievements
  - `notificationStore` - Toast notifications

- **API Services (7):**
  - `authService` - Login, register, get current user (3 endpoints)
  - `grammarService` - Topics, practice sessions, progress (14 endpoints)
  - `vocabularyService` - Words, flashcards, quizzes, lists (26 endpoints)
  - `conversationService` - Sessions, messages, history (4 endpoints)
  - `contextService` - Contexts CRUD (5 endpoints)
  - `analyticsService` - Progress, achievements, leaderboards (14 endpoints)
  - `integrationService` - Dashboard, learning path, session analysis (3 endpoints)

- **Type System (7 Type Files):**
  - 150+ TypeScript interfaces
  - Full API request/response types
  - Frontend-backend contract

**State Patterns:**
- localStorage persistence for critical state
- Optimistic updates for instant UX
- Error boundaries for fault tolerance
- JWT interceptors for auth
- Centralized error handling

---

### Backend Architecture (3 Codemaps)

#### 4. [Backend Architecture](./backend.md)
**Purpose:** FastAPI application structure, services, and overall design

**Coverage:**
- Application entry point (main.py)
- Configuration management (Pydantic settings)
- Middleware (CORS, authentication)
- Dependency injection patterns
- Service layer architecture

**Services:**
- **ConversationAI:** Claude Sonnet 4.5 integration, context-aware conversations
- **GrammarAIService:** Exercise generation, answer evaluation, error explanations
- **VocabularyAIService:** Word analysis, vocabulary detection, recommendations
- **AnalyticsService:** Progress tracking, achievements, error pattern analysis
- **IntegrationService:** Cross-module workflows, personalized learning paths

**Key Features:**
- 104 tests with >80% coverage
- Automatic API documentation (Swagger UI)
- Async/await for performance
- Dependency injection
- Environment-based configuration

---

#### 5. [Backend Database](./backend-database.md)
**Purpose:** PostgreSQL schema, models, relationships, and migrations

**Coverage:**
- **20 SQLAlchemy Models:**
  - Core (4): User, Context, Session, Message
  - Grammar (6): GrammarTopic, GrammarExercise, UserGrammarProgress, GrammarSession, GrammarExerciseAttempt, DiagnosticTest
  - Vocabulary (7): Vocabulary, UserVocabularyProgress, UserVocabularyList, VocabularyListWords, VocabularyReview, FlashcardSession, VocabularyQuiz
  - Analytics (4): Achievement, UserAchievement, UserStats, ProgressSnapshot

- **2 Alembic Migrations:**
  - `001_update_vocabulary_schema` - Comprehensive vocabulary schema alignment
  - `002_add_vocabulary_sessions` - Multi-worker session persistence

**Relationships:**
- User → Sessions (one-to-many)
- Session → Messages (one-to-many)
- User → Grammar Progress (one-to-many)
- User → Vocabulary Progress (one-to-many)
- User → Achievements (many-to-many)
- Vocabulary Lists → Words (many-to-many)

**Database Patterns:**
- Soft deletes (is_active flags)
- Timestamps (created_at, updated_at)
- JSON fields for flexible data (metadata, questions_data)
- Indexes for performance (user_id, session_id, topic_id)
- Foreign keys with cascading deletes

---

#### 6. [Backend API](./backend-api.md)
**Purpose:** REST API endpoint organization, request/response schemas, and routing

**Coverage:**
- **74 REST Endpoints across 7 modules:**
  - Authentication (3): register, login, get current user
  - Sessions (4): start, send message, end, history
  - Contexts (5): list, get, create, update, delete
  - Grammar (14): topics, practice sessions, progress, diagnostics, recommendations
  - Vocabulary (26): words, flashcards, lists, quizzes, progress, AI features
  - Analytics (14): progress, achievements, leaderboards, heatmaps, error analysis
  - Integration (3): dashboard, learning path, session analysis
  - Health (2): root, health check

- **Authentication:**
  - OAuth2 password flow
  - JWT tokens (30-minute expiry)
  - bcrypt password hashing
  - Protected endpoints with dependency injection

- **API Patterns:**
  - RESTful design (GET, POST, PUT, DELETE)
  - Pydantic validation
  - Comprehensive error handling (422, 404, 401, 500)
  - Pagination support
  - Filtering and sorting

**Endpoint Examples:**
- `POST /api/grammar/practice/start` - Start grammar practice session
- `GET /api/v1/vocabulary/words?category=business&difficulty=B2` - Filter vocabulary
- `GET /api/v1/analytics/heatmap/activity` - Get 365-day activity heatmap
- `GET /api/v1/integration/learning-path` - Get personalized daily plan

---

## Module Interactions

### 1. Conversation → Grammar Practice Flow
```
User completes conversation
    ↓
Backend detects grammar errors (ConversationAI)
    ↓
IntegrationService analyzes session
    ↓
Frontend displays grammar topics to practice
    ↓
User clicks "Practice This Topic"
    ↓
Grammar practice session starts with filtered exercises
```

### 2. Learning Path → Multi-Module Flow
```
User views Learning Path page
    ↓
IntegrationService analyzes:
  - Grammar weak areas (low mastery < 0.5)
  - Vocabulary review queue (due items)
  - Conversation contexts (unpracticed)
    ↓
Backend generates:
  - Daily plan (75 min: 15 vocab + 30 grammar + 30 convo)
  - Focus areas (prioritized: critical → high → medium → low)
  - Weekly goals (session targets + milestones)
    ↓
Frontend renders with "Start" buttons
    ↓
User clicks → Redirects to respective module practice page
```

### 3. Spaced Repetition Flow (Grammar & Vocabulary)
```
User completes exercise/flashcard
    ↓
Backend calculates mastery adjustment:
  - Correct → Increase mastery, extend interval
  - Incorrect → Decrease mastery, reset interval
    ↓
Progress updated in database
    ↓
Review queue recalculated (due items based on next_review_date)
    ↓
Dashboard shows "X items due"
    ↓
User practices → Cycle continues
```

### 4. Achievement Unlock Flow
```
User completes activity (session, exercise, etc.)
    ↓
AnalyticsService checks achievement criteria:
  - Count-based: "Complete 10 sessions"
  - Streak-based: "7-day streak"
  - Accuracy-based: "90% accuracy on 50 exercises"
    ↓
Achievement unlocked → user_achievements table updated
    ↓
Frontend shows toast notification
    ↓
Achievement visible in Achievements page
```

---

## Data Flow Patterns

### Frontend → Backend (API Request)
```
User Action
    ↓
Component Event Handler
    ↓
Zustand Store Action (optimistic update)
    ↓
API Service Function (Axios)
    ↓
HTTP Request (with JWT token in header)
    ↓
Backend API Endpoint
```

### Backend → Database (Data Persistence)
```
API Endpoint Receives Request
    ↓
Pydantic Schema Validation
    ↓
Service Layer Business Logic
    ↓
SQLAlchemy ORM Query
    ↓
PostgreSQL Database
    ↓
Return Result (ORM Model)
    ↓
Convert to Pydantic Response Schema
    ↓
JSON Response to Frontend
```

### AI Integration (Claude Sonnet 4.5)
```
User Sends Conversation Message
    ↓
Backend Receives Message
    ↓
ConversationAI Service:
  - Load context (business scenario)
  - Build conversation history
  - Call Anthropic API
  - Parse AI response
  - Detect grammar errors
  - Extract vocabulary
    ↓
Save to Database (messages, grammar_corrections)
    ↓
Return AI Response + Feedback to Frontend
```

---

## Technology Stack

### Frontend
- **React 18** - UI library with hooks
- **TypeScript** - Type-safe JavaScript
- **Vite 5.x** - Lightning-fast build tool
- **Tailwind CSS v3** - Utility-first styling
- **Zustand** - Lightweight state management (6 stores)
- **Axios** - HTTP client with interceptors
- **React Router v6** - Client-side routing (30 routes)
- **Recharts 3.7** - Data visualization
- **Headless UI** - Accessible components
- **React Hot Toast** - Toast notifications

### Backend
- **Python 3.10** - Core language
- **FastAPI** - Modern async web framework
- **PostgreSQL 15** - Relational database
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migrations
- **Anthropic Claude Sonnet 4.5** - AI conversation and generation
- **bcrypt 4.2.0** - Password hashing
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server (multi-worker support)
- **pytest** - Testing framework (104 tests, >80% coverage)

### Deployment
- **Ubuntu 20.04 LTS** - Production server
- **Nginx** - Reverse proxy
- **Systemd** - Service management
- **Git** - Version control

---

## Key Metrics

### Codebase Size
- **Frontend:** 135 files, ~22,000 LOC
- **Backend:** ~150 files, ~15,000 LOC
- **Total:** ~285 files, ~37,000 LOC

### API Coverage
- **74 REST Endpoints** across 7 modules
- **20 Database Models** with relationships
- **104 Backend Tests** (>80% coverage)
- **0 Frontend Tests** (Phase 8 pending)

### Features
- **5 Core Modules:** Grammar, Vocabulary, Conversation, Analytics, Learning Path
- **12+ Conversation Contexts** (business + daily)
- **50+ Grammar Topics** (A1-C2)
- **200+ Manual Exercises** (5 types)
- **150+ Vocabulary Words** (foundation for 1000+)
- **31 Achievements** (4 tiers, 5,825 points)

---

## Development Status

**Phase 0:** ✅ Project Setup (40h)
**Phase 1:** ✅ Authentication (50h)
**Phase 2:** ✅ Dashboard & Layout (45h)
**Phase 3:** ✅ Grammar Module (120h)
**Phase 4:** ✅ Vocabulary Module (100h)
**Phase 5:** ✅ Conversation Practice (60h)
**Phase 6:** ✅ Analytics & Progress (55h)
**Phase 7:** ✅ Learning Path (50h)
**Phase 8:** ⏳ Testing & Documentation (50h - Not Started)

**Total Progress:** 520h / 570h (94% Complete)

---

## Quick Navigation

### Frontend Codemaps
- [Frontend Architecture](./frontend.md) - App structure, build config, directory layout
- [Frontend Components](./frontend-components.md) - 81 components, design patterns
- [Frontend State Management](./frontend-state.md) - Zustand stores, API services

### Backend Codemaps
- [Backend Architecture](./backend.md) - FastAPI app, services, business logic
- [Backend Database](./backend-database.md) - 20 models, relationships, migrations
- [Backend API](./backend-api.md) - 74 endpoints, request/response schemas

### Documentation
- [Main README](../../README.md) - Project overview and quick start
- [Deployment Guide](../GUIDES/deployment/DEPLOYMENT_GUIDE.md) - Production deployment
- [Testing Documentation](../testing/) - Test reports and bug tracking

---

## Recent Updates (January 22-24, 2026)

### Frontend Changes
- ✅ Added Learning Path module (4 components, 1 page)
- ✅ Fixed grammar practice loading bugs (BUG-020, BUG-021)
- ✅ Fixed session duration calculation issues
- ✅ Fixed vocabulary flashcard/quiz completion timestamps
- ✅ Resolved infinite loop in grammar session cleanup

### Backend Changes
- ✅ Implemented batch content feeding system for vocabulary
- ✅ Fixed grammar session end response structure
- ✅ Added defensive error handling to grammar endpoints
- ✅ Configured Pydantic to ignore extra environment variables

### Documentation Updates
- ✅ Updated all frontend codemaps to include Learning Path (this update)
- ✅ Updated main README.md with Phase 7 completion
- ✅ Updated docs/README.md with correct frontend status (94%)
- ✅ Created comprehensive CODEMAPS/INDEX.md (this file)

---

**For questions about architecture, see the specific codemaps above.**
**For setup and deployment, see:** [Deployment Guide](../GUIDES/deployment/DEPLOYMENT_GUIDE.md)
**For API documentation, visit:** http://192.168.178.100:8000/docs
