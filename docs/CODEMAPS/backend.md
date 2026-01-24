# Backend Architecture Codemap

**Last Updated:** 2026-01-22
**Entry Points:** `app/main.py`, `app/config.py`, `app/database.py`

## Overview

The German Learning Application backend is a production-ready FastAPI application with 74 REST API endpoints, 22 database models, and 5 service classes (3 AI-powered). It features comprehensive language learning capabilities including AI conversation practice, grammar drilling with 50+ topics, vocabulary management with 150+ words, and progress analytics with 31 achievements.

**Key Statistics:**
- **API Endpoints:** 74 across 7 router modules
- **Database Models:** 22 organized in 7 files (20 exported in __init__.py)
- **Services:** 5 (ConversationAI, GrammarAI, VocabularyAI, Analytics, Integration)
- **Tests:** 104 comprehensive tests (>80% coverage)
- **Lines of Code:** ~8,088 total (excluding tests)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT (Browser/Mobile)                   │
└────────────────────────┬────────────────────────────────────┘
                         │ HTTP/JSON
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                     FASTAPI APPLICATION                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Middleware Layer                      │  │
│  │  • CORS (Cross-Origin Resource Sharing)               │  │
│  │  • Request Logging (RotatingFileHandler)              │  │
│  │  • TrustedHost (Optional)                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                   API Router Layer                     │  │
│  │  /api/v1/auth      - Authentication (3 endpoints)      │  │
│  │  /api/sessions     - Conversations (4 endpoints)       │  │
│  │  /api/contexts     - Contexts (5 endpoints)            │  │
│  │  /api/grammar      - Grammar (14 endpoints)            │  │
│  │  /api/v1/vocabulary - Vocabulary (26 endpoints)        │  │
│  │  /api/v1/analytics  - Analytics (14 endpoints)         │  │
│  │  /api/v1/integration - Integration (3 endpoints)       │  │
│  │  /api/health       - Health Check (2 endpoints)        │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Dependency Injection Layer                │  │
│  │  • get_db() - Database session                         │  │
│  │  • get_current_user() - JWT authentication             │  │
│  │  • get_current_active_user() - Active user check       │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Service Layer                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │           AI Services (External API)            │  │  │
│  │  │  • ConversationAI - Claude conversations        │  │  │
│  │  │  • GrammarAIService - Exercise generation       │  │  │
│  │  │  • VocabularyAIService - Word analysis          │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │         Business Logic Services                 │  │  │
│  │  │  • AnalyticsService - Progress tracking         │  │  │
│  │  │  • IntegrationService - Cross-module workflows  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │                  Schema Layer (Pydantic)               │  │
│  │  • Request validation                                  │  │
│  │  • Response serialization                              │  │
│  │  • Type checking (50+ schema classes)                  │  │
│  └───────────────────────────────────────────────────────┘  │
│                         │                                    │
│                         ▼                                    │
│  ┌───────────────────────────────────────────────────────┐  │
│  │              Model Layer (SQLAlchemy ORM)              │  │
│  │  • 21 database models                                  │  │
│  │  • Relationship mapping                                │  │
│  │  • Query construction                                  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               POSTGRESQL DATABASE (21 Tables)                │
│  • Core: users, contexts, sessions, messages                │
│  • Grammar: 6 tables (topics, exercises, progress, etc.)    │
│  • Vocabulary: 7 tables (words, flashcards, quizzes, etc.)  │
│  • Analytics: 4 tables (achievements, stats, snapshots)     │
└─────────────────────────────────────────────────────────────┘

         ┌────────────────────────────────────┐
         │  EXTERNAL SERVICES                 │
         │  • Anthropic API (Claude Sonnet 4.5)│
         │  • Redis (optional caching)        │
         └────────────────────────────────────┘
