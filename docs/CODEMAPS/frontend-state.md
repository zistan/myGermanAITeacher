# Frontend State Management Codemap

**Last Updated:** 2026-01-22
**Entry Points:** `frontend/src/store/` (6 Zustand stores), `frontend/src/api/client.ts`

## State Management Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Frontend Components                          │
│  Pages, UI Components, Forms, Modals                            │
└────────────────────┬────────────────────────────────────────────┘
                     │ (useState, useEffect, event handlers)
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                  Zustand State Stores (6 stores)                 │
│  authStore │ grammarStore │ vocabularyStore │ conversationStore │
│  analyticsStore │ notificationStore                             │
│                                                                  │
│  Actions: setUser, startSession, addToast, etc.                 │
│  Selectors: (state) => state.user, state.currentSession, etc.   │
│  Middleware: persist (localStorage with 24h session expiry)     │
└────────────────────┬────────────────────────────────────────────┘
                     │ (store actions call API services)
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                    API Service Layer (7 classes)                 │
│  authService │ grammarService │ vocabularyService │ etc.        │
│                                                                  │
│  Service Methods: async functions returning Promise<T>          │
└────────────────────┬────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────────┐
│                      Axios HTTP Client                           │
│  Base URL: http://localhost:8000                                │
│  Request Interceptor: Add JWT Bearer token                      │
│  Response Interceptor: Handle 401, validation errors            │
└────────────────────┬────────────────────────────────────────────┘
                     │ (HTTP requests: GET, POST, PUT, DELETE)
                     │
                     ▼
              Backend REST API (74 endpoints)
```

## Zustand Stores (6 total)

### 1. authStore.ts (56 lines)
**Purpose:** User authentication and session management

**State Shape:**
```typescript
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}
```

**Actions:**
| Action | Purpose | Side Effects |
|--------|---------|--------------|
| `setUser(user)` | Set authenticated user | Updates isAuthenticated, clears error |
| `setLoading(isLoading)` | Toggle loading state | Used during API calls |
| `setError(error)` | Set error message | Displays authentication errors |
| `logout()` | Clear user session | Removes token and user from localStorage |
| `initialize()` | Restore session on app load | Reads user from localStorage |

**Persistence:** Direct localStorage access (no Zustand persist middleware)
- **Token:** `localStorage.getItem('access_token')`
- **User:** `localStorage.getItem('user')` (JSON string)

**Usage Example:**
```typescript
const { user, isAuthenticated, logout } = useAuthStore();
```

---

### 2. notificationStore.ts (55 lines)
**Purpose:** Toast notification queue management

**State Shape:**
```typescript
interface NotificationState {
  toasts: ToastProps[];
}
```

**Toast Type:**
```typescript
interface ToastProps {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  title: string;
  message?: string;
  duration: number;
  isVisible: boolean;
  onClose: () => void;
}
```

**Actions:**
| Action | Purpose | Behavior |
|--------|---------|----------|
| `addToast(type, title, message, duration)` | Add toast to queue | Auto-generates ID, auto-dismisses after duration (default 5s) |
| `removeToast(id)` | Remove toast from queue | Called after animation completes |

**Auto-Dismiss Flow:**
1. Toast added with duration (e.g., 5000ms)
2. After duration expires, `isVisible` set to `false` (triggers fade-out animation)
3. After 300ms animation, toast removed from array

**No Persistence:** Toasts are ephemeral, not stored in localStorage

**Usage Example:**
```typescript
const addToast = useNotificationStore((state) => state.addToast);
addToast('success', 'Saved!', 'Your progress has been saved.', 3000);
```

---

### 3. grammarStore.ts (Large store with session persistence)
**Purpose:** Grammar practice session state and exercise tracking

**Key State:**
```typescript
interface GrammarState {
  // Current session
  currentSession: PracticeSessionResponse | null;
  currentExercise: GrammarExercise | null;
  sessionState: 'idle' | 'in_progress' | 'completed';

  // Session data
  exercises: GrammarExercise[];
  userAnswers: Map<number, string>;
  feedback: Map<number, ExerciseFeedback>;
  sessionNotes: SessionNote[];
  bookmarkedExercises: Set<number>;

