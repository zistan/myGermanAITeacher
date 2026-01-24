# Backend Database Schema Codemap

**Last Updated:** 2026-01-22
**Entry Points:** `app/models/__init__.py` (20 model exports), `app/database.py`

## Overview

The German Learning Application database uses PostgreSQL with SQLAlchemy ORM, featuring 22 database models organized across 7 files. The schema supports comprehensive language learning with conversation tracking, grammar drilling (50+ topics, 200+ exercises), vocabulary management (150+ words with spaced repetition), and gamification (31 achievements across 4 tiers).

**Database Statistics:**
- **Total Tables:** 22
- **Total Models:** 22 (4 core, 6 grammar, 7 vocabulary, 4 analytics, 1 corrections)
- **Models Exported:** 20 (`FlashcardSession` and `VocabularyQuiz` not exported in __init__.py)
- **Foreign Keys:** 35+ relationships
- **Unique Constraints:** 7 (prevent duplicate data)
- **Indexes:** 50+ indexed columns (performance optimization)
- **Spaced Repetition:** 2 systems (grammar & vocabulary with different algorithms)

## Database Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         CORE TABLES (4)                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐                                                        │
│  │  users   │◄──────────────┐                                       │
│  └────┬─────┘               │                                       │
│       │ 1:N                 │ 1:N                                   │
│       │                     │                                       │
│  ┌────▼─────────┐     ┌─────┴──────┐                               │
│  │  sessions    │────►│  contexts   │                               │
│  └────┬─────────┘     └────────────┘                               │
│       │ 1:N                                                          │
│       │                                                              │
│  ┌────▼──────────────┐                                              │
│  │ conversation_turns │                                              │
│  └────────────────────┘                                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                      GRAMMAR MODULE (6 tables)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐                                                │
│  │ grammar_topics  │◄──┐  (hierarchical: parent_topic_id)           │
│  └────┬────────────┘   │                                            │
│       │ 1:N            │                                            │
│       │                │                                            │
│  ┌────▼──────────────┐ │                                            │
│  │ grammar_exercises │ │                                            │
│  └────┬──────────────┘ │                                            │
│       │                │                                            │
│       │ N:1            │ N:1                                        │
│  ┌────▼───────────────────────┐       ┌──────────────────────┐     │
│  │ user_grammar_progress      │◄──────│  users               │     │
│  │ (spaced repetition)        │       └──────────────────────┘     │
│  └────────────────────────────┘                                     │
│                                                                      │
│  ┌──────────────────┐                                               │
│  │ grammar_sessions │◄───users (1:N)                                │
│  └────┬─────────────┘                                               │
│       │ 1:N                                                          │
│       │                                                              │
│  ┌────▼────────────────────────┐                                    │
│  │ grammar_exercise_attempts   │                                    │
│  └─────────────────────────────┘                                    │
│                                                                      │
│  ┌───────────────────┐                                              │
│  │ diagnostic_tests  │◄───users (1:N)                               │
│  └───────────────────┘                                              │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                   VOCABULARY MODULE (7 tables)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐                                                   │
│  │ vocabulary   │                                                   │
│  └────┬─────────┘                                                   │
│       │ 1:N                                                          │
│       │                                                              │
│  ┌────▼──────────────────────────┐       ┌──────────────────┐      │
│  │ user_vocabulary_progress      │◄──────│  users           │      │
│  │ (SM-2 spaced repetition)      │       └──────────────────┘      │
│  └───────────────────────────────┘                                  │
│                                                                      │
│  ┌───────────────────────────────┐                                  │
│  │ user_vocabulary_lists         │◄──users (1:N)                    │
│  └────┬──────────────────────────┘                                  │
│       │ 1:N                                                          │
│       │                                                              │
│  ┌────▼──────────────────────┐                                      │
│  │ vocabulary_list_words     │───►vocabulary (N:1)                  │
│  │ (many-to-many)            │                                      │
│  └───────────────────────────┘                                      │
│                                                                      │
│  ┌───────────────────────┐                                          │
│  │ vocabulary_reviews    │◄──users + vocabulary (N:1)               │
│  │ (review history)      │                                          │
│  └───────────────────────┘                                          │
│                                                                      │
│  ┌────────────────────────┐                                         │
│  │ flashcard_sessions     │◄──users (1:N)  [DB-persisted]           │
│  │ (multi-worker safe)    │                                         │
│  └────────────────────────┘                                         │
│                                                                      │
│  ┌────────────────────────┐                                         │
│  │ vocabulary_quizzes     │◄──users (1:N)  [DB-persisted]           │
│  │ (multi-worker safe)    │                                         │
│  └────────────────────────┘                                         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    ANALYTICS MODULE (4 tables)                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐                                                   │
│  │ achievements │                                                   │
│  └────┬─────────┘                                                   │
│       │ 1:N                                                          │
│       │                                                              │
│  ┌────▼──────────────────┐       ┌──────────────────┐              │
│  │ user_achievements     │◄──────│  users           │              │
│  │ (progress tracking)   │       └──────────────────┘              │
│  └───────────────────────┘                                          │
│                                                                      │
│  ┌───────────────────┐                                              │
│  │ user_stats        │◄──users (1:1)  [aggregate statistics]        │
│  │ (leaderboards)    │                                              │
│  └───────────────────┘                                              │
│                                                                      │
│  ┌────────────────────────┐                                         │
│  │ progress_snapshots     │◄──users (1:N)  [historical tracking]    │
│  └────────────────────────┘                                         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                 CROSS-MODULE TABLES (1 table)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌────────────────────────┐                                         │
│  │ grammar_corrections    │◄──users, conversation_turns, topics     │
│  │ (conversation errors)  │                                         │
│  └────────────────────────┘                                         │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