```

## Directory Structure

```
backend/
├── app/                                    # Main application package
│   ├── main.py                             # FastAPI app, middleware, routes (114 lines)
│   ├── config.py                           # Settings management (48 lines)
│   ├── database.py                         # SQLAlchemy setup (60 lines)
│   │
│   ├── models/                             # Database models (855 lines total)
│   │   ├── __init__.py                     # Model exports (21 models)
│   │   ├── user.py                         # User model (35 lines)
│   │   ├── context.py                      # Context model (42 lines)
│   │   ├── session.py                      # Session, ConversationTurn (104 lines)
│   │   ├── grammar.py                      # 6 grammar models (279 lines)
│   │   ├── vocabulary.py                   # 7 vocabulary models (308 lines)
│   │   ├── achievement.py                  # Achievement, UserAchievement (55 lines)
│   │   └── progress.py                     # UserStats, ProgressSnapshot (32 lines)
│   │
│   ├── schemas/                            # Pydantic schemas (1,213 lines total)
│   │   ├── user.py                         # User schemas (45 lines)
│   │   ├── context.py                      # Context schemas (48 lines)
│   │   ├── session.py                      # Session, message schemas (89 lines)
│   │   ├── grammar.py                      # 20+ grammar schemas (412 lines)
│   │   ├── vocabulary.py                   # 22 vocabulary schemas (441 lines)
│   │   └── analytics.py                    # 30+ analytics schemas (178 lines)
│   │
│   ├── api/                                # API endpoints (3,319 lines total)
│   │   └── v1/
│   │       ├── __init__.py                 # Router exports
│   │       ├── deps.py                     # Dependency injection (29 lines)
│   │       ├── auth.py                     # Authentication (3 endpoints, 83 lines)
│   │       ├── sessions.py                 # Conversations (4 endpoints, 209 lines)
│   │       ├── contexts.py                 # Contexts (5 endpoints, 154 lines)
│   │       ├── grammar.py                  # Grammar (14 endpoints, 844 lines)
│   │       ├── vocabulary.py               # Vocabulary (26 endpoints, 1,417 lines)
│   │       ├── analytics.py                # Analytics (14 endpoints, 471 lines)
│   │       └── integration.py              # Integration (3 endpoints, 112 lines)
│   │
│   ├── services/                           # Business logic (2,701 lines total)
│   │   ├── ai_service.py                   # ConversationAI (478 lines)
│   │   ├── grammar_ai_service.py           # GrammarAIService (685 lines)
│   │   ├── vocabulary_ai_service.py        # VocabularyAIService (924 lines)
│   │   ├── analytics_service.py            # AnalyticsService (512 lines)
│   │   └── integration_service.py          # IntegrationService (102 lines)
│   │
│   └── utils/                              # Utilities
│       └── auth.py                         # JWT, password hashing (71 lines)
│
├── scripts/                                # Data seeding scripts
│   ├── seed_contexts.py                    # 12+ conversation contexts
│   ├── seed_grammar_data.py                # 50+ topics, 200+ exercises
│   ├── seed_vocabulary_data.py             # 150+ vocabulary words
│   └── seed_achievements.py                # 31 achievements (4 tiers)
│
├── tests/                                  # Test suite (104 tests, >80% coverage)
│   ├── conftest.py                         # Pytest fixtures
│   ├── test_auth.py                        # Authentication tests
│   ├── test_conversations.py               # Conversation tests
│   ├── test_contexts.py                    # Context tests
│   ├── test_grammar.py                     # Grammar tests (25 tests)
│   ├── test_vocabulary.py                  # Vocabulary tests (30 tests)
│   ├── test_analytics.py                   # Analytics tests (18 tests)
│   ├── test_integration.py                 # Integration tests (11 tests)
│   └── test_spaced_repetition.py           # Spaced repetition tests
│
├── alembic/                                # Database migrations
│   ├── versions/
│   │   ├── 001_initial_schema.py           # Initial database schema
│   │   ├── 001_update_vocabulary_schema.py # Vocabulary model alignment
│   │   └── 002_add_vocabulary_sessions.py  # Multi-worker session persistence
│   ├── env.py                              # Alembic environment
│   └── alembic.ini                         # Alembic configuration
│
├── logs/                                   # Application logs (rotating)
│   └── app.log                             # RotatingFileHandler (10MB, 5 backups)
│
├── requirements.txt                        # Python dependencies (43 lines)
├── .env.example                            # Environment variable template
└── README.md                               # Backend documentation
```

## Key Modules

### Application Core

| Module | Purpose | Key Exports | Lines | Dependencies |
|--------|---------|-------------|-------|--------------|
| `main.py` | FastAPI application entry point | `app` (FastAPI instance) | 114 | FastAPI, SQLAlchemy, all routers |
| `config.py` | Settings management from .env | `settings` (Settings instance) | 48 | Pydantic Settings |
| `database.py` | SQLAlchemy engine, session factory | `Base`, `engine`, `get_db()` | 60 | SQLAlchemy, Config |

### Models Layer (7 files, 855 lines)

| Module | Models | Purpose | Lines |
|--------|--------|---------|-------|
| `user.py` | User | User accounts with authentication | 35 |
| `context.py` | Context | Conversation scenarios (12+ default) | 42 |
| `session.py` | Session, ConversationTurn | Conversation sessions and messages | 104 |
| `grammar.py` | GrammarTopic, GrammarExercise, UserGrammarProgress, GrammarSession, GrammarExerciseAttempt, DiagnosticTest | Grammar learning system (6 models) | 279 |
| `vocabulary.py` | Vocabulary, UserVocabularyProgress, UserVocabularyList, VocabularyListWord, VocabularyReview, FlashcardSession, VocabularyQuiz, GrammarCorrection | Vocabulary management (9 models) | 308 |
| `achievement.py` | Achievement, UserAchievement | Gamification system | 55 |
| `progress.py` | UserStats, ProgressSnapshot | Analytics and tracking | 32 |

### Schemas Layer (6 files, 1,213 lines)

| Module | Schema Count | Purpose | Lines |
|--------|--------------|---------|-------|
| `user.py` | 4 | UserCreate, UserLogin, UserResponse, Token | 45 |
| `context.py` | 4 | ContextCreate, ContextUpdate, ContextResponse, ContextWithStats | 48 |
| `session.py` | 6 | SessionCreate, SessionResponse, MessageCreate, MessageResponse, etc. | 89 |
| `grammar.py` | 20+ | Topic, exercise, session, progress schemas | 412 |
| `vocabulary.py` | 22 | Word, flashcard, quiz, list, progress schemas | 441 |
| `analytics.py` | 30+ | Achievement, stats, heatmap, leaderboard schemas | 178 |

### API Layer (7 routers, 3,319 lines)

| Router | Endpoints | Purpose | Lines |
|--------|-----------|---------|-------|
| `auth.py` | 3 | User registration, login, profile | 83 |
| `sessions.py` | 4 | Start conversation, send message, end session, history | 209 |
| `contexts.py` | 5 | List, get, create, update, delete contexts | 154 |
| `grammar.py` | 14 | Topics, exercises, practice sessions, progress, diagnostics | 844 |
| `vocabulary.py` | 26 | Words, flashcards, quizzes, lists, progress, AI analysis | 1,417 |
| `analytics.py` | 14 | Progress, achievements, heatmaps, leaderboards, stats | 471 |
| `integration.py` | 3 | Session analysis, learning paths, unified dashboard | 112 |

### Service Layer (5 services, 2,701 lines)

| Service | Type | Purpose | Key Methods | Lines |
|---------|------|---------|-------------|-------|
| `ai_service.py` | AI | Conversation practice with Claude | `generate_response()`, `analyze_grammar()`, `detect_vocabulary()` | 478 |
| `grammar_ai_service.py` | AI | Grammar exercise generation | `generate_exercises()`, `evaluate_answer()`, `explain_grammar_error()` | 685 |
| `vocabulary_ai_service.py` | AI | Word analysis and quiz generation | `analyze_word()`, `detect_vocabulary()`, `generate_flashcard()`, `generate_quiz()` | 924 |
| `analytics_service.py` | Business Logic | Progress tracking and achievements | `get_overall_progress()`, `analyze_errors()`, `generate_heatmap()` | 512 |
| `integration_service.py` | Business Logic | Cross-module workflows | `analyze_conversation_session()`, `get_learning_path()`, `get_dashboard_data()` | 102 |

## Application Entry Point

### main.py Structure

```python
# 1. Imports and Logging Setup
- Rotating file handler (10MB max, 5 backups)
- Logs to logs/app.log
- INFO level by default

