#!/usr/bin/env python3
"""
AI-assisted vocabulary generator using Claude API.

This script generates premium-quality German vocabulary entries using
Claude AI, with automatic validation and export to seed file format.

Usage:
    python ai_generator.py --category finance --subcategory "payment methods" --count 50
    python ai_generator.py --category business --subcategory "meetings" --count 100
    python ai_generator.py --batch-file batches.json
"""

import os
import sys
import json
import argparse
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))

try:
    from anthropic import Anthropic
except ImportError:
    print("ERROR: anthropic package not installed")
    print("Run: pip install anthropic")
    sys.exit(1)

from core.data_format import VocabularyWord, CEFR_LEVELS, VALID_CATEGORIES
from core.validation import VocabularyValidator


class VocabularyGenerator:
    """AI-assisted vocabulary generator using Claude."""

    def __init__(self, api_key: Optional[str] = None, verbose: bool = False):
        """
        Initialize generator.

        Args:
            api_key: Anthropic API key (defaults to ANTHROPIC_API_KEY env var)
            verbose: If True, print detailed progress
        """
        self.verbose = verbose

        # Get API key from parameter or environment
        api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError(
                "No API key provided. Set ANTHROPIC_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = Anthropic(api_key=api_key)
        self.validator = VocabularyValidator(verbose=verbose)

    def generate_vocabulary(
        self,
        category: str,
        subcategory: str,
        count: int,
        difficulty: str = "mixed",
        context: str = ""
    ) -> List[VocabularyWord]:
        """
        Generate vocabulary words for a specific category/subcategory.

        Args:
            category: Main category (finance, business, etc.)
            subcategory: Subcategory description (e.g., "payment methods", "meetings")
            count: Number of words to generate
            difficulty: CEFR level or "mixed" (default: mixed)
            context: Additional context for generation

        Returns:
            List of validated VocabularyWord dictionaries
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Generating {count} words for: {category} / {subcategory}")
            print(f"Difficulty: {difficulty}")
            print(f"{'='*60}\n")

        # Build AI prompt
        prompt = self._build_generation_prompt(
            category, subcategory, count, difficulty, context
        )

        # Call Claude API
        if self.verbose:
            print("Calling Claude API...")

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-5-20250929",  # Latest Claude Sonnet
                max_tokens=16000,
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract response
            response_text = response.content[0].text

            if self.verbose:
                print(f"✓ Received response ({len(response_text)} chars)")

        except Exception as e:
            print(f"✗ Error calling Claude API: {str(e)}")
            return []

        # Parse JSON response
        words = self._parse_response(response_text)

        if self.verbose:
            print(f"✓ Parsed {len(words)} words from response")

        # Validate words
        validation_result = self.validator.validate_words(words)

        if not validation_result.is_valid():
            print(f"\n⚠ Validation found {len(validation_result.errors)} errors:")
            for error in validation_result.errors[:10]:
                print(f"  - {error}")
            if len(validation_result.errors) > 10:
                print(f"  ... and {len(validation_result.errors) - 10} more")

        if self.verbose:
            print(f"✓ Validation complete: {validation_result.valid_count} valid, "
                  f"{validation_result.invalid_count} invalid")

        # Return only valid words
        valid_words = [
            word for i, word in enumerate(words)
            if i < validation_result.valid_count
        ]

        return valid_words

    def _build_generation_prompt(
        self,
        category: str,
        subcategory: str,
        count: int,
        difficulty: str,
        context: str
    ) -> str:
        """Build the AI prompt for vocabulary generation."""

        difficulty_guidance = ""
        if difficulty != "mixed":
            difficulty_guidance = f"All words should be CEFR level {difficulty}."
        else:
            difficulty_guidance = (
                "Mix of CEFR levels: 10% A1-A2, 40% B1-B2, 50% C1-C2 "
                "(focus on advanced business vocabulary)."
            )

        prompt = f"""Generate {count} German vocabulary words for a German learning application.

**Category**: {category}
**Subcategory**: {subcategory}
{f"**Context**: {context}" if context else ""}

**Quality Requirements** (PREMIUM TIER):
- All 14 fields must be populated for each word
- Accurate German-Italian translations
- Authentic example sentences (real-world usage)
- Detailed usage notes with context, register, collocations
- Pronunciation in simplified phonetic format
- German definition (1-2 sentences)
- Synonyms and antonyms (JSON array format)

**CEFR Level Distribution**:
{difficulty_guidance}

**Target User**: Italian native speaker, fluent in English, working in payments/finance in Switzerland, learning business German (B2/C1 level).

**Output Format** (JSON array):
```json
[
  {{
    "word": "die Überweisung",
    "translation_it": "il bonifico",
    "part_of_speech": "noun",
    "gender": "feminine",
    "plural_form": "die Überweisungen",
    "difficulty": "B2",
    "category": "{category}",
    "example_de": "Die Überweisung dauert 1-2 Werktage.",
    "example_it": "Il bonifico richiede 1-2 giorni lavorativi.",
    "pronunciation": "dee ü-ber-VAI-zung",
    "definition_de": "Zahlungsvorgang zur Übertragung von Geld von einem Konto auf ein anderes",
    "usage_notes": "Standard bank transfer. Most common payment method in Germany. SEPA transfers within EU typically take 1 business day.",
    "synonyms": "[\\"die Banküberweisung\\", \\"der Transfer\\"]",
    "antonyms": "[\\"die Lastschrift\\"]",
    "is_idiom": 0,
    "is_compound": 1,
    "is_separable_verb": 0
  }}
]
```

**CRITICAL REQUIREMENTS**:
1. **Articles for Nouns**: Always include der/die/das with nouns
2. **Gender**: Must match article (masculine/feminine/neuter)
3. **Plural Forms**: Provide for all nouns
4. **Boolean Fields**: Use 0 or 1 (not true/false)
5. **JSON Arrays**: Synonyms/antonyms as JSON strings: "[\\"word1\\", \\"word2\\"]"
6. **Pronunciation**: Simplified phonetic (not IPA): "dee ü-ber-VAI-zung"
7. **Usage Notes**: Real-world context, not just definitions. Include:
   - When/where it's used
   - Common collocations
   - Register (formal/informal)
   - Related terms or concepts
   - Any regional variations (Germany/Austria/Switzerland)

**Examples of Premium Quality**:
- Technical terms: Include English equivalents if commonly used
- Compound words: Set is_compound to 1
- Separable verbs: Set is_separable_verb to 1
- Idioms: Set is_idiom to 1, explain literal vs. figurative meaning

Generate exactly {count} words. Return ONLY the JSON array, no additional text."""

        return prompt

    def _parse_response(self, response_text: str) -> List[VocabularyWord]:
        """
        Parse Claude API response into VocabularyWord list.

        Args:
            response_text: Raw response from Claude

        Returns:
            List of VocabularyWord dictionaries
        """
        # Extract JSON array from response
        # Claude sometimes wraps JSON in markdown code blocks
        json_text = response_text.strip()

        # Remove markdown code blocks if present
        if json_text.startswith("```json"):
            json_text = json_text[7:]
        if json_text.startswith("```"):
            json_text = json_text[3:]
        if json_text.endswith("```"):
            json_text = json_text[:-3]

        json_text = json_text.strip()

        try:
            words = json.loads(json_text)

            if not isinstance(words, list):
                print(f"✗ Error: Expected JSON array, got {type(words)}")
                return []

            return words

        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {str(e)}")
            print(f"Response preview: {response_text[:500]}...")
            return []

    def save_to_file(
        self,
        words: List[VocabularyWord],
        filename: str,
        format: str = "python"
    ):
        """
        Save vocabulary words to a file.

        Args:
            words: List of vocabulary words
            filename: Output filename
            format: Output format - "python" or "json"
        """
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)

        if format == "json":
            # Save as JSON
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(words, f, indent=2, ensure_ascii=False)

            if self.verbose:
                print(f"✓ Saved {len(words)} words to {filename} (JSON)")

        elif format == "python":
            # Save as Python code for seed module
            with open(filename, "w", encoding="utf-8") as f:
                f.write('"""Generated vocabulary words."""\n\n')
                f.write('from typing import List\n')
                f.write('from ..core.data_format import VocabularyWord\n\n\n')
                f.write('def get_vocabulary_words() -> List[VocabularyWord]:\n')
                f.write('    """Get generated vocabulary words."""\n')
                f.write('    words = ')

                # Write words as Python list
                f.write(json.dumps(words, indent=4, ensure_ascii=False))

                f.write('\n\n    return words\n')

            if self.verbose:
                print(f"✓ Saved {len(words)} words to {filename} (Python)")


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AI-assisted vocabulary generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --category finance --subcategory "payment methods" --count 80
  %(prog)s --category business --subcategory "meetings and presentations" --count 100 --difficulty B2
  %(prog)s --category finance --subcategory "blockchain" --count 50 --output blockchain.json
        """
    )

    # Generation parameters
    parser.add_argument(
        "--category",
        required=True,
        choices=VALID_CATEGORIES,
        help="Main category"
    )

    parser.add_argument(
        "--subcategory",
        required=True,
        help="Subcategory description (e.g., 'payment methods', 'meetings')"
    )

    parser.add_argument(
        "--count",
        type=int,
        default=50,
        help="Number of words to generate (default: 50)"
    )

    parser.add_argument(
        "--difficulty",
        default="mixed",
        help="CEFR level or 'mixed' (default: mixed)"
    )

    parser.add_argument(
        "--context",
        default="",
        help="Additional context for generation"
    )

    # Output options
    parser.add_argument(
        "--output",
        "-o",
        help="Output filename (default: auto-generated)"
    )

    parser.add_argument(
        "--format",
        choices=["json", "python"],
        default="python",
        help="Output format (default: python)"
    )

    # Options
    parser.add_argument(
        "--api-key",
        help="Anthropic API key (default: ANTHROPIC_API_KEY env var)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print detailed progress"
    )

    args = parser.parse_args()

    # Initialize generator
    try:
        generator = VocabularyGenerator(
            api_key=args.api_key,
            verbose=args.verbose
        )
    except ValueError as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)

    # Generate vocabulary
    words = generator.generate_vocabulary(
        category=args.category,
        subcategory=args.subcategory,
        count=args.count,
        difficulty=args.difficulty,
        context=args.context
    )

    if not words:
        print("✗ No valid words generated")
        sys.exit(1)

    # Determine output filename
    if args.output:
        output_filename = args.output
    else:
        # Auto-generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_subcategory = args.subcategory.replace(" ", "_").replace("/", "_")
        ext = "json" if args.format == "json" else "py"
        output_filename = f"generated_{args.category}_{safe_subcategory}_{timestamp}.{ext}"

    # Save to file
    generator.save_to_file(words, output_filename, format=args.format)

    print(f"\n{'='*60}")
    print(f"✓ SUCCESS")
    print(f"{'='*60}")
    print(f"Generated: {len(words)} words")
    print(f"Category: {args.category} / {args.subcategory}")
    print(f"Output: {output_filename}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