  // Session stats
  sessionProgress: SessionProgress;
  timeElapsed: number;

  // Session expiry (24h)
  sessionExpiresAt: number | null;
}
```

**Key Actions:**
- `startSession(request)` - Start new practice session, save to localStorage
- `loadNextExercise()` - Fetch next exercise from backend
- `submitAnswer(answer)` - Submit answer, get feedback, update progress
- `addNote(exerciseId, note)` - Bookmark exercise with note
- `endSession()` - Complete session, save results, clear state
- `restoreSession()` - Restore from localStorage if not expired (24h)

**Persistence:** Zustand persist middleware with localStorage
- **Storage Key:** `grammar-session-storage`
- **Session Expiry:** 24 hours (86400000ms)
- **Expiry Check:** On mount, if `sessionExpiresAt < Date.now()`, clear session

**Session Lifecycle:**
1. User starts session → `startSession()` → Save to localStorage with expiry
2. User completes exercises → State updates persisted automatically
3. Page refresh → `restoreSession()` → Check expiry → Restore or clear
4. User ends session → `endSession()` → Clear state and localStorage

---

### 4. vocabularyStore.ts (Large store with flashcard/quiz state)
**Purpose:** Vocabulary learning, flashcards, quizzes, and word lists

**Key State:**
```typescript
interface VocabularyState {
  // Word browsing
  words: VocabularyWithProgress[];
  filters: VocabularyFilters;
  selectedWord: VocabularyWithProgress | null;

  // Flashcard session
  flashcardSession: FlashcardSessionResponse | null;
  flashcardState: 'idle' | 'in_progress' | 'completed';
  currentCardIndex: number;
  isFlipped: boolean;
  flashcardResults: FlashcardResult[];

  // Quiz session
  quizSession: VocabularyQuizResponse | null;
  quizState: 'idle' | 'in_progress' | 'completed';
  currentQuestionIndex: number;
  quizAnswers: Map<number, string>;

  // Vocabulary lists
  userLists: PersonalVocabularyList[];
  currentList: PersonalVocabularyListWithWords | null;

  // Progress
  progressSummary: VocabularyProgressSummary | null;
}
```

**Key Actions:**
- **Words:** `fetchWords(filters)`, `selectWord(wordId)`, `createWord(word)`
- **Flashcards:** `startFlashcardSession(config)`, `flipCard()`, `rateCard(rating)`, `nextCard()`
- **Quizzes:** `startQuiz(config)`, `submitQuizAnswer(answer)`, `completeQuiz()`
- **Lists:** `fetchLists()`, `createList(list)`, `addWordToList(listId, wordId)`, `deleteList(listId)`
- **Progress:** `fetchProgressSummary()`, `fetchReviewQueue()`

**Persistence:** Zustand persist middleware (selective keys)
- **Persisted:** `words`, `filters`, `userLists`, `progressSummary`
- **Not Persisted:** Session state (flashcards/quizzes expire on page reload)

---

### 5. conversationStore.ts (Large store with message history)
**Purpose:** AI conversation practice state and message management

**Key State:**
```typescript
interface ConversationState {
  // Current session
  currentSession: ConversationSession | null;
  sessionState: 'idle' | 'in_progress' | 'completed';

  // Messages
  messages: ConversationTurnResponse[];
  isTyping: boolean;

  // Settings
  requestFeedback: boolean;
  showGrammarFeedback: boolean;
  showVocabularyHighlights: boolean;

  // Contexts
  contexts: Context[];
  selectedContext: Context | null;

  // History
  sessionHistory: ConversationSession[];

