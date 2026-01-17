# Business Requirements Document: German Learning Application

**Version:** 1.0  
**Date:** 2026-01-16  
**Target User:** Igor - B2/C1 German learner, business context focus  
**Development Tool:** Claude Code  
**Primary Developer Context:** Python expertise, systematic approach, cloud infrastructure experience

---

## 1. Executive Summary

### 1.1 Project Overview
Interactive web-based application for advanced German language learning (B2-C1 level) with focus on business vocabulary in the payments/finance sector, everyday conversational skills, and comprehensive grammar mastery. The application uses AI-powered conversations and adaptive grammar exercises to provide personalized, context-rich learning experiences.

### 1.2 Key Objectives
- Improve German business vocabulary in payments/finance domain
- Enhance conversational fluency in both professional and everyday contexts
- Master German grammar through systematic practice and drilling
- Automatically identify and address grammar weaknesses from conversations
- Provide immediate, detailed feedback on grammar and usage
- Track comprehensive progress across vocabulary, conversation, and grammar
- Enable 60-90 minutes daily practice sessions (30-60 min conversation/vocab + 30 min grammar)
- Maintain high engagement through varied, realistic scenarios and adaptive exercises

### 1.3 Success Criteria
- User completes 5+ sessions per week (combined conversation + grammar)
- Measurable vocabulary expansion (trackable in database)
- Measurable grammar mastery improvement across topics
- Improved fluency in business contexts
- Grammar accuracy improvement in conversations
- User-reported satisfaction with learning effectiveness

---

## 2. Technical Architecture

### 2.1 Technology Stack

**Backend:**
- **Primary Framework:** FastAPI (main API server)
- **Secondary Framework:** Flask (optional admin dashboard)
- **Language:** Python 3.11+
- **Database:** PostgreSQL 15+
- **ORM:** SQLAlchemy 2.0
- **Migration Tool:** Alembic
- **Task Queue:** Celery (for async operations if needed)

**Frontend:**
- **Framework:** React 18+ with TypeScript (recommended) OR vanilla JavaScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State Management:** React Context API or Zustand
- **HTTP Client:** Axios

**AI Integration:**
- **Primary LLM:** Anthropic Claude (Claude 3.5 Sonnet via API)
- **Fallback LLM:** OpenAI GPT-4 (optional)
- **Text-to-Speech:** (Phase 2) - TBD
- **Speech-to-Text:** (Phase 2) - TBD

**Deployment:**
- **Environment:** Ubuntu Server (local) or development notebook
- **Web Server:** Uvicorn (for FastAPI)
- **Reverse Proxy:** Nginx (optional, for production-like setup)
- **Process Manager:** systemd or supervisord

### 2.2 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Session    │  │  Vocabulary  │  │   Progress    │  │
│  │  Interface  │  │   Review     │  │   Dashboard   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│  ┌─────────────┐  ┌──────────────┐                     │
│  │  Grammar    │  │   Context    │                     │
│  │  Practice   │  │   Library    │                     │
│  └─────────────┘  └──────────────┘                     │
└────────────────────────┬────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Session    │  │  Vocabulary  │  │   Progress   │  │
│  │   Manager    │  │   Manager    │  │   Tracker    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │  AI Service  │  │  Evaluation  │  │   Grammar    │  │
│  │   Wrapper    │  │   Engine     │  │   Engine     │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│  ┌──────────────┐  ┌──────────────┐                    │
│  │  Grammar AI  │  │   Exercise   │                    │
│  │   Service    │  │  Generator   │                    │
│  └──────────────┘  └──────────────┘                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
│  - Users          - Vocabulary         - Grammar Topics │
│  - Sessions       - Progress Tracking  - Exercises      │
│  - Conversations  - Context Library    - Diagnostics    │
│  - Grammar Corrections & Progress                       │
└─────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│              External AI Services                        │
│  - Anthropic Claude API (Conversations + Grammar)       │
│  - (Optional) OpenAI API                                 │
└─────────────────────────────────────────────────────────┘
```

---

## 3. Database Schema

### 3.1 Core Tables

#### 3.1.1 Users
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    native_language VARCHAR(10) DEFAULT 'it',
    target_language VARCHAR(10) DEFAULT 'de',
    proficiency_level VARCHAR(10) DEFAULT 'B2', -- A1, A2, B1, B2, C1, C2
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    settings JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);
```

#### 3.1.2 Contexts (Scenarios/Topics)
```sql
CREATE TABLE contexts (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL, -- 'business', 'daily', 'finance', 'social'
    difficulty_level VARCHAR(10), -- B1, B2, C1, C2
    description TEXT,
    system_prompt TEXT NOT NULL, -- AI system prompt for this context
    suggested_vocab JSONB DEFAULT '[]'::jsonb, -- Array of relevant vocab IDs
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_contexts_category ON contexts(category);
CREATE INDEX idx_contexts_difficulty ON contexts(difficulty_level);
```

#### 3.1.3 Vocabulary
```sql
CREATE TABLE vocabulary (
    id SERIAL PRIMARY KEY,
    word_de VARCHAR(255) NOT NULL,
    word_it VARCHAR(255) NOT NULL,
    word_en VARCHAR(255),
    part_of_speech VARCHAR(50), -- noun, verb, adjective, etc.
    difficulty_level VARCHAR(10),
    context_category VARCHAR(50), -- business, daily, finance, etc.
    example_sentence_de TEXT,
    example_sentence_it TEXT,
    notes TEXT,
    gender VARCHAR(10), -- for nouns: der, die, das
    plural_form VARCHAR(255), -- for nouns
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_reviewed TIMESTAMP,
    review_count INTEGER DEFAULT 0
);

CREATE INDEX idx_vocabulary_word_de ON vocabulary(word_de);
CREATE INDEX idx_vocabulary_category ON vocabulary(context_category);
CREATE INDEX idx_vocabulary_difficulty ON vocabulary(difficulty_level);
```

#### 3.1.4 User Vocabulary Progress
```sql
CREATE TABLE user_vocabulary (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    vocabulary_id INTEGER REFERENCES vocabulary(id) ON DELETE CASCADE,
    familiarity_score FLOAT DEFAULT 0.0, -- 0.0 to 1.0
    times_encountered INTEGER DEFAULT 0,
    times_correct INTEGER DEFAULT 0,
    times_incorrect INTEGER DEFAULT 0,
    last_encountered TIMESTAMP,
    first_encountered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    next_review_date TIMESTAMP,
    notes TEXT,
    UNIQUE(user_id, vocabulary_id)
);

CREATE INDEX idx_user_vocab_user ON user_vocabulary(user_id);
CREATE INDEX idx_user_vocab_score ON user_vocabulary(familiarity_score);
CREATE INDEX idx_user_vocab_next_review ON user_vocabulary(next_review_date);
```

#### 3.1.5 Sessions
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    context_id INTEGER REFERENCES contexts(id),
    session_type VARCHAR(50) DEFAULT 'conversation', -- conversation, vocab_review, mixed
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    duration_minutes INTEGER,
    total_turns INTEGER DEFAULT 0,
    grammar_errors INTEGER DEFAULT 0,
    vocab_score FLOAT, -- 0.0 to 1.0
    fluency_score FLOAT, -- 0.0 to 1.0
    overall_score FLOAT, -- 0.0 to 1.0
    ai_model_used VARCHAR(50),
    session_summary TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_started ON sessions(started_at);