## Model Organization

### Core Models (4 tables)

| Table | Model | Purpose | Key Fields | Relationships |
|-------|-------|---------|------------|---------------|
| `users` | User | User accounts and authentication | username, email, password_hash, proficiency_level | achievements, stats, progress_snapshots |
| `contexts` | Context | Conversation scenarios (12+ default) | name, category, system_prompt, difficulty_level | - |
| `sessions` | Session | Practice sessions (conversation) | user_id, context_id, session_type, scores | user (N:1), context (N:1) |
| `conversation_turns` | ConversationTurn | Individual conversation messages | session_id, speaker, message_text, feedback | session (N:1) |

### Grammar Module (6 tables)

| Table | Model | Purpose | Key Fields | Relationships |
|-------|-------|---------|------------|---------------|
| `grammar_topics` | GrammarTopic | Grammar topics (50+ topics) | name_de, category, difficulty_level, parent_topic_id | self-referential (hierarchy) |
| `grammar_exercises` | GrammarExercise | Grammar exercises (200+ manual) | topic_id, exercise_type, question_text, correct_answer | topic (N:1) |
| `user_grammar_progress` | UserGrammarProgress | Progress tracking with spaced repetition | user_id, topic_id, mastery_level (0.0-1.0), next_review_date | user (N:1), topic (N:1) |
| `grammar_sessions` | GrammarSession | Practice session tracking | user_id, topic_id, total_exercises, exercises_correct | user (N:1), topic (N:1) |
| `grammar_exercise_attempts` | GrammarExerciseAttempt | Individual exercise answers | grammar_session_id, exercise_id, user_answer, is_correct | session (N:1), exercise (N:1) |
| `diagnostic_tests` | DiagnosticTest | Assessment results | user_id, overall_level, topic_scores, weak_areas | user (N:1) |

### Vocabulary Module (7 tables)

| Table | Model | Purpose | Key Fields | Relationships |
|-------|-------|---------|------------|---------------|
| `vocabulary` | Vocabulary | Vocabulary words (150+ words) | word, translation_it, part_of_speech, difficulty, category | - |
| `user_vocabulary_progress` | UserVocabularyProgress | Progress with SM-2 spaced repetition | user_id, word_id, mastery_level (0-5), ease_factor, interval_days | user (N:1), word (N:1) |
| `user_vocabulary_lists` | UserVocabularyList | Custom vocabulary lists | user_id, name, description, is_public | user (N:1) |
| `vocabulary_list_words` | VocabularyListWord | List-word association (many-to-many) | list_id, word_id, notes | list (N:1), word (N:1) |
| `vocabulary_reviews` | VocabularyReview | Review history for analytics | user_id, word_id, review_type, was_correct, confidence_rating | user (N:1), word (N:1) |
| `flashcard_sessions` | FlashcardSession | Flashcard practice sessions (DB-persisted) | user_id, total_cards, current_index, cards_data (JSON) | user (N:1) |
| `vocabulary_quizzes` | VocabularyQuiz | Quiz sessions (DB-persisted) | user_id, quiz_type, questions_data (JSON) | user (N:1) |

### Analytics Module (4 tables)

| Table | Model | Purpose | Key Fields | Relationships |
|-------|-------|---------|------------|---------------|
| `achievements` | Achievement | Achievement definitions (31 total) | name, category, tier (bronze/silver/gold/platinum), points | user_achievements (1:N) |
| `user_achievements` | UserAchievement | Earned achievements | user_id, achievement_id, progress_value, is_completed | user (N:1), achievement (N:1) |
| `user_stats` | UserStats | Aggregate statistics for leaderboards | user_id, total_study_time, current_streak, grammar/vocab stats | user (1:1) |
| `progress_snapshots` | ProgressSnapshot | Historical progress snapshots | user_id, snapshot_date, snapshot_type, stats (JSON) | user (N:1) |

### Cross-Module Tables (1 table)

| Table | Model | Purpose | Key Fields | Relationships |
|-------|-------|---------|------------|---------------|
| `grammar_corrections` | GrammarCorrection | Grammar errors from conversations | turn_id, user_id, grammar_topic_id, error_type, severity | turn (N:1), user (N:1), topic (N:1) |

## Detailed Model Documentation

### Core Models

#### User (users)

```python
# Primary authentication and profile model
id: Integer (PK, indexed)
username: String(50) (unique, indexed)
email: String(255) (unique, indexed)
password_hash: String(255)

# Language settings
native_language: String(10) = "it"
target_language: String(10) = "de"
proficiency_level: String(10) = "B2"  # A1-C2

# Timestamps
created_at: TIMESTAMP
last_login: TIMESTAMP

# JSON settings
settings: JSON = {}

# Relationships
achievements → UserAchievement (1:N)
stats → UserStats (1:1)
progress_snapshots → ProgressSnapshot (1:N)
```

#### Context (contexts)

```python
# Conversation scenarios for AI practice
id: Integer (PK, indexed)
name: String(100)
category: String(50) (indexed)  # business, daily, finance, social
difficulty_level: String(10) (indexed)  # B1, B2, C1, C2
description: Text
system_prompt: Text  # Claude system prompt
suggested_vocab: JSON  # Array of vocabulary IDs
is_active: Boolean = True
created_at: TIMESTAMP
```

#### Session (sessions)

```python
# Practice session tracking
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
context_id: Integer (FK contexts.id, indexed)
session_type: String(50) = "conversation"

# Timing
started_at: TIMESTAMP (indexed)
ended_at: TIMESTAMP
duration_minutes: Integer

# Metrics
total_turns: Integer = 0
grammar_errors: Integer = 0
vocab_score: Float  # 0.0-1.0
fluency_score: Float  # 0.0-1.0
overall_score: Float  # 0.0-1.0

# AI tracking
ai_model_used: String(50)
session_summary: Text
metadata: JSON (Column name: "metadata")
```

**Metadata Column Note:** Uses `Column("metadata", JSON)` to avoid SQLAlchemy reserved keyword conflict.

#### ConversationTurn (conversation_turns)

```python
# Individual messages in conversations
id: Integer (PK, indexed)
session_id: Integer (FK sessions.id, CASCADE, indexed)
turn_number: Integer
speaker: String(20)  # 'user' or 'ai'
message_text: Text
timestamp: TIMESTAMP

# AI analysis
grammar_feedback: JSON  # Array of corrections
vocabulary_used: JSON  # Array of vocabulary IDs
ai_evaluation: JSON
metadata: JSON (Column name: "metadata")

# Composite index
Index("idx_conversation_turns_session_turn", session_id, turn_number)
```

### Grammar Module Models

#### GrammarTopic (grammar_topics)

```python
# Grammar topics with hierarchical structure
id: Integer (PK, indexed)
name_de: String(255)  # German name
name_en: String(255)  # English name
category: String(100) (indexed)  # cases, verbs, sentence_structure
subcategory: String(100)
difficulty_level: String(10) (indexed)  # A1-C2
parent_topic_id: Integer (FK grammar_topics.id)  # Self-referential
order_index: Integer  # Sequential learning path
description_de: Text
explanation_de: Text  # Detailed explanation in German
created_at: TIMESTAMP
```

**Hierarchical Structure:** Topics can have parent-child relationships via `parent_topic_id`.

#### GrammarExercise (grammar_exercises)

```python
# Grammar practice exercises
id: Integer (PK, indexed)
topic_id: Integer (FK grammar_topics.id, indexed)
exercise_type: String(50) (indexed)  # fill_blank, multiple_choice, etc.
difficulty_level: String(10) (indexed)

# Exercise content
question_text: Text
question_data: JSON  # Exercise-specific data (options, blanks)

# Answers
correct_answer: Text
alternative_answers: JSON  # Array of acceptable alternatives

# Explanations
explanation_de: Text
explanation_it: Text  # Optional Italian explanation
hints: JSON  # Array of progressive hints

# Categorization
context_category: String(50)  # business, daily, general
source: String(50) = "manual"  # manual, ai_generated
is_active: Boolean = True
created_at: TIMESTAMP
metadata: JSON (Column name: "metadata")
```

**Exercise Types:**
- `fill_blank` - Fill-in-the-blank exercises
- `multiple_choice` - Multiple choice questions
- `translation` - Translation exercises
- `error_correction` - Find and correct errors
- `sentence_building` - Construct sentences from words

