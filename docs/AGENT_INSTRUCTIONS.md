# Agent Instructions: Content Expansion Implementation

**Context**: German Learning App content expansion project
**Plan Document**: `docs/CONTENT_EXPANSION_PLAN.md` (read this first)
**Target**: Implement grammar expansion (18 topics) and vocabulary expansion (25,000 words)

---

## Quick Start Guide

### For Grammar Expansion Agent

**Task**: Implement 18 B2/C1 grammar topics with 90-120 exercises

**Read First**:
1. `docs/CONTENT_EXPANSION_PLAN.md` - Full plan (Part 1: Grammar Expansion)
2. `backend/scripts/seed_grammar_data.py` - Existing pattern to follow
3. `backend/app/models/grammar.py` - Database models

**Your Goal**: Create `backend/scripts/seed_grammar_data_b2c1_business.py`

**Start With**:
```bash
# 1. Read the plan
cat docs/CONTENT_EXPANSION_PLAN.md | grep -A 200 "Part 1: Grammar"

# 2. Examine existing seed script
cat backend/scripts/seed_grammar_data.py

# 3. Create new file
touch backend/scripts/seed_grammar_data_b2c1_business.py
```

**Implementation Steps**:

1. **Setup** (30 min):
   - Copy imports and database setup from existing seed script
   - Create function skeleton: `seed_b2c1_business_grammar()`

2. **Tier 1 Topics** (10-12 hours) - **START HERE**:
   - Implement 8 topics in this order:
     1. Plusquamperfekt (Pluperfect) - B2
     2. Futur II (Future Perfect) - B2
     3. Konditionalsätze (Conditionals) - B2
     4. Konzessive Sätze (Concessive) - B2
     5. Kausale/Konsekutive Sätze (Cause/Effect) - B2
     6. Finale Sätze (Purpose) - B2
     7. Modalverben in Nebensätzen - B2
     8. Nominalstil vs. Verbalstil - C1

   - For each topic:
     - Create topic dictionary (see Plusquamperfekt sample in plan)
     - Write German explanation (explanation_de) - 150-300 words, business-focused
     - Create 5-6 exercises:
       - 2× fill_blank (business context)
       - 1× multiple_choice
       - 1× translation (Italian→German)
       - 1× error_correction
       - 0-1× sentence_building
     - Ensure explanations in German AND Italian
     - Add 3 progressive hints per exercise

3. **Tier 2 + 3 Topics** (6-8 hours):
   - Implement remaining 10 topics (4-5 exercises each)
   - Same quality standards

4. **Integration** (2 hours):
   - Complete the seeding function
   - Add error handling
   - Test locally:
     ```bash
     python backend/scripts/seed_grammar_data_b2c1_business.py
     ```

5. **Validation**:
   - Check database: `SELECT COUNT(*) FROM grammar_topics;` should be 53
   - Check exercises: `SELECT COUNT(*) FROM grammar_exercises;` should be 220+
   - Verify 50%+ business context: `SELECT COUNT(*) FROM grammar_exercises WHERE context_category='business';`

**Quality Requirements**:
- ✅ German explanations (explanation_de) for all topics
- ✅ Italian explanations (explanation_it) for all exercises
- ✅ Business context 50%+
- ✅ 3 hints per exercise
- ✅ Alternative answers where applicable
- ✅ All 5 exercise types represented

**Sample to Follow**:
See "Sample Exercise Set: Plusquamperfekt" in `docs/CONTENT_EXPANSION_PLAN.md`

---

### For Vocabulary Expansion Agent

**Task**: Implement 25,000-word vocabulary expansion

**Read First**:
1. `docs/CONTENT_EXPANSION_PLAN.md` - Full plan (Part 2: Vocabulary Expansion)
2. `backend/scripts/seed_vocabulary_data.py` - Existing pattern
3. `backend/app/models/vocabulary.py` - Database model

**Your Goal**: Create modular vocabulary seed system

**Start With**:
```bash
# 1. Create directory structure
mkdir -p backend/scripts/vocabulary_seeds/{business,core,thematic,specialized,utils}
touch backend/scripts/vocabulary_seeds/__init__.py

# 2. Read the plan
cat docs/CONTENT_EXPANSION_PLAN.md | grep -A 500 "Part 2: Vocabulary"

# 3. Examine existing vocabulary model
cat backend/app/models/vocabulary.py
```

**Implementation Phases**:

