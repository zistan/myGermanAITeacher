# Frontend Components Codemap

**Last Updated:** 2026-01-24
**Entry Points:** `frontend/src/components/` (81 components), `frontend/src/pages/` (26 pages)

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Atomic Design Pattern                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐      ┌─────────────────┐      ┌──────────────────┐
│ Common (12)   │      │ Feature-Specific│      │ Page Components  │
│ Presentational│      │ Components (65) │      │ (26)             │
│               │      │                 │      │                  │
│ • Button      │      │ Grammar (7)     │      │ Auth (2)         │
│ • Card        │      │ Vocabulary (26) │      │ Grammar (5)      │
│ • Badge       │──────│ Conversation (13│──────│ Vocabulary (6)   │
│ • Modal       │      │ Dashboard (6)   │      │ Conversation (4) │
│ • Loading     │      │ Analytics (10)  │      │ Analytics (5)    │
│ • Toast       │      │ Learning Path(4)│      │ Learning Path(1) │
│               │      │ Layout (4)      │      │ Dashboard (1)    │
└───────────────┘      └─────────────────┘      └──────────────────┘
        │                        │                        │
        └────────────────────────▼────────────────────────┘
                                 │
                          Barrel Exports
                    (index.ts in each directory)
```

## Component Organization by Module

### Common Components (12 files)
**Location:** `frontend/src/components/common/`
**Purpose:** Reusable presentational components used across all modules

| Component | Purpose | Props | Key Features |
|-----------|---------|-------|--------------|
| **Button** | Action trigger | variant, size, isLoading, icons | 4 variants (primary/secondary/danger/ghost), 3 sizes, loading state |
| **Card** | Content container | header, footer, padding | Flexible layout with optional header/footer |
| **Badge** | Status/category label | variant, size | Multiple color variants, compact display |
| **Loading** | Loading indicator | fullScreen, size, text | Spinner with optional full-screen overlay |
| **ProgressBar** | Visual progress | value, max, color, label | Percentage-based progress with label |
| **Skeleton** | Content placeholder | lines, height, width | Loading skeleton for async content |
| **Modal** | Dialog overlay | isOpen, onClose, title, size | Headless UI Dialog with 5 sizes, animations |
| **Toast** | Notification | type, message, duration | Success/error/info/warning notifications |
| **Dropdown** | Select menu | items, onSelect, trigger | Headless UI Menu with keyboard navigation |
| **Table** | Data grid | columns, data, onSort | Sortable columns, pagination support |
| **EmptyState** | No data message | icon, title, description | Centered empty state display |
| **ErrorBoundary** | Error catcher | fallback, onError | React error boundary wrapper |

**Component Pattern Example (Button):**
```typescript
<Button
  variant="primary"     // primary | secondary | danger | ghost
  size="md"             // sm | md | lg
  isLoading={false}     // Shows spinner
  leftIcon={<Icon />}   // Optional left icon
  fullWidth={false}     // Full width button
>
  Submit
</Button>
```

---

### Grammar Components (7 files)
**Location:** `frontend/src/components/grammar/`
**Purpose:** Grammar practice session components

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **ExerciseRenderer** | Renders exercise types | 5 exercise types (fill_blank, multiple_choice, translation, error_correction, sentence_building) |
| **FeedbackDisplay** | Shows answer feedback | Correct/incorrect state, explanation, text diff highlighting |
| **SessionHeader** | Session progress bar | Exercise count, timer, accuracy, difficulty badge |
| **SessionControls** | Action buttons | Skip, bookmark, note, end session, keyboard shortcuts |
| **TextDiff** | Highlights differences | Uses diff-match-patch for user answer vs correct answer comparison |
| **NotesList** | Session notes display | List of bookmarked exercises with notes |
| **TopicCard** | Topic selection card | Topic name, difficulty, progress, mastery level |

**Exercise Types:**
- **fill_blank:** Text input for fill-in-the-blank questions
- **multiple_choice:** Radio buttons for single selection
- **translation:** Textarea for German translations
- **error_correction:** Textarea for fixing grammatical errors
- **sentence_building:** Text input for word reordering

**Design Pattern:** Compound components with ExerciseRenderer as main renderer switching between exercise types

---

### Vocabulary Components (26 files)
**Location:** `frontend/src/components/vocabulary/`
**Purpose:** Vocabulary learning, flashcards, lists, and quizzes

#### Core Components (4)
| Component | Purpose | Props |
|-----------|---------|-------|
| **WordCard** | Word display card | word, onClick, showProgress |
| **MasteryIndicator** | Mastery level visual | level (0-5), size |
| **DifficultyBadge** | Difficulty label | level (A1-C2), size |
| **CategoryBadge** | Category label | category, variant |

#### Browser Components (2)
| Component | Purpose | Features |
|-----------|---------|----------|
| **WordFilters** | Search and filters | Search, difficulty, category, mastery filters |
| **WordDetailModal** | Word details popup | Definition, examples, progress, actions |

#### Flashcard Components (4)
| Component | Purpose | Features |
|-----------|---------|----------|
| **FlashcardDisplay** | 3D flip card | Front/back with flip animation, 5 card types |
| **FlashcardControls** | Rating buttons | 5-level confidence rating (1-5) |
| **FlashcardSessionSetup** | Session config | Difficulty, category, count selection |
| **FlashcardSessionSummary** | Results display | Total cards, accuracy, time, performance breakdown |

**Flashcard Types:**
- **definition:** Word → Definition
- **translation:** German → Italian
- **usage:** Word → Usage context
- **synonym:** Word → Synonyms
- **example:** Word → Example sentence

**3D Flip Animation:** CSS transform with 500ms transition, perspective: 1000px

#### List Components (3)
| Component | Purpose | Features |
|-----------|---------|----------|
| **ListCard** | List overview card | Name, word count, public/private badge, actions |
| **CreateListModal** | New list form | Name, description, visibility (public/private) |
| **AddWordToListModal** | Add word to lists | Select from user's lists, create new list option |

#### Quiz Components (4)
| Component | Purpose | Features |
|-----------|---------|----------|
| **QuizSetup** | Quiz configuration | Type (multiple_choice/fill_blank/matching), count, filters |
| **QuizQuestion** | Question display | Renders based on quiz type, user input |
| **QuizFeedback** | Answer feedback | Correct/incorrect state, explanation |
| **QuizResults** | Quiz summary | Score, time, accuracy, detailed results |

#### Progress Components (5)
| Component | Purpose | Features |
|-----------|---------|----------|
| **ProgressOverview** | Progress summary | Total words, mastery breakdown, review queue |
| **MasteryChart** | Mastery distribution | Bar chart of mastery levels (0-5) |
| **CategoryBreakdown** | Category stats | Words per category with progress |
| **ReviewQueue** | Due words list | Words due for review with mastery indicators |
| **WordRecommendations** | Suggested words | AI-recommended words based on progress |

---

### Conversation Components (13 files)
**Location:** `frontend/src/components/conversation/`
**Purpose:** AI conversation practice interface

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **ChatInterface** | Main conversation UI | Message list, typing indicator, chat input, auto-scroll |
| **MessageBubble** | Single message display | User/AI styling, grammar feedback, vocabulary highlights |
| **ChatInput** | Message input field | Textarea with German characters (ä, ö, ü, ß), feedback toggle |
| **TypingIndicator** | AI typing animation | Three animated dots |
| **GrammarFeedbackPanel** | Grammar corrections | Detected errors with explanations |
| **VocabularyHighlight** | Clickable vocabulary | Highlighted words with click handler |
| **ContextCard** | Context selection card | Name, description, difficulty, usage stats |
| **ContextBadge** | Context category label | Business/daily life categories |
| **SessionTimer** | Session duration | Running timer with start/end timestamps |
| **MessageActions** | Message menu | Copy, translate, practice grammar/vocabulary |
| **EndSessionModal** | Session end confirmation | Summary stats, save/discard options |
| **SessionSummary** | Completed session stats | Duration, messages, grammar feedback count |
| **EmptyConversationState** | No messages yet | Tips for better practice, German characters guide |

**Message Flow:**
1. User types in ChatInput (with German character buttons)
2. Optional: Toggle "Request Grammar Feedback" checkbox
3. Message sent → TypingIndicator appears
4. AI response → MessageBubble with optional grammar feedback
5. Grammar errors → GrammarFeedbackPanel with corrections
6. Vocabulary words → VocabularyHighlight (clickable)

**Auto-Scroll Hook:** `useAutoScroll` hook automatically scrolls to latest message with smooth behavior

---

### Dashboard Components (6 files)
**Location:** `frontend/src/components/dashboard/`
**Purpose:** Dashboard widget cards for unified overview

| Component | Purpose | Data Displayed |
|-----------|---------|----------------|
| **OverallProgressCard** | Overall progress | Progress score (0-100), module breakdown (grammar/vocab/conversation) |
| **CurrentStreakCard** | Activity streak | Current streak, longest streak, days active |
| **DueItemsCard** | Items for review | Grammar topics due, vocabulary words due, action buttons |
| **QuickActionsCard** | Suggested actions | AI-recommended next steps with priorities |
| **RecentActivityCard** | Activity timeline | Last 5 activities with timestamps and types |
| **AchievementsBadge** | Close achievements | Achievements near completion with progress bars |

**Data Source:** All components consume data from `integrationService.getDashboardData()` which returns unified dashboard data

**Layout Pattern:** Grid layout with 2 columns on large screens, stacked on mobile

---

### Analytics Components (10 files)
**Location:** `frontend/src/components/analytics/`
**Purpose:** Progress visualizations and analytics displays

| Component | Purpose | Visualization |
|-----------|---------|---------------|
| **AchievementCard** | Achievement display | Icon, name, tier, progress bar, earned badge |
| **AchievementFilters** | Achievement filters | Category, tier, status filters |
| **ShowcaseToggle** | Showcase star button | Star toggle for earned achievements |
| **ProgressChart** | Progress over time | Line chart with date range selector |
| **PieChart** | Category distribution | Recharts pie chart with legend |
| **StatCard** | Metric display card | Value, label, trend indicator |
| **ModuleStatsCard** | Module statistics | Progress bar, 4-stat grid |
| **HeatmapGrid** | Activity/mastery heatmap | 365-day calendar grid with color intensity |
| **LeaderboardTable** | Rankings list | Rank, username, score, badges |
| **ErrorAnalysisCard** | Error patterns | Recurring errors with frequency |

**Charting Library:** Recharts 3.7.0 for responsive, accessible charts

**Heatmap Pattern:**
- Activity heatmap: 365-day grid, green intensity based on minutes studied
- Grammar mastery heatmap: Per-topic grid, color based on mastery level (0.0-1.0)

**Achievement Tiers:**
- **Bronze:** Slate (border-slate-400, bg-slate-50)
- **Silver:** Blue (border-blue-400, bg-blue-50)
- **Gold:** Amber (border-amber-400, bg-amber-50)
- **Platinum:** Purple (border-purple-400, bg-purple-50)

---

### Learning Path Components (4 files)
**Location:** `frontend/src/components/learning-path/`
**Purpose:** Personalized learning recommendations and daily study plans

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **DailyPlan** | Daily study plan | 75-minute timeline breakdown (15 vocab + 30 grammar + 30 conversation), time-of-day emojis (🌅🌙), priority badges, "Start Now" buttons |
| **FocusArea** | Priority weak areas | 4 priority levels (critical/high/medium/low) with color coding, module badges, "Start Practice" quick actions |
| **WeeklyGoals** | Weekly targets | Session goals, focus distribution, milestone checklist, gradient background (primary-500 → primary-700) |
| **RecommendedContext** | Context suggestions | Priority border colors, category icons, stats (difficulty, practice count), "Start Conversation" navigation |

**Priority Color System:**
- **Critical:** Red (border-red-500, bg-red-50, text-red-700)
- **High:** Orange (border-orange-500, bg-orange-50, text-orange-700)
- **Medium:** Yellow (border-yellow-500, bg-yellow-50, text-yellow-700)
- **Low:** Blue (border-blue-500, bg-blue-50, text-blue-700)

**Module Color Coding:**
- **Grammar:** Blue (bg-blue-100, text-blue-700)
- **Vocabulary:** Green (bg-green-100, text-green-700)
- **Conversation:** Purple (bg-purple-100, text-purple-700)

**Design Pattern:** Card-based layout with border-left-4 accent, responsive grid (1/2/3 columns based on screen size)

---

### Layout Components (4 files)
**Location:** `frontend/src/components/layout/`
**Purpose:** Application layout structure and navigation

| Component | Purpose | Key Features |
|-----------|---------|--------------|
| **Layout** | Main layout wrapper | Sidebar + Header + content area, mobile-responsive |
| **Sidebar** | Navigation menu | Module links, collapsible on mobile, active route highlighting |
| **Header** | Top app bar | Hamburger menu (mobile), user profile, logout button |
| **ProtectedRoute** | Auth guard | Redirects to /login if not authenticated |

**Layout Structure:**
```
<Layout>
  <Sidebar />
  <div className="flex-1 flex flex-col">
    <Header />
    <main>{children}</main>
  </div>
</Layout>
```

**Navigation Links (Sidebar):**
- Dashboard → `/dashboard`
- Grammar → `/grammar`
- Vocabulary → `/vocabulary`
- Conversation → `/conversation`
- Analytics → `/analytics/progress`

**Mobile Behavior:** Sidebar hidden by default, toggles via hamburger menu in Header

---

## Page Components (23 files)

### Authentication Pages (2)
**Location:** `frontend/src/pages/auth/`

| Page | Route | Purpose |
|------|-------|---------|
| **LoginPage** | `/login` | Login form with email/password, redirect to /dashboard |
| **RegisterPage** | `/register` | Registration form with email/username/password |

---

### Dashboard Page (1)
**Location:** `frontend/src/pages/`

| Page | Route | Purpose | Components Used |
|------|-------|---------|-----------------|
| **DashboardPage** | `/dashboard` | Unified overview | OverallProgressCard, CurrentStreakCard, DueItemsCard, QuickActionsCard, RecentActivityCard |

**Data Flow:**
1. `useEffect` calls `integrationService.getDashboardData()`
2. Data stored in local state
3. Passed as props to dashboard components

---

### Grammar Pages (5)
**Location:** `frontend/src/pages/grammar/`

| Page | Route | Purpose | Key Components |
|------|-------|---------|----------------|
| **GrammarTopicsPage** | `/grammar` | Browse topics | TopicCard, difficulty filters |
| **PracticeSessionPage** | `/grammar/practice` | Practice session | ExerciseRenderer, FeedbackDisplay, SessionHeader, SessionControls |
| **ProgressPage** | `/grammar/progress` | Grammar progress | ProgressChart, mastery breakdown by topic |
| **ReviewQueuePage** | `/grammar/review-queue` | Due topics | List of topics due for review |
| **ResultsPage** | `/grammar/results` | Session results | Accuracy, time, exercises completed, notes |

**Session Flow:**
1. GrammarTopicsPage: Select topic + difficulty
2. PracticeSessionPage: Complete exercises
3. ResultsPage: View session summary

**Session Persistence:** 24h localStorage via Zustand persist middleware (see frontend-state.md)

---

### Vocabulary Pages (6)
**Location:** `frontend/src/pages/vocabulary/`

| Page | Route | Purpose | Key Components |
|------|-------|---------|----------------|
| **VocabularyBrowserPage** | `/vocabulary` | Browse words | WordCard, WordFilters, WordDetailModal |
| **FlashcardSessionPage** | `/vocabulary/flashcards` | Flashcard practice | FlashcardDisplay, FlashcardControls, FlashcardSessionSummary |
| **VocabularyListsPage** | `/vocabulary/lists` | Manage lists | ListCard, CreateListModal |
| **VocabularyListDetailPage** | `/vocabulary/lists/:id` | View list words | WordCard, AddWordToListModal |
| **VocabularyQuizPage** | `/vocabulary/quiz` | Quiz session | QuizQuestion, QuizFeedback, QuizResults |
| **VocabularyProgressPage** | `/vocabulary/progress` | Vocabulary stats | MasteryChart, CategoryBreakdown, ReviewQueue |

**Flashcard Flow:**
1. FlashcardSessionSetup modal: Select difficulty, category, count
2. FlashcardSessionPage: Practice cards with flip animation
3. FlashcardSessionSummary: View results

---

### Conversation Pages (4)
**Location:** `frontend/src/pages/conversation/`

| Page | Route | Purpose | Key Components |
|------|-------|---------|----------------|
| **ContextsPage** | `/conversation` | Select context | ContextCard, context filters |
| **PracticePage** | `/conversation/practice` | Active conversation | ChatInterface, GrammarFeedbackPanel, SessionTimer |
| **HistoryPage** | `/conversation/history` | Past sessions | Session list with timestamps |
| **SessionDetailPage** | `/conversation/session/:id` | View past session | Full message history, grammar feedback |

**Conversation Flow:**
1. ContextsPage: Select conversation context (business meeting, restaurant, etc.)
2. PracticePage: Chat with AI in German
3. End session → HistoryPage: View all past sessions
4. SessionDetailPage: Review specific session

---

### Analytics Pages (5)
**Location:** `frontend/src/pages/analytics/`

| Page | Route | Purpose | Key Components |
|------|-------|---------|----------------|
| **ProgressOverviewPage** | `/analytics/progress` | Overall progress | ProgressChart, module breakdown, improvement trends |
| **AchievementsPage** | `/analytics/achievements` | Achievement showcase | AchievementGrid, filters by category/tier |
| **HeatmapPage** | `/analytics/heatmaps` | Activity/mastery heatmaps | HeatmapGrid (activity + grammar mastery) |
| **LeaderboardPage** | `/analytics/leaderboards` | Rankings | LeaderboardTable (overall, grammar, vocabulary, streak) |
| **ErrorAnalysisPage** | `/analytics/errors` | Error patterns | ErrorAnalysisCard, recurring mistakes |

---

### Learning Path Page (1)
**Location:** `frontend/src/pages/`

| Page | Route | Purpose | Key Components |
|------|-------|---------|----------------|
| **LearningPathPage** | `/learning-path` | Personalized study plan | DailyPlan, FocusArea, WeeklyGoals, RecommendedContext |

**Data Flow:**
1. Page loads → `integrationService.getLearningPath()` API call
2. Backend analyzes user progress (grammar/vocabulary/conversation)
3. Returns: motivation message, daily plan, focus areas, weekly goals, context recommendations
4. Components render with navigation to practice pages

**Key Features:**
- AI-generated 75-minute daily breakdown (15 min vocab + 30 min grammar + 30 min conversation)
- Priority-coded focus areas (critical/high/medium/low)
- Weekly session goals with module distribution
- Recommended contexts prioritizing unpracticed scenarios
- One-click "Start" navigation to all modules

---

## Component Patterns

### 1. Presentational vs. Container Components
- **Presentational:** Common components (Button, Card, Badge) - no business logic
- **Container:** Page components (DashboardPage, PracticePage) - data fetching, state management

### 2. Compound Components
**Example: Flashcard System**
```tsx
<FlashcardDisplay card={card} isFlipped={isFlipped} onFlip={handleFlip} />
<FlashcardControls onRate={handleRate} disabled={!isFlipped} />
```
- FlashcardDisplay: Visual card component
- FlashcardControls: Separate control buttons
- Both work together but are independent

### 3. Render Props Pattern
**Example: TextDiff Component**
```tsx
<TextDiff
  original={correctAnswer}
  modified={userAnswer}
  render={(parts) => (
    <div>
      {parts.map((part, i) => (
        <span key={i} className={part.added ? 'bg-green-100' : part.removed ? 'bg-red-100' : ''}>
          {part.value}
        </span>
      ))}
    </div>
  )}
/>
```

### 4. Higher-Order Components
**Example: ProtectedRoute**
```tsx
<ProtectedRoute>
  <Layout>
    <DashboardPage />
  </Layout>
</ProtectedRoute>
```
Wraps content to check authentication before rendering

### 5. Custom Hooks Integration
- **useKeyboardShortcuts:** Module-specific shortcuts (e.g., Enter to submit exercise)
- **useSessionPersistence:** Auto-save session state every 30 seconds
- **useAutoScroll:** Smooth scroll to bottom on new messages

---

## Props & TypeScript Interfaces

### Common Prop Patterns

**1. Variant Props (Union Types):**
```typescript
variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
size?: 'sm' | 'md' | 'lg'
```

**2. Event Handler Props:**
```typescript
onClick?: () => void
onChange?: (value: string) => void
onSubmit?: (data: FormData) => Promise<void>
```

**3. Data Props (Typed Objects):**
```typescript
exercise: GrammarExercise
word: VocabularyWord
message: ConversationTurnResponse
```

**4. Display Props (Booleans/Optional):**
```typescript
isLoading?: boolean
showFeedback?: boolean
disabled?: boolean
```

### Type Definition Imports
All components import types from `api/types/`:
- `grammar.types.ts` → GrammarExercise, GrammarTopic, etc.
- `vocabulary.types.ts` → VocabularyWord, FlashcardResponse, etc.
- `conversation.types.ts` → ConversationTurnResponse, Context, etc.
- `common.types.ts` → PaginatedResponse, ApiError, etc.

---

## Styling Patterns

### Tailwind Utility Classes
**Consistent patterns across all components:**

**1. Color Scheme (German Flag Theme):**
```css
/* Primary (Gold): bg-primary-500, text-primary-600, border-primary-500 */
/* Danger (Red): bg-danger-500, text-danger-600, border-danger-500 */
/* Neutral: bg-gray-50, text-gray-900, border-gray-200 */
```

**2. Spacing Scale:**
```css
/* Padding: p-4 (16px), p-6 (24px), p-8 (32px) */
/* Margin: mb-4, mt-6, space-y-4 (vertical gap) */
```

**3. Responsive Design:**
```css
/* Mobile-first approach */
className="px-4 sm:px-6 lg:px-8"  /* Responsive padding */
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3"  /* Responsive grid */
```

**4. Interactive States:**
```css
/* Hover: hover:bg-primary-600, hover:text-gray-900 */
/* Focus: focus:ring-2 focus:ring-primary-500 focus:outline-none */
/* Disabled: disabled:opacity-50 disabled:cursor-not-allowed */
```

**5. Animations:**
```css
/* Transitions: transition-colors duration-200 */
/* Loading spinner: animate-spin */
/* Flashcard flip: transition-transform duration-500 */
```

### Conditional Styling with clsx
```typescript
import clsx from 'clsx';

className={clsx(
  'base-classes',
  variant === 'primary' && 'bg-primary-500',
  isActive && 'border-2 border-primary-500',
  className  // Allow prop override
)}
```

---

## Reusability Patterns

### 1. Barrel Exports (index.ts)
Every component directory exports via index.ts:
```typescript
// components/common/index.ts
export { Button } from './Button';
export type { ButtonProps } from './Button';
```

**Benefits:**
- Clean imports: `import { Button, Card } from '../common'`
- Type exports alongside components
- Centralized component API

### 2. Component Composition
Build complex UIs from simple components:
```tsx
<Card header={<h2>Session Progress</h2>}>
  <ProgressBar value={75} max={100} />
  <Button variant="primary">Continue</Button>
</Card>
```

### 3. Shared Utilities
- **textDiff.ts:** Text difference highlighting (used in grammar feedback)
- **clsx:** Conditional className merging (used in all components)
- **date-fns:** Date formatting (used in timestamps, heatmaps)

### 4. Component Variants
Single component with multiple variants reduces duplication:
- Button: primary, secondary, danger, ghost
- Badge: Multiple colors, sizes
- Modal: 5 sizes (sm, md, lg, xl, full)

---

## Accessibility Features

### Keyboard Navigation
- **Tab Index:** All interactive elements keyboard-accessible
- **Focus States:** Visible focus rings on all inputs/buttons
- **Keyboard Shortcuts:** Via useKeyboardShortcuts hook
  - Enter: Submit answer/send message
  - Escape: Close modal/cancel action
  - Arrow keys: Navigate exercises/cards

### Screen Reader Support
- **Semantic HTML:** button, nav, main, header, footer
- **ARIA Labels:** aria-label, aria-describedby on interactive elements
- **Headless UI:** Accessible components (Dialog, Menu, Disclosure)
- **Test IDs:** data-testid on components for testing

### Visual Accessibility
- **Color Contrast:** WCAG AA compliant (4.5:1 ratio)
- **Focus Indicators:** 2px ring on focus
- **Text Sizing:** Responsive text (text-base, text-lg)
- **Loading States:** Clear loading indicators

---

## Related Areas

- **[Frontend Architecture](./frontend.md)** - Overall frontend structure, routing, and configuration
- **[Frontend State Management](./frontend-state.md)** - Zustand stores, API integration, and data flow
- **[Backend API](./backend-api.md)** - REST endpoints consumed by frontend services
- **[Frontend Development Guide](../GUIDES/frontend.md)** - Component development best practices

---

**Quick Navigation:**
- [← Back to Frontend Architecture](./frontend.md)
- [Frontend State Management →](./frontend-state.md)
- [← Back to Codemaps Index](./README.md)
