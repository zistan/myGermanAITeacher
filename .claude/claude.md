# Claude Code Project Context

## Project: German Learning Application (myGermanAITeacher)

### Overview
An AI-powered German language learning application designed for advanced learners (B2/C1 level) with a focus on:
- Business vocabulary (payments/finance sector)
- Conversational fluency (business & everyday contexts)
- Comprehensive grammar mastery through systematic drilling

**User Profile**: Igor - Italian native speaker, fluent in English, works in payments/finance in Switzerland

### Core Features
1. **AI Conversation Practice**: Interactive conversations with Anthropic Claude in various contexts
2. **Grammar Learning System**: Diagnostic tests, 50+ topics, targeted drilling with 15+ exercises per topic
3. **Vocabulary Management**: 500+ words with spaced repetition algorithm
4. **Progress Analytics**: Comprehensive tracking across all modules with mastery heatmaps

### Technology Stack

**Backend:**
- Python 3.11+
- FastAPI (REST API)
- PostgreSQL 15+ (database)
- SQLAlchemy 2.0 (ORM)
- Alembic (migrations)
- Anthropic Claude 3.5 Sonnet (AI)

**Frontend:**
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
**Current Phase**: Phase 1 - Core Infrastructure (Weeks 1-2)
**Timeline**: 10-week development plan

### Key Documents
- `brd and planning documents/german_learning_app_brd.md` - Complete Business Requirements Document (v1.1)
- `brd and planning documents/plan.md` - Detailed 10-week implementation plan

### Database Schema Highlights

**Core Tables:**
- `users` - User accounts and authentication
- `contexts` - Conversation scenarios (business, daily life)
- `vocabulary` - German words with translations (IT/EN)
- `user_vocabulary` - User's vocabulary progress with spaced repetition
- `sessions` - Conversation practice sessions
- `conversation_turns` - Individual messages in conversations
- `grammar_corrections` - Grammar errors with topic mapping

**Grammar Module (6 tables):**
- `grammar_topics` - 50+ topics (cases, verbs, sentence structure, etc.)
- `grammar_exercises` - Exercise database (manual + AI-generated)
- `user_grammar_progress` - Mastery levels per topic with spaced repetition
- `grammar_sessions` - Drill practice sessions (15+ exercises)
- `grammar_exercise_attempts` - Individual exercise answers
- `diagnostic_tests` - Grammar assessment results

**Analytics:**
- `progress_snapshots` - Daily/weekly/monthly metrics
- `grammar_corrections` - Error tracking with severity levels

### API Structure

**Authentication:**
- POST `/api/v1/auth/register`
- POST `/api/v1/auth/login`
- GET `/api/v1/auth/me`

**Conversations:**
- POST `/api/sessions/start`
- POST `/api/sessions/{id}/message`
- POST `/api/sessions/{id}/end`
- GET `/api/sessions/{id}`

**Grammar Module:**
- POST `/api/grammar/diagnostic/start` - Start assessment
- POST `/api/grammar/sessions/start` - Start drill session
- POST `/api/grammar/sessions/{id}/answer` - Submit answer
- POST `/api/grammar/sessions/{id}/hint` - Get hints
- GET `/api/grammar/recommendations` - Suggested topics
- GET `/api/grammar/progress/overview` - Overall stats
- GET `/api/grammar/progress/heatmap` - Mastery visualization

**Vocabulary:**
- GET `/api/vocabulary/overview`
- GET `/api/vocabulary/list`
- POST `/api/vocabulary/review/start`
- POST `/api/vocabulary/review/answer`

**Progress:**
- GET `/api/progress/dashboard`
- GET `/api/progress/errors`
- GET `/api/progress/grammar-heatmap`