#### Phase 1: Infrastructure (Week 1 - 4-6 hours) - DO THIS FIRST

Create these 3 utility files:

1. **`vocabulary_seeds/utils/validation.py`**:
   ```python
   class VocabularyValidator:
       """Validates vocabulary data quality."""
       # Copy class from plan - validates required fields, duplicates, CEFR levels
   ```

2. **`vocabulary_seeds/utils/bulk_insert.py`**:
   ```python
   def bulk_insert_vocabulary(words, batch_size=1000, skip_duplicates=True):
       """Efficiently insert vocabulary with batch commits."""
       # Copy function from plan - uses PostgreSQL ON CONFLICT
   ```

3. **`vocabulary_seeds/seed_vocabulary_master.py`**:
   ```python
   # Orchestrator script that imports all category modules
   # Copy full structure from plan
   # Supports: --dry-run, --priority, --categories flags
   ```

Test infrastructure:
```bash
python backend/scripts/vocabulary_seeds/seed_vocabulary_master.py --dry-run
# Should work without inserting any data
```

#### Phase 2: Critical Business Vocabulary (Week 2 - 15-20 hours) - **HIGHEST PRIORITY**

**Why Start Here**: Delivers immediate professional value for Igor's payments/finance work

**Create These Files in Priority Order**:

1. **`business/seed_finance_payments.py`** (800 words) - **START HERE**:
   - 10 subcategories (see plan for full breakdown):
     - Payment Methods (80 words): Kartenzahlung, Kreditkarte, Debitkarte, Echtzeitüberweisung, etc.
     - Transaction Processing (120): Transaktion, Autorisierung, Zahlungsabwicklung, Clearing, etc.
     - Security & Fraud (80): Betrugserkennung, Verschlüsselung, 3D-Secure, etc.
     - Compliance (100): PCI-DSS-Konformität, Zahlungsdiensterichtlinie (PSD2), etc.
     - Settlement & Clearing (70)
     - Payment APIs (90)
     - Customer Experience (80)
     - Merchant Services (90)
     - Cross-Border (90)

   **Data Sources**:
   - Stripe Germany glossary: https://stripe.com/de/resources/glossary
   - Adyen documentation (German)
   - Payment processor websites
   - Financial terminology databases

   **Each Word Must Have** (Premium Quality Tier):
   - `word`: German word with article (e.g., "die Kartenzahlung")
   - `translation_it`: Italian translation
   - `part_of_speech`: noun, verb, adjective, etc.
   - `gender`: masculine/feminine/neuter (for nouns)
   - `plural_form`: For nouns
   - `difficulty`: Mostly C1, some B2
   - `category`: "finance_payments"
   - `example_de`: German example sentence using the word
   - `example_it`: Italian translation of example
   - `pronunciation`: IPA or phonetic (e.g., "dee KAR-ten-tsah-lung")
   - `definition_de`: German definition
   - `usage_notes`: Context, register, when to use
   - `synonyms`: List of synonyms (if applicable)
   - `is_compound`: True for compound words
   - `is_separable_verb`: True for separable verbs

   **Structure**:
   ```python
   PAYMENT_METHODS = [
       {
           "word": "die Kartenzahlung",
           "translation_it": "il pagamento con carta",
           # ... all fields
       },
       # ... 79 more
   ]

   # ... 9 more subcategories

   def create_payment_vocabulary():
       words = []
       words.extend(PAYMENT_METHODS)
       words.extend(TRANSACTION_PROCESSING)
       # ... all subcategories
       return words
   ```

   **Use Tools**:
   - DeepL API for Italian translations (500K chars/month free)
   - Claude API for generating example sentences
   - German pronunciation dictionaries

2. **`business/seed_business_general.py`** (1,500 words):
   - Meeting vocabulary (200): Besprechung, Tagesordnung, Protokoll
   - Email/communication (300): Betreff, Anlage, mit freundlichen Grüßen
   - Negotiation (200): verhandeln, Angebot, Gegenangebot
   - Project management (300): Meilenstein, Zeitplan, Ressourcen
   - Strategy (250): Geschäftsstrategie, Wettbewerbsvorteil
   - Management (250): Geschäftsführung, Vorstand, Abteilung

3. **`business/seed_finance_banking.py`** (400 words):
   - Banking terms: Konto, Überweisung, Zinsen, Kredit

