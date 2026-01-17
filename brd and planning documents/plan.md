# German Learning Application - Implementation Plan

**Version:** 1.0
**Date:** 2026-01-17
**Based on:** BRD v1.1
**Development Timeline:** 10 weeks

---

## Executive Summary

This plan outlines the phased implementation of a comprehensive German learning application featuring:
- AI-powered conversation practice (Anthropic Claude)
- Comprehensive grammar learning system with diagnostic tests and drilling
- Vocabulary management with spaced repetition
- Progress tracking and analytics
- Interactive practice sessions

**Tech Stack:**
- Backend: FastAPI + Python 3.11+ + PostgreSQL + SQLAlchemy
- Frontend: React 18 + TypeScript + Vite + Tailwind CSS
- AI: Anthropic Claude 3.5 Sonnet
- Deployment: Local Ubuntu server or development machine

---

## Phase 1: Core Infrastructure (Weeks 1-2)

### Objectives
Set up foundational architecture, database, and authentication system.

### Tasks

#### 1.1 Project Setup
- [ ] Initialize Git repository with proper .gitignore
- [ ] Create directory structure (backend, frontend, docs)
- [ ] Set up Python virtual environment
- [ ] Create requirements.txt with dependencies
- [ ] Set up Node.js project with Vite + React + TypeScript
- [ ] Configure Tailwind CSS
- [ ] Create .env.example templates

#### 1.2 Database Design & Setup
- [ ] Install PostgreSQL
- [ ] Create database: `german_learning`
- [ ] Set up SQLAlchemy with database.py
- [ ] Create all database models:
  - `models/user.py` - Users table
  - `models/vocabulary.py` - Vocabulary and user_vocabulary tables
  - `models/context.py` - Contexts table
  - `models/session.py` - Sessions and conversation_turns tables
  - `models/grammar.py` - Grammar topics, exercises, progress tables
  - `models/progress.py` - Progress snapshots and grammar_corrections
- [ ] Set up Alembic for migrations
- [ ] Create initial migration
- [ ] Run migration to create all tables
- [ ] Add proper indexes as per BRD schema

#### 1.3 Backend API Structure
- [ ] Create FastAPI main app (`app/main.py`)
- [ ] Set up configuration management (`app/config.py`)
- [ ] Configure CORS for frontend communication
- [ ] Create database session dependency (`app/database.py`)
- [ ] Set up logging with RotatingFileHandler
- [ ] Create health check endpoint
- [ ] Set up error handling middleware

#### 1.4 Authentication System
- [ ] Implement password hashing with bcrypt
- [ ] Create JWT token generation/validation
- [ ] Build authentication endpoints:
  - POST `/api/v1/auth/register`
  - POST `/api/v1/auth/login`
  - GET `/api/v1/auth/me`
- [ ] Create authentication dependency for protected routes
- [ ] Add user schemas (Pydantic models)

#### 1.5 Testing & Validation
- [ ] Test database connection and migrations
- [ ] Test user registration and login flow
- [ ] Verify JWT token generation/validation
- [ ] Test all database models CRUD operations

### Deliverables
- Working PostgreSQL database with all tables
- FastAPI backend with authentication
- Basic project structure for frontend
- Database migrations setup
- All models and schemas defined

---

## Phase 2: AI Integration & Conversation Engine (Weeks 3-4)

### Objectives
Integrate Anthropic Claude API and build conversation functionality with grammar analysis.

### Tasks

#### 2.1 AI Service Integration
- [ ] Create `services/ai_service.py`
- [ ] Implement ConversationAI class with Claude API
- [ ] Build conversation response generation
- [ ] Implement grammar analysis function
- [ ] Implement vocabulary detection function
- [ ] Add error handling and retry logic
- [ ] Add fallback responses for API failures
- [ ] Test API integration thoroughly

#### 2.2 Context Management
- [ ] Create context CRUD endpoints in `api/v1/contexts.py`:
  - GET `/api/contexts` - List contexts
  - GET `/api/contexts/{id}` - Get context details
  - POST `/api/contexts` - Create custom context
