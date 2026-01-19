# Frontend Development Instructions
## German Learning Application - Phase 7

**Last Updated:** 2026-01-18
**Status:** Planning Phase
**Backend Status:** ✅ Complete (74 endpoints, production-ready)
**Frontend Status:** 🚀 Starting from scratch

---

## Project Overview

Building a comprehensive React-based frontend for an AI-powered German learning application. The backend is fully implemented and deployed, providing 74 REST API endpoints across 7 modules.

**Target User:** Igor - Italian native speaker, advanced German learner (B2/C1), works in payments/finance in Switzerland

---

## Critical Requirements

### 1. DO NOT MODIFY BACKEND
- ⚠️ **NEVER** change backend code, schemas, or API endpoints
- ⚠️ The backend is production-ready and fully tested
- ⚠️ Frontend must adapt to existing API contracts

### 2. Reference Documents (MUST READ and MUST ABIDE TO)
- `/brd and planning documents/german_learning_app_brd.md` - Complete BRD with Section 6.4 for frontend specs
- `/docs/EXERCISE_CYCLE_REVIEW.md` - 23 UX improvements for grammar and vocabulary
- '/frontend/DEVELOPMENT_STATUS.md' - which is the sole reference of the development status as well as the overall implementation plan for the frontend part
- Backend API docs: http://localhost:8000/docs (Swagger UI)

### 3. Technology Stack (REQUIRED)
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State Management:** Zustand (global state) + React Query (server state)
- **HTTP Client:** Axios with interceptors
- **UI Components:** Headless UI or Radix UI (for accessibility)
- **Icons:** Heroicons or Lucide React
- **Testing:** React Testing Library + Vitest + Cypress/Playwright

---

## Module Breakdown (7 Major Modules)

### Module 1: Authentication & User Management
**Priority:** P0 (Must complete first)
**Endpoints:** 3 endpoints (`/api/v1/auth/*`)

**Features:**
- Login page with email/password
- Registration page with user profile setup
- JWT token management (localStorage or secure cookie)
- Protected route wrapper component
- Auto-redirect on 401 errors
- "Remember me" functionality
- Password validation (8-100 chars)

**Key Components:**
- `LoginPage.tsx`
- `RegisterPage.tsx`
- `ProtectedRoute.tsx`
- `AuthProvider.tsx` (context)

**State:**
- Zustand store for auth state (user, token, isAuthenticated)
- Auto-refresh token on expiry (if implemented)

---

### Module 2: Dashboard (Main Landing Page)
**Priority:** P0 (Entry point after login)
**Endpoints:** 1 endpoint (`/api/v1/integration/dashboard`)

**Features:**
- Overall progress score (0-100) with visual indicator
- Current streak display with fire icon
- Due items counter (grammar + vocabulary)
- Recent activity timeline (last 5 actions)
- Quick action buttons (Start Grammar, Review Vocabulary, New Conversation)
- Module progress cards (Conversation, Grammar, Vocabulary)
- Achievement showcase (latest earned)

**Key Components:**
- `Dashboard.tsx`
- `ProgressScoreCard.tsx`
- `StreakCounter.tsx`
- `DueItemsWidget.tsx`
- `RecentActivityTimeline.tsx`
- `QuickActionButtons.tsx`
- `ModuleProgressCard.tsx`

**State:**
- React Query cache for dashboard data
- Auto-refresh every 5 minutes

---

### Module 3: Conversation Practice
**Priority:** P1 (Core learning feature)
**Endpoints:** 4 endpoints (`/api/sessions/*`)

**Features:**
- Context library browser (12+ contexts)
- Context selection with filters (category, difficulty)
- Chat interface with real-time messaging
- Message history display
- Grammar feedback inline with corrections
- Vocabulary detection highlights
- Session controls (Start, Pause, End)
- Session summary modal with recommendations

**Key Components:**
- `ConversationPage.tsx`
- `ContextLibrary.tsx`
- `ContextCard.tsx`
- `ChatInterface.tsx`
- `MessageBubble.tsx`
- `GrammarFeedbackInline.tsx`
- `SessionSummaryModal.tsx`

**State:**
- Current session (session_id, messages, context)
- Message input state
- Loading states for AI responses

**UX Requirements:**
- Typing indicators when AI is responding
- Auto-scroll to latest message
- Message timestamp display
- Copy button for AI messages
- Export session as PDF/text

---

### Module 4: Grammar Learning System
**Priority:** P1 (Core learning feature)
**Endpoints:** 14 endpoints (`/api/grammar/*`)

**Features:**

#### 4A. Topic Browser
- Grid/list view of 50+ topics
- Filter by category (9 categories: verbs, nouns, adjectives, etc.)
- Filter by difficulty (A1-C2)
- Sort by mastery level, last practiced
- Search by topic name
- Topic card with progress indicator

#### 4B. Practice Session Interface
- 5 exercise types:
  - Fill-in-the-blank
  - Multiple choice (4 options)
  - Translation (German ↔ Italian)
  - Error correction
  - Sentence building
- Real-time answer submission
- Immediate feedback with explanations
- Progress bar (X of Y exercises)
- Score tracker (correct/total)
- Skip button (with confirmation)
- Exit button (save progress)

#### 4C. UX Improvements (12 from Exercise Cycle Review)
**HIGH PRIORITY (Phase 7.1):**
- **G1: Keyboard Shortcuts** (4h effort)
  - Enter: Submit answer
  - Esc: Exit/close modal
  - 1-4: Select multiple choice option
  - Ctrl+Enter: Skip exercise
  - Space: Next exercise (after feedback)
  - ?: Show hint
- **G2: Session State Persistence** (6h effort)
  - Auto-save to localStorage every answer
  - Resume interrupted sessions
  - "Continue where you left off" prompt
- **G3: Pause & Resume** (8h effort)
  - Pause button in session
  - Resume from same exercise
  - Timer pause/resume
- **G4: In-session Streak Tracking** (3h effort)
  - Live streak counter (3, 5, 10 in a row)
  - Celebration animation on milestones
  - Reset notification on incorrect answer

**MEDIUM PRIORITY (Phase 7.2):**
- **G5: Understanding Self-Assessment** (5h effort)
  - 👍 "Got it easily" / 🤔 "Struggled" / 👎 "Still confused"
  - Affects spaced repetition weighting
- **G6: Text Diff Visualization** (4h effort)
  - Show differences for incorrect answers
  - Red (removed) / green (added) highlighting
  - Use `diff-match-patch` library
- **G7: Exercise Bookmarking** (6h effort)
  - "Flag for Review" button
  - Save to personal review list
  - Accessible from topic detail page
- **G8: Estimated Time Remaining** (3h effort)
  - Calculate based on average answer time
  - Display "~5 minutes remaining"

**LOW PRIORITY (Phase 7.3):**
- **G9: Auto-advance Option** (2h effort)
  - Settings toggle: auto-advance after 3s
  - User configurable delay
- **G10: Focus Mode** (2h effort)
  - Full-screen mode (hide navigation)
  - F11 shortcut or button
- **G11: Session Notes** (3h effort)
  - Side panel for personal notes
  - Auto-save to localStorage
  - Export with session summary
- **G12: 3-Level Hint System** (4h effort)
  - Hint 1: Grammar rule reminder
  - Hint 2: Example sentence
  - Hint 3: Partial answer reveal

#### 4D. Progress Dashboard
- Overall grammar mastery (0-100%)
- Category breakdown (pie chart or bar chart)
- Weak areas list with recommendations
- Strong areas recognition
- Review queue (overdue, due today, upcoming)

**Key Components:**
- `GrammarTopicBrowser.tsx`
- `GrammarTopicCard.tsx`
- `GrammarPracticeSession.tsx`
- `ExerciseCard.tsx` (factory for 5 types)
- `FillBlankExercise.tsx`
- `MultipleChoiceExercise.tsx`
- `TranslationExercise.tsx`
- `ErrorCorrectionExercise.tsx`
- `SentenceBuildingExercise.tsx`
- `ExerciseFeedback.tsx`
- `GrammarProgressDashboard.tsx`
- `ReviewQueue.tsx`

**State:**
- Current practice session (session_id, exercises, current_index)
- Exercise state (user_answer, is_submitted, feedback)
- Session stats (correct, total, accuracy, streak)
- Persisted state in localStorage

---

### Module 5: Vocabulary Management
**Priority:** P1 (Core learning feature)
**Endpoints:** 26 endpoints (`/api/v1/vocabulary/*`)

**Features:**

#### 5A. Word Browser
- Table view (default) and card view toggle
- Columns: Word, Translation, Part of Speech, Category, Difficulty, Mastery, Last Reviewed
- Filters:
  - Category (business, daily, finance, social, technical)
  - Difficulty (A1-C2)
  - Part of Speech (noun, verb, adjective, adverb)
  - Mastery Level (0-5)
  - Search by word or translation
- Sort by word, difficulty, mastery, last reviewed
- Pagination (50 words per page)
- Click word for detail view

#### 5B. Word Detail View
- Full word information (word, translation, definition, pronunciation)
- Example sentences (German + Italian)
- Gender and plural form (for nouns)
- Synonyms and antonyms
- Usage notes
- Personal progress (mastery level, times reviewed, accuracy rate)
- Next review date (spaced repetition)
- Add to personal list button
- Practice this word button (flashcard)