4. **`business/seed_finance_accounting.py`** (300 words):
   - Accounting: Bilanz, Gewinn-und-Verlustrechnung, Steuer

5. **`business/seed_business_legal.py`** (300 words):
   - Legal: Vertrag, Vertragsklausel, Haftung, Compliance

**Test Priority Deployment**:
```bash
# Dry run first
python vocabulary_seeds/seed_vocabulary_master.py --priority --dry-run

# Deploy business vocabulary
python vocabulary_seeds/seed_vocabulary_master.py --priority

# Verify
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary WHERE category LIKE '%finance%' OR category LIKE '%business%';"
# Should show ~3,500 words
```

#### Phase 3: Core Frequency Vocabulary (Week 3-4 - 20-30 hours)

**Data Collection**:
1. Goethe Institut word lists:
   - A1: ~800 words (most common beginners vocabulary)
   - A2: ~1,200 words
   - B1: ~2,500 words
   - B2: ~5,000 words

2. Leipzig Corpora frequency lists: https://wortschatz.uni-leipzig.de/

3. DWDS (German dictionary): https://www.dwds.de/

**Create Files**:
1. `core/seed_a1_foundation.py` (800 words)
2. `core/seed_a2_expansion.py` (1,200 words)
3. `core/seed_b1_intermediate.py` (4,000 words)
4. `core/seed_b2_upper_intermediate.py` (4,000 words)

**Quality Tier**: Standard (required fields + pronunciation 80%+)

**Semi-Automated Approach**:
```python
# Helper function for enrichment
def enrich_word_from_frequency_list(word: str, level: str):
    """Semi-automated enrichment."""
    # 1. Get Italian translation (DeepL API)
    # 2. Determine part of speech (spaCy German model)
    # 3. Generate examples (Claude API)
    # 4. Get pronunciation (German phonetic library)
    # 5. Get definition (Wiktionary API)
    return word_dict
```

#### Phase 4: Advanced Vocabulary (Week 5-6 - 20-25 hours)

**Create Files**:
1. `core/seed_c1_advanced.py` (5,000 words)
   - Abstract concepts: Ambiguität, Authentizität
   - Business strategy: Kernkompetenz, Wertschöpfungskette
   - Academic discourse markers

2. `core/seed_c2_mastery.py` (3,000 words)
   - Literary vocabulary
   - Technical jargon
   - Rare idioms

**Data Sources**:
- German newspapers: FAZ, Süddeutsche Zeitung, Handelsblatt
- Academic papers
- Legal/technical documents

**Quality Tier**: Premium for C1-C2

#### Phase 5: Thematic Vocabulary (Week 7-8 - 15-20 hours)

**Create 10+ Files** (400-800 words each):

1. `thematic/seed_food_drink.py` (800 words):
   - Ingredients: Gemüse, Obst, Fleisch, Gewürze
   - Cooking: kochen, braten, backen
   - Restaurants: Speisekarte, bestellen, Rechnung

2. `thematic/seed_travel_transport.py` (600 words):
   - Airport: Flughafen, Check-in, Boarding
   - Train: Bahnhof, Gleis, Anschluss
   - Hotel: Rezeption, Zimmer, Frühstück

3. `thematic/seed_technology_digital.py` (500 words):
   - Computers: Computer, Software, Hardware
   - Internet: Browser, Website, E-Mail

4. `thematic/seed_health_medical.py` (400 words):
   - Body parts: Kopf, Hand, Fuß
   - Symptoms: Schmerzen, Fieber, Husten
   - Doctor: Arzt, Apotheke, Medikament

5-10. Additional thematic files (see plan for full list)

**Quality Tier**: Standard

#### Phase 6: Linguistic Completeness (Week 9 - 10-15 hours)

**Create Files**:

1. `specialized/seed_verbs_frequency.py` (1,500 verbs):
   - Top 2,000 German verbs by frequency
   - Include conjugation notes in usage_notes

2. `specialized/seed_adjectives_frequency.py` (1,000 adjectives):
   - Descriptive, evaluative, emotional, technical

