# Backend API Architecture Codemap

**Last Updated:** 2026-01-22
**Entry Points:** `app/api/v1/__init__.py`, `app/main.py` (router registration), `app/api/deps.py` (dependency injection)

## Overview

The German Learning Application API is built on FastAPI with 74 REST endpoints organized across 7 router modules. The architecture follows a service-oriented pattern with dependency injection for authentication and database sessions. Three AI-powered services (ConversationAI, GrammarAIService, VocabularyAIService) integrate with Anthropic Claude Sonnet 4.5, while two business logic services (AnalyticsService, IntegrationService) handle progress tracking and cross-module workflows.

**API Statistics:**
- **Total Endpoints:** 74
- **Router Modules:** 7 (auth, sessions, contexts, grammar, vocabulary, analytics, integration)
- **Service Classes:** 5 (3 AI-powered, 2 business logic)
- **AI Methods:** 15+ methods across 3 services
- **Analytics Methods:** 15+ progress tracking methods
- **Authentication:** JWT with bcrypt password hashing

## API Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      CLIENT REQUEST                              │
│              (HTTP/JSON with optional JWT token)                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI APPLICATION                           │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                   MIDDLEWARE                              │  │
│  │  • CORS (Cross-Origin Resource Sharing)                  │  │
│  │  • Request Logging (RotatingFileHandler)                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │               ROUTER LAYER (7 Modules)                    │  │
│  │                                                            │  │
│  │  /api/v1/auth      ──► auth.py        (3 endpoints)       │  │
│  │  /api/sessions     ──► sessions.py    (4 endpoints)       │  │
│  │  /api/contexts     ──► contexts.py    (5 endpoints)       │  │
│  │  /api/grammar      ──► grammar.py     (14 endpoints)      │  │
│  │  /api/v1/vocabulary ──► vocabulary.py (26 endpoints)      │  │
│  │  /api/v1/analytics  ──► analytics.py  (14 endpoints)      │  │
│  │  /api/v1/integration ──► integration.py (3 endpoints)     │  │
│  │  /api/health       ──► main.py        (2 endpoints)       │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         DEPENDENCY INJECTION (deps.py)                    │  │
│  │                                                            │  │
│  │  get_db() ──────────────► SQLAlchemy Session              │  │
│  │  get_current_user() ────► JWT decode + DB lookup          │  │
│  │  get_current_active_user() ► Active user check            │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              ROUTE HANDLER FUNCTIONS                      │  │
│  │  • Request validation (Pydantic schemas)                  │  │
│  │  • Authentication check (if protected)                    │  │
│  │  • Business logic delegation to services                  │  │
│  │  • Response serialization                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                SERVICE LAYER                              │  │
│  │                                                            │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │         AI SERVICES (External API)               │    │  │
│  │  │                                                   │    │  │
│  │  │  ConversationAI:                                 │    │  │
│  │  │    • generate_response()                         │    │  │
│  │  │    • analyze_grammar()                           │    │  │
│  │  │    • detect_vocabulary()                         │    │  │
│  │  │                                                   │    │  │
│  │  │  GrammarAIService:                               │    │  │
│  │  │    • generate_exercises()                        │    │  │
│  │  │    • evaluate_answer()                           │    │  │
│  │  │    • explain_grammar_error()                     │    │  │
│  │  │                                                   │    │  │
│  │  │  VocabularyAIService:                            │    │  │
│  │  │    • analyze_word()                              │    │  │
│  │  │    • detect_vocabulary()                         │    │  │
│  │  │    • generate_flashcard()                        │    │  │
│  │  │    • generate_quiz()                             │    │  │
│  │  │    • generate_example_sentences()                │    │  │
│  │  │    • suggest_related_words()                     │    │  │
│  │  │                                                   │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  │                         │                                  │  │
│  │                         ▼                                  │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │      BUSINESS LOGIC SERVICES (Database)          │    │  │
│  │  │                                                   │    │  │
│  │  │  AnalyticsService:                               │    │  │
│  │  │    • get_overall_progress()                      │    │  │
│  │  │    • analyze_error_patterns()                    │    │  │
│  │  │    • analyze_improvement_trends()                │    │  │
│  │  │    • generate_activity_heatmap()                 │    │  │
│  │  │    • generate_grammar_mastery_heatmap()          │    │  │
│  │  │    • get_leaderboard_rankings()                  │    │  │
│  │  │    • check_achievements()                        │    │  │
│  │  │                                                   │    │  │
│  │  │  IntegrationService:                             │    │  │
│  │  │    • analyze_conversation_session()              │    │  │
│  │  │    • get_learning_path()                         │    │  │
│  │  │    • get_dashboard_data()                        │    │  │
│  │  │                                                   │    │  │
│  │  └──────────────────────────────────────────────────┘    │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            SCHEMA LAYER (Pydantic Validation)             │  │
│  │  • Request validation (UserCreate, SessionCreate, etc.)   │  │
│  │  • Response serialization (UserResponse, etc.)            │  │
│  │  • Type checking (50+ schema classes)                     │  │
│  └──────────────────────────────────────────────────────────┘  │
│                         │                                        │
│                         ▼                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │          MODEL LAYER (SQLAlchemy ORM Queries)             │  │
│  │  • Database queries (SELECT, INSERT, UPDATE, DELETE)      │  │
│  │  • Relationship loading                                   │  │
│  │  • Transaction management                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   POSTGRESQL DATABASE                            │
│  • 19 tables, 35+ foreign keys                                  │
│  • Connection pooling (QueuePool: size=10, max_overflow=20)     │
└─────────────────────────────────────────────────────────────────┘

         ┌────────────────────────────────────┐
         │  EXTERNAL SERVICES                 │
         │  • Anthropic Claude Sonnet 4.5     │
         │    (AI conversation, analysis)     │
         └────────────────────────────────────┘
