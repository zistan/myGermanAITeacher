"""
Vocabulary AI Service - analyzes words, generates definitions, and provides context.
This service extends the conversation AI to focus on vocabulary learning.
"""
from typing import List, Dict, Optional
import json
import re
from anthropic import Anthropic, APIError

from app.config import settings


class VocabularyAIService:
    """Service for AI-powered vocabulary analysis and learning."""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Vocabulary AI service.

        Args:
            api_key: Anthropic API key (uses config if not provided)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-5"  # Latest Claude Sonnet 4.5 (auto-updates)

    def analyze_word(
        self,
        word: str,
        user_level: str = "B2",
        include_examples: bool = True
    ) -> Dict:
        """Analyze a German word and provide comprehensive information.

        Args:
            word: German word to analyze
            user_level: User's CEFR level
            include_examples: Include example sentences

        Returns:
            Dictionary with word analysis (translation, grammar, usage, etc.)
        """
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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            analysis = self._extract_json(response.content[0].text)
            if analysis and isinstance(analysis, dict):
                return analysis
            else:
                # Fallback
                return {
                    "word": word,
                    "translation_it": "Traduzione non disponibile",
                    "part_of_speech": "unknown",
                    "difficulty_level": user_level,
                    "definition_de": f"Wort: {word}",
                    "examples": []
                }

        except APIError as e:
            print(f"Error analyzing word: {e}")
            return {
                "word": word,
                "error": "Analysis failed",
                "translation_it": "Errore",
                "examples": []
            }

    def detect_vocabulary_from_text(
        self,
        text: str,
        user_level: str = "B2",
        min_difficulty: str = "B1"
    ) -> List[Dict]:
        """Detect important vocabulary words from a German text.

        Args:
            text: German text to analyze
            user_level: User's current level
            min_difficulty: Minimum difficulty to include

        Returns:
            List of vocabulary words with basic info
        """
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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.5,
                messages=[{"role": "user", "content": prompt}]
            )

            vocab_list = self._extract_json(response.content[0].text)
            if vocab_list and isinstance(vocab_list, list):
                return vocab_list
            else:
                return []

        except APIError as e:
            print(f"Error detecting vocabulary: {e}")
            return []

    def generate_flashcard_content(
        self,
        word: str,
        word_info: Dict,
        card_type: str = "definition"
    ) -> Dict:
        """Generate flashcard content for a vocabulary word.

        Args:
            word: The vocabulary word
            word_info: Word information from database
            card_type: Type of flashcard (definition, translation, usage, listening)

        Returns:
            Dictionary with front and back of flashcard
        """
        # Different card types for varied practice
        prompts = {
            "definition": f"Was bedeutet '{word}'? Erkläre auf Deutsch.",
            "translation": f"Wie übersetzt man '{word}' auf Italienisch?",
            "usage": f"Vervollständige den Satz mit '{word}'.",
            "synonym": f"Nenne ein Synonym für '{word}'.",
            "example": f"Bilde einen Beispielsatz mit '{word}'."
        }

        if card_type == "definition":
            return {
                "front": f"Was bedeutet:\n\n**{word}**",
                "back": word_info.get("definition_de", "Definition nicht verfügbar"),
                "hint": word_info.get("usage_notes", "")
            }
        elif card_type == "translation":
            return {
                "front": f"Übersetze ins Italienische:\n\n**{word}**",
                "back": word_info.get("translation_it", "Traduzione non disponibile"),
                "hint": f"({word_info.get('part_of_speech', 'word')})"
            }
        elif card_type == "usage":
            examples = word_info.get("examples", [])
            if examples:
                example = examples[0]["de"]
                # Blank out the word
                blanked = example.replace(word, "____")
                return {
                    "front": f"Vervollständige:\n\n{blanked}",
                    "back": example,
                    "hint": f"Verwende: {word}"
                }
            else:
                return {
                    "front": f"Bilde einen Satz mit:\n\n**{word}**",
                    "back": "Beispiel nicht verfügbar",
                    "hint": ""
                }
        else:
            return {
                "front": word,
                "back": word_info.get("translation_it", "Traduzione"),
                "hint": ""
            }

    def suggest_similar_words(
        self,
        word: str,
        category: str = "synonym",
        count: int = 5
    ) -> List[str]:
        """Suggest similar words for vocabulary building.

        Args:
            word: Base word
            category: Type of similarity (synonym, antonym, related, same_family)
            count: Number of suggestions

        Returns:
            List of similar words
        """
        category_prompts = {
            "synonym": "Synonyme",
            "antonym": "Antonyme",
            "related": "verwandte Wörter",
            "same_family": "Wörter aus derselben Wortfamilie"
        }

        prompt = f"""Nenne {count} {category_prompts.get(category, 'verwandte Wörter')} für das deutsche Wort: {word}

Gib nur eine JSON-Liste mit den Wörtern zurück (mit Artikeln für Nomen):

```json
["Wort1", "Wort2", "Wort3"]
```"""

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            words = self._extract_json(response.content[0].text)
            if words and isinstance(words, list):
                return words[:count]
            else:
                return []

        except APIError as e:
            print(f"Error suggesting similar words: {e}")
            return []

    def generate_vocabulary_quiz(
        self,
        words: List[str],
        quiz_type: str = "multiple_choice",
        difficulty: str = "B2"
    ) -> List[Dict]:
        """Generate a vocabulary quiz from a list of words.

        Args:
            words: List of German words to quiz on
            quiz_type: Type of quiz (multiple_choice, fill_blank, matching)
            difficulty: Difficulty level

        Returns:
            List of quiz questions
        """
        words_str = ", ".join(words)

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=3000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            quiz = self._extract_json(response.content[0].text)
            if quiz and isinstance(quiz, list):
                return quiz
            else:
                return []

        except APIError as e:
            print(f"Error generating quiz: {e}")
            return []

    def get_word_context_examples(
        self,
        word: str,
        context_category: str = "daily",
        count: int = 3
    ) -> List[Dict]:
        """Get context-specific example sentences for a word.

        Args:
            word: German word
            context_category: Context (business, daily, academic)
            count: Number of examples

        Returns:
            List of example sentences with translations
        """
        context_desc = {
            "business": "geschäftlicher Kontext (Meetings, E-Mails, Verhandlungen)",
            "daily": "alltäglicher Kontext (Gespräche, Einkaufen, Freizeit)",
            "academic": "akademischer Kontext (Studium, Forschung, Vorträge)"
        }

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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            examples = self._extract_json(response.content[0].text)
            if examples and isinstance(examples, list):
                return examples
            else:
                return []

        except APIError as e:
            print(f"Error generating examples: {e}")
            return []

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
