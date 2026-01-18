"""
AI service for conversation generation, grammar analysis, and vocabulary detection.
Uses Anthropic Claude API for natural language processing.
"""
import logging
from typing import List, Dict, Optional
import json
from anthropic import Anthropic, APIError
import time

from app.config import settings

logger = logging.getLogger(__name__)


class ConversationAI:
    """
    AI service wrapper for Anthropic Claude.
    Handles conversation generation, grammar analysis, and vocabulary detection.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI service.

        Args:
            api_key: Anthropic API key (defaults to settings.ANTHROPIC_API_KEY)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.model = settings.AI_MODEL  # Configurable AI model from environment

    def generate_response(
        self,
        context_prompt: str,
        conversation_history: List[Dict[str, str]],
        user_message: str,
        user_level: str = "B2"
    ) -> str:
        """
        Generate AI response in conversation.

        Args:
            context_prompt: System prompt defining the conversation context
            conversation_history: List of previous messages [{"role": "user|assistant", "content": "text"}]
            user_message: Current user message
            user_level: User's German proficiency level (A1-C2)

        Returns:
            str: AI's response in German

        Raises:
            AIServiceError: If API call fails after retries
        """
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

        try:
            # Build messages list
            messages = conversation_history + [
                {"role": "user", "content": user_message}
            ]

            # Call Claude API
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=system_prompt,
                messages=messages
            )

            return response.content[0].text

        except APIError as e:
            logger.error(f"Anthropic API error: {e}")
            raise AIServiceError(f"Failed to generate response: {str(e)}")

    def analyze_grammar(
        self,
        user_message: str,
        user_level: str = "B2",
        context_name: str = "general"
    ) -> List[Dict]:
        """
        Analyze user's message for grammar errors.

        Args:
            user_message: The user's German text to analyze
            user_level: User's proficiency level
            context_name: Conversation context name

        Returns:
            List[Dict]: List of grammar errors with corrections and explanations

        Example return:
            [
                {
                    "error_type": "case",
                    "incorrect_text": "der Mann",
                    "corrected_text": "den Mann",
                    "explanation": "Il verbo 'sehen' richiede l'accusativo.",
                    "severity": "moderate",
                    "rule": "Akkusativ nach 'sehen'",
                    "grammar_topic_hint": "accusative_case"
                }
            ]
        """
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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": analysis_prompt}]
            )

            # Parse JSON response
            content = response.content[0].text
            errors = self._extract_json(content)
            return errors if errors is not None else []

        except APIError as e:
            logger.error(f"Grammar analysis API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing grammar analysis: {e}")
            return []

    def detect_vocabulary(
        self,
        text: str,
        user_level: str = "B2",
        context_name: str = "general"
    ) -> List[Dict]:
        """
        Extract key vocabulary from German text.

        Args:
            text: German text to analyze
            user_level: User's proficiency level
            context_name: Conversation context

        Returns:
            List[Dict]: List of vocabulary items detected

        Example return:
            [
                {
                    "word": "die Zahlung",
                    "lemma": "Zahlung",
                    "part_of_speech": "noun",
                    "difficulty": "B2",
                    "context_category": "business",
                    "is_idiom": false,
                    "is_compound": false
                }
            ]
        """
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

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                messages=[{"role": "user", "content": vocab_prompt}]
            )

            content = response.content[0].text
            vocabulary = self._extract_json(content)
            return vocabulary if vocabulary is not None else []

        except APIError as e:
            logger.error(f"Vocabulary detection API error: {e}")
            return []
        except Exception as e:
            logger.error(f"Error parsing vocabulary: {e}")
            return []

    def _extract_json(self, content: str) -> Optional[List[Dict]]:
        """
        Extract JSON from AI response text.

        Args:
            content: Response text that may contain JSON

        Returns:
            Optional[List[Dict]]: Parsed JSON or None if parsing fails
        """
        try:
            # Try to parse directly
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code block or text
            start = content.find('[')
            end = content.rfind(']') + 1
            if start != -1 and end != 0:
                try:
                    return json.loads(content[start:end])
                except json.JSONDecodeError:
                    pass
            return None

    def generate_response_with_retry(
        self,
        *args,
        max_retries: int = 3,
        **kwargs
    ) -> str:
        """
        Generate response with retry logic for transient failures.

        Args:
            max_retries: Maximum number of retry attempts
            *args, **kwargs: Arguments to pass to generate_response

        Returns:
            str: AI response

        Raises:
            AIServiceError: If all retries fail
        """
        for attempt in range(max_retries):
            try:
                return self.generate_response(*args, **kwargs)
            except APIError as e:
                logger.error(f"API error on attempt {attempt + 1}: {e}")

                if attempt == max_retries - 1:
                    # Last attempt failed, return fallback
                    return self._fallback_response()

                # Exponential backoff
                time.sleep(2 ** attempt)

        return self._fallback_response()

    def _fallback_response(self) -> str:
        """
        Simple fallback response when AI is unavailable.

        Returns:
            str: Fallback message in German
        """
        return "Entschuldigung, ich habe gerade technische Probleme. Können Sie das bitte wiederholen?"


class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass
