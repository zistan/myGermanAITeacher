# Frontend Architecture Codemap

**Last Updated:** 2026-01-22
**Entry Points:** `frontend/src/main.tsx`, `frontend/src/App.tsx`, `frontend/vite.config.ts`

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface Layer                      │
│  Browser → main.tsx → App.tsx → React Router → Page Components  │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                     Component Layer (73 files)                   │
│  Common (12) │ Grammar (7) │ Vocabulary (26) │ Conversation (13) │
│  Dashboard (6) │ Analytics (9) │ Layout (4)                     │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                State Management Layer (6 Zustand stores)         │
│  authStore │ grammarStore │ vocabularyStore │ conversationStore │
│  analyticsStore │ notificationStore (with localStorage persist) │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                  API Service Layer (7 services)                  │
│  Axios client with interceptors → JWT auth → Error handling     │
│  authService │ grammarService │ vocabularyService │ etc.        │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ▼
              Backend REST API (74 endpoints)
```

## Directory Structure

```
frontend/
├── src/                                 # Source code (126 files, ~20,000 LOC)
│   ├── main.tsx                        # Application entry point
│   ├── App.tsx                         # Root component with routing
│   ├── index.css                       # Global styles (Tailwind)
│   │
│   ├── pages/                          # Page components (23 files)
│   │   ├── auth/                       # Authentication (2 files)
│   │   ├── grammar/                    # Grammar practice (5 files)
│   │   ├── vocabulary/                 # Vocabulary learning (6 files)
│   │   ├── conversation/               # Conversation practice (4 files)
│   │   ├── analytics/                  # Progress analytics (5 files)
│   │   └── DashboardPage.tsx           # Main dashboard (1 file)
│   │
│   ├── components/                     # Reusable components (73 files)
│   │   ├── common/                     # Shared UI (12 files)
│   │   ├── grammar/                    # Grammar-specific (7 files)
│   │   ├── vocabulary/                 # Vocabulary-specific (26 files)
│   │   ├── conversation/               # Conversation-specific (13 files)
│   │   ├── dashboard/                  # Dashboard widgets (6 files)
│   │   ├── analytics/                  # Analytics visualizations (9 files)
│   │   └── layout/                     # Layout structure (4 files)
│   │
│   ├── store/                          # Zustand state management (6 stores)
│   │   ├── authStore.ts                # Authentication state
│   │   ├── grammarStore.ts             # Grammar session state
│   │   ├── vocabularyStore.ts          # Vocabulary learning state
│   │   ├── conversationStore.ts        # Conversation state
│   │   ├── analyticsStore.ts           # Analytics data state
│   │   └── notificationStore.ts        # Toast notifications
│   │
│   ├── api/                            # API integration layer
│   │   ├── client.ts                   # Axios instance with interceptors
│   │   ├── services/                   # API service classes (7 files)
│   │   │   ├── authService.ts
│   │   │   ├── grammarService.ts
│   │   │   ├── vocabularyService.ts
│   │   │   ├── conversationService.ts
│   │   │   ├── contextService.ts
│   │   │   ├── analyticsService.ts
│   │   │   └── integrationService.ts
│   │   └── types/                      # TypeScript type definitions (7 files)
│   │       ├── auth.types.ts
│   │       ├── common.types.ts
│   │       ├── grammar.types.ts
│   │       ├── vocabulary.types.ts
│   │       ├── conversation.types.ts
│   │       ├── analytics.types.ts
│   │       └── integration.types.ts
│   │
│   ├── hooks/                          # Custom React hooks (3 files)
│   │   ├── useKeyboardShortcuts.ts     # Comprehensive keyboard navigation
│   │   ├── useSessionPersistence.ts    # Auto-save and recovery
│   │   └── useAutoScroll.ts            # Smooth scrolling
│   │
│   └── utils/                          # Utility functions
│       └── textDiff.ts                 # Text difference highlighting
│
├── public/                             # Static assets
│   └── vite.svg
│
├── index.html                          # HTML entry point
├── package.json                        # Dependencies and scripts
├── vite.config.ts                      # Vite build configuration
├── tsconfig.json                       # TypeScript project references
├── tsconfig.app.json                   # TypeScript compiler options
├── tsconfig.node.json                  # TypeScript config for Vite
├── tailwind.config.js                  # Tailwind CSS configuration
├── postcss.config.js                   # PostCSS configuration
├── eslint.config.js                    # ESLint configuration
└── README.md                           # Frontend documentation
```

## Technology Stack

| Category | Technology | Version | Purpose |
|----------|-----------|---------|---------|
| **Framework** | React | 19.2.0 | UI library with concurrent features |
| **Language** | TypeScript | 5.9.3 | Type-safe development |
| **Build Tool** | Vite | 7.2.4 | Fast development and optimized builds |
| **Routing** | React Router | 7.12.0 | Client-side navigation |
| **State Management** | Zustand | 5.0.10 | Lightweight global state |
| **HTTP Client** | Axios | 1.13.2 | API communication |
| **Styling** | Tailwind CSS | 3.4.19 | Utility-first CSS framework |
| **Charts** | Recharts | 3.7.0 | Data visualization |
| **UI Components** | Headless UI | 2.2.9 | Unstyled accessible components |
| **Icons** | Heroicons | 2.2.0 | SVG icon library |
| **Icons** | Lucide React | 0.468.0 | Additional icons |
| **Notifications** | React Hot Toast | 2.6.0 | Toast notifications |
| **Date Handling** | date-fns | 4.1.0 | Date formatting and manipulation |
| **Text Diff** | diff-match-patch | 1.0.5 | Text comparison for grammar feedback |
| **Class Names** | clsx | 2.1.1 | Conditional className utility |
| **Data Fetching** | TanStack Query | 5.90.19 | Server state management |

## Module Organization

### Pages (23 files)

| Module | Files | Purpose |
|--------|-------|---------|
| **Authentication** | 2 | Login and registration pages |
| **Dashboard** | 1 | Main dashboard with unified data |
| **Grammar** | 5 | Topics, practice session, progress, review queue, results |
| **Vocabulary** | 6 | Browser, flashcards, lists, list detail, quiz, progress |
| **Conversation** | 4 | Contexts, practice, history, session detail |
| **Analytics** | 5 | Progress overview, achievements, heatmaps, leaderboards, error analysis |

### Components (73 files)

| Module | Files | Examples |
|--------|-------|----------|
| **Common** | 12 | Button, Card, Badge, Loading, ProgressBar, Modal, Toast |
| **Grammar** | 7 | ExerciseRenderer, FeedbackDisplay, SessionHeader, TextDiff |
| **Vocabulary** | 26 | FlashcardDisplay, WordCard, QuizQuestion, ListCard, SearchBar |
| **Conversation** | 13 | ChatInterface, MessageBubble, ContextCard, GrammarFeedback |
| **Dashboard** | 6 | CurrentStreakCard, DueItemsCard, QuickActionsCard, RecentActivity |
| **Analytics** | 9 | AchievementCard, ProgressChart, PieChart, HeatmapGrid |
| **Layout** | 4 | Layout, Sidebar, Header, ProtectedRoute |

### State Management (6 stores)

| Store | Purpose | Key Features |
|-------|---------|--------------|
| **authStore** | User authentication | JWT token, login/logout, user data |
| **grammarStore** | Grammar practice | Session state, exercise tracking, 24h persistence |
| **vocabularyStore** | Vocabulary learning | Word browsing, flashcards, quizzes, lists |
| **conversationStore** | Conversation practice | Message history, grammar feedback, session persistence |
| **analyticsStore** | Progress tracking | Achievements, stats, leaderboards, heatmaps |
| **notificationStore** | UI notifications | Toast queue, success/error/info messages |

### API Services (7 classes)

| Service | Endpoints | Purpose |
|---------|-----------|---------|
| **authService** | 3 | Registration, login, profile retrieval |
| **grammarService** | 14 | Topics, exercises, practice sessions, progress |
| **vocabularyService** | 26 | Words, flashcards, lists, quizzes, progress |
| **conversationService** | 4 | Start session, send message, end session, history |
| **contextService** | 5 | List contexts, get details, create/update/delete |
| **analyticsService** | 14 | Progress, achievements, stats, leaderboards, heatmaps |
| **integrationService** | 3 | Session analysis, learning paths, dashboard data |

## Application Entry Point

### main.tsx
- **Purpose:** Application bootstrap
- **Key Elements:**
  - React 19 StrictMode wrapper
  - Root DOM rendering with `createRoot`
  - Global CSS import (Tailwind)
  - App component mount

### App.tsx
- **Purpose:** Root component with routing configuration
- **Key Features:**
  - React Router v7 with BrowserRouter
  - Authentication initialization on mount
  - Protected route wrapper for authenticated pages
  - Layout component wrapper for dashboard/module pages
  - Toast notification container
  - 404 fallback route

## Routing Structure

The application uses React Router v7 with 30+ routes organized by module:

### Public Routes (2)
- `/login` - Login page
- `/register` - Registration page

### Protected Routes (26)

| Route Path | Page Component | Module |
|------------|---------------|--------|
| `/dashboard` | DashboardPage | Dashboard |
| `/grammar` | GrammarTopicsPage | Grammar |
| `/grammar/practice` | PracticeSessionPage | Grammar |
| `/grammar/progress` | GrammarProgressPage | Grammar |
| `/grammar/review-queue` | ReviewQueuePage | Grammar |
| `/grammar/results` | ResultsPage | Grammar |
| `/vocabulary` | VocabularyBrowserPage | Vocabulary |
| `/vocabulary/flashcards` | FlashcardSessionPage | Vocabulary |
| `/vocabulary/lists` | VocabularyListsPage | Vocabulary |
| `/vocabulary/lists/:id` | VocabularyListDetailPage | Vocabulary |
| `/vocabulary/quiz` | VocabularyQuizPage | Vocabulary |
| `/vocabulary/progress` | VocabularyProgressPage | Vocabulary |
| `/conversation` | ContextsPage | Conversation |
| `/conversation/practice` | PracticePage | Conversation |
| `/conversation/history` | HistoryPage | Conversation |
| `/conversation/session/:id` | SessionDetailPage | Conversation |
| `/analytics/progress` | ProgressOverviewPage | Analytics |
| `/analytics/achievements` | AchievementsPage | Analytics |
| `/analytics/heatmaps` | HeatmapPage | Analytics |
| `/analytics/leaderboards` | LeaderboardPage | Analytics |
| `/analytics/errors` | ErrorAnalysisPage | Analytics |

### Redirects (3)
- `/` → `/dashboard` (default)
- `/progress` → `/analytics/progress` (backward compatibility)
- `/achievements` → `/analytics/achievements` (backward compatibility)

### Route Protection
All protected routes wrap content with:
1. `<ProtectedRoute>` - Checks authentication, redirects to `/login` if unauthenticated
2. `<Layout>` - Provides sidebar navigation and header

## Build Configuration

### Vite (vite.config.ts)
- **Plugins:** @vitejs/plugin-react for React Fast Refresh
- **Server:**
  - Host: `0.0.0.0` (accessible from network)
  - Port: `5173` (default Vite port)
  - StrictPort: `false` (fallback to next available port)

### TypeScript (tsconfig.app.json)
- **Target:** ES2022
- **Module:** ESNext with bundler resolution
- **JSX:** react-jsx (automatic JSX runtime)
- **Strict Mode:** Enabled with strict type checking
- **Linting:** noUnusedLocals, noUnusedParameters, noFallthroughCasesInSwitch
- **Library:** DOM, DOM.Iterable, ES2022

### Tailwind CSS (tailwind.config.js)
- **Content:** `./index.html`, `./src/**/*.{js,ts,jsx,tsx}`
- **Theme Extensions:**
  - German flag colors: black (#000000), red (#DD0000), gold (#FFCC00)
  - Primary color scale (50-900) based on German gold
  - Danger color scale (50-900) based on German red
  - Custom font family: Inter with system fallbacks

### ESLint (eslint.config.js)
- **Configurations:**
  - ESLint recommended rules
  - TypeScript ESLint recommended
  - React Hooks rules (flat config)
  - React Refresh rules (Vite integration)
- **Target:** ES2020 with browser globals
- **Files:** `**/*.{ts,tsx}`

## External Dependencies

### Production (12 core dependencies)
```json
{
  "@headlessui/react": "^2.2.9",       // Accessible unstyled components
  "@heroicons/react": "^2.2.0",        // SVG icons
  "@tanstack/react-query": "^5.90.19", // Server state management
  "axios": "^1.13.2",                  // HTTP client
  "clsx": "^2.1.1",                    // className utility
  "date-fns": "^4.1.0",                // Date utilities
  "diff-match-patch": "^1.0.5",        // Text diff algorithm
  "lucide-react": "^0.468.0",          // Additional icons
  "react": "^19.2.0",                  // UI library
  "react-dom": "^19.2.0",              // React DOM renderer
  "react-hot-toast": "^2.6.0",         // Toast notifications
  "react-router-dom": "^7.12.0",       // Client-side routing
  "recharts": "^3.7.0",                // Charts and visualizations
  "zustand": "^5.0.10"                 // State management
}
```

### Development (16 dev dependencies)
- **Testing:** @playwright/test, @testing-library/react, @testing-library/jest-dom, vitest, jsdom
- **TypeScript:** typescript, @types/react, @types/react-dom, @types/node
- **Build Tools:** vite, @vitejs/plugin-react
- **Linting:** eslint, typescript-eslint, prettier
- **Styling:** tailwindcss, autoprefixer, postcss

## Key Features

### Authentication Flow
1. User lands on `/login` or `/register` (public routes)
2. On successful login, JWT token stored in authStore (localStorage)
3. ProtectedRoute checks auth on navigation
4. Axios interceptor injects Bearer token in all API requests
5. On 401 response, user redirected to `/login` with clear auth state

### State Persistence
- **Zustand Persist Middleware:** All stores except authStore use localStorage
- **Session Expiry:** Grammar and conversation sessions expire after 24h
- **Auto-Restore:** Sessions restored on page refresh if not expired
- **Clear on Logout:** All persisted state cleared on authentication logout

### Keyboard Shortcuts
- Comprehensive keyboard navigation via `useKeyboardShortcuts` hook
- Module-specific shortcuts (grammar exercises, flashcards, conversations)
- Global shortcuts (navigation, help dialog, escape to close modals)

### Error Handling
- **API Interceptor:** Catches 4xx/5xx responses
- **Toast Notifications:** User-friendly error messages
- **Validation Errors:** Field-level error display
- **Network Errors:** Graceful offline handling
- **401 Auto-Redirect:** Seamless re-authentication flow

### Responsive Design
- Mobile-first Tailwind CSS utilities
- Sidebar collapses on mobile (hamburger menu)
- Touch-friendly UI elements
- Responsive charts and tables

## Development Workflow

### Available Scripts
```bash
npm run dev      # Start Vite dev server (http://localhost:5173)
npm run build    # TypeScript compile + Vite production build
npm run lint     # Run ESLint on all TypeScript files
npm run preview  # Preview production build locally
```

### Development Server
- **Hot Module Replacement (HMR):** Fast Refresh for React components
- **TypeScript Checking:** Real-time type errors in terminal
- **ESLint Integration:** Lint errors shown in browser overlay
- **Network Access:** Dev server accessible from other devices (0.0.0.0)

### Environment Configuration
- **API Base URL:** Configured in `src/api/client.ts` (default: http://localhost:8000)
- **No .env File:** Backend URL hardcoded for local development
- **Production Build:** Update API URL before building for production

## Related Areas

- **[Frontend Components](./frontend-components.md)** - Component architecture, design patterns, and UI organization
- **[Frontend State Management](./frontend-state.md)** - Zustand stores, API integration, and data flow
- **[Backend API](./backend-api.md)** - REST API endpoints consumed by frontend services
- **[Frontend Setup Guide](../GUIDES/frontend.md)** - Installation and development setup
- **[Deployment Guide](../GUIDES/deployment.md)** - Production deployment instructions
- **[Troubleshooting Guide](../GUIDES/troubleshooting.md)** - Common issues and solutions

---

**Quick Navigation:**
- [← Back to Codemaps Index](./README.md)
- [Frontend Components →](./frontend-components.md)
- [Frontend State Management →](./frontend-state.md)