- [ ] Create context schemas
- [ ] Build seed script for default contexts (12+ contexts)
- [ ] Add business contexts (Banking, Partnerships, Compliance, etc.)
- [ ] Add daily life contexts (Restaurant, Shopping, Travel, etc.)

#### 2.3 Session Management API
- [ ] Create session endpoints in `api/v1/sessions.py`:
  - POST `/api/sessions/start` - Start new session
  - POST `/api/sessions/{id}/message` - Send message
  - POST `/api/sessions/{id}/end` - End session
  - GET `/api/sessions/{id}` - Get session history
- [ ] Implement session creation logic
- [ ] Implement conversation turn storage
- [ ] Implement grammar feedback integration
- [ ] Implement vocabulary detection and storage
- [ ] Create session summary generation
- [ ] Map grammar errors to grammar topics (FK relationships)

#### 2.4 Frontend Conversation Interface
- [ ] Create React conversation components:
  - `ConversationInterface.tsx` - Main container
  - `MessageBubble.tsx` - Display messages
  - `MessageInput.tsx` - User input area
  - `GrammarFeedback.tsx` - Inline corrections
  - `SessionControls.tsx` - Start/end/timer
- [ ] Create conversation service (`services/conversationService.ts`)
- [ ] Build conversation page layout
- [ ] Add real-time message display
- [ ] Add grammar feedback toggle
- [ ] Add session timer
- [ ] Add vocabulary sidebar (optional display)
- [ ] Style with Tailwind CSS

#### 2.5 Testing
- [ ] Test full conversation flow end-to-end
- [ ] Test grammar analysis accuracy
- [ ] Test vocabulary detection
- [ ] Test error handling
- [ ] Test UI responsiveness

### Deliverables
- Working AI conversation service
- Grammar analysis with topic mapping
- Vocabulary detection system
- Session management API (complete)
- Functional conversation UI
- 12+ seeded contexts
- Grammar error → topic mapping implementation

---

## Phase 3: Grammar Learning System (Weeks 5-6)

### Objectives
Build comprehensive grammar module with diagnostics, exercises, and drilling.

### Tasks

#### 3.1 Grammar Data Setup
- [ ] Create `scripts/seed_grammar_data.py`
- [ ] Define 50+ grammar topics with:
  - Cases (Nominativ, Akkusativ, Dativ, Genitiv)
  - Verb conjugation (all tenses + moods)
  - Sentence structure
  - Articles & pronouns
  - Adjectives & adverbs
  - Prepositions
  - Passive voice, indirect speech, conjunctions
- [ ] Write detailed explanations in German for each topic
- [ ] Create hierarchical topic structure (parent/child)
- [ ] Seed grammar topics into database

#### 3.2 Exercise Generation System
- [ ] Create `services/grammar_ai_service.py`
- [ ] Implement GrammarAIService class
- [ ] Build exercise generation with Claude:
  - Fill-in-the-blank exercises
  - Multiple choice exercises
  - Translation exercises (Italian → German)
  - Error correction exercises
  - Sentence building exercises
- [ ] Implement grammar rule explanation generator
- [ ] Create manual exercise database (200+ exercises)
- [ ] Build seed script for manual exercises
- [ ] Test exercise quality and variety

#### 3.3 Diagnostic Assessment System
- [ ] Build diagnostic test generator (30 questions)
- [ ] Create diagnostic endpoints in `api/v1/grammar.py`:
  - POST `/api/grammar/diagnostic/start`
  - GET `/api/grammar/diagnostic/{id}/questions`
  - POST `/api/grammar/diagnostic/{id}/answer`
  - GET `/api/grammar/diagnostic/{id}/results`
- [ ] Implement test scoring and analysis
- [ ] Build learning path recommendation algorithm
- [ ] Identify weak areas and strong areas
- [ ] Store diagnostic results