```

## Service Layer Architecture

### AI Services (3 services, external API dependency)

#### ConversationAI (app/services/ai_service.py)

```python
class ConversationAI:
    """AI-powered conversation generation and analysis."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or settings.ANTHROPIC_API_KEY)
        self.model = settings.AI_MODEL  # claude-sonnet-4-5
```

**Key Methods:**

| Method | Purpose | Inputs | Returns | AI Model |
|--------|---------|--------|---------|----------|
| `generate_response()` | Generate AI response in conversation | context_prompt, conversation_history, user_message, user_level | AI response text | Claude Sonnet 4.5 |
| `analyze_grammar()` | Detect grammar errors in user message | user_message, user_level, context_name | List of grammar corrections | Claude Sonnet 4.5 |
| `detect_vocabulary()` | Extract vocabulary words from text | text, user_level | List of detected words | Claude Sonnet 4.5 |

**System Prompt Pattern:**
```python
system_prompt = f"""You are a German language conversation partner helping an advanced learner (level {user_level}).

Context: {context_prompt}

Guidelines:
- Respond naturally in German appropriate to the context
- Match the user's proficiency level ({user_level})
- Use vocabulary relevant to the scenario
- Keep responses conversational (2-4 sentences)
"""
```

#### GrammarAIService (app/services/grammar_ai_service.py)

```python
class GrammarAIService:
    """AI-powered grammar exercise generation and feedback."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or settings.ANTHROPIC_API_KEY)
        self.model = settings.AI_MODEL  # claude-sonnet-4-5
```

**Key Methods:**

| Method | Purpose | Inputs | Returns | AI Model |
|--------|---------|--------|---------|----------|
| `generate_exercises()` | Generate exercises for a grammar topic | topic_name, topic_explanation, difficulty_level, exercise_type, count, context_category | List of exercise dictionaries | Claude Sonnet 4.5 |
| `evaluate_answer()` | Evaluate user's exercise answer | exercise_question, user_answer, correct_answer, topic_name | Evaluation with feedback | Claude Sonnet 4.5 |
| `explain_grammar_error()` | Explain why an answer is incorrect | exercise_question, user_answer, correct_answer, topic_name, topic_explanation | Detailed explanation | Claude Sonnet 4.5 |
| `generate_hint()` | Generate progressive hint for exercise | exercise_question, correct_answer, hint_number | Context-appropriate hint | Claude Sonnet 4.5 |

**Exercise Types Supported:**
- `fill_blank` - Fill-in-the-blank exercises
- `multiple_choice` - Multiple choice questions
- `translation` - Translation exercises (Italian ↔ German)
- `error_correction` - Find and correct errors
- `sentence_building` - Construct sentences from words

**JSON Response Format:**
```json
[
  {
    "question_text": "Die Frage oder der Satz",
    "correct_answer": "Die richtige Antwort",
    "alternative_answers": ["alternative 1", "alternative 2"],
    "explanation_de": "Detaillierte Erklärung auf Deutsch",
    "hints": ["Hinweis 1", "Hinweis 2"]
  }
]
```

#### VocabularyAIService (app/services/vocabulary_ai_service.py)

```python
class VocabularyAIService:
    """AI-powered vocabulary analysis and learning."""

    def __init__(self, api_key: Optional[str] = None):
        self.client = Anthropic(api_key=api_key or settings.ANTHROPIC_API_KEY)
        self.model = settings.AI_MODEL  # claude-sonnet-4-5
