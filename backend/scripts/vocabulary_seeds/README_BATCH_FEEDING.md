# Batch Content Feeding System

**Continuous batch generation of vocabulary and grammar content with intelligent gap analysis and deduplication.**

## Overview

The Batch Content Feeding System enables **continuous, automated scaling** of vocabulary and grammar content from current levels (150 words, 200 exercises) to target levels (25,000 words, 5,000 exercises) with conservative daily limits to minimize AI costs.

### Key Features

- ✅ **Conservative Daily Limits**: 50 words/day, 25 exercises/day (configurable)
- ✅ **Intelligent Gap Analysis**: Prioritizes content generation based on category gaps and CEFR distribution
- ✅ **Smart Deduplication**: Queries database before generating to minimize redundant AI calls
- ✅ **Both Fill & Create**: Fills exercises for existing topics AND creates new grammar topics
- ✅ **CEFR B2-C1 Heavy**: Distribution targets user's learning level (B2: 30%, C1: 25%)
- ✅ **Complete Audit Trail**: JSON logs track all batch executions with detailed metrics
- ✅ **Manual Execution**: User controls when batches run (optional cron scheduling)

### Architecture

```
batch_feed.py (CLI)
    ↓
UnifiedBatchFeeder
    ├── VocabularyBatchFeeder
    │   ├── VocabularyGapAnalyzer → Recommend next batch
    │   ├── VocabularyDeduplicator → Filter duplicates
    │   ├── VocabularyGenerator (AI) → Generate words
    │   └── VocabularyInserter → Bulk insert to DB
    │
    └── GrammarBatchFeeder
        ├── GrammarGapAnalyzer → Recommend topics/exercises
        ├── GrammarTopicGenerator (AI) → Create new topics
        ├── GrammarAIService → Generate exercises
        ├── GrammarDeduplicator → Filter duplicates
        └── Database → Insert topics/exercises

BatchExecutionTracker (persistent JSON logs)
    └── Enforce daily/weekly/global caps
```

---

## Quick Start

### 1. Setup Environment Variables

Add batch feeding configuration to `/backend/.env`:

```bash
# Vocabulary Batch Limits
BATCH_VOCAB_MAX_WORDS_PER_RUN=50
BATCH_VOCAB_MAX_WORDS_TOTAL=25000
BATCH_VOCAB_CHUNK_SIZE=40

# Grammar Batch Limits
BATCH_GRAMMAR_MAX_EXERCISES_PER_RUN=25
BATCH_GRAMMAR_MAX_EXERCISES_TOTAL=5000
BATCH_GRAMMAR_TARGET_PER_TOPIC=50
BATCH_GRAMMAR_MAX_NEW_TOPICS_PER_RUN=2

# AI Rate Limiting
BATCH_AI_CALLS_PER_MINUTE=20
BATCH_AI_RETRY_DELAY_SECONDS=5
BATCH_AI_MAX_RETRIES=3

# Daily/Weekly Caps (Conservative)
BATCH_DAILY_CAP_WORDS=50
BATCH_DAILY_CAP_EXERCISES=25
BATCH_WEEKLY_CAP_WORDS=200
BATCH_WEEKLY_CAP_EXERCISES=100

# Deduplication
BATCH_VOCAB_CHECK_EXISTING=true
BATCH_VOCAB_SIMILARITY_THRESHOLD=0.85
BATCH_GRAMMAR_CHECK_DUPLICATES=true

# Execution Tracking
BATCH_EXECUTION_LOG_PATH=logs/batch_execution.json
BATCH_HISTORY_RETENTION_DAYS=90

# Content Priority (B2-C1 Heavy)
BATCH_VOCAB_PRIORITY_CATEGORIES=business,cefr_core
BATCH_VOCAB_CEFR_DISTRIBUTION=A1:5,A2:10,B1:20,B2:30,C1:25,C2:10

# Grammar Priority
BATCH_GRAMMAR_PRIORITY_CATEGORIES=cases,verbs,tenses
BATCH_GRAMMAR_MISSING_TOPICS=subjunctive,passive_voice,indirect_speech
```

### 2. Run Your First Batch

