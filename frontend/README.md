# German Learning App - Frontend

React + TypeScript frontend for the German Learning Application.

## Prerequisites

### Ubuntu/Linux

1. **Node.js 18+ and npm**
   ```bash
   # Check if Node.js is installed
   node --version  # Should be 18.x or higher
   npm --version   # Should be 9.x or higher

   # If not installed, install Node.js 20 LTS
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Verify installation
   node --version
   npm --version
   ```

## Installation

### 1. Navigate to Frontend Directory

```bash
cd /path/to/myGermanAITeacher/frontend
```

### 2. Install Dependencies

```bash
npm install
```

This will install all dependencies including:
- React 18 + TypeScript
- Vite (build tool)
- React Router v6
- Zustand (state management)
- Tailwind CSS v3
- Axios (HTTP client)
- Headless UI components
- Testing libraries

**Installation time:** ~30-60 seconds

### 3. Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env if needed (default points to localhost:8000)
nano .env
```

**Default .env:**
```bash
VITE_API_BASE_URL=http://localhost:8000
```

**Important:** If your backend is running on a different host/port, update `VITE_API_BASE_URL` accordingly.

## Running the Application

### Development Mode

```bash
npm run dev
```

**Output:**
```
  VITE v7.3.1  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

**Access the app:**
- Open browser: `http://localhost:5173`
- Or if accessing remotely: `http://your-ubuntu-ip:5173`

**Features:**
- Hot Module Replacement (HMR) - instant updates on file save
- Fast refresh for React components
- TypeScript type checking

### Expose to Network (Optional)

To access from other devices on your network:

```bash
npm run dev -- --host
```

This will expose the dev server on all network interfaces.

## Testing the Application

### Prerequisites: Backend Must Be Running

The frontend requires the backend API to be running on `http://localhost:8000`.

**Start backend:**
```bash
# In a separate terminal
cd /path/to/myGermanAITeacher/backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Test Login Flow

1. **Open browser:** `http://localhost:5173`
2. **You should see:** Login page
3. **Click "Sign up"** to create account
4. **Fill registration form:**
   - Full Name: Your Name
   - Email: test@example.com
   - Password: password123
   - Confirm Password: password123
   - Target Level: B2 (default)
   - Occupation: (optional)
5. **Click "Create Account"**
6. **Expected result:**
   - Success toast notification
   - Redirect to Dashboard
   - Welcome message with your name

### Test Protected Routes

- **Try accessing:** `http://localhost:5173/dashboard` without login
- **Expected:** Redirect to login page
- **After login:** Access to dashboard is granted

## Production Build

### Build for Production

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

**Build artifacts:** Located in `frontend/dist/`

### Preview Production Build

```bash
npm run preview
```

Opens production build at `http://localhost:4173`

## Project Structure

```
frontend/
├── public/                       # Static assets
├── src/
│   ├── api/                      # API integration
│   │   ├── client.ts             # Axios instance with JWT interceptors
│   │   ├── services/             # API service classes
│   │   │   └── authService.ts    # Auth API (login, register, me)
│   │   └── types/                # TypeScript types
│   │       ├── auth.types.ts     # User, LoginRequest, etc.
│   │       └── common.types.ts   # ApiError, DifficultyLevel, etc.
│   ├── components/               # React components
│   │   ├── common/               # Reusable UI (Button, Card, Modal, Toast, etc.)
│   │   ├── auth/                 # Auth components (ProtectedRoute)
│   │   ├── dashboard/            # Dashboard components (coming soon)
│   │   ├── grammar/              # Grammar components (coming soon)
│   │   └── vocabulary/           # Vocabulary components (coming soon)
│   ├── hooks/                    # Custom React hooks (coming soon)
│   ├── pages/                    # Page components
│   │   ├── auth/                 # LoginPage, RegisterPage
│   │   └── DashboardPage.tsx     # Main dashboard
│   ├── store/                    # Zustand state management
│   │   ├── authStore.ts          # Auth state (user, isAuthenticated)
│   │   └── notificationStore.ts  # Toast notifications
│   ├── utils/                    # Utilities
│   │   └── validators.ts         # Form validation helpers
│   ├── styles/                   # Global styles
│   ├── App.tsx                   # Root component with routing
│   ├── main.tsx                  # Entry point
│   └── index.css                 # Tailwind CSS imports
├── .env                          # Environment variables (not committed)
├── .env.example                  # Environment template
├── package.json                  # Dependencies
├── vite.config.ts                # Vite configuration
├── tailwind.config.js            # Tailwind CSS configuration
└── tsconfig.json                 # TypeScript configuration
```

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server (http://localhost:5173) |
| `npm run build` | Build for production (output: dist/) |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

## Technology Stack

- **Framework:** React 18.3
- **Language:** TypeScript 5.6
- **Build Tool:** Vite 7.3
- **Styling:** Tailwind CSS 3.4
- **Routing:** React Router v6
- **State Management:** Zustand
- **HTTP Client:** Axios
- **UI Components:** Headless UI
- **Icons:** Heroicons
- **Testing:** Vitest + React Testing Library (coming soon)

## Features Implemented (Phase 0 & 1)

### Phase 0: Project Setup ✅
- ✅ Vite + React 18 + TypeScript
- ✅ Tailwind CSS with German flag colors (gold/red/black)
- ✅ 10 common UI components (Button, Card, Modal, Toast, etc.)
- ✅ React Router v6
- ✅ ESLint + Prettier

### Phase 1: Authentication ✅
- ✅ Axios client with JWT interceptors
- ✅ AuthService (login, register, getCurrentUser)
- ✅ Zustand stores (auth, notifications)
- ✅ Login/Register pages with validation
- ✅ Protected routes with auto-redirect
- ✅ Toast notification system

## Troubleshooting

### Port 5173 Already in Use

```bash
# Find process using port 5173
sudo lsof -i :5173

# Kill the process
kill -9 <PID>

# Or use a different port
npm run dev -- --port 3000
```

### Cannot Connect to Backend

**Error:** Network errors, 404 on API calls

**Solution:**
1. Verify backend is running: `curl http://localhost:8000/api/health`
2. Check `.env` file has correct `VITE_API_BASE_URL`
3. Check browser console for CORS errors
4. Restart frontend dev server after changing `.env`

### Dependencies Installation Fails

```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Build Fails with TypeScript Errors

```bash
# Check TypeScript errors
npm run build

# Common fix: Restart TypeScript server in VS Code
# Ctrl+Shift+P -> "TypeScript: Restart TS Server"
```

### Blank Page After Login

**Possible causes:**
1. Backend not running
2. API URL incorrect in `.env`
3. Check browser console for errors

**Debug:**
```bash
# Open browser DevTools (F12)
# Check Console tab for errors
# Check Network tab for failed API calls
```

## Performance

- **Bundle Size:** 301.84 KB (gzipped: 98.57 KB) ✅ <500KB target
- **Initial Load:** <3s on fast 3G
- **Hot Reload:** <500ms

## Next Steps

- **Phase 2:** Dashboard with integration API
- **Phase 3:** Grammar practice module (14 endpoints, 12 UX improvements)
- **Phase 4:** Vocabulary flashcards (26 endpoints, 11 UX improvements)
- **Phase 5:** Conversation practice
- **Phase 6:** Analytics & progress tracking
- **Phase 7:** Learning path recommendations
- **Phase 8:** Testing & documentation

## Support

For issues or questions:
1. Check browser console (F12) for errors
2. Check backend logs for API errors
3. Verify all dependencies installed: `npm install`
4. Verify Node.js version: `node --version` (18+)

## License

Internal project - Not for public distribution