#### 3.4 Grammar Practice Session API
- [ ] Implement grammar practice endpoints:
  - GET `/api/grammar/recommendations` - Get suggested topics
  - GET `/api/grammar/topics/{id}` - Topic details + explanation
  - POST `/api/grammar/sessions/start` - Start drill session
  - POST `/api/grammar/sessions/{id}/answer` - Submit answer
  - POST `/api/grammar/sessions/{id}/hint` - Get progressive hints
  - POST `/api/grammar/sessions/{id}/end` - End session + summary
  - POST `/api/grammar/exercises/generate` - AI exercise generation
- [ ] Implement immediate feedback logic
- [ ] Build session summary with detailed statistics
- [ ] Identify weak subtopics during sessions

#### 3.5 Grammar Progress & Spaced Repetition
- [ ] Create `utils/grammar_spaced_repetition.py`
- [ ] Implement mastery level calculation
- [ ] Implement next review date calculation
- [ ] Build conversation-triggered practice detection
- [ ] Create progress tracking endpoints:
  - GET `/api/grammar/progress/overview`
  - GET `/api/grammar/progress/topic/{id}`
  - GET `/api/grammar/progress/heatmap`
- [ ] Update user_grammar_progress after each session

#### 3.6 Frontend Grammar Interface
- [ ] Create grammar components:
  - `GrammarTopicSelector.tsx` - Browse/select topics
  - `GrammarExplanation.tsx` - Display rules in German
  - `ExerciseInterface.tsx` - Generic exercise display
  - `FillBlankExercise.tsx` - Fill-in-the-blank type
  - `MultipleChoiceExercise.tsx` - Multiple choice type
  - `TranslationExercise.tsx` - Translation type
  - `ImmediateFeedback.tsx` - Show corrections + explanations
  - `GrammarSessionSummary.tsx` - End session stats
  - `DiagnosticTest.tsx` - Diagnostic interface
- [ ] Create `pages/Grammar.tsx`
- [ ] Create `services/grammarService.ts`
- [ ] Build topic selection view (recommended, browse, search)
- [ ] Build exercise flow (question → answer → feedback → next)
- [ ] Add hint system (progressive hints)
- [ ] Add progress indicators (5/15)
- [ ] Build session summary view
- [ ] Build diagnostic test interface

#### 3.7 Conversation → Grammar Integration
- [ ] Detect grammar error patterns after conversation ends
- [ ] Prompt user: "Möchtest du [topic] üben?" (3+ errors)
- [ ] Auto-generate targeted drill session
- [ ] Link grammar session to conversation session (FK)
- [ ] Update grammar progress based on conversation errors

#### 3.8 Testing
- [ ] Test diagnostic assessment flow
- [ ] Test exercise generation quality (all 5 types)
- [ ] Test drill session completion
- [ ] Test spaced repetition calculations
- [ ] Test conversation-triggered practice
- [ ] Test all grammar UI components
- [ ] Validate mastery level updates

### Deliverables
- 50+ grammar topics seeded
- 200+ manual exercises seeded
- AI exercise generation working
- Diagnostic test system complete
- Grammar drill sessions functional
- Grammar spaced repetition implemented
- Complete grammar UI
- Conversation → grammar practice integration
- Grammar progress tracking

---

## Phase 4: Vocabulary System (Week 7)

### Objectives
Build vocabulary management, spaced repetition, and review system.

### Tasks

#### 4.1 Vocabulary Database Setup
- [ ] Create vocabulary seed script
- [ ] Seed 500+ vocabulary items:
  - Business/finance vocabulary (200+)
  - Daily life vocabulary (200+)
  - General vocabulary (100+)
- [ ] Include German, Italian, English translations
- [ ] Add example sentences
- [ ] Add grammatical info (gender, plural, part of speech)
- [ ] Categorize by difficulty (B1, B2, C1, C2)