3. **`specialized/seed_modal_particles.py` (100 particles) - CRITICAL FOR C1**:
   - doch, mal, ja, eben, halt, schon, wohl, etwa, etc.
   - These are ESSENTIAL for natural-sounding German
   - Premium quality with extensive usage_notes
   - Example:
     ```python
     {
         "word": "doch",
         "translation_it": "ma sì / invece / però",
         "part_of_speech": "particle",
         "difficulty": "B2",
         "category": "modal_particles",
         "example_de": "Das war doch nicht so schwer, oder?",
         "example_it": "Non era poi così difficile, vero?",
         "pronunciation": "dokh",
         "definition_de": "Modalpartikel zur Verstärkung oder zum Widerspruch",
         "usage_notes": "Untranslatable particle expressing contradiction, emphasis, or appeal to shared knowledge. Critical for natural German. Usage varies by context: 1) Contradiction: 'Das stimmt doch nicht!' 2) Appeal: 'Du weißt doch...' 3) Encouragement: 'Komm doch mit!' 4) Insistence: 'Das ist doch klar!'"
     }
     ```

4. `specialized/seed_idioms_expressions.py` (500 idioms):
   - Common expressions and fixed phrases

#### Phase 7: QA & Deployment (Week 10 - 8-10 hours)

**Validation**:
```bash
# Full dry run
python seed_vocabulary_master.py --dry-run

# Check output for:
# - Total: 25,000 words
# - No duplicates
# - CEFR distribution: 64% B2/C1
# - Business: 34% (8,500 words)
```

**Quality Sampling**:
1. Review 500 random words (2%)
2. Check 20 words per category
3. Verify CEFR progression (A1 simpler than C2)
4. Validate all business vocabulary personally

**Performance Testing**:
```bash
# Measure bulk insert time
time python seed_vocabulary_master.py

# Should complete in <5 minutes
```

**Query Performance**:
```sql
-- Test common queries
EXPLAIN ANALYZE SELECT * FROM vocabulary WHERE category = 'finance_payments' AND difficulty = 'C1';
-- Should use index, <100ms

EXPLAIN ANALYZE SELECT * FROM vocabulary WHERE word ILIKE '%zahlung%';
-- Should use index, <50ms

EXPLAIN ANALYZE SELECT * FROM user_vocabulary_progress WHERE next_review_date <= NOW() AND user_id = 1;
-- Should use index, <200ms
```

**Deploy**:
```bash
# Full deployment
python seed_vocabulary_master.py

# Verify final count
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"
# Should show 25,000+ words
```

**Documentation**:
1. Update `.claude/CLAUDE.md`:
   - Grammar: 35→53 topics, 132→220+ exercises
   - Vocabulary: 150→25,000 words
   - Update all statistics

2. Create `docs/VOCABULARY_CATEGORIES.md`:
   - List all categories with word counts
   - Sample words per category
   - CEFR distribution per category

---

## Command Reference

### Grammar Commands
```bash
# Test grammar seed script
python backend/scripts/seed_grammar_data_b2c1_business.py

# Verify topics
psql -d german_learning -c "SELECT COUNT(*), difficulty_level FROM grammar_topics GROUP BY difficulty_level;"

# Verify exercises
psql -d german_learning -c "SELECT COUNT(*), context_category FROM grammar_exercises GROUP BY context_category;"
```

### Vocabulary Commands
```bash
# Dry run (validation only)
python vocabulary_seeds/seed_vocabulary_master.py --dry-run

# Priority business vocabulary
python vocabulary_seeds/seed_vocabulary_master.py --priority

# Specific categories
python vocabulary_seeds/seed_vocabulary_master.py --categories finance_payments business_general

# Full deployment
python vocabulary_seeds/seed_vocabulary_master.py

# Skip validation (faster, use after testing)
python vocabulary_seeds/seed_vocabulary_master.py --skip-validation --batch-size 2000
```

### Database Queries
```bash
# Grammar stats
psql -d german_learning -c "SELECT COUNT(*) FROM grammar_topics;"
psql -d german_learning -c "SELECT COUNT(*) FROM grammar_exercises;"

# Vocabulary stats
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"
psql -d german_learning -c "SELECT difficulty, COUNT(*) FROM vocabulary GROUP BY difficulty ORDER BY difficulty;"
psql -d german_learning -c "SELECT category, COUNT(*) FROM vocabulary GROUP BY category ORDER BY COUNT(*) DESC LIMIT 20;"
```

---

## Quality Checklist

### Grammar Expansion
- [ ] 18 new topics created (Tier 1-3)
- [ ] 90-120 new exercises
- [ ] All topics have German explanations (explanation_de)
- [ ] All exercises have Italian explanations (explanation_it)
- [ ] 50%+ exercises in business context
- [ ] All exercise types represented (fill_blank, multiple_choice, translation, error_correction, sentence_building)
- [ ] 3 hints per exercise
- [ ] Alternative answers provided where applicable
- [ ] Script runs without errors
- [ ] Database updated: 53 topics, 220+ exercises

