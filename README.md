# German Learning Application (myGermanAITeacher)

An AI-powered German language learning application for advanced learners (B2/C1 level) with comprehensive grammar drilling, conversation practice, and vocabulary management.

## Features

- **AI Conversation Practice**: Interactive conversations with Anthropic Claude in various business and daily life contexts
- **Grammar Learning System**: Diagnostic tests, 50+ grammar topics, targeted drilling with 15+ exercises per topic
- **Vocabulary Management**: 500+ words with spaced repetition algorithm
- **Progress Analytics**: Comprehensive tracking across all modules with mastery heatmaps

## Technology Stack

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

## Project Structure

```
myGermanAITeacher/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy database models
│   │   ├── schemas/         # Pydantic validation schemas
│   │   ├── api/v1/          # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── utils/           # Utility functions
│   │   ├── main.py          # FastAPI application
│   │   ├── config.py        # Configuration management
│   │   └── database.py      # Database setup
│   ├── alembic/             # Database migrations
│   ├── tests/               # Unit and integration tests
│   ├── scripts/             # Seed and utility scripts
│   └── requirements.txt     # Python dependencies
├── frontend/                # React frontend (to be implemented)
└── brd and planning documents/
    ├── german_learning_app_brd.md
    └── plan.md
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- PostgreSQL 15 or higher
- Git

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd myGermanAITeacher
   ```

2. **Create and activate virtual environment**
   ```bash
   cd backend
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env

   # Edit .env and add your configuration:
   # - DATABASE_URL (PostgreSQL connection string)
   # - ANTHROPIC_API_KEY (your Claude API key)
   # - SECRET_KEY (generate with: openssl rand -hex 32)
   ```

5. **Create PostgreSQL database**
   ```bash
   # Using psql or your preferred PostgreSQL client
   createdb german_learning
   ```

6. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

7. **Run the development server**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The API will be available at http://localhost:8000

8. **View API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development Workflow

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply migrations
alembic upgrade head

# Revert last migration
alembic downgrade -1

# View migration history
alembic history
```

### Code Quality

```bash
# Format code with black
black app/ tests/

# Lint with flake8
flake8 app/ tests/

# Type checking with mypy
mypy app/
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Health Check
- `GET /` - API information
- `GET /api/health` - Health check endpoint

*More endpoints will be added in subsequent phases*

## Database Schema

The application uses PostgreSQL with the following main tables:

**Core Tables:**
- `users` - User accounts and authentication
- `contexts` - Conversation scenarios
- `vocabulary` - German words with translations
- `user_vocabulary` - User's vocabulary progress
- `sessions` - Practice sessions
- `conversation_turns` - Individual messages

**Grammar Module (6 tables):**
- `grammar_topics` - 50+ grammar topics
- `grammar_exercises` - Exercise database
- `user_grammar_progress` - Mastery levels per topic
- `grammar_sessions` - Drill practice sessions
- `grammar_exercise_attempts` - Exercise answers
- `diagnostic_tests` - Assessment results

**Analytics:**
- `progress_snapshots` - Daily/weekly metrics
- `grammar_corrections` - Error tracking

## Current Development Phase

**Phase 1: Core Infrastructure** ✅ (Completed)
- Backend directory structure
- Database models and migrations
- Authentication system with JWT
- Basic API structure
- Test infrastructure

**Next: Phase 2 - AI Integration & Conversation Engine**

## Contributing

This is a personal learning project. See `.claude/claude.md` for development guidelines.

## License

Private project - All rights reserved

## Contact

Igor - German language learner and developer
