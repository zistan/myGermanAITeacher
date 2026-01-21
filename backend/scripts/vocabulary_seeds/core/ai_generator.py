#!/usr/bin/env python3
"""
AI-assisted vocabulary generator using Claude API.

This script generates premium-quality German vocabulary entries using
Claude AI, with automatic validation and export to seed file format.

Usage:
    python ai_generator.py --category finance --subcategory "payment methods" --count 50
    python ai_generator.py --category business --subcategory "meetings" --count 80
    python ai_generator.py --category finance --subcategory "banking" --count 150 --chunk-size 50

Features:
    - Auto-chunking: Large batches are automatically split into smaller chunks
    - Example: --count 80 will be split into 2 chunks of 40 words each
    - Results are aggregated into a single output file
    - Default chunk size: 40 words (configurable with --chunk-size)
"""

import os
import sys
import json
import re
import argparse
from typing import List, Dict, Optional
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv

# Load .env from backend directory (3 levels up)
env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
load_dotenv(dotenv_path=env_path)

# Add parent directories to path
# Add backend directory (3 levels up)
sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
# Add vocabulary_seeds directory (1 level up) for core imports
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

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

        # Get AI model from environment or use default
        # Matches backend app configuration (backend/app/config.py)
        self.model = os.getenv("AI_MODEL", "claude-sonnet-4-5")

        if self.verbose:
            print(f"Using AI model: {self.model}")

    def generate_vocabulary(
        self,
        category: str,
        subcategory: str,
        count: int,
        difficulty: str = "mixed",
        context: str = "",
        auto_chunk: bool = True,
        chunk_size: int = 40
    ) -> List[VocabularyWord]:
        """
        Generate vocabulary words for a specific category/subcategory.

        Automatically splits large batches into smaller chunks to avoid token limits.

        Args:
            category: Main category (finance, business, etc.)
            subcategory: Subcategory description (e.g., "payment methods", "meetings")
            count: Number of words to generate (total)
            difficulty: CEFR level or "mixed" (default: mixed)
            context: Additional context for generation
            auto_chunk: Automatically split into smaller batches (default: True)
            chunk_size: Words per chunk when auto_chunk enabled (default: 40)

        Returns:
            List of validated VocabularyWord dictionaries
        """
        if self.verbose:
            print(f"\n{'='*60}")
            print(f"Generating {count} words for: {category} / {subcategory}")
            print(f"Difficulty: {difficulty}")
            print(f"{'='*60}\n")

        # Auto-chunk large batches to avoid truncation
        if auto_chunk and count > chunk_size:
            print(f"🔄 Auto-chunking: Splitting {count} words into chunks of {chunk_size}")
            return self._generate_with_chunking(
                category, subcategory, count, difficulty, context, chunk_size
            )

        # Warn if batch size is too large and auto_chunk is disabled
        if not auto_chunk and count > 50:
            print(f"⚠ WARNING: Batch size of {count} words is large")
            print(f"⚠ Recommended: Enable auto_chunk or use 30-50 words per batch")
            print(f"⚠ Risk: Response may be truncated due to token limits")
            print()

        # Build AI prompt
        prompt = self._build_generation_prompt(
            category, subcategory, count, difficulty, context
        )

        # Call Claude API
        if self.verbose:
            print("Calling Claude API...")

        try:
            response = self.client.messages.create(
                model=self.model,  # Configurable from .env (AI_MODEL)
                max_tokens=8192,  # Claude Sonnet 4.5 max output limit
                temperature=0.7,
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )

            # Extract response
            response_text = response.content[0].text

            # Check if response was truncated
            if response.stop_reason == "max_tokens":
                print(f"⚠ WARNING: Response truncated due to token limit!")
                print(f"⚠ Reduce batch size (current: {count} words)")
                print(f"⚠ Recommended: 30-50 words per batch for premium quality")

            if self.verbose:
                print(f"✓ Received response ({len(response_text)} chars)")
                print(f"  Stop reason: {response.stop_reason}")

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

    def _generate_with_chunking(
        self,
        category: str,
        subcategory: str,
        total_count: int,
        difficulty: str,
        context: str,
        chunk_size: int
    ) -> List[VocabularyWord]:
        """
        Generate vocabulary in chunks and aggregate results.

        Args:
            category: Main category
            subcategory: Subcategory description
            total_count: Total number of words to generate
            difficulty: CEFR level or "mixed"
            context: Additional context
            chunk_size: Words per chunk

        Returns:
            Aggregated list of validated VocabularyWord dictionaries
        """
        import math
        import time

        # Calculate number of chunks
        num_chunks = math.ceil(total_count / chunk_size)
        all_words = []

        print(f"📦 Generating {total_count} words in {num_chunks} chunks of ~{chunk_size} words each\n")

        for i in range(num_chunks):
            # Calculate words for this chunk
            remaining = total_count - len(all_words)
            words_in_chunk = min(chunk_size, remaining)

            print(f"{'='*60}")
            print(f"Chunk {i+1}/{num_chunks}: Generating {words_in_chunk} words")
            print(f"Progress: {len(all_words)}/{total_count} words completed ({len(all_words)/total_count*100:.1f}%)")
            print(f"{'='*60}")

            # Generate chunk (recursive call without auto_chunk)
            chunk_words = self.generate_vocabulary(
                category=category,
                subcategory=subcategory,
                count=words_in_chunk,
                difficulty=difficulty,
                context=context,
                auto_chunk=False  # Disable auto_chunk for recursive call
            )

            if not chunk_words:
                print(f"⚠ WARNING: Chunk {i+1} generated 0 words")
                continue

            # Add to aggregated list
            all_words.extend(chunk_words)
            print(f"✓ Chunk {i+1} complete: {len(chunk_words)} words generated")
            print(f"✓ Total so far: {len(all_words)}/{total_count} words\n")

            # Add delay between chunks to avoid rate limits
            if i < num_chunks - 1:  # Don't delay after last chunk
                delay = 2  # 2 seconds between chunks
                if self.verbose:
                    print(f"⏳ Waiting {delay}s before next chunk...")
                time.sleep(delay)

        # Final summary
        print(f"\n{'='*60}")
        print(f"✓ CHUNKING COMPLETE")
        print(f"{'='*60}")
        print(f"Requested: {total_count} words")
        print(f"Generated: {len(all_words)} words")
        print(f"Success rate: {len(all_words)/total_count*100:.1f}%")
        print(f"{'='*60}\n")

        return all_words

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