#### 4.2 Vocabulary API Endpoints
- [ ] Create `api/v1/vocabulary.py`:
  - GET `/api/vocabulary/overview` - Stats overview
  - GET `/api/vocabulary/list` - Filtered vocabulary list
  - POST `/api/vocabulary/add` - Add custom vocabulary
  - POST `/api/vocabulary/review/start` - Start review session
  - POST `/api/vocabulary/review/answer` - Submit answer
  - GET `/api/vocabulary/{id}` - Get word details
- [ ] Implement vocabulary search and filtering
- [ ] Build review session logic
- [ ] Track vocabulary encounters during conversations

#### 4.3 Spaced Repetition Implementation
- [ ] Create `utils/spaced_repetition.py`
- [ ] Implement SM-2-like algorithm
- [ ] Calculate familiarity scores
- [ ] Calculate next review dates
- [ ] Update scores based on review performance
- [ ] Identify vocabulary due for review

#### 4.4 Frontend Vocabulary Interface
- [ ] Create vocabulary components:
  - `VocabularyDashboard.tsx` - Main view
  - `VocabularyCard.tsx` - Display word info
  - `VocabularyFilters.tsx` - Search/filter controls
  - `VocabularyReview.tsx` - Review session interface
  - `VocabularyStats.tsx` - Progress stats
- [ ] Create `pages/Vocabulary.tsx`
- [ ] Create `services/vocabularyService.ts`
- [ ] Build search and filter UI
- [ ] Build review session flow
- [ ] Add spaced repetition queue indicator
- [ ] Display familiarity scores visually

#### 4.5 Testing
- [ ] Test vocabulary CRUD operations
- [ ] Test spaced repetition algorithm
- [ ] Test review sessions
- [ ] Test filtering and search
- [ ] Test vocabulary detection during conversations

### Deliverables
- 500+ vocabulary items seeded
- Vocabulary management API complete
- Spaced repetition algorithm working
- Vocabulary review system functional
- Vocabulary dashboard UI complete

---

## Phase 5: Progress Tracking & Analytics (Week 8)

### Objectives
Build comprehensive analytics for conversation, grammar, and vocabulary progress.

### Tasks

#### 5.1 Progress Tracking Backend
- [ ] Create `services/analytics_service.py`
- [ ] Implement progress snapshot generation
- [ ] Build error pattern analysis (conversation + grammar drills)
- [ ] Create achievement/badge system
- [ ] Build trend analysis (grammar accuracy, vocabulary growth)
- [ ] Calculate grammar mastery by category
- [ ] Track learning streaks

#### 5.2 Progress API Endpoints
- [ ] Create `api/v1/progress.py`:
  - GET `/api/progress/dashboard` - Main stats
  - GET `/api/progress/errors` - Error breakdown
  - GET `/api/progress/grammar-heatmap` - Grammar mastery visualization
  - GET `/api/progress/trends` - Time-series data
  - GET `/api/progress/achievements` - Badges/milestones
- [ ] Implement daily/weekly/monthly snapshots
- [ ] Build aggregation queries for statistics

#### 5.3 Frontend Analytics Dashboard
- [ ] Create analytics components:
  - `ProgressDashboard.tsx` - Main dashboard
  - `StatsCard.tsx` - Key metric cards
  - `GrammarAccuracyChart.tsx` - Line chart
  - `VocabularyGrowthChart.tsx` - Area chart
  - `GrammarHeatmap.tsx` - Mastery by category
  - `ErrorBreakdown.tsx` - Pie chart
  - `SessionCalendar.tsx` - Activity heatmap
  - `Achievements.tsx` - Badges display
- [ ] Create `pages/Progress.tsx`
- [ ] Integrate Chart.js or Recharts
- [ ] Build period selector (week/month/all-time)
- [ ] Add drill-down capabilities (click topic → details)
- [ ] Link weak areas to practice buttons

#### 5.4 Achievement System
- [ ] Define achievements:
  - Session streaks (3, 7, 14, 30 days)
  - Vocabulary milestones (100, 250, 500 words)
  - Grammar topics mastered (5, 10, 20, 50)
  - Accuracy achievements (90%+, 95%+)
  - Practice volume (50, 100, 200 sessions)