CREATE INDEX idx_sessions_context ON sessions(context_id);
```

#### 3.1.6 Conversation Turns
```sql
CREATE TABLE conversation_turns (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sessions(id) ON DELETE CASCADE,
    turn_number INTEGER NOT NULL,
    speaker VARCHAR(20) NOT NULL, -- 'user' or 'ai'
    message_text TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    grammar_feedback JSONB, -- Array of grammar corrections
    vocabulary_used JSONB, -- Array of vocabulary IDs detected
    ai_evaluation JSONB, -- AI's assessment of the turn
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_turns_session ON conversation_turns(session_id);
CREATE INDEX idx_turns_turn_number ON conversation_turns(session_id, turn_number);
```

#### 3.1.7 Grammar Corrections
```sql
CREATE TABLE grammar_corrections (
    id SERIAL PRIMARY KEY,
    turn_id INTEGER REFERENCES conversation_turns(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    grammar_topic_id INTEGER REFERENCES grammar_topics(id), -- Link to grammar topic
    error_type VARCHAR(100), -- case, gender, verb_conjugation, word_order, etc.
    incorrect_text TEXT NOT NULL,
    corrected_text TEXT NOT NULL,
    explanation TEXT,
    rule_reference TEXT,
    severity VARCHAR(20), -- minor, moderate, major
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grammar_user ON grammar_corrections(user_id);
CREATE INDEX idx_grammar_error_type ON grammar_corrections(error_type);
CREATE INDEX idx_grammar_topic ON grammar_corrections(grammar_topic_id);
```

#### 3.1.8 Progress Snapshots
```sql
CREATE TABLE progress_snapshots (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    snapshot_date DATE DEFAULT CURRENT_DATE,
    total_sessions INTEGER DEFAULT 0,
    total_practice_minutes INTEGER DEFAULT 0,
    vocabulary_learned INTEGER DEFAULT 0,
    vocabulary_mastered INTEGER DEFAULT 0, -- familiarity_score > 0.8
    grammar_topics_mastered INTEGER DEFAULT 0, -- mastery_level > 0.8
    grammar_topics_learning INTEGER DEFAULT 0,
    avg_grammar_accuracy FLOAT,
    avg_fluency_score FLOAT,
    common_errors JSONB, -- Top grammar errors this period
    grammar_drill_sessions INTEGER DEFAULT 0,
    achievements JSONB, -- Milestones reached
    UNIQUE(user_id, snapshot_date)
);

CREATE INDEX idx_snapshots_user ON progress_snapshots(user_id);
CREATE INDEX idx_snapshots_date ON progress_snapshots(snapshot_date);
```

### 3.2 Relationships Diagram

```
users
  ├─── user_vocabulary ───── vocabulary
  ├─── user_grammar_progress ───── grammar_topics
  ├─── grammar_sessions ───── grammar_topics
  │       └─── grammar_exercise_attempts ───── grammar_exercises
  ├─── diagnostic_tests
  ├─── sessions ───── contexts
  │       └─── conversation_turns
  │               └─── grammar_corrections ───── grammar_topics (FK to map error to topic)
  └─── progress_snapshots

grammar_topics
  ├─── grammar_exercises
  ├─── user_grammar_progress
  └─── grammar_sessions
```

---

## 4. Core Features & Functionality

### 4.1 Feature: Grammar Learning & Practice System

#### 4.1.1 Description
Comprehensive grammar learning system with diagnostic assessment, targeted exercises, drilling capabilities, and adaptive progression. The system analyzes errors from conversations to generate personalized grammar exercises and tracks detailed progress across all grammatical topics.

#### 4.1.2 Grammar Topics Coverage

**Cases (Fälle):**
- Nominativ, Akkusativ, Dativ, Genitiv
- Case usage with prepositions
- Case with verbs
- Adjective declension in all cases

**Verb Conjugation (Verben):**
- Present tense (Präsens)
- Simple past (Präteritum)
- Present perfect (Perfekt)
- Past perfect (Plusquamperfekt)
- Future I & II (Futur I & II)
- Subjunctive I & II (Konjunktiv I & II)
- Imperative (Imperativ)
- Modal verbs (Modalverben)
- Separable/inseparable prefixes
- Reflexive verbs

**Sentence Structure (Satzbau):**
- Main clauses
- Subordinate clauses
- Position of verbs (V2, V-final)
- Time-Manner-Place rule
- Negation position

**Articles & Pronouns:**
- Definite/indefinite articles
- Article declension
- Possessive pronouns
- Demonstrative pronouns
- Relative pronouns

**Adjectives & Adverbs:**
- Adjective endings
- Comparative and superlative
- Adverb formation

**Prepositions:**
- Accusative prepositions
- Dative prepositions
- Two-way prepositions (Wechselpräpositionen)
- Genitive prepositions

**Other Topics:**
- Passive voice
- Indirect speech
- Conjunctions (coordinating, subordinating)
- Word formation (compounds, derivatives)

#### 4.1.3 Exercise Types Implementation

**Type 1: Fill-in-the-Blank (Lückentexte)**
```json
{
    "exercise_type": "fill_blank",
    "topic": "dative_case",
    "subtopic": "dative_with_prepositions",
    "question": "Ich gehe ____ (zu/der) Arzt.",
    "correct_answer": "zum",
    "explanation": "Die Präposition 'zu' verlangt den Dativ. 'der Arzt' wird zu 'dem Arzt', und 'zu + dem' wird zu 'zum' kontrahiert.",
    "difficulty": "B1",
    "hints": ["Welcher Fall nach 'zu'?", "Maskulinum Singular"]
}
```

**Type 2: Multiple Choice (Auswahl)**
```json
{
    "exercise_type": "multiple_choice",
    "topic": "verb_conjugation",
    "subtopic": "perfect_tense",
    "question": "Gestern ____ ich ins Kino ____.",
    "options": [
        "habe ... gegangen",
        "bin ... gegangen",
        "habe ... gehen",
        "bin ... gehen"
    ],
    "correct_answer": "bin ... gegangen",
    "explanation": "Das Verb 'gehen' bildet das Perfekt mit 'sein', weil es eine Bewegung ausdrückt. Das Partizip II ist 'gegangen'.",
    "difficulty": "B1"
}
```

**Type 3: Translation (Übersetzung)**
```json
{
    "exercise_type": "translation",
    "topic": "sentence_structure",
    "subtopic": "subordinate_clauses",
    "source_language": "it",
    "source_text": "So che lui arriva domani.",
    "correct_answer": "Ich weiß, dass er morgen kommt.",
    "alternative_answers": ["Ich weiß, dass er morgen ankommt."],
    "explanation": "Im Nebensatz mit 'dass' steht das konjugierte Verb am Ende.",
    "difficulty": "B2"
}
```

**Type 4: Error Correction (Fehlerkorrektur)**
```json
{
    "exercise_type": "error_correction",
    "topic": "cases",
    "subtopic": "accusative_case",
    "incorrect_sentence": "Ich sehe der Mann.",
    "correct_sentence": "Ich sehe den Mann.",
    "error_location": "der",
    "explanation": "Das Verb 'sehen' verlangt den Akkusativ. Der Artikel 'der' (Nominativ) muss zu 'den' (Akkusativ) geändert werden.",
    "difficulty": "A2"
}
```

**Type 5: Sentence Building (Satzbau)**
```json
{
    "exercise_type": "sentence_building",
    "topic": "sentence_structure",
    "subtopic": "word_order",
    "words": ["gestern", "ich", "habe", "einen Film", "gesehen"],
    "correct_order": ["Gestern", "habe", "ich", "einen Film", "gesehen"],
    "explanation": "In der Umstellung beginnt der Satz mit einer temporalen Angabe ('gestern'), danach folgt das Verb an zweiter Stelle (V2-Regel).",
    "difficulty": "B1"
}
```

#### 4.1.4 User Flow

**Initial Diagnostic Assessment:**
1. User starts grammar module for first time
2. System presents 30-question diagnostic test covering main topics
3. System analyzes results and identifies weak areas
4. System creates personalized learning path

**Daily Grammar Session:**
1. User selects "Grammar Practice" from main menu
2. System shows:
   - Topics due for review (based on spaced repetition)
   - Weak areas from recent conversations
   - Recommended next topic in learning path
3. User selects topic or accepts recommendation
4. System generates drill session (15+ exercises)
5. User completes exercises with immediate feedback
6. System shows session summary with detailed stats
7. System updates learning path and schedules next review

**Conversation-Triggered Practice:**
1. User completes conversation session with grammar errors
2. System identifies error patterns (e.g., 3 dative errors)
3. System prompts: "Möchtest du Dativübungen machen?"
4. If yes, generates targeted 15-exercise drill on dative
5. Results feed back into overall grammar progress

#### 4.1.5 Technical Implementation

**Database Schema for Grammar Module:**

```sql
-- Grammar rules and topics
CREATE TABLE grammar_topics (
    id SERIAL PRIMARY KEY,
    name_de VARCHAR(255) NOT NULL,
    name_en VARCHAR(255),
    category VARCHAR(100) NOT NULL, -- cases, verbs, sentence_structure, etc.
    subcategory VARCHAR(100),
    difficulty_level VARCHAR(10), -- A1, A2, B1, B2, C1, C2
    description_de TEXT,
    explanation_de TEXT, -- Detailed grammar explanation in German
    parent_topic_id INTEGER REFERENCES grammar_topics(id), -- For hierarchical topics
    order_index INTEGER, -- For sequential learning path
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grammar_topics_category ON grammar_topics(category);
CREATE INDEX idx_grammar_topics_difficulty ON grammar_topics(difficulty_level);

-- Grammar exercises
CREATE TABLE grammar_exercises (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES grammar_topics(id),
    exercise_type VARCHAR(50) NOT NULL, -- fill_blank, multiple_choice, translation, etc.
    difficulty_level VARCHAR(10),
    question_text TEXT NOT NULL,
    question_data JSONB NOT NULL, -- Exercise-specific data (options, blanks, etc.)
    correct_answer TEXT NOT NULL,
    alternative_answers JSONB, -- Array of acceptable alternatives
    explanation_de TEXT NOT NULL,
    explanation_it TEXT, -- Optional Italian explanation
    hints JSONB, -- Array of progressive hints
    context_category VARCHAR(50), -- business, daily, general
    source VARCHAR(50) DEFAULT 'manual', -- manual, ai_generated
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_grammar_exercises_topic ON grammar_exercises(topic_id);
CREATE INDEX idx_grammar_exercises_type ON grammar_exercises(exercise_type);
CREATE INDEX idx_grammar_exercises_difficulty ON grammar_exercises(difficulty_level);

-- User grammar progress per topic
CREATE TABLE user_grammar_progress (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    topic_id INTEGER REFERENCES grammar_topics(id),
    mastery_level FLOAT DEFAULT 0.0, -- 0.0 to 1.0
    total_exercises_attempted INTEGER DEFAULT 0,
    total_exercises_correct INTEGER DEFAULT 0,
    total_exercises_incorrect INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    last_practiced TIMESTAMP,
    next_review_date TIMESTAMP,
    weak_subtopics JSONB, -- Array of problematic subtopics
    notes TEXT,
    UNIQUE(user_id, topic_id)
);

CREATE INDEX idx_user_grammar_progress_user ON user_grammar_progress(user_id);
CREATE INDEX idx_user_grammar_progress_mastery ON user_grammar_progress(mastery_level);
CREATE INDEX idx_user_grammar_progress_next_review ON user_grammar_progress(next_review_date);

-- Grammar drill sessions
CREATE TABLE grammar_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    session_type VARCHAR(50) DEFAULT 'drill', -- drill, diagnostic, review, conversation_triggered
    topic_id INTEGER REFERENCES grammar_topics(id),
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP,
    total_exercises INTEGER DEFAULT 0,
    exercises_correct INTEGER DEFAULT 0,
    exercises_incorrect INTEGER DEFAULT 0,
    accuracy_rate FLOAT,
    completion_rate FLOAT,
    triggered_by_conversation_id INTEGER REFERENCES sessions(id), -- If triggered by conversation errors
    session_summary JSONB,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_grammar_sessions_user ON grammar_sessions(user_id);
CREATE INDEX idx_grammar_sessions_topic ON grammar_sessions(topic_id);
CREATE INDEX idx_grammar_sessions_started ON grammar_sessions(started_at);

-- Individual exercise attempts
CREATE TABLE grammar_exercise_attempts (
    id SERIAL PRIMARY KEY,
    grammar_session_id INTEGER REFERENCES grammar_sessions(id) ON DELETE CASCADE,
    exercise_id INTEGER REFERENCES grammar_exercises(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    user_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    time_spent_seconds INTEGER,
    hints_used INTEGER DEFAULT 0,
    attempt_number INTEGER DEFAULT 1, -- If user retries
    feedback_given TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grammar_attempts_session ON grammar_exercise_attempts(grammar_session_id);
CREATE INDEX idx_grammar_attempts_user ON grammar_exercise_attempts(user_id);
CREATE INDEX idx_grammar_attempts_exercise ON grammar_exercise_attempts(exercise_id);

-- Diagnostic test results
CREATE TABLE diagnostic_tests (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    overall_level VARCHAR(10), -- Determined level: B1, B2, C1
    topic_scores JSONB, -- {"cases": 0.75, "verbs": 0.60, ...}
    weak_areas JSONB, -- Array of topics needing work
    strong_areas JSONB, -- Array of mastered topics
    recommended_path JSONB, -- Suggested learning sequence
    total_questions INTEGER,
    correct_answers INTEGER,
    test_duration_minutes INTEGER
);

CREATE INDEX idx_diagnostic_tests_user ON diagnostic_tests(user_id);
CREATE INDEX idx_diagnostic_tests_date ON diagnostic_tests(test_date);
```

**API Endpoints:**

```python
# ===== DIAGNOSTIC ASSESSMENT =====

# Start diagnostic test
POST /api/grammar/diagnostic/start
Response:
{
    "test_id": int,
    "total_questions": 30,
    "estimated_time_minutes": 20,
    "instructions_de": str
}

# Get diagnostic test questions
GET /api/grammar/diagnostic/{test_id}/questions
Response:
{
    "questions": [
        {
            "question_number": int,
            "exercise_type": str,
            "question": str,
            "options": [] (if applicable),
            "question_data": {}
        }
    ]
}

# Submit diagnostic test answer
POST /api/grammar/diagnostic/{test_id}/answer
Request Body:
{
    "question_number": int,
    "answer": str
}
Response:
{
    "recorded": bool,
    "remaining_questions": int
}

# Get diagnostic test results
GET /api/grammar/diagnostic/{test_id}/results
Response:
{
    "overall_level": "B2",
    "accuracy": 0.73,
    "topic_breakdown": [
        {
            "topic": "cases",
            "score": 0.80,
            "status": "good"
        },
        {
            "topic": "verb_conjugation",
            "score": 0.55,
            "status": "needs_work"
        }
    ],
    "weak_areas": ["konjunktiv_II", "passive_voice"],
    "strong_areas": ["present_tense", "accusative"],
    "recommended_learning_path": [
        {"topic_id": 15, "topic_name": "Konjunktiv II", "priority": 1},
        {"topic_id": 23, "topic_name": "Passiv", "priority": 2}
    ]
}

# ===== GRAMMAR PRACTICE SESSIONS =====

# Get practice recommendations
GET /api/grammar/recommendations
Response:
{
    "due_for_review": [
        {
            "topic_id": int,
            "topic_name_de": str,
            "mastery_level": float,
            "days_since_last_practice": int
        }
    ],
    "conversation_triggered": [
        {
            "topic_id": int,
            "topic_name_de": str,
            "error_count_recent": int,
            "priority": "high|medium|low"
        }
    ],
    "next_in_path": {
        "topic_id": int,
        "topic_name_de": str,
        "difficulty": str
    }
}

# Get topic details with explanation
GET /api/grammar/topics/{topic_id}
Response:
{
    "id": int,
    "name_de": str,
    "category": str,
    "difficulty_level": str,
    "explanation_de": str, // Full grammar explanation
    "subtopics": [
        {
            "id": int,
            "name_de": str,
            "your_mastery": float
        }
    ],
    "your_progress": {
        "mastery_level": float,
        "exercises_attempted": int,
        "accuracy_rate": float,
        "last_practiced": str,
        "weak_subtopics": []
    },
    "example_exercises": [
        // 2-3 sample exercises
    ]
}

# Start grammar drill session
POST /api/grammar/sessions/start
Request Body:
{
    "topic_id": int,
    "exercise_count": int, // Default: 15
    "exercise_types": ["fill_blank", "multiple_choice"], // Optional filter
    "difficulty_range": ["B1", "B2"], // Optional
    "subtopic_focus": str // Optional: focus on specific subtopic
}
Response:
{
    "session_id": int,
    "topic": {
        "id": int,
        "name_de": str,
        "explanation_de": str // Brief reminder
    },
    "total_exercises": int,
    "exercises": [
        {
            "exercise_id": int,
            "exercise_number": 1,
            "exercise_type": str,
            "question": str,
            "options": [] // if multiple_choice
        }
    ]
}

# Submit exercise answer
POST /api/grammar/sessions/{session_id}/answer
Request Body:
{
    "exercise_id": int,
    "answer": str,
    "time_spent_seconds": int
}
Response:
{
    "is_correct": bool,
    "correct_answer": str,
    "your_answer": str,
    "explanation_de": str,
    "additional_examples": [str], // Optional: similar examples
    "next_exercise": {
        "exercise_id": int,
        "exercise_number": int,
        "question": str
    } // null if last exercise
}

# Get hint for current exercise
POST /api/grammar/sessions/{session_id}/hint
Request Body:
{
    "exercise_id": int,
    "hint_level": int // 1, 2, 3 for progressive hints
}
Response:
{
    "hint": str,
    "hints_remaining": int
}

# End grammar session
POST /api/grammar/sessions/{session_id}/end
Response:
{
    "session_summary": {
        "topic_name": str,
        "total_exercises": int,
        "correct": int,
        "incorrect": int,
        "accuracy_rate": float,
        "time_spent_minutes": int,
        "updated_mastery_level": float,
        "mastery_change": float, // +/- change
        "weak_points_identified": [
            {
                "subtopic": str,
                "error_count": int
            }
        ],
        "achievement_unlocked": str | null,
        "next_review_date": str
    },
    "incorrect_exercises_review": [
        {
            "question": str,
            "your_answer": str,
            "correct_answer": str,
            "explanation": str
        }
    ]
}

# ===== AI-GENERATED EXERCISES =====

# Generate custom exercises for topic
POST /api/grammar/exercises/generate
Request Body:
{
    "topic_id": int,
    "count": int,
    "exercise_types": [str],
    "difficulty": str,
    "context_category": str, // Optional: business, daily
    "use_user_vocabulary": bool // Use user's known vocabulary
}
Response:
{
    "exercises_generated": int,
    "exercise_ids": [int]
}

# ===== PROGRESS & ANALYTICS =====

# Get grammar overview
GET /api/grammar/progress/overview
Response:
{
    "overall_stats": {
        "total_topics": int,
        "topics_mastered": int, // mastery > 0.8
        "topics_learning": int, // 0.3 < mastery < 0.8
        "topics_weak": int, // mastery < 0.3
        "total_exercises_completed": int,
        "average_accuracy": float
    },
    "category_breakdown": [
        {
            "category": "cases",
            "mastery": 0.75,
            "topics_count": 8,
            "exercises_completed": 145
        }
    ],
    "recent_sessions": [
        {
            "date": str,
            "topic": str,
            "accuracy": float
        }
    ],
    "learning_streak": {
        "current_days": int,
        "longest_days": int
    }
}

# Get detailed progress for topic
GET /api/grammar/progress/topic/{topic_id}
Response:
{
    "topic": {
        "name_de": str,
        "category": str
    },
    "progress": {
        "mastery_level": float,
        "total_attempts": int,
        "accuracy_rate": float,
        "accuracy_trend": [
            {"date": "2026-01-10", "accuracy": 0.67},
            {"date": "2026-01-12", "accuracy": 0.73}
        ]
    },
    "subtopic_breakdown": [
        {
            "subtopic": str,
            "accuracy": float,
            "attempts": int
        }
    ],
    "common_mistakes": [
        {
            "error_pattern": str,
            "count": int,
            "last_occurred": str
        }
    ]
}

# Get grammar heatmap (topics vs mastery)
GET /api/grammar/progress/heatmap
Response:
{
    "categories": [
        {
            "category": "cases",
            "topics": [
                {
                    "topic_name": "Akkusativ",
                    "mastery": 0.85
                },
                {
                    "topic_name": "Dativ",
                    "mastery": 0.62
                }
            ]
        }
    ]
}
```

**AI Service Integration for Exercise Generation:**

```python
# services/grammar_ai_service.py
from anthropic import Anthropic
import json
from typing import List, Dict

class GrammarAIService:
    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    async def generate_exercises(
        self,
        topic: str,
        subtopic: str,
        difficulty: str,
        count: int = 15,
        exercise_type: str = "mixed",
        context_category: str = None,
        user_vocabulary: List[str] = None
    ) -> List[Dict]:
        """
        Generate grammar exercises using AI
        
        Args:
            topic: Main grammar topic (e.g., "cases", "verb_conjugation")
            subtopic: Specific aspect (e.g., "dative_prepositions")
            difficulty: B1, B2, C1, C2
            count: Number of exercises to generate
            exercise_type: fill_blank, multiple_choice, translation, etc.
            context_category: business, daily, or None for general
            user_vocabulary: List of user's known words to incorporate
        """
        
        vocab_instruction = ""
        if user_vocabulary and len(user_vocabulary) > 0:
            vocab_sample = ", ".join(user_vocabulary[:20])
            vocab_instruction = f"\nIncorporate some of these vocabulary words when appropriate: {vocab_sample}"
        
        context_instruction = ""
        if context_category:
            context_instruction = f"\nCreate exercises with {context_category} context and vocabulary."
        
        prompt = f"""Generate {count} German grammar exercises for the following topic:

Topic: {topic}
Subtopic: {subtopic}
Difficulty Level: {difficulty}
Exercise Types: {exercise_type}
{context_instruction}{vocab_instruction}

Requirements:
1. All exercises must test {subtopic}
2. Difficulty appropriate for {difficulty} level
3. Questions and explanations in German (use advanced grammatical terminology)
4. Include detailed explanations using proper grammatical terms
5. For fill-in-blank: provide the sentence with blank marker
6. For multiple choice: provide 4 options with only one correct
7. For translation: provide Italian source text
8. All explanations must be clear and pedagogically sound

Return ONLY a JSON array with this exact structure:
[
    {{
        "exercise_type": "fill_blank|multiple_choice|translation|error_correction|sentence_building",
        "question": "the question text",
        "correct_answer": "the correct answer",
        "options": ["option1", "option2", "option3", "option4"], // only for multiple_choice
        "source_text": "Italian text", // only for translation
        "incorrect_sentence": "wrong sentence", // only for error_correction
        "words_to_arrange": ["word1", "word2"], // only for sentence_building
        "explanation_de": "detailed explanation in German using proper grammar terminology",
        "hints": ["hint1", "hint2", "hint3"],
        "alternative_answers": ["alt1", "alt2"] // optional acceptable alternatives
    }}
]

Generate exactly {count} varied and well-crafted exercises."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            exercises = json.loads(response.content[0].text)
            return exercises
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            content = response.content[0].text
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != 0:
                exercises = json.loads(content[start:end])
                return exercises
            else:
                raise ValueError("Could not parse AI response as JSON")
    
    async def generate_diagnostic_test(
        self,
        level_estimate: str = "B2"
    ) -> List[Dict]:
        """Generate a 30-question diagnostic test covering main topics"""
        
        topics_to_test = [
            ("cases", "accusative", 3),
            ("cases", "dative", 3),
            ("cases", "genitive", 2),
            ("verb_conjugation", "perfect_tense", 3),
            ("verb_conjugation", "subjunctive", 2),
            ("verb_conjugation", "modal_verbs", 2),
            ("sentence_structure", "subordinate_clauses", 3),
            ("sentence_structure", "word_order", 2),
            ("prepositions", "two_way_prepositions", 3),
            ("adjectives", "adjective_endings", 3),
            ("passive_voice", "passive_formation", 2),
            ("pronouns", "relative_pronouns", 2)
        ]
        
        all_exercises = []
        
        for topic, subtopic, count in topics_to_test:
            exercises = await self.generate_exercises(
                topic=topic,
                subtopic=subtopic,
                difficulty=level_estimate,
                count=count,
                exercise_type="multiple_choice"  # Easier to grade automatically
            )
            all_exercises.extend(exercises)
        
        return all_exercises
    
    async def explain_grammar_rule(
        self,
        topic: str,
        subtopic: str,
        user_level: str = "B2"
    ) -> str:
        """Generate comprehensive explanation of grammar rule in German"""
        
        prompt = f"""Erkläre folgende deutsche Grammatikregel auf Deutsch (Niveau {user_level}):

Thema: {topic}
Unterthema: {subtopic}

Anforderungen:
1. Verwende präzise grammatische Fachterminologie
2. Gib klare Regeln und Muster
3. Füge 3-4 Beispielsätze hinzu
4. Erkläre häufige Fehler
5. Gib praktische Tipps zum Lernen
6. Strukturiere die Erklärung klar (verwende Absätze, keine Aufzählungspunkte)

Die Erklärung sollte umfassend sein (300-500 Wörter), aber für fortgeschrittene Lerner ({user_level}) geeignet."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.content[0].text
```

**Spaced Repetition for Grammar Topics:**

```python
# utils/grammar_spaced_repetition.py
from datetime import datetime, timedelta
from typing import Tuple

class GrammarSpacedRepetition:
    """
    Spaced repetition algorithm for grammar topics
    More aggressive than vocabulary due to need for drilling
    """
    
    @staticmethod
    def calculate_next_review(
        mastery_level: float,
        total_attempted: int,
        total_correct: int,
        total_incorrect: int,
        last_practiced: datetime,
        current_streak: int
    ) -> Tuple[datetime, float, int]:
        """
        Calculate next review date, updated mastery, and streak
        
        Returns:
            (next_review_date, new_mastery_level, new_streak)
        """
        
        if total_attempted == 0:
            # First practice
            return (
                datetime.now() + timedelta(days=1),
                0.0,
                0
            )
        
        # Calculate current session accuracy
        session_accuracy = total_correct / total_attempted if total_attempted > 0 else 0
        
        # Update mastery level (weighted moving average)
        # Give more weight to recent performance
        new_mastery = (mastery_level * 0.7) + (session_accuracy * 0.3)
        new_mastery = min(1.0, max(0.0, new_mastery))
        
        # Update streak
        days_since_last = (datetime.now() - last_practiced).days if last_practiced else 0
        if days_since_last <= 1:
            new_streak = current_streak + 1
        else:
            new_streak = 1
        
        # Calculate interval based on mastery and streak
        if new_mastery < 0.3:
            # Struggling: review daily
            interval_days = 1
        elif new_mastery < 0.5:
            # Learning: review every 2 days
            interval_days = 2
        elif new_mastery < 0.7:
            # Good progress: 3-4 days
            interval_days = 3 + (new_streak // 3)
        elif new_mastery < 0.85:
            # Strong: 5-7 days
            interval_days = 5 + (new_streak // 2)
        else:
            # Mastered: 10-14 days
            interval_days = 10 + min(new_streak, 4)
        
        next_review = datetime.now() + timedelta(days=interval_days)
        
        return (next_review, new_mastery, new_streak)
    
    @staticmethod
    def should_trigger_from_conversation(
        error_count: int,
        topic_mastery: float,
        days_since_last_practice: int
    ) -> bool:
        """
        Determine if conversation errors should trigger grammar drill
        """
        # Trigger if:
        # - Multiple errors (3+) in one conversation
        # - OR 2+ errors and low mastery (<0.5)
        # - OR any errors and haven't practiced in 7+ days
        
        if error_count >= 3:
            return True
        
        if error_count >= 2 and topic_mastery < 0.5:
            return True
        
        if error_count >= 1 and days_since_last_practice >= 7:
            return True
        
        return False
```

### 4.2 Feature: Interactive Conversation Sessions

#### 4.1.1 Description
User engages in text-based conversation with AI in German. The AI plays different roles based on selected context (e.g., business meeting, casual chat, bank discussion).

#### 4.1.2 User Flow
1. User selects session type: "Free conversation" or "Specific context"
2. If specific context: User selects from available contexts (business/daily/mixed)
3. System initializes AI with appropriate system prompt
4. User sends message in German
5. System:
   - Analyzes message for grammar errors
   - Identifies vocabulary used
   - Generates AI response
   - Provides inline feedback (optional toggle)
6. Conversation continues for desired duration
7. User ends session
8. System provides session summary with scores and insights

#### 4.1.3 Technical Implementation

**API Endpoints:**

```python
# Start new session
POST /api/sessions/start
Request Body:
{
    "context_id": int | null,  # null for free conversation
    "session_type": "conversation" | "vocab_review" | "mixed"
}
Response:
{
    "session_id": int,
    "context": {
        "name": str,
        "description": str,
        "difficulty": str
    },
    "initial_message": str  # AI's opening message
}

# Send message in conversation
POST /api/sessions/{session_id}/message
Request Body:
{
    "message": str,
    "request_feedback": bool  # default: true
}
Response:
{
    "turn_id": int,
    "ai_response": str,
    "grammar_feedback": [
        {
            "error_type": str,
            "incorrect": str,
            "corrected": str,
            "explanation": str,
            "severity": str
        }
    ],
    "vocabulary_detected": [
        {
            "word": str,
            "familiarity_score": float,
            "is_new": bool
        }
    ],
    "suggestions": []  # Optional vocabulary/phrase suggestions
}

# End session
POST /api/sessions/{session_id}/end
Response:
{
    "session_summary": {
        "duration_minutes": int,
        "total_turns": int,
        "grammar_accuracy": float,
        "vocabulary_used_count": int,
        "new_vocabulary_count": int,
        "overall_score": float,
        "achievements": [],
        "areas_for_improvement": []
    }
}

# Get session history
GET /api/sessions/{session_id}
Response:
{
    "session": {
        "id": int,
        "context": {},
        "started_at": str,
        "ended_at": str,
        "scores": {}
    },
    "conversation": [
        {
            "turn_number": int,
            "speaker": str,
            "message": str,
            "timestamp": str,
            "feedback": {}
        }
    ]
}
```

**AI Service Integration:**

```python
# ai_service.py
import anthropic
from typing import List, Dict, Optional

class ConversationAI:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20241022"
    
    def generate_response(
        self,
        context_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        user_level: str = "B2"
    ) -> str:
        """Generate AI response in conversation"""
        
        system_prompt = f"""You are a German language conversation partner helping an advanced learner (level {user_level}). 
        
Context: {context_prompt}

Guidelines:
- Respond naturally in German appropriate to the context
- Match the user's proficiency level ({user_level})
- Use vocabulary relevant to the scenario
- Occasionally introduce new vocabulary naturally
- Be conversational and engaging
- If user makes errors, continue conversation naturally (don't correct immediately)
"""
        
        messages = conversation_history + [
            {"role": "user", "content": user_message}
        ]
        
        response = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            system=system_prompt,
            messages=messages
        )
        
        return response.content[0].text
    
    def analyze_grammar(
        self,
        user_message: str,
        user_level: str = "B2"
    ) -> List[Dict]:
        """Analyze user's message for grammar errors"""
        
        analysis_prompt = f"""Analyze this German text for grammar errors. User level: {user_level}

Text: "{user_message}"

Provide analysis in JSON format:
[
    {{
        "error_type": "case|gender|verb_conjugation|word_order|article|preposition|other",
        "incorrect_text": "the wrong part",
        "corrected_text": "the correct version",
        "explanation": "brief explanation in Italian",
        "severity": "minor|moderate|major",
        "rule": "grammar rule reference"
    }}
]

If no errors, return empty array. Be strict but fair for {user_level} level."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            messages=[{"role": "user", "content": analysis_prompt}]
        )
        
        # Parse JSON response
        import json
        try:
            return json.loads(response.content[0].text)
        except:
            return []
```

### 4.3 Feature: Vocabulary Management & Review

#### 4.2.1 Description
System tracks vocabulary encountered during conversations, manages spaced repetition, and provides targeted review sessions.

#### 4.2.2 User Flow
1. User accesses vocabulary dashboard
2. Views vocabulary organized by:
   - Recently learned
   - Needs review (based on spaced repetition)
   - Mastered vs. learning
   - Category (business, daily, etc.)
3. User can:
   - Start vocabulary review session
   - Search/filter vocabulary
   - Add custom vocabulary
   - View usage examples from their own conversations

#### 4.2.3 Technical Implementation

**API Endpoints:**

```python
# Get vocabulary overview
GET /api/vocabulary/overview
Response:
{
    "total_vocabulary": int,
    "mastered": int,
    "learning": int,
    "needs_review": int,
    "categories": {
        "business": int,
        "daily": int,
        "finance": int
    }
}

# Get vocabulary list with filters
GET /api/vocabulary/list
Query Parameters:
    - category: str
    - difficulty: str
    - status: "mastered" | "learning" | "needs_review"
    - search: str
    - limit: int
    - offset: int
Response:
{
    "vocabulary": [
        {
            "id": int,
            "word_de": str,
            "word_it": str,
            "part_of_speech": str,
            "example_sentence_de": str,
            "familiarity_score": float,
            "times_encountered": int,
            "last_encountered": str,
            "next_review_date": str
        }
    ],
    "total": int
}

# Add custom vocabulary
POST /api/vocabulary/add
Request Body:
{
    "word_de": str,
    "word_it": str,
    "context_category": str,
    "example_sentence_de": str (optional)
}

# Start vocabulary review session
POST /api/vocabulary/review/start
Request Body:
{
    "review_type": "due" | "category" | "random",
    "category": str (if review_type = "category"),
    "count": int  # number of words to review
}
Response:
{
    "review_session_id": str,
    "vocabulary_items": [
        {
            "id": int,
            "word_de": str,
            "context_category": str
        }
    ]
}

# Submit vocabulary review answer
POST /api/vocabulary/review/answer
Request Body:
{
    "review_session_id": str,
    "vocabulary_id": int,
    "user_translation": str,
    "confidence": "low" | "medium" | "high"
}
Response:
{
    "correct": bool,
    "correct_translation": str,
    "feedback": str
}
```

**Spaced Repetition Algorithm:**

```python
# spaced_repetition.py
from datetime import datetime, timedelta
from typing import Tuple

class SpacedRepetition:
    """Simple SM-2 like algorithm for vocabulary review"""
    
    @staticmethod
    def calculate_next_review(
        familiarity_score: float,
        times_correct: int,
        times_incorrect: int,
        last_encountered: datetime
    ) -> Tuple[datetime, float]:
        """
        Calculate next review date and updated familiarity score
        
        Returns:
            (next_review_date, new_familiarity_score)
        """
        total_encounters = times_correct + times_incorrect
        
        if total_encounters == 0:
            # First encounter
            return (
                datetime.now() + timedelta(days=1),
                0.3
            )
        
        # Calculate accuracy rate
        accuracy = times_correct / total_encounters if total_encounters > 0 else 0
        
        # Update familiarity score
        new_score = min(1.0, familiarity_score * 0.9 + accuracy * 0.1)
        
        # Calculate interval based on familiarity
        if new_score < 0.3:
            interval_days = 1
        elif new_score < 0.5:
            interval_days = 2
        elif new_score < 0.7:
            interval_days = 4
        elif new_score < 0.9:
            interval_days = 7
        else:
            interval_days = 14
        
        next_review = datetime.now() + timedelta(days=interval_days)
        
        return (next_review, new_score)
```

### 4.4 Feature: Progress Tracking & Analytics

#### 4.3.1 Description
Dashboard showing learning progress, statistics, and insights to help user understand their improvement areas.

#### 4.3.2 Metrics Tracked
- Total study time (daily, weekly, monthly)
- Vocabulary learned/mastered
- Grammar accuracy trends
- Most common grammar errors
- Session completion rate
- Streak days
- Category-specific progress (business vs. daily)

#### 4.3.3 API Endpoints

```python
# Get progress dashboard
GET /api/progress/dashboard
Query Parameters:
    - period: "week" | "month" | "all_time"
Response:
{
    "period_stats": {
        "total_sessions": int,
        "total_minutes": int,
        "vocabulary_learned": int,
        "vocabulary_mastered": int,
        "avg_grammar_accuracy": float,
        "current_streak": int
    },
    "grammar_accuracy_trend": [
        {"date": "2026-01-10", "accuracy": 0.85},
        {"date": "2026-01-11", "accuracy": 0.87}
    ],
    "vocabulary_growth": [
        {"date": "2026-01-10", "total": 245, "mastered": 89},
        {"date": "2026-01-11", "total": 252, "mastered": 92}
    ],
    "common_errors": [
        {
            "error_type": "case",
            "count": 15,
            "percentage": 35.7
        }
    ],
    "achievements": [
        {
            "title": "7-day streak",
            "earned_date": "2026-01-15"
        }
    ]
}

# Get detailed error analysis
GET /api/progress/errors
Query Parameters:
    - period: "week" | "month"
    - error_type: str (optional)
Response:
{
    "error_breakdown": [
        {
            "error_type": str,
            "count": int,
            "examples": [
                {
                    "incorrect": str,
                    "corrected": str,
                    "context": str
                }
            ]
        }
    ]
}
```

### 4.5 Feature: Context Library

#### 4.4.1 Description
Pre-defined conversation scenarios covering business and daily life topics. System admin (user) can add custom contexts.

#### 4.4.2 Default Contexts to Include

**Business Contexts:**
1. "Banking Meeting" - Discussing payment solutions, card issuing
2. "Partnership Negotiation" - Discussing partnerships and collaborations
3. "Compliance Discussion" - Regulatory and compliance topics
4. "Team Meeting" - Internal team discussions
5. "Client Presentation" - Presenting solutions to clients
6. "Email Correspondence" - Professional email writing practice

**Daily Life Contexts:**
1. "At the Restaurant" - Ordering food, discussing preferences
2. "Shopping" - Buying items, asking for assistance
3. "Doctor's Appointment" - Medical conversations
4. "Travel Planning" - Discussing trips, transportation
5. "Social Conversation" - Casual chat with friends/colleagues
6. "Housing/Apartment" - Renting, utilities, maintenance

#### 4.4.3 API Endpoints

```python
# List all contexts
GET /api/contexts
Query Parameters:
    - category: "business" | "daily" | "all"
    - difficulty: "B1" | "B2" | "C1" | "C2"
Response:
{
    "contexts": [
        {
            "id": int,
            "name": str,
            "category": str,
            "difficulty_level": str,
            "description": str,
            "times_used": int
        }
    ]
}

# Create custom context
POST /api/contexts
Request Body:
{
    "name": str,
    "category": str,
    "difficulty_level": str,
    "description": str,
    "system_prompt": str,
    "suggested_vocab": [int]  # vocabulary IDs
}

# Get context details
GET /api/contexts/{context_id}
Response:
{
    "id": int,
    "name": str,
    "category": str,
    "difficulty_level": str,
    "description": str,
    "system_prompt": str,
    "suggested_vocab": [
        {
            "id": int,
            "word_de": str,
            "word_it": str
        }
    ],
    "recent_sessions": [
        {
            "session_id": int,
            "date": str,
            "score": float
        }
    ]
}
```

---

## 5. AI Integration Strategy

### 5.1 AI Models Usage

**Primary: Anthropic Claude 3.5 Sonnet**
- Conversation generation
- Grammar analysis
- Feedback generation
- Context understanding

**Rationale:**
- Excellent at nuanced language understanding
- Strong multilingual capabilities (German, Italian, English)
- Good at following complex system prompts
- Reliable JSON output for structured data

### 5.2 Prompt Engineering Guidelines

#### 5.2.1 Conversation System Prompts

```python
CONVERSATION_SYSTEM_PROMPT_TEMPLATE = """You are a German conversation partner helping {user_name}, an advanced German learner at {level} level.

Current Context: {context_description}

Your role:
- Engage naturally in German, staying in character for this context
- Use vocabulary appropriate for {level} level (introduce ~10-15% more advanced words)
- Maintain conversational flow even when user makes errors
- Speak naturally as a native German speaker would in this situation
- Use Swiss German business terminology when relevant to the context

Topics to naturally weave in:
{suggested_topics}

User's background:
- Native Italian speaker, fluent in English
- Works in payments/finance industry in Switzerland
- Particular interest in: {user_interests}

Remember:
- Do NOT correct errors during conversation (that's handled separately)
- Keep responses conversational, not lecture-like
- Vary sentence structure and complexity
- Use authentic German expressions and idioms
- Length: 2-4 sentences per turn unless context requires more
"""

GRAMMAR_ANALYSIS_PROMPT_TEMPLATE = """Analyze the following German text for grammatical errors. The writer is at {level} level.

Text to analyze: "{user_text}"

Requirements:
1. Identify ALL grammatical errors, even minor ones
2. Categorize each error precisely
3. Provide corrections
4. Explain in Italian (writer's native language)
5. Rate severity appropriately for {level} level

Return JSON array with this exact structure:
[
    {{
        "error_type": "case|gender|verb_conjugation|word_order|article|preposition|adjective_ending|syntax|other",
        "incorrect_text": "exact text that is wrong",
        "corrected_text": "corrected version",
        "explanation": "brief explanation in Italian",
        "severity": "minor|moderate|major",
        "rule": "grammar rule name or reference",
        "position": {{ "start": 0, "end": 10 }}
    }}
]

If no errors: return []

Context: This is from a conversation about {context_name}
"""
```

#### 5.2.2 Vocabulary Detection Prompt

```python
VOCABULARY_DETECTION_PROMPT = """Extract key vocabulary from this German text that would be valuable for a {level} learner to track.

Text: "{text}"
Context: {context_name}

Return JSON array:
[
    {{
        "word": "das Wort",
        "lemma": "base form",
        "part_of_speech": "noun|verb|adjective|...",
        "difficulty": "B1|B2|C1|C2",
        "context_category": "business|daily|finance|technical|general",
        "is_idiom": false,
        "is_compound": false
    }}
]

Focus on:
- Technical/business terms
- Less common vocabulary
- Idioms and expressions
- Words relevant to {context_name}

Skip:
- Very common words (articles, pronouns, basic verbs)
- Words already known at A1-A2 level
"""
```

### 5.3 Error Handling & Fallbacks

```python
# ai_service.py
import logging
from typing import Optional

class AIServiceError(Exception):
    """Custom exception for AI service errors"""
    pass

class ConversationAI:
    def __init__(self, api_key: str, fallback_enabled: bool = True):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.fallback_enabled = fallback_enabled
        self.logger = logging.getLogger(__name__)
    
    def generate_response_with_retry(
        self,
        *args,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """Generate response with retry logic"""
        
        for attempt in range(max_retries):
            try:
                return self.generate_response(*args, **kwargs)
            except anthropic.APIError as e:
                self.logger.error(f"API error on attempt {attempt + 1}: {e}")
                
                if attempt == max_retries - 1:
                    if self.fallback_enabled:
                        return self._fallback_response()
                    raise AIServiceError(f"Failed after {max_retries} attempts")
                
                # Exponential backoff
                time.sleep(2 ** attempt)
        
    def _fallback_response(self) -> str:
        """Simple fallback when AI is unavailable"""
        return "Entschuldigung, ich habe gerade technische Probleme. Können Sie das bitte wiederholen?"
```

---

## 6. User Interface & Experience

### 6.1 Main Views

#### 6.1.1 Dashboard (Home)
- Quick stats: Today's progress, current streak, vocabulary due for review, grammar topics due
- Quick start buttons: "Start Conversation", "Review Vocabulary", "Practice Grammar", "Continue Last Session"
- Recent activity feed
- Progress charts (weekly grammar accuracy, vocabulary growth, grammar mastery)

#### 6.1.2 Conversation Interface
- Clean chat-like interface
- User message input area (textarea with German keyboard support)
- AI responses displayed in chat bubbles
- Optional sidebar showing:
  - Real-time vocabulary detection
  - Quick grammar tips
  - Context information
- Feedback toggle (show/hide grammar corrections inline)
- Session timer
- End session button with option to practice detected grammar errors

#### 6.1.3 Grammar Practice Interface
- Topic selection view:
  - Recommended topics (due for review, weak areas, conversation-triggered)
  - Browse by category (cases, verbs, sentence structure, etc.)
  - Search topics
- Grammar explanation modal (detailed rules in German)
- Exercise view:
  - Clear question display
  - Answer input area (varies by exercise type)
  - Progress indicator (5/15)
  - Hint button (progressive hints)
  - Timer (optional)
  - Submit button
- Immediate feedback:
  - Correct/incorrect indicator
  - Detailed explanation in German
  - Similar examples
  - Next exercise button
- Session summary view:
  - Accuracy stats
  - Mastery level update
  - Review of incorrect answers
  - Achievement notifications

#### 6.1.4 Vocabulary Dashboard
- Search and filter controls
- Vocabulary cards showing:
  - German word with article/gender
  - Italian translation
  - Proficiency indicator
  - Last reviewed date
  - Example sentence
- Actions: Review, Edit, Add to favorites
- Spaced repetition queue indicator

#### 6.1.5 Progress Analytics
- Time period selector (week, month, all-time)
- Key metrics cards (including grammar topics mastered)
- Charts:
  - Grammar accuracy over time (line chart)
  - Vocabulary growth (area chart)
  - Grammar mastery heatmap by category
  - Session frequency heatmap
  - Error type distribution (pie chart)
- Detailed error breakdown table with links to practice
- Grammar topic breakdown with mastery levels
- Achievements/badges section

#### 6.1.6 Context Library
- Grid/list view of available contexts
- Filters: Category, difficulty
- Each context card shows:
  - Name and description
  - Difficulty level
  - Times practiced
  - Average score
  - "Start" button
- Create custom context button

### 6.2 UI/UX Principles

1. **Minimal Cognitive Load**: Clean, distraction-free during conversations
2. **Immediate Feedback**: Grammar corrections appear inline but not intrusively
3. **Progress Visibility**: Always show progress indicators and achievements
4. **Flexibility**: Easy to switch between contexts, pause/resume sessions
5. **Mobile-Friendly**: Responsive design (though primary use is desktop/laptop)

### 6.3 Wireframe Structure

```
┌─────────────────────────────────────────────────────────────┐
│  Header: Logo | Dashboard | Vocabulary | Progress | Settings│
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Conversation Area (Main)                      │   │
│  │                                                        │   │
│  │  AI: Guten Tag! Wie kann ich Ihnen helfen?           │   │
│  │                                                        │   │
│  │                     User: Ich möchte über...    [✓]   │   │
│  │                                                        │   │
│  │  AI: Natürlich! ...                                   │   │
│  │                                                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  [Type your message in German...]                    │   │
│  │                                          [Send Button]│   │
│  └──────────────────────────────────────────────────────┘   │
│                                                               │
│  Session: 12 min | Turns: 8 | [Show Feedback] [End Session] │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Development Roadmap

### 7.1 Phase 1: Core Infrastructure (Weeks 1-2)

**Objectives:**
- Set up development environment
- Database design and creation (including grammar tables)
- Basic API structure
- Authentication system

**Deliverables:**
1. PostgreSQL database with all tables created (including grammar module)
2. FastAPI application structure
3. Basic authentication (JWT-based)
4. Database models with SQLAlchemy (users, sessions, vocabulary, contexts, grammar)
5. Alembic migrations setup
6. Basic health check endpoints

### 7.2 Phase 2: AI Integration & Conversation Engine (Weeks 3-4)

**Objectives:**
- Integrate Anthropic Claude API
- Build conversation management system
- Implement grammar analysis with topic mapping
- Create basic conversation UI

**Deliverables:**
1. Working AI conversation service
2. Grammar analysis engine with topic detection
3. Vocabulary detection system
4. Session management API endpoints
5. Basic React conversation interface
6. Real-time conversation functionality
7. Grammar error → topic mapping system

### 7.3 Phase 3: Grammar Learning System (Weeks 5-6)

**Objectives:**
- Build complete grammar module
- Implement diagnostic assessment
- Create exercise generation system
- Build grammar practice UI

**Deliverables:**
1. Grammar topics database (50+ topics with explanations)
2. Exercise generation AI service
3. Manual exercise database (200+ exercises across topics)
4. Diagnostic test system
5. Grammar drill session API
6. Grammar practice UI (topic selection, exercise interface, feedback)
7. Grammar spaced repetition implementation
8. Conversation → grammar practice integration
9. Initial grammar seeding script

### 7.4 Phase 4: Vocabulary System (Week 7)

**Objectives:**
- Build vocabulary management system
- Implement spaced repetition for vocabulary
- Create vocabulary review sessions
- Build vocabulary UI

**Deliverables:**
1. Vocabulary CRUD operations
2. Spaced repetition algorithm
3. Vocabulary review API
4. Vocabulary dashboard UI
5. Initial vocabulary database (500+ words)

### 7.5 Phase 5: Progress Tracking & Analytics (Week 8)

**Objectives:**
- Build comprehensive analytics system
- Create progress snapshots
- Implement achievement system
- Build analytics dashboard UI

**Deliverables:**
1. Progress tracking endpoints (conversation + grammar + vocabulary)
2. Analytics dashboard with grammar heatmaps
3. Achievement/badge system
4. Error pattern analysis (conversation + exercises)
5. Data visualization components
6. Grammar topic mastery tracking

### 7.6 Phase 6: Context Library & Integration (Week 9)

**Objectives:**
- Create default contexts
- Build context management UI
- Integrate all modules seamlessly
- Polish user experience

**Deliverables:**
1. 12+ default contexts (business + daily)
2. Context management API
3. Context library UI
4. Custom context creation interface
5. Seamless flow between conversation → grammar → vocabulary

### 7.7 Phase 7: Testing & Optimization (Week 10)

**Objectives:**
- Comprehensive testing
- Performance optimization
- UI/UX refinements
- Documentation

**Deliverables:**
1. Unit tests (>80% coverage)
2. Integration tests for all workflows
3. Grammar exercise validation
4. User documentation
5. Deployment guide
6. Performance benchmarks

**Technical Tasks:**
```bash
# Project structure
german-learning-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── vocabulary.py
│   │   │   ├── context.py
│   │   │   └── grammar.py  # NEW: Grammar models
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── session.py
│   │   │   ├── vocabulary.py
│   │   │   └── grammar.py  # NEW: Grammar schemas
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── deps.py
│   │   │   ├── auth.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── users.py
│   │   │       ├── sessions.py
│   │   │       ├── vocabulary.py
│   │   │       ├── contexts.py
│   │   │       └── grammar.py  # NEW: Grammar endpoints
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── ai_service.py
│   │   │   ├── vocabulary_service.py
│   │   │   ├── analytics_service.py
│   │   │   └── grammar_ai_service.py  # NEW: Grammar AI service
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── spaced_repetition.py
│   │       └── grammar_spaced_repetition.py  # NEW
│   ├── alembic/
│   ├── tests/
│   ├── scripts/
│   │   └── seed_grammar_data.py  # NEW: Seed grammar topics & exercises
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── conversation/
│   │   │   ├── vocabulary/
│   │   │   └── grammar/  # NEW: Grammar components
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Conversation.jsx
│   │   │   ├── Vocabulary.jsx
│   │   │   ├── Grammar.jsx  # NEW: Grammar practice page
│   │   │   └── Progress.jsx
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   ├── conversationService.js
│   │   │   ├── vocabularyService.js
│   │   │   └── grammarService.js  # NEW
│   │   ├── utils/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── vite.config.js
├── docs/
└── README.md
```

**Key Files:**

```python
# backend/app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # AI Services
    ANTHROPIC_API_KEY: str
    OPENAI_API_KEY: str = None  # Optional fallback
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    APP_NAME: str = "German Learning App"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
---

## 8. Technical Specifications

### 8.1 API Authentication

```python
# JWT-based authentication
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Fetch user from database
    # ...
    return user
```

### 8.2 Database Connection Pooling

```python
# backend/app/database.py
from sqlalchemy.pool import QueuePool

engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600  # Recycle connections after 1 hour
)
```

### 8.3 Caching Strategy

```python
# Use Redis for caching AI responses and vocabulary lookups
from redis import Redis
import json

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

def cache_vocabulary_lookup(word: str, data: dict, ttl: int = 86400):
    """Cache vocabulary lookup for 24 hours"""
    key = f"vocab:{word}"
    redis_client.setex(key, ttl, json.dumps(data))

def get_cached_vocabulary(word: str) -> dict | None:
    """Get cached vocabulary data"""
    key = f"vocab:{word}"
    data = redis_client.get(key)
    return json.loads(data) if data else None
```

### 8.4 Error Logging

```python
# backend/app/main.py
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log all API requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    return response
```

---

## 9. Security Considerations

### 9.1 Data Protection
- User passwords hashed with bcrypt
- JWT tokens for session management
- HTTPS only in production
- SQL injection prevention via SQLAlchemy ORM
- Input validation on all endpoints
- Rate limiting on AI API calls

### 9.2 API Key Management
- Store API keys in environment variables
- Never commit .env file
- Rotate API keys periodically
- Monitor API usage

### 9.3 User Privacy
- No PII sharing with AI services
- User conversations stored locally only
- Option to delete all data
- No analytics tracking without consent

---

## 10. Performance Targets

### 10.1 Response Times
- API endpoints: < 200ms (excluding AI calls)
- AI conversation response: < 3s
- Grammar analysis: < 2s
- Page load: < 1s
- Vocabulary lookup: < 100ms

### 10.2 Scalability
- Support 1 concurrent user initially (single-user app)
- Database optimized for 10,000+ vocabulary entries
- Efficient indexing for fast lookups
- AI API rate limit handling

---

## 11. Testing Strategy

### 11.1 Unit Tests
- All service functions
- Spaced repetition algorithm
- Database models
- API endpoint logic

### 11.2 Integration Tests
- Full conversation flow
- Vocabulary review session
- Progress tracking
- AI service integration

### 11.3 Manual Testing Checklist
- [ ] User registration and login
- [ ] Start conversation session
- [ ] Grammar correction accuracy in conversations
- [ ] Grammar error → topic mapping accuracy
- [ ] Vocabulary detection
- [ ] Take diagnostic test
- [ ] Start grammar drill session
- [ ] Complete 15-exercise drill
- [ ] Receive conversation-triggered grammar practice prompt
- [ ] View grammar topic explanation
- [ ] Request hints during exercises
- [ ] Review incorrect exercises
- [ ] Track grammar mastery progression
- [ ] Spaced repetition calculations (vocab + grammar)
- [ ] Progress dashboard accuracy (all modules)
- [ ] Context switching
- [ ] Custom context creation
- [ ] Session history retrieval
- [ ] Error handling across all modules
- [ ] AI exercise generation quality

---

## 12. Deployment

### 12.1 Local Development Setup

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create database
createdb german_learning

# Run migrations
alembic upgrade head

# Seed initial data (contexts, vocabulary)
python scripts/seed_data.py

# Start server
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### 12.2 Production Deployment (Ubuntu Server)

```bash
# Install dependencies
sudo apt update
sudo apt install postgresql nginx python3-pip

# Setup database
sudo -u postgres createdb german_learning
sudo -u postgres createuser german_app

# Clone repository
git clone [repo-url]
cd german-learning-app

# Backend setup
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit with actual values

# Run migrations
alembic upgrade head

# Setup systemd service
sudo nano /etc/systemd/system/german-app.service
```

**systemd service file:**
```ini
[Unit]
Description=German Learning App
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/german-learning-app/backend
Environment="PATH=/path/to/german-learning-app/backend/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
# Start service
sudo systemctl enable german-app
sudo systemctl start german-app

# Frontend build
cd ../frontend
npm install
npm run build

# Configure Nginx
sudo nano /etc/nginx/sites-available/german-app
```

**Nginx configuration:**
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

---

## 13. Maintenance & Monitoring

### 13.1 Regular Tasks
- Weekly database backup
- Monthly vocabulary database updates
- API usage monitoring
- Error log review
- Performance metrics check

### 13.2 Monitoring
```python
# Simple monitoring endpoint
@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "database": check_db_connection(),
        "ai_service": check_ai_service(),
        "timestamp": datetime.now().isoformat()
    }
```

---

## 14. Future Enhancements (Phase 2)

### 14.1 Voice Integration
- Speech-to-text for spoken practice
- Text-to-speech for listening practice
- Pronunciation evaluation
- Accent analysis

### 14.2 Advanced Features
- Writing exercises with essay evaluation
- Reading comprehension tests
- Listening exercises with transcripts
- Mobile app (React Native)
- Offline mode
- Multi-user support (if needed)
- Export progress reports

### 14.3 Content Expansion
- Video lessons integration
- Podcast recommendations
- News article practice
- Cultural context lessons

---

## 15. Success Metrics & KPIs

### 15.1 Learning Effectiveness
- Vocabulary retention rate > 80%
- Grammar topic mastery improvement trend
- Grammar accuracy improvement in conversations
- Session completion rate > 85%
- User engagement: 5+ sessions/week (conversation + grammar combined)
- Grammar drill completion rate > 90%
- Diagnostic test improvement over time

### 15.2 Technical Performance
- API uptime > 99%
- Average response time < targets
- Zero data loss
- AI API cost per session < $0.15 (increased for grammar generation)
- Exercise generation success rate > 95%

---

## 16. Appendices

### 16.1 Glossary of Terms

- **Spaced Repetition**: Learning technique using increasing intervals between reviews
- **Familiarity Score**: 0.0-1.0 metric of how well user knows a vocabulary item
- **Context**: Predefined conversation scenario/topic
- **Turn**: Single message exchange in conversation
- **Session**: Complete practice session from start to end

### 16.2 Reference Documents

- SQLAlchemy 2.0 Documentation
- FastAPI Documentation
- Anthropic Claude API Documentation
- German Grammar Reference (Duden)
- CEFR Level Descriptors (A1-C2)

### 16.3 Sample Data Structures

**Example Context:**
```json
{
    "id": 1,
    "name": "Banking Meeting - Payment Solutions",
    "category": "business",
    "difficulty_level": "C1",
    "description": "Discussion about payment processing solutions and card issuing with banking partners",
    "system_prompt": "You are a senior banking executive discussing payment solutions. Focus on technical terminology around card issuing, payment processing, compliance, and partnerships. Be professional but approachable.",
    "suggested_vocab": [101, 102, 103, 205, 301]
}
```

**Example Vocabulary Item:**
```json
{
    "id": 101,
    "word_de": "die Kartenzahlung",
    "word_it": "il pagamento con carta",
    "word_en": "card payment",
    "part_of_speech": "noun",
    "difficulty_level": "B2",
    "context_category": "business",
    "example_sentence_de": "Die Kartenzahlung hat in den letzten Jahren stark zugenommen.",
    "example_sentence_it": "Il pagamento con carta è aumentato notevolmente negli ultimi anni.",
    "gender": "die",
    "plural_form": "die Kartenzahlungen"
}
```

**Example Grammar Topic:**
```json
{
    "id": 15,
    "name_de": "Dativ mit Präpositionen",
    "name_en": "Dative with Prepositions",
    "category": "cases",
    "subcategory": "dative",
    "difficulty_level": "B1",
    "explanation_de": "Bestimmte Präpositionen verlangen immer den Dativ. Die wichtigsten sind: aus, bei, mit, nach, seit, von, zu, gegenüber, außer. Der Artikel und das Substantiv müssen im Dativ stehen. Beispiele: 'Ich komme aus dem Haus' (das Haus → dem Haus), 'Sie spricht mit der Lehrerin' (die Lehrerin → der Lehrerin), 'Er geht zu den Freunden' (die Freunde → den Freunden)."
}
```

**Example Grammar Exercise:**
```json
{
    "id": 523,
    "topic_id": 15,
    "exercise_type": "fill_blank",
    "difficulty_level": "B1",
    "question_text": "Ich fahre ____ (zu/der) Bahnhof.",
    "question_data": {
        "blank_position": 2,
        "preposition": "zu",
        "article": "der",
        "noun": "Bahnhof"
    },
    "correct_answer": "zum",
    "alternative_answers": ["zu dem"],
    "explanation_de": "Die Präposition 'zu' verlangt den Dativ. Der bestimmte Artikel 'der' (Nominativ maskulin) wird zu 'dem' (Dativ maskulin). Die Kombination 'zu + dem' wird standardmäßig zu 'zum' kontrahiert.",
    "hints": [
        "Welcher Fall folgt auf 'zu'?",
        "Wie lautet der Dativartikel für maskuline Substantive?",
        "Kannst du 'zu' und 'dem' kombinieren?"
    ],
    "context_category": "daily"
}
```

**Example Session Summary:**
```json
{
    "session_id": 42,
    "user_id": 1,
    "context": "Banking Meeting - Payment Solutions",
    "duration_minutes": 25,
    "total_turns": 12,
    "grammar_accuracy": 0.87,
    "vocabulary_used_count": 18,
    "new_vocabulary_count": 3,
    "overall_score": 0.85,
    "achievements": ["5_session_streak", "business_vocab_expert"],
    "areas_for_improvement": [
        {
            "area": "Dative case with prepositions",
            "error_count": 2,
            "recommendation": "Review dative case rules",
            "grammar_topic_id": 15,
            "practice_available": true
        }
    ]
}
```

**Example Grammar Drill Session Summary:**
```json
{
    "grammar_session_id": 88,
    "user_id": 1,
    "topic": {
        "id": 15,
        "name_de": "Dativ mit Präpositionen"
    },
    "session_type": "conversation_triggered",
    "total_exercises": 15,
    "exercises_correct": 13,
    "exercises_incorrect": 2,
    "accuracy_rate": 0.867,
    "time_spent_minutes": 12,
    "mastery_before": 0.62,
    "mastery_after": 0.71,
    "mastery_change": 0.09,
    "weak_subtopics": [
        "Kontraktion (zu+dem→zum)"
    ],
    "next_review_date": "2026-01-20",
    "triggered_by_conversation": 42
}
```

**Example Diagnostic Test Results:**
```json
{
    "test_id": 5,
    "user_id": 1,
    "test_date": "2026-01-16T10:00:00Z",
    "overall_level": "B2",
    "total_questions": 30,
    "correct_answers": 22,
    "accuracy": 0.733,
    "topic_scores": {
        "cases": 0.80,
        "verb_conjugation": 0.58,
        "sentence_structure": 0.75,
        "prepositions": 0.67,
        "adjectives": 0.83,
        "passive_voice": 0.50
    },
    "weak_areas": [
        {"topic_id": 23, "topic_name": "Konjunktiv II", "score": 0.33},
        {"topic_id": 18, "topic_name": "Passiv", "score": 0.50},
        {"topic_id": 12, "topic_name": "Perfekt mit sein/haben", "score": 0.58}
    ],
    "strong_areas": [
        {"topic_id": 8, "topic_name": "Adjektivdeklination", "score": 0.83},
        {"topic_id": 3, "topic_name": "Akkusativ", "score": 0.80}
    ],
    "recommended_learning_path": [
        {"topic_id": 23, "priority": 1, "reason": "lowest_score"},
        {"topic_id": 18, "priority": 2, "reason": "weak_area"},
        {"topic_id": 12, "priority": 3, "reason": "needs_improvement"}
    ]
}
```

---

## 17. Development Best Practices

### 17.1 Code Style
- Follow PEP 8 for Python
- Use type hints
- Write docstrings for all functions
- Keep functions focused and small
- Meaningful variable names

### 17.2 Git Workflow
- Feature branches for new features
- Descriptive commit messages
- Regular commits
- Code review before merging

### 17.3 Documentation
- Update README for major changes
- Document all API endpoints
- Inline comments for complex logic
- Keep this BRD updated

---

## Document Control

**Version History:**
- v1.0 (2026-01-16): Initial comprehensive BRD
- v1.1 (2026-01-17): Added comprehensive Grammar Learning Module
  - 6 new database tables for grammar system
  - Diagnostic assessment system
  - Exercise generation with AI
  - 50+ grammar topics coverage
  - Drill sessions (15+ exercises per topic)
  - Conversation-triggered practice
  - Grammar spaced repetition
  - Extended roadmap to 10 weeks

**Approval:**
- Created for: Igor (User & Developer)
- Created by: Claude (Anthropic)
- Purpose: Development guide for Claude Code

**Next Review:** After Phase 3 completion (Grammar Module)

---

**END OF DOCUMENT**
