"""
Grammar Topic Generator

Generate specifications for NEW grammar topics using AI.
Uses GrammarAIService to analyze topics and generate metadata.
"""

import json
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class GrammarTopicGenerator:
    """Generate new grammar topic specifications using AI"""

    def __init__(self, grammar_ai_service):
        """
        Initialize generator

        Args:
            grammar_ai_service: Instance of GrammarAIService
        """
        self.ai_service = grammar_ai_service
        logger.info("Initialized GrammarTopicGenerator")

    def generate_topic_metadata(self, topic_name: str) -> Dict:
        """
        Use AI to generate full topic metadata

        Args:
            topic_name: Topic name (e.g., "subjunctive", "passive_voice")

        Returns:
            {
                "name_de": "Konjunktiv II",
                "name_en": "Subjunctive II",
                "category": "verbs",
                "subcategory": "moods",
                "difficulty_level": "B2",
                "description_de": "Short description",
                "explanation_de": "Full German explanation (500+ words)",
                "order_index": 51,
                "parent_topic_id": None
            }
        """
        try:
            logger.info(f"Generating metadata for topic: {topic_name}")

            # Create prompt for topic metadata generation
            prompt = self._build_topic_metadata_prompt(topic_name)

            # Call AI service
            response = self.ai_service._call_ai(
                prompt=prompt,
                max_tokens=2000
            )

            # Parse response
            metadata = self._parse_topic_metadata(response, topic_name)

            logger.info(f"✅ Generated metadata for topic: {metadata.get('name_en', topic_name)}")
            return metadata

        except Exception as e:
            logger.error(f"Failed to generate topic metadata: {e}")
            # Return fallback metadata
            return self._fallback_metadata(topic_name)

    def create_topic_with_exercises(self, topic_metadata: Dict, exercise_count: int = 20) -> Dict:
        """
        Create topic AND generate initial exercises

        Args:
            topic_metadata: Topic metadata dictionary
            exercise_count: Number of initial exercises to generate

        Returns:
            {
                "topic": topic_data,
                "exercises": [exercise1, exercise2, ...]
            }
        """
        try:
            logger.info(f"Creating topic with {exercise_count} exercises: {topic_metadata.get('name_en')}")

            # Generate exercises using existing AI service
            exercises = []

            # Generate exercises of different types
            types_to_generate = ['fill_blank', 'multiple_choice', 'translation', 'error_correction']
            exercises_per_type = max(1, exercise_count // len(types_to_generate))

            for exercise_type in types_to_generate:
                logger.info(f"Generating {exercises_per_type} {exercise_type} exercises...")

                batch = self.ai_service.generate_exercises(
                    topic_name=topic_metadata.get('name_de', topic_metadata.get('name_en')),
                    topic_explanation=topic_metadata.get('explanation_de', ''),
                    difficulty_level=topic_metadata.get('difficulty_level', 'B1'),
                    exercise_type=exercise_type,
                    count=exercises_per_type
                )

                exercises.extend(batch)

            logger.info(f"✅ Generated {len(exercises)} exercises for new topic")

            return {
                'topic': topic_metadata,
                'exercises': exercises[:exercise_count]  # Trim to exact count
            }

        except Exception as e:
            logger.error(f"Failed to create topic with exercises: {e}")
            return {
                'topic': topic_metadata,
                'exercises': []
            }

    def _build_topic_metadata_prompt(self, topic_name: str) -> str:
        """Build prompt for topic metadata generation"""
        return f"""You are a German grammar expert. Generate comprehensive metadata for the following grammar topic:

Topic: {topic_name.replace('_', ' ').title()}

Please provide the following information in JSON format:

{{
    "name_de": "German name of the topic",
    "name_en": "English name of the topic",
    "category": "one of: cases, verbs, tenses, pronouns, adjectives, articles, prepositions, conjunctions, sentence_structure, other",
    "subcategory": "specific subcategory (e.g., 'moods', 'word_order', 'agreement')",
    "difficulty_level": "CEFR level (A1, A2, B1, B2, C1, or C2)",
    "description_de": "Brief 2-3 sentence description in German",
    "explanation_de": "Comprehensive German explanation (500-800 words) covering rules, examples, and common mistakes"
}}

Requirements:
- name_de and name_en should be clear and specific
- category must be one of the listed options
- difficulty_level should reflect the complexity of the topic
- explanation_de should be detailed, include examples, and be written in clear German
- Use proper German grammar and orthography

Return ONLY valid JSON, no additional text."""

    def _parse_topic_metadata(self, ai_response: str, topic_name: str) -> Dict:
        """Parse AI response into topic metadata"""
        try:
            # Extract JSON from response
            json_start = ai_response.find('{')
            json_end = ai_response.rfind('}') + 1

            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")

            json_str = ai_response[json_start:json_end]
            metadata = json.loads(json_str)

            # Add computed fields
            metadata['order_index'] = 999  # Will be updated when inserted
            metadata['parent_topic_id'] = None

            # Validate required fields
            required_fields = ['name_de', 'name_en', 'category', 'difficulty_level', 'explanation_de']
            missing_fields = [field for field in required_fields if not metadata.get(field)]

            if missing_fields:
                logger.warning(f"Missing fields in metadata: {missing_fields}")
                # Fill in defaults
                for field in missing_fields:
                    metadata[field] = self._get_default_value(field, topic_name)

            return metadata

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from AI response: {e}")
            logger.debug(f"AI response: {ai_response}")
            return self._fallback_metadata(topic_name)

        except Exception as e:
            logger.error(f"Error parsing topic metadata: {e}")
            return self._fallback_metadata(topic_name)

    def _fallback_metadata(self, topic_name: str) -> Dict:
        """Generate fallback metadata when AI fails"""
        return {
            'name_de': topic_name.replace('_', ' ').title(),
            'name_en': topic_name.replace('_', ' ').title(),
            'category': 'other',
            'subcategory': 'general',
            'difficulty_level': 'B1',
            'description_de': f"Übungen zu {topic_name.replace('_', ' ')}",
            'explanation_de': f"Dies ist ein Thema der deutschen Grammatik: {topic_name.replace('_', ' ')}. "
                            "Bitte beachten Sie die spezifischen Regeln und Beispiele für dieses Thema.",
            'order_index': 999,
            'parent_topic_id': None
        }

    def _get_default_value(self, field: str, topic_name: str) -> str:
        """Get default value for missing field"""
        defaults = {
            'name_de': topic_name.replace('_', ' ').title(),
            'name_en': topic_name.replace('_', ' ').title(),
            'category': 'other',
            'subcategory': 'general',
            'difficulty_level': 'B1',
            'description_de': f"Übungen zu {topic_name.replace('_', ' ')}",
            'explanation_de': f"Grammatikthema: {topic_name.replace('_', ' ')}"
        }
        return defaults.get(field, '')


if __name__ == "__main__":
    # Test topic generator (requires AI service)
    logging.basicConfig(level=logging.INFO)

    import sys
    import os

    # Add backend to path
    backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    sys.path.insert(0, backend_dir)

    from app.services.grammar_ai_service import GrammarAIService

    # Create AI service
    ai_service = GrammarAIService()

    # Create generator
    generator = GrammarTopicGenerator(ai_service)

    # Test topic metadata generation
    test_topic = "subjunctive"
    print(f"Generating metadata for: {test_topic}")
    print("=" * 60)

    metadata = generator.generate_topic_metadata(test_topic)

    print(json.dumps(metadata, indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    print(f"✅ Topic: {metadata.get('name_en')} ({metadata.get('difficulty_level')})")
    print(f"   Category: {metadata.get('category')} / {metadata.get('subcategory')}")
    print(f"   Description: {metadata.get('description_de', '')[:100]}...")