#### UserGrammarProgress (user_grammar_progress)

```python
# Spaced repetition progress tracking for grammar
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
topic_id: Integer (FK grammar_topics.id)

# Progress metrics
mastery_level: Float = 0.0 (indexed)  # 0.0-1.0 (5 levels)
total_exercises_attempted: Integer = 0
total_exercises_correct: Integer = 0
total_exercises_incorrect: Integer = 0
current_streak: Integer = 0

# Spaced repetition (exponential backoff)
last_practiced: TIMESTAMP
next_review_date: TIMESTAMP (indexed)

# Weak areas
weak_subtopics: JSON  # Array of problematic subtopics
notes: Text

# Unique constraint
UniqueConstraint(user_id, topic_id, name="uq_user_grammar_topic")
```

**Spaced Repetition Algorithm:** Exponential backoff (1→2→4→8→16→30 days)

#### GrammarSession (grammar_sessions)

```python
# Grammar practice sessions
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
topic_id: Integer (FK grammar_topics.id, indexed)
triggered_by_conversation_id: Integer (FK sessions.id)
session_type: String(50) = "drill"  # drill, diagnostic, review, conversation_triggered

# Timing
started_at: TIMESTAMP (indexed)
ended_at: TIMESTAMP

# Performance
total_exercises: Integer = 0
exercises_correct: Integer = 0
exercises_incorrect: Integer = 0
accuracy_rate: Float
completion_rate: Float

# Summary
session_summary: JSON
metadata: JSON (Column name: "metadata")
```

#### GrammarExerciseAttempt (grammar_exercise_attempts)

```python
# Individual exercise answers
id: Integer (PK, indexed)
grammar_session_id: Integer (FK grammar_sessions.id, CASCADE, indexed)
exercise_id: Integer (FK grammar_exercises.id, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)

# Attempt data
user_answer: Text
is_correct: Boolean
time_spent_seconds: Integer
hints_used: Integer = 0
attempt_number: Integer = 1  # Retry tracking

# Feedback
feedback_given: Text
timestamp: TIMESTAMP
```

#### DiagnosticTest (diagnostic_tests)

```python
# Grammar assessment tests
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
test_date: TIMESTAMP (indexed)

# Results
overall_level: String(10)  # B1, B2, C1 (determined level)
total_questions: Integer
correct_answers: Integer
test_duration_minutes: Integer

# Detailed analysis (JSON)
topic_scores: JSON  # {"cases": 0.75, "verbs": 0.60, ...}
weak_areas: JSON  # Array of topics needing work
strong_areas: JSON  # Array of mastered topics
recommended_path: JSON  # Suggested learning sequence
```

### Vocabulary Module Models

#### Vocabulary (vocabulary)

```python
# Vocabulary word definitions
id: Integer (PK, indexed)

# Translations
word: String(255) (unique, indexed)  # German word with article
translation_it: String(255)
word_en: String(255)  # English translation

# Grammatical info
part_of_speech: String(50)  # noun, verb, adjective
gender: String(10)  # masculine, feminine, neuter
plural_form: String(255)

# Categorization
difficulty: String(10) (indexed)  # A1-C2
category: String(50) (indexed)  # business, daily, finance, verbs

# Examples
example_de: Text  # German example sentence
example_it: Text  # Italian example sentence
definition_de: Text
usage_notes: Text
pronunciation: String(255)

# Word properties (Integer booleans: 0=false, 1=true)
synonyms: Text  # JSON array
antonyms: Text  # JSON array
is_idiom: Integer = 0
is_compound: Integer = 0
is_separable_verb: Integer = 0

# Tracking
created_at: TIMESTAMP
last_reviewed: TIMESTAMP
review_count: Integer = 0

# Unique constraint (migration 003)
UniqueConstraint(word, name="uq_vocabulary_word")
```

**Boolean Fields:** Stored as Integer (0/1) for PostgreSQL compatibility.

#### UserVocabularyProgress (user_vocabulary_progress)

```python
# SM-2 spaced repetition for vocabulary
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
word_id: Integer (FK vocabulary.id, CASCADE)

# Progress (6 mastery levels: 0-5)
mastery_level: Integer = 0 (indexed)  # 0=new, 1-5=increasing mastery
confidence_score: Float = 0.0  # 0.0-1.0
times_reviewed: Integer = 0
times_correct: Integer = 0
times_incorrect: Integer = 0
current_streak: Integer = 0

# Spaced repetition (SM-2 inspired)
last_reviewed: TIMESTAMP
first_reviewed: TIMESTAMP
next_review_date: TIMESTAMP (indexed)
ease_factor: Float = 2.5  # SM-2 ease factor
interval_days: Integer = 1  # Days until next review

# Personal notes
personal_note: Text

# Unique constraint
UniqueConstraint(user_id, word_id, name="uq_user_vocabulary_progress")
```