#### 5C. Flashcard Sessions
- Card types: definition, translation, usage, synonym, example
- 3D card flip animation
- Front: German word + context
- Back: Translation + example + notes
- Confidence rating (1-5 buttons)
- Spaced repetition algorithm
- Session progress bar

#### 5D. UX Improvements (11 from Exercise Cycle Review)
**HIGH PRIORITY (Phase 7.1):**
- **V1: Keyboard + Mobile Swipe Gestures** (8h effort)
  - **Keyboard:**
    - Space: Flip card
    - 1-5: Rate confidence (1=Again, 5=Perfect)
    - Backspace: Undo last rating
    - Esc: Exit session
  - **Mobile:**
    - Swipe up: Perfect (5)
    - Swipe right: Good (4)
    - Swipe down: Hard (2)
    - Swipe left: Again (1)
- **V2: Undo Last Rating** (4h effort)
  - Undo button (3-second timeout)
  - Toast: "Card rating undone"
  - Re-insert card into stack
- **V3: Visual 3D Card Stack** (6h effort)
  - Show 3-4 cards stacked behind current
  - Animate card flying off on rating
  - Progress indicator: "5 of 20 cards"
- **V4: Running Session Stats** (3h effort)
  - Live stats bar: Cards completed, Time elapsed, Accuracy, Streak
  - Update in real-time

**MEDIUM PRIORITY (Phase 7.2):**
- **V5: Spaced Repetition Visibility** (2h effort)
  - After rating: "See again in 3 days" tooltip
  - Color-code next review (red=today, yellow=soon, green=later)
- **V6: Difficult Cards Pile** (6h effort)
  - Track cards rated 1-2 ("Again" or "Hard")
  - End-of-session focused review (5-10 difficult cards)
  - "Review difficult cards now?" prompt
- **V7: Audio Pronunciation** (4h effort)
  - Speaker icon on card
  - Use browser Speech Synthesis API
  - German language (de-DE voice)
  - Auto-play option (toggle in settings)
- **V8: Pause/Resume** (6h effort)
  - Pause button in session
  - Save session state to localStorage
  - "Resume session" prompt on return

**LOW PRIORITY (Phase 7.3):**
- **V9: Flip Timer** (2h effort)
  - Show "Time to flip: 3s" countdown
  - Encourage thinking before flipping
  - Self-awareness tool
- **V10: Personal Mnemonic Notes** (4h effort)
  - "Add memory trick" button on back of card
  - Save to localStorage and backend
  - Display on future reviews
- **V11: Next Card Preview** (2h effort)
  - Small preview of next card (word only, no translation)
  - Prepare brain for next word

#### 5E. Personal Lists
- Create custom vocabulary lists
- Add/remove words
- Practice list as flashcard session
- Share lists (if `is_public=true`)

#### 5F. Quiz Generation
- Quiz types: multiple choice, fill blank, matching
- 10-20 questions per quiz
- Instant feedback
- Final score display

#### 5G. Progress Summary
- Total words learned (150+)
- Mastery distribution (level 0-5)
- Words by CEFR level (A1-C2)
- Words by category
- Review queue (due today, this week)
- Current streak

**Key Components:**
- `VocabularyBrowser.tsx`
- `WordCard.tsx`
- `WordDetailModal.tsx`
- `FlashcardSession.tsx`
- `FlashcardCard.tsx` (3D flip)
- `FlashcardRatingButtons.tsx`
- `FlashcardStats.tsx`
- `PersonalListManager.tsx`
- `VocabularyQuiz.tsx`
- `VocabularyProgressSummary.tsx`

**State:**
- Current flashcard session (session_id, cards, current_index)
- Card state (is_flipped, user_rating, time_spent)
- Personal lists (list_id, words)
- Persisted state in localStorage

---

### Module 6: Analytics & Progress Tracking
**Priority:** P2 (Enhance engagement)
**Endpoints:** 14 endpoints (`/api/v1/analytics/*`)

**Features:**

#### 6A. Progress Overview
- Time period selector (7, 30, 90 days)
- Key metrics cards:
  - Total study time
  - Sessions completed
  - Exercises completed
  - Words learned
  - Current streak
- Line charts:
  - Daily activity over time
  - Accuracy trend over time
- Module breakdown (pie chart): Conversation vs Grammar vs Vocabulary

#### 6B. Achievement Gallery
- 31 achievements across 4 tiers (bronze, silver, gold, platinum)
- Grid layout with card animations
- Earned achievements (unlocked, with date)
- Locked achievements (grayscale, with progress %)
- Achievement detail modal (description, criteria, points)
- Showcase toggle (display on profile)
- Total points earned

#### 6C. Error Analysis
- Recurring mistakes list (top 10)
- Error type distribution (pie chart)
- Grammar category errors (bar chart)
- Vocabulary category errors
- Recommendations based on errors

