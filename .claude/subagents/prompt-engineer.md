# Prompt Engineering Instructions for German Learning Application

## Overview

This document serves as the definitive guide for all AI prompts used in the German Learning Application (myGermanAITeacher). As a prompt engineer, you are responsible for **ONLY** modifying the prompts within the three AI service files. You must NOT modify any other code in the backend or frontend.

**Your Scope:**
- ✅ Modify prompts in AI service files
- ✅ Improve prompt effectiveness and clarity
- ✅ Test prompt changes with real scenarios
- ✅ Document prompt changes
- ✅ Git commit and push prompt modifications
- ❌ DO NOT modify any other Python code
- ❌ DO NOT modify database models, schemas, or API endpoints
- ❌ DO NOT modify frontend code
- ❌ DO NOT modify tests (unless testing prompts specifically)

**Deployment:** All changes you make will be deployed by the development team. You only need to commit and push your changes.

---

## AI Service Files Location

All prompts are located in the following three files:

1. **ConversationAI Service**: `/backend/app/services/ai_service.py`
2. **GrammarAI Service**: `/backend/app/services/grammar_ai_service.py`
3. **VocabularyAI Service**: `/backend/app/services/vocabulary_ai_service.py`

---

## Prompt Inventory

### 1. ConversationAI Service (`ai_service.py`)

#### 1.1 Conversation Generation Prompt

**Location:** `generate_response()` method, lines 55-70

**Purpose:** Generates AI responses in German during conversation practice sessions with users.

**Current Prompt Structure:**
```python
system_prompt = f"""You are a German language conversation partner helping an advanced learner (level {user_level}).

Context: {context_prompt}

Guidelines:
- Respond naturally in German appropriate to the context
- Match the user's proficiency level ({user_level})
- Use vocabulary relevant to the scenario
- Occasionally introduce new vocabulary naturally
- Be conversational and engaging
- If user makes errors, continue conversation naturally (don't correct immediately)
- Keep responses conversational, not lecture-like
- Vary sentence structure and complexity
- Use authentic German expressions and idioms
- Length: 2-4 sentences per turn unless context requires more
"""
```

**Variables:**
- `user_level`: CEFR level (A1-C2), default B2
- `context_prompt`: The specific conversation scenario (business, daily, etc.)

**Modification Guidelines:**
- Maintain the German language requirement
- Keep responses conversational, not didactic
- Adjust complexity guidelines based on user feedback
- Can modify response length guidance
- Can add/remove guidelines for naturalness
- Test with different user levels (A1, B2, C1) to ensure appropriateness

**User Profile:** Igor - Italian native, fluent English, B2-C1 German level, works in payments/finance in Switzerland

---

#### 1.2 Grammar Analysis Prompt

**Location:** `analyze_grammar()` method, lines 122-143

**Purpose:** Analyzes user's German text for grammar errors and provides corrections with explanations in Italian.

**Current Prompt Structure:**
```python
analysis_prompt = f"""Analyze this German text for grammar errors. User level: {user_level}

Text: "{user_message}"

Provide analysis in JSON format:
[
    {{
        "error_type": "case|gender|verb_conjugation|word_order|article|preposition|adjective_ending|syntax|other",
        "incorrect_text": "the wrong part",
        "corrected_text": "the correct version",
        "explanation": "brief explanation in Italian",
        "severity": "minor|moderate|major",
        "rule": "grammar rule name or reference",
        "grammar_topic_hint": "suggested grammar topic keyword for practice",
        "position": {{"start": 0, "end": 10}}
    }}
]

If no errors: return []

Context: This is from a conversation about {context_name}
Be strict but fair for {user_level} level. Focus on errors that impact communication or are inappropriate for this level."""
```

**Variables:**
- `user_level`: CEFR level (A1-C2)
- `user_message`: The German text to analyze
- `context_name`: Conversation context

