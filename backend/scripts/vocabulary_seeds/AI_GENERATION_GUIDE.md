# AI-Assisted Vocabulary Generation Guide

Complete guide for generating 25,000 German vocabulary words using Claude AI.

---

## Overview

This system uses Claude Sonnet 4.5 to generate premium-quality German vocabulary entries with:
- Accurate translations (German → Italian)
- Example sentences in both languages
- Pronunciation guides
- Usage notes with real-world context
- Synonyms and antonyms
- Full validation before saving

**Estimated Time**: 3-5 hours for all 25,000 words (with automation)

**Estimated Cost**: ~$30-50 in API credits (depending on Claude pricing)

---

## Quick Start

### Prerequisites

1. **Anthropic API Key** (Already Configured ✅)

   The API key is already configured in `/backend/.env`:
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-api-key-here
   ```

   Scripts automatically read this via `os.getenv("ANTHROPIC_API_KEY")`.

   **No manual export needed** - the `.env` file is already in place.

   To verify configuration:
   ```bash
   cd /opt/german-learning-app/backend
   grep ANTHROPIC_API_KEY .env
   ```

2. **Install Dependencies**
   ```bash
   cd backend
   source venv/bin/activate  # On server
   pip install anthropic
   ```

3. **Test Installation**
   ```bash
   cd scripts/vocabulary_seeds
   python3 core/ai_generator.py --help
   ```

---

## Method 1: Generate Single Category (Manual)

### Generate Payment Methods Vocabulary (80 words)

```bash
cd backend/scripts/vocabulary_seeds

python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment methods" \
  --count 80 \
  --difficulty B2 \
  --output business/generated_payments_methods.py \
  --verbose
```

**Expected Output**:
```
============================================================
Generating 80 words for: finance / payment methods
Difficulty: B2
============================================================

Calling Claude API...
✓ Received response (45231 chars)
✓ Parsed 80 words from response
✓ Validation complete: 80 valid, 0 invalid
✓ Saved 80 words to business/generated_payments_methods.py (Python)

============================================================
✓ SUCCESS
============================================================
Generated: 80 words
Category: finance / payment methods
Output: business/generated_payments_methods.py
============================================================
```

### Review Generated File

```bash
# Check word count
grep -c '"word":' business/generated_payments_methods.py

# Preview first 3 words
head -100 business/generated_payments_methods.py
```

### Integrate into Seed Module

1. **Review generated content** for quality
2. **Copy content** into `business/seed_finance_payments.py`
3. **Run validation**:
   ```bash
   python3 master_seed.py --categories business --dry-run --verbose
   ```

---

## Method 2: Batch Generation (Automated) ⭐ RECOMMENDED

### Generate ALL Business Vocabulary (3,500 words)

```bash
cd backend/scripts/vocabulary_seeds/batches

# Generate all 32 batches (takes ~2 hours)
python3 run_batch_generation.py business_vocabulary_batches.json --verbose

# OR: Generate first 5 batches only (test run)
python3 run_batch_generation.py business_vocabulary_batches.json --only 0,1,2,3,4 --verbose

# OR: Resume from batch 10 (if previous batches done)
python3 run_batch_generation.py business_vocabulary_batches.json --start-from 10 --verbose
```

**What It Does**:
1. Reads `business_vocabulary_batches.json` (32 predefined batches)
2. Calls Claude API for each batch
3. Validates all generated words
4. Saves to `business/generated_*.py` files
5. Provides summary report

**Output Structure**:
```
business/
├── generated_payments_01_methods.py          (80 words)
├── generated_payments_02_processing.py       (120 words)
├── generated_payments_03_security.py         (80 words)
├── generated_payments_04_compliance.py       (100 words)
├── generated_payments_05_settlement.py       (70 words)
├── generated_payments_06_apis.py             (90 words)
├── generated_payments_07_checkout.py         (80 words)
├── generated_payments_08_merchant.py         (90 words)
├── generated_payments_09_international.py    (90 words)
├── generated_general_01_meetings.py          (150 words)
├── generated_general_02_email.py             (150 words)
...
└── generated_hr_03_development.py            (50 words)
```

### Consolidate Generated Files

After batch generation, consolidate into final seed modules:

```bash
# Consolidate all payment files into one
cat business/generated_payments_*.py > business/seed_finance_payments.py

# Consolidate all business general files
cat business/generated_general_*.py > business/seed_business_general.py

# Consolidate banking files
cat business/generated_banking_*.py > business/seed_finance_banking.py

# Consolidate accounting files
cat business/generated_accounting_*.py > business/seed_finance_accounting.py

# Consolidate legal files
cat business/generated_legal_*.py > business/seed_business_legal.py