**Spaced Repetition Algorithm:** SM-2 inspired with confidence-based interval adjustment.

#### UserVocabularyList (user_vocabulary_lists)

```python
# Custom vocabulary lists
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
name: String(255)
description: Text
is_public: Integer = 0  # Boolean: 0=private, 1=public
color: String(50)  # UI organization
created_at: TIMESTAMP
updated_at: TIMESTAMP (auto-update on modification)
```

#### VocabularyListWord (vocabulary_list_words)

```python
# Many-to-many association: lists ↔ words
id: Integer (PK, indexed)
list_id: Integer (FK user_vocabulary_lists.id, CASCADE, indexed)
word_id: Integer (FK vocabulary.id, CASCADE, indexed)
notes: Text  # Custom notes for word in this list
added_at: TIMESTAMP

# Unique constraint
UniqueConstraint(list_id, word_id, name="uq_list_word")
```

#### VocabularyReview (vocabulary_reviews)

```python
# Historical review tracking
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)
word_id: Integer (FK vocabulary.id, CASCADE, indexed)

# Review details
review_type: String(50)  # flashcard, quiz, conversation
was_correct: Integer  # 0=incorrect, 1=correct
confidence_rating: Integer  # 1-5 (optional user rating)
time_spent_seconds: Integer
reviewed_at: TIMESTAMP (indexed)
```

#### FlashcardSession (flashcard_sessions) **[Multi-Worker Safe]**

```python
# Database-persisted flashcard sessions
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)

# Timing
started_at: TIMESTAMP
ended_at: TIMESTAMP

# Session state
total_cards: Integer
current_index: Integer = 0
cards_data: Text  # JSON string of flashcard data
use_spaced_repetition: Integer = 1  # Boolean

# Filters
category: String(50)
difficulty: String(10)
```

**Multi-Worker Safety:** Replaced in-memory dictionary with database persistence (BUG-015, BUG-016 fix).

#### VocabularyQuiz (vocabulary_quizzes) **[Multi-Worker Safe]**

```python
# Database-persisted quiz sessions
id: Integer (PK, indexed)
user_id: Integer (FK users.id, CASCADE, indexed)

# Timing
created_at: TIMESTAMP
completed_at: TIMESTAMP

# Quiz configuration
quiz_type: String(50)  # multiple_choice, fill_blank, matching
total_questions: Integer
questions_data: Text  # JSON string of quiz questions

# Filters
category: String(50)
difficulty: String(10)
```

**Multi-Worker Safety:** Replaced in-memory dictionary with database persistence (BUG-015, BUG-016 fix).

### Analytics Module Models

#### Achievement (achievements)

```python
# Achievement definitions (31 total)
id: Integer (PK, indexed)
name: String(100) (unique)
description: Text
category: String(50)  # conversation, grammar, vocabulary, activity
badge_icon: String(50)
badge_color: String(20)

# Criteria
criteria_type: String(50)  # sessions_count, words_learned, streak, mastery
criteria_value: Integer  # Threshold value
criteria_metadata: JSON  # Additional criteria details

# Rarity
tier: String(20)  # bronze, silver, gold, platinum
points: Integer = 0  # Achievement points awarded

is_active: Boolean = True
created_at: DateTime

# Relationships
user_achievements → UserAchievement (1:N)
```

**Achievement Tiers:**
- Bronze: 7 achievements
- Silver: 7 achievements
- Gold: 10 achievements
- Platinum: 7 achievements
- **Total Points:** 5,825

#### UserAchievement (user_achievements)

```python
# User's earned achievements
id: Integer (PK, indexed)
user_id: Integer (FK users.id)
achievement_id: Integer (FK achievements.id)

earned_at: DateTime
progress_value: Integer = 0  # Current progress toward achievement
is_completed: Boolean = False

# Display settings
is_showcased: Boolean = False  # Display on profile
showcase_order: Integer = 0

# Relationships
user → User
achievement → Achievement
```

#### UserStats (user_stats)

```python
# Aggregate statistics for leaderboards
id: Integer (PK, indexed)
user_id: Integer (FK users.id, unique)  # 1:1 relationship

# Overall
total_study_time_minutes: Integer = 0
total_sessions: Integer = 0
current_streak_days: Integer = 0
longest_streak_days: Integer = 0
last_activity_date: DateTime

# Conversation
conversation_sessions: Integer = 0
total_messages_sent: Integer = 0

# Grammar
grammar_sessions: Integer = 0
grammar_exercises_completed: Integer = 0
grammar_exercises_correct: Integer = 0
grammar_topics_mastered: Integer = 0
average_grammar_accuracy: Integer = 0  # Percentage

# Vocabulary
vocabulary_words_learned: Integer = 0
vocabulary_words_mastered: Integer = 0
vocabulary_reviews_completed: Integer = 0
vocabulary_reviews_correct: Integer = 0
average_vocabulary_accuracy: Integer = 0  # Percentage

# Achievements
total_achievement_points: Integer = 0
achievements_earned: Integer = 0

# Rankings (updated periodically)
overall_rank: Integer
grammar_rank: Integer
vocabulary_rank: Integer

updated_at: DateTime (auto-update)

# Relationships
user → User (1:1)
```