# 2. FastAPI Application
app = FastAPI(
    title="German Learning App",
    description="AI-powered German learning...",
    version="1.0.0"
)

# 3. Middleware Configuration
- CORSMiddleware (configurable origins)
- Request logging middleware (logs all HTTP requests)

# 4. Health Check Endpoints
GET /              - API information
GET /api/health    - Health check (DB + AI status)

# 5. Router Registration (7 routers)
/api/v1/auth        - Authentication
/api/sessions       - Conversations
/api/contexts       - Contexts
/api/grammar        - Grammar module
/api/v1/vocabulary  - Vocabulary module
/api/v1/analytics   - Analytics module
/api/v1/integration - Integration module
```

### Health Check Response
```json
{
  "status": "healthy|degraded",
  "environment": "development|production",
  "database": "connected|disconnected|error: ...",
  "ai_service": "configured|not_configured"
}
```

## Configuration Management

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost/german_learning

# AI Services
ANTHROPIC_API_KEY=sk-ant-...
AI_MODEL=claude-sonnet-4-5  # Auto-updating Claude Sonnet 4.5

# Security (generate with: openssl rand -hex 32)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
APP_NAME=German Learning App
DEBUG=False  # Set to False in production
ENVIRONMENT=production

# CORS (comma-separated frontend URLs)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Redis (optional)
REDIS_HOST=localhost
REDIS_PORT=6379
```

