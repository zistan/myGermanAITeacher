# Timezone Fix - Deployment Guide

**Date:** 2026-01-25
**Git Commit:** ca24be1
**Migration:** 003_add_timezone_to_timestamps

---

## Problem Summary

Session completion timestamps (ended_at, completed_at) were stored in the wrong timezone across all modules:
- Grammar practice sessions
- Vocabulary quizzes and flashcards
- Conversation sessions
- All progress tracking timestamps

**Root Cause:** Database columns used `TIMESTAMP` (without timezone) instead of `TIMESTAMPTZ`. When the backend set `datetime.utcnow()` (UTC), PostgreSQL interpreted it as local server time, causing timezone offset errors.

---

## Solution Applied

**Models Updated:** All 7 model files (37 timestamp columns total)
- `TIMESTAMP` → `DateTime(timezone=True)` in SQLAlchemy models
- Results in PostgreSQL `TIMESTAMPTZ` (timestamp with time zone)

**Migration Created:** `003_add_timezone_to_timestamps.py`
- Converts all 37 timestamp columns to TIMESTAMPTZ
- Preserves existing data (PostgreSQL handles conversion)
- Includes rollback (downgrade) capability

---

## Deployment Instructions (Ubuntu Server)

### Step 1: Pull Latest Changes

```bash
# SSH to your Ubuntu server
ssh user@your-server-ip

# Navigate to project directory
cd /opt/german-learning-app

# Pull latest changes
git pull origin master

# Verify commit
git log --oneline -1
# Should show: ca24be1 fix(database): Add timezone awareness to all timestamp columns
```

### Step 2: Backup Database (IMPORTANT!)

```bash
# Create backup before migration
sudo -u postgres pg_dump german_learning > ~/backup_before_timezone_fix_$(date +%Y%m%d_%H%M%S).sql

# Verify backup created
ls -lh ~/backup_*.sql
```

### Step 3: Stop Backend Service

```bash
# Stop backend to prevent concurrent writes during migration
sudo systemctl stop german-learning

# Verify service stopped
sudo systemctl status german-learning
```

### Step 4: Run Database Migration

```bash
# Navigate to backend directory
cd /opt/german-learning-app/backend

# Activate virtual environment
source venv/bin/activate

# Check current migration status
alembic current
# Should show: 002_add_vocabulary_sessions (previous migration)

# Run the timezone migration
alembic upgrade 003_add_timezone_to_timestamps

# Verify migration succeeded
alembic current
# Should now show: 003_add_timezone_to_timestamps
```

**Expected Output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade 002_add_vocabulary_sessions -> 003_add_timezone_to_timestamps, Add timezone to all timestamp columns
```

### Step 5: Verify Database Changes

```bash
# Connect to PostgreSQL
sudo -u postgres psql german_learning

# Check that columns are now TIMESTAMPTZ
\d+ grammar_sessions

# Expected output for timestamp columns:
# Column     | Type                        | ...
# started_at | timestamp with time zone    | ...
# ended_at   | timestamp with time zone    | ...

# Check some sample data
SELECT id, started_at, ended_at,
       EXTRACT(TIMEZONE FROM started_at) as tz_offset
FROM grammar_sessions
WHERE ended_at IS NOT NULL
LIMIT 5;

# tz_offset should be 0 (UTC) for all rows
# Times should now be stored in UTC

# Exit psql
\q
```

### Step 6: Start Backend Service

```bash
# Start backend service
sudo systemctl start german-learning

# Verify service started successfully
sudo systemctl status german-learning

# Check logs for any errors
sudo journalctl -u german-learning -n 50 --no-pager
```

### Step 7: Verify Application Works

```bash
# Test health endpoint
curl http://localhost:8000/api/health
# Should return: {"status":"ok","environment":"production"}

# Test a session endpoint (get recent sessions)
# Replace TOKEN with a valid JWT token
curl http://localhost:8000/api/sessions/history \
  -H "Authorization: Bearer $TOKEN"

# Verify timestamps in response are correct
```

### Step 8: Frontend - No Changes Needed

```bash
# No frontend rebuild or deployment needed
# Frontend already handles timestamps correctly
# This is a backend/database-only fix
```

---

## Verification Tests

### Test 1: Grammar Session Timestamps

```bash
# Complete a grammar practice session in the UI
# Then check the database