#### 6D. Heatmaps
- **Activity Heatmap** (GitHub-style)
  - 365 days (last year)
  - Color intensity: 0 (gray) → 5+ sessions (dark green)
  - Tooltip on hover: "3 sessions on Jan 15, 2026"
- **Grammar Mastery Heatmap**
  - Y-axis: 9 grammar categories
  - X-axis: Time periods (weeks/months)
  - Color: Mastery level (0% red → 100% green)

#### 6E. Leaderboards
- 4 leaderboard types: Overall, Grammar, Vocabulary, Streak
- Time period filter: All-time, Monthly, Weekly
- Top 100 users
- User's rank highlighted
- Profile links (if public)

**Key Components:**
- `ProgressOverview.tsx`
- `MetricCard.tsx`
- `ProgressChart.tsx` (reusable chart component)
- `AchievementGallery.tsx`
- `AchievementCard.tsx`
- `AchievementModal.tsx`
- `ErrorAnalysis.tsx`
- `ActivityHeatmap.tsx` (use library like `react-calendar-heatmap`)
- `GrammarHeatmap.tsx`
- `Leaderboard.tsx`
- `LeaderboardEntry.tsx`

**State:**
- Analytics data (cached with React Query)
- Selected time period
- Leaderboard type and period

---

### Module 7: Learning Path & Recommendations
**Priority:** P2 (Enhance user experience)
**Endpoints:** 1 endpoint (`/api/v1/integration/learning-path`)

**Features:**
- Personalized daily plan (75 minutes total)
  - 15 min: Vocabulary review
  - 30 min: Grammar practice
  - 30 min: Conversation
- Weekly goals tracker (5+ sessions)
- Module distribution recommendations
- Focus areas based on weak points
- Recommended contexts for conversation
- Motivation messages in German

**Key Components:**
- `LearningPathPage.tsx`
- `DailyPlanCard.tsx`
- `WeeklyGoalsTracker.tsx`
- `FocusAreasList.tsx`
- `RecommendedContexts.tsx`

**State:**
- Learning path data (cached)
- Custom plan settings

---

## Component Architecture

### Directory Structure
```
frontend/
├── public/                      # Static assets
├── src/
│   ├── components/              # Reusable components
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx
│   │   │   ├── RegisterForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   ├── dashboard/
│   │   │   ├── DashboardCard.tsx
│   │   │   ├── QuickActions.tsx
│   │   │   └── ProgressSummary.tsx
│   │   ├── conversation/
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── ContextSelector.tsx
│   │   │   └── SessionAnalysis.tsx
│   │   ├── grammar/
│   │   │   ├── TopicBrowser.tsx
│   │   │   ├── ExerciseCard.tsx
│   │   │   └── ProgressTracker.tsx
│   │   ├── vocabulary/
│   │   │   ├── WordBrowser.tsx
│   │   │   ├── FlashcardStack.tsx
│   │   │   └── QuizInterface.tsx
│   │   ├── analytics/
│   │   │   ├── AchievementGallery.tsx
│   │   │   ├── Heatmap.tsx
│   │   │   └── Leaderboard.tsx
│   │   ├── learning-path/
│   │   │   ├── DailyPlan.tsx
│   │   │   └── WeeklyGoals.tsx
│   │   └── common/
│   │       ├── Button.tsx
│   │       ├── Modal.tsx
│   │       ├── Toast.tsx
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── EmptyState.tsx
│   ├── pages/                   # Route pages
│   │   ├── LoginPage.tsx
│   │   ├── RegisterPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ConversationPage.tsx
│   │   ├── GrammarPage.tsx
│   │   ├── VocabularyPage.tsx
│   │   ├── AnalyticsPage.tsx
│   │   └── LearningPathPage.tsx
│   ├── services/                # API service layer
│   │   ├── api.ts               # Axios setup with interceptors
│   │   ├── authService.ts       # Auth endpoints
│   │   ├── conversationService.ts
│   │   ├── grammarService.ts
│   │   ├── vocabularyService.ts
│   │   ├── analyticsService.ts
│   │   └── integrationService.ts
│   ├── stores/                  # Zustand stores
│   │   ├── authStore.ts
│   │   ├── conversationStore.ts
│   │   ├── grammarStore.ts
│   │   └── vocabularyStore.ts
│   ├── hooks/                   # Custom React hooks
│   │   ├── useAuth.ts
│   │   ├── useKeyboardShortcuts.ts
│   │   ├── useSwipeGestures.ts
│   │   └── useLocalStorage.ts
│   ├── utils/                   # Helper functions
│   │   ├── formatters.ts        # Date, number formatting
│   │   ├── validators.ts        # Form validation
│   │   └── constants.ts         # App constants
│   ├── types/                   # TypeScript types
│   │   ├── api.types.ts         # API response types
│   │   └── app.types.ts         # App-specific types
│   ├── App.tsx                  # Main app component
│   ├── main.tsx                 # Entry point
│   └── index.css                # Global styles (Tailwind)
├── .env.example                 # Environment variables template
├── .env.local                   # Local environment (gitignored)
├── index.html                   # HTML entry point
├── package.json                 # Dependencies
├── tsconfig.json                # TypeScript config
├── vite.config.ts               # Vite config
├── tailwind.config.js           # Tailwind config
├── postcss.config.js            # PostCSS config
└── README.md                    # Frontend documentation
```