- [ ] Implement achievement detection
- [ ] Store achievements in progress_snapshots
- [ ] Display new achievements after sessions

#### 5.5 Testing
- [ ] Test progress snapshot generation
- [ ] Test analytics calculations accuracy
- [ ] Test trend analysis
- [ ] Test achievement detection
- [ ] Test all chart visualizations

### Deliverables
- Complete analytics service
- Progress tracking API endpoints
- Analytics dashboard UI with charts
- Achievement system
- Grammar mastery heatmap
- Error pattern analysis (all modules)

---

## Phase 6: Context Library & Integration (Week 9)

### Objectives
Polish context system, integrate all modules seamlessly, refine UX.

### Tasks

#### 6.1 Context Library Enhancement
- [ ] Ensure all 12+ default contexts are seeded
- [ ] Create context library UI:
  - `ContextLibrary.tsx` - Grid/list view
  - `ContextCard.tsx` - Context display
  - `ContextFilters.tsx` - Category/difficulty filters
  - `CreateContextModal.tsx` - Custom context creator
- [ ] Add context usage statistics
- [ ] Show recent sessions per context
- [ ] Add suggested vocabulary preview

#### 6.2 Main Dashboard
- [ ] Create `pages/Dashboard.tsx`
- [ ] Build quick stats display:
  - Today's progress
  - Current streak
  - Vocabulary due for review
  - Grammar topics due
- [ ] Add quick start buttons:
  - "Start Conversation"
  - "Review Vocabulary"
  - "Practice Grammar"
  - "Continue Last Session"
- [ ] Show recent activity feed
- [ ] Display progress charts preview
- [ ] Add motivational elements

#### 6.3 Navigation & Routing
- [ ] Set up React Router
- [ ] Create navigation component
- [ ] Add routes:
  - `/` - Dashboard
  - `/conversation` - Conversation interface
  - `/grammar` - Grammar practice
  - `/vocabulary` - Vocabulary dashboard
  - `/progress` - Analytics
  - `/contexts` - Context library
  - `/settings` - User settings (optional)
- [ ] Add breadcrumb navigation
- [ ] Implement protected routes

#### 6.4 Module Integration & Flow
- [ ] Ensure seamless conversation → grammar practice flow
- [ ] Add vocabulary review prompts from dashboard
- [ ] Link progress page weak areas to practice
- [ ] Add "practice similar exercises" after grammar sessions
- [ ] Implement session pause/resume functionality
- [ ] Add quick navigation between modules

#### 6.5 UI/UX Polish
- [ ] Refine Tailwind CSS styling across all components
- [ ] Ensure responsive design (mobile-friendly)
- [ ] Add loading states and skeletons
- [ ] Add error states and user-friendly messages
- [ ] Implement toast notifications for actions
- [ ] Add keyboard shortcuts for common actions
- [ ] Optimize performance (lazy loading, code splitting)

#### 6.6 Testing
- [ ] Test cross-module navigation
- [ ] Test responsive design on multiple screen sizes
- [ ] Test all user flows end-to-end
- [ ] User acceptance testing (as Igor)

### Deliverables
- Complete context library UI
- Main dashboard with quick actions
- Full navigation system
- Seamless module integration
- Polished UI/UX across application

---

## Phase 7: Testing & Optimization (Week 10)

### Objectives
Comprehensive testing, performance optimization, documentation.

### Tasks

#### 7.1 Backend Testing
- [ ] Write unit tests for all services:
  - `tests/test_ai_service.py`
  - `tests/test_grammar_ai_service.py`
  - `tests/test_vocabulary_service.py`
  - `tests/test_analytics_service.py`
  - `tests/test_spaced_repetition.py`
- [ ] Write API endpoint tests
- [ ] Test database operations and constraints
- [ ] Test authentication and authorization
- [ ] Aim for >80% code coverage

