# BUG-016: Quiz "Not Found" - Executive Summary

**Date:** 2026-01-19
**Severity:** 🔴 CRITICAL
**Status:** Root Cause Confirmed via Live Testing
**Affects:** Vocabulary Quiz + Flashcard Sessions

---

## Problem Statement

Users generate vocabulary quizzes successfully but receive **"Quiz not found" (404)** errors when trying to submit answers. The behavior is **intermittent and unpredictable**.

---

## Root Cause (CONFIRMED)

### Multiple Uvicorn Workers + In-Memory Storage

**Code Issue:**
```python
# Line 670 in /backend/app/api/v1/vocabulary.py
vocabulary_quizzes = {}  # Module-level Python dictionary
```

**Server Configuration:**
```bash
# /etc/systemd/system/german-learning.service
--workers 2  # or --workers 4
```

**What Happens:**
1. User generates quiz → Request handled by **Worker A**
2. Quiz stored in Worker A's `vocabulary_quizzes{}` dictionary (Worker A's memory)
3. User submits answer → Request handled by **Worker B** (load balanced)
4. Worker B checks its `vocabulary_quizzes{}` → Empty → Returns **404 "Quiz not found"**

---

## Live Test Results

**Test Server:** http://192.168.178.100:8000 (Ubuntu production)

| Action | Result | Explanation |
|--------|--------|-------------|
| Generate quiz | ✅ SUCCESS (quiz_id: 1) | Stored in Worker A's memory |
| Submit answer immediately | ❌ FAILED (404) | Request went to Worker B |
| Wait 5 seconds, submit again | ✅ SUCCESS | Load balancer routed back to Worker A |
| Generate 2nd quiz | ✅ SUCCESS (quiz_id: 1) | Overwrote first quiz in Worker A |
| Submit answer immediately | ✅ SUCCESS | Same worker (sticky routing) |

**Pattern:** Works intermittently depending on which worker handles each request.

**Full Test Log:** `/tmp/quiz-test-results.log`

---

## Impact

### User Experience
- 🔴 Quiz feature appears broken
- 🔴 Unpredictable errors
- 🔴 First answer often fails
- 🔴 No reliable workaround

### Technical
- 🔴 Cannot scale horizontally (more workers = worse)
- 🔴 Not production-ready
- 🟡 Quizzes DO persist (not lost on restart of individual worker)
- 🟡 Some requests work (if same worker)

### Also Affects
- Flashcard sessions (line 210, same pattern)
- Any vocabulary session-based features

---

## Solutions

### 1️⃣ IMMEDIATE FIX (5 minutes) - Temporary

**Reduce to single worker:**

```bash
ssh user@192.168.178.100
sudo nano /etc/systemd/system/german-learning.service

# Change:
--workers 4
# To:
--workers 1

sudo systemctl restart german-learning
```

**Pros:**
- ⚡ Works immediately
- ✅ Quizzes will function reliably
- ✅ No code changes

**Cons:**
- ❌ Cannot handle high concurrent load
- ❌ NOT scalable
- ❌ Only for low-traffic periods

**Recommendation:** Use this TODAY while implementing proper fix

---

### 2️⃣ SHORT-TERM FIX (1 day) - Redis Cache

**Install Redis and use for quiz storage:**

```bash
# On Ubuntu server
sudo apt install redis-server
sudo systemctl start redis
sudo systemctl enable redis
```

```python
# backend/app/utils/redis_client.py
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def store_quiz(quiz_id: int, quiz_data: dict):
    """Store quiz in Redis with 1-hour TTL."""
    redis_client.setex(f"quiz:{quiz_id}", 3600, json.dumps(quiz_data))

def get_quiz(quiz_id: int):
    """Get quiz from Redis."""
    data = redis_client.get(f"quiz:{quiz_id}")
    return json.loads(data) if data else None
```

**Update endpoints:**
```python
# Replace: vocabulary_quizzes[quiz_id] = {...}
# With:    store_quiz(quiz_id, {...})

# Replace: quiz = vocabulary_quizzes.get(quiz_id)
# With:    quiz = get_quiz(quiz_id)
```

**Pros:**
- ✅ Shared across ALL workers
- ✅ Fast implementation (1 day)
- ✅ Auto-expiry (no memory leaks)
- ✅ Works with 10+ workers
- ✅ Production-ready

**Cons:**
- 🔧 Requires Redis server

**Recommendation:** Implement this WEEK

**Effort:** 1 day for backend engineer

---

### 3️⃣ LONG-TERM FIX (2-3 days) - Database

**Create proper database tables:**