---

## State Management Strategy

### 1. Zustand (Global State)
Use for client-side global state:
- **Auth Store:** `user`, `token`, `isAuthenticated`
- **UI Store:** `theme`, `sidebarOpen`, `toasts`
- **Preferences Store:** `language`, `auto_advance`, `audio_enabled`

```typescript
// Example: authStore.ts
import create from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  user: UserResponse | null
  token: string | null
  isAuthenticated: boolean
  login: (token: string, user: UserResponse) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (token, user) => set({ token, user, isAuthenticated: true }),
      logout: () => set({ token: null, user: null, isAuthenticated: false }),
    }),
    { name: 'auth-storage' }
  )
)
```

### 2. React Query (Server State)
Use for API data caching and synchronization:
- All API calls wrapped in React Query hooks
- Auto-refetch on focus/reconnect
- Optimistic updates for better UX
- Error handling and retries

```typescript
// Example: useGrammarTopics hook
import { useQuery } from '@tanstack/react-query'
import { grammarService } from '@/services/grammarService'

export function useGrammarTopics(category?: string, difficulty?: string) {
  return useQuery({
    queryKey: ['grammar-topics', category, difficulty],
    queryFn: () => grammarService.getTopics(category, difficulty),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}
```

### 3. localStorage (Persistence)
Use for:
- Session state (grammar/vocabulary sessions)
- User preferences (shortcuts enabled, auto-advance)
- Bookmarked exercises
- Personal notes and mnemonics

---

## API Integration Layer

### Axios Setup with Interceptors

```typescript
// services/api.ts
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor: Add auth token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: Handle 401 errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout()
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)
```

### Service Class Pattern

```typescript
// services/grammarService.ts
import { api } from './api'
import type {
  GrammarTopicResponse,
  StartGrammarPracticeRequest,
  GrammarPracticeSessionResponse,
  SubmitExerciseAnswerRequest,
  SubmitExerciseAnswerResponse,
} from '@/types/api.types'

export const grammarService = {
  // Get all topics
  async getTopics(category?: string, difficulty?: string) {
    const params = new URLSearchParams()
    if (category) params.append('category', category)
    if (difficulty) params.append('difficulty', difficulty)
    const response = await api.get<GrammarTopicResponse[]>(`/api/grammar/topics?${params}`)
    return response.data
  },

  // Start practice session
  async startPractice(request: StartGrammarPracticeRequest) {
    const response = await api.post<GrammarPracticeSessionResponse>(
      '/api/grammar/practice/start',
      request
    )
    return response.data
  },

  // Submit answer
  async submitAnswer(sessionId: number, request: SubmitExerciseAnswerRequest) {
    const response = await api.post<SubmitExerciseAnswerResponse>(
      `/api/grammar/practice/${sessionId}/answer`,
      request
    )
    return response.data
  },

  // End session
  async endSession(sessionId: number) {
    await api.post(`/api/grammar/practice/${sessionId}/end`)
  },
}
```

---

## Design System

### Color Palette
```css
/* tailwind.config.js */
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          black: '#000000',
          red: '#DD0000',
          gold: '#FFCC00',
        },
        background: {
          light: '#F9FAFB',
          dark: '#1F2937',
        },
        success: '#10B981',
        error: '#EF4444',
        warning: '#F59E0B',
        info: '#3B82F6',
      },
    },
  },
}
```

### Typography
- Font family: Inter or system-ui (supports ä, ö, ü, ß)
- Sizes: text-xs, text-sm, text-base, text-lg, text-xl, text-2xl
- Weights: font-normal (400), font-medium (500), font-semibold (600), font-bold (700)

### Spacing
- Tailwind spacing scale (4px base): 0, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 32, 40, 48, 64

### Shadows
- shadow-sm: Small shadow for cards
- shadow-md: Medium shadow for elevated elements
- shadow-lg: Large shadow for modals

---

## Accessibility (WCAG 2.1 AA)

### Keyboard Navigation
- All interactive elements must be focusable
- Logical tab order
- Skip links for main content
- Keyboard shortcuts (with toggle in settings)
- Focus indicators (ring-2 ring-blue-500)