**Part of Speech Distribution**:
- Nouns: ~60% (include articles: der/die/das, use part_of_speech: "noun")
- Verbs: ~25% (include separable verbs, use part_of_speech: "verb")
- Adjectives/Adverbs: ~10% (use part_of_speech: "adjective" or "adverb")
- Idioms/Expressions: ~5% (use part_of_speech: "idiom", set is_idiom: 1)

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

**Output Format** (JSON array with examples of different parts of speech):
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
  }},
  {{
    "word": "überweisen",
    "translation_it": "fare un bonifico",
    "part_of_speech": "verb",
    "gender": null,
    "plural_form": null,
    "difficulty": "B2",
    "category": "{category}",
    "example_de": "Ich überweise das Geld morgen auf Ihr Konto.",
    "example_it": "Domani farò un bonifico sul suo conto.",
    "pronunciation": "ü-ber-VAI-zen",
    "definition_de": "Geld elektronisch von einem Bankkonto auf ein anderes übertragen",
    "usage_notes": "Inseparable verb (nicht trennbar). Common in business context. Conjugation: ich überweise, du überweist, er überweist. Past: überwies, hat überwiesen.",
    "synonyms": "[\\"transferieren\\", \\"senden\\"]",
    "antonyms": "[\\"empfangen\\", \\"erhalten\\"]",
    "is_idiom": 0,
    "is_compound": 0,
    "is_separable_verb": 0
  }},
  {{
    "word": "bargeldlos",
    "translation_it": "senza contanti",
    "part_of_speech": "adjective",
    "gender": null,
    "plural_form": null,
    "difficulty": "B2",
    "category": "{category}",
    "example_de": "Die bargeldlose Zahlung ist in der Schweiz sehr verbreitet.",
    "example_it": "Il pagamento senza contanti è molto diffuso in Svizzera.",
    "pronunciation": "BAR-gelt-lohs",
    "definition_de": "Ohne Verwendung von physischem Geld; durch elektronische Zahlungsmittel",
    "usage_notes": "Common in business/finance contexts. Collocations: bargeldlose Zahlung, bargeldloser Verkehr, bargeldlose Gesellschaft. Register: formal/neutral.",
    "synonyms": "[\\"elektronisch\\", \\"digital\\"]",
    "antonyms": "[\\"bar\\", \\"in bar\\"]",
    "is_idiom": 0,
    "is_compound": 1,
    "is_separable_verb": 0
  }},
  {{
    "word": "Geld auf den Kopf hauen",
    "translation_it": "sperperare denaro",
    "part_of_speech": "idiom",
    "gender": null,
    "plural_form": null,
    "difficulty": "B2",
    "category": "{category}",
    "example_de": "Er hat sein ganzes Gehalt auf den Kopf gehauen.",
    "example_it": "Ha sperperato tutto il suo stipendio.",
    "pronunciation": "gelt owf deyn kopf HOW-en",
    "definition_de": "Viel Geld schnell und unüberlegt ausgeben",
    "usage_notes": "Informal/colloquial idiom. Literal: 'hit money on the head'. Figurative: spend money recklessly. Common in everyday speech, not in formal business contexts. Synonym idiom: 'Geld zum Fenster hinauswerfen'.",
    "synonyms": "[\\"verschwenden\\", \\"verprassen\\"]",
    "antonyms": "[\\"sparen\\", \\"zurücklegen\\"]",
    "is_idiom": 1,
    "is_compound": 0,
    "is_separable_verb": 0
  }}
]
```

**CRITICAL REQUIREMENTS**:

**For Nouns**:
- Always include article (der/die/das)
- Gender must match article (masculine/feminine/neuter)
- Provide plural forms
- Set gender and plural_form fields

**For Verbs**:
- Include infinitive form without "zu"
- Set is_separable_verb to 1 for separable verbs (e.g., "abbuchen" = ab|buchen)
- In usage_notes, mention: conjugation pattern, common tenses, prepositions used with verb
- Set gender and plural_form to null

**For Adjectives/Adverbs**:
- Provide base form (not declined)
- In usage_notes, mention: typical collocations, comparative/superlative if irregular
- Set gender and plural_form to null

**For All Parts of Speech**:
- **Boolean Fields**: Use 0 or 1 (not true/false)
- **JSON Arrays**: Synonyms/antonyms as JSON strings: "[\\"word1\\", \\"word2\\"]"
- **Pronunciation**: Simplified phonetic (not IPA): "dee ü-ber-VAI-zung"
- **Usage Notes**: Real-world context with:
  - Common collocations
  - Register (formal/informal/technical)
  - Regional variations (Germany/Austria/Switzerland)
  - When/where it's used in business contexts

**Special Cases**:
- Compound words: Set is_compound to 1
- Separable verbs: Set is_separable_verb to 1 (e.g., "abbuchen" - separable prefix "ab")
- Idioms/expressions: Use part_of_speech: "idiom", set is_idiom to 1, explain literal vs. figurative meaning
- Technical terms: Include English equivalents if commonly used

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

        # Strategy 1: Remove markdown code blocks using string operations
        # Look for ```json or ``` markers and remove them
        if "```json" in json_text:
            # Split by ```json and take the part after it
            parts = json_text.split("```json", 1)
            if len(parts) > 1:
                json_text = parts[1]
                # Now remove trailing ``` if present
                if "```" in json_text:
                    json_text = json_text.split("```")[0]
        elif json_text.startswith("```"):
            # Remove leading ```
            json_text = json_text[3:]
            # Remove trailing ``` if present
            if "```" in json_text:
                json_text = json_text.split("```")[0]

        json_text = json_text.strip()

        # Strategy 2: If still doesn't start with [, try to find JSON array
        if not json_text.startswith('['):
            # Find the first [ and last ] in the text
            start_idx = json_text.find('[')
            end_idx = json_text.rfind(']')
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                json_text = json_text[start_idx:end_idx + 1]

        json_text = json_text.strip()

        try:
            words = json.loads(json_text)

            if not isinstance(words, list):
                print(f"✗ Error: Expected JSON array, got {type(words)}")
                return []

            if self.verbose:
                print(f"✓ Successfully parsed {len(words)} words")

            # Fix common issues with synonyms/antonyms fields
            words = self._fix_json_array_fields(words)

            return words

        except json.JSONDecodeError as e:
            print(f"✗ Error parsing JSON: {str(e)}")
            print(f"Response preview: {response_text[:500]}...")
            print(f"Extracted text preview: {json_text[:500]}...")

            # Try to repair common JSON issues
            print(f"\n⚙ Attempting to repair JSON...")
            repaired_json = self._repair_json(json_text)

            if repaired_json != json_text:
                try:
                    words = json.loads(repaired_json)
                    if isinstance(words, list):
                        print(f"✓ JSON repaired successfully! Parsed {len(words)} words")
                        # Fix common issues with synonyms/antonyms fields
                        words = self._fix_json_array_fields(words)
                        return words
                except json.JSONDecodeError:
                    print(f"✗ JSON repair failed")

            # Save raw response to file for debugging
            print(f"\nTrying to save raw response for debugging...")
            try:
                with open("/tmp/claude_response_debug.txt", "w", encoding="utf-8") as f:
                    f.write(response_text)
                with open("/tmp/claude_extracted_debug.txt", "w", encoding="utf-8") as f:
                    f.write(json_text)
                print(f"✓ Raw response saved to /tmp/claude_response_debug.txt")
                print(f"✓ Extracted JSON saved to /tmp/claude_extracted_debug.txt")
            except Exception:
                pass
            return []

    def _repair_json(self, json_text: str) -> str:
        """
        Attempt to repair common JSON issues.

        Args:
            json_text: Potentially malformed JSON string

        Returns:
            Repaired JSON string
        """
        # Remove trailing commas before } or ]
        json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)

        # Fix truncated JSON - if doesn't end with ], try to close it
        json_text = json_text.rstrip()
        if not json_text.endswith(']'):
            # Count open brackets vs close brackets
            open_brackets = json_text.count('[')
            close_brackets = json_text.count(']')
            open_braces = json_text.count('{')
            close_braces = json_text.count('}')

            # Try to close incomplete structures
            if open_braces > close_braces:
                # Close any incomplete objects
                json_text += '\n}' * (open_braces - close_braces)

            if open_brackets > close_brackets:
                # Close any incomplete arrays
                json_text += '\n]' * (open_brackets - close_brackets)

        return json_text

    def _fix_json_array_fields(self, words: List[VocabularyWord]) -> List[VocabularyWord]:
        """
        Fix common issues with synonyms/antonyms JSON array fields.

        Args:
            words: List of vocabulary words

        Returns:
            Fixed list of vocabulary words
        """
        for word in words:
            for field in ['synonyms', 'antonyms']:
                if field in word and word[field]:
                    value = word[field]

                    # If empty string or "none" or "N/A", remove field
                    if value.lower() in ['', 'none', 'n/a', 'null', '-', 'keine']:
                        del word[field]
                        continue

                    # If already valid JSON array, check if empty
                    if value.startswith('[') and value.endswith(']'):
                        try:
                            parsed = json.loads(value)
                            # If empty array, remove field
                            if isinstance(parsed, list) and len(parsed) == 0:
                                del word[field]
                                continue
                            # If valid non-empty array, keep it
                            continue
                        except:
                            pass

                    # If plain text without brackets, wrap in JSON array
                    # Common cases: "word" or "word1, word2"
                    if not value.startswith('['):
                        # Split by comma if present
                        items = [item.strip() for item in value.split(',')]
                        # Wrap each item in quotes and create JSON array
                        word[field] = json.dumps(items, ensure_ascii=False)

        return words

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
                f.write('from vocabulary_seeds.core.data_format import VocabularyWord\n\n\n')
                f.write('def get_vocabulary_words() -> List[VocabularyWord]:\n')
                f.write('    """\n')
                f.write('    Get generated vocabulary words.\n')
                f.write('    \n')
                f.write('    Returns:\n')
                f.write('        List of VocabularyWord dictionaries with proper type hints\n')
                f.write('    """\n')
                f.write('    words = ')

                # Write words as Python list
                json_output = json.dumps(words, indent=4, ensure_ascii=False)

                # Replace JSON null with Python None
                json_output = json_output.replace(': null', ': None')

                f.write(json_output)

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
  # Auto-chunking enabled by default (recommended)
  %(prog)s --category finance --subcategory "payment methods" --count 80
  %(prog)s --category business --subcategory "meetings" --count 150 --chunk-size 50

  # Custom chunk size
  %(prog)s --category finance --subcategory "banking" --count 200 --chunk-size 40

  # Disable auto-chunking (not recommended for large batches)
  %(prog)s --category finance --subcategory "blockchain" --count 30 --no-auto-chunk

Note: Auto-chunking splits large batches into smaller chunks (default: 40 words)
      and aggregates results into a single file. This prevents truncation.
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
        default=40,
        help="Number of words to generate (default: 40, recommended: 30-50)"
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

    parser.add_argument(
        "--no-auto-chunk",
        action="store_true",
        help="Disable automatic batch chunking (not recommended for large batches)"
    )

    parser.add_argument(
        "--chunk-size",
        type=int,
        default=40,
        help="Words per chunk when auto-chunking (default: 40)"
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
        context=args.context,
        auto_chunk=not args.no_auto_chunk,  # Enable by default
        chunk_size=args.chunk_size
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