```

**Key Methods:**

| Method | Purpose | Inputs | Returns | AI Model |
|--------|---------|--------|---------|----------|
| `analyze_word()` | Comprehensive word analysis | word, user_level, include_examples | Dictionary with translations, grammar, usage | Claude Sonnet 4.5 |
| `detect_vocabulary()` | Extract vocabulary from text | text, user_level, category | List of detected vocabulary words | Claude Sonnet 4.5 |
| `generate_flashcard()` | Create flashcard for a word | word, card_type, user_level | Flashcard data (question, answer, hint) | Claude Sonnet 4.5 |
| `generate_quiz()` | Generate vocabulary quiz | words, quiz_type, count | Quiz questions with answers | Claude Sonnet 4.5 |
| `generate_example_sentences()` | Create example sentences | word, count, context | List of example sentences (DE + IT) | Claude Sonnet 4.5 |
| `suggest_related_words()` | Suggest related vocabulary | word, relation_type, count | List of related words | Claude Sonnet 4.5 |
| `recommend_words_for_context()` | Recommend words for scenario | context_name, difficulty_level, count | List of recommended words | Claude Sonnet 4.5 |

**Word Analysis Response:**
```json
{
  "word": "das Konto",
  "translation_it": "il conto",
  "part_of_speech": "noun",
  "gender": "neuter",
  "plural_form": "die Konten",
  "difficulty_level": "B1",
  "pronunciation": "ˈkɔntoː",
  "definition_de": "Ein Konto bei einer Bank",
  "usage_notes": "Wichtig im Finanzbereich",
  "synonyms": ["das Bankkonto"],
  "antonyms": [],
  "examples": [
    {"de": "Ich eröffne ein Konto.", "it": "Apro un conto."}
  ],
  "is_compound": false,
  "register": "neutral",
  "frequency": "very_common"
}
```

### Business Logic Services (2 services, database-focused)

#### AnalyticsService (app/services/analytics_service.py)

```python
class AnalyticsService:
    """Comprehensive progress tracking and analysis."""

    def __init__(self, db: Session):
        self.db = db
```

**Key Methods:**

| Method | Purpose | Database Tables | Returns |
|--------|---------|-----------------|---------|
| `get_overall_progress()` | Overall progress across all modules | ConversationSession, GrammarSession, UserVocabularyProgress | Combined progress metrics |
| `analyze_error_patterns()` | Identify recurring grammar errors | GrammarCorrection, GrammarExerciseAttempt | Error patterns with frequency |
| `analyze_improvement_trends()` | Track improvement over time | ProgressSnapshot, UserGrammarProgress | Trend analysis |
| `generate_activity_heatmap()` | 365-day activity heatmap | ConversationSession, GrammarSession, VocabularyReview | Date → activity count map |
| `generate_grammar_mastery_heatmap()` | Grammar topic mastery heatmap | UserGrammarProgress, GrammarTopic | Topic → mastery level map |
| `get_leaderboard_rankings()` | Leaderboard by type | UserStats | Ranked user list |
| `check_achievements()` | Check and award achievements | UserAchievement, Achievement, UserStats | Newly earned achievements |
| `create_progress_snapshot()` | Create point-in-time snapshot | All progress tables | ProgressSnapshot record |
| `get_due_items()` | Get items due for review | UserGrammarProgress, UserVocabularyProgress | Due topics and words |

**Overall Progress Score Calculation:**
```python
# Combined score from 3 modules (0-100)
overall_score = (
    conversation_score * 0.3 +
    grammar_score * 0.4 +
    vocabulary_score * 0.3
)
```

**Heatmap Data Format:**
```python
# Activity heatmap (365 days)
{
  "2026-01-15": {"conversations": 2, "grammar": 3, "vocabulary": 5},
  "2026-01-16": {"conversations": 1, "grammar": 2, "vocabulary": 3},
  ...
}