  // Session persistence
  sessionExpiresAt: number | null;
}
```

**Key Actions:**
- `startSession(contextId)` - Start conversation with selected context
- `sendMessage(message, requestFeedback)` - Send user message, get AI response
- `endSession()` - Complete session, save history
- `fetchHistory()` - Load past conversation sessions
- `restoreSession()` - Restore active session if not expired (24h)
- `toggleFeedback()` - Toggle grammar feedback display
- `selectContext(context)` - Set conversation context

**Message Flow:**
1. User types message → `sendMessage()` called
2. `isTyping` set to `true` (shows typing indicator)
3. Backend responds with AI message + optional grammar feedback
4. Message added to `messages` array
5. `isTyping` set to `false`
6. Auto-scroll to bottom

**Persistence:** Zustand persist middleware with 24h expiry
- **Persisted:** `currentSession`, `messages`, `sessionExpiresAt`, `contexts`
- **Session Expiry:** 24 hours (same as grammar)

---

### 6. analyticsStore.ts (Analytics data and progress tracking)
**Purpose:** User progress, achievements, stats, and leaderboards

**Key State:**
```typescript
interface AnalyticsState {
  // Overall progress
  overallProgress: OverallProgressResponse | null;

  // Achievements
  allAchievements: Achievement[];
  earnedAchievements: UserAchievement[];
  achievementProgress: AchievementProgress[];

  // User stats
  userStats: UserStats | null;

  // Leaderboards
  leaderboards: Record<LeaderboardType, LeaderboardEntry[]>;

  // Heatmaps
  activityHeatmap: HeatmapData | null;
  grammarMasteryHeatmap: HeatmapData | null;

  // Error analysis
  errorPatterns: ErrorPattern[] | null;
}
```

**Key Actions:**
- `fetchOverallProgress()` - Get overall progress summary
- `fetchAchievements()` - Load all achievements + user's earned achievements
- `fetchUserStats()` - Get user statistics for leaderboards
- `fetchLeaderboard(type)` - Load leaderboard (overall, grammar, vocabulary, streak)
- `fetchActivityHeatmap()` - Get 365-day activity heatmap
- `fetchGrammarMasteryHeatmap()` - Get grammar mastery by topic heatmap
- `fetchErrorPatterns()` - Get recurring error analysis

**Persistence:** Zustand persist middleware (selective keys)
- **Persisted:** `overallProgress`, `earnedAchievements`, `userStats`
- **Cache Duration:** No expiry (refreshed on page visit)

---

## Store Patterns

### 1. Zustand Store Creation
All stores use the `create` function from Zustand:
```typescript
import { create } from 'zustand';

export const useMyStore = create<MyState>((set, get) => ({
  // State
  data: null,

  // Actions
  setData: (data) => set({ data }),
  fetchData: async () => {
    const result = await apiService.getData();
    set({ data: result });
  },
}));
```

### 2. Persist Middleware Pattern
Stores with persistence use Zustand's persist middleware:
```typescript
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useMyStore = create<MyState>()(
  persist(
    (set, get) => ({
      // State and actions
    }),
    {
      name: 'my-storage-key',
      storage: localStorage,
      partialize: (state) => ({
        // Select which keys to persist
        user: state.user,
        settings: state.settings,
      }),
    }
  )
);
```

### 3. Session Expiry Pattern (Grammar & Conversation)
```typescript
interface StoreState {
  sessionExpiresAt: number | null;
  // other state...
}

const actions = {
  startSession: () => {
    const expiresAt = Date.now() + 24 * 60 * 60 * 1000; // 24h
    set({ sessionExpiresAt: expiresAt });
  },

  restoreSession: () => {
    const { sessionExpiresAt } = get();
    if (sessionExpiresAt && Date.now() > sessionExpiresAt) {
      // Session expired, clear state
      set({ currentSession: null, sessionExpiresAt: null });
    }
  },
};
```

### 4. Optimistic UI Updates
Some actions update UI immediately, then call API:
```typescript
const toggleBookmark = (exerciseId: number) => {
  // Optimistic update
  set((state) => ({
    bookmarked: new Set(state.bookmarked).add(exerciseId)
  }));

  // API call (fire and forget)
  apiService.bookmarkExercise(exerciseId).catch(() => {
    // Revert on error
    set((state) => {
      const bookmarked = new Set(state.bookmarked);
      bookmarked.delete(exerciseId);
      return { bookmarked };
    });
  });
};
```

---

## API Integration

### Axios Client Configuration (client.ts)

**Base Configuration:**
```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});
```

**Environment Variable:**
- **Development:** `VITE_API_BASE_URL` not set → defaults to `http://localhost:8000`
- **Production:** Set `VITE_API_BASE_URL` to actual backend URL