sudo -u postgres psql german_learning -c "
SELECT id, user_id,
       started_at AT TIME ZONE 'UTC' as started_utc,
       ended_at AT TIME ZONE 'UTC' as ended_utc,
       (ended_at - started_at) as duration
FROM grammar_sessions
WHERE ended_at IS NOT NULL
ORDER BY ended_at DESC
LIMIT 5;
"

# Verify:
# - started_utc matches when you started the session
# - ended_utc matches when you completed it
# - duration looks reasonable (minutes, not hours off)
```

### Test 2: Vocabulary Session Timestamps

```bash
sudo -u postgres psql german_learning -c "
SELECT id, user_id,
       started_at AT TIME ZONE 'UTC' as started_utc,
       ended_at AT TIME ZONE 'UTC' as ended_utc
FROM flashcard_sessions
WHERE ended_at IS NOT NULL
ORDER BY ended_at DESC
LIMIT 5;
"

# Verify ended_utc matches actual completion time
```

### Test 3: Conversation Session Timestamps

```bash
sudo -u postgres psql german_learning -c "
SELECT id, user_id,
       started_at AT TIME ZONE 'UTC' as started_utc,
       ended_at AT TIME ZONE 'UTC' as ended_utc
FROM sessions
WHERE ended_at IS NOT NULL
ORDER BY ended_at DESC
LIMIT 5;
"

# Verify timestamps are correct
```

### Test 4: Timezone Consistency

```bash
# Verify all timestamp columns are now TIMESTAMPTZ
sudo -u postgres psql german_learning <<EOF
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
  AND data_type IN ('timestamp without time zone', 'timestamp with time zone')
ORDER BY table_name, column_name;
EOF

# Expected: ALL should be "timestamp with time zone"
# If any show "timestamp without time zone", migration didn't work
```

---

## Rollback Plan (If Issues Found)

### Option 1: Revert Migration Only

```bash
# Stop backend
sudo systemctl stop german-learning

# Rollback migration
cd /opt/german-learning-app/backend
source venv/bin/activate
alembic downgrade 002_add_vocabulary_sessions

# Start backend
sudo systemctl start german-learning
```

### Option 2: Full Rollback (Code + Database)

```bash
# Stop backend
sudo systemctl stop german-learning

# Revert code changes
cd /opt/german-learning-app
git revert ca24be1

# Rollback migration
cd backend
source venv/bin/activate
alembic downgrade 002_add_vocabulary_sessions

# Restart backend
sudo systemctl restart german-learning
```

### Option 3: Restore from Backup (Last Resort)

```bash
# Stop backend
sudo systemctl stop german-learning

# Restore database backup
sudo -u postgres psql german_learning < ~/backup_before_timezone_fix_*.sql

# Verify restoration
sudo -u postgres psql german_learning -c "
SELECT COUNT(*) FROM grammar_sessions;
"

# Restart backend
sudo systemctl start german-learning
```

---

## Post-Deployment Monitoring

### Check for Timezone-Related Errors

```bash
# Monitor backend logs for 24 hours
sudo journalctl -u german-learning -f | grep -i "timestamp\|timezone\|utc"
```

### Verify New Sessions Have Correct Timestamps

```bash
# Check timestamps of sessions created AFTER migration
sudo -u postgres psql german_learning -c "
SELECT
    'grammar' as type, COUNT(*) as count,
    MAX(started_at AT TIME ZONE 'UTC') as most_recent
FROM grammar_sessions
WHERE started_at > NOW() - INTERVAL '1 hour'
UNION ALL
SELECT
    'conversation' as type, COUNT(*) as count,
    MAX(started_at AT TIME ZONE 'UTC') as most_recent
FROM sessions
WHERE started_at > NOW() - INTERVAL '1 hour'
UNION ALL
SELECT
    'flashcard' as type, COUNT(*) as count,
    MAX(started_at AT TIME ZONE 'UTC') as most_recent