#### 7.2 Frontend Testing
- [ ] Write component tests (React Testing Library)
- [ ] Test user interactions
- [ ] Test form validations
- [ ] Test API service functions
- [ ] E2E tests with Playwright or Cypress (optional)

#### 7.3 Integration Testing
- [ ] Test complete conversation flow
- [ ] Test complete grammar drill flow
- [ ] Test vocabulary review flow
- [ ] Test diagnostic assessment flow
- [ ] Test conversation → grammar practice trigger
- [ ] Test progress tracking accuracy

#### 7.4 Performance Optimization
- [ ] Profile API response times
- [ ] Optimize database queries (add missing indexes)
- [ ] Implement caching for:
  - Vocabulary lookups
  - Grammar topic explanations
  - Context data
- [ ] Optimize frontend bundle size
- [ ] Implement lazy loading for routes
- [ ] Optimize images and assets

#### 7.5 Security Audit
- [ ] Review authentication implementation
- [ ] Test JWT token security
- [ ] Check for SQL injection vulnerabilities
- [ ] Validate input sanitization
- [ ] Review API rate limiting needs
- [ ] Secure environment variables

#### 7.6 Documentation
- [ ] Write comprehensive README.md:
  - Project overview
  - Setup instructions
  - Running the application
  - Project structure
  - Technologies used
- [ ] Document API endpoints (OpenAPI/Swagger)
- [ ] Write developer guide
- [ ] Document deployment process
- [ ] Create user guide (how to use the app)
- [ ] Document database schema
- [ ] Add inline code comments

#### 7.7 Deployment Preparation
- [ ] Create deployment scripts
- [ ] Write systemd service file
- [ ] Configure Nginx reverse proxy
- [ ] Set up database backup strategy
- [ ] Create migration rollback procedures
- [ ] Document server requirements

#### 7.8 Final Testing & Bug Fixes
- [ ] Conduct full application walkthrough
- [ ] Fix all identified bugs
- [ ] Test on production-like environment
- [ ] Verify all features against BRD requirements

### Deliverables
- >80% test coverage
- Performance benchmarks met
- Complete documentation
- Deployment guide
- Production-ready application

---

## Post-Launch Tasks

### Immediate (Weeks 11-12)
- [ ] Monitor application performance
- [ ] Collect usage data and user feedback
- [ ] Fix critical bugs
- [ ] Fine-tune grammar exercise generation
- [ ] Adjust spaced repetition intervals based on usage
- [ ] Add missing vocabulary/contexts as needed

### Near-term Enhancements
- [ ] Add more grammar exercises (manual and AI-generated)
- [ ] Expand vocabulary database (1000+ words)
- [ ] Add more contexts (20+ total)
- [ ] Implement export functionality (progress reports)
- [ ] Add user settings customization
- [ ] Implement dark mode (optional)

---

## Technical Requirements Checklist

### Development Environment
- [ ] Python 3.11+
- [ ] Node.js 18+
- [ ] PostgreSQL 15+
- [ ] Git
- [ ] Code editor (VS Code recommended)