---

### Request Interceptor (JWT Authentication)

**Purpose:** Automatically inject JWT Bearer token in all requests

```typescript
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token');
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);
```

**Flow:**
1. Any API request made (e.g., `apiClient.get('/api/grammar/topics')`)
2. Interceptor runs before request is sent
3. Token fetched from localStorage
4. `Authorization: Bearer <token>` header added
5. Request sent to backend

---

### Response Interceptor (Error Handling)

**Purpose:** Global error handling for all API responses

```typescript
apiClient.interceptors.response.use(
  (response) => response,  // Pass through successful responses
  (error: AxiosError<any>) => {
    if (error.response) {
      // Backend responded with error status (4xx, 5xx)
      let errorMessage = 'An error occurred';

      // Case 1: FastAPI validation error (422)
      if (Array.isArray(error.response.data.detail)) {
        errorMessage = error.response.data.detail
          .map((err: any) => `${err.loc[err.loc.length - 1]}: ${err.msg}`)
          .join(', ');
      }
      // Case 2: Simple string detail
      else if (typeof error.response.data.detail === 'string') {
        errorMessage = error.response.data.detail;
      }

      // Handle 401 Unauthorized (token expired)
      if (error.response.status === 401) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('user');
        window.location.href = '/login';  // Force redirect
      }

      return Promise.reject({
        detail: errorMessage,
        status_code: error.response.status,
      } as ApiError);
    } else if (error.request) {
      // Network error (no response received)
      return Promise.reject({
        detail: 'Network error. Please check your connection.',
      } as ApiError);
    } else {
      // Other errors
      return Promise.reject({
        detail: error.message || 'An unexpected error occurred',
      } as ApiError);
    }
  }
);
```

**Error Handling Cases:**
1. **Validation Error (422):** Parse field-level errors from FastAPI
2. **Authentication Error (401):** Clear tokens, redirect to login
3. **Network Error:** Show connection error message
4. **Other Errors:** Generic error message

---

## API Services (7 classes)

All services follow the same pattern:
- Singleton instances exported as `export default new ServiceName();`
- Methods are async functions returning `Promise<T>`
- Use `apiClient` for HTTP requests
- TypeScript types from `api/types/*.types.ts`

### 1. authService (98 lines)
**Endpoints:** 3 (login, register, getCurrentUser)
**Base URL:** `/api/v1/auth`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `login(credentials)` | POST `/api/v1/auth/login` | Get JWT token, fetch user data |
| `register(userData)` | POST `/api/v1/auth/register` | Create user, auto-login |
| `getCurrentUser()` | GET `/api/v1/auth/me` | Fetch current user with token |
| `logout()` | N/A (local) | Clear localStorage |
| `isAuthenticated()` | N/A (local) | Check if token exists |
| `getStoredUser()` | N/A (local) | Parse user from localStorage |

**OAuth2 Password Flow:**
```typescript
// Login uses form data (not JSON)
const formData = new URLSearchParams();
formData.append('username', credentials.username);
formData.append('password', credentials.password);

await apiClient.post('/api/v1/auth/login', formData, {
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
});
```

---

### 2. grammarService (216 lines)
**Endpoints:** 14 grammar endpoints
**Base URL:** `/api/grammar`

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `getTopics(params)` | GET | `/api/grammar/topics` | List topics with filters |
| `getTopic(id)` | GET | `/api/grammar/topics/{id}` | Get topic with user stats |
| `startPracticeSession(request)` | POST | `/api/grammar/practice/start` | Start session |
| `getNextExercise(sessionId)` | GET | `/api/grammar/practice/{sessionId}/next` | Get exercise |
| `submitAnswer(sessionId, request)` | POST | `/api/grammar/practice/{sessionId}/answer` | Submit answer |
| `endPracticeSession(sessionId)` | POST | `/api/grammar/practice/{sessionId}/end` | End session |
| `getProgressSummary()` | GET | `/api/grammar/progress` | Overall progress |
| `getTopicProgress(topicId)` | GET | `/api/grammar/progress/topic/{topicId}` | Topic progress |
| `getWeakAreas()` | GET | `/api/grammar/progress/weak-areas` | Weak areas |
| `getReviewQueue()` | GET | `/api/grammar/review-queue` | Due topics |
| `startDiagnosticTest(request)` | POST | `/api/grammar/diagnostic/start` | Start test |
| `completeDiagnosticTest(testId)` | POST | `/api/grammar/diagnostic/complete` | Complete test |
| `generateExercises(request)` | POST | `/api/grammar/generate-exercises` | AI-generate exercises |
| `getCategories()` | GET | `/api/grammar/categories` | List categories |
| `getRecommendations()` | GET | `/api/grammar/recommendations` | Practice recommendations |