#### ProgressSnapshot (progress_snapshots)

```python
# Historical progress tracking
id: Integer (PK, indexed)
user_id: Integer (FK users.id)

snapshot_date: DateTime
snapshot_type: String(50) = "weekly"  # daily, weekly, monthly

# JSON snapshot data
overall_progress: JSON
conversation_stats: JSON
grammar_stats: JSON
vocabulary_stats: JSON
activity_stats: JSON
error_analysis: JSON

# Summary metrics
overall_score: Integer  # 0-100
total_sessions: Integer
study_time_minutes: Integer

created_at: DateTime

# Relationships
user → User
```

### Cross-Module Models

#### GrammarCorrection (grammar_corrections)

```python
# Grammar errors from conversations
id: Integer (PK, indexed)

# Foreign keys (links conversations → grammar topics)
turn_id: Integer (FK conversation_turns.id, CASCADE)
user_id: Integer (FK users.id, CASCADE, indexed)
grammar_topic_id: Integer (FK grammar_topics.id, indexed)

# Error details
error_type: String(100) (indexed)  # case, gender, verb_conjugation
incorrect_text: Text
corrected_text: Text

# Explanation
explanation: Text
rule_reference: Text
severity: String(20)  # minor, moderate, major

created_at: TIMESTAMP
```

**Purpose:** Links conversation errors to grammar topics for targeted practice recommendations.

## Foreign Key Relationships

### CASCADE Deletes (Data Cleanup)

When a user is deleted, these records are automatically deleted:

```sql
users.id CASCADE →
  - sessions (user_id)
  - user_grammar_progress (user_id)
  - grammar_sessions (user_id)
  - grammar_exercise_attempts (user_id)
  - user_vocabulary_progress (user_id)
  - user_vocabulary_lists (user_id)
  - vocabulary_reviews (user_id)
  - flashcard_sessions (user_id)
  - vocabulary_quizzes (user_id)
  - user_achievements (user_id)
  - grammar_corrections (user_id)

sessions.id CASCADE →
  - conversation_turns (session_id)

grammar_sessions.id CASCADE →
  - grammar_exercise_attempts (grammar_session_id)

user_vocabulary_lists.id CASCADE →
  - vocabulary_list_words (list_id)

vocabulary.id CASCADE →
  - user_vocabulary_progress (word_id)
  - vocabulary_list_words (word_id)
  - vocabulary_reviews (word_id)
```

### Standard Foreign Keys (No CASCADE)

```sql
sessions.context_id → contexts.id
grammar_exercises.topic_id → grammar_topics.id
user_grammar_progress.topic_id → grammar_topics.id
grammar_sessions.topic_id → grammar_topics.id
user_achievements.achievement_id → achievements.id
grammar_corrections.grammar_topic_id → grammar_topics.id
```

### Self-Referential Foreign Key

```sql
grammar_topics.parent_topic_id → grammar_topics.id
```

**Purpose:** Hierarchical topic organization (e.g., "Dative Case" → "Prepositions with Dative")

## Indexing Strategy

### Primary Indexes (All Tables)

- All tables have `id` column indexed (primary key)

### User-Related Indexes

```sql
users.username (unique, indexed)
users.email (unique, indexed)
```

### Foreign Key Indexes (Performance)

```sql
sessions.user_id, sessions.context_id
conversation_turns.session_id
grammar_sessions.user_id, grammar_sessions.topic_id
grammar_exercise_attempts.grammar_session_id, grammar_exercise_attempts.exercise_id, grammar_exercise_attempts.user_id
user_grammar_progress.user_id, user_grammar_progress.mastery_level
user_vocabulary_progress.user_id, user_vocabulary_progress.mastery_level
vocabulary_reviews.user_id, vocabulary_reviews.word_id
flashcard_sessions.user_id
vocabulary_quizzes.user_id
grammar_corrections.user_id, grammar_corrections.grammar_topic_id
```

### Spaced Repetition Indexes

```sql
user_grammar_progress.next_review_date
user_vocabulary_progress.next_review_date
```

**Purpose:** Efficiently query due items for review.

### Categorization Indexes