### Screen Reader Support
- ARIA labels for all buttons/links
- ARIA live regions for dynamic content (toasts, chat messages)
- Semantic HTML (header, nav, main, article, aside, footer)
- Alt text for all images
- Form labels properly associated

### Visual Accessibility
- 4.5:1 contrast ratio for normal text
- 3:1 for large text (>18px or 14px bold)
- No color-only information (use icons + text)
- Support 200% zoom without horizontal scroll
- High contrast mode support

### Motor Accessibility
- Minimum click target: 44×44px (mobile)
- No hover-only content (must be accessible on tap)
- Generous spacing between interactive elements
- Support for keyboard-only navigation

---

## Performance Optimization

### Code Splitting
```typescript
// Route-based code splitting with React.lazy
import { lazy, Suspense } from 'react'

const DashboardPage = lazy(() => import('@/pages/DashboardPage'))
const GrammarPage = lazy(() => import('@/pages/GrammarPage'))

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/grammar" element={<GrammarPage />} />
      </Routes>
    </Suspense>
  )
}
```

### Caching Strategy
- **React Query:** 5-minute stale time for static data (topics, contexts)
- **localStorage:** Persist session state, preferences
- **Service Worker:** Cache API responses for offline support (Phase 8)

### Bundle Size Target
- Initial JS bundle: <500KB
- Use dynamic imports for large libraries (Chart.js, diff-match-patch)
- Tree-shaking for unused code

### Runtime Performance
- Virtualize long lists (react-window for 100+ items)
- Debounce search inputs (300ms delay)
- Memoize expensive computations (useMemo, useCallback)
- Optimize re-renders (React.memo for pure components)

---

## Error Handling Patterns

### Network Errors
```typescript
// Offline indicator component
function OfflineIndicator() {
  const [isOnline, setIsOnline] = useState(navigator.onLine)

  useEffect(() => {
    window.addEventListener('online', () => setIsOnline(true))
    window.addEventListener('offline', () => setIsOnline(false))
  }, [])

  if (isOnline) return null

  return (
    <div className="fixed top-0 left-0 right-0 bg-red-500 text-white p-2 text-center z-50">
      You are offline. Some features may not work.
    </div>
  )
}
```

### Validation Errors (400)
- Display field-specific error messages below inputs
- Highlight invalid fields with red border
- Clear errors on input change

### Authentication Errors (401)
- Redirect to login page
- Preserve intended URL for return after login
- Show toast: "Session expired. Please log in again."

### Not Found (404)
- Friendly 404 page with suggestions
- Link back to dashboard
- Search bar to find content

### Empty States
- Friendly illustrations
- Clear CTA button (e.g., "Start your first session")
- Contextual help text

---

## Testing Strategy

### Unit Tests (Vitest)
- All utility functions (formatters, validators)
- Custom hooks (useAuth, useKeyboardShortcuts)
- Service classes (API mocking with MSW)
- Coverage: >80%

```typescript
// Example: formatters.test.ts
import { describe, it, expect } from 'vitest'
import { formatDuration, formatDate } from './formatters'

describe('formatDuration', () => {
  it('formats minutes correctly', () => {
    expect(formatDuration(125)).toBe('2h 5m')
  })

  it('handles zero', () => {
    expect(formatDuration(0)).toBe('0m')
  })
})
```

### Component Tests (React Testing Library)
- Render tests (component appears correctly)
- Interaction tests (button clicks, form submissions)
- Accessibility tests (keyboard navigation, screen reader)
- Snapshot tests (prevent unintended UI changes)

```typescript
// Example: LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { LoginForm } from './LoginForm'

describe('LoginForm', () => {
  it('renders login form', () => {
    render(<LoginForm />)
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument()
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument()
  })

  it('submits form with valid data', async () => {
    const mockLogin = vi.fn()
    render(<LoginForm onLogin={mockLogin} />)

    fireEvent.change(screen.getByLabelText(/email/i), {
      target: { value: 'test@example.com' },
    })
    fireEvent.change(screen.getByLabelText(/password/i), {
      target: { value: 'password123' },
    })
    fireEvent.click(screen.getByRole('button', { name: /log in/i }))

    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'test@example.com',
        password: 'password123',
      })
    })
  })
})
```

### Integration Tests
- User flows (login → dashboard → start session)
- Form submissions with API mocking
- Error scenario handling (401, 404, 500)

### E2E Tests (Cypress or Playwright)
```typescript
// Example: conversation.spec.ts
describe('Conversation Practice', () => {
  it('completes a conversation session', () => {
    cy.login('test@example.com', 'password')
    cy.visit('/conversation')
    cy.get('[data-testid="context-card"]').first().click()
    cy.get('[data-testid="start-session-button"]').click()
    cy.get('[data-testid="message-input"]').type('Guten Tag!')
    cy.get('[data-testid="send-button"]').click()
    cy.get('[data-testid="ai-message"]').should('be.visible')
    cy.get('[data-testid="end-session-button"]').click()
    cy.get('[data-testid="session-summary"]').should('be.visible')
  })
})
```