### Project Structure
```
myGermanAITeacher/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Settings & environment vars
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models/              # Database models
│   │   │   ├── user.py
│   │   │   ├── vocabulary.py
│   │   │   ├── context.py
│   │   │   ├── session.py
│   │   │   ├── grammar.py       # Grammar module models
│   │   │   └── progress.py
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── api/v1/              # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── sessions.py
│   │   │   ├── vocabulary.py
│   │   │   ├── grammar.py       # Grammar endpoints
│   │   │   ├── contexts.py
│   │   │   └── progress.py
│   │   ├── services/            # Business logic
│   │   │   ├── ai_service.py              # Conversation AI
│   │   │   ├── grammar_ai_service.py      # Exercise generation
│   │   │   ├── vocabulary_service.py
│   │   │   └── analytics_service.py
│   │   └── utils/               # Utilities
│   │       ├── spaced_repetition.py              # Vocabulary SR
│   │       └── grammar_spaced_repetition.py      # Grammar SR
│   ├── alembic/                 # Database migrations
│   ├── tests/                   # Unit & integration tests
│   ├── scripts/                 # Seed scripts
│   │   ├── seed_contexts.py
│   │   ├── seed_vocabulary.py
│   │   └── seed_grammar_data.py # Grammar topics & exercises
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── conversation/
│   │   │   ├── vocabulary/
│   │   │   └── grammar/         # Grammar UI components
│   │   ├── pages/
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Conversation.tsx
│   │   │   ├── Grammar.tsx      # Grammar practice page
│   │   │   ├── Vocabulary.tsx
│   │   │   └── Progress.tsx
│   │   ├── services/
│   │   │   ├── conversationService.ts
│   │   │   ├── grammarService.ts
│   │   │   └── vocabularyService.ts
│   │   └── App.tsx
│   └── package.json
├── docs/
├── logs/
└── brd and planning documents/
    ├── german_learning_app_brd.md
    └── plan.md
```

### Key Implementation Notes

**AI Integration:**
- Primary AI: Anthropic Claude 3.5 Sonnet (`claude-3-5-sonnet-20241022`)
- Used for: Conversations, grammar analysis, exercise generation
- API key stored in `.env` as `ANTHROPIC_API_KEY`

**Grammar System:**
- 50+ topics covering: cases, verb conjugation, sentence structure, articles, pronouns, adjectives, prepositions, passive voice
- 5 exercise types: fill-in-blank, multiple choice, translation (IT→DE), error correction, sentence building
- AI generates exercises on-demand + manual database of 200+ exercises
- Diagnostic test: 30 questions across main topics to assess level
- Drill sessions: 15+ exercises per topic with immediate feedback
- Conversation errors automatically mapped to grammar topics → trigger practice recommendations

**Spaced Repetition:**
- Vocabulary: Familiarity score 0.0-1.0, intervals from 1-14 days
- Grammar: Mastery level 0.0-1.0, more aggressive intervals (1-14 days), triggered by conversation errors

**Authentication:**
- JWT tokens with bcrypt password hashing
- Token expiration: 30 minutes (configurable)

**Performance Targets:**
- API endpoints: <200ms (excluding AI)
- AI conversation response: <3s
- Grammar analysis: <2s
- Exercise generation: <5s

### Current Development Phase: Phase 1 (Weeks 1-2)

**Phase 1 Objectives:**
1. Set up development environment
2. Create database with all tables (including grammar module)
3. Build FastAPI backend structure
4. Implement JWT authentication
5. Initialize React frontend with Vite + TypeScript
6. Configure Tailwind CSS
7. Set up Alembic migrations

**Next Steps:**
- Create directory structure
- Set up virtual environment
- Create requirements.txt
- Initialize PostgreSQL database
- Create SQLAlchemy models for all tables
- Set up Alembic migrations
- Create authentication system
- Initialize React app with Vite

### Environment Variables (.env)
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
```

### Development Commands

**Backend:**
```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run migrations
alembic upgrade head

# Seed data
python scripts/seed_grammar_data.py

# Start server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/
```

**Frontend:**
```bash
# Install dependencies
npm install

# Development server
npm run dev