```sql
contexts.category, contexts.difficulty_level
grammar_topics.category, grammar_topics.difficulty_level
grammar_exercises.exercise_type, grammar_exercises.difficulty_level
vocabulary.difficulty, vocabulary.category
```

### Time-Based Indexes

```sql
sessions.started_at
grammar_sessions.started_at
diagnostic_tests.test_date
vocabulary_reviews.reviewed_at
```

### Composite Index

```sql
Index("idx_conversation_turns_session_turn", conversation_turns.session_id, conversation_turns.turn_number)
```

**Purpose:** Efficiently query conversation turns in order.

## Unique Constraints

### User Uniqueness

```sql
users.username (unique)
users.email (unique)
```

### Achievement Uniqueness

```sql
achievements.name (unique)
```

### Progress Tracking Uniqueness

```sql
UniqueConstraint(user_id, topic_id) → user_grammar_progress
UniqueConstraint(user_id, word_id) → user_vocabulary_progress
```

**Purpose:** Prevent duplicate progress records per user-topic/word pair.

### List Management Uniqueness

```sql
UniqueConstraint(list_id, word_id) → vocabulary_list_words
```

**Purpose:** Prevent duplicate words in a single list.

### Vocabulary Uniqueness

```sql
UniqueConstraint(word) → vocabulary (migration 003)
```

**Purpose:** Allow `ON CONFLICT (word) DO NOTHING` in bulk inserts.

### Stats Uniqueness

```sql
user_stats.user_id (unique)
```

**Purpose:** Ensure 1:1 relationship between users and stats.

## Special Features

### 1. Spaced Repetition Algorithms

**Grammar (Exponential Backoff):**
```
Mastery Level: 0.0 → 0.2 → 0.4 → 0.6 → 0.8 → 1.0
Interval Days:  1  →  2  →  4  →  8  → 16  → 30
```

**Vocabulary (SM-2 Inspired):**
```
Mastery Level: 0 → 1 → 2 → 3 → 4 → 5
Ease Factor: 2.5 (adjusted based on performance)
Interval Days: Calculated using SM-2 algorithm with confidence scoring
```

### 2. Session Persistence (Multi-Worker Safe)

**Problem:** In-memory dictionaries lost data across Uvicorn workers and server restarts.

**Solution:** Database-backed sessions using `flashcard_sessions` and `vocabulary_quizzes` tables.

```python
# Before (BUG-015, BUG-016):
flashcard_sessions = {}  # Lost on worker change or restart

# After (fixed):
session = FlashcardSession(
    id=session_id,
    user_id=user.id,
    cards_data=json.dumps(cards)  # Persisted in PostgreSQL
)
db.add(session)
db.commit()
```

### 3. Hierarchical Structure

**Grammar Topics:**
```
Topic 1: Cases
├── Topic 1.1: Nominative Case
├── Topic 1.2: Accusative Case
│   └── Topic 1.2.1: Prepositions with Accusative
└── Topic 1.3: Dative Case
```

**Implementation:**
```python
parent_topic_id: Integer (FK grammar_topics.id)
```

### 4. JSON Flexible Storage

**Use Cases:**
- `settings` (users) - User preferences
- `suggested_vocab` (contexts) - Vocabulary IDs array
- `question_data` (grammar_exercises) - Exercise-specific data
- `weak_subtopics` (user_grammar_progress) - Problematic areas
- `session_summary` (grammar_sessions) - Summary data
- `topic_scores` (diagnostic_tests) - Detailed test results
- All `metadata` columns - Flexible expansion

### 5. Boolean Handling

**Integer Booleans (0/1):**
- `is_idiom`, `is_compound`, `is_separable_verb` (vocabulary)
- `is_public` (user_vocabulary_lists)
- `was_correct` (vocabulary_reviews)
- `use_spaced_repetition` (flashcard_sessions)

**Reason:** PostgreSQL compatibility and explicit storage.

**True Booleans:**
- `is_active` (contexts, grammar_exercises, achievements)
- `is_correct` (grammar_exercise_attempts)
- `is_completed`, `is_showcased` (user_achievements)

### 6. Metadata Column Naming

**Problem:** SQLAlchemy reserves `metadata` attribute for table metadata.

**Solution:** Explicit column naming:
```python
session_metadata = Column("metadata", JSON, default={})
```

**Affected Models:**
- Session, ConversationTurn, GrammarExercise, GrammarSession

## Connection Pooling

### Configuration (database.py)

```python
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,           # Maintain 10 connections
    max_overflow=20,        # Allow 20 additional connections (30 total max)
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=3600,      # Recycle connections after 1 hour
    echo=settings.DEBUG     # Log SQL queries in debug mode
)
```

**Benefits:**
- **Performance:** Reuse connections instead of creating new ones
- **Reliability:** Pre-ping detects stale connections
- **Stability:** Recycle prevents connection timeouts