# Grammar mastery heatmap
{
  "cases": {"Nominative": 0.8, "Accusative": 0.6, "Dative": 0.4},
  "verbs": {"Present": 0.9, "Past": 0.7, "Future": 0.5},
  ...
}
```

#### IntegrationService (app/services/integration_service.py)

```python
class IntegrationService:
    """Cross-module workflows and intelligent recommendations."""

    def __init__(self, db: Session):
        self.db = db
        self.analytics = AnalyticsService(db)
```

**Key Methods:**

| Method | Purpose | Data Sources | Returns |
|--------|---------|--------------|---------|
| `analyze_conversation_session()` | Analyze session with recommendations | Session, ConversationTurn, GrammarCorrection | Session analysis + grammar/vocab recommendations |
| `get_learning_path()` | Personalized daily/weekly plan | UserGrammarProgress, UserVocabularyProgress, UserStats | Daily/weekly learning goals |
| `get_dashboard_data()` | Unified dashboard data | All modules | Due items, recent activity, quick actions |

**Learning Path Format:**
```python
{
  "daily_plan": {
    "total_duration_minutes": 75,
    "vocabulary_review": {"duration": 15, "due_words": 12},
    "grammar_practice": {"duration": 30, "due_topics": 3},
    "conversation": {"duration": 30, "recommended_context": "Business Meeting"}
  },
  "weekly_goals": {
    "target_sessions": 5,
    "conversation_sessions": 2,
    "grammar_sessions": 2,
    "vocabulary_sessions": 1
  }
}
```

## Service Dependencies Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL DEPENDENCIES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────┐           │
│  │         Anthropic Claude API                      │           │
│  │  • Model: claude-sonnet-4-5 (auto-updating)      │           │
│  │  • Pricing: $3/M input, $15/M output tokens      │           │
│  │  • Used by: ConversationAI, GrammarAIService,    │           │
│  │             VocabularyAIService                   │           │
│  └──────────────────────────────────────────────────┘           │
│                         ▲                                        │
│                         │ API calls via anthropic SDK            │
│                         │                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────┼────────────────────────────────────────┐
│                    SERVICE LAYER                                 │
├─────────────────────────┼────────────────────────────────────────┤
│                         │                                        │
│  ┌──────────────────────┴───────────────────────┐               │
│  │         AI SERVICES (3 classes)              │               │
│  │  • ConversationAI                            │               │
│  │  • GrammarAIService                          │               │
│  │  • VocabularyAIService                       │               │
│  └──────────────────────────────────────────────┘               │
│                                                                  │
│  ┌──────────────────────────────────────────────┐               │
│  │    BUSINESS LOGIC SERVICES (2 classes)       │               │
│  │  • AnalyticsService ───► Uses all DB models  │               │
│  │  • IntegrationService ─► Uses AnalyticsService│              │
│  │                          + all DB models      │               │
│  └──────────────────────────────────────────────┘               │
│                         │                                        │
│                         ▼                                        │
└─────────────────────────┼────────────────────────────────────────┘
                          │
                          │
┌─────────────────────────┼────────────────────────────────────────┐
│                 DATABASE LAYER (PostgreSQL)                      │
├─────────────────────────┼────────────────────────────────────────┤
│                         │                                        │
│  ┌──────────────────────▼───────────────────────┐               │
│  │           SQLAlchemy ORM Models               │               │
│  │  • 19 tables, 35+ relationships               │               │
│  │  • Connection pooling (size=10, overflow=20)  │               │
│  └──────────────────────────────────────────────┘               │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**Service Composition:**
- `IntegrationService` → depends on `AnalyticsService`
- `AnalyticsService` → depends on database session
- All AI services → depend on Anthropic API client
- All API endpoints → instantiate services as needed

## API Endpoints by Module

### Authentication (3 endpoints) - /api/v1/auth

| Method | Endpoint | Purpose | Auth Required | Request Body | Response |
|--------|----------|---------|---------------|--------------|----------|
| POST | `/register` | Register new user | No | UserCreate | UserResponse (201) |
| POST | `/login` | User login | No | OAuth2PasswordRequestForm | Token |
| GET | `/me` | Get current user profile | Yes | - | UserResponse |

**Authentication Flow:**
```python
# 1. Register
POST /api/v1/auth/register
{
  "username": "igor",
  "email": "igor@example.com",
  "password": "secure_password"
}
→ bcrypt.hash(password) → save to database