# Consolidate HR files
cat business/generated_hr_*.py > business/seed_business_hr.py
```

**Manual Cleanup** (recommended):
- Remove duplicate `get_vocabulary_words()` function definitions
- Merge words arrays into single list
- Review for any duplicates or errors
- Add module docstring

---

## Method 3: Custom Categories

### Create Your Own Batch Configuration

```json
{
  "description": "Custom vocabulary batches",
  "batches": [
    {
      "name": "blockchain_crypto",
      "category": "technology",
      "subcategory": "blockchain and cryptocurrency",
      "count": 100,
      "difficulty": "C1",
      "context": "Bitcoin, Ethereum, smart contracts, DeFi, NFTs, mining",
      "output_file": "thematic/generated_blockchain.py"
    },
    {
      "name": "medical_german",
      "category": "health",
      "subcategory": "medical terminology",
      "count": 200,
      "difficulty": "C1",
      "context": "Doctors, hospitals, diagnoses, treatments, medications",
      "output_file": "thematic/generated_medical.py"
    }
  ]
}
```

### Run Custom Batches

```bash
python3 batches/run_batch_generation.py custom_batches.json --verbose
```

---

## Validation & Quality Control

### 1. Dry Run Validation

```bash
cd backend/scripts/vocabulary_seeds

# Validate business vocabulary
python3 master_seed.py --categories business --dry-run --verbose
```

**Expected Output**:
```
============================================================
STEP 1: COLLECTING WORDS
============================================================

Category: BUSINESS
============================================================
  Loading module: business.seed_finance_payments
  ✓ Loaded 800 words from business.seed_finance_payments
  Loading module: business.seed_business_general
  ✓ Loaded 1500 words from business.seed_business_general
  ...

✓ Collected 3500 words from 1 categories

============================================================
STEP 2: VALIDATION
============================================================
Valid words: 3500
Invalid words: 0
Errors: 0
Warnings: 12

✓ VALIDATION PASSED

============================================================
STATISTICS
============================================================
Total words: 3500
Duplicates: 0

CEFR Distribution:
  B1: 450 (12.9%)
  B2: 1200 (34.3%)
  C1: 1850 (52.9%)

Quality Distribution:
  premium: 3500 (100.0%)
  standard: 0 (0.0%)
  basic: 0 (0.0%)

============================================================
DRY RUN - Not inserting into database
============================================================
Would insert 3500 words
```

### 2. Check for Errors

```bash
# Find validation errors
python3 master_seed.py --categories business --dry-run 2>&1 | grep "Error"

# Count unique words
python3 -c "
from business.seed_finance_payments import get_vocabulary_words
words = get_vocabulary_words()
unique = set(w['word'] for w in words)
print(f'Total: {len(words)}, Unique: {len(unique)}, Duplicates: {len(words) - len(unique)}')
"
```

### 3. Manual Review Checklist

For each generated file, check:
- [ ] All words have German articles (der/die/das) for nouns
- [ ] Translations are accurate (spot-check with dict.cc)
- [ ] Example sentences are realistic
- [ ] Usage notes provide real-world context
- [ ] CEFR levels are appropriate
- [ ] No duplicates within file

---

## Deploy to Database

### Step 1: Test Insert (Small Batch)

```bash
# Insert only first 100 words (test)
python3 -c "
from business.seed_finance_payments import get_vocabulary_words
from core.bulk_insert import bulk_insert_vocabulary
words = get_vocabulary_words()[:100]
result = bulk_insert_vocabulary(words, verbose=True)
print(result.summary())
"
```

### Step 2: Full Deployment

```bash
# Deploy all business vocabulary
python3 master_seed.py --categories business --verbose
```

**Expected Output**:
```
============================================================
STEP 3: DATABASE INSERTION
============================================================
Current vocabulary count: 150

Processing batch 1/4 (1000 words)...
Processing batch 2/4 (1000 words)...
Processing batch 3/4 (1000 words)...
Processing batch 4/4 (500 words)...

============================================================
BULK INSERT SUMMARY
============================================================
Inserted:  3500 words
Skipped:   0 words (duplicates)
Errors:    0
Duration:  4.23 seconds
============================================================

New vocabulary count: 3650 (added 3500)

============================================================
COMPLETED
============================================================
Total duration: 6.45 seconds
✓ Vocabulary seeding completed successfully
```

### Step 3: Verify in Database

```bash
# On server (via SSH)
psql -d german_learning -c "
SELECT
  category,
  difficulty,
  COUNT(*) as count
FROM vocabulary
WHERE category IN ('finance', 'business', 'legal')
GROUP BY category, difficulty
ORDER BY category, difficulty;
"
```

**Expected Result**:
```
 category | difficulty | count
