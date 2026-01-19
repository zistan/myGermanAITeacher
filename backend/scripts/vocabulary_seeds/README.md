# Vocabulary Seeds - 150 → 25,000 Words Expansion

Modular, scalable vocabulary seeding system for the German Learning Application.

## Overview

This directory contains infrastructure and data for expanding vocabulary from 150 to 25,000 German words across 6 phases:

- **Phase 1**: Infrastructure (validation, bulk insert, orchestration) ✅
- **Phase 2**: Business vocabulary (3,500 words - HIGHEST PRIORITY) 🔄
- **Phase 3**: Core frequency A1-B2 (10,000 words)
- **Phase 4**: Advanced C1-C2 (8,000 words)
- **Phase 5**: Thematic categories (5,000 words)
- **Phase 6**: Linguistic completeness (3,200 words)

## Directory Structure

```
vocabulary_seeds/
├── master_seed.py              # CLI orchestrator
├── core/                       # Infrastructure
│   ├── data_format.py          # TypedDict definitions & constants
│   ├── validation.py           # VocabularyValidator class
│   └── bulk_insert.py          # Efficient batch insertion
├── business/                   # Phase 2 - PRIORITY (3,500 words)
│   ├── seed_finance_payments.py      # 800 words - CRITICAL
│   ├── seed_business_general.py      # 1,500 words
│   ├── seed_finance_banking.py       # 400 words
│   ├── seed_finance_accounting.py    # 300 words
│   ├── seed_business_legal.py        # 300 words
│   └── seed_business_hr.py           # 200 words
├── cefr_core/                  # Phase 3 (10,000 words)
├── advanced/                   # Phase 4 (8,000 words)
├── thematic/                   # Phase 5 (5,000 words)
└── linguistic/                 # Phase 6 (3,200 words)
```

## Quick Start

### On Server (Production)

```bash
# 1. Pull latest changes
cd /opt/german-learning-app
git pull origin master

# 2. Activate virtual environment
cd backend
source venv/bin/activate

# 3. Dry run (validate without inserting)
cd scripts/vocabulary_seeds
python3 master_seed.py --priority --dry-run --verbose

# 4. Insert priority business vocabulary
python3 master_seed.py --priority

# 5. Verify in database
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary WHERE category IN ('finance', 'business');"
```

## Usage

### CLI Commands

```bash
# Seed all categories (25,000 words)
python3 master_seed.py --all

# Seed priority business vocabulary (3,500 words)
python3 master_seed.py --priority

# Seed specific categories
python3 master_seed.py --categories business cefr_core

# Dry run (validate without inserting)
python3 master_seed.py --all --dry-run

# Verbose output with statistics
python3 master_seed.py --priority --verbose

# Skip validation (use with caution)
python3 master_seed.py --all --skip-validation

# Custom batch size
python3 master_seed.py --all --batch-size 2000
```

### Create New Seed Module

Each seed module must implement `get_vocabulary_words()` function:

```python
"""Seed module for [category description]."""

from typing import List
from ..core.data_format import VocabularyWord


def get_vocabulary_words() -> List[VocabularyWord]:
    """
    Get vocabulary words for [category].

    Returns:
        List of VocabularyWord dictionaries
    """
    words = [
        {
            # Required fields
            "word": "die Überweisung",
            "translation_it": "il bonifico",
            "part_of_speech": "noun",
            "difficulty": "B2",
            "category": "finance",
            "example_de": "Die Überweisung dauert 1-2 Werktage.",
            "example_it": "Il bonifico richiede 1-2 giorni lavorativi.",

            # Noun-specific
            "gender": "feminine",
            "plural_form": "die Überweisungen",

            # Optional enrichment (Premium quality)
            "pronunciation": "dee ü-ber-vai-zung",
            "definition_de": "Zahlungsvorgang zur Übertragung von Geld",
            "usage_notes": "Common in banking contexts. See also: Echtzeitüberweisung.",
            "synonyms": '["die Zahlung", "der Transfer"]',
            "antonyms": '["die Lastschrift"]',

            # Linguistic flags
            "is_idiom": 0,
            "is_compound": 1,
            "is_separable_verb": 0
        },
        # ... more words
    ]

    return words
```

## Data Quality Standards

