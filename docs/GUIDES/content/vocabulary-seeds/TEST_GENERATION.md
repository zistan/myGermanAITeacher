# Test AI Generation - Quick Start

This guide shows how to test the AI vocabulary generator with a single small batch.

---

## Prerequisites

```bash
# 1. Set API key
export ANTHROPIC_API_KEY="sk-ant-your-key-here"

# 2. Install anthropic package
cd backend
source venv/bin/activate  # On server
pip install anthropic
```

---

## Test 1: Generate 10 Payment Terms (Quick Test)

This generates just 10 words to verify the system works:

```bash
cd backend/scripts/vocabulary_seeds

python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment methods" \
  --count 10 \
  --difficulty B2 \
  --output test_output.py \
  --verbose
```

**Expected Output** (~30 seconds):
```
============================================================
Generating 10 words for: finance / payment methods
Difficulty: B2
============================================================

Calling Claude API...
✓ Received response (8542 chars)
✓ Parsed 10 words from response
✓ Validation complete: 10 valid, 0 invalid
✓ Saved 10 words to test_output.py (Python)

============================================================
✓ SUCCESS
============================================================
Generated: 10 words
Category: finance / payment methods
Output: test_output.py
============================================================
```

**Review Generated File**:
```bash
cat test_output.py
```

**Expected Content**:
```python
"""Generated vocabulary words."""

from typing import List
from ..core.data_format import VocabularyWord


def get_vocabulary_words() -> List[VocabularyWord]:
    """Get generated vocabulary words."""
    words = [
        {
            "word": "die Überweisung",
            "translation_it": "il bonifico",
            "part_of_speech": "noun",
            "gender": "feminine",
            "plural_form": "die Überweisungen",
            "difficulty": "B2",
            "category": "finance",
            "example_de": "Die Überweisung dauert 1-2 Werktage.",
            "example_it": "Il bonifico richiede 1-2 giorni lavorativi.",
            "pronunciation": "dee ü-ber-VAI-zung",
            "definition_de": "Zahlungsvorgang zur Übertragung von Geld",
            "usage_notes": "Standard bank transfer. Most common...",
            "synonyms": "[\"die Banküberweisung\", \"der Transfer\"]",
            "antonyms": "[\"die Lastschrift\"]",
            "is_idiom": 0,
            "is_compound": 1,
            "is_separable_verb": 0
        },
        # ... 9 more words
    ]

    return words
```

---

## Test 2: Validate Generated Words

```bash
# Import and validate
python3 -c "
import sys
sys.path.insert(0, '.')
from test_output import get_vocabulary_words
from core.validation import VocabularyValidator

words = get_vocabulary_words()
validator = VocabularyValidator(verbose=True)
result = validator.validate_words(words)

print(result.summary())

if result.is_valid():
    print('\n✓ All words valid!')
else:
    print('\n✗ Validation errors found')
    for error in result.errors:
        print(f'  - {error}')
"
```

---

## Test 3: Test Batch Generation (Single Batch)

Generate only the first batch from the business configuration:

```bash
cd batches

python3 run_batch_generation.py \
  business_vocabulary_batches.json \
  --only 0 \
  --verbose
```

This generates:
- **Batch 0**: Payment methods (80 words)
- **Output**: `business/generated_payments_01_methods.py`
- **Time**: ~2 minutes

---

## Test 4: Insert Test Words to Database

```bash
cd ..

# Dry run first (no database changes)
python3 master_seed.py --categories business --dry-run

# If validation passes, insert to database
python3 master_seed.py --categories business
```

---

## Troubleshooting Tests

### Test Fails: "No module named 'anthropic'"

```bash
pip install anthropic
```

### Test Fails: "No API key provided"

```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# Set it if missing
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

### Test Fails: "Invalid JSON response"

This can happen if Claude's response includes extra text. The parser handles most cases, but occasionally manual cleanup is needed.

**Solution**: Run with `--verbose` to see the raw response, then report the issue.

### Generated Words Have Validation Errors

**Common issues**:
1. Missing gender for nouns
2. Boolean fields as strings ("true" instead of 1)
3. Invalid CEFR level

**Solution**: Edit the generated file manually to fix errors, then re-validate.

---

## Success Criteria

✅ **Test 1**: Generates 10 words successfully
✅ **Test 2**: All 10 words pass validation
✅ **Test 3**: Batch generation creates file with 80 words
✅ **Test 4**: Words insert into database without errors

If all tests pass, you're ready to generate the full 3,500 business vocabulary!

---

## Next: Full Business Vocabulary Generation

Once tests pass, run the full batch:

```bash
cd batches
python3 run_batch_generation.py business_vocabulary_batches.json --verbose
```

This will generate all 3,500 business words in ~2 hours.