# 2. Login
POST /api/v1/auth/login
{
  "username": "igor",
  "password": "secure_password"
}
→ verify_password(plain, hashed)
→ create_access_token({"sub": str(user.id)})
→ return {"access_token": "eyJ...", "token_type": "bearer"}

# 3. Protected endpoints
GET /api/v1/auth/me
Authorization: Bearer eyJ...
→ decode_access_token(token)
→ query user from database
→ return user data
```

### Conversations (4 endpoints) - /api/sessions

| Method | Endpoint | Purpose | Auth Required | Request Body | Response |
|--------|----------|---------|---------------|--------------|----------|
| POST | `/start` | Start conversation session | Yes | SessionCreate | SessionResponse |
| POST | `/{id}/message` | Send message in session | Yes | MessageCreate | MessageResponse |
| POST | `/{id}/end` | End session | Yes | - | SessionResponse |
| GET | `/history` | List user's sessions | Yes | - | List[SessionResponse] |

**Conversation Flow:**
```
1. POST /api/sessions/start
   → Create Session record
   → Return session_id

2. POST /api/sessions/{session_id}/message
   → ConversationAI.generate_response()
   → ConversationAI.analyze_grammar()
   → ConversationAI.detect_vocabulary()
   → Store ConversationTurn (user + AI)
   → Return AI response with feedback

3. POST /api/sessions/{session_id}/end
   → Calculate session metrics
   → Update Session record (ended_at, scores)
   → Check for achievements
```

### Contexts (5 endpoints) - /api/contexts

| Method | Endpoint | Purpose | Auth Required | Request Body | Response |
|--------|----------|---------|---------------|--------------|----------|
| GET | `/` | List all contexts | No | Query: category, difficulty | List[ContextResponse] |
| GET | `/{id}` | Get context details | No | - | ContextWithStats |
| POST | `/` | Create custom context | Yes | ContextCreate | ContextResponse (201) |
| PUT | `/{id}` | Update context | Yes | ContextUpdate | ContextResponse |
| DELETE | `/{id}` | Deactivate context | Yes | - | 204 No Content |

### Grammar (14 endpoints) - /api/grammar

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/topics` | List all topics | No | Filter by category, difficulty |
| GET | `/topics/{id}` | Get topic details | No | Includes exercises count |
| POST | `/practice/start` | Start practice session | Yes | Filter by topic_ids, difficulty |
| GET | `/practice/{session_id}/next` | Get next exercise | Yes | Returns exercise with hints |
| POST | `/practice/{session_id}/answer` | Submit answer | Yes | Evaluate answer, update progress |
| POST | `/practice/{session_id}/end` | End practice session | Yes | Calculate accuracy, update mastery |
| GET | `/progress` | Get overall progress | Yes | All topics with mastery levels |
| GET | `/progress/topic/{topic_id}` | Get topic progress | Yes | Detailed progress for one topic |
| POST | `/generate-exercises` | AI-generate exercises | Yes | GrammarAIService.generate_exercises() |
| GET | `/categories` | List categories | No | Distinct categories from topics |
| GET | `/recommendations` | Get practice recommendations | Yes | Based on weak areas and due dates |
| GET | `/review-queue` | Get due topics | Yes | Topics due for spaced repetition |
| POST | `/diagnostic/start` | Start diagnostic test | Yes | Assessment across all topics |
| POST | `/diagnostic/complete` | Complete diagnostic | Yes | Determine level, identify weak areas |

**Practice Session Flow:**
```
1. POST /api/grammar/practice/start
   → Create GrammarSession
   → Select exercises (filter by topic_ids, difficulty)
   → Return session_id

2. GET /api/grammar/practice/{session_id}/next
   → Get next exercise from session
   → Return exercise data

3. POST /api/grammar/practice/{session_id}/answer
   → Evaluate answer (exact match or AI evaluation)
   → Store GrammarExerciseAttempt
   → Update UserGrammarProgress
   → Return feedback

4. POST /api/grammar/practice/{session_id}/end
   → Calculate accuracy_rate
   → Update mastery_level
   → Update next_review_date (spaced repetition)
   → Check achievements
```

