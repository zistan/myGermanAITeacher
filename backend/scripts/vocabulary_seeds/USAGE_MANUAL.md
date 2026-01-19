# Vocabulary Generation System - Usage Manual

**Complete guide for generating and deploying German vocabulary using AI**

Version: 1.0
Last Updated: 2026-01-19

---

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Quick Start (5 Minutes)](#quick-start-5-minutes)
4. [Detailed Workflows](#detailed-workflows)
5. [Common Tasks](#common-tasks)
6. [Troubleshooting](#troubleshooting)
7. [Reference](#reference)

---

## Overview

This system generates German vocabulary words using Claude AI (Anthropic). It creates premium-quality entries with translations, examples, pronunciation, and usage notes.

### What You Get

Each generated word includes 14 fields:
- German word with article (e.g., "die Überweisung")
- Italian translation
- Example sentences (German + Italian)
- Pronunciation guide
- Usage notes with real-world context
- Synonyms and antonyms
- CEFR difficulty level (A1-C2)

### Capacity

- **Manual Mode**: Generate 10-200 words at a time
- **Batch Mode**: Generate 3,500+ words automatically
- **Full System**: Can generate all 25,000 words (~20 hours total)

### Cost

- **Claude API**: ~$3-5 per 1,000 words
- **Phase 2 (Business)**: ~$10-15 for 3,500 words
- **All 25,000 words**: ~$30-50 total

---

## Prerequisites

### 1. Server Access

You need SSH access to the Ubuntu server where the application is deployed:

```bash
ssh your-username@your-server-ip
```

### 2. API Key

Get an Anthropic API key from: https://console.anthropic.com/

**Note**: Keep this key secret! Never commit it to Git.

### 3. Python Environment

The system requires:
- Python 3.10+
- `anthropic` package
- Virtual environment activated

---

## Quick Start (5 Minutes)

### Step 1: Setup (One-Time)

```bash
# SSH to server
ssh your-username@your-server-ip

# Navigate to project
cd /opt/german-learning-app

# Pull latest code
git pull origin master

# Activate virtual environment
cd backend
source venv/bin/activate

# Install anthropic package
pip install anthropic

# Set API key (replace with your actual key)
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"
```

**💡 Tip**: Add the API key to your `~/.bashrc` to make it permanent:
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### Step 2: Test (2 Minutes)

Generate 10 test words to verify everything works:

```bash
cd scripts/vocabulary_seeds

python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment methods" \
  --count 10 \
  --output test_output.py \
  --verbose
```

**Expected Output**:
```
============================================================
Generating 10 words for: finance / payment methods
============================================================
Calling Claude API...
✓ Received response
✓ Parsed 10 words from response
✓ Validation complete: 10 valid, 0 invalid
✓ Saved 10 words to test_output.py

✓ SUCCESS
============================================================
```

### Step 3: Review Test Output

```bash
# View generated words
cat test_output.py

# Count words
grep -c '"word":' test_output.py
# Should show: 10
```

### Step 4: Validate

```bash
# Test validation (ensures words are correct)
python3 -c "
import sys
sys.path.insert(0, '.')
from test_output import get_vocabulary_words
from core.validation import VocabularyValidator

words = get_vocabulary_words()
validator = VocabularyValidator(verbose=True)
result = validator.validate_words(words)

print(result.summary())
print('\n✓ All words valid!' if result.is_valid() else '\n✗ Errors found')
"
```

**✅ If you see "All words valid!", the system is working correctly!**

---

## Detailed Workflows

### Workflow A: Generate Small Batches (Manual Mode)

**Use Case**: Generate 50-100 words for a specific topic

#### Example: Generate 80 Payment Method Words

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds

python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment methods" \
  --count 80 \
  --difficulty B2 \
  --output business/payments_methods.py \
  --verbose
```

**Parameters**:
- `--category`: finance, business, legal, technology, health, etc.
- `--subcategory`: Describe what you want (e.g., "credit cards", "bank accounts")
- `--count`: Number of words (10-200 recommended)
- `--difficulty`: A1, A2, B1, B2, C1, C2, or "mixed"
- `--output`: Where to save the file
- `--verbose`: Show detailed progress

**Time**: ~1-2 minutes for 80 words

#### Review Generated Words

```bash
# Preview first 50 lines
head -50 business/payments_methods.py

# Count words
grep -c '"word":' business/payments_methods.py

# Search for specific word
grep -A 15 '"word": "die Kreditkarte"' business/payments_methods.py
```

---

### Workflow B: Batch Generation (Automated Mode) ⭐ RECOMMENDED

**Use Case**: Generate 3,500 business words automatically

#### Step 1: Review Batch Configuration

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds/batches

# View batch configuration
cat business_vocabulary_batches.json | python3 -m json.tool | head -50
```

This file contains 32 pre-configured batches:
- Batch 0-8: Finance/payments (800 words)
- Batch 9-18: Business general (1,500 words)
- Batch 19-21: Banking (400 words)
- Batch 22-24: Accounting (300 words)
- Batch 25-27: Legal (300 words)
- Batch 28-31: HR (200 words)

#### Step 2: Run Test Batch (First Batch Only)

```bash
# Generate only batch 0 (80 words - payment methods)
python3 run_batch_generation.py \
  business_vocabulary_batches.json \
  --only 0 \
  --verbose
```

**Time**: ~2 minutes
**Output**: `business/generated_payments_01_methods.py`

#### Step 3: Review Test Batch

```bash
# Check if file was created
ls -lh ../business/generated_payments_01_methods.py

# Count words
grep -c '"word":' ../business/generated_payments_01_methods.py
# Should show: ~80

# Preview content
head -100 ../business/generated_payments_01_methods.py
```

#### Step 4: Run Full Batch Generation

If test batch looks good, generate all 32 batches:

```bash
python3 run_batch_generation.py \
  business_vocabulary_batches.json \
  --verbose
```

**Time**: ~2-3 hours (32 batches × ~3-5 minutes each)
**Output**: 32 files in `business/generated_*.py`

**💡 Tip**: Run this in a `screen` or `tmux` session so it continues if your SSH connection drops:

```bash
# Start screen session
screen -S vocab_gen

# Run batch generation
python3 run_batch_generation.py business_vocabulary_batches.json --verbose

# Detach from screen: Press Ctrl+A, then D

# Later, reattach to check progress:
screen -r vocab_gen
```

#### Step 5: Monitor Progress

If running in background, check progress:

```bash
# Count generated files
ls -1 ../business/generated_*.py | wc -l
# Shows how many batches completed

# Check last generated file
ls -lt ../business/generated_*.py | head -5

# View summary of latest file
tail -20 ../business/generated_payments_09_international.py
```

---

### Workflow C: Resume Interrupted Generation

If batch generation stops (network issue, timeout, etc.), resume from where it left off:

```bash
# Check which batches are done
ls -1 ../business/generated_*.py | sort

# Example: If batches 0-9 are done, resume from batch 10
python3 run_batch_generation.py \
  business_vocabulary_batches.json \
  --start-from 10 \
  --verbose
```

---

## Common Tasks

### Task 1: Consolidate Generated Files

After batch generation, merge multiple files into final seed modules:

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds/business

# Consolidate payment files (batches 0-8)
cat generated_payments_*.py > seed_finance_payments_generated.py

# Consolidate business general files (batches 9-18)
cat generated_general_*.py > seed_business_general_generated.py

# Consolidate banking files (batches 19-21)
cat generated_banking_*.py > seed_finance_banking_generated.py

# Consolidate accounting files (batches 22-24)
cat generated_accounting_*.py > seed_finance_accounting_generated.py

# Consolidate legal files (batches 25-27)
cat generated_legal_*.py > seed_business_legal_generated.py

# Consolidate HR files (batches 28-31)
cat generated_hr_*.py > seed_business_hr_generated.py
```

**⚠️ Important**: These consolidated files will have duplicate `get_vocabulary_words()` function definitions. You need to manually clean them:

```bash
# Edit each file and keep only ONE get_vocabulary_words() function
nano seed_finance_payments_generated.py

# Manually:
# 1. Delete duplicate function definitions
# 2. Merge all words arrays into one list
# 3. Keep only one return statement
```

**Better Approach**: Use a helper script (see Task 8 below)

---

### Task 2: Validate Generated Vocabulary

Before deploying to database, validate all words:

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds

# Dry run validation (no database changes)
python3 master_seed.py --categories business --dry-run --verbose
```

**Expected Output**:
```
============================================================
STEP 1: COLLECTING WORDS
============================================================
Category: BUSINESS
  ✓ Loaded 800 words from business.seed_finance_payments
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

CEFR Distribution:
  B1: 450 (12.9%)
  B2: 1200 (34.3%)
  C1: 1850 (52.9%)

Quality Distribution:
  premium: 3500 (100.0%)
```

**If Errors Found**:
```
✗ VALIDATION FAILED - 15 errors found

First 10 errors:
  - Word #45 'Zahlung': Missing required field 'gender'
  - Word #67 'Transaktion': Invalid difficulty 'B3'. Must be one of: A1, A2, B1, B2, C1, C2
  ...
```

Fix errors manually in the generated files and re-validate.

---

### Task 3: Deploy to Database

After validation passes, insert words into database:

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds

# Check current count
python3 -c "
from core.bulk_insert import get_vocabulary_count
print(f'Current vocabulary count: {get_vocabulary_count()}')
"

# Deploy business vocabulary
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

✓ Vocabulary seeding completed successfully
```

---

### Task 4: Verify Database Deployment

```bash
# Check total count
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"

# Check by category
psql -d german_learning -c "
SELECT category, COUNT(*) as count
FROM vocabulary
GROUP BY category
ORDER BY count DESC;
"

# Check by difficulty
psql -d german_learning -c "
SELECT difficulty, COUNT(*) as count
FROM vocabulary
GROUP BY difficulty
ORDER BY difficulty;
"

# View sample words
psql -d german_learning -c "
SELECT word, category, difficulty
FROM vocabulary
WHERE category = 'finance'
ORDER BY RANDOM()
LIMIT 10;
"
```

---

### Task 5: Generate Custom Category

Want to generate vocabulary for a topic not in the batch configuration?

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds

# Example: Generate blockchain terminology
python3 core/ai_generator.py \
  --category technology \
  --subcategory "blockchain and cryptocurrency" \
  --count 100 \
  --difficulty C1 \
  --context "Bitcoin, Ethereum, smart contracts, DeFi, NFTs, mining, wallets" \
  --output thematic/blockchain_crypto.py \
  --verbose
```

**Parameters Explained**:
- `--context`: Additional context to guide AI generation (optional but helpful)
- Helps Claude understand what specific terms you want

---

### Task 6: Export to JSON (for Review)

If you want to review words in JSON format before converting to Python:

```bash
python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment APIs" \
  --count 50 \
  --format json \
  --output review_apis.json \
  --verbose

# Review JSON
cat review_apis.json | python3 -m json.tool | less

# Convert to Python later if approved
python3 core/ai_generator.py \
  --category finance \
  --subcategory "payment APIs" \
  --count 50 \
  --format python \
  --output business/seed_payment_apis.py
```

---

### Task 7: Check Generation Costs

Monitor API usage to estimate costs:

```bash
# Count total generated words
find business/ -name "generated_*.py" -exec grep -c '"word":' {} \; | \
  awk '{s+=$1} END {print "Total words generated:", s}'

# Estimate cost (rough calculation)
# Formula: words × 6 tokens/word × $0.015/1000 tokens ≈ $0.09/1000 words
python3 -c "
words = 3500  # Replace with your actual count
cost_per_1000 = 0.09
total_cost = (words / 1000) * cost_per_1000
print(f'Estimated cost for {words} words: \${total_cost:.2f}')
"
```

---

### Task 8: Auto-Consolidate Files (Helper Script)

Create a helper script to merge files automatically:

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds

# Create consolidation script
cat > consolidate.sh << 'EOF'
#!/bin/bash

# Consolidate payment files
echo "Consolidating payment files..."
python3 -c "
import glob
import json

all_words = []
for file in sorted(glob.glob('business/generated_payments_*.py')):
    exec(open(file).read())
    all_words.extend(get_vocabulary_words())

# Write consolidated file
with open('business/seed_finance_payments.py', 'w') as f:
    f.write('\"\"\"Finance and payments vocabulary (800 words).\"\"\"\\n\\n')
    f.write('from typing import List\\n')
    f.write('from ..core.data_format import VocabularyWord\\n\\n\\n')
    f.write('def get_vocabulary_words() -> List[VocabularyWord]:\\n')
    f.write('    \"\"\"Get finance/payments vocabulary.\"\"\"\\n')
    f.write('    words = ' + json.dumps(all_words, indent=4, ensure_ascii=False) + '\\n\\n')
    f.write('    return words\\n')

print(f'✓ Consolidated {len(all_words)} payment words')
"

# Repeat for other categories...
echo "Done!"
EOF

chmod +x consolidate.sh
./consolidate.sh
```

---

### Task 9: Clean Up Generated Files

After consolidation, optionally remove individual generated files:

```bash
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds/business

# Backup first
mkdir -p ../backup
cp generated_*.py ../backup/

# Remove individual files (keep consolidated only)
rm generated_payments_*.py
rm generated_general_*.py
rm generated_banking_*.py
rm generated_accounting_*.py
rm generated_legal_*.py
rm generated_hr_*.py

# Or keep them for reference
# (They don't affect the system, master_seed.py loads from seed_*.py files only)
```

---

### Task 10: Update Progress Tracking

Update `.claude/CLAUDE.md` after successful deployment:

```bash
cd /opt/german-learning-app

# Edit CLAUDE.md
nano .claude/CLAUDE.md

# Update vocabulary count from 150 to 3,650
# Update Phase 2 status to: ✅ Complete

# Commit update
git add .claude/CLAUDE.md
git commit -m "docs: Update vocabulary count to 3,650 (Phase 2 complete)"
git push origin master
```

---

## Troubleshooting

### Problem: "No module named 'anthropic'"

**Cause**: anthropic package not installed

**Solution**:
```bash
pip install anthropic

# If that doesn't work, try:
pip3 install anthropic

# Or with explicit version:
pip install anthropic==0.34.0
```

---

### Problem: "No API key provided"

**Cause**: ANTHROPIC_API_KEY environment variable not set

**Solution**:
```bash
# Check if key is set
echo $ANTHROPIC_API_KEY

# If empty, set it:
export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"

# Make it permanent (add to ~/.bashrc):
echo 'export ANTHROPIC_API_KEY="sk-ant-your-actual-key-here"' >> ~/.bashrc
source ~/.bashrc
```

**Test**:
```bash
# Verify key is set
python3 -c "import os; print('✓ Key is set' if os.getenv('ANTHROPIC_API_KEY') else '✗ Key not set')"
```

---

### Problem: "Rate limit exceeded"

**Cause**: Too many API calls too quickly (Anthropic rate limits)

**Solution**:
```bash
# Increase delay between batches (default is 2 seconds)
python3 run_batch_generation.py \
  business_vocabulary_batches.json \
  --delay 5 \
  --verbose

# For Tier 1 API accounts, use --delay 10
```

---

### Problem: "Validation errors after generation"

**Cause**: AI-generated words don't meet validation requirements

**Common Validation Errors**:

1. **Missing gender for nouns**
   ```
   Error: Word #45 'Zahlung': Noun missing gender field
   ```
   **Fix**: Edit file, add `"gender": "feminine"` for "die Zahlung"

2. **Invalid CEFR level**
   ```
   Error: Word #67: Invalid difficulty 'B3'. Must be one of: A1, A2, B1, B2, C1, C2
   ```
   **Fix**: Change `"difficulty": "B3"` to `"difficulty": "B2"`

3. **Boolean as string**
   ```
   Error: Field 'is_compound' must be 0 or 1, got: "true"
   ```
   **Fix**: Change `"is_compound": "true"` to `"is_compound": 1`

4. **Missing article for noun**
   ```
   Error: Noun should include article (der/die/das)
   ```
   **Fix**: Change `"word": "Zahlung"` to `"word": "die Zahlung"`

**How to Fix**:
```bash
# 1. Note which file has errors (from validation output)
# 2. Edit file
nano business/generated_payments_01_methods.py

# 3. Find and fix errors
# 4. Save and re-validate
python3 master_seed.py --categories business --dry-run
```

---

### Problem: "Duplicate words found"

**Cause**: Same word generated multiple times across different batches

**Solution**:
```bash
# Find duplicates
cd business
grep -h '"word":' generated_*.py | sort | uniq -d

# Example output:
# "word": "die Zahlung",
# "word": "die Überweisung",

# Manually remove duplicates from one of the files
nano generated_payments_02_processing.py
# Delete the duplicate entry
```

---

### Problem: "JSON parsing error"

**Cause**: Claude's response includes markdown or extra text

**Example Error**:
```
✗ Error parsing JSON: Expecting value: line 1 column 1 (char 0)
Response preview: Here are the vocabulary words you requested:

```json
[
  ...
```

**Solution**: The script usually handles this automatically. If it doesn't:

```bash
# Run with --verbose to see raw response
python3 core/ai_generator.py ... --verbose

# Manually copy JSON from response and save to file
nano manual_words.json
# Paste JSON array, save

# Validate JSON
python3 -m json.tool < manual_words.json

# Convert to Python
python3 -c "
import json
with open('manual_words.json') as f:
    words = json.load(f)

with open('output.py', 'w') as f:
    f.write('from typing import List\\n')
    f.write('from ..core.data_format import VocabularyWord\\n\\n')
    f.write('def get_vocabulary_words() -> List[VocabularyWord]:\\n')
    f.write('    words = ' + json.dumps(words, indent=4, ensure_ascii=False) + '\\n')
    f.write('    return words\\n')
"
```

---

### Problem: "Database insertion fails"

**Cause**: Database connection issue or permission problem

**Check Database**:
```bash
# Test database connection
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"

# If connection fails, check .env file
cat /opt/german-learning-app/backend/.env | grep DATABASE_URL
```

**Check Permissions**:
```bash
# Ensure vocabulary table exists
psql -d german_learning -c "\d vocabulary"

# Check if you can insert
psql -d german_learning -c "
INSERT INTO vocabulary (word, translation_it, part_of_speech, difficulty, category, example_de, example_it)
VALUES ('test', 'test', 'noun', 'A1', 'daily', 'test', 'test')
ON CONFLICT (word) DO NOTHING
RETURNING id;
"
```

---

### Problem: "Screen session lost"

**Cause**: SSH disconnected or server rebooted

**Solution**:
```bash
# List all screen sessions
screen -ls

# Reattach to session
screen -r vocab_gen

# If session doesn't exist, check if process is still running
ps aux | grep run_batch_generation

# Check last generated file to see where it stopped
ls -lt backend/scripts/vocabulary_seeds/business/generated_*.py | head -5

# Resume from last completed batch
cd /opt/german-learning-app/backend/scripts/vocabulary_seeds/batches
python3 run_batch_generation.py business_vocabulary_batches.json --start-from 15
```

---

## Reference

### File Structure

```
vocabulary_seeds/
├── core/
│   ├── ai_generator.py          # AI generation tool
│   ├── validation.py            # Validation system
│   ├── bulk_insert.py           # Database insertion
│   └── data_format.py           # Type definitions
├── batches/
│   ├── business_vocabulary_batches.json   # 32 batch configs
│   └── run_batch_generation.py            # Batch runner
├── business/
│   ├── generated_*.py           # AI-generated files (32 files)
│   ├── seed_finance_payments.py           # Final consolidated
│   ├── seed_business_general.py
│   ├── seed_finance_banking.py
│   ├── seed_finance_accounting.py
│   ├── seed_business_legal.py
│   └── seed_business_hr.py
├── master_seed.py               # Main deployment tool
├── README.md                    # System overview
├── AI_GENERATION_GUIDE.md       # Technical guide
├── TEST_GENERATION.md           # Testing guide
└── USAGE_MANUAL.md             # This file
```

### Command Reference

#### Generate Single Category
```bash
python3 core/ai_generator.py \
  --category <category> \
  --subcategory "<description>" \
  --count <number> \
  --difficulty <level> \
  --output <filename> \
  --verbose
```

#### Run Batch Generation
```bash
python3 batches/run_batch_generation.py <config.json> [options]

Options:
  --verbose              Show detailed progress
  --start-from <N>       Resume from batch N
  --only <N,M,P>         Generate only specific batches
  --delay <seconds>      Delay between API calls (default: 2)
```

#### Validate Words
```bash
python3 master_seed.py --categories <category> --dry-run [--verbose]
```

#### Deploy to Database
```bash
python3 master_seed.py --categories <category> [--verbose]
```

### Categories

Valid categories:
- `finance` - Banking, payments, accounting
- `business` - General business, management, strategy
- `legal` - Contracts, compliance, law
- `technology` - IT, software, digital
- `daily` - Everyday vocabulary
- `food` - Food and dining
- `travel` - Transportation, tourism
- `health` - Medical, wellness
- `sports` - Sports and hobbies
- `home` - Housing, furniture
- `education` - School, learning
- `environment` - Nature, ecology
- `culture` - Arts, society
- `politics` - Government, policy

### CEFR Levels

- `A1` - Beginner (200-400 words)
- `A2` - Elementary (400-800 words)
- `B1` - Intermediate (1,200-2,000 words)
- `B2` - Upper Intermediate (2,500-3,500 words)
- `C1` - Advanced (5,000+ words)
- `C2` - Mastery (8,000+ words)
- `mixed` - Distribution across all levels (recommended for most batches)

### Quality Tiers

- **Premium**: All 14 fields populated (business, C1-C2, modal particles)
- **Standard**: 8+ fields (B1-B2, thematic)
- **Basic**: 7 required fields (A1-A2)

---

## Quick Reference Card

### Setup (One-Time)
```bash
export ANTHROPIC_API_KEY="sk-ant-your-key"
pip install anthropic
```

### Generate 10 Test Words
```bash
python3 core/ai_generator.py --category finance --subcategory "payments" --count 10 --output test.py --verbose
```

### Generate All Business Vocabulary (3,500 words)
```bash
python3 batches/run_batch_generation.py business_vocabulary_batches.json --verbose
```

### Validate Before Deploying
```bash
python3 master_seed.py --categories business --dry-run --verbose
```

### Deploy to Database
```bash
python3 master_seed.py --categories business --verbose
```

### Check Database
```bash
psql -d german_learning -c "SELECT COUNT(*) FROM vocabulary;"
```

---

## Support

### Documentation Files
- **This Manual**: `USAGE_MANUAL.md` - Practical usage guide
- **Technical Guide**: `AI_GENERATION_GUIDE.md` - Detailed technical documentation
- **Testing Guide**: `TEST_GENERATION.md` - Testing procedures
- **System Overview**: `README.md` - Infrastructure overview

### Getting Help

1. **Check Troubleshooting** section above
2. **Review error messages** - most are self-explanatory
3. **Validate data** before deploying
4. **Test with small batches** first (10-50 words)
5. **Check API key** if authentication fails

### Best Practices

✅ **DO**:
- Test with 10 words before generating large batches
- Run batch generation in `screen` or `tmux`
- Validate with `--dry-run` before deploying
- Back up generated files before consolidating
- Review quality of first few batches manually
- Monitor API costs periodically

❌ **DON'T**:
- Generate 1,000+ words in a single call (slow, expensive)
- Skip validation before database deployment
- Commit API keys to Git
- Run batch generation without screen/tmux on unreliable networks
- Deploy without reviewing at least sample outputs

---

**End of Manual**

Version: 1.0
Last Updated: 2026-01-19
Author: Claude Sonnet 4.5

For questions or issues, refer to the technical documentation or project README.