---

### 3. vocabularyService (26 endpoints)
**Base URL:** `/api/v1/vocabulary`

**Endpoint Groups:**
- **Words (3):** `getWords()`, `getWord(id)`, `createWord(word)`
- **Flashcards (3):** `startFlashcardSession()`, `submitFlashcardAnswer()`, `getCurrentFlashcard()`
- **Lists (6):** `createList()`, `getLists()`, `getList(id)`, `addWordToList()`, `removeWordFromList()`, `deleteList()`
- **Quizzes (2):** `generateQuiz()`, `submitQuizAnswer()`
- **Progress (2):** `getProgressSummary()`, `getReviewQueue()`
- **AI Features (3):** `analyzeWord()`, `detectVocabulary()`, `getRecommendations()`

---

### 4. conversationService (4 endpoints)
**Base URL:** `/api/sessions`

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `startSession(contextId)` | POST | `/api/sessions/start` | Start conversation |
| `sendMessage(sessionId, message, requestFeedback)` | POST | `/api/sessions/{sessionId}/message` | Send message |
| `endSession(sessionId)` | POST | `/api/sessions/{sessionId}/end` | End session |
| `getHistory()` | GET | `/api/sessions/history` | Get past sessions |

---

### 5. contextService (5 endpoints)
**Base URL:** `/api/contexts`

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `getContexts(filters)` | GET | `/api/contexts` | List conversation contexts |
| `getContext(id)` | GET | `/api/contexts/{id}` | Get context details |
| `createContext(context)` | POST | `/api/contexts` | Create custom context |
| `updateContext(id, context)` | PUT | `/api/contexts/{id}` | Update context |
| `deleteContext(id)` | DELETE | `/api/contexts/{id}` | Deactivate context |

---

### 6. analyticsService (14 endpoints)
**Base URL:** `/api/v1/analytics`

**Endpoint Groups:**
- **Progress (2):** `getProgress()`, `compareProgress(period1, period2)`
- **Achievements (4):** `getAchievements()`, `getEarnedAchievements()`, `getAchievementProgress()`, `showcaseAchievement(id)`
- **Stats (2):** `getUserStats()`, `refreshStats()`
- **Leaderboards (1):** `getLeaderboard(type)`
- **Heatmaps (2):** `getActivityHeatmap()`, `getGrammarMasteryHeatmap()`
- **Errors (1):** `getErrorPatterns()`
- **Snapshots (2):** `createSnapshot()`, `getSnapshots()`

---

### 7. integrationService (3 endpoints)
**Base URL:** `/api/v1/integration`

| Method | HTTP | Endpoint | Purpose |
|--------|------|----------|---------|
| `getSessionAnalysis(sessionId)` | GET | `/api/v1/integration/session-analysis/{sessionId}` | Analyze conversation |
| `getLearningPath()` | GET | `/api/v1/integration/learning-path` | Get personalized plan |
| `getDashboardData()` | GET | `/api/v1/integration/dashboard` | Unified dashboard data |

---

## TypeScript Type Definitions (7 files)

All API types are defined in `frontend/src/api/types/*.types.ts`:

### 1. auth.types.ts
- **User:** User profile (id, username, email, created_at)
- **LoginRequest:** Login credentials (username, password)
- **RegisterRequest:** Registration data (username, email, password)
- **AuthResponse:** JWT token response (access_token, token_type)

### 2. common.types.ts
- **DifficultyLevel:** `'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'`
- **MasteryLevel:** `0 | 1 | 2 | 3 | 4 | 5`
- **ApiError:** Error response (detail, status_code)
- **PaginatedResponse:** Paginated list (items, total, page, size)

