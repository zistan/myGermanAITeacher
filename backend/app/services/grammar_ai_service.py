"""
Grammar AI Service - generates exercises and provides feedback using Claude AI.
This service extends the conversation AI to focus on grammar learning.
"""
from typing import List, Dict, Optional
import json
import re
from anthropic import Anthropic, APIError

from app.config import settings


class GrammarAIService:
    """Service for AI-powered grammar exercise generation and feedback."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Grammar AI service.

        Args:
            api_key: Anthropic API key (uses config if not provided)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def generate_exercises(
        self,
        topic_name: str,
        topic_explanation: str,
        difficulty_level: str,
        exercise_type: str,
        count: int = 5,
        context_category: str = "general"
    ) -> List[Dict]:
        """Generate grammar exercises for a specific topic using AI.

        Args:
            topic_name: Name of the grammar topic (e.g., "Akkusativ")
            topic_explanation: Full explanation of the topic
            difficulty_level: CEFR level (A1-C2)
            exercise_type: Type of exercise (fill_blank, multiple_choice, etc.)
            count: Number of exercises to generate
            context_category: Context (business, daily, general)

        Returns:
            List of exercise dictionaries with question, answer, explanation, hints
        """
        exercise_type_descriptions = {
            "fill_blank": "Fill-in-the-blank exercises where users complete missing words",
            "multiple_choice": "Multiple choice questions with one correct answer and 3 distractors",
            "translation": "Translation exercises from Italian to German",
            "error_correction": "Sentences with errors that need to be corrected",
            "sentence_building": "Word ordering exercises to build correct sentences"
        }

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = response.content[0].text
            exercises = self._extract_json(response_text)

            if exercises and isinstance(exercises, list):
                # Add difficulty level and context to each exercise
                for exercise in exercises:
                    exercise["difficulty_level"] = difficulty_level
                    exercise["exercise_type"] = exercise_type
                    exercise["context_category"] = context_category
                return exercises
            else:
                # Return empty list if parsing failed
                return []

        except APIError as e:
            print(f"Error generating exercises: {e}")
            return []

    def evaluate_answer(
        self,
        question_text: str,
        user_answer: str,
        correct_answer: str,
        topic_name: str,
        difficulty_level: str
    ) -> Dict:
        """Evaluate a user's answer with detailed feedback.

        Args:
            question_text: The exercise question
            user_answer: User's submitted answer
            correct_answer: The correct answer
            topic_name: Grammar topic being practiced
            difficulty_level: User's level

        Returns:
            Dictionary with is_correct, feedback, and suggestions
        """
        prompt = f"""Du bist ein geduldiger Deutschlehrer für italienischsprachige Lernende (Niveau {difficulty_level}).

**Grammatikthema:** {topic_name}

**Aufgabe:** {question_text}

**Richtige Antwort:** {correct_answer}

**Antwort des Lernenden:** {user_answer}

Bewerte die Antwort des Lernenden und gib Feedback.

**Format:** Antworte als JSON:

```json
{{
  "is_correct": true/false,
  "is_partially_correct": true/false,  // wenn fast richtig (z.B. nur kleine Fehler)
  "feedback_de": "Detailliertes Feedback auf Deutsch (2-4 Sätze)",
  "specific_errors": ["Fehler 1", "Fehler 2"],  // spezifische identifizierte Fehler
  "suggestions": ["Vorschlag 1", "Vorschlag 2"]  // konstruktive Verbesserungsvorschläge
}}
```

**Anforderungen:**
- Sei ermutigend und konstruktiv
- Erkläre WARUM etwas falsch oder richtig ist
- Gib spezifische Hinweise zur Grammatikregel
- Wenn fast richtig, erwähne was gut war
- Wenn komplett falsch, zeige den Unterschied klar auf"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1000,
                temperature=0.3,  # Lower temperature for more consistent evaluation
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = response.content[0].text
            evaluation = self._extract_json(response_text)

            if evaluation and isinstance(evaluation, dict):
                return evaluation
            else:
                # Fallback to simple comparison
                is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
                return {
                    "is_correct": is_correct,
                    "is_partially_correct": False,
                    "feedback_de": "Richtig!" if is_correct else f"Nicht ganz. Die richtige Antwort ist: {correct_answer}",
                    "specific_errors": [] if is_correct else ["Antwort stimmt nicht überein"],
                    "suggestions": [] if is_correct else ["Überprüfe die Grammatikregel noch einmal"]
                }

        except APIError as e:
            print(f"Error evaluating answer: {e}")
            # Fallback evaluation
            is_correct = user_answer.strip().lower() == correct_answer.strip().lower()
            return {
                "is_correct": is_correct,
                "is_partially_correct": False,
                "feedback_de": "Richtig!" if is_correct else f"Die richtige Antwort ist: {correct_answer}",
                "specific_errors": [],
                "suggestions": []
            }

    def generate_diagnostic_test(
        self,
        target_level: str,
        num_questions: int = 20,
        topics: Optional[List[str]] = None
    ) -> List[Dict]:
        """Generate a diagnostic test to assess user's grammar level.

        Args:
            target_level: Target CEFR level to test (A1-C2)
            num_questions: Number of questions (default 20)
            topics: Optional list of topics to include

        Returns:
            List of diagnostic test questions with answers
        """
        topics_str = ", ".join(topics) if topics else "alle wichtigen Grammatikthemen"

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=6000,
                temperature=0.7,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract JSON from response
            response_text = response.content[0].text
            questions = self._extract_json(response_text)

            if questions and isinstance(questions, list):
                return questions
            else:
                return []

        except APIError as e:
            print(f"Error generating diagnostic test: {e}")
            return []

    def explain_grammar_error(
        self,
        user_sentence: str,
        correct_sentence: str,
        topic_name: str,
        user_level: str = "B2"
    ) -> str:
        """Provide detailed explanation of a grammar error.

        Args:
            user_sentence: User's incorrect sentence
            correct_sentence: The correct version
            topic_name: Grammar topic involved
            user_level: User's proficiency level

        Returns:
            Detailed explanation in German
        """
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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=800,
                temperature=0.5,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            explanation = response.content[0].text.strip()
            return explanation

        except APIError as e:
            print(f"Error generating explanation: {e}")
            return f"Der korrekte Satz ist: {correct_sentence}"

    def _extract_json(self, text: str) -> Optional[dict]:
        """Extract JSON from AI response text.

        Args:
            text: Text potentially containing JSON

        Returns:
            Parsed JSON object or None if extraction failed
        """
        # First, try to parse the entire text as JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Try to find JSON in markdown code blocks
        json_pattern = r'```(?:json)?\s*(\{.*?\}|\[.*?\])\s*```'
        matches = re.findall(json_pattern, text, re.DOTALL)

        if matches:
            try:
                return json.loads(matches[0])
            except json.JSONDecodeError:
                pass

        # Try to find JSON without code blocks
        json_pattern = r'(\{.*\}|\[.*\])'
        matches = re.findall(json_pattern, text, re.DOTALL)

        if matches:
            # Try each match, starting with the longest
            sorted_matches = sorted(matches, key=len, reverse=True)
            for match in sorted_matches:
                try:
                    return json.loads(match)
                except json.JSONDecodeError:
                    continue

        return None