### Vocabulary (26 endpoints) - /api/v1/vocabulary

**Words (7 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/words` | List words | Yes | Filter by category, difficulty, mastery |
| GET | `/words/{id}` | Get word details | Yes | Include user progress |
| POST | `/words` | Create word | Yes | Add to vocabulary database |
| PUT | `/words/{id}` | Update word | Yes | Edit word details |
| DELETE | `/words/{id}` | Delete word | Yes | Remove from database |
| POST | `/words/bulk` | Bulk import words | Yes | Import multiple words at once |
| GET | `/words/search` | Search words | Yes | Fuzzy search by German or Italian |

**Flashcards (3 endpoints) - [Database-persisted, multi-worker safe]:**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| POST | `/flashcards/start` | Start flashcard session | Yes | Create FlashcardSession in DB |
| POST | `/flashcards/{session_id}/answer` | Submit flashcard answer | Yes | Update progress, save review |
| GET | `/flashcards/{session_id}/current` | Get current flashcard | Yes | Retrieve from FlashcardSession |

**Lists (6 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| POST | `/lists` | Create vocabulary list | Yes | UserVocabularyList |
| GET | `/lists` | Get all lists | Yes | User's custom lists |
| GET | `/lists/{id}` | Get list with words | Yes | Include all words in list |
| POST | `/lists/{id}/words` | Add word to list | Yes | VocabularyListWord association |
| DELETE | `/lists/{id}/words/{word_id}` | Remove word | Yes | Delete association |
| DELETE | `/lists/{id}` | Delete list | Yes | Cascade delete list and associations |

**Quizzes (2 endpoints) - [Database-persisted, multi-worker safe]:**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| POST | `/quiz/generate` | Generate quiz | Yes | VocabularyAIService.generate_quiz(), store in VocabularyQuiz |
| POST | `/quiz/{quiz_id}/answer` | Submit quiz answer | Yes | Evaluate, update progress |

**Progress (3 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/progress/summary` | Progress summary | Yes | Overall vocabulary statistics |
| GET | `/progress/review-queue` | Due words | Yes | Words due for spaced repetition |
| POST | `/progress/reset/{word_id}` | Reset word progress | Yes | Reset mastery to 0 |

**AI-Powered (5 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| POST | `/analyze` | AI word analysis | Yes | VocabularyAIService.analyze_word() |
| POST | `/detect` | Detect vocabulary | Yes | Extract words from text |
| POST | `/recommend` | Get recommendations | Yes | Suggest words for context |
| POST | `/examples` | Generate examples | Yes | Create example sentences |
| POST | `/related` | Find related words | Yes | Synonyms, antonyms, collocations |

**Flashcard Session Persistence:**
```python
# Before (BUG-015, BUG-016): In-memory dictionary
flashcard_sessions = {}  # Lost on worker change or restart

# After (fixed): Database persistence
session = FlashcardSession(
    id=session_id,
    user_id=user.id,
    total_cards=len(cards),
    current_index=0,
    cards_data=json.dumps(cards),  # Persisted in PostgreSQL
    use_spaced_repetition=True
)
db.add(session)
db.commit()
```

### Analytics (14 endpoints) - /api/v1/analytics

**Progress (3 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/progress` | Overall progress | Yes | AnalyticsService.get_overall_progress() |
| GET | `/progress/comparison` | Compare periods | Yes | Week-over-week, month-over-month |
| GET | `/errors` | Error analysis | Yes | Recurring mistakes, patterns |

**Snapshots (2 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| POST | `/snapshots` | Create snapshot | Yes | Point-in-time progress capture |
| GET | `/snapshots` | Get snapshots | Yes | Historical progress data |

**Achievements (4 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/achievements` | List all achievements | No | 31 achievements (4 tiers) |
| GET | `/achievements/earned` | User's achievements | Yes | Earned achievements with progress |
| GET | `/achievements/progress` | Achievement progress | Yes | Progress toward unearned achievements |
| POST | `/achievements/{id}/showcase` | Showcase achievement | Yes | Display on profile |

**Stats (2 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/stats` | User statistics | Yes | Aggregate stats (UserStats) |
| POST | `/stats/refresh` | Refresh stats | Yes | Recalculate all statistics |

**Leaderboards & Heatmaps (3 endpoints):**

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/leaderboard/{type}` | Leaderboard rankings | Yes | overall, grammar, vocabulary, streak |
| GET | `/heatmap/activity` | Activity heatmap | Yes | 365-day activity calendar |
| GET | `/heatmap/grammar` | Grammar mastery heatmap | Yes | Topic-level mastery visualization |

### Integration (3 endpoints) - /api/v1/integration

| Method | Endpoint | Purpose | Auth Required | Description |
|--------|----------|---------|---------------|-------------|
| GET | `/session-analysis/{session_id}` | Analyze conversation | Yes | Extract grammar/vocab, recommend practice |
| GET | `/learning-path` | Personalized plan | Yes | Daily/weekly goals based on progress |
| GET | `/dashboard` | Unified dashboard | Yes | Due items, recent activity, quick actions |

**Dashboard Data Format:**
```json
{
  "user_id": 1,
  "due_items": {
    "grammar_topics": [{"id": 5, "name": "Dativ", "due_date": "2026-01-20"}],
    "vocabulary_words": [{"id": 12, "word": "das Konto", "due_date": "2026-01-21"}]
  },
  "recent_activity": [
    {"type": "conversation", "timestamp": "2026-01-22 10:30", "context": "Business Meeting"},
    {"type": "grammar", "timestamp": "2026-01-21 15:45", "topic": "Akkusativ"}
  ],
  "quick_actions": [
    {"action": "review_vocabulary", "count": 12, "priority": "high"},
    {"action": "practice_grammar", "count": 3, "priority": "medium"}
  ],
  "streak": {"current": 7, "longest": 15},
  "overall_progress": {"score": 68, "modules": {...}}
}
```

### Health (2 endpoints) - /api/health

| Method | Endpoint | Purpose | Auth Required | Response |
|--------|----------|---------|---------------|----------|
| GET | `/` | API information | No | App name, version, status |
| GET | `/api/health` | Health check | No | DB status, AI service status |

**Health Check Response:**
```json
{
  "status": "healthy",
  "environment": "production",
  "database": "connected",
  "ai_service": "configured"
}
```

## Authentication Flow

### JWT Token Generation

```python
# 1. Password Hashing (Registration)
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

hashed_password = pwd_context.hash("user_password")
# → $2b$12$... (bcrypt hash)

# 2. Password Verification (Login)
is_valid = pwd_context.verify("user_password", hashed_password)
# → True/False

# 3. JWT Token Creation
from jose import jwt
from datetime import datetime, timedelta

token_data = {"sub": str(user.id)}  # sub = subject (user ID)
expire = datetime.utcnow() + timedelta(minutes=30)
token_data.update({"exp": expire})

token = jwt.encode(
    token_data,
    settings.SECRET_KEY,
    algorithm="HS256"
)
# → eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# 4. JWT Token Decoding (Protected Endpoints)
payload = jwt.decode(
    token,
    settings.SECRET_KEY,
    algorithms=["HS256"]
)
# → {"sub": "1", "exp": 1706000000}

user_id = int(payload["sub"])
user = db.query(User).filter(User.id == user_id).first()
```

### Dependency Injection Chain

```python
# api/deps.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    payload = decode_access_token(token)
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    # Future: check if user.is_active
    return current_user

# Usage in routes
@router.get("/profile")
def get_profile(current_user: User = Depends(get_current_active_user)):
    return current_user
```

**Dependency Resolution:**
```
get_current_active_user()
  └── get_current_user()
        ├── oauth2_scheme() → Extract token from Authorization header
        └── get_db() → Create database session
              └── SessionLocal() → SQLAlchemy session factory
```

## Error Handling Patterns

### HTTPException (API Errors)

```python
from fastapi import HTTPException, status

# 1. Resource Not Found (404)
if not session:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Session not found"
    )

# 2. Authentication Error (401)
if not verify_password(password, user.password_hash):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )

# 3. Validation Error (400)
if existing_user:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username already registered"
    )

# 4. Permission Error (403)
if session.user_id != current_user.id:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Not authorized to access this session"
    )
```

### Pydantic Validation (Automatic)

```python
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr  # Automatic email validation
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)

# FastAPI automatically validates request body
# Returns 422 Unprocessable Entity if validation fails
```

### AI Service Fallbacks

```python
try:
    response = self.client.messages.create(...)
    return response.content[0].text
except APIError as e:
    logger.error(f"Anthropic API error: {e}")
    # Fallback: return generic response or cached data
    return self._get_fallback_response()
```

## API Design Patterns

### 1. Service Pattern

**Purpose:** Encapsulate business logic in reusable service classes

```python
# Service instantiation in route
@router.post("/generate-exercises")
def generate_exercises(
    request: GenerateExercisesRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    service = GrammarAIService(settings.ANTHROPIC_API_KEY)
    exercises = service.generate_exercises(...)

    # Store exercises in database
    for ex in exercises:
        db_exercise = GrammarExercise(**ex)
        db.add(db_exercise)
    db.commit()

    return exercises
```

### 2. Factory Pattern

**Purpose:** Create service instances with configuration

```python
class ServiceFactory:
    @staticmethod
    def create_conversation_ai() -> ConversationAI:
        return ConversationAI(api_key=settings.ANTHROPIC_API_KEY)

    @staticmethod
    def create_grammar_ai() -> GrammarAIService:
        return GrammarAIService(api_key=settings.ANTHROPIC_API_KEY)
```

### 3. Adapter Pattern

**Purpose:** Convert AI API responses to domain models

```python
def _extract_json(self, ai_response: str) -> Dict:
    """Extract JSON from AI response (may include markdown)."""
    # Handle ```json ... ``` markdown blocks
    json_match = re.search(r'```json\n(.*?)\n```', ai_response, re.DOTALL)
    if json_match:
        return json.loads(json_match.group(1))

    # Handle plain JSON
    return json.loads(ai_response)
```

### 4. Dependency Injection

**Purpose:** Automatic wiring of database sessions and authentication

```python
@router.get("/words")
def get_words(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    # db and current_user automatically injected by FastAPI
    query = db.query(Vocabulary)
    if category:
        query = query.filter(Vocabulary.category == category)
    return query.all()
```

## External Dependencies

### Anthropic Claude API

| Property | Value |
|----------|-------|
| **Model** | claude-sonnet-4-5 (auto-updating alias) |
| **Alternative** | claude-sonnet-4-5-20250929 (fixed snapshot) |
| **API Key** | Environment variable `ANTHROPIC_API_KEY` |
| **SDK** | `anthropic>=0.5.0` (Python client) |
| **Pricing** | $3 per million input tokens, $15 per million output tokens |
| **Max Tokens** | 1024-4000 (varies by use case) |
| **Temperature** | 0.3-0.7 (0.3 for word analysis, 0.7 for exercises) |

**Usage by Service:**
- ConversationAI: Conversation generation, grammar analysis, vocabulary detection
- GrammarAIService: Exercise generation, answer evaluation, error explanation
- VocabularyAIService: Word analysis, flashcard generation, quiz creation

### PostgreSQL Database

| Property | Value |
|----------|-------|
| **Version** | 12+ (15+ recommended) |
| **Connection** | `DATABASE_URL` environment variable |
| **Pooling** | QueuePool (size=10, max_overflow=20) |
| **ORM** | SQLAlchemy 2.0 |
| **Migrations** | Alembic 1.12.0+ |

### Authentication Libraries

| Library | Purpose | Version |
|---------|---------|---------|
| `python-jose[cryptography]` | JWT token creation/validation | >=3.3.0 |
| `passlib[bcrypt]` | Password hashing | >=1.7.4 |
| `bcrypt` | Bcrypt algorithm (pinned) | ==4.2.0 |

## Related Areas

- **[Backend Architecture](backend.md)** - Overall backend structure and directory organization
- **[Database Schema](backend-database.md)** - Complete database model documentation
- **[Deployment Guide](/docs/GUIDES/deployment/DEPLOYMENT_GUIDE.md)** - Production deployment walkthrough
- **[Troubleshooting Guide](/docs/GUIDES/troubleshooting/TROUBLESHOOTING.md)** - Common API issues

---

**API Architecture Summary:**

The API follows a clean service-oriented architecture with:
1. **74 endpoints** organized across 7 router modules
2. **5 service classes** (3 AI-powered, 2 business logic)
3. **JWT authentication** with dependency injection
4. **Pydantic validation** for type safety
5. **Multi-worker safe** session persistence (database-backed)
6. **Comprehensive error handling** with fallback mechanisms
7. **External AI integration** via Anthropic Claude Sonnet 4.5

All endpoints follow RESTful conventions with proper HTTP status codes, authentication guards, and response serialization.