FROM flashcard_sessions
WHERE started_at > NOW() - INTERVAL '1 hour';
"
```

---

## Common Issues & Solutions

### Issue 1: Migration Fails - Column Already TIMESTAMPTZ

**Error:**
```
alembic.util.exc.CommandError: column "started_at" is already type timestamp with time zone
```

**Solution:**
Migration already ran successfully. Skip to Step 6 (restart backend).

### Issue 2: Migration Fails - Permission Denied

**Error:**
```
permission denied for table grammar_sessions
```

**Solution:**
```bash
# Ensure alembic runs with proper database user
cd /opt/german-learning-app/backend

# Check .env DATABASE_URL
cat .env | grep DATABASE_URL

# Ensure user has ALTER TABLE permissions
sudo -u postgres psql german_learning -c "
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO german_app_user;
"

# Retry migration
alembic upgrade 003_add_timezone_to_timestamps
```

### Issue 3: Timestamps Still Wrong After Migration

**Symptoms:**
Completion times still off by timezone offset

**Diagnosis:**
```bash
# Check if column type actually changed
sudo -u postgres psql german_learning -c "\d+ grammar_sessions"

# If still shows "timestamp without time zone", migration didn't apply
```

**Solution:**
```bash
# Manually run ALTER TABLE commands
sudo -u postgres psql german_learning <<EOF
ALTER TABLE grammar_sessions
ALTER COLUMN started_at TYPE TIMESTAMPTZ USING started_at AT TIME ZONE 'UTC';

ALTER TABLE grammar_sessions
ALTER COLUMN ended_at TYPE TIMESTAMPTZ USING ended_at AT TIME ZONE 'UTC';

-- Repeat for other tables if needed
EOF

# Verify changes
sudo -u postgres psql german_learning -c "\d+ grammar_sessions"
```

---

## Success Criteria

**After deployment, verify:**
- [ ] All 37 timestamp columns are `TIMESTAMPTZ` in database
- [ ] New session timestamps match actual completion time
- [ ] Backend service running without errors
- [ ] No timezone-related errors in logs
- [ ] Users can complete sessions successfully
- [ ] Timestamps display correctly in frontend (if applicable)

---

## Quick Reference Commands

### Check Migration Status
```bash
cd /opt/german-learning-app/backend && source venv/bin/activate && alembic current
```

### View Recent Sessions with Timestamps
```bash
sudo -u postgres psql german_learning -c "
SELECT id, started_at, ended_at,
       (ended_at - started_at) as duration
FROM grammar_sessions
WHERE ended_at IS NOT NULL
ORDER BY ended_at DESC
LIMIT 10;
"
```

### Check Service Status
```bash
sudo systemctl status german-learning
```

### View Logs
```bash
sudo journalctl -u german-learning -n 100 --no-pager
```

### Restart Backend
```bash
sudo systemctl restart german-learning && sudo systemctl status german-learning
```

---

## Timeline Estimate

- **Step 1-2:** 5 minutes (pull code, backup database)
- **Step 3-4:** 2 minutes (stop service, run migration)
- **Step 5:** 2 minutes (verify database changes)
- **Step 6:** 1 minute (start service)
- **Step 7-8:** 5 minutes (verify application, test endpoints)

**Total:** ~15 minutes

---

## Files Changed (8 files)

1. `backend/app/models/grammar.py` - 8 timestamp columns
2. `backend/app/models/session.py` - 3 timestamp columns
3. `backend/app/models/vocabulary.py` - 13 timestamp columns
4. `backend/app/models/user.py` - 2 timestamp columns
5. `backend/app/models/context.py` - 2 timestamp columns
6. `backend/app/models/progress.py` - 1 timestamp column
7. `backend/app/models/achievement.py` - 6 timestamp columns
8. `backend/alembic/versions/003_add_timezone_to_timestamps.py` - Migration script

**Total:** 37 timestamp columns converted to TIMESTAMPTZ

---

**Deployment Status:** 🚀 READY
**Risk Level:** LOW-MEDIUM (database schema change, but reversible)
**Downtime Required:** YES (~2 minutes during migration)
**Backup Required:** YES (mandatory before migration)

Last Updated: 2026-01-25
Git Commit: ca24be1
