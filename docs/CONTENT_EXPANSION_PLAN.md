# German Learning App - Content Expansion Plan

**Created**: 2026-01-19
**Target User**: Igor - Italian native, B2/C1 level, payments/finance professional
**Goal**: Expand grammar (35→53 topics) and vocabulary (150→25,000 words)

---

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Part 1: Grammar Expansion](#part-1-grammar-expansion)
3. [Part 2: Vocabulary Expansion](#part-2-vocabulary-expansion)
4. [Implementation Timeline](#implementation-timeline)
5. [Agent Instructions](#agent-instructions)

---

## Executive Summary

### Grammar Expansion
- **Current**: 35 topics, 132 exercises
- **Target**: 53 topics (+18), 220-250 exercises (+90-120)
- **Focus**: B2/C1 business German (50%+ business context)
- **Timeline**: 2-3 weeks

### Vocabulary Expansion
- **Current**: ~150 words
- **Target**: 25,000 words (+24,850)
- **Focus**: 64% at B2/C1, 34% business/finance (8,500 words)
- **Timeline**: 10 weeks (phased, incremental deployment)

### Priority
**Week 2**: Critical business vocabulary (3,500 words) + Tier 1 grammar (8 topics)
Delivers immediate professional value for Igor's payments/finance work

---

## Part 1: Grammar Expansion

### Current State Analysis
- **35 grammar topics** organized into 7 categories
- **132 exercises** across 5 types (fill_blank, multiple_choice, translation, error_correction, sentence_building)
- **CEFR distribution**: Heavy A2-B1 focus, light on B2/C1
- **Business context**: Only 10.6% of exercises

### Expansion Goals
- **53 total topics** (+18 new topics in 3 tiers)
- **220-250 total exercises** (+90-120 new exercises)
- **Business context**: 50%+ in new exercises
- **Level distribution**: 75%+ new exercises at B2/C1
- **Context balance**: Business, daily, general scenarios

### New Grammar Topics (18 Topics)

#### Tier 1: Essential Business Grammar (8 topics - HIGHEST PRIORITY)

1. **Plusquamperfekt (Pluperfect)** - B2
   - Past perfect tense for business narratives
   - Usage: "Nachdem wir die Zahlung erhalten hatten, haben wir die Ware verschickt."
   - 5-6 exercises (fill_blank, multiple_choice, translation, error_correction, sentence_building)

2. **Futur II (Future Perfect)** - B2
   - Future perfect for projections
   - Usage: "Bis Ende des Jahres werden wir 1000 Transaktionen verarbeitet haben."
   - 5-6 exercises

3. **Konditionalsätze (Conditional Sentences)** - B2
   - wenn...dann structures
   - Types: Real conditions, Unreal conditions (Konjunktiv II)
   - Business scenarios: negotiations, contracts
   - 6 exercises

4. **Konzessive Sätze (Concessive Clauses)** - B2
   - obwohl, trotzdem, dennoch
   - Usage: "Obwohl die Kosten hoch sind, investieren wir in neue Technologie."
   - 5 exercises

5. **Kausale und Konsekutive Sätze (Cause/Effect)** - B2
   - weil, da, sodass, deshalb, daher
   - Critical for business reasoning
   - 5-6 exercises

6. **Finale Sätze (Purpose Clauses)** - B2
   - um...zu, damit
   - Usage: "Wir digitalisieren Prozesse, um effizienter zu arbeiten."
   - 5 exercises

7. **Modalverben in Nebensätzen (Modals in Subordinate Clauses)** - B2
   - Word order with modal verbs in subordinate clauses
   - Usage: "Ich weiß, dass wir das Projekt abschließen müssen."
   - 5 exercises

8. **Nominalstil vs. Verbalstil (Nominal vs. Verbal Style)** - C1
   - Nominal style in business writing
   - Usage: "Die Durchführung der Zahlung" vs. "Die Zahlung durchführen"
   - 5 exercises

#### Tier 2: Advanced Refinement (6 topics)

9. **Erweiterte Attribute (Extended Attributes)** - C1
   - Extended attributes before nouns
   - "Die gestern eingegangene Zahlung"

10. **Partizipialkonstruktionen (Participial Constructions)** - C1
    - "Die von der Bank genehmigte Transaktion"

11. **Präpositionale Ausdrücke (Prepositional Expressions)** - B2
    - Business phrases: im Hinblick auf, in Bezug auf, aufgrund

12. **Indirekte Rede erweitert (Extended Indirect Speech)** - C1
    - All tenses in indirect speech
    - Reporting in business contexts

13. **Subjektive Modalverben (Subjective Modal Verbs)** - C1
    - dürfte, soll, will (subjective meanings)
    - "Er soll sehr erfahren sein." (supposedly)

14. **Konjunktiv II der Vergangenheit (Past Subjunctive II)** - C1
    - "Hätten wir früher investiert, wären wir erfolgreicher."

#### Tier 3: Professional Precision (4 topics)

15. **Funktionsverbgefüge (Function Verb Phrases)** - C1
    - Fixed combinations: eine Entscheidung treffen, in Kraft treten

16. **Graduierung und Intensivierung (Gradation)** - B2
    - äußerst wichtig, höchst interessant

17. **Rhetorische Strukturen (Rhetorical Structures)** - C1
    - For presentations and speeches

18. **Register und Höflichkeit (Register and Politeness)** - B2
    - Formal vs. informal, Swiss German etiquette

### Exercise Distribution Strategy

**Total New Exercises**: 90-120

**By Tier**:
- Tier 1 (8 topics): 5-6 exercises each = 40-48 exercises
- Tier 2 (6 topics): 4-5 exercises each = 24-30 exercises
- Tier 3 (4 topics): 4-5 exercises each = 16-20 exercises
- Additional for existing topics: 10-22 exercises

**By Exercise Type**:
- fill_blank: 35-45 (40%)
- multiple_choice: 20-25 (22%)
- translation: 15-20 (17%)
- error_correction: 15-20 (17%)
- sentence_building: 5-10 (4%)

**By Context**:
- **business**: 50%+ (45-60 exercises) - Payments, contracts, meetings
- **daily**: 25% (22-30 exercises) - Professional situations
- **general**: 25% (22-30 exercises) - Universal examples

**By Difficulty**:
- **B2**: 60-65% (55-70 exercises)
- **C1**: 30-35% (30-45 exercises)
- **C2**: 5% (5-10 exercises)

### Implementation Structure

**File**: `backend/scripts/seed_grammar_data_b2c1_business.py`

**Rationale for Single File**:
- Maintains consistency with existing `seed_grammar_data.py`
- All B2/C1 business extensions in one reviewable unit
- Easy to deploy: `python backend/scripts/seed_grammar_data_b2c1_business.py`

**Code Structure**:
```python
# backend/scripts/seed_grammar_data_b2c1_business.py

"""
Grammar Topics and Exercises - B2/C1 Business Focus
Extends existing 35 topics with 18 advanced topics.
"""

from app.database import SessionLocal
from app.models.grammar import GrammarTopic, GrammarExercise
from sqlalchemy import func

# ========== TIER 1: ESSENTIAL BUSINESS GRAMMAR ==========

# Topic 1: Plusquamperfekt
PLUSQUAMPERFEKT_TOPIC = {
    "name_de": "Plusquamperfekt (Vorvergangenheit)",
    "name_en": "Pluperfect / Past Perfect",
    "category": "verbs",
    "subcategory": "tenses",
    "difficulty_level": "B2",
    "description_de": "Zeitform für Ereignisse vor anderen vergangenen Ereignissen",
    "explanation_de": """
Das Plusquamperfekt beschreibt Handlungen, die VOR anderen vergangenen Handlungen abgeschlossen wurden.

**Bildung**: hatten/waren + Partizip II
- Mit 'haben': Ich hatte die E-Mail geschrieben.
- Mit 'sein': Er war angekommen.

**Verwendung**:
1. Vorvergangenheit: "Nachdem ich die Rechnung bezahlt hatte, bekam ich die Ware."
2. Indirekte Rede: "Er sagte, er hatte das Projekt abgeschlossen."
3. Irreale Bedingungen: "Wenn wir früher investiert hätten..."

**Im Business-Kontext**:
- Berichte über abgeschlossene Projekte
- Ursache-Wirkung in Vergangenheit
- Chronologische Darstellung von Ereignissen
    """,
    "order_index": 36
}

PLUSQUAMPERFEKT_EXERCISES = [
    {
        "exercise_type": "fill_blank",
        "difficulty_level": "B2",
        "question_text": "Nachdem wir die Zahlung {{blank}} (erhalten), haben wir die Ware verschickt.",
        "question_data": {
            "blanks": [{"id": 1, "position": "after 'die Zahlung'"}],
            "context": "business_payment"
        },
        "correct_answer": "erhalten hatten",
        "alternative_answers": ["bekommen hatten"],
        "explanation_de": "Plusquamperfekt mit 'haben': hatte(n) + Partizip II. Das Erhalten der Zahlung geschah VOR dem Versenden der Ware.",
        "explanation_it": "Trapassato prossimo: aveva(no) + participio. Il ricevimento è avvenuto PRIMA della spedizione.",
        "hints": [
            "Verwende das Plusquamperfekt (Vorvergangenheit)",
            "Benötigt 'hatten' + Partizip II",
            "'erhalten' bildet Perfekt mit 'haben'"
        ],
        "context_category": "business",
        "source": "manual",
        "is_active": True
    },
    # ... 4-5 more exercises for Plusquamperfekt
]

# Topics 2-8: Futur II, Conditional, Concessive, Causal, Final, Modal in subordinate, Nominal style
# ... (similar structure)

# ========== TIER 2: ADVANCED REFINEMENT ==========
# Topics 9-14
# ...

# ========== TIER 3: PROFESSIONAL PRECISION ==========
# Topics 15-18
# ...

def seed_b2c1_business_grammar():
    """Seed advanced B2/C1 business grammar (18 topics, 90-120 exercises)."""
    db = SessionLocal()

    try:
        existing_count = db.query(func.count(GrammarTopic.id)).scalar()
        print(f"Existing topics: {existing_count}")

        # Collect all new topics
        new_topics = [
            PLUSQUAMPERFEKT_TOPIC,
            FUTUR_II_TOPIC,
            # ... all 18 topics
        ]

        # Insert topics
        topics_created = []
        for topic_data in new_topics:
            existing = db.query(GrammarTopic).filter(
                GrammarTopic.name_de == topic_data["name_de"]
            ).first()

            if not existing:
                topic = GrammarTopic(**topic_data)
                db.add(topic)
                db.flush()
                topics_created.append(topic)
                print(f"✅ Created: {topic.name_de}")
            else:
                topics_created.append(existing)
                print(f"⚠️  Exists: {topic_data['name_de']}")

        db.commit()

        # Collect all exercises
        all_exercises = []
        all_exercises.extend([(topics_created[0], ex) for ex in PLUSQUAMPERFEKT_EXERCISES])
        # ... add all exercises for all topics

        # Insert exercises
        exercises_created = 0
        for topic, exercise_data in all_exercises:
            exercise_data["topic_id"] = topic.id
            exercise = GrammarExercise(**exercise_data)
            db.add(exercise)
            exercises_created += 1

        db.commit()

        print("\n" + "="*60)
        print("✅ B2/C1 BUSINESS GRAMMAR COMPLETE")
        print("="*60)
        print(f"Topics: {len(topics_created)}")
        print(f"Exercises: {exercises_created}")
        print("="*60)

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_b2c1_business_grammar()
```

### Sample Exercise Set: Plusquamperfekt

Complete example showing all 5 exercise types:

**1. Fill Blank - Business Payment**
```python
{
    "exercise_type": "fill_blank",
    "difficulty_level": "B2",
    "question_text": "Nachdem wir die Zahlung {{blank}} (erhalten), haben wir die Ware verschickt.",
    "correct_answer": "erhalten hatten",
    "alternative_answers": ["bekommen hatten"],
    "explanation_de": "Plusquamperfekt: hatte(n) + Partizip II. Das Erhalten geschah VOR dem Versenden.",
    "explanation_it": "Trapassato prossimo: aveva(no) + participio. Ricevimento PRIMA della spedizione.",
    "hints": ["Verwende Plusquamperfekt", "hatten + Partizip II", "erhalten mit 'haben'"],
    "context_category": "business"
}
```

**2. Multiple Choice - Timeline**
```python
{
    "exercise_type": "multiple_choice",
    "difficulty_level": "B2",
    "question_text": "Welcher Satz beschreibt die richtige zeitliche Reihenfolge?",
    "question_data": {
        "options": [
            "Der Kunde beschwerte sich, weil er die Rechnung nicht bekommen hatte.",
            "Der Kunde beschwerte sich, weil er die Rechnung nicht bekommen hat.",
            "Der Kunde hat sich beschwert, weil er die Rechnung nicht bekommen hatte."
        ],
        "correct_index": 0
    },
    "correct_answer": "0",
    "explanation_de": "Option 1: Plusquamperfekt (bekommen hatte) für frühere Handlung, Präteritum (beschwerte) für spätere.",
    "hints": ["Nicht-Bekommen geschah zuerst", "Frühere = Plusquamperfekt", "Spätere = Präteritum"],
    "context_category": "business"
}
```

**3. Translation - Italian to German**
```python
{
    "exercise_type": "translation",
    "difficulty_level": "B2",
    "question_text": "Übersetze: Dopo che avevamo firmato il contratto, abbiamo iniziato il progetto.",
    "correct_answer": "Nachdem wir den Vertrag unterschrieben hatten, haben wir das Projekt begonnen.",
    "alternative_answers": [
        "Nachdem wir den Vertrag unterzeichnet hatten, begannen wir das Projekt."
    ],
    "explanation_de": "Plusquamperfekt nach 'nachdem', Perfekt/Präteritum für Folgehandlung.",
    "hints": ["'Dopo che' = 'Nachdem'", "unterschreiben = firmare", "den Vertrag (Akkusativ)"],
    "context_category": "business"
}
```

**4. Error Correction**
```python
{
    "exercise_type": "error_correction",
    "difficulty_level": "B2",
    "question_text": "Korrigiere: Bevor wir die Präsentation gehalten haben, hatten wir alle Daten geprüft.",
    "correct_answer": "Bevor wir die Präsentation hielten, hatten wir alle Daten geprüft.",
    "alternative_answers": ["Nachdem wir alle Daten geprüft hatten, hielten wir die Präsentation."],
    "explanation_de": "Mit 'bevor' ist Plusquamperfekt im Nebensatz falsch. Richtig: Präteritum im Nebensatz, Plusquamperfekt im Hauptsatz.",
    "hints": ["Zeitenfolge bei 'bevor' ist umgekehrt", "Frühere Handlung = Plusquamperfekt"],
    "context_category": "business"
}
```

**5. Sentence Building**
```python
{
    "exercise_type": "sentence_building",
    "difficulty_level": "B2",
    "question_text": "Ordne die Wörter: verschickt / Nachdem / die Ware / wir / hatten / erhalten / die Rechnung / wir / haben",
    "correct_answer": "Nachdem wir die Ware erhalten hatten, haben wir die Rechnung verschickt.",
    "explanation_de": "Nebensatz mit 'nachdem' + Plusquamperfekt, dann Hauptsatz mit Perfekt.",
    "hints": ["Beginne mit 'Nachdem'", "Verb am Ende des Nebensatzes", "Hauptsatz: normales SVO"],
    "context_category": "business"
}
```

---

## Part 2: Vocabulary Expansion to 25,000 Words

### Current State
- **~150 words** across 6 categories (business, daily, verbs, adjectives, idioms, compounds)
- **Distribution**: A1=28, A2=35, B1=50, B2=25, C1=10, C2=2
- **Business**: Only 25 words (16.7%)

### Expansion Goals
- **25,000 total words** (+24,850 new)
- **B2/C1 focus**: 64% (16,000 words)
- **Business/finance**: 34% (8,500 words)
- **All semantic fields**: food, travel, technology, health, culture, etc.

### Target CEFR Distribution

| Level | Words | % | Rationale |
|-------|-------|---|-----------|
| **A1** | 800 | 3.2% | Foundation (Igor knows most) |
| **A2** | 1,200 | 4.8% | Review level |
| **B1** | 4,000 | 16% | Intermediate base |
| **B2** | 8,000 | 32% | **PRIMARY** - Current level |
| **C1** | 8,000 | 32% | **PRIMARY** - Target level |
| **C2** | 3,000 | 12% | Advanced mastery |
| **TOTAL** | **25,000** | **100%** | |

### Category Breakdown

#### A. Business & Finance (8,500 words - 34%)

| Subcategory | Words | Priority | File |
|------------|-------|----------|------|
| Payments & Processing | 800 | **CRITICAL** | `seed_finance_payments.py` |
| General Business | 2,500 | High | `seed_business_general.py` |
| Business Communication | 1,000 | High | (in general) |
| Finance - Banking | 600 | High | `seed_finance_banking.py` |
| Finance - Accounting | 400 | High | `seed_finance_accounting.py` |
| Legal & Compliance | 800 | High | `seed_business_legal.py` |
| Management & HR | 600 | Medium | `seed_business_hr.py` |
| Marketing & Sales | 400 | Medium | (in general) |
| Project Management | 400 | Medium | (in general) |
| IT & Software | 600 | Medium | `seed_technology_digital.py` |
| Swiss German Business | 400 | High | (integrated) |

#### B. Daily Life & General (7,000 words - 28%)

| Category | Words | Levels | File |
|----------|-------|--------|------|
| Food & Drink | 1,200 | A1-B2 | `seed_food_drink.py` |
| Home & Housing | 800 | A1-B2 | `seed_home_housing.py` |
| Health & Medical | 700 | A1-C1 | `seed_health_medical.py` |
| Travel & Transport | 900 | A1-B2 | `seed_travel_transport.py` |
| Shopping & Services | 600 | A1-B1 | (in daily) |
| Family & Relationships | 500 | A1-B2 | (in daily) |
| Weather & Nature | 400 | A1-B1 | `seed_nature_weather.py` |
| Time & Calendar | 300 | A1-B1 | (in core) |
| Emotions & Feelings | 500 | A2-C1 | `seed_emotions_social.py` |
| Hobbies & Leisure | 500 | A2-B2 | `seed_sports_leisure.py` |
| Culture & Media | 600 | B1-C1 | `seed_culture_media.py` |

#### C. Core Linguistic (6,500 words - 26%)

| Type | Words | File |
|------|-------|------|
| Verbs | 2,500 | `seed_verbs_frequency.py` |
| Adjectives | 1,500 | `seed_adjectives_frequency.py` |
| Nouns | 1,200 | (distributed) |
| Adverbs | 600 | `seed_adverbs.py` |
| Compounds | 800 | `seed_compound_words.py` |
| Separable Verbs | 400 | `seed_separable_verbs.py` |

#### D. Specialized (2,000 words - 8%)

| Category | Words |
|----------|-------|
| Education & Learning | 500 |
| Science & Technology | 600 |
| Politics & Society | 400 |
| Environment | 300 |
| Philosophy & Ethics | 200 |

#### E. Expressions & Idioms (1,000 words - 4%)

| Type | Words |
|------|-------|
| Common Idioms | 300 |
| Business Phrases | 200 |
| Colloquial Expressions | 200 |
| Fixed Phrases | 150 |
| Modal Particles | 150 |

### Implementation Architecture: Modular Structure

**30+ category-based seed files** in organized directory:

```
backend/scripts/vocabulary_seeds/
├── __init__.py
├── seed_vocabulary_master.py          # Orchestrator (entry point)
├── core/
│   ├── seed_a1_foundation.py          # 800 words
│   ├── seed_a2_expansion.py           # 1,200 words
│   ├── seed_b1_intermediate.py        # 2,000 words
│   ├── seed_b2_upper_intermediate.py  # 3,000 words
│   ├── seed_c1_advanced.py            # 2,500 words
│   └── seed_c2_mastery.py             # 500 words
├── business/
│   ├── seed_finance_payments.py       # 800 words (HIGHEST PRIORITY)
│   ├── seed_business_general.py       # 1,500 words
│   ├── seed_finance_banking.py        # 400 words
│   ├── seed_finance_accounting.py     # 300 words
│   ├── seed_business_legal.py         # 300 words
│   └── seed_business_hr.py            # 200 words
├── thematic/
│   ├── seed_food_drink.py             # 800 words
│   ├── seed_travel_transport.py       # 600 words
│   ├── seed_technology_digital.py     # 500 words
│   ├── seed_health_medical.py         # 400 words
│   ├── seed_home_housing.py           # 500 words
│   ├── seed_culture_media.py          # 400 words
│   ├── seed_sports_leisure.py         # 400 words
│   ├── seed_nature_weather.py         # 400 words
│   └── seed_emotions_social.py        # 300 words
├── specialized/
│   ├── seed_verbs_frequency.py        # 1,500 verbs
│   ├── seed_adjectives_frequency.py   # 1,000 adjectives
│   ├── seed_adverbs.py                # 400 adverbs
│   ├── seed_compound_words.py         # 600 compounds
│   ├── seed_separable_verbs.py        # 400 verbs
│   ├── seed_idioms_expressions.py     # 500 idioms
│   └── seed_modal_particles.py        # 100 particles (CRITICAL for C1)
└── utils/
    ├── bulk_insert.py                 # Performance optimization
    ├── validation.py                  # Quality assurance
    └── data_sources.py                # Reference lists
```

**Rationale for Modular Structure**:
- **Maintainability**: Each category independent
- **Quality Control**: Focused review per file
- **Incremental Deployment**: Deploy high-priority first
- **Performance**: Bulk insert with batching
- **Collaboration**: Parallel development possible

### Word Data Structure

**Required Fields**:
```python
{
    "word": str,                    # With article for nouns (der/die/das)
    "translation_it": str,
    "part_of_speech": str,          # noun, verb, adjective, adverb, etc.
    "difficulty": str,              # A1, A2, B1, B2, C1, C2
    "category": str,
    "example_de": str,
    "example_it": str,
}
```

**Recommended Fields** (80%+ coverage for B2+):
```python
{
    "pronunciation": str,           # IPA or phonetic
    "definition_de": str,           # German definition
    "usage_notes": str,             # Context and usage guidelines
}
```

**Optional Fields**:
```python
{
    "gender": str,                  # masculine/feminine/neuter (nouns only)
    "plural_form": str,
    "synonyms": List[str],
    "antonyms": List[str],
    "is_idiom": bool,
    "is_compound": bool,
    "is_separable_verb": bool,
}
```

### Quality Tiers

**Tier 1: Premium Quality (35% - 8,750 words)**
- **Who**: All business/finance (3,500) + C1-C2 (5,000) + modal particles (250)
- **Requirements**: ALL fields populated (pronunciation, definition_de, usage_notes, synonyms)
- **Review**: Hand-reviewed examples, IPA pronunciation

**Tier 2: Standard Quality (50% - 12,500 words)**
- **Who**: B1-B2 core + thematic + high-frequency
- **Requirements**: All required + pronunciation (80%+), usage notes for tricky cases

**Tier 3: Basic Quality (15% - 3,750 words)**
- **Who**: A1-A2 foundation
- **Requirements**: Required fields only, basic examples

### Master Orchestrator Script

**File**: `backend/scripts/vocabulary_seeds/seed_vocabulary_master.py`

**Key Features**:
- Import all category modules dynamically
- Validation before insertion (duplicates, completeness, CEFR distribution)
- Bulk insert with batching (1000 words/commit)
- Progress tracking and reporting
- PostgreSQL ON CONFLICT for duplicate handling
- Distribution analysis

**Usage**:
```bash
# Seed all vocabulary (25K words)
python seed_vocabulary_master.py

# Dry run (validation only, no insert)
python seed_vocabulary_master.py --dry-run

# Priority categories only (business + B2/C1)
python seed_vocabulary_master.py --priority

# Specific categories
python seed_vocabulary_master.py --categories finance_payments business_general

# Fast mode (skip validation)
python seed_vocabulary_master.py --skip-validation --batch-size 2000
```

**Code Structure**:
```python
# backend/scripts/vocabulary_seeds/seed_vocabulary_master.py

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.database import SessionLocal
from app.models.vocabulary import Vocabulary
from sqlalchemy import func

# Import all category modules
from vocabulary_seeds.business.seed_finance_payments import create_payment_vocabulary
from vocabulary_seeds.business.seed_business_general import create_business_vocabulary
# ... import all modules

from vocabulary_seeds.utils.validation import VocabularyValidator
from vocabulary_seeds.utils.bulk_insert import bulk_insert_vocabulary

# Category registry
CATEGORY_MODULES = {
    "finance_payments": create_payment_vocabulary,
    "business_general": create_business_vocabulary,
    # ... all 30+ categories
}

def seed_vocabulary_database(
    categories=None,
    dry_run=False,
    skip_validation=False,
    batch_size=1000
):
    """
    Master function to seed vocabulary from all/selected categories.
    """
    print("="*80)
    print("  VOCABULARY DATABASE SEEDING")
    print("="*80)

    # Determine categories
    selected = {k: v for k, v in CATEGORY_MODULES.items() if not categories or k in categories}

    # Generate words from modules
    all_words = []
    for category, generator in selected.items():
        words = generator()
        all_words.extend(words)
        print(f"✅ {category}: {len(words)} words")

    print(f"\n✅ Generated {len(all_words):,} words")

    # Validation
    if not skip_validation:
        validator = VocabularyValidator()
        duplicates = validator.check_duplicates(all_words)
        distribution = validator.validate_distribution(all_words)
        # ... validation logic

    if dry_run:
        return {"mode": "dry_run", "total": len(all_words)}

    # Bulk insert
    stats = bulk_insert_vocabulary(all_words, batch_size, skip_duplicates=True)

    print(f"\n✅ Inserted: {stats['inserted']:,}")
    print(f"⚠️  Skipped: {stats['skipped']:,}")

    return stats

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--categories", nargs="+")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--priority", action="store_true")
    parser.add_argument("--skip-validation", action="store_true")
    parser.add_argument("--batch-size", type=int, default=1000)

    args = parser.parse_args()

    if args.priority:
        categories = ["finance_payments", "business_general", "b2_upper_intermediate", "c1_advanced"]
        stats = seed_vocabulary_database(categories=categories, dry_run=args.dry_run)
    else:
        stats = seed_vocabulary_database(
            categories=args.categories,
            dry_run=args.dry_run,
            skip_validation=args.skip_validation,
            batch_size=args.batch_size
        )
```

### Bulk Insert Optimization

**File**: `backend/scripts/vocabulary_seeds/utils/bulk_insert.py`

**Features**:
- Batch commits (1000 words per commit)
- PostgreSQL `INSERT ... ON CONFLICT DO NOTHING` for duplicates
- Progress logging
- Error handling with rollback
- Target: <5 minutes for 25,000 words

**Code Structure**:
```python
from sqlalchemy.dialects.postgresql import insert as pg_insert
from app.database import SessionLocal
from app.models.vocabulary import Vocabulary

def bulk_insert_vocabulary(words, batch_size=1000, skip_duplicates=True):
    """Efficiently insert large vocabulary datasets."""
    db = SessionLocal()
    stats = {"inserted": 0, "skipped": 0, "errors": 0}

    try:
        for i in range(0, len(words), batch_size):
            batch = words[i:i + batch_size]

            if skip_duplicates:
                stmt = pg_insert(Vocabulary).values(batch)
                stmt = stmt.on_conflict_do_nothing(index_elements=['word'])
                result = db.execute(stmt)
                stats["inserted"] += result.rowcount
                stats["skipped"] += (len(batch) - result.rowcount)
            else:
                db.bulk_insert_mappings(Vocabulary, batch)
                stats["inserted"] += len(batch)

            db.commit()
            print(f"  Batch {i//batch_size + 1}: {stats['inserted']} total")

    except Exception as e:
        db.rollback()
        stats["errors"] += 1
        raise
    finally:
        db.close()

    return stats
```

### Validation Framework

**File**: `backend/scripts/vocabulary_seeds/utils/validation.py`

**Features**:
- Required field checks
- CEFR level validation
- Duplicate detection (case-insensitive)
- Article validation for nouns
- Example sentence contains word
- Tier-specific quality checks
- Distribution analysis (CEFR, category)

**Code Structure**:
```python
class VocabularyValidator:
    REQUIRED_FIELDS = [
        "word", "translation_it", "part_of_speech",
        "difficulty", "category", "example_de", "example_it"
    ]

    def validate_word(self, word_dict, tier="standard"):
        """Validate single word entry. Returns list of errors."""
        errors = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if not word_dict.get(field):
                errors.append(f"Missing: {field}")

        # CEFR level validation
        if word_dict.get("difficulty") not in ["A1", "A2", "B1", "B2", "C1", "C2"]:
            errors.append(f"Invalid CEFR: {word_dict.get('difficulty')}")

        # Article for nouns
        if word_dict.get("part_of_speech") == "noun":
            if not word_dict["word"].startswith(("der ", "die ", "das ")):
                errors.append("Noun missing article")

        # Example contains word
        word_lemma = word_dict["word"].split()[-1]
        if word_lemma.lower() not in word_dict.get("example_de", "").lower():
            errors.append("Example doesn't contain word")

        # Tier-specific checks
        if tier == "premium":
            if not word_dict.get("pronunciation"):
                errors.append("Premium: missing pronunciation")

        return errors

    def check_duplicates(self, words):
        """Check for duplicate words (case-insensitive)."""
        seen = set()
        duplicates = []

        for word_dict in words:
            normalized = word_dict["word"].lower()
            if normalized in seen:
                duplicates.append(word_dict["word"])
            seen.add(normalized)

        return duplicates

    def validate_distribution(self, words):
        """Analyze CEFR and category distribution."""
        levels = {"A1": 0, "A2": 0, "B1": 0, "B2": 0, "C1": 0, "C2": 0}
        categories = {}

        for word in words:
            levels[word["difficulty"]] += 1
            cat = word["category"]
            categories[cat] = categories.get(cat, 0) + 1

        return {"level_distribution": levels, "category_distribution": categories}
```

### Sample Implementation: Payment Vocabulary

**File**: `backend/scripts/vocabulary_seeds/business/seed_finance_payments.py`

**800 words organized in 10 subcategories**:
1. Payment Methods (80) - Cards, wallets, transfers
2. Transaction Processing (120) - Authorization, clearing, settlement
3. Security & Fraud (80) - Fraud detection, 3DS, encryption
4. Compliance (100) - PCI-DSS, PSD2, AML
5. Settlement & Clearing (70)
6. Payment APIs (90) - Webhooks, endpoints
7. Customer Experience (80) - Checkout, UX
8. Merchant Services (90) - Fees, chargebacks
9. Cross-Border (90) - Currency, international

**Sample Entry (Premium Quality)**:
```python
{
    "word": "die Echtzeitüberweisung",
    "translation_it": "il bonifico istantaneo",
    "part_of_speech": "noun",
    "gender": "feminine",
    "plural_form": "die Echtzeitüberweisungen",
    "difficulty": "C1",
    "category": "finance_payments",
    "example_de": "Echtzeitüberweisungen werden innerhalb von Sekunden verarbeitet.",
    "example_it": "I bonifici istantanei vengono elaborati in pochi secondi.",
    "pronunciation": "dee EKHT-tsait-ü-ber-vai-zung",
    "definition_de": "Sofortige Überweisung (SEPA Instant Payment), die in wenigen Sekunden abgewickelt wird",
    "usage_notes": "Technical term in payment processing. Also called 'Instant Payment' or 'Sofortüberweisung'. EU regulation enables 10-second transfers.",
    "synonyms": ["die Sofortüberweisung", "das Instant Payment"],
    "antonyms": ["die normale Überweisung"],
    "is_idiom": False,
    "is_compound": True,
    "is_separable_verb": False
}
```

**Code Structure**:
```python
# backend/scripts/vocabulary_seeds/business/seed_finance_payments.py

"""Payment Processing Vocabulary - 800 words (HIGHEST PRIORITY)"""

PAYMENT_METHODS = [
    {
        "word": "die Kartenzahlung",
        "translation_it": "il pagamento con carta",
        "part_of_speech": "noun",
        "gender": "feminine",
        "difficulty": "B1",
        "category": "finance_payments",
        "example_de": "Die Kartenzahlung ist die beliebteste Zahlungsmethode.",
        "example_it": "Il pagamento con carta è il metodo più popolare.",
        "pronunciation": "dee KAR-ten-tsah-lung",
        "definition_de": "Bezahlung mit Kredit- oder Debitkarte",
        "usage_notes": "Covers both credit and debit cards",
        "synonyms": ["die Zahlung per Karte"],
        "is_compound": True
    },
    # ... 79 more payment methods
]

TRANSACTION_PROCESSING = [
    # 120 processing terms
]

SECURITY_FRAUD = [
    # 80 security terms
]

# ... 7 more subcategories

def create_payment_vocabulary():
    """Generate 800 payment vocabulary words."""
    words = []
    words.extend(PAYMENT_METHODS)          # 80
    words.extend(TRANSACTION_PROCESSING)   # 120
    words.extend(SECURITY_FRAUD)           # 80
    words.extend(COMPLIANCE_REGULATIONS)   # 100
    words.extend(SETTLEMENT_CLEARING)      # 70
    words.extend(PAYMENT_APIS)             # 90
    words.extend(CUSTOMER_EXPERIENCE)      # 80
    words.extend(MERCHANT_SERVICES)        # 90
    words.extend(CROSS_BORDER)             # 90

    print(f"✅ Generated {len(words)} payment words")
    return words

if __name__ == "__main__":
    from ..utils.validation import VocabularyValidator

    words = create_payment_vocabulary()
    validator = VocabularyValidator()

    # Validate
    errors = []
    for word in words:
        word_errors = validator.validate_word(word, tier="premium")
        if word_errors:
            errors.append((word["word"], word_errors))

    if errors:
        print(f"⚠️  {len(errors)} validation errors")
    else:
        print("✅ All words valid")
```

### Database Performance

**Current Indexes** (already exist):
- `word` (for searches)
- `difficulty` (for CEFR filtering)
- `category` (for category filtering)
- `next_review_date` (for spaced repetition)

**Add Composite Index**:
```sql
CREATE INDEX idx_vocabulary_category_difficulty
ON vocabulary(category, difficulty);
```

**Performance Targets**:
- Bulk insert 25K words: <5 minutes
- Word lookup: <50ms
- Category filter query: <100ms
- Review queue query: <200ms

### Data Sources

**High-Quality German Sources**:
1. **Goethe Institut** - Official CEFR lists (A1-C2)
2. **DWDS** - Definitions, examples, frequency (dwds.de)
3. **Leipzig Corpora** - Top 25K frequency from 100M+ texts
4. **OpenThesaurus** - Synonyms/antonyms (open license)
5. **Wiktionary** - Definitions, pronunciations

**Business Sources**:
6. **Stripe Germany** - Payment glossary
7. **Handelsblatt** - Business corpus
8. **Business German textbooks** - Systematic vocabulary

**Automation Tools**:
9. **DeepL API** - Italian translations (500K free)
10. **Claude API** - Generate contextual examples
11. **spaCy German** - POS tagging

---

## Implementation Timeline

### Grammar (2-3 weeks)

**Week 1: Tier 1 Topics (8 topics, 40-48 exercises)**
- Days 1-2: Setup, Plusquamperfekt, Futur II
- Days 3-4: Conditional, Concessive
- Days 5-7: Causal, Final, Modals, Nominal style
- Output: Tier 1 complete, deployable

**Week 2: Tier 2 + 3 (10 topics, 40-56 exercises)**
- Days 1-4: Tier 2 (6 topics)
- Days 5-7: Tier 3 (4 topics)
- Output: All 18 topics complete

**Week 3: Polish & Deploy**
- Testing, documentation, deployment

### Vocabulary (10 weeks)

**Week 1: Infrastructure**
- Directory structure, utilities (bulk_insert, validation)
- Master orchestrator script
- Validation testing

**Week 2: Critical Business (3,500 words) - PRIORITY**
- Payment vocabulary (800) - **HIGHEST PRIORITY**
- Business general (1,500)
- Banking (400), Accounting (300), Legal (200)
- **Deliverable**: Immediate professional value for Igor

**Week 3-4: Core Frequency (10,000 words)**
- A1 (800), A2 (1,200), B1 (4,000), B2 (4,000)
- Semi-automated enrichment
- **Deliverable**: Strong foundation

**Week 5-6: Advanced (8,500 words)**
- C1 (5,000), C2 (3,000)
- Specialized domains
- **Deliverable**: Complete CEFR coverage

**Week 7-8: Thematic (2,500 words)**
- Food, travel, technology, health, home, culture
- **Deliverable**: Well-rounded vocabulary

**Week 9: Linguistic (1,500 words)**
- Verbs, adjectives, particles, idioms
- **Deliverable**: Natural German fluency

**Week 10: QA & Deployment**
- Validation, testing, optimization
- **Deliverable**: Production-ready 25K dataset

---

## Agent Instructions

### For Implementing Grammar Expansion

**Agent Name**: `grammar-expansion-agent`

**Task**: Implement B2/C1 business grammar expansion

**Instructions**:

1. **Phase 1: Setup (30 min)**
   - Read existing seed script: `backend/scripts/seed_grammar_data.py`
   - Read grammar models: `backend/app/models/grammar.py`
   - Create new file: `backend/scripts/seed_grammar_data_b2c1_business.py`

2. **Phase 2: Implement Tier 1 Topics (10-12 hours)**
   - For each of 8 Tier 1 topics:
     - Create topic dictionary with all fields (see sample)
     - Write German explanation (explanation_de) - comprehensive, business-focused
     - Create 5-6 exercises per topic:
       - 2 fill_blank (business context)
       - 1 multiple_choice
       - 1 translation (Italian→German)
       - 1 error_correction
       - 0-1 sentence_building
     - Ensure 50%+ business context
     - All exercises need: question, answer, explanation_de, explanation_it, hints

3. **Phase 3: Implement Tier 2 + 3 (6-8 hours)**
   - Same process for 10 additional topics
   - 4-5 exercises each

4. **Phase 4: Integration (2 hours)**
   - Complete `seed_b2c1_business_grammar()` function
   - Add all topics and exercises
   - Test locally: `python backend/scripts/seed_grammar_data_b2c1_business.py`

5. **Phase 5: Documentation (1 hour)**
   - Update `.claude/CLAUDE.md` with new stats
   - Create `docs/GRAMMAR_TOPICS_B2C1.md` listing all 18 topics

**Quality Checklist**:
- [ ] All 18 topics have German explanations
- [ ] 90-120 total exercises
- [ ] 50%+ business context
- [ ] All exercises have Italian explanations
- [ ] All exercises have 3 hints
- [ ] Script runs without errors
- [ ] Database updated correctly

**Sample Topic to Follow**: See Plusquamperfekt example in plan

**Validation**: After implementation, verify:
```bash
python backend/scripts/seed_grammar_data_b2c1_business.py
# Should print: "✅ B2/C1 BUSINESS GRAMMAR COMPLETE"
# Check database: 53 topics, 220+ exercises
```

---

### For Implementing Vocabulary Expansion

**Agent Name**: `vocabulary-expansion-agent`

**Task**: Implement 25,000-word vocabulary expansion

**Instructions**:

#### Phase 1: Infrastructure (Week 1 - 4-6 hours)

1. **Create Directory Structure**:
   ```bash
   mkdir -p backend/scripts/vocabulary_seeds/{business,core,thematic,specialized,utils}
   touch backend/scripts/vocabulary_seeds/__init__.py
   ```

2. **Create Utility Files**:
   - `utils/bulk_insert.py` - Copy structure from plan
   - `utils/validation.py` - Copy VocabularyValidator class from plan
   - `utils/data_sources.py` - Placeholder for reference lists

3. **Create Master Orchestrator**:
   - `seed_vocabulary_master.py` - Copy structure from plan
   - Add argparse for CLI usage
   - Test dry run: `python seed_vocabulary_master.py --dry-run`

#### Phase 2: Critical Business Vocabulary (Week 2 - 15-20 hours) **HIGHEST PRIORITY**

**Start Here** - Delivers immediate value for Igor's payments work

1. **Create `business/seed_finance_payments.py` (800 words)**:
   - Structure: 10 subcategories (see plan)
   - Quality tier: Premium (all fields required)
   - Data sources:
     - Stripe Germany glossary
     - Payment processor documentation
     - Financial terminology databases
   - Each word needs:
     - German word with article
     - Italian translation (use DeepL API if needed)
     - Part of speech, gender, difficulty (C1 for most)
     - German definition (definition_de)
     - Example sentences (German + Italian)
     - Pronunciation (IPA format preferred)
     - Usage notes (context, register)
     - Synonyms where applicable
     - Mark as compound word if applicable

2. **Create `business/seed_business_general.py` (1,500 words)**:
   - Meeting vocabulary
   - Email/communication terms
   - Negotiation language
   - Project management
   - Quality: Premium tier

3. **Create Additional Business Files**:
   - `business/seed_finance_banking.py` (400 words)
   - `business/seed_finance_accounting.py` (300 words)
   - `business/seed_business_legal.py` (300 words)

4. **Test Priority Deployment**:
   ```bash
   python seed_vocabulary_master.py --priority --dry-run
   # Should validate ~3,500 business words

   python seed_vocabulary_master.py --priority
   # Deploy to database
   ```

#### Phase 3: Core Frequency Vocabulary (Week 3-4 - 20-30 hours)

1. **Data Collection**:
   - Download Goethe Institut word lists (A1-B2)
   - Use Leipzig Corpora frequency lists
   - Cross-reference with DWDS dictionary

2. **Create Core Files**:
   - `core/seed_a1_foundation.py` (800 words)
   - `core/seed_a2_expansion.py` (1,200 words)
   - `core/seed_b1_intermediate.py` (4,000 words)
   - `core/seed_b2_upper_intermediate.py` (4,000 words)

3. **Semi-Automated Enrichment**:
   - Use DeepL API for Italian translations
   - Use Claude API for example sentences
   - Use spaCy for POS tagging
   - Manual review of samples

4. **Quality Tier**: Standard (required + pronunciation 80%+)

#### Phase 4: Advanced Vocabulary (Week 5-6 - 20-25 hours)

1. **Create Advanced Files**:
   - `core/seed_c1_advanced.py` (5,000 words)
   - `core/seed_c2_mastery.py` (3,000 words)

2. **Data Sources**:
   - German newspapers (FAZ, Handelsblatt)
   - Academic papers
   - Legal/technical documents

3. **Quality Tier**: Premium for C1-C2

#### Phase 5: Thematic Vocabulary (Week 7-8 - 15-20 hours)

Create 10+ thematic files (800-500 words each):
- `thematic/seed_food_drink.py`
- `thematic/seed_travel_transport.py`
- `thematic/seed_technology_digital.py`
- `thematic/seed_health_medical.py`
- (etc.)

**Quality Tier**: Standard

#### Phase 6: Linguistic Completeness (Week 9 - 10-15 hours)

1. **Create Linguistic Files**:
   - `specialized/seed_verbs_frequency.py` (1,500 verbs)
   - `specialized/seed_adjectives_frequency.py` (1,000 adj)
   - `specialized/seed_modal_particles.py` (100 particles) **CRITICAL for C1**
   - `specialized/seed_idioms_expressions.py` (500 idioms)

2. **Special Focus**: Modal particles
   - doch, mal, ja, eben, halt, schon, wohl, etwa
   - These are essential for natural German at C1 level
   - Premium quality with detailed usage notes

#### Phase 7: QA & Deployment (Week 10 - 8-10 hours)

1. **Validation**:
   ```bash
   python seed_vocabulary_master.py --dry-run
   # Check: 25,000 words, no duplicates, proper distribution
   ```

2. **Quality Sampling**:
   - Review 500 random words (2%)
   - 20 words per category
   - Verify CEFR progression

3. **Performance Testing**:
   - Benchmark bulk insert (<5 min target)
   - Test common queries (<100ms)
   - Verify indexes used correctly

4. **Deploy**:
   ```bash
   python seed_vocabulary_master.py
   # Full 25K deployment
   ```

5. **Documentation**:
   - Update `.claude/CLAUDE.md` with new statistics
   - Create `docs/VOCABULARY_25K.md` with category breakdown

**Quality Checklist**:
- [ ] 25,000 total words (+24,850 from 150)
- [ ] 64% at B2/C1 levels (16,000 words)
- [ ] 34% business/finance (8,500 words)
- [ ] Zero duplicates (case-insensitive)
- [ ] 100% validation pass rate
- [ ] All required fields populated
- [ ] 80%+ pronunciation for B2+ words
- [ ] Bulk insert <5 minutes
- [ ] Query performance <100ms

---

## Success Metrics

### Grammar
- ✅ 53 total topics (+18 new)
- ✅ 220-250 total exercises (+90-120 new)
- ✅ 50%+ business context
- ✅ 75%+ B2/C1 exercises

### Vocabulary
- ✅ 25,000 total words
- ✅ 16,000 words at B2/C1 (64%)
- ✅ 8,500 business words (34%)
- ✅ All CEFR levels covered
- ✅ 30+ categories

### Quality
- ✅ Zero duplicates
- ✅ 100% validation pass
- ✅ Premium quality for business
- ✅ All words have Italian translations

---

## Priority Deployment Strategy

**For Immediate Value** (Deploy in 2 weeks):

1. **Week 1**: Grammar Tier 1 (8 topics, 40 exercises)
2. **Week 2**: Business vocabulary (3,500 words)

This delivers the most critical content for Igor's professional needs (payments/finance vocabulary + essential B2/C1 grammar) while building toward the complete expansion.

**Commands**:
```bash
# Grammar Tier 1
python backend/scripts/seed_grammar_data_b2c1_business.py

# Business vocabulary priority
python backend/scripts/vocabulary_seeds/seed_vocabulary_master.py --priority

# Verify
psql -d german_learning -c "SELECT COUNT(*) FROM grammar_topics;"  # Should be 43+
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary WHERE category LIKE '%business%' OR category LIKE '%finance%';"  # Should be 3500+
```

---

**End of Plan**

This comprehensive plan provides everything needed to expand the German learning app content from current foundation to production-scale educational platform optimized for Igor's B2/C1 business German learning journey.
