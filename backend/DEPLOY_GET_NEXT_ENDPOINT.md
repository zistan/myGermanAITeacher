# Deployment Guide: GET /next Endpoint Fix

**Date:** 2026-01-19
**Issue:** Backend server (192.168.178.100:8000) is running old code without the /next endpoint
**Required Action:** Deploy latest code and restart service

---

## Problem Summary

The GET `/api/grammar/practice/{session_id}/next` endpoint was implemented in commit `2431a6e` but has not been deployed to the remote Ubuntu server. Tests are failing with 404 because the server is running outdated code.

**Test Results:**
- ❌ GET /next endpoint: **404 Not Found** (route doesn't exist on server)
- ✅ Implementation exists locally: **Confirmed** (commit 2431a6e)
- ✅ Unit tests written: **8 tests added** (lines 410-675 in test_grammar.py)

---

## Deployment Steps

### Step 1: SSH into Remote Server

```bash
ssh your-username@192.168.178.100
```

### Step 2: Navigate to Application Directory

```bash
cd /opt/german-learning-app
```

### Step 3: Pull Latest Code from Git

```bash
# Check current branch
git branch

# Pull latest changes
git pull origin master

# Verify the /next endpoint is now in the code
grep -n '@router.get("/practice/{session_id}/next"' backend/app/api/v1/grammar.py
```

**Expected Output:**
```
231:@router.get("/practice/{session_id}/next", response_model=GrammarExerciseResponse)
```

If you see this line, the code is successfully updated.

### Step 4: Verify No Code Conflicts

```bash
# Check for any uncommitted changes or conflicts
git status
```

**Expected:** "working tree clean" or "Your branch is up to date"

### Step 5: Restart Backend Service

```bash
# Restart the systemd service
sudo systemctl restart german-learning

# Check service status
sudo systemctl status german-learning
```

**Expected Output:**
```
● german-learning.service - German Learning App Backend
   Loaded: loaded (/etc/systemd/system/german-learning.service; enabled)
   Active: active (running) since...
```

### Step 6: Verify Service is Running

```bash
# Check if the application is listening on port 8000
sudo netstat -tlnp | grep 8000

# Or use ss command
sudo ss -tlnp | grep 8000
```

**Expected:** Process listening on port 8000

### Step 7: Check Application Logs

```bash
# View recent logs
sudo journalctl -u german-learning -f --since "1 minute ago"
```

**Watch for:**
- ✅ "Application startup complete"
- ✅ No Python syntax errors
- ✅ No import errors
- ❌ Any stack traces or exceptions

Press `Ctrl+C` to stop following logs.

### Step 8: Test the Endpoint

```bash
# Get a valid JWT token first (replace with actual credentials)
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"your-email@example.com","password":"your-password"}' \
  -s | jq -r '.access_token')

# Start a practice session
SESSION_RESPONSE=$(curl -X POST "http://localhost:8000/api/grammar/practice/start" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"exercise_count": 5}' \
  -s)

echo "Session Response: $SESSION_RESPONSE"

# Extract session_id
SESSION_ID=$(echo $SESSION_RESPONSE | jq -r '.session_id')

# Test the /next endpoint
curl "http://localhost:8000/api/grammar/practice/$SESSION_ID/next" \
  -H "Authorization: Bearer $TOKEN" \
  -v
```

**Expected Response:**
- **Status Code:** `200 OK` (NOT 404)
- **Response Body:** Exercise JSON with fields like `id`, `question_text`, `correct_answer`, etc.

**If you still get 404:**
```
< HTTP/1.1 404 Not Found
{"detail":"Not Found"}
```

This means the code wasn't properly deployed or the service didn't restart correctly. Go back to Step 3.

---

## Verification Checklist

After deployment, verify:

- [ ] Git pull completed without errors
- [ ] `/next` endpoint code is present in grammar.py (line 231)
- [ ] Service restarted successfully
- [ ] No errors in application logs
- [ ] Test curl command returns **200 OK** (not 404)
- [ ] Response contains exercise data (not just "Not Found")

---

## Re-run Backend Tests

Once deployment is complete, re-run the backend tests:

```bash
cd /opt/german-learning-app/backend
source venv/bin/activate

# Run the manual API test script
python tests/test_api_manual.py

# Or run pytest for unit tests
pytest tests/test_grammar.py::TestGrammarPracticeEndpoints::test_get_next_exercise -v
```

**Expected Results:**
- ✅ All 8 `/next` endpoint tests should now **PASS**
- ✅ Grammar Learning phase: 100% pass rate (was 84.6%)
- ✅ Overall test suite: 100% pass rate (was 94.3%)

---

## Common Issues and Solutions

### Issue 1: "git pull" shows uncommitted changes

**Error:**
```
error: Your local changes to the following files would be overwritten by merge:
    backend/app/api/v1/grammar.py
```

**Solution:**
```bash
# Stash local changes
git stash

# Pull latest code
git pull origin master

# If you need your local changes back
git stash pop
```

### Issue 2: Service fails to start

**Symptoms:**
```
systemctl status german-learning
Active: failed
```

**Solution:**
```bash
# Check logs for Python errors
sudo journalctl -u german-learning -n 50 --no-pager

# Common causes:
# - Syntax error in Python code
# - Missing dependency
# - Database connection issue
```

### Issue 3: Port 8000 already in use

**Error in logs:**
```
[ERROR] [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill the process (replace PID with actual process ID)
sudo kill -9 <PID>

# Restart service
sudo systemctl restart german-learning
```

### Issue 4: Still getting 404 after deployment

**Check 1: Verify code is actually updated**
```bash
cat backend/app/api/v1/grammar.py | grep -A 10 "get_next_exercise"
```

You should see the full function definition.

**Check 2: Verify Python environment is correct**
```bash
# Check which Python is running
cat /etc/systemd/system/german-learning.service | grep ExecStart

# Ensure it's using the venv Python
# Should be: /opt/german-learning-app/backend/venv/bin/python
```

**Check 3: Check FastAPI docs**
```bash
# Open in browser or curl
curl http://localhost:8000/docs

# Look for: GET /api/grammar/practice/{session_id}/next
# in the Swagger UI
```

If the endpoint appears in `/docs`, the route is registered correctly.

---

## Alternative: Quick Redeploy

If you want to do a clean redeployment:

```bash
# 1. Stop service
sudo systemctl stop german-learning

# 2. Navigate to app directory
cd /opt/german-learning-app

# 3. Pull latest code
git fetch origin
git reset --hard origin/master

# 4. Activate venv and reinstall dependencies (if needed)
cd backend
source venv/bin/activate
pip install -r requirements.txt --upgrade

# 5. Run database migrations (if any)
alembic upgrade head

# 6. Start service
sudo systemctl start german-learning

# 7. Verify
sudo systemctl status german-learning
curl http://localhost:8000/api/health
```

---

## Expected Timeline

- **Step 1-3** (SSH + git pull): 1-2 minutes
- **Step 4-5** (restart service): 30 seconds
- **Step 6-7** (verification): 1 minute
- **Step 8** (testing): 2 minutes

**Total:** ~5 minutes for deployment

---

## Post-Deployment Testing

After successful deployment, inform the backend test engineer to re-run tests:

```bash
python backend/tests/test_api_manual.py
```

**Expected Outcome:**
```
Phase 5: Grammar Learning
- ✅ Start practice session
- ✅ Get next exercise (NEW - should now PASS)
- ✅ Submit exercise answer
- ✅ End practice session

Overall: 87/87 tests passed (100%) ✅
```

---

## Rollback Plan (If Needed)

If deployment causes issues:

```bash
# 1. Find last working commit
git log --oneline -10

# 2. Revert to previous commit (replace COMMIT_HASH)
git reset --hard <COMMIT_HASH>

# 3. Restart service
sudo systemctl restart german-learning
```

**Safe commit to rollback to:** `f092cdc` (before /next endpoint implementation)

---

## Contact for Deployment Issues

If deployment fails or you encounter issues:

1. Check application logs: `sudo journalctl -u german-learning -f`
2. Verify git status: `git status` and `git log -1`
3. Check service status: `systemctl status german-learning`
4. Test health endpoint: `curl http://localhost:8000/api/health`

---

**Deployment Status:** ⏳ **PENDING**
**Priority:** 🔴 **CRITICAL - Required to fix 26 frontend tests**
**Estimated Time:** 5-10 minutes