### Settings Class (config.py)

- **BaseSettings** from Pydantic Settings for type-safe config
- **Automatic .env loading** via `env_file = ".env"`
- **CORS parsing** with `cors_origins_list` property
- **Type validation** for all settings
- **Default values** for optional settings

## Database Configuration

### Connection Pooling (database.py)

```python
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Maintain 10 connections
    max_overflow=20,        # Allow 20 additional connections
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=settings.DEBUG     # Log SQL queries in debug mode
)
```

### Session Factory

- **sessionmaker** with `autocommit=False`, `autoflush=False`
- **get_db()** dependency for FastAPI route injection
- **Automatic session cleanup** via try/finally

### Base Model

- **declarative_base()** for all ORM models
- **Shared across all model files** via `from app.database import Base`

## Testing Structure

### Test Organization (104 tests total)

| Test File | Tests | Coverage | Purpose |
|-----------|-------|----------|---------|
| `test_auth.py` | 8 | Auth endpoints | Registration, login, JWT validation |
| `test_conversations.py` | 12 | Conversation flow | Start, message, end session, AI integration |
| `test_contexts.py` | 8 | Context CRUD | List, get, create, update, delete |
| `test_grammar.py` | 25 | Grammar module | Topics, exercises, sessions, progress, AI generation |
| `test_vocabulary.py` | 30 | Vocabulary module | Words, flashcards, quizzes, lists, reviews, AI analysis |
| `test_analytics.py` | 18 | Analytics module | Achievements, stats, heatmaps, leaderboards, progress |
| `test_integration.py` | 11 | Cross-module workflows | Session analysis, learning paths, dashboard |
| `test_spaced_repetition.py` | 6 | Spaced repetition algorithms | Grammar and vocabulary mastery tracking |

### Test Patterns

```python
# 1. Fixture-based setup (conftest.py)
@pytest.fixture
def db_session():
    # Test database setup

# 2. Mocked AI services (avoid API calls)
with patch('app.services.ai_service.Anthropic'):
    # Test with mocked Claude API

# 3. FastAPI TestClient
from fastapi.testclient import TestClient
client = TestClient(app)
response = client.get("/api/health")

# 4. Database-backed tests
# All tests use real PostgreSQL with test fixtures
# No in-memory dictionaries for session storage
```

## External Dependencies

### Core Framework (requirements.txt)

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | >=0.104.0 | Web framework with async support |
| `uvicorn[standard]` | >=0.24.0 | ASGI server with WebSocket support |
| `python-multipart` | >=0.0.6 | Form data parsing |

### Database

| Package | Version | Purpose |
|---------|---------|---------|
| `sqlalchemy` | >=2.0.0 | ORM with async support |
| `alembic` | >=1.12.0 | Database migrations |
| `psycopg2-binary` | >=2.9.9 | PostgreSQL adapter |

### Validation & Schemas

| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic` | >=2.4.0 | Data validation and serialization |
| `pydantic-settings` | >=2.0.0 | Settings management from .env |
| `email-validator` | >=2.0.0 | Email validation |

### Authentication

| Package | Version | Purpose |
|---------|---------|---------|
| `python-jose[cryptography]` | >=3.3.0 | JWT token generation/validation |
| `passlib[bcrypt]` | >=1.7.4 | Password hashing |
| `bcrypt` | ==4.2.0 | Bcrypt algorithm (pinned for compatibility) |

### AI Integration

| Package | Version | Purpose |
|---------|---------|---------|
| `anthropic` | >=0.5.0 | Anthropic Claude API client |

### Optional Services

| Package | Version | Purpose |
|---------|---------|---------|
| `redis` | >=5.0.0 | Caching layer (optional) |
| `celery` | >=5.3.0 | Task queue (optional) |

### Testing

| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | >=7.4.0 | Testing framework |
| `pytest-asyncio` | >=0.21.0 | Async test support |
| `pytest-cov` | >=4.1.0 | Code coverage reporting |
| `httpx` | >=0.25.0 | HTTP client for API testing |

### Development Tools

| Package | Version | Purpose |
|---------|---------|---------|
| `black` | >=23.10.0 | Code formatting |
| `flake8` | >=6.1.0 | Linting |
| `mypy` | >=1.6.0 | Type checking |
| `python-dotenv` | >=1.0.0 | .env file loading |

## Key Implementation Patterns

### 1. Dependency Injection

```python
# api/v1/deps.py
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    # JWT validation and user lookup