### Premium Tier (Business, C1-C2, Modal Particles)
- All 14 fields populated
- Pronunciation (IPA or simplified)
- German definition (1-2 sentences)
- Usage notes with context and register
- Synonyms array

### Standard Tier (B1-B2, Thematic)
- 7 required fields + pronunciation + usage_notes
- 80%+ with pronunciation

### Basic Tier (A1-A2)
- 7 required fields only

## Validation Rules

The `VocabularyValidator` checks:

1. **Required Fields**: word, translation_it, part_of_speech, difficulty, category, example_de, example_it
2. **CEFR Levels**: Must be A1, A2, B1, B2, C1, or C2
3. **Categories**: Must be in VALID_CATEGORIES list
4. **Part of Speech**: Must be in VALID_POS list
5. **Nouns**: Must include article (der/die/das)
6. **Gender**: Must match article (masculine/feminine/neuter)
7. **Boolean Fields**: Must be 0, 1, True, or False
8. **JSON Arrays**: Synonyms/antonyms must be valid JSON format
9. **Duplicates**: Case-insensitive duplicate detection

## Performance

- **Target**: <5 minutes for 25,000 words
- **Batch Size**: 1000 words per commit (configurable)
- **Method**: PostgreSQL `INSERT ... ON CONFLICT DO NOTHING`
- **Duplicate Handling**: Automatic skip (no errors)

## Database Schema

Vocabulary table fields:
- `word` (TEXT, UNIQUE) - German word with article
- `translation_it` (TEXT) - Italian translation
- `part_of_speech` (TEXT) - noun, verb, adjective, etc.
- `gender` (TEXT, nullable) - masculine, feminine, neuter
- `plural_form` (TEXT, nullable)
- `difficulty` (TEXT) - CEFR level
- `category` (TEXT) - finance, business, daily, etc.
- `example_de` (TEXT) - German example
- `example_it` (TEXT) - Italian translation
- `pronunciation` (TEXT, nullable)
- `definition_de` (TEXT, nullable)
- `synonyms` (TEXT, nullable) - JSON array
- `antonyms` (TEXT, nullable) - JSON array
- `usage_notes` (TEXT, nullable)
- `is_idiom` (INTEGER) - 0 or 1
- `is_compound` (INTEGER) - 0 or 1
- `is_separable_verb` (INTEGER) - 0 or 1

## Troubleshooting

### "Module not found" during dry run
- Module not yet implemented - expected for incomplete phases
- Check module path in CATEGORY_REGISTRY

### Validation errors
- Check required fields are present
- Verify CEFR level is uppercase (A1-C2)
- Ensure category is in VALID_CATEGORIES
- Nouns must have article and gender

### Duplicates
- Automatically skipped during insertion (ON CONFLICT DO NOTHING)
- Check validation output for warnings

### Slow performance
- Increase --batch-size (try 2000)
- Verify database indexes exist on word, category, difficulty

## Implementation Status

- [x] **Phase 1**: Infrastructure complete
  - [x] data_format.py - Type definitions
  - [x] validation.py - VocabularyValidator
  - [x] bulk_insert.py - Batch insertion
  - [x] master_seed.py - CLI orchestrator

- [ ] **Phase 2**: Business vocabulary (PRIORITY)
  - [ ] seed_finance_payments.py (800 words)
  - [ ] seed_business_general.py (1,500 words)
  - [ ] seed_finance_banking.py (400 words)
  - [ ] seed_finance_accounting.py (300 words)
  - [ ] seed_business_legal.py (300 words)
  - [ ] seed_business_hr.py (200 words)

- [ ] **Phase 3-6**: Remaining categories (19,500 words)

## Contributing

When adding new seed modules:

1. Follow data format in `core/data_format.py`
2. Implement `get_vocabulary_words()` function
3. Register module in `master_seed.py` CATEGORY_REGISTRY
4. Test with `--dry-run --verbose` first
5. Verify quality tier meets phase requirements
6. Commit and push to Git

## References

- BRD: `/brd and planning documents/german_learning_app_brd.md`
- Implementation Plan: See commit message for detailed phase breakdown
- Database Schema: `/backend/alembic/versions/001_update_vocabulary_schema.py`

---

**Status**: Phase 1 Complete ✅ | Phase 2 In Progress 🔄
**Last Updated**: 2026-01-19