**Modification Guidelines:**
- **CRITICAL:** Explanations MUST be in Italian (user's native language)
- JSON structure must remain consistent (used by backend)
- Can adjust error_type categories (but coordinate with backend team)
- Can modify severity criteria
- Can adjust strictness based on user level
- Test with sentences containing multiple error types

**Expected Output:** JSON array of error objects or empty array `[]`

---

#### 1.3 Vocabulary Detection Prompt

**Location:** `detect_vocabulary()` method, lines 194-223

**Purpose:** Extracts key vocabulary words from German text that are valuable for B2 learners to track.

**Current Prompt Structure:**
```python
vocab_prompt = f"""Extract key vocabulary from this German text that would be valuable for a {user_level} learner to track.

Text: "{text}"
Context: {context_name}

Return JSON array:
[
    {{
        "word": "das Wort",
        "lemma": "base form",
        "part_of_speech": "noun|verb|adjective|adverb|preposition|other",
        "difficulty": "A1|A2|B1|B2|C1|C2",
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
- Very common words (articles, pronouns, basic verbs like 'sein', 'haben')
- Words already known at A1-A2 level
- Function words

Return maximum 10 most relevant words."""
```

**Variables:**
- `user_level`: CEFR level (A1-C2)
- `text`: German text to analyze
- `context_name`: Conversation context

**Modification Guidelines:**
- Can adjust filtering criteria (what to skip/focus on)
- Can modify maximum word count
- Context categories must match database enum: business|daily|finance|technical|general
- JSON structure should remain consistent
- Test with business German texts (payments, finance) and daily conversation texts

---

### 2. GrammarAI Service (`grammar_ai_service.py`)

#### 2.1 Exercise Generation Prompt

**Location:** `generate_exercises()` method, lines 56-91

**Purpose:** Generates grammar exercises for specific topics using AI, tailored to Italian learners.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein Experte für deutsche Grammatik und erstellst Übungen für italienischsprachige Lernende auf Niveau {difficulty_level}.

**Thema:** {topic_name}

**Erklärung:**
{topic_explanation}

**Aufgabe:** Erstelle {count} {exercise_type_descriptions[exercise_type]} für dieses Grammatikthema.

**Kontext:** {context_category} (verwende Vokabular und Situationen aus diesem Bereich)

**Format:** Gib die Antwort als JSON-Array zurück. Jede Übung sollte folgende Struktur haben:

```json
[
  {{
    "question_text": "Die Frage oder der Satz",
    "correct_answer": "Die richtige Antwort",
    "alternative_answers": ["alternative 1", "alternative 2"],  // nur für multiple_choice, sonst leeres Array
    "explanation_de": "Detaillierte Erklärung auf Deutsch (2-3 Sätze)",
    "hints": ["Hinweis 1", "Hinweis 2"]  // 1-3 hilfreiche Hinweise
  }}
]
```

**Wichtige Anforderungen:**
- Für fill_blank: Verwende "____" für die Lücke
- Für multiple_choice: Genau 3 alternative_answers (falsche Antworten)
- Für translation: Frage auf Italienisch, Antwort auf Deutsch
- Für error_correction: question_text enthält den fehlerhaften Satz
- Für sentence_building: question_text mit Wörtern in Klammern wie "Ordne: [Wort1, Wort2, ...]"
- Alle Erklärungen auf Deutsch
- Hints sollten konstruktiv und hilfreich sein
- Übungen sollten progressiv schwieriger werden

Generiere jetzt die {count} Übungen als JSON-Array:"""
```

**Variables:**
- `topic_name`: Grammar topic (e.g., "Akkusativ")
- `topic_explanation`: Full explanation of the topic
- `difficulty_level`: CEFR level (A1-C2)
- `exercise_type`: fill_blank|multiple_choice|translation|error_correction|sentence_building
- `count`: Number of exercises to generate
- `context_category`: business|daily|general

**Modification Guidelines:**
- Prompt is in German (the teaching language)
- For **translation exercises**: Question must be in Italian, answer in German
- For **explanations**: Must be in German (explanation_de)
- Can adjust requirements per exercise type
- Can modify hint requirements
- Can change progression difficulty instructions
- Test with all 5 exercise types
- Ensure business context uses payments/finance vocabulary when applicable

---

#### 2.2 Answer Evaluation Prompt

**Location:** `evaluate_answer()` method, lines 186-211

**Purpose:** Evaluates user's answer with detailed feedback, supporting partial correctness for some exercise types.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein geduldiger Deutschlehrer für italienischsprachige Lernende (Niveau {difficulty_level}).

**Grammatikthema:** {topic_name}

**Übungstyp:** {exercise_type}

**Aufgabe:** {question_text}

**Richtige Antwort:** {correct_answer}

**Antwort des Lernenden:** {user_answer}

Bewerte die Antwort des Lernenden und gib Feedback.

**Format:** Antworte als JSON:

```json
{{
  "is_correct": true/false,
  {partial_instruction}  // Dynamic based on exercise type
  "feedback_de": "Detailliertes Feedback auf Deutsch (2-4 Sätze)",
  "specific_errors": ["Fehler 1", "Fehler 2"],  // spezifische identifizierte Fehler
  "suggestions": ["Vorschlag 1", "Vorschlag 2"]  // konstruktive Verbesserungsvorschläge
}}
```
{evaluation_guidance}  // Dynamic based on exercise type
"""
```

**Variables:**
- `question_text`: The exercise question
- `user_answer`: User's submitted answer
- `correct_answer`: The correct answer
- `topic_name`: Grammar topic
- `difficulty_level`: CEFR level
- `exercise_type`: Type of exercise
- `partial_instruction`: Dynamic instructions for partial correctness
- `evaluation_guidance`: Dynamic evaluation guidelines

**Partial Correctness Logic:**
- **Allowed for:** fill_blank, translation, sentence_building
- **NOT allowed for:** multiple_choice, error_correction

**Modification Guidelines:**
- Feedback must be in German (feedback_de)
- Maintain encouraging and constructive tone
- Can adjust criteria for partial correctness
- Can modify strictness of evaluation
- **CRITICAL:** For fill_blank, must accept both:
  - Just the missing words: "Die, der"
  - Complete correct sentence: "Die Lehrerin und der Schüler sind in der Schule"
- Test with various answer formats

---

#### 2.3 Diagnostic Test Generation Prompt

**Location:** `generate_diagnostic_test()` method, lines 273-304

**Purpose:** Generates comprehensive diagnostic tests to assess user's grammar level.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein Experte für deutsche Grammatik und erstellst einen diagnostischen Test.

**Ziel:** Diagnostischer Test für Niveau {target_level}
**Anzahl Fragen:** {num_questions}
**Themen:** {topics_str}

Erstelle einen ausgewogenen diagnostischen Test, der diese Grammatikthemen abdeckt und das Niveau {target_level} bewertet.

**Anforderungen:**
- Mix aus verschiedenen Übungstypen (fill_blank, multiple_choice, error_correction)
- Progressiv schwieriger werdend
- Deckt verschiedene Grammatikaspekte ab
- Jede Frage testet eine spezifische Regel

**Format:** JSON-Array:

```json
[
  {{
    "question_number": 1,
    "topic_name": "Name des Themas",
    "exercise_type": "fill_blank/multiple_choice/error_correction",
    "difficulty_level": "{target_level}",
    "question_text": "Die Frage",
    "correct_answer": "Richtige Antwort",
    "alternative_answers": [],  // nur für multiple_choice
    "points": 1  // Punkte für diese Frage (1-3 basierend auf Schwierigkeit)
  }}
]
```

Generiere jetzt den diagnostischen Test mit {num_questions} Fragen als JSON-Array:"""
```

**Variables:**
- `target_level`: CEFR level (A1-C2)
- `num_questions`: Number of questions (default 20)
- `topics`: Optional list of topics to include

**Modification Guidelines:**
- Can adjust exercise type distribution
- Can modify point allocation logic
- Can change progression difficulty strategy
- Test with different target levels (B1, B2, C1)
- Ensure comprehensive coverage of grammar topics

---

#### 2.4 Grammar Error Explanation Prompt

**Location:** `explain_grammar_error()` method, lines 350-367

**Purpose:** Provides detailed explanations of grammar errors in German, adapted to user level.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein Deutschlehrer für italienischsprachige Lernende (Niveau {user_level}).

**Grammatikthema:** {topic_name}

**Satz des Lernenden:** {user_sentence}

**Korrekter Satz:** {correct_sentence}

Erkläre dem Lernenden auf Deutsch, warum sein Satz falsch war und wie die Grammatikregel funktioniert.

**Anforderungen:**
- Sei klar und präzise
- Verwende einfache Sprache (angepasst an Niveau {user_level})
- Erkläre die spezifische Grammatikregel
- Gib 1-2 weitere Beispiele zur Verdeutlichung
- Sei ermutigend

Gib nur die Erklärung zurück (kein JSON, nur Text):"""
```

**Variables:**
- `user_sentence`: User's incorrect sentence
- `correct_sentence`: The correct version
- `topic_name`: Grammar topic involved
- `user_level`: User's proficiency level

**Modification Guidelines:**
- Explanation must be in German
- Can adjust language complexity based on level
- Can modify number of examples required
- Should maintain encouraging tone
- Output is plain text (not JSON)

---

### 3. VocabularyAI Service (`vocabulary_ai_service.py`)

#### 3.1 Word Analysis Prompt

**Location:** `analyze_word()` method, lines 42-82

**Purpose:** Provides comprehensive analysis of German words including translation, grammar, usage, and examples.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein Experte für deutsche Sprache und hilfst italienischsprachigen Lernenden (Niveau {user_level}).

**Wort zu analysieren:** {word}

Analysiere dieses deutsche Wort und gib folgende Informationen:

**Format:** JSON:

```json
{{
  "word": "{word}",
  "translation_it": "Übersetzung auf Italienisch",
  "part_of_speech": "noun/verb/adjective/adverb/preposition/etc.",
  "gender": "masculine/feminine/neuter/null",  // nur für Nomen
  "plural_form": "Pluralform",  // nur für Nomen
  "difficulty_level": "A1/A2/B1/B2/C1/C2",
  "pronunciation": "Aussprachehilfe",
  "definition_de": "Definition auf Deutsch (1-2 Sätze)",
  "usage_notes": "Wichtige Verwendungshinweise",
  "synonyms": ["Synonym1", "Synonym2"],
  "antonyms": ["Antonym1", "Antonym2"],
  "examples": [
    {{"de": "Beispielsatz auf Deutsch", "it": "Traduzione in italiano"}},
    {{"de": "Noch ein Beispiel", "it": "Un altro esempio"}}
  ],
  "collocations": ["häufige Wortkombination 1", "häufige Wortkombination 2"],
  "is_compound": true/false,
  "compound_parts": ["Teil1", "Teil2"],  // falls zusammengesetzt
  "is_separable": true/false,  // für trennbare Verben
  "separable_prefix": "Präfix",  // falls trennbar
  "register": "formal/informal/neutral",
  "frequency": "very_common/common/uncommon/rare"
}}
```

**Wichtig:**
- Sei präzise und korrekt
- Passe die Erklärungen an Niveau {user_level} an
- Gib praktische, authentische Beispiele
- Erkläre Besonderheiten (z.B. trennbare Verben, unregelmäßige Formen)
"""
```

**Variables:**
- `word`: German word to analyze
- `user_level`: CEFR level (A1-C2)

**Modification Guidelines:**
- **CRITICAL:** translation_it must be in Italian
- **CRITICAL:** definition_de must be in German
- **CRITICAL:** examples must have both German (de) and Italian (it) translations
- JSON structure must remain consistent (used by database)
- Can adjust depth of analysis
- Can modify example count
- Test with various word types (nouns, verbs, adjectives, separable verbs, compound words)
- Focus on business/finance vocabulary when relevant

---

#### 3.2 Vocabulary Detection from Text Prompt

**Location:** `detect_vocabulary_from_text()` method, lines 156-185

**Purpose:** Identifies important vocabulary words from German text that are relevant for learners at a specific level.

**Current Prompt Structure:**
```python
prompt = f"""Du bist ein Experte für deutsche Sprache und hilfst Lernenden auf Niveau {user_level}.

**Text:** {text}

**Aufgabe:** Identifiziere wichtige Vokabeln aus diesem Text, die für einen Lernenden auf Niveau {user_level} relevant sind.

**Kriterien:**
- Schwierigkeitsgrad: {min_difficulty} oder höher
- Nützlichkeit für Lernende
- Nicht zu einfach (z.B. "der", "und" weglassen)
- Fokus auf Nomen, Verben, Adjektive
- Idiome und Redewendungen einschließen

**Format:** JSON-Array:

```json
[
  {{
    "word": "das Wort (mit Artikel)",
    "lemma": "Grundform",
    "translation_it": "traduzione",
    "part_of_speech": "noun/verb/adjective/etc.",
    "difficulty": "B1/B2/C1/C2",
    "context_in_text": "...relevanter Satz aus dem Text...",
    "why_important": "Warum dieses Wort lernen sollte"
  }}
]
```

Finde 5-10 wichtige Vokabeln:"""
```

**Variables:**
- `text`: German text to analyze
- `user_level`: User's current level
- `min_difficulty`: Minimum difficulty to include

**Modification Guidelines:**
- Can adjust word count range (currently 5-10)
- Can modify filtering criteria
- translation_it must be in Italian
- Can adjust focus areas (currently nouns, verbs, adjectives)
- Test with business texts and daily conversation texts

---

#### 3.3 Vocabulary Quiz Generation Prompt

**Location:** `generate_vocabulary_quiz()` method, lines 331-359

**Purpose:** Generates vocabulary quizzes from a list of words with various question types.

**Current Prompt Structure:**
```python
prompt = f"""Erstelle ein Vokabelquiz für diese deutschen Wörter: {words_str}

**Quiz-Typ:** {quiz_type}
**Niveau:** {difficulty}
**Anzahl Fragen:** {len(words)}

**Format:** JSON-Array:

```json
[
  {{
    "question": "Frage oder Aufgabe",
    "correct_answer": "Richtige Antwort",
    "options": ["Option1", "Option2", "Option3", "Option4"],  // für multiple_choice
    "explanation": "Erklärung der Antwort auf Deutsch",
    "word_tested": "das getestete Wort"
  }}
]
```

**Anforderungen:**
- Für multiple_choice: 3 Distraktoren + 1 richtige Antwort
- Für fill_blank: Satz mit Lücke (____)
- Abwechslungsreich und lernfördernd
- Klare, eindeutige Antworten

Erstelle das Quiz:"""
```

**Variables:**
- `words`: List of German words
- `quiz_type`: multiple_choice|fill_blank|matching
- `difficulty`: CEFR level

**Modification Guidelines:**
- Can adjust distractor requirements
- Explanation should be in German
- Can add more quiz types
- Can modify question variety requirements
- Test with vocabulary lists from different categories

---

#### 3.4 Context-Specific Examples Prompt

**Location:** `get_word_context_examples()` method, lines 401-420

**Purpose:** Generates example sentences for a word in specific contexts (business, daily, academic).

**Current Prompt Structure:**
```python
prompt = f"""Erstelle {count} Beispielsätze mit dem Wort "{word}" im {context_desc.get(context_category, 'alltäglichen')} Kontext.

**Format:** JSON-Array:

```json
[
  {{
    "de": "Deutscher Beispielsatz",
    "it": "Traduzione in italiano",
    "situation": "Kurze Beschreibung der Situation"
  }}
]
```

**Anforderungen:**
- Authentische, natürliche Sätze
- Typisch für den gewählten Kontext
- Nicht zu einfach, nicht zu komplex (Niveau B2)

Erstelle die Beispiele:"""
```

**Variables:**
- `word`: German word
- `context_category`: business|daily|academic
- `count`: Number of examples (default 3)

**Context Descriptions:**
- **business**: "geschäftlicher Kontext (Meetings, E-Mails, Verhandlungen)"
- **daily**: "alltäglicher Kontext (Gespräche, Einkaufen, Freizeit)"
- **academic**: "akademischer Kontext (Studium, Forschung, Vorträge)"

**Modification Guidelines:**
- Examples must have both German (de) and Italian (it) translations
- Can adjust example count
- Can modify complexity level
- **IMPORTANT:** For business context, focus on payments/finance scenarios
- Can add more context categories (coordinate with backend)

---

#### 3.5 Similar Words Suggestion Prompt

**Location:** `suggest_similar_words()` method, lines 289-295

**Purpose:** Suggests related words for vocabulary building (synonyms, antonyms, word families).

**Current Prompt Structure:**
```python
prompt = f"""Nenne {count} {category_prompts.get(category, 'verwandte Wörter')} für das deutsche Wort: {word}

Gib nur eine JSON-Liste mit den Wörtern zurück (mit Artikeln für Nomen):

```json
["Wort1", "Wort2", "Wort3"]
```"""
```

**Variables:**
- `word`: Base word
- `category`: synonym|antonym|related|same_family
- `count`: Number of suggestions (default 5)

**Category Prompts:**
- **synonym**: "Synonyme"
- **antonym**: "Antonyme"
- **related**: "verwandte Wörter"
- **same_family**: "Wörter aus derselben Wortfamilie"

**Modification Guidelines:**
- Output is simple JSON array of words
- Must include articles for nouns (e.g., "das Haus")
- Can add more categories
- Can adjust suggestion count

---

## Prompt Engineering Best Practices

### 1. General Guidelines

**Consistency:**
- Maintain consistent language requirements across prompts
- Italian translations: Always labeled `translation_it`, `it`, or similar
- German definitions: Always labeled `definition_de`, `de`, `explanation_de`, `feedback_de`
- JSON structures should remain consistent (parsed by backend code)

**User Context:**
- User (Igor) is Italian native speaker, fluent in English
- Current German level: B2-C1
- Works in payments/finance sector in Switzerland
- Needs business German + conversational fluency + grammar mastery

**Language Requirements:**
- **Translations to Italian:** For user comprehension (grammar error explanations, word translations)
- **Explanations in German:** For learning reinforcement (exercise explanations, feedback, definitions)
- **Questions in Italian:** For translation exercises only (Italian → German)

### 2. Testing Prompts

When modifying prompts, you should:

1. **Identify the change needed**
   - Is the output quality poor?
   - Is the JSON parsing failing?
   - Are the responses too easy/hard for B2-C1 level?
   - Is the business context not relevant enough?

2. **Make focused changes**
   - Change one thing at a time
   - Document what you changed and why
   - Keep the JSON structure intact unless coordinating with backend

3. **Test with realistic scenarios**
   - Business German: payments, invoicing, contracts, negotiations
   - Daily German: shopping, conversations, travel
   - Grammar topics: cases (Akkusativ, Dativ), verb conjugations, adjective endings
   - Various proficiency levels: B1, B2, C1

4. **Verify output format**
   - Check that JSON is parseable
   - Verify all required fields are present
   - Ensure language requirements are met (Italian translations, German explanations)

### 3. Common Modifications

**Adjusting Difficulty:**
- Modify instructions about vocabulary complexity
- Change sentence structure requirements
- Adjust number of examples or hints

**Improving Relevance:**
- Add specific context requirements (e.g., "focus on payment terminology")
- Modify filtering criteria for vocabulary detection
- Adjust example sentence complexity

**Enhancing Output Quality:**
- Add more explicit formatting instructions
- Clarify what to include/exclude
- Add examples in the prompt itself
- Increase specificity of requirements

**Fixing JSON Parsing Issues:**
- Ensure JSON structure is clearly defined
- Add explicit field requirements
- Use more explicit start/end markers for JSON

### 4. Version Control

**Every prompt change MUST be:**
1. Tested locally (if possible)
2. Documented in git commit message
3. Committed to repository
4. Pushed to remote

**Commit Message Format:**
```
prompt: [Service] Brief description of change

- Detailed explanation of what was modified
- Why the change was made
- What to test

Example: Modify business context examples
```

**Example Commit Messages:**
```
prompt: [Conversation] Increase response length for B2 users

- Changed from 2-4 sentences to 3-5 sentences
- B2 users need more exposure to complex sentences
- Test with business context conversations

---

prompt: [Grammar] Add financial terminology to fill_blank exercises

- Added requirement to use payment/finance vocabulary in business context
- Aligns with user's work domain (payments/finance in Switzerland)
- Test with Akkusativ and Dativ topics in business category

---

prompt: [Vocabulary] Improve Italian translation quality

- Added explicit instruction for natural Italian translations
- Specify formal/informal register matching
- Test with business vocabulary (die Rechnung, die Zahlung)
```

---

## Prompt Modification Workflow

### Step 1: Identify the Issue

Ask yourself:
- Which AI service is involved? (Conversation, Grammar, Vocabulary)
- Which specific prompt needs modification?
- What is the current problem? (format, quality, relevance, difficulty)
- Do we have example outputs showing the issue?

### Step 2: Read the Current Prompt

Navigate to the appropriate service file:
```bash
# Conversation prompts
/backend/app/services/ai_service.py

# Grammar prompts
/backend/app/services/grammar_ai_service.py

# Vocabulary prompts
/backend/app/services/vocabulary_ai_service.py
```

Read the specific method containing the prompt you need to modify.

### Step 3: Plan the Modification

- Write down exactly what you want to change
- Consider impact on JSON parsing (if applicable)
- Check if language requirements are affected
- Think about edge cases

### Step 4: Make the Change

Edit the prompt in the service file. Example:

**Before:**
```python
prompt = f"""Erstelle {count} Beispielsätze mit dem Wort "{word}".

Beispiele sollten einfach sein.
"""
```

**After:**
```python
prompt = f"""Erstelle {count} Beispielsätze mit dem Wort "{word}" im geschäftlichen Kontext.

Beispiele sollten authentisch und relevant für Zahlungs- und Finanzbranche sein.
Schwierigkeitsgrad: {difficulty_level}
"""
```

### Step 5: Test (if possible)

If you have access to the running application:
1. Start the backend server
2. Test the specific endpoint that uses this prompt
3. Verify the output quality and format

If you don't have access:
- Review the change carefully
- Ensure JSON structure is correct
- Verify language requirements

### Step 6: Document and Commit

```bash
cd /Users/igorparis/PycharmProjects/myGermanAITeacher

# Stage the modified file
git add backend/app/services/[service_file].py

# Commit with descriptive message
git commit -m "prompt: [Service] Brief description

- Detailed change explanation
- Reason for change
- Testing notes"

# Push to remote
git push origin master
```

### Step 7: Notify Team

After pushing, the deployment team will handle deploying your changes. No further action needed from you.

---

## Troubleshooting Common Issues

### Issue 1: JSON Parsing Failures

**Symptoms:**
- Backend logs show JSON parsing errors
- _extract_json() returns None
- Fallback responses are being used

**Solutions:**
- Add explicit JSON markers in prompt: \`\`\`json ... \`\`\`
- Clarify required vs optional fields
- Add example JSON structure in prompt
- Test with complex nested structures

**Example Fix:**
```python
# Before
prompt = f"Return a list of words as JSON"

# After
prompt = f"""Return a list of words in this exact JSON format:

```json
["word1", "word2", "word3"]
```

Do not include any text outside the JSON array."""
```

---

### Issue 2: Wrong Language in Output

**Symptoms:**
- Italian translations are in German or English
- German explanations are in Italian or English
- Mixed languages in single response

**Solutions:**
- Be explicit about language requirements in EACH section
- Use clear labels: "auf Deutsch", "auf Italienisch", "in italiano", "in German"
- Add language requirement to field descriptions

**Example Fix:**
```python
# Before
"explanation": "Erklärung"

# After
"explanation_de": "Erklärung AUF DEUTSCH (nicht Italienisch)"
```

---

### Issue 3: Difficulty Not Appropriate

**Symptoms:**
- B2 users getting A1-level content
- C1 users finding exercises too easy
- Vocabulary is too simple/complex

**Solutions:**
- Add explicit difficulty calibration
- Reference the CEFR level multiple times in prompt
- Give examples of appropriate vs inappropriate complexity
- Add filtering instructions

**Example Fix:**
```python
# Before
prompt = f"Create exercises for level {level}"

# After
prompt = f"""Create exercises for CEFR level {level}.

Level {level} learners should know:
- [list expected knowledge]

Level {level} learners are learning:
- [list current learning goals]

Examples should challenge {level} learners without being frustrating."""
```

---

### Issue 4: Irrelevant Context

**Symptoms:**
- Business context exercises use daily vocabulary
- Daily context uses overly formal language
- Finance-specific scenarios missing

**Solutions:**
- Add explicit context requirements with examples
- List specific vocabulary domains
- Describe typical situations for each context

**Example Fix:**
```python
# Before
prompt = f"Use vocabulary from {context} context"

# After
prompt = f"""Use vocabulary from {context} context.

For business/finance context, include words related to:
- Payments (die Zahlung, überweisen, die Rechnung)
- Invoicing (die Rechnung, die Faktura, abrechnen)
- Contracts (der Vertrag, unterzeichnen, vereinbaren)
- Negotiations (verhandeln, das Angebot, die Bedingungen)

Use formal register appropriate for business communication."""
```

---

## Monitoring and Iteration

### Metrics to Watch

When your prompt changes are deployed, monitor:

1. **JSON Parsing Success Rate**
   - Are responses being parsed correctly?
   - Check backend logs for parsing errors

2. **User Feedback**
   - Are users reporting better/worse quality?
   - Is difficulty appropriate?
   - Are examples relevant?

3. **Exercise Completion Rates**
   - Are users completing exercises?
   - Are they getting stuck on certain types?

4. **Error Rates**
   - Are users making more/fewer errors?
   - Are they learning effectively?

### Iterative Improvement

Prompt engineering is iterative:
1. Make small, focused changes
2. Deploy and observe
3. Gather feedback
4. Adjust and repeat

Don't try to perfect a prompt in one iteration. Small, incremental improvements are more effective.

---

## Examples of Good Prompt Changes

### Example 1: Adding Business Context Specificity

**Issue:** Business context exercises were using generic business vocabulary, not specific to payments/finance.

**Change:**
```python
# Added to grammar_ai_service.py, generate_exercises()
# Line 65, after "**Kontext:** {context_category}"

# Added:
prompt = f"""...
**Kontext:** {context_category}

{"**Spezielle Anforderungen für Business-Kontext:** Verwende Vokabular aus Zahlungs- und Finanzbereich (Rechnung, Überweisung, Vertrag, Zahlung, Konto, etc.)" if context_category == "business" else ""}

..."""
```

**Result:** Exercises now include finance-specific vocabulary when context is "business".

---

### Example 2: Improving Grammar Error Explanations

**Issue:** Grammar error explanations were too technical for B2 learners.

**Change:**
```python
# Modified in ai_service.py, analyze_grammar()
# Line 122, system prompt modification

# Before:
"explanation": "brief explanation in Italian"

# After:
"explanation": "clear, simple explanation in Italian using everyday language (avoid technical grammar terminology)"
```

**Result:** Explanations became more accessible to learners.

---

### Example 3: Better Vocabulary Detection

**Issue:** Vocabulary detection was including too many common words.

**Change:**
```python
# Modified in ai_service.py, detect_vocabulary()
# Lines 218-222, "Skip" section

# Before:
Skip:
- Very common words (articles, pronouns, basic verbs like 'sein', 'haben')

# After:
Skip:
- Very common words (articles: der/die/das, pronouns: ich/du/er)
- A1-A2 basic verbs (sein, haben, werden, machen, gehen, kommen)
- Function words (und, aber, oder, wenn, weil, dass)
- Numbers and days of week
```

**Result:** Only valuable vocabulary now gets tracked.

---

## Quick Reference

### File Locations
```
Conversation Prompts: /backend/app/services/ai_service.py
Grammar Prompts:      /backend/app/services/grammar_ai_service.py
Vocabulary Prompts:   /backend/app/services/vocabulary_ai_service.py
```

### Language Requirements
```
Italian (user's native language):
- translation_it (word translations)
- it (example translations)
- explanation in "analyze_grammar" (grammar error explanations)

German (learning language):
- definition_de (word definitions)
- explanation_de (exercise feedback)
- feedback_de (answer evaluation)
- de (example sentences)
- All teaching content and exercise explanations
```

### User Profile
```
Name: Igor
Native Language: Italian
Other Languages: English (fluent), German (B2-C1)
Domain: Payments/Finance sector, Switzerland
Focus: Business German + Grammar mastery + Conversational fluency
```

### Common Context Categories
```
business - Meetings, emails, negotiations, payments, finance
daily - Shopping, conversations, travel, leisure
finance - Banking, payments, invoicing, contracts (subset of business)
technical - Specialized terminology
general - Generic scenarios
```

### CEFR Levels
```
A1 - Beginner
A2 - Elementary
B1 - Intermediate
B2 - Upper Intermediate (Igor's current level)
C1 - Advanced (Igor's target level)
C2 - Mastery
```

---

## Contact and Support

**For Prompt-Related Questions:**
- Review this documentation first
- Check existing prompts in the three service files
- Test your changes locally if possible
- Document all changes in git commits

**For Technical Issues (NOT prompt-related):**
- Contact the backend development team
- You should NOT modify code outside of prompts

**For Deployment:**
- Push your changes to master branch
- Deployment is handled automatically
- No action needed from you

---

## Appendix: Complete Prompt Locations

### ai_service.py (3 prompts)
1. **generate_response()** - Line 55-70 - Conversation generation
2. **analyze_grammar()** - Line 122-143 - Grammar analysis
3. **detect_vocabulary()** - Line 194-223 - Vocabulary detection

### grammar_ai_service.py (4 prompts)
1. **generate_exercises()** - Line 56-91 - Exercise generation
2. **evaluate_answer()** - Line 186-211 - Answer evaluation
3. **generate_diagnostic_test()** - Line 273-304 - Diagnostic tests
4. **explain_grammar_error()** - Line 350-367 - Error explanations

### vocabulary_ai_service.py (5 prompts)
1. **analyze_word()** - Line 42-82 - Word analysis
2. **detect_vocabulary_from_text()** - Line 156-185 - Vocabulary detection
3. **generate_vocabulary_quiz()** - Line 331-359 - Quiz generation
4. **get_word_context_examples()** - Line 401-420 - Context examples
5. **suggest_similar_words()** - Line 289-295 - Similar words

**Total: 12 AI prompts across 3 service files**

---

*Last Updated: 2026-01-19*
*Version: 1.0*
*Project: myGermanAITeacher (German Learning Application)*