----------+------------+-------
 business | B1         |   350
 business | B2         |   800
 business | C1         |   650
 finance  | B1         |   200
 finance  | B2         |   600
 finance  | C1         |  1000
 legal    | C1         |   300
```

---

## Troubleshooting

### Issue: "No module named 'anthropic'"

**Solution**:
```bash
pip install anthropic
```

### Issue: "No API key provided"

**Root Cause**: The `/backend/.env` file is missing or doesn't contain `ANTHROPIC_API_KEY`.

**Solution**:
```bash
# Check if .env file exists and has the key
cd /opt/german-learning-app/backend
cat .env | grep ANTHROPIC_API_KEY

# If missing, add it to .env file:
echo "ANTHROPIC_API_KEY=sk-ant-your-actual-key" >> .env
chmod 600 .env  # Secure the file

# Verify it's there:
grep ANTHROPIC_API_KEY .env
```

**Note**: The API key is shared by both the backend application and vocabulary seed scripts. Both read from `/backend/.env` automatically via `os.getenv("ANTHROPIC_API_KEY")`. No need to manually export environment variables.

### Issue: "Rate limit exceeded"

**Solution**:
```bash
# Increase delay between batches
python3 batches/run_batch_generation.py business_vocabulary_batches.json --delay 5
```

### Issue: "Validation errors after generation"

**Common Causes**:
1. Missing articles for nouns → Add manually
2. Invalid CEFR level → Change to A1/A2/B1/B2/C1/C2
3. Invalid category → Use one from VALID_CATEGORIES
4. Boolean fields as strings → Change "true" to 1, "false" to 0

**Solution**:
```bash
# Review errors
python3 master_seed.py --categories business --dry-run | grep "Error"

# Fix manually in generated file
nano business/generated_payments_01_methods.py
```

### Issue: "Duplicate words across files"

**Solution**:
```bash
# Find duplicates across all business files
grep -h '"word":' business/*.py | sort | uniq -d

# Remove duplicates manually from files
```

---

## Performance & Cost Optimization

### API Usage

- **Claude Sonnet 4.5 Pricing** (as of 2026):
  - Input: $3 per million tokens
  - Output: $15 per million tokens

- **Estimated Costs**:
  - 50 words: ~3,000 tokens output → $0.045
  - 100 words: ~6,000 tokens output → $0.09
  - 3,500 words (Phase 2): ~$3-5
  - 25,000 words (all phases): ~$30-50

### Rate Limiting

- **Anthropic Rate Limits**:
  - Tier 1: 50 requests/minute, 40,000 tokens/minute
  - Tier 2: 1,000 requests/minute, 80,000 tokens/minute

- **Batch Runner Settings**:
  - Default delay: 2 seconds between batches
  - For Tier 1: Use `--delay 5`
  - For Tier 2: Use `--delay 1`

### Optimization Tips

1. **Generate in batches of 50-150 words** (optimal size)
2. **Run during off-peak hours** (if rate-limited)
3. **Use parallelization** for multiple categories:
   ```bash
   # Run 3 batch generators in parallel (different categories)
   python3 run_batch_generation.py business_batches.json &
   python3 run_batch_generation.py cefr_batches.json &
   python3 run_batch_generation.py thematic_batches.json &
   ```

---

## Next Steps

### After Phase 2 (Business Vocabulary)

1. **Create batch configs for remaining phases**:
   - `cefr_core_batches.json` (10,000 words)
   - `advanced_batches.json` (8,000 words)
   - `thematic_batches.json` (5,000 words)
   - `linguistic_batches.json` (3,200 words)

2. **Run batch generation for each phase**:
   ```bash
   python3 batches/run_batch_generation.py cefr_core_batches.json
   python3 batches/run_batch_generation.py advanced_batches.json
   python3 batches/run_batch_generation.py thematic_batches.json
   python3 batches/run_batch_generation.py linguistic_batches.json
   ```

3. **Deploy all to database**:
   ```bash
   python3 master_seed.py --all --verbose
   ```

4. **Verify final count**:
   ```bash
   psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"
   # Expected: 25,000+
   ```

---

## Summary

✅ **Infrastructure Ready** - All tools in place
✅ **AI Generator** - Claude Sonnet 4.5 integration
✅ **Batch System** - Automated generation for 3,500 business words
✅ **Validation** - Comprehensive quality checks
✅ **Documentation** - Complete usage guide

**Estimated Time to Generate All 25,000 Words**: 3-5 hours (mostly automated)

**Next Action**: Run batch generation for Phase 2 (business vocabulary)

```bash
cd backend/scripts/vocabulary_seeds/batches
python3 run_batch_generation.py business_vocabulary_batches.json --verbose
```

---

**Questions?** See `README.md` or check `.claude/CLAUDE.md` for project context.