---

## Environment Variables

### .env.example
```bash
# API Base URL
VITE_API_BASE_URL=http://localhost:8000

# Environment
VITE_ENVIRONMENT=development

# Feature Flags
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_AUDIO=true

# Sentry (optional)
VITE_SENTRY_DSN=
```

### .env.local (development)
```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_ENVIRONMENT=development
VITE_ENABLE_ANALYTICS=false
VITE_ENABLE_AUDIO=true
```

### .env.production
```bash
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_ENVIRONMENT=production
VITE_ENABLE_ANALYTICS=true
VITE_ENABLE_AUDIO=true
VITE_SENTRY_DSN=your-sentry-dsn
```

---

## Development Workflow

### Initial Setup
```bash
# 1. Initialize Vite + React + TypeScript
npm create vite@latest frontend -- --template react-ts

# 2. Install dependencies
cd frontend
npm install

# 3. Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 4. Install state management
npm install zustand @tanstack/react-query axios

# 5. Install UI components
npm install @headlessui/react @heroicons/react

# 6. Install dev dependencies
npm install -D @testing-library/react @testing-library/jest-dom vitest
```

### Development Commands
```bash
# Start dev server
npm run dev

# Run tests
npm run test

# Run tests with coverage
npm run test:coverage

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check

# Lint
npm run lint
```

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/auth-module

# Commit regularly with clear messages
git add .
git commit -m "feat: implement login page with JWT auth"

# Push to remote
git push origin feature/auth-module