```bash
cd /opt/german-learning-app/backend
source venv/bin/activate
cd scripts/vocabulary_seeds

# Check current status
python batch_feed.py --status

# Analyze gaps
python batch_feed.py --gaps

# Execute vocabulary batch
python batch_feed.py --vocabulary --verbose

# Execute grammar batch
python batch_feed.py --grammar --verbose

# Execute both
python batch_feed.py --both --verbose
```

### 3. Monitor Progress

```bash
# View execution history
python batch_feed.py --history

# Check configuration
python batch_feed.py --config

# View status after execution
python batch_feed.py --status
```

---

## Command Reference

### Execution Commands

```bash
# Execute vocabulary batch only
python batch_feed.py --vocabulary [--verbose]

# Execute grammar batch only
python batch_feed.py --grammar [--verbose]

# Execute both batches (default)
python batch_feed.py --both [--verbose]

# Force execution (bypass caps) - USE WITH CAUTION
python batch_feed.py --both --force --verbose
```

### Monitoring Commands

```bash
# Show current status (today/week/global progress, cap enforcement)
python batch_feed.py --status

# Show gap analysis (vocabulary categories, CEFR distribution, incomplete grammar topics)
python batch_feed.py --gaps

# Show execution history (last 10 batch runs)
python batch_feed.py --history

# Show current configuration (all environment variables)
python batch_feed.py --config
```

---

## Configuration Reference

### Vocabulary Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `BATCH_VOCAB_MAX_WORDS_PER_RUN` | 50 | Max new words per batch execution |
| `BATCH_VOCAB_MAX_WORDS_TOTAL` | 25000 | Global cap (stop when reached) |
| `BATCH_VOCAB_CHUNK_SIZE` | 40 | Words per AI call (chunking) |

### Grammar Limits

| Variable | Default | Description |
|----------|---------|-------------|
| `BATCH_GRAMMAR_MAX_EXERCISES_PER_RUN` | 25 | Max exercises per batch |
| `BATCH_GRAMMAR_MAX_EXERCISES_TOTAL` | 5000 | Global cap |
| `BATCH_GRAMMAR_TARGET_PER_TOPIC` | 50 | Target exercises per topic |
| `BATCH_GRAMMAR_MAX_NEW_TOPICS_PER_RUN` | 2 | Max new topics to create per run |

### Daily/Weekly Caps

| Variable | Default | Description |
|----------|---------|-------------|
| `BATCH_DAILY_CAP_WORDS` | 50 | Daily vocabulary limit |
| `BATCH_DAILY_CAP_EXERCISES` | 25 | Daily grammar limit |
| `BATCH_WEEKLY_CAP_WORDS` | 200 | Weekly vocabulary limit |
| `BATCH_WEEKLY_CAP_EXERCISES` | 100 | Weekly grammar limit |

**Cap Hierarchy:** Daily < Weekly < Global. System enforces the strictest limit.

### Deduplication

| Variable | Default | Description |
|----------|---------|-------------|
| `BATCH_VOCAB_CHECK_EXISTING` | true | Query DB before generating |
| `BATCH_VOCAB_SIMILARITY_THRESHOLD` | 0.85 | Fuzzy match threshold (0.0-1.0) |
| `BATCH_GRAMMAR_CHECK_DUPLICATES` | true | Check for similar exercises |

**Fuzzy Matching Algorithm:**
- Normalizes German words (removes articles, lowercase)
- Uses `difflib.SequenceMatcher` for similarity ratio
- Threshold 0.85 means 85% similarity triggers duplicate flag

### Content Priority

**CEFR Distribution (B2-C1 Heavy for Advanced Learner):**
```
A1: 5%   (Foundation)
A2: 10%  (Basic)
B1: 20%  (Intermediate)
B2: 30%  (Upper Intermediate) ← User's primary level
C1: 25%  (Advanced) ← User's target level
C2: 10%  (Mastery)
```