### Python Dependencies (requirements.txt)
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.9
pydantic>=2.4.0
pydantic-settings>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
anthropic>=0.5.0
redis>=5.0.0
celery>=5.3.0  # Optional, for async tasks
pytest>=7.4.0
pytest-asyncio>=0.21.0
httpx>=0.25.0  # For testing
```

### Frontend Dependencies
```json
{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.18.0",
    "axios": "^1.6.0",
    "zustand": "^4.4.0",
    "tailwindcss": "^3.3.0",
    "recharts": "^2.10.0",
    "react-hot-toast": "^2.4.1"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.2.0",
    "vite": "^5.0.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31"
  }
}
```

### External Services
- [ ] Anthropic API account (Claude API key)
- [ ] PostgreSQL database setup

---

## Success Criteria

### Functional Requirements ✓
- [x] User can register and login
- [ ] User can have AI conversations in German
- [ ] User receives grammar corrections with topic mapping
- [ ] User can take diagnostic grammar test
- [ ] User can practice grammar drills (15+ exercises per topic)
- [ ] Conversation errors trigger grammar practice recommendations
- [ ] User can review vocabulary with spaced repetition
- [ ] User can track progress across all modules
- [ ] User can view grammar mastery heatmap
- [ ] User can select from 12+ contexts
- [ ] User can create custom contexts
- [ ] System tracks 500+ vocabulary items
- [ ] System covers 50+ grammar topics

### Performance Targets
- [ ] API response time < 200ms (excluding AI)
- [ ] AI conversation response < 3s
- [ ] Grammar analysis < 2s
- [ ] Page load < 1s
- [ ] Exercise generation < 5s

### Quality Metrics
- [ ] Test coverage > 80%
- [ ] Zero critical bugs
- [ ] All BRD features implemented
- [ ] Documentation complete
- [ ] User satisfaction (self-assessed by Igor)

---

## Risk Management

### Technical Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| AI API rate limits | High | Implement caching, fallback responses |
| Database performance | Medium | Proper indexing, query optimization |
| Exercise generation quality | High | Manual review, seed manual exercises |
| Frontend state complexity | Medium | Use Zustand, clear data flow |

### Timeline Risks
| Risk | Impact | Mitigation |
|------|--------|------------|
| Grammar module complexity | High | Prioritize core features, test early |
| AI integration delays | Medium | Start early, have fallback prompts |
| Testing time underestimated | Medium | Test continuously, not just Phase 7 |

---

## Key Decisions & Assumptions

### Decisions
1. **Single-user application**: No multi-user complexity initially
2. **TypeScript for frontend**: Better type safety and developer experience
3. **Anthropic Claude only**: No OpenAI fallback in v1.0
4. **Local deployment**: Ubuntu server or development machine, not cloud
5. **Grammar in German**: Advanced learners benefit from native explanations
6. **15-exercise drill sessions**: Optimal balance between depth and time

### Assumptions
1. User (Igor) has B2/C1 German proficiency
2. User has Python and cloud infrastructure experience
3. Primary usage on desktop/laptop (responsive design secondary)
4. Internet connection available (no offline mode in v1.0)
5. Anthropic API reliable and cost-effective (~$0.15/session)

---

## Development Guidelines

### Code Style
- **Python**: PEP 8, type hints, docstrings
- **TypeScript**: ESLint + Prettier, functional components
- **Naming**: Descriptive, consistent conventions
- **Comments**: Explain "why", not "what"

### Git Workflow
- Feature branches: `feature/grammar-exercises`, `feature/conversation-ui`
- Commit messages: Descriptive, present tense
- Regular commits (daily minimum)
- Main branch always deployable

### Testing Philosophy
- Write tests alongside features (TDD when applicable)
- Test user flows, not just functions
- Mock external services (AI API)
- Prioritize integration tests for critical flows

---

## Appendix: Quick Reference

### Project Structure
```
myGermanAITeacher/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── api/v1/         # API endpoints
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helpers
│   ├── alembic/            # Migrations
│   ├── tests/
│   ├── scripts/            # Seed scripts
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── App.tsx
│   └── package.json
├── docs/
├── logs/
└── brd and planning documents/
```

### Key Commands
```bash
# Backend
uvicorn app.main:app --reload --port 8000
alembic revision --autogenerate -m "message"
alembic upgrade head
pytest tests/

# Frontend
npm run dev
npm run build
npm run preview

# Database
psql german_learning
python scripts/seed_grammar_data.py
```

### Important Files
- `.env` - Environment variables (API keys, DB URL)
- `requirements.txt` - Python dependencies
- `package.json` - Node dependencies
- `alembic/env.py` - Migration configuration
- `app/config.py` - Application configuration

---

**END OF PLAN**

This implementation plan provides a structured roadmap for building the German Learning Application over 10 weeks. Follow phases sequentially, check off tasks as completed, and refer to the BRD for detailed specifications.