### 3. grammar.types.ts (100+ lines)
- **GrammarTopic:** Topic definition
- **GrammarExercise:** Exercise with question, answer, hints
- **ExerciseType:** `fill_blank | multiple_choice | translation | error_correction | sentence_building`
- **PracticeSessionResponse:** Session metadata
- **ExerciseFeedback:** Answer feedback with corrections
- **SessionProgress:** Session stats (accuracy, points, streak)

### 4. vocabulary.types.ts
- **VocabularyWord:** Word definition (word, translation, difficulty, category)
- **VocabularyWithProgress:** Word with user progress
- **FlashcardResponse:** Flashcard data (front, back, hint, card_type)
- **PersonalVocabularyList:** User-created word list
- **VocabularyQuizResponse:** Quiz questions

### 5. conversation.types.ts
- **Context:** Conversation scenario (name, description, difficulty)
- **ConversationSession:** Active session (id, context, start_time)
- **ConversationTurnResponse:** Message exchange (user message, AI response, grammar feedback)
- **GrammarFeedback:** Grammar corrections from AI

### 6. analytics.types.ts
- **Achievement:** Achievement definition (name, description, tier, points)
- **UserAchievement:** User's earned achievement (earned_at, progress)
- **UserStats:** User statistics (total_time, exercises_completed, accuracy)
- **LeaderboardEntry:** Leaderboard rank (rank, username, score)
- **HeatmapData:** Heatmap data points (date, value, intensity)

### 7. integration.types.ts
- **DashboardData:** Unified dashboard (overall_progress, due_items, quick_actions, recent_activity)
- **LearningPath:** Personalized plan (daily_plan, weekly_goals, recommendations)
- **SessionAnalysis:** Conversation analysis (grammar_topics, vocabulary_words, recommendations)

---

## Data Flow Patterns

### Pattern 1: Component → Store → API → Store → Component

**Example: Loading Grammar Topics**
```typescript
// 1. Component calls store action
function GrammarTopicsPage() {
  const fetchTopics = useGrammarStore((state) => state.fetchTopics);

  useEffect(() => {
    fetchTopics();
  }, []);

  const topics = useGrammarStore((state) => state.topics);

  return <div>{topics.map(topic => <TopicCard key={topic.id} topic={topic} />)}</div>;
}

// 2. Store action calls API service
const fetchTopics = async () => {
  const topics = await grammarService.getTopics();
  set({ topics });
};

// 3. API service makes HTTP request
const getTopics = async () => {
  const response = await apiClient.get<GrammarTopic[]>('/api/grammar/topics');
  return response.data;
};

// 4. Axios interceptor adds JWT token
// 5. Backend responds with data
// 6. Store updates state
// 7. Component re-renders with new data
```

---

### Pattern 2: Session Persistence Flow

**Example: Grammar Session Restore**
```typescript
// 1. App mounts, store initialized
useEffect(() => {
  const restoreSession = useGrammarStore((state) => state.restoreSession);
  restoreSession();
}, []);

// 2. Store checks expiry
const restoreSession = () => {
  const { sessionExpiresAt, currentSession } = get();

  // Check if session expired (24h)
  if (sessionExpiresAt && Date.now() > sessionExpiresAt) {
    set({ currentSession: null, sessionExpiresAt: null });
    return;
  }

  // Session still valid, keep state
  if (currentSession) {
    set({ sessionState: 'in_progress' });
  }
};

// 3. Zustand persist middleware automatically saves/loads from localStorage
```

---

### Pattern 3: Error Handling Flow

**Example: API Error → Interceptor → Toast**
```typescript
// 1. Component calls store action
const submitAnswer = useGrammarStore((state) => state.submitAnswer);
const addToast = useNotificationStore((state) => state.addToast);

try {
  await submitAnswer('My answer');
} catch (error) {
  const apiError = error as ApiError;
  addToast('error', 'Submission failed', apiError.detail);
}

// 2. Store action calls API
const submitAnswer = async (answer: string) => {
  const response = await grammarService.submitAnswer(sessionId, { user_answer: answer });
  set({ feedback: response.feedback });
};

// 3. API service makes request
const submitAnswer = async (sessionId, request) => {
  const response = await apiClient.post(`/api/grammar/practice/${sessionId}/answer`, request);
  return response.data;
};

// 4. Backend returns 4xx/5xx error
// 5. Response interceptor catches error, formats ApiError
// 6. Promise rejected with ApiError
// 7. Component catch block shows toast
```

