# Frontend Troubleshooting Guide

## ERR_CONNECTION_REFUSED - Backend Not Running

**Error in browser console:**
```
POST http://localhost:8000/api/v1/auth/register net::ERR_CONNECTION_REFUSED
```

### Cause
The frontend cannot connect to the backend API server. This means:
1. Backend server is not running, OR
2. Backend is running on a different port, OR
3. Firewall is blocking the connection

### Solution: Start the Backend

#### Step 1: Check if Backend is Running

**On Ubuntu (or where backend should be running):**
```bash
# Check if port 8000 is in use
sudo lsof -i :8000
# or
netstat -tulpn | grep 8000

# Check for uvicorn process
ps aux | grep uvicorn
```

**Expected result if running:**
```
python    12345  user  5u  IPv4  123456  0t0  TCP *:8000 (LISTEN)
```

**If nothing shows up:** Backend is NOT running.

#### Step 2: Start the Backend

**Terminal 1: Start Backend**

```bash
# Navigate to repository root
cd /opt/myGermanAITeacher

# Go to backend directory
cd backend

# Activate virtual environment
source venv/bin/activate

# You should see (venv) in your prompt
# (venv) user@ubuntu:/opt/myGermanAITeacher/backend$

# Start the backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/opt/myGermanAITeacher/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

#### Step 3: Verify Backend is Accessible

**From Ubuntu terminal:**
```bash
curl http://localhost:8000/api/health
```

**Expected response:**
```json
{"status":"healthy"}
```

**If you get connection refused:** Backend still not running properly.

#### Step 4: Check from Windows (if running Ubuntu remotely)

**In Windows PowerShell or CMD:**
```powershell
# Replace with your Ubuntu server IP
curl http://192.168.1.100:8000/api/health
```

**Expected response:**
```json
{"status":"healthy"}
```

#### Step 5: Update Frontend .env if Backend is on Different Host

**If backend is on Ubuntu server (not localhost):**

```bash
# On your Ubuntu machine where frontend is running
cd /opt/myGermanAITeacher/frontend

# Edit .env file
nano .env
```

**Update to your Ubuntu server IP:**
```bash
# Change from:
VITE_API_BASE_URL=http://localhost:8000

# To (replace with your actual IP):
VITE_API_BASE_URL=http://192.168.1.100:8000
```

**After changing .env, restart frontend:**
```bash
# Stop frontend (Ctrl+C)
# Start again
npm run dev
```

#### Step 6: Try Registration Again

1. Open browser: `http://localhost:5173/register`
2. Fill the form
3. Click "Create Account"
4. Check browser DevTools console (F12) for errors

## Common Scenarios

### Scenario 1: Both Frontend & Backend on Same Ubuntu Machine

**Configuration:**
- Backend: Ubuntu at `http://localhost:8000`
- Frontend: Ubuntu at `http://localhost:5173`
- Browser: On Ubuntu (Firefox/Chrome)

**Frontend .env:**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

### Scenario 2: Backend on Ubuntu, Frontend on Ubuntu, Browser on Windows

**Configuration:**
- Backend: Ubuntu at IP `192.168.1.100:8000`
- Frontend: Ubuntu at IP `192.168.1.100:5173`
- Browser: Windows accessing `http://192.168.1.100:5173`

**Frontend .env:**
```bash
VITE_API_BASE_URL=http://192.168.1.100:8000
```

**Start frontend with --host:**
```bash
npm run dev -- --host
```

### Scenario 3: Backend on Ubuntu, Frontend on Windows

**Configuration:**
- Backend: Ubuntu at IP `192.168.1.100:8000`
- Frontend: Windows at `http://localhost:5173`
- Browser: Windows

**Frontend .env:**
```bash
VITE_API_BASE_URL=http://192.168.1.100:8000
```

## Verify Current Setup

### Check Backend

```bash
# SSH to Ubuntu
ssh user@192.168.1.100

# Check backend is running
curl http://localhost:8000/api/health

# Should return: {"status":"healthy"}
```

### Check Frontend .env

```bash
# On machine running frontend
cd /opt/myGermanAITeacher/frontend
cat .env

# Should show correct backend URL
```

### Check from Browser

**Open browser DevTools (F12):**
1. Go to **Network** tab
2. Try to register
3. Look at the failed request
4. Check **Request URL** - is it correct?
5. Check **Status** - what error?

**Common issues:**
- `ERR_CONNECTION_REFUSED` → Backend not running
- `404 Not Found` → Wrong API endpoint
- `CORS error` → Backend CORS not configured
- `500 Internal Server Error` → Backend crashed (check logs)

## Backend Logs

**Check backend terminal for errors:**
```
# Look for:
ERROR:    Exception in ASGI application
Traceback (most recent call last):
...
```

**Common backend issues:**
- Database not running (PostgreSQL)
- Missing environment variables
- Port 8000 already in use
- Python dependencies missing

## Database Check

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# If not running:
sudo systemctl start postgresql

# Test database connection
psql -U german_app_user -d german_learning -c "SELECT 1;"
```

## Port Conflicts

**If port 8000 is already in use:**

```bash
# Find what's using port 8000
sudo lsof -i :8000

# Kill the process
sudo kill -9 <PID>

# Or use a different port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

# Update frontend .env:
VITE_API_BASE_URL=http://localhost:8001
```

## Complete Restart Procedure

**When nothing works, restart everything:**

```bash
# 1. Stop everything
pkill -f uvicorn  # Kill backend
pkill -f vite     # Kill frontend

# 2. Start backend
cd /opt/myGermanAITeacher/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Wait for: "Application startup complete"

# 3. Test backend
curl http://localhost:8000/api/health

# 4. Start frontend (new terminal)
cd /opt/myGermanAITeacher/frontend
npm run dev

# 5. Access browser
# http://localhost:5173
```

## CORS Issues

**Error in browser console:**
```
Access to XMLHttpRequest at 'http://localhost:8000/api/v1/auth/register'
from origin 'http://localhost:5173' has been blocked by CORS policy
```

**Fix: Update backend CORS settings**

```bash
# Edit backend/.env
nano /opt/myGermanAITeacher/backend/.env

# Add frontend URL to CORS_ORIGINS:
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://192.168.1.100:5173

# Restart backend
```

## Quick Checklist

Before trying to use frontend:

- [ ] PostgreSQL is running: `sudo systemctl status postgresql`
- [ ] Backend is running: `ps aux | grep uvicorn`
- [ ] Backend responds: `curl http://localhost:8000/api/health`
- [ ] Frontend .env is correct: `cat frontend/.env`
- [ ] Frontend is running: `ps aux | grep vite`
- [ ] Browser can access frontend: `http://localhost:5173`
- [ ] No CORS errors in browser console

## Still Not Working?

**Collect diagnostic info:**

```bash
# 1. Backend status
curl http://localhost:8000/api/health

# 2. Port usage
sudo lsof -i :8000
sudo lsof -i :5173

# 3. Environment
cat backend/.env | grep -v "SECRET\|PASSWORD"
cat frontend/.env

# 4. Network info
hostname -I

# 5. Process list
ps aux | grep -E "uvicorn|vite"

# 6. Recent backend logs
tail -n 50 backend/logs/app.log  # if logging to file
```

**Share this info for support.**

---

**Quick Reference:**
- Backend health: `curl http://localhost:8000/api/health`
- Start backend: `cd backend && source venv/bin/activate && uvicorn app.main:app --reload`
- Start frontend: `cd frontend && npm run dev`
- Check ports: `sudo lsof -i :8000` and `sudo lsof -i :5173`