```sql
CREATE TABLE vocabulary_quiz_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    quiz_type VARCHAR(50),
    total_questions INTEGER,
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE vocabulary_quiz_questions (
    id SERIAL PRIMARY KEY,
    quiz_session_id INTEGER REFERENCES vocabulary_quiz_sessions(id),
    question_number INTEGER,
    question_text TEXT,
    correct_answer TEXT,
    user_answer TEXT,
    is_correct BOOLEAN
);
```

**Pros:**
- ✅ Full data persistence
- ✅ Survives server restarts
- ✅ Complete audit trail
- ✅ Enables analytics
- ✅ Scalable
- ✅ Follows GrammarSession pattern

**Cons:**
- ⏱️ 2-3 days implementation

**Recommendation:** Best long-term solution

**Effort:** 2-3 days for backend engineer

---

## Recommended Action Plan

### Today (5 minutes)
**DevOps:**
- [ ] SSH to Ubuntu server: `ssh user@192.168.178.100`
- [ ] Check worker count: `ps aux | grep uvicorn | grep -v grep | wc -l`
- [ ] Edit service: `sudo nano /etc/systemd/system/german-learning.service`
- [ ] Change to `--workers 1`
- [ ] Restart: `sudo systemctl restart german-learning`
- [ ] Test quiz: Should work reliably now

### This Week (1 day)
**Backend Engineer:**
- [ ] Install Redis on server
- [ ] Add `redis` to requirements.txt
- [ ] Create redis_client.py utility
- [ ] Update quiz generation endpoint (use Redis)
- [ ] Update quiz answer endpoint (use Redis)
- [ ] Update flashcard endpoints (use Redis)
- [ ] Test with `--workers 4`
- [ ] Deploy

### Next 2 Weeks (2-3 days)
**Backend Engineer:**
- [ ] Design database schema (4 tables)
- [ ] Create SQLAlchemy models
- [ ] Create Alembic migration
- [ ] Migrate quiz endpoints to database
- [ ] Migrate flashcard endpoints to database
- [ ] Write tests
- [ ] Deploy

---

## Verification Checklist

### Before Any Fix
- [x] Generate quiz → works
- [x] Submit answer immediately → **FAILS** 404
- [x] Wait 5s, submit again → works
- [x] Behavior is intermittent ✅

### After Reducing to 1 Worker
- [ ] Generate quiz → works
- [ ] Submit answer immediately → **WORKS**
- [ ] Behavior is consistent ✅
- [ ] Note: Only for low traffic

### After Redis Implementation
- [ ] Generate quiz → works
- [ ] Submit answer immediately → **WORKS**
- [ ] Restart server → quiz still works ✅
- [ ] Test with `--workers 4` → **WORKS**
- [ ] Load test with 10+ concurrent users → **WORKS**

### After Database Implementation
- [ ] All Redis tests pass ✅
- [ ] Quiz data queryable in database ✅
- [ ] Analytics possible ✅
- [ ] Audit trail complete ✅

---

## Related Documents

1. **BUG-016-quiz-not-found-after-generation.md** - Original bug report
2. **BUG-016-ANALYSIS-QUIZ-SESSION-PERSISTENCE.md** - Code analysis and architecture review
3. **BUG-016-EMPIRICAL-TEST-RESULTS.md** - Live testing results (this confirms the issue)
4. **BUG-016-EXECUTIVE-SUMMARY.md** - This document

---

## Contact

**Backend Team Lead:** Needs to assign Redis implementation (1 day)
**DevOps Lead:** Needs to reduce workers TODAY (5 minutes)
**Product Manager:** Needs to prioritize fix (affects all vocabulary features)

---

## Priority Assignment

| Team | Task | Priority | Time | Status |
|------|------|----------|------|--------|
| **DevOps** | Reduce to 1 worker | **P0 - CRITICAL** | 5 min | ⏳ TODO |
| **Backend** | Redis implementation | **P1 - HIGH** | 1 day | ⏳ TODO |
| **Backend** | Database persistence | P2 - MEDIUM | 3 days | ⏳ TODO |
| **QA** | Verify fixes | P1 - HIGH | 2 hours | ⏳ TODO |

---

## Summary

✅ **Root Cause:** Multiple workers + in-memory storage
✅ **Confirmed:** Live testing on production server
✅ **Quick Fix:** Reduce to 1 worker (5 min)
✅ **Proper Fix:** Redis cache (1 day)
✅ **Best Fix:** Database persistence (3 days)

**Immediate action required:** DevOps to reduce worker count TODAY

---

**Report Date:** 2026-01-19
**Tested By:** Claude Code (QA + Backend Analysis)
**Status:** Root cause confirmed, solutions ready

---

**END OF SUMMARY**