# Build for production
npm run build
```

### Testing Strategy
- Unit tests for all service functions
- Integration tests for API endpoints
- Test coverage target: >80%
- Mock AI API calls in tests
- Focus on critical user flows:
  - Complete conversation session
  - Grammar diagnostic test
  - Grammar drill session (15 exercises)
  - Conversation → grammar practice trigger
  - Vocabulary review
  - Progress tracking accuracy

### Design Principles
1. **User-centric**: Designed specifically for Igor's learning goals (business German, grammar mastery)
2. **Immediate feedback**: Grammar corrections and exercise feedback shown instantly
3. **Adaptive learning**: Spaced repetition + conversation-triggered practice
4. **Comprehensive tracking**: Progress across conversation, grammar, and vocabulary
5. **Context-rich**: Business scenarios aligned with user's work domain

### Success Metrics
- User completes 5+ sessions per week (conversation + grammar combined)
- Vocabulary retention rate >80%
- Grammar mastery improvement measurable via diagnostic tests
- Conversation grammar accuracy improves over time
- Session completion rate >85%
- User satisfaction (self-assessed)

### Important Constraints
- Single-user application (no multi-tenancy in v1.0)
- Local deployment only (not cloud-hosted initially)
- German explanations for grammar (advanced learner preference)
- No voice/speech features in v1.0 (Phase 2)
- Focus on text-based interaction

### Reference Materials
- CEFR Level Descriptors (B2/C1 target)
- Duden Grammar Reference (German grammar rules)
- Anthropic Claude API Documentation
- FastAPI Documentation
- SQLAlchemy 2.0 Documentation

---

**For Claude Code Developers:**

When working on this project:
1. Always refer to BRD for detailed specifications
2. Follow the 10-week plan in `plan.md`
3. Check current phase before starting new work
4. Maintain test coverage >80%
5. Use type hints (Python) and TypeScript (frontend)
6. Write descriptive commit messages
7. Test grammar exercise generation quality carefully
8. Ensure grammar topics are properly mapped to conversation errors
9. Validate spaced repetition calculations (both vocab and grammar)

**CRITICAL REQUIREMENTS:**

1. **Testing is MANDATORY**
   - **Write tests for ALL code you create**
   - Tests must be written alongside the implementation, not after
   - Every service function MUST have corresponding unit tests
   - Every API endpoint MUST have integration tests
   - Test both success and failure cases
   - Mock external dependencies (AI API, database in unit tests)
   - Use pytest for backend, React Testing Library for frontend
   - Aim for >80% code coverage minimum
   - Run tests before considering any task complete

2. **Git Commits are MANDATORY**
   - **Commit ALL changes to the Git repository**
   - Commit after completing each logical unit of work
   - Write clear, descriptive commit messages in present tense
   - Format: `Add user authentication endpoints` or `Fix grammar exercise validation`
   - Commit frequently (multiple times per session)
   - Include both implementation AND test files in commits
   - Never leave uncommitted code
   - Use meaningful commit messages that explain WHAT and WHY

**Development Workflow (MANDATORY):**
1. Write code for feature/function
2. Write tests for the code (unit + integration as applicable)
3. Run tests and ensure they pass
4. Commit code + tests to Git with descriptive message
5. Move to next task

**Example Commit Flow:**
```bash
# After implementing user model
git add backend/app/models/user.py backend/tests/test_user_model.py
git commit -m "Add User model with authentication fields and validation tests"

# After implementing auth endpoints
git add backend/app/api/v1/auth.py backend/tests/test_auth_endpoints.py
git commit -m "Implement user registration and login endpoints with JWT tests"

# After implementing grammar service
git add backend/app/services/grammar_ai_service.py backend/tests/test_grammar_ai_service.py
git commit -m "Add grammar exercise generation service with AI integration tests"
```

**Phase 1 Priority Tasks:**
- Database setup with all tables including 6 grammar tables
- SQLAlchemy models (user, vocabulary, session, context, grammar, progress)
- Authentication endpoints
- Basic API structure
- Frontend initialization with React + TypeScript + Tailwind

---

Last Updated: 2026-01-17
Project Version: 1.0 (Phase 1 - Core Infrastructure)