**Priority Categories:**
- **Vocabulary**: `business,cefr_core` (aligned with user's payment/finance domain)
- **Grammar**: `cases,verbs,tenses` (core German grammar)

---

## Scheduling with Cron (Optional)

### Manual Setup

The batch feeding system supports manual cron scheduling. Here are recommended cron patterns:

**Example 1: Run every 6 hours**
```bash
0 */6 * * * cd /opt/german-learning-app/backend && source venv/bin/activate && python scripts/vocabulary_seeds/batch_feed.py --both >> logs/batch_cron.log 2>&1
```

**Example 2: Daily at 2 AM**
```bash
0 2 * * * cd /opt/german-learning-app/backend && source venv/bin/activate && python scripts/vocabulary_seeds/batch_feed.py --both >> logs/batch_cron.log 2>&1
```

**Example 3: Twice daily (morning and evening)**
```bash
0 8,20 * * * cd /opt/german-learning-app/backend && source venv/bin/activate && python scripts/vocabulary_seeds/batch_feed.py --both >> logs/batch_cron.log 2>&1
```

**Example 4: Weekdays only at 10 PM**
```bash
0 22 * * 1-5 cd /opt/german-learning-app/backend && source venv/bin/activate && python scripts/vocabulary_seeds/batch_feed.py --both >> logs/batch_cron.log 2>&1
```

### Setup Instructions

1. Edit crontab:
   ```bash
   crontab -e
   ```

2. Add one of the cron patterns above

3. Save and exit

4. Verify cron job:
   ```bash
   crontab -l
   ```

5. Monitor cron execution:
   ```bash
   tail -f /opt/german-learning-app/backend/logs/batch_cron.log
   ```

**Note:** Daily/weekly caps will still be enforced even with cron scheduling. If caps are reached, the batch will exit gracefully with "skipped" status.

---

## Execution Workflow

### Vocabulary Batch Workflow

```
1. Load configuration from .env
2. Check daily/weekly/global caps
   ├─ If caps reached → Exit with "skipped"
   └─ If caps OK → Continue
3. Analyze gaps (category gaps + CEFR distribution)
4. Recommend next batch (e.g., "business, B2, 50 words")
5. Query existing words from database (deduplication)
6. Generate vocabulary using Claude AI (with chunking)
7. Filter duplicates (fuzzy matching + exact matching)
8. Validate words (schema validation)
9. Bulk insert to database
10. Log execution to JSON file
11. Return results
```

### Grammar Batch Workflow

```
1. Load configuration from .env
2. Check daily/weekly/global caps
   ├─ If caps reached → Exit with "skipped"
   └─ If caps OK → Continue
3. Analyze gaps
   ├─ Get incomplete topics (< 50 exercises)
   └─ Get missing topics (from config)
4. Decide action:
   ├─ If incomplete topics exist → Fill exercises
   └─ If all complete → Create new topic
5. Execute action:
   ├─ Fill Exercises:
   │   ├─ Query existing exercises (deduplication)
   │   ├─ Generate exercises using Claude AI
   │   ├─ Filter duplicates
   │   └─ Insert to database
   └─ Create Topic:
       ├─ Generate topic metadata using Claude AI
       ├─ Create topic in database
       ├─ Generate initial 20 exercises
       └─ Insert exercises
6. Log execution to JSON file
7. Return results
```

---

## Cost Estimation

### Conservative Mode (Default - Recommended)

**Daily Limits:**
- Vocabulary: 50 words/day
- Grammar: 25 exercises/day

**Monthly Cost:**
- Vocabulary: 1,500 words × ~500 tokens/word = 750,000 tokens
- Grammar: 750 exercises × ~300 tokens/exercise = 225,000 tokens
- **Total**: ~975,000 tokens/month ≈ **$15-30/month**

**Timeline to Target:**
- 25,000 words: ~16 months
- 5,000 exercises: ~6 months

### Moderate Mode (If Needed Later)

**Daily Limits:**
- Vocabulary: 200 words/day (4x)
- Grammar: 100 exercises/day (4x)

**Monthly Cost:**
- **Total**: ~4 million tokens/month ≈ **$60-120/month**

**Timeline to Target:**
- 25,000 words: ~4 months
- 5,000 exercises: ~1.5 months

**To Enable Moderate Mode:**
```bash
# Update .env
BATCH_DAILY_CAP_WORDS=200
BATCH_DAILY_CAP_EXERCISES=100
BATCH_WEEKLY_CAP_WORDS=800
BATCH_WEEKLY_CAP_EXERCISES=400
```

---

## Troubleshooting

### Issue: "Daily cap reached" message

**Cause:** Today's batch execution already generated the maximum allowed content.

**Solution:**
- Wait until tomorrow for caps to reset (caps are per-day)
- OR increase daily caps in `.env` (will increase costs)
- OR use `--force` flag to bypass caps (not recommended)

```bash
# Check current status
python batch_feed.py --status

# Force execution (use sparingly)
python batch_feed.py --both --force --verbose
```

### Issue: "No gaps found" message

**Cause:** All targets are met (all topics have 50+ exercises, distribution is balanced).

**Solution:**
- Increase targets in `.env`:
  ```bash
  BATCH_VOCAB_MAX_WORDS_TOTAL=50000  # Increase from 25000
  BATCH_GRAMMAR_MAX_EXERCISES_TOTAL=10000  # Increase from 5000
  BATCH_GRAMMAR_TARGET_PER_TOPIC=100  # Increase from 50
  ```
- Add more missing topics:
  ```bash
  BATCH_GRAMMAR_MISSING_TOPICS=subjunctive,passive_voice,indirect_speech,relative_clauses,modal_verbs
  ```

### Issue: High duplicate rate (>50%)

**Cause:** Similarity threshold too strict OR category already has many words.

**Solution:**
- Adjust similarity threshold:
  ```bash
  BATCH_VOCAB_SIMILARITY_THRESHOLD=0.90  # Stricter (from 0.85)
  ```
- Focus on different categories (check gap analysis)

### Issue: AI generation fails

**Cause:** Invalid API key, rate limits, or network issues.

**Solution:**
1. Check API key in `.env`:
   ```bash
   grep ANTHROPIC_API_KEY backend/.env
   ```

2. Test API connection:
   ```bash
   curl -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     https://api.anthropic.com/v1/messages
   ```

3. Check rate limits:
   ```bash
   # Reduce calls per minute
   BATCH_AI_CALLS_PER_MINUTE=10  # From 20
   ```

### Issue: Database insertion fails

**Cause:** Database connection lost, constraint violations, or schema mismatches.

**Solution:**
1. Check database connection:
   ```bash
   psql $DATABASE_URL -c "SELECT COUNT(*) FROM vocabulary;"
   ```

2. Check logs:
   ```bash
   tail -f logs/batch_cron.log
   ```

3. Check execution history for errors:
   ```bash
   python batch_feed.py --history
   cat logs/batch_execution.json | jq '.executions[-1].results.errors'
   ```

### Issue: Execution log file corrupted

**Cause:** JSON file corruption (rare, but possible if process killed mid-write).

**Solution:**
The system automatically backs up corrupted logs:
```bash
# Check for backups
ls -la logs/batch_execution.json.backup.*

# Restore from backup if needed
cp logs/batch_execution.json.backup.YYYYMMDD_HHMMSS logs/batch_execution.json
```

---

## Monitoring & Analytics

### Key Metrics to Track

**Execution Logs (`logs/batch_execution.json`):**
```json
{
  "execution_id": "vocab_20260123_143022",
  "timestamp": "2026-01-23T14:30:22Z",
  "type": "vocabulary",
  "status": "completed",
  "results": {
    "generated": 48,
    "inserted": 45,
    "skipped_duplicates": 3,
    "ai_calls": 2,
    "duration_seconds": 45.2
  },
  "daily_totals": {"words": 45, "exercises": 0},
  "weekly_totals": {"words": 145, "exercises": 58}
}
```

**Key Performance Indicators:**
- **Success Rate**: % of executions with `status: "completed"`
- **Duplicate Rate**: `skipped_duplicates / generated` (target: <10%)
- **Average Duration**: Mean `duration_seconds` (target: <2 minutes)
- **AI Efficiency**: `words_generated / ai_calls` (target: 35-40 words/call)

### Query Execution Logs

```bash
# Show all executions
cat logs/batch_execution.json | jq '.executions'

# Show today's executions
cat logs/batch_execution.json | jq '.executions[] | select(.timestamp | startswith("2026-01-23"))'

# Calculate success rate
cat logs/batch_execution.json | jq '.executions | [.[] | select(.status == "completed")] | length'

# Show errors
cat logs/batch_execution.json | jq '.executions[] | select(.results.errors | length > 0) | {id: .execution_id, errors: .results.errors}'
```

---

## Advanced Usage

### Custom Gap Analysis

Analyze gaps programmatically:

```python
from core.batch_config import BatchConfig
from gap_analysis.vocabulary_gaps import VocabularyGapAnalyzer
from gap_analysis.grammar_gaps import GrammarGapAnalyzer
from app.database import SessionLocal

config = BatchConfig.load()
db = SessionLocal()

# Vocabulary gaps
vocab_analyzer = VocabularyGapAnalyzer(db, config)
gaps = vocab_analyzer.analyze_category_gaps()
recommendation = vocab_analyzer.recommend_next_batch(50)

# Grammar gaps
grammar_analyzer = GrammarGapAnalyzer(db, config)
topic_gaps = grammar_analyzer.analyze_topic_gaps()
recommendations = grammar_analyzer.recommend_next_topics(5)

db.close()
```

### Custom Batch Execution

Run batches programmatically:

```python
from core.batch_config import BatchConfig
from batch_jobs.unified_feeder import UnifiedBatchFeeder
from app.database import SessionLocal

config = BatchConfig.load()
db = SessionLocal()

feeder = UnifiedBatchFeeder(db, config)
results = feeder.execute(mode="both", force=False)

print(f"Vocabulary: {results['vocabulary']['status']}")
print(f"Grammar: {results['grammar']['status']}")

db.close()
```

---

## File Structure

```
backend/scripts/vocabulary_seeds/
├── batch_feed.py                       # CLI entry point
├── README_BATCH_FEEDING.md            # This file
│
├── core/                               # Core components
│   ├── batch_config.py                # Configuration management
│   ├── batch_tracker.py               # Execution tracking
│   ├── deduplicator.py                # Deduplication engine
│   ├── ai_generator.py                # Vocabulary AI generator (existing)
│   ├── bulk_insert.py                 # Database bulk insertion (existing)
│   └── validation.py                  # Validation logic (existing)
│
├── gap_analysis/                       # Gap detection
│   ├── vocabulary_gaps.py             # Vocabulary gap analyzer
│   ├── grammar_gaps.py                # Grammar gap analyzer
│   └── grammar_topic_generator.py     # New topic generator (AI)
│
└── batch_jobs/                         # Orchestration
    ├── vocabulary_feeder.py           # Vocabulary workflow
    ├── grammar_feeder.py              # Grammar workflow
    └── unified_feeder.py              # Combined workflow
```

---

## FAQ

**Q: Can I run batches in parallel?**
A: No, batch execution should be sequential to avoid race conditions in cap tracking.

**Q: What happens if I run out of missing topics?**
A: The system will log "No gaps found" and exit gracefully. Add more topics to `BATCH_GRAMMAR_MISSING_TOPICS`.

**Q: Can I change caps while batches are running?**
A: Yes, config is loaded at execution start. Changes take effect on next batch run.

**Q: How do I reset daily caps manually?**
A: Caps reset automatically at midnight (system time). To force reset, edit `logs/batch_execution.json` and remove today's entries (not recommended).

**Q: What's the minimum daily cap?**
A: Technically 1 word/exercise, but recommended minimum is 10 for efficiency.

**Q: Can I skip deduplication to speed up batches?**
A: Yes, set `BATCH_VOCAB_CHECK_EXISTING=false`, but this will increase costs due to redundant AI calls.

---

## Support

For issues or questions about the batch feeding system:

1. Check execution logs: `cat logs/batch_execution.json | jq '.executions[-1]'`
2. Run diagnostics: `python batch_feed.py --status --gaps`
3. Review this documentation
4. Check GitHub issues: https://github.com/zistan/myGermanAITeacher/issues

---

**Last Updated**: 2026-01-23
**Version**: 1.0