# Usage in routes
@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user
```

### 2. Service Pattern

```python
# Services encapsulate business logic
class GrammarAIService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)

    def generate_exercises(self, topic: str) -> List[Exercise]:
        # AI-powered exercise generation

# Routes use services
@router.post("/generate-exercises")
def generate_exercises(db: Session = Depends(get_db)):
    service = GrammarAIService(settings.ANTHROPIC_API_KEY)
    return service.generate_exercises(...)
```

### 3. Database Session Management

```python
# Automatic session cleanup via dependency
@router.get("/items")
def get_items(db: Session = Depends(get_db)):
    # Session automatically closed after request
    return db.query(Item).all()
```

### 4. Error Handling

```python
# HTTPException for API errors
if not user:
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

# Pydantic validation errors (automatic)
class UserCreate(BaseModel):
    email: EmailStr  # Automatic email validation
    password: str = Field(min_length=8)
```

### 5. Multi-Worker Session Persistence

```python
# Database-backed sessions (not in-memory dictionaries)
class FlashcardSession(Base):
    __tablename__ = "flashcard_sessions"
    id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    cards_data = Column(Text)  # JSON serialized

# Safe for multiple Uvicorn workers
# Sessions persist across server restarts
```

## Production Deployment

### Systemd Service

```ini
[Unit]
Description=German Learning App Backend
After=network.target postgresql.service

[Service]
Type=notify
User=german-app
WorkingDirectory=/opt/german-learning-app/backend
ExecStart=/opt/german-learning-app/backend/venv/bin/uvicorn app.main:app \
    --host 0.0.0.0 --port 8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

### Nginx Reverse Proxy

```nginx
upstream german_learning {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://german_learning;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Production Environment

- **Python 3.10+** (tested on Ubuntu 20.04 LTS)
- **PostgreSQL 12+** (15+ recommended)
- **Uvicorn with 3+ workers** (multi-worker safe)
- **Nginx as reverse proxy** (optional)
- **SSL/TLS with Let's Encrypt** (recommended)

## Common Development Tasks

### Start Development Server

```bash
cd backend
source venv/bin/activate  # If using virtual environment
uvicorn app.main:app --reload --port 8000
```

### Run Database Migrations

```bash
cd backend
alembic upgrade head  # Apply all migrations
alembic downgrade -1  # Rollback one migration
```

### Seed Initial Data

```bash
cd backend
python scripts/seed_contexts.py      # 12+ conversation contexts
python scripts/seed_grammar_data.py  # 50+ topics, 200+ exercises
python scripts/seed_vocabulary_data.py  # 150+ vocabulary words
python scripts/seed_achievements.py  # 31 achievements
```

### Run Tests

```bash
cd backend
pytest tests/ -v                # Run all tests with verbose output
pytest tests/test_grammar.py -v  # Run specific test file
pytest --cov=app tests/         # Generate coverage report
```

### API Documentation

- **Swagger UI:** http://localhost:8000/docs (interactive API testing)
- **ReDoc:** http://localhost:8000/redoc (alternative documentation format)

## Related Areas

- **[Database Schema](backend-database.md)** - Complete database model documentation with relationships
- **[API Architecture](backend-api.md)** - Service layer and endpoint organization
- **[Deployment Guide](/docs/GUIDES/deployment/DEPLOYMENT_GUIDE.md)** - Production deployment walkthrough
- **[Troubleshooting Guide](/docs/GUIDES/troubleshooting/TROUBLESHOOTING.md)** - Common issues and solutions

---

**Architecture Summary:**

The backend follows a clean layered architecture with clear separation of concerns:
1. **API Layer** (FastAPI routers) handles HTTP requests and responses
2. **Schema Layer** (Pydantic) validates and serializes data
3. **Service Layer** encapsulates business logic and external API calls
4. **Model Layer** (SQLAlchemy ORM) manages database operations
5. **Database Layer** (PostgreSQL) persists all application data

This design enables easy testing (mock services), maintainability (isolated layers), and scalability (stateless API, database-backed sessions).