### Vocabulary Expansion
- [ ] Directory structure created
- [ ] Infrastructure files (master, bulk_insert, validation)
- [ ] 25,000 total words (verify with SQL query)
- [ ] Zero duplicates (case-insensitive)
- [ ] CEFR distribution: 64% at B2/C1 (16,000 words)
- [ ] Business vocabulary: 34% (8,500 words)
- [ ] All required fields populated for all words
- [ ] 80%+ pronunciation coverage for B2+ words
- [ ] Premium quality for business vocabulary
- [ ] Bulk insert completes in <5 minutes
- [ ] Query performance <100ms
- [ ] Validation passes 100%

---

## Troubleshooting

### Grammar Issues

**Problem**: "Topic already exists"
```python
# Solution: Check for existing topic before insert
existing = db.query(GrammarTopic).filter(
    GrammarTopic.name_de == topic_data["name_de"]
).first()
```

**Problem**: Exercise validation fails
```python
# Solution: Ensure all required fields present
# Check: topic_id, exercise_type, difficulty_level, question_text, correct_answer
```

### Vocabulary Issues

**Problem**: Duplicate word error
```python
# Solution: Use ON CONFLICT in bulk_insert.py
stmt = pg_insert(Vocabulary).values(batch)
stmt = stmt.on_conflict_do_nothing(index_elements=['word'])
```

**Problem**: Boolean fields not working
```python
# Solution: Convert boolean to int (0/1) for database
is_compound=1 if word_data.get("is_compound") else 0
```

**Problem**: Slow bulk insert
```python
# Solution: Increase batch size, ensure indexes exist
bulk_insert_vocabulary(words, batch_size=2000)
```

---

## Success Criteria

### Minimum Viable Product (MVP)
- ✅ Grammar Tier 1 complete (8 topics, 40 exercises)
- ✅ Business vocabulary complete (3,500 words)
- ✅ Infrastructure working (master script, validation, bulk insert)

### Enhanced Success
- ✅ All 18 grammar topics (220+ exercises)
- ✅ Core vocabulary complete (A1-B2: 10,000 words)
- ✅ Advanced vocabulary (C1-C2: 8,000 words)

### Full Success
- ✅ Complete 25,000 vocabulary words
- ✅ All thematic categories
- ✅ All linguistic categories (verbs, adjectives, particles)
- ✅ Performance targets met
- ✅ Documentation updated

---

## Timeline Summary

**Week 1**: Grammar Tier 1 + Infrastructure
**Week 2**: Business vocabulary (PRIORITY - immediate value)
**Week 3-4**: Core frequency vocabulary
**Week 5-6**: Advanced vocabulary
**Week 7-8**: Thematic vocabulary
**Week 9**: Linguistic completeness
**Week 10**: QA & deployment

---

## Priority Recommendation

**Start with these in order for maximum value**:

1. **Vocabulary infrastructure** (Week 1) - Foundation for everything
2. **Payment vocabulary** (Week 2) - Highest priority for Igor's work
3. **Grammar Tier 1** (Week 1) - Essential B2/C1 topics
4. **Business vocabulary** (Week 2) - Complete professional coverage

This delivers immediate professional value while building toward complete expansion.

---

## Support & Resources

**Reference Files**:
- `docs/CONTENT_EXPANSION_PLAN.md` - Complete detailed plan
- `backend/scripts/seed_grammar_data.py` - Existing grammar pattern
- `backend/scripts/seed_vocabulary_data.py` - Existing vocabulary pattern
- `.claude/CLAUDE.md` - Current project status

**Data Sources**:
- Goethe Institut: https://www.goethe.de/
- DWDS: https://www.dwds.de/
- Leipzig Corpora: https://wortschatz.uni-leipzig.de/
- DeepL: https://www.deepl.com/pro-api
- Stripe Germany: https://stripe.com/de/resources/glossary

**Database Models**:
- `backend/app/models/grammar.py`
- `backend/app/models/vocabulary.py`

---

**End of Agent Instructions**

This document provides complete step-by-step instructions for implementing the content expansion. Follow the phases in order, starting with infrastructure and high-priority business content for immediate value.