## Migration History

### Migration 001: Update Vocabulary Schema
**Date:** 2026-01-17
**Purpose:** Align vocabulary table with SQLAlchemy model

**Changes:**
- Renamed columns: `word_de` → `word`, `word_it` → `translation_it`, `difficulty_level` → `difficulty`, `context_category` → `category`, `example_sentence_de` → `example_de`, `example_sentence_it` → `example_it`, `notes` → `usage_notes`
- Added columns: `definition_de`, `pronunciation`, `synonyms`, `antonyms`, `is_idiom`, `is_compound`, `is_separable_verb`
- Renamed table: `user_vocabulary` → `user_vocabulary_progress`
- Renamed columns: `vocabulary_id` → `word_id`, `familiarity_score` → `confidence_score`, `times_encountered` → `times_reviewed`, `last_encountered` → `last_reviewed`, `first_encountered` → `first_reviewed`, `notes` → `personal_note`
- Added columns: `mastery_level`, `current_streak`, `ease_factor`, `interval_days`
- Created tables: `user_vocabulary_lists`, `vocabulary_list_words`, `vocabulary_reviews`

### Migration 002: Add Vocabulary Sessions
**Date:** 2026-01-19
**Purpose:** Fix multi-worker session persistence (BUG-015, BUG-016)

**Changes:**
- Created `flashcard_sessions` table with indexes on `id` and `user_id`
- Created `vocabulary_quizzes` table with indexes on `id` and `user_id`
- Replaced in-memory dictionaries with database persistence

**Impact:** Sessions now persist across Uvicorn workers and server restarts.

### Migration 003: Add Vocabulary Word Unique Constraint
**Date:** 2026-01-21
**Purpose:** Allow bulk insert with conflict handling

**Changes:**
- Added unique constraint `uq_vocabulary_word` on `vocabulary.word`
- Enables `ON CONFLICT (word) DO NOTHING` in bulk insert operations

## Statistics Summary

| Category | Count | Details |
|----------|-------|---------|
| **Total Tables** | 19 | 4 core, 6 grammar, 7 vocabulary, 4 analytics, 1 corrections |
| **Total Models** | 19 | All models exported from `app/models/__init__.py` |
| **Foreign Keys** | 35+ | Relationships across modules |
| **Unique Constraints** | 7 | Prevent duplicate data |
| **Indexed Columns** | 50+ | Performance optimization |
| **Grammar Topics** | 50+ | Seeded from `seed_grammar_data.py` |
| **Grammar Exercises** | 200+ | Manual exercises across 5 types |
| **Vocabulary Words** | 150+ | Foundation for 1000+ words |
| **Achievements** | 31 | 7 bronze, 7 silver, 10 gold, 7 platinum |
| **Achievement Points** | 5,825 | Total points available |
| **Conversation Contexts** | 12+ | 6 business, 6 daily scenarios |

## Data Types

### Timestamps
- **TIMESTAMP:** Used in most models (grammar, vocabulary, conversation)
- **DateTime:** Used in analytics models (achievement, progress)

### Booleans
- **Boolean:** SQLAlchemy Boolean type (achievements, exercises)
- **Integer (0/1):** Explicit boolean storage (vocabulary properties)

### Text Storage
- **String(N):** Fixed-length fields (names, categories)
- **Text:** Unlimited text (descriptions, explanations, notes)
- **JSON:** Structured flexible data (settings, metadata, arrays)

### Numeric Types
- **Integer:** Counts, IDs, rankings
- **Float:** Scores, ratios (0.0-1.0), ease factors

## Related Areas

- **[Backend Architecture](backend.md)** - Overall backend structure and entry points
- **[API Architecture](backend-api.md)** - Service layer and endpoint organization
- **[Deployment Guide](/docs/GUIDES/deployment/DEPLOYMENT_GUIDE.md)** - Database setup and migrations
- **[Troubleshooting Guide](/docs/GUIDES/troubleshooting/TROUBLESHOOTING.md)** - Database connection issues

---

**Database Summary:**

The database schema supports a comprehensive language learning platform with:
1. **Multi-module architecture** (core, grammar, vocabulary, analytics)
2. **Dual spaced repetition systems** (grammar exponential, vocabulary SM-2)
3. **Hierarchical organization** (grammar topics, achievement tiers)
4. **Multi-worker safety** (database-persisted sessions)
5. **Comprehensive tracking** (progress, reviews, achievements, corrections)
6. **Performance optimization** (50+ indexes, connection pooling)
7. **Data integrity** (7 unique constraints, 35+ foreign keys)

All tables are production-ready with proper indexing, foreign key constraints, and CASCADE delete behavior for data cleanup.