---

## Custom Hooks (3 hooks)

### 1. useKeyboardShortcuts.ts (~50+ lines shown)
**Purpose:** Comprehensive keyboard navigation across all modules

**Features:**
- Context-based shortcut registration (e.g., grammar vs. vocabulary shortcuts)
- Modifier key support (Ctrl, Shift, Alt, Meta)
- Input field awareness (some shortcuts disabled in input fields)
- Priority system (higher priority contexts handle events first)

**Common Shortcuts:**
- **Enter:** Submit answer, send message, continue
- **Escape:** Close modal, cancel action, return to previous screen
- **Arrow Keys:** Navigate exercises, flip cards, move through quiz questions
- **Numbers (1-5):** Rate flashcards (1=Again, 2=Hard, 3=Good, 4=Easy, 5=Perfect)
- **F:** Flip flashcard
- **N:** Next exercise/card
- **S:** Skip exercise
- **B:** Bookmark exercise

**Usage:**
```typescript
useKeyboardShortcuts({
  enabled: true,
  contexts: [
    {
      id: 'grammar-session',
      shortcuts: [
        { key: 'Enter', action: handleSubmit, description: 'Submit answer' },
        { key: 'Escape', action: handleCancel, description: 'Cancel' },
      ],
    },
  ],
});
```

---

### 2. useSessionPersistence.ts
**Purpose:** Auto-save session state every 30 seconds

**Features:**
- Automatic state persistence to localStorage
- Configurable save interval (default 30s)
- Debounced saves (prevents excessive writes)
- Session expiry handling

**Usage:**
```typescript
useSessionPersistence({
  sessionId: currentSession?.id,
  state: {
    exercises: exercises,
    userAnswers: userAnswers,
    sessionProgress: sessionProgress,
  },
  onExpire: () => {
    clearSession();
    navigate('/grammar');
  },
});
```

---

### 3. useAutoScroll.ts
**Purpose:** Smooth scroll to bottom on new messages/exercises

**Features:**
- Auto-scroll when dependencies change (e.g., new message added)
- Smooth scroll behavior
- Scroll threshold detection (don't auto-scroll if user scrolled up)
- Manual scroll button when user is not at bottom

**Usage:**
```typescript
const { containerRef, messagesEndRef, handleScroll } = useAutoScroll(
  [messages.length, isTyping],  // Dependencies
  100  // Scroll delay (ms)
);

return (
  <div ref={containerRef} onScroll={handleScroll}>
    {messages.map(msg => <MessageBubble key={msg.id} message={msg} />)}
    <div ref={messagesEndRef} />  {/* Scroll anchor */}
  </div>
);
```

---

## Backend Integration

### Consumed Endpoints (74 total)

| Module | Endpoints | Service Class |
|--------|-----------|---------------|
| Authentication | 3 | authService |
| Conversations | 4 | conversationService |
| Contexts | 5 | contextService |
| Grammar | 14 | grammarService |
| Vocabulary | 26 | vocabularyService |
| Analytics | 14 | analyticsService |
| Integration | 3 | integrationService |
| Health | 2 | N/A (rarely used) |

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Related Areas

- **[Frontend Architecture](./frontend.md)** - Overall structure, routing, build configuration
- **[Frontend Components](./frontend-components.md)** - UI components consuming store state
- **[Backend API](./backend-api.md)** - REST endpoints and request/response schemas
- **[Backend Database](./backend-database.md)** - Data models and relationships
- **[Frontend Development Guide](../GUIDES/frontend.md)** - State management best practices

---

**Quick Navigation:**
- [← Back to Frontend Architecture](./frontend.md)
- [← Back to Frontend Components](./frontend-components.md)
- [← Back to Codemaps Index](./README.md)
