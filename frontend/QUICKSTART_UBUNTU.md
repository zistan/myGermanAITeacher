# Quick Start Guide - Running Frontend on Ubuntu

Complete step-by-step guide to run the German Learning App frontend on Ubuntu 20.04+.

## Step 1: Install Node.js 20 LTS

```bash
# Update system packages
sudo apt update

# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version   # Should show v20.x.x
npm --version    # Should show 10.x.x
```

**Expected output:**
```
v20.18.1
10.8.2
```

## Step 2: Navigate to Frontend Directory

```bash
# Assuming your project is in /opt/german-learning-app
cd /opt/german-learning-app/frontend

# Or use your actual path
cd /path/to/myGermanAITeacher/frontend
```

## Step 3: Install Dependencies

```bash
npm install
```

**Expected output:**
```
added 380 packages, and audited 387 packages in 30s

95 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

**Time:** ~30-60 seconds depending on internet speed

## Step 4: Setup Environment Variables

```bash
# Copy example .env file
cp .env.example .env

# Verify the contents
cat .env
```

**Expected .env contents:**
```
VITE_API_BASE_URL=http://localhost:8000
```

**Optional:** Edit if backend is on different host/port:
```bash
nano .env
# Change to your backend URL, e.g.:
# VITE_API_BASE_URL=http://192.168.1.100:8000
```

## Step 5: Start Backend (Required)

The frontend needs the backend running. Open a **new terminal** and start the backend:

```bash
# Terminal 1 - Backend
cd /path/to/myGermanAITeacher/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Will watch for changes in these directories: ['/path/to/backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [12345] using StatReload
INFO:     Started server process [12346]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Verify backend is running:**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

## Step 6: Start Frontend Dev Server

In your **second terminal**, start the frontend:

```bash
# Terminal 2 - Frontend
cd /path/to/myGermanAITeacher/frontend
npm run dev
```

**Expected output:**
```
  VITE v7.3.1  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

## Step 7: Access the Application

### Option A: Local Browser (on Ubuntu machine)

```bash
# Install a browser if not available
sudo apt install firefox

# Open the app
firefox http://localhost:5173
```

### Option B: Remote Browser (from Windows/Mac)

1. **Get your Ubuntu IP address:**
   ```bash
   hostname -I | awk '{print $1}'
   # Example output: 192.168.1.100
   ```

2. **Expose Vite dev server to network:**
   ```bash
   # Stop current dev server (Ctrl+C)
   # Restart with --host flag
   npm run dev -- --host
   ```

3. **Open in browser:**
   ```
   http://192.168.1.100:5173
   ```

## Step 8: Test the Application

### Register a New Account

1. Click **"Sign up"** link
2. Fill the form:
   - **Full Name:** Test User
   - **Email:** test@example.com
   - **Password:** password123
   - **Confirm Password:** password123
   - **Target Level:** B2 (default)
   - **Occupation:** Developer (optional)
3. Click **"Create Account"**

**Expected result:**
- ✅ Green toast notification: "Registration successful"
- ✅ Redirect to Dashboard
- ✅ Welcome message: "Welcome back, Test User!"
- ✅ Dashboard shows target level: B2

### Test Login

1. Logout (refresh page or clear localStorage)
2. Go to http://localhost:5173/login
3. Enter credentials:
   - **Email:** test@example.com
   - **Password:** password123
4. Click **"Sign In"**

**Expected result:**
- ✅ Green toast notification: "Login successful"
- ✅ Redirect to Dashboard

### Test Protected Routes

1. Open browser console (F12)
2. Clear localStorage: `localStorage.clear()`
3. Try to access: http://localhost:5173/dashboard
4. **Expected:** Auto-redirect to /login

## Troubleshooting

### Issue: "Cannot find module" errors

```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

### Issue: Port 5173 already in use

```bash
# Find and kill the process
sudo lsof -i :5173
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3000
```

### Issue: Cannot connect to backend

**Check 1: Backend is running**
```bash
curl http://localhost:8000/api/health
# Should return: {"status":"healthy"}
```

**Check 2: CORS is configured**
```bash
# In backend/.env, ensure CORS_ORIGINS includes frontend URL
grep CORS_ORIGINS backend/.env
# Should include: http://localhost:5173
```

**Check 3: Frontend .env is correct**
```bash
cat frontend/.env
# Should show: VITE_API_BASE_URL=http://localhost:8000
```

### Issue: Blank page or white screen

**Debug steps:**
1. Open browser DevTools (F12)
2. Check **Console** tab for JavaScript errors
3. Check **Network** tab for failed API calls
4. Check **Application** > **Local Storage** for access_token

**Common causes:**
- Backend not running
- Wrong API URL in .env
- Browser cache (try Ctrl+Shift+R to hard refresh)

### Issue: EACCES permission errors

```bash
# Fix npm global directory permissions
mkdir ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

## Running in Production Mode

### Build the application

```bash
npm run build
```

**Output:**
```
dist/index.html                  0.46 kB │ gzip:  0.29 kB
dist/assets/index-DchqPB1Q.css  20.88 kB │ gzip:  4.36 kB
dist/assets/index-CHcu--qT.js  301.84 kB │ gzip: 98.57 kB
✓ built in 4.74s
```

### Preview production build

```bash
npm run preview
```

Opens production build at: http://localhost:4173

### Serve with Nginx (Optional)

```bash
# Install Nginx
sudo apt install nginx

# Copy build files
sudo cp -r dist/* /var/www/html/german-app/

# Create Nginx config
sudo nano /etc/nginx/sites-available/german-app
```

**Nginx config:**
```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/html/german-app;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/german-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Useful Commands

```bash
# Development server
npm run dev              # Start dev server on localhost:5173
npm run dev -- --host    # Expose to network
npm run dev -- --port 3000  # Use different port

# Build
npm run build            # Build for production (output: dist/)
npm run preview          # Preview production build

# Maintenance
npm install              # Install/update dependencies
npm run lint             # Run ESLint
npm cache clean --force  # Clear npm cache

# Process management
pkill -f "vite"          # Kill all Vite processes
lsof -i :5173            # Check what's using port 5173
```

## Development Workflow

**Typical development session:**

```bash
# Terminal 1: Backend
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Terminal 2: Frontend
cd frontend && npm run dev

# Terminal 3: Git operations, testing, etc.
```

**Hot reload is enabled:**
- Edit any `.tsx`, `.ts`, `.css` file
- Save the file
- Browser automatically refreshes (<500ms)
- No need to restart dev server

## Next Steps

After verifying everything works:
- ✅ Phase 0 & 1 complete
- 🔄 Ready for Phase 2: Dashboard with integration API
- ⏳ Phase 3: Grammar practice module
- ⏳ Phase 4: Vocabulary flashcards
- ⏳ Phase 5: Conversation practice

## Support

**Check logs:**
```bash
# Frontend console: Browser DevTools (F12) > Console
# Backend logs: Check terminal running uvicorn
# Nginx logs: sudo tail -f /var/log/nginx/error.log
```

**Report issues:**
1. Copy error messages from browser console
2. Copy terminal output
3. Check backend logs for API errors
4. Document steps to reproduce

---

**Status:** Phase 0 & 1 Complete ✅
**Last Updated:** 2026-01-18
**Bundle Size:** 98.57 KB (gzipped) ✅