# Create pull request
gh pr create --title "feat: Authentication Module" --body "Implements login, register, and protected routes"
```

---

## Implementation Phases

### Phase 7.1: Core Infrastructure (Week 1)
**Priority:** P0
**Estimated:** 40 hours

**Tasks:**
1. Project setup (Vite, TypeScript, Tailwind) - 4h
2. API service layer with Axios - 6h
3. Authentication module (login, register, protected routes) - 12h
4. Dashboard page with unified data - 8h
5. Common components (Button, Modal, Toast, Loading) - 6h
6. Unit tests for services and utilities - 4h

**Deliverables:**
- ✅ Working authentication flow
- ✅ Dashboard with progress overview
- ✅ Reusable component library
- ✅ API integration layer

### Phase 7.2: Conversation Module (Week 2)
**Priority:** P1
**Estimated:** 32 hours

**Tasks:**
1. Context library browser - 8h
2. Chat interface with message history - 12h
3. Session management (start, end) - 6h
4. Session summary modal - 4h
5. Component tests - 2h

**Deliverables:**
- ✅ Functional conversation practice
- ✅ Context selection
- ✅ Real-time chat with AI
- ✅ Session analytics

### Phase 7.3: Grammar Module (Weeks 3-4)
**Priority:** P1
**Estimated:** 50 hours (base) + 50 hours (UX improvements)

**Base Features (Week 3):**
1. Topic browser with filters - 8h
2. Practice session interface - 16h
3. 5 exercise types implementation - 16h
4. Progress dashboard - 6h
5. Component tests - 4h

**UX Improvements (Week 4):**
- High priority (G1-G4): 21h
- Medium priority (G5-G8): 18h
- Low priority (G9-G12): 11h

**Deliverables:**
- ✅ Complete grammar learning system
- ✅ All 5 exercise types
- ✅ 12 UX improvements
- ✅ Spaced repetition integration

### Phase 7.4: Vocabulary Module (Weeks 5-6)
**Priority:** P1
**Estimated:** 48 hours (base) + 47 hours (UX improvements)

**Base Features (Week 5):**
1. Word browser with filters - 10h
2. Word detail view - 6h
3. Flashcard session - 16h
4. Personal lists - 8h
5. Progress summary - 4h
6. Component tests - 4h

**UX Improvements (Week 6):**
- High priority (V1-V4): 21h
- Medium priority (V5-V8): 18h
- Low priority (V9-V11): 8h

**Deliverables:**
- ✅ Complete vocabulary system
- ✅ Flashcards with spaced repetition
- ✅ 11 UX improvements
- ✅ Personal lists and quizzes

### Phase 7.5: Analytics Module (Week 7)
**Priority:** P2
**Estimated:** 32 hours

**Tasks:**
1. Progress overview with charts - 10h
2. Achievement gallery - 8h
3. Activity heatmap (GitHub-style) - 6h
4. Grammar mastery heatmap - 4h
5. Leaderboards - 4h

**Deliverables:**
- ✅ Comprehensive analytics
- ✅ Achievement system
- ✅ Heatmaps
- ✅ Leaderboards

### Phase 7.6: Learning Path & Polish (Week 8)
**Priority:** P2
**Estimated:** 24 hours

**Tasks:**
1. Learning path page - 8h
2. Daily plan component - 4h
3. Weekly goals tracker - 4h
4. Error analysis page - 4h
5. Final polish and bug fixes - 4h

**Deliverables:**
- ✅ Personalized learning paths
- ✅ Goal tracking
- ✅ Polished user experience

### Phase 7.7: Testing & Deployment (Week 9)
**Priority:** P0
**Estimated:** 24 hours

**Tasks:**
1. E2E tests (Cypress) - 12h
2. Accessibility audit - 4h
3. Performance optimization - 4h
4. Production build and deployment - 4h

**Deliverables:**
- ✅ E2E test coverage
- ✅ WCAG 2.1 AA compliance
- ✅ Optimized production build
- ✅ Deployed frontend

**Total Estimated Effort:** ~400 hours (9-10 weeks)

---

## Critical Success Factors

### 1. DO NOT MODIFY BACKEND ⚠️
- Backend is production-ready and fully tested
- Frontend must adapt to existing API contracts
- If API doesn't meet needs, work around it in frontend (not ideal but acceptable)

### 2. Follow BRD Specifications
- All UI/UX specs in BRD Section 6.4 are mandatory
- 23 Exercise Cycle UX improvements are high-impact features
- Design system (colors, typography) must match specifications

### 3. Accessibility First
- WCAG 2.1 AA compliance is non-negotiable
- Test with keyboard navigation
- Test with screen reader (NVDA, JAWS, VoiceOver)
- Support 200% zoom

### 4. Performance Matters
- <500KB initial bundle size
- <1s page load time
- 60fps animations
- Virtualize long lists

### 5. Testing is Mandatory
- Write tests alongside implementation
- >80% code coverage
- Test accessibility
- E2E tests for critical flows

### 6. Git Discipline
- **ALWAYS commit AND push** after completing each bug fix or feature
- Commit after each logical unit of work
- Clear commit messages (feat:, fix:, docs:, test:, refactor:)
- **Never leave commits unpushed** - push immediately after committing
- Create pull requests for review

---

## Common Pitfalls to Avoid

### 1. Over-engineering
- Don't create abstractions for single-use components
- Keep it simple until complexity is needed
- YAGNI (You Aren't Gonna Need It)

### 2. API Assumptions
- Always read Swagger docs before implementing
- Don't assume API structure—verify with actual calls
- Handle all error cases (400, 401, 404, 500)

### 3. State Management Confusion
- Use Zustand for global client state (auth, UI)
- Use React Query for server state (API data)
- Don't duplicate state between them
- Use localStorage only for persistence

### 4. Accessibility Afterthought
- Build accessibility in from the start
- Use semantic HTML (not div soup)
- Test keyboard navigation as you build
- ARIA labels for all interactive elements

### 5. Performance Ignored
- Don't render 1000+ items without virtualization
- Debounce search inputs
- Memoize expensive computations
- Code-split large pages

---

## Resources & References

### Documentation
- **React 18:** https://react.dev
- **TypeScript:** https://www.typescriptlang.org/docs
- **Vite:** https://vitejs.dev
- **Tailwind CSS:** https://tailwindcss.com/docs
- **Zustand:** https://github.com/pmndrs/zustand
- **React Query:** https://tanstack.com/query/latest
- **Headless UI:** https://headlessui.com
- **React Testing Library:** https://testing-library.com/react

### Libraries
- **Diff visualization:** diff-match-patch
- **Charts:** Chart.js or Recharts
- **Heatmap:** react-calendar-heatmap
- **Icons:** Heroicons or Lucide React
- **Forms:** React Hook Form + Zod (validation)
- **Date handling:** date-fns

### Testing Tools
- **Unit/Component:** Vitest + React Testing Library
- **E2E:** Cypress or Playwright
- **API Mocking:** MSW (Mock Service Worker)

### AI Tools
- **Claude Code:** For code generation and debugging
- **GitHub Copilot:** For autocomplete

---

## Questions & Support

### If You Get Blocked:
1. **Check BRD:** Section 6.4 has detailed frontend specs
2. **Check Exercise Cycle Review:** 23 UX improvements documented
3. **Check Swagger UI:** http://localhost:8000/docs for API reference
4. **Ask User:** If requirements are unclear, ask before implementing

### Before Asking for Help:
1. Did you read the BRD Section 6.4?
2. Did you check the Exercise Cycle Review?
3. Did you test the API endpoint in Swagger UI?
4. Did you check the backend code to understand the response schema?
5. Did you search for similar implementations in the codebase?

---

**Last Updated:** 2026-01-18
**Status:** Ready for Phase 7 Implementation
**Next Step:** Initialize Vite project and set up infrastructure
