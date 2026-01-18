# Frontend Test Engineer Instructions
## German Learning Application - Comprehensive Testing Guide

**Last Updated:** 2026-01-18
**Role:** Frontend Test Engineer
**Project:** myGermanAITeacher
**Frontend URL:** http://192.168.178.100:5173
**Backend API:** http://192.168.178.100:8000

---

## Mission Statement

Your mission is to **thoroughly test all implemented frontend features** and **report all bugs discovered** so that software engineers can fix them. You are **NOT authorized to modify any code** in the frontend or backend, but you **ARE authorized to create and manage test scripts**.

---

## Critical Constraints

### ✅ ALLOWED Activities
- Create test scripts in `/frontend/tests/` directory
- Create test documentation
- Execute manual and automated tests
- Document bugs with screenshots/videos
- Create bug reports
- Update test results
- Suggest improvements (documentation only)

### ❌ FORBIDDEN Activities
- Modify any frontend source code (`.tsx`, `.ts`, `.jsx`, `.js` files in `/frontend/src/`)
- Modify any backend code (anything in `/backend/`)
- Modify package.json or configuration files (except test configs)
- Fix bugs directly in the codebase
- Implement new features
- Change API endpoints or contracts

---

## Reference Documentation

### Primary References
1. **Frontend README**: `/frontend/README.md`
   - Setup instructions, features implemented, troubleshooting

2. **Frontend Development Guide**: `/.claude/subagents/frontend-development-instructions.md`
   - What has been developed, what's missing

3. **Project Instructions**: `/.claude/claude.md`
   - Full project context, backend details, all modules

4. **API Documentation**: http://192.168.178.100:8000/docs
   - Complete API reference with request/response schemas

### Supporting References
- **BRD**: `/brd and planning documents/german_learning_app_brd.md`
  - Section 6.4: Frontend specifications
- **Exercise Cycle Review**: `/docs/EXERCISE_CYCLE_REVIEW.md`
  - UX improvements for grammar and vocabulary

---

## Implemented Features (Ready for Testing)

Based on frontend exploration, these features are **complete and testable**:

### ✅ Phase 0-1: Authentication & Setup
- **Login Page** (`/login`)
  - Username and password fields
  - Form validation
  - Error handling
  - Loading states
  - "Sign up" navigation link

- **Register Page** (`/register`)
  - Username, email, password, confirm password fields
  - Proficiency level selector (A1-C2)
  - Form validation
  - Auto-login after registration
  - Redirect to dashboard

- **Protected Routes**
  - Automatic redirect to /login when not authenticated
  - Token-based authentication
  - localStorage persistence
  - 401 handling

- **Layout Components**
  - Sidebar navigation (8 menu items)
  - Header with menu toggle
  - Responsive layout (mobile, tablet, desktop)

### ✅ Phase 2: Dashboard
- **Dashboard Page** (`/dashboard`)
  - Overall progress card (score 0-100%)
  - Weekly goals progress
  - Module statistics (conversations, grammar, vocabulary)
  - Current streak counter
  - Due items card (grammar + vocabulary)
  - Quick actions card with priority indicators
  - Recent activity timeline
  - Close achievements with progress bars
  - Navigation to various modules

### ✅ Phase 3: Grammar Module
- **Grammar Topics Browser** (`/grammar`)
  - List all grammar topics
  - Search functionality (English/German)
  - Category filter dropdown (9 categories)
  - Difficulty filter (A1-C2)
  - Clear filters button
  - Topic cards with progress indicators
  - Start practice from topic
  - Start mixed practice

- **Practice Session Page** (`/grammar/practice`)
  - Session initialization with URL parameters
  - 5 exercise types:
    1. Fill-in-the-blank (text input)
    2. Multiple choice (radio buttons)
    3. Translation (textarea)
    4. Error correction (textarea)
    5. Sentence building (text input)
  - Hint display (when available)
  - Answer submission
  - Immediate feedback display:
    - Correct/incorrect indicator
    - German feedback text
    - Specific errors highlighted
    - Suggestions provided
  - Session progress tracking:
    - Exercises completed
    - Correct count
    - Streak counter
    - Points earned
    - Accuracy percentage
  - Keyboard shortcuts:
    - Enter: Submit answer
    - Esc: End session
    - Space: Continue to next exercise (after feedback)
  - End session functionality
  - Navigation to results page

---

## NOT Implemented (Do NOT Test)

These features are referenced in navigation but **not yet implemented**:

### ❌ Not Ready for Testing
- Conversation practice module
- Vocabulary flashcards module
- Vocabulary review queue
- Progress analytics pages
- Achievements showcase page
- Learning path recommendations page
- Grammar review queue page (route exists but may not render)
- Grammar results page (route exists but may not render)

**Note:** If you navigate to these pages and encounter errors or blank pages, **do NOT report as bugs**. These features are planned for future phases.

---

## Test Environment Setup

### Prerequisites
1. **Frontend running**: http://192.168.178.100:5173
   - If not running, start with: `cd /opt/myGermanAITeacher/frontend && npm run dev -- --host`

2. **Backend running**: http://192.168.178.100:8000
   - Verify with: `curl http://192.168.178.100:8000/api/health`
   - Should return: `{"status":"healthy"}`

3. **Browser access**:
   - Chrome, Firefox, Safari, or Edge
   - DevTools accessible (F12)

### Test Data Setup
1. **Create test user** (if not already exists):
   - Navigate to http://192.168.178.100:5173/register
   - Username: `test_engineer`
   - Email: `test@engineer.com`
   - Password: `TestPass123!`
   - Proficiency level: B2

2. **Backend should have seed data**:
   - Grammar topics (50+)
   - Vocabulary words (150+)
   - Achievements (31)
   - Contexts (12+)

---

## Test Categories & Checklist

### 1. Functional Testing

#### 1.1 Authentication Flow

**Test Case: Login Page - Required Fields**
- [ ] Navigate to `/login`
- [ ] Click "Login" without entering credentials
- [ ] Verify validation errors appear
- [ ] Expected: "Username is required" and "Password is required" errors

**Test Case: Login Page - Invalid Credentials**
- [ ] Enter invalid username/password
- [ ] Click "Login"
- [ ] Verify error toast appears
- [ ] Expected: "Invalid credentials" or similar error message

**Test Case: Login Page - Successful Login**
- [ ] Enter valid credentials
- [ ] Click "Login"
- [ ] Verify loading state appears (button disabled, spinner shown)
- [ ] Verify redirect to `/dashboard`
- [ ] Verify token stored in localStorage (check DevTools > Application > Local Storage)
- [ ] Expected: Dashboard loads with user data

**Test Case: Registration Page - Form Validation**
- [ ] Navigate to `/register`
- [ ] Submit empty form
- [ ] Verify all required field errors appear
- [ ] Enter invalid email (e.g., "notanemail")
- [ ] Verify email format error
- [ ] Enter password less than 8 characters
- [ ] Verify password length error
- [ ] Enter mismatched passwords
- [ ] Verify password match error
- [ ] Expected: All validation errors display clearly

**Test Case: Registration Page - Successful Registration**
- [ ] Fill all fields correctly with unique username/email
- [ ] Select proficiency level (B2)
- [ ] Click "Create Account"
- [ ] Verify loading state
- [ ] Verify auto-login occurs
- [ ] Verify redirect to `/dashboard`
- [ ] Expected: User logged in and dashboard displays

**Test Case: Protected Routes**
- [ ] Clear localStorage (Application > Local Storage > Clear All)
- [ ] Try to access `/dashboard`
- [ ] Verify redirect to `/login`
- [ ] Login successfully
- [ ] Verify redirect back to `/dashboard`
- [ ] Expected: Protected routes enforce authentication

**Test Case: Logout**
- [ ] Login successfully
- [ ] Navigate to dashboard
- [ ] Click logout (if available in UI, or manually clear localStorage)
- [ ] Verify redirect to `/login`
- [ ] Try to access `/dashboard` again
- [ ] Verify redirect to `/login` again
- [ ] Expected: Logout clears auth state

**Test Case: Auth Persistence**
- [ ] Login successfully
- [ ] Refresh page (F5)
- [ ] Verify still logged in
- [ ] Close tab and reopen app
- [ ] Verify still logged in
- [ ] Expected: Auth persists across page reloads

#### 1.2 Dashboard Features

**Test Case: Dashboard Data Loading**
- [ ] Login and navigate to `/dashboard`
- [ ] Observe loading state
- [ ] Verify dashboard data fetched from API
- [ ] Check Network tab: GET `/api/v1/integration/dashboard`
- [ ] Verify response status 200
- [ ] Expected: Dashboard loads with complete data

**Test Case: Overall Progress Card**
- [ ] Verify progress score displays (0-100%)
- [ ] Verify visual progress indicator (circle or bar)
- [ ] Verify weekly goals section
- [ ] Verify module statistics (conversations, grammar, vocabulary)
- [ ] Expected: All data displays correctly

**Test Case: Current Streak Card**
- [ ] Verify current streak number displays
- [ ] Verify streak icon/visual indicator
- [ ] Expected: Streak displays correctly

**Test Case: Due Items Card**
- [ ] Verify grammar due items list
- [ ] Verify vocabulary due items list
- [ ] Click on due item (should navigate to practice/review)
- [ ] Verify "View All" buttons work
- [ ] Expected: Due items displayed with correct counts

**Test Case: Quick Actions Card**
- [ ] Verify quick action buttons display
- [ ] Verify priority indicators (high/medium/low)
- [ ] Click each quick action button
- [ ] Verify navigation to correct pages
- [ ] Expected Actions:
  - Review due items → `/review` or specific review page
  - Start daily plan → Learning path page
  - Start conversation → Conversation page
  - Practice grammar → `/grammar`

**Test Case: Recent Activity Timeline**
- [ ] Verify recent activities display (last 5-10)
- [ ] Verify activity types shown (conversation, grammar, vocabulary)
- [ ] Verify timestamps display
- [ ] Expected: Activity timeline populated

**Test Case: Close Achievements**
- [ ] Verify achievement progress bars display
- [ ] Verify achievement names and descriptions
- [ ] Verify progress percentages
- [ ] Expected: Shows 3-5 achievements close to completion

#### 1.3 Grammar Topics Browser

**Test Case: Topics List Loading**
- [ ] Navigate to `/grammar`
- [ ] Verify grammar topics load
- [ ] Check Network tab: GET `/api/grammar/topics`
- [ ] Verify response status 200
- [ ] Expected: Grid/list of 50+ topics displays

**Test Case: Search Functionality**
- [ ] Enter search term in search box (e.g., "Präsens")
- [ ] Verify topics filter in real-time
- [ ] Try English search term (e.g., "Present")
- [ ] Verify topics filter correctly
- [ ] Clear search
- [ ] Verify all topics display again
- [ ] Expected: Search filters topics by name (German/English) or description

**Test Case: Category Filter**
- [ ] Open category filter dropdown
- [ ] Select a category (e.g., "Verbs")
- [ ] Verify only topics in that category display
- [ ] Change to different category
- [ ] Verify filter updates
- [ ] Select "All Categories"
- [ ] Verify all topics display
- [ ] Expected: Category filter works correctly

**Test Case: Difficulty Filter**
- [ ] Open difficulty filter dropdown
- [ ] Select difficulty level (e.g., "B2")
- [ ] Verify only B2 topics display
- [ ] Try different levels (A1, C1, etc.)
- [ ] Verify filter updates
- [ ] Select "All Levels"
- [ ] Verify all topics display
- [ ] Expected: Difficulty filter works correctly

**Test Case: Combined Filters**
- [ ] Apply search term + category + difficulty
- [ ] Verify all filters work together
- [ ] Click "Clear Filters"
- [ ] Verify all filters reset
- [ ] Expected: Multiple filters combine correctly

**Test Case: Topic Card Display**
- [ ] Verify each topic card shows:
  - [ ] Topic name (German)
  - [ ] Topic name (English)
  - [ ] Category
  - [ ] Difficulty level
  - [ ] Progress indicator (if user has practiced)
  - [ ] "Start Practice" button
- [ ] Expected: All topic information displays

**Test Case: Start Practice from Topic**
- [ ] Click "Start Practice" on a topic card
- [ ] Verify navigation to `/grammar/practice`
- [ ] Verify URL includes topic ID parameter
- [ ] Verify practice session starts
- [ ] Expected: Practice session initializes with selected topic

**Test Case: Mixed Practice**
- [ ] Click "Start Mixed Practice" button (if available)
- [ ] Verify navigation to `/grammar/practice`
- [ ] Verify multiple topics included
- [ ] Expected: Mixed practice session starts

#### 1.4 Grammar Practice Session

**Test Case: Session Initialization**
- [ ] Start practice session from topic
- [ ] Verify session initializes
- [ ] Check Network tab: POST `/api/grammar/practice/start`
- [ ] Verify response includes session_id
- [ ] Verify URL includes session parameters
- [ ] Expected: Session starts successfully

**Test Case: Exercise Loading**
- [ ] Verify first exercise loads
- [ ] Check Network tab: GET `/api/grammar/practice/{session_id}/next`
- [ ] Verify exercise type displays correctly
- [ ] Expected: Exercise renders properly

**Test Case: Fill-in-the-Blank Exercise**
- [ ] Verify exercise type is "fill_blank"
- [ ] Verify question text displays with blank (`______`)
- [ ] Verify text input field available
- [ ] Type answer in input field
- [ ] Click Submit (or press Enter)
- [ ] Verify answer submitted
- [ ] Expected: Exercise renders and submits correctly

**Test Case: Multiple Choice Exercise**
- [ ] Verify exercise type is "multiple_choice"
- [ ] Verify question displays
- [ ] Verify 4 answer options with radio buttons
- [ ] Select an option
- [ ] Click Submit (or press Enter)
- [ ] Verify answer submitted
- [ ] Expected: Multiple choice works correctly

**Test Case: Translation Exercise**
- [ ] Verify exercise type is "translation"
- [ ] Verify source text displays (Italian)
- [ ] Verify textarea for German translation
- [ ] Type translation
- [ ] Click Submit (or press Enter)
- [ ] Verify answer submitted
- [ ] Expected: Translation exercise works

**Test Case: Error Correction Exercise**
- [ ] Verify exercise type is "error_correction"
- [ ] Verify incorrect sentence displays
- [ ] Verify textarea for correction
- [ ] Type corrected sentence
- [ ] Click Submit (or press Enter)
- [ ] Verify answer submitted
- [ ] Expected: Error correction works

**Test Case: Sentence Building Exercise**
- [ ] Verify exercise type is "sentence_building"
- [ ] Verify word elements provided
- [ ] Verify text input for built sentence
- [ ] Type constructed sentence
- [ ] Click Submit (or press Enter)
- [ ] Verify answer submitted
- [ ] Expected: Sentence building works

**Test Case: Hint Display**
- [ ] Find exercise with hint available
- [ ] Verify hint displays (or hint button shows)
- [ ] Click hint button (if applicable)
- [ ] Verify hint text displays
- [ ] Expected: Hints accessible when available

**Test Case: Answer Submission**
- [ ] Answer an exercise
- [ ] Click Submit button
- [ ] Verify loading state (button disabled)
- [ ] Check Network tab: POST `/api/grammar/practice/{session_id}/answer`
- [ ] Verify response includes feedback
- [ ] Expected: Answer submits successfully

**Test Case: Feedback Display - Correct Answer**
- [ ] Submit correct answer
- [ ] Verify correct indicator (green checkmark, "Richtig!", etc.)
- [ ] Verify positive feedback in German
- [ ] Verify "Continue" or "Next" button appears
- [ ] Expected: Positive feedback displays

**Test Case: Feedback Display - Incorrect Answer**
- [ ] Submit incorrect answer
- [ ] Verify incorrect indicator (red X, "Falsch", etc.)
- [ ] Verify feedback in German explaining the error
- [ ] Verify specific errors highlighted (if available)
- [ ] Verify suggestions provided (if available)
- [ ] Verify correct answer displayed
- [ ] Verify "Continue" button appears
- [ ] Expected: Detailed negative feedback displays

**Test Case: Session Progress Tracking**
- [ ] Verify progress bar updates (X of Y exercises)
- [ ] Verify correct count updates
- [ ] Verify total attempts updates
- [ ] Verify streak counter updates
- [ ] Verify points earned updates
- [ ] Verify accuracy percentage updates
- [ ] Expected: All progress metrics update in real-time

**Test Case: Streak Counter**
- [ ] Answer 3 exercises correctly in a row
- [ ] Verify streak increases to 3
- [ ] Answer one incorrectly
- [ ] Verify streak resets to 0
- [ ] Expected: Streak tracks consecutive correct answers

**Test Case: Keyboard Shortcuts - Enter to Submit**
- [ ] Type answer in exercise
- [ ] Press Enter key (without clicking Submit)
- [ ] Verify answer submits
- [ ] Expected: Enter key submits answer

**Test Case: Keyboard Shortcuts - Space to Continue**
- [ ] Submit answer and view feedback
- [ ] Press Space key
- [ ] Verify next exercise loads
- [ ] Expected: Space key continues to next exercise

**Test Case: Keyboard Shortcuts - Esc to End**
- [ ] During active session, press Esc key
- [ ] Verify end session confirmation (or immediate end)
- [ ] Expected: Esc key ends session

**Test Case: End Session Button**
- [ ] Click "End Session" button
- [ ] Verify confirmation prompt (if applicable)
- [ ] Confirm end session
- [ ] Check Network tab: POST `/api/grammar/practice/{session_id}/end`
- [ ] Verify navigation to results page or dashboard
- [ ] Expected: Session ends gracefully

**Test Case: Session Completion**
- [ ] Complete all exercises in session
- [ ] Verify automatic session end
- [ ] Verify results summary displays
- [ ] Verify navigation to results page
- [ ] Expected: Session completes successfully

### 2. UI/UX Testing

#### 2.1 Responsive Design

**Test Case: Mobile Layout (375px width)**
- [ ] Resize browser to 375px width (or use DevTools responsive mode)
- [ ] Verify sidebar hidden by default
- [ ] Verify menu button visible in header
- [ ] Click menu button
- [ ] Verify sidebar slides in as overlay
- [ ] Click outside sidebar
- [ ] Verify sidebar closes
- [ ] Verify login form stacks vertically
- [ ] Verify dashboard cards full width (single column)
- [ ] Verify grammar topics cards stack
- [ ] Verify practice exercises readable
- [ ] Verify buttons appropriately sized
- [ ] Expected: Fully functional on mobile

**Test Case: Tablet Layout (768px width)**
- [ ] Resize browser to 768px width
- [ ] Verify sidebar toggles with overlay (or partially visible)
- [ ] Verify dashboard cards in 2 columns (if designed)
- [ ] Verify forms appropriately sized
- [ ] Verify navigation accessible
- [ ] Expected: Good tablet experience

**Test Case: Desktop Layout (1440px width)**
- [ ] Resize browser to 1440px+ width
- [ ] Verify sidebar always visible on left
- [ ] Verify dashboard 2-column grid
- [ ] Verify topic cards in grid (3-4 columns)
- [ ] Verify all features accessible
- [ ] Verify optimal spacing and layout
- [ ] Expected: Optimal desktop experience

#### 2.2 Visual Design

**Test Case: Color Scheme**
- [ ] Verify German flag colors used (gold #FFCC00, red #DD0000, black #000000)
- [ ] Verify consistent primary/secondary colors
- [ ] Verify adequate contrast for text readability
- [ ] Verify color-blind friendly indicators (not relying on color alone)
- [ ] Expected: Consistent, accessible color palette

**Test Case: Typography**
- [ ] Verify font sizes readable (minimum 16px for body text)
- [ ] Verify heading hierarchy clear (h1 > h2 > h3)
- [ ] Verify line spacing comfortable (1.5 minimum)
- [ ] Verify text alignment appropriate
- [ ] Expected: Readable, well-structured typography

**Test Case: Spacing & Layout**
- [ ] Verify consistent padding/margins throughout
- [ ] Verify elements properly aligned
- [ ] Verify balanced white space
- [ ] Verify no overlapping elements
- [ ] Expected: Clean, organized layout

#### 2.3 Interactive Elements

**Test Case: Button States**
- [ ] Hover over buttons
- [ ] Verify hover state visible (color change, shadow, etc.)
- [ ] Click button (active state)
- [ ] Verify active state visible
- [ ] Verify disabled buttons clearly disabled (opacity, cursor, etc.)
- [ ] Verify loading buttons show spinner
- [ ] Expected: All button states clear

**Test Case: Form Input States**
- [ ] Click in text input
- [ ] Verify focus state (border color, outline)
- [ ] Type in input
- [ ] Verify text displays correctly
- [ ] Trigger validation error
- [ ] Verify error state (red border, error message)
- [ ] Fix error
- [ ] Verify valid state (or neutral state)
- [ ] Expected: Clear input states

**Test Case: Toast Notifications**
- [ ] Trigger success action (e.g., login)
- [ ] Verify success toast appears (green, checkmark icon)
- [ ] Wait 5 seconds
- [ ] Verify toast auto-dismisses
- [ ] Trigger error action (e.g., invalid login)
- [ ] Verify error toast appears (red, X icon)
- [ ] Click dismiss button on toast
- [ ] Verify toast dismisses immediately
- [ ] Expected: Toasts work correctly

**Test Case: Animations**
- [ ] Observe page transitions
- [ ] Verify smooth animations (sidebar, modals, toasts)
- [ ] Verify no janky or slow animations
- [ ] Expected: Smooth, professional animations

### 3. Error Handling & Edge Cases

#### 3.1 API Errors

**Test Case: Network Failure**
- [ ] Disconnect from network (or block backend in DevTools)
- [ ] Try to login
- [ ] Verify error message displays
- [ ] Verify user-friendly error (not raw error stack)
- [ ] Expected: Graceful network error handling

**Test Case: 401 Unauthorized**
- [ ] Manually modify token in localStorage to invalid value
- [ ] Refresh page or make API call
- [ ] Verify redirect to `/login`
- [ ] Verify toast notification about session expiry
- [ ] Expected: Auth errors handled correctly

**Test Case: 422 Validation Errors**
- [ ] Submit registration with invalid data
- [ ] Verify field-level error messages display
- [ ] Verify errors associated with correct fields
- [ ] Expected: Validation errors clear and actionable

**Test Case: 500 Server Errors**
- [ ] Trigger server error (may need backend cooperation or mock)
- [ ] Verify user-friendly error message
- [ ] Verify error doesn't crash app
- [ ] Expected: Server errors handled gracefully

#### 3.2 Data Edge Cases

**Test Case: Empty States**
- [ ] Login as new user with no practice history
- [ ] Verify dashboard shows empty states gracefully
- [ ] Verify "No recent activity" or similar message
- [ ] Verify "No due items" message
- [ ] Navigate to grammar topics with filters that yield no results
- [ ] Verify "No topics found" message
- [ ] Expected: Empty states handled well

**Test Case: Large Datasets**
- [ ] Load grammar topics page with 50+ topics
- [ ] Verify performance acceptable
- [ ] Verify no UI breaking
- [ ] Test with exercise containing very long question text
- [ ] Verify text wraps correctly
- [ ] Test with very long feedback text
- [ ] Verify scrollable or properly formatted
- [ ] Expected: Large data handled gracefully

#### 3.3 User Input Edge Cases

**Test Case: Empty Submission**
- [ ] Leave exercise answer blank
- [ ] Click Submit
- [ ] Verify validation prevents submission (or accepts as wrong answer)
- [ ] Expected: Empty submissions handled

**Test Case: Very Long Text**
- [ ] Enter 500+ characters in textarea exercise
- [ ] Verify text displays correctly
- [ ] Submit answer
- [ ] Verify submission works
- [ ] Expected: Long text handled

**Test Case: Special Characters**
- [ ] Enter special characters (ä, ö, ü, ß, é, à, etc.)
- [ ] Verify characters display correctly
- [ ] Submit answer
- [ ] Verify submission works
- [ ] Expected: Unicode and special characters supported

**Test Case: XSS Attempt**
- [ ] Enter `<script>alert('XSS')</script>` in text input
- [ ] Submit
- [ ] Verify script doesn't execute
- [ ] Verify sanitization works
- [ ] Expected: XSS prevented

**Test Case: SQL Injection Attempt**
- [ ] Enter `' OR '1'='1` in username field
- [ ] Submit login
- [ ] Verify doesn't bypass authentication
- [ ] Expected: SQL injection prevented (backend should handle, but verify frontend doesn't expose)

### 4. Performance Testing

#### 4.1 Load Times

**Test Case: Initial Page Load**
- [ ] Clear browser cache
- [ ] Load http://192.168.178.100:5173
- [ ] Measure load time (Network tab)
- [ ] Target: <3 seconds
- [ ] Expected: Fast initial load

**Test Case: Authentication Performance**
- [ ] Login with valid credentials
- [ ] Measure time from submit to dashboard display
- [ ] Target: <2 seconds
- [ ] Expected: Fast authentication

**Test Case: Dashboard Data Fetch**
- [ ] Navigate to dashboard
- [ ] Measure API call time (Network tab)
- [ ] Target: <2 seconds
- [ ] Expected: Fast dashboard load

**Test Case: Grammar Topics Load**
- [ ] Navigate to `/grammar`
- [ ] Measure API call and render time
- [ ] Target: <1 second
- [ ] Expected: Fast topics load

**Test Case: Exercise Load**
- [ ] Start practice session
- [ ] Measure exercise fetch time
- [ ] Target: <1 second per exercise
- [ ] Expected: Fast exercise rendering

#### 4.2 Interactions

**Test Case: Form Submission Feedback**
- [ ] Fill form
- [ ] Click Submit
- [ ] Verify immediate loading indicator
- [ ] Expected: No perceived lag

**Test Case: Navigation Speed**
- [ ] Click sidebar menu items
- [ ] Verify instant route changes
- [ ] Expected: Fast navigation

**Test Case: Filtering/Searching**
- [ ] Type in search box on grammar topics
- [ ] Verify filtering happens quickly
- [ ] Target: <500ms response
- [ ] Expected: Real-time filtering

#### 4.3 Bundle Size

**Test Case: Production Build Size**
- [ ] Run `npm run build` in frontend directory
- [ ] Check output bundle size
- [ ] Target: <500KB (gzipped <150KB)
- [ ] Current: 301KB (gzipped 98KB) ✅
- [ ] Expected: Acceptable bundle size

### 5. Accessibility Testing

#### 5.1 Keyboard Navigation

**Test Case: Tab Order**
- [ ] Press Tab key repeatedly on login page
- [ ] Verify tab order logical (username → password → login button → signup link)
- [ ] Navigate entire app with keyboard only
- [ ] Verify all interactive elements reachable
- [ ] Expected: Logical tab order

**Test Case: Focus Indicators**
- [ ] Tab through interactive elements
- [ ] Verify focus indicator visible on each element
- [ ] Verify focus indicator clear (border, outline, shadow)
- [ ] Expected: Clear focus indicators

**Test Case: Keyboard Shortcuts**
- [ ] Test all documented keyboard shortcuts:
  - [ ] Enter to submit
  - [ ] Esc to close/end
  - [ ] Space to continue
- [ ] Verify shortcuts work consistently
- [ ] Expected: Shortcuts functional

**Test Case: No Keyboard Traps**
- [ ] Navigate entire app with keyboard
- [ ] Verify no elements trap focus (can always Tab out)
- [ ] Verify modals can be closed with Esc
- [ ] Expected: No keyboard traps

#### 5.2 Screen Reader Support

**Test Case: Semantic HTML**
- [ ] Inspect page elements
- [ ] Verify use of semantic HTML (`<nav>`, `<main>`, `<article>`, `<button>`, etc.)
- [ ] Verify proper heading hierarchy (`<h1>`, `<h2>`, `<h3>`)
- [ ] Expected: Semantic HTML used

**Test Case: ARIA Labels**
- [ ] Inspect interactive elements without text (icons, close buttons)
- [ ] Verify `aria-label` or `aria-labelledby` attributes
- [ ] Verify form inputs have associated `<label>` elements
- [ ] Expected: Proper ARIA attributes

**Test Case: Error Messages**
- [ ] Trigger form validation errors
- [ ] Verify error messages programmatically associated with inputs
- [ ] Verify `aria-invalid` or `aria-describedby` used
- [ ] Expected: Errors accessible to screen readers

#### 5.3 Visual Accessibility

**Test Case: Color Contrast**
- [ ] Use browser extension (e.g., WAVE, Axe DevTools)
- [ ] Scan pages for contrast issues
- [ ] Target: WCAG AA compliance (4.5:1 for normal text, 3:1 for large text)
- [ ] Expected: Adequate contrast

**Test Case: Text Resizing**
- [ ] Set browser zoom to 200%
- [ ] Verify all text readable
- [ ] Verify no layout breaking
- [ ] Verify no text overlap
- [ ] Expected: Functional at 200% zoom

**Test Case: Focus Indicators**
- [ ] Verify focus indicators have 3:1 contrast with background
- [ ] Expected: Clear focus indicators

**Test Case: No Color-Only Information**
- [ ] Verify correct/incorrect feedback uses icons + color
- [ ] Verify status indicators don't rely on color alone
- [ ] Expected: Information conveyed beyond color

---

## Bug Reporting Guidelines

### Bug Report Template

Create a file: `/frontend/tests/manual/bugs/BUG-XXX-short-title.md`

```markdown
# BUG-XXX: [Short Descriptive Title]

**Severity:** [Critical | High | Medium | Low]
**Category:** [Authentication | Dashboard | Grammar | UI/UX | Performance | Accessibility]
**Reported:** [Date]
**Reporter:** [Your name]
**Status:** [Open | In Progress | Fixed | Closed | Wont Fix]

## Description
[Brief description of the bug]

## Steps to Reproduce
1. [First step]
2. [Second step]
3. [Third step]
...

## Expected Result
[What should happen]

## Actual Result
[What actually happens]

## Screenshots/Videos
[Attach screenshots or link to videos in /media/ subdirectory]
- Screenshot 1: ![](./media/BUG-XXX-screenshot1.png)
- Video: [Link to screen recording]

## Environment
- **Browser:** [Chrome 120, Firefox 121, etc.]
- **OS:** [Windows 11, macOS Sonoma, Ubuntu 22.04, etc.]
- **Screen Size:** [1920x1080, 375x667 (mobile), etc.]
- **Frontend URL:** http://192.168.178.100:5173
- **Backend URL:** http://192.168.178.100:8000

## Console Errors
```
[Paste any console errors from DevTools]
```

## Network Errors
[If applicable, paste failed network requests from Network tab]
- Request URL:
- Status Code:
- Response:

## Additional Context
[Any other relevant information]

## Related Bugs
[Links to related bug reports, if any]
```

### Severity Classification

**Critical (P0):**
- App crashes or won't load
- Data loss occurs
- Security vulnerabilities (XSS, auth bypass)
- Authentication completely broken
- Core features completely unusable

**High (P1):**
- Major features broken (grammar practice won't start, dashboard won't load)
- Incorrect data displayed
- Poor UX that blocks core workflows
- Significant performance issues
- Accessibility issues preventing usage

**Medium (P2):**
- Minor features broken
- Visual issues (misaligned elements, wrong colors)
- Slow performance (but still usable)
- Non-critical validation errors
- Minor UX improvements needed

**Low (P3):**
- Cosmetic issues
- Typos or text inconsistencies
- Minor UX improvements (nice-to-haves)
- Edge cases with rare occurrence

### Bug Summary Document

Create a file: `/frontend/tests/manual/bug-summary.md`

```markdown
# Bug Summary - Frontend Testing

**Last Updated:** [Date]
**Total Bugs:** XX
**Critical:** X | **High:** X | **Medium:** X | **Low:** X

## Critical Bugs (P0)

### BUG-001: [Title]
- **Status:** Open
- **Category:** Authentication
- **Link:** [./bugs/BUG-001-title.md](./bugs/BUG-001-title.md)

## High Bugs (P1)

### BUG-002: [Title]
- **Status:** Open
- **Category:** Grammar
- **Link:** [./bugs/BUG-002-title.md](./bugs/BUG-002-title.md)

## Medium Bugs (P2)
...

## Low Bugs (P3)
...

## Fixed Bugs
...

## Statistics
- **Open:** XX
- **In Progress:** XX
- **Fixed:** XX
- **Closed:** XX
```

---

## Test Results Documentation

Create a file: `/frontend/tests/manual/test-results.md`

```markdown
# Test Results - Frontend Testing

**Test Date:** [Date]
**Tester:** [Your name]
**Frontend Version:** [Git commit hash or version]
**Backend Version:** [Backend version]

## Test Execution Summary

**Total Test Cases:** XXX
**Passed:** XXX (XX%)
**Failed:** XX (XX%)
**Blocked:** XX (XX%)
**Not Tested:** XX (XX%)

## Results by Category

### 1. Functional Testing
- **Authentication:** X/X passed (XX%)
- **Dashboard:** X/X passed (XX%)
- **Grammar Topics:** X/X passed (XX%)
- **Practice Session:** X/X passed (XX%)

### 2. UI/UX Testing
- **Responsive Design:** X/X passed (XX%)
- **Visual Design:** X/X passed (XX%)
- **Interactive Elements:** X/X passed (XX%)

### 3. Error Handling
- **API Errors:** X/X passed (XX%)
- **Data Edge Cases:** X/X passed (XX%)
- **Input Edge Cases:** X/X passed (XX%)

### 4. Performance Testing
- **Load Times:** X/X passed (XX%)
- **Interactions:** X/X passed (XX%)
- **Bundle Size:** PASS ✅

### 5. Accessibility Testing
- **Keyboard Navigation:** X/X passed (XX%)
- **Screen Reader:** X/X passed (XX%)
- **Visual Accessibility:** X/X passed (XX%)

## Detailed Results

### Authentication

#### Test Case: Login Page - Required Fields
- **Status:** ✅ PASS | ❌ FAIL | ⏸️ BLOCKED | ⏭️ NOT TESTED
- **Notes:** [Any relevant notes]
- **Bug:** [Link to bug report if failed]

[Continue for all test cases...]

## Browser Compatibility

| Test Category | Chrome | Firefox | Safari | Edge |
|--------------|--------|---------|--------|------|
| Authentication | ✅ | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ❌ | ✅ | ✅ |
| Grammar | ✅ | ✅ | ⏭️ | ✅ |
...

## Device Testing

| Test Category | Desktop | Tablet | Mobile |
|--------------|---------|--------|--------|
| Authentication | ✅ | ✅ | ✅ |
| Dashboard | ✅ | ✅ | ❌ |
...

## Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Initial Load | <3s | 2.1s | ✅ |
| Login | <2s | 1.5s | ✅ |
| Dashboard | <2s | 1.8s | ✅ |
| Topics Load | <1s | 0.7s | ✅ |
| Exercise Load | <1s | 0.9s | ✅ |
| Bundle Size | <500KB | 301KB | ✅ |

## Coverage Report

**Implemented Features Tested:** XX/XX (XX%)
**Not Implemented Features:** XX (not tested)

## Recommendations

1. [High priority fix recommendation]
2. [Medium priority improvement]
3. [Low priority enhancement]

## Next Steps

- [ ] Retest failed test cases after fixes
- [ ] Complete blocked test cases
- [ ] Test on additional browsers/devices
- [ ] Automated E2E test suite creation
```

---

## Automated Testing Setup

### Install Playwright (Recommended)

```bash
cd /opt/myGermanAITeacher/frontend
npm install --save-dev @playwright/test
npx playwright install
```

### Sample E2E Test Script

Create file: `/frontend/tests/e2e/auth.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('should login successfully with valid credentials', async ({ page }) => {
    await page.goto('http://192.168.178.100:5173/login');

    await page.fill('input[name="username"]', 'test_engineer');
    await page.fill('input[name="password"]', 'TestPass123!');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL(/dashboard/);
    await expect(page.locator('h1')).toContainText('Dashboard');
  });

  test('should show error for invalid credentials', async ({ page }) => {
    await page.goto('http://192.168.178.100:5173/login');

    await page.fill('input[name="username"]', 'invalid_user');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('.toast-error')).toBeVisible();
  });

  test('should redirect to login when accessing protected route', async ({ page }) => {
    await page.goto('http://192.168.178.100:5173/dashboard');

    await expect(page).toHaveURL(/login/);
  });
});
```

### Run Playwright Tests

```bash
# Run all tests
npx playwright test

# Run specific test file
npx playwright test tests/e2e/auth.spec.ts

# Run with UI mode (interactive)
npx playwright test --ui

# Generate report
npx playwright show-report
```

---

## Daily Testing Workflow

### Morning Routine
1. Pull latest frontend code
   ```bash
   cd /opt/myGermanAITeacher
   git pull origin master
   cd frontend
   npm install  # if dependencies changed
   ```

2. Review what features were implemented/changed
   - Check git commits
   - Review PR descriptions
   - Update test cases if needed

3. Start testing environment
   - Verify backend running: `curl http://192.168.178.100:8000/api/health`
   - Start frontend: `npm run dev -- --host` (if not already running)

### Testing Session
1. Execute relevant test cases for new/changed features
2. Document results immediately
3. Create bug reports for failures
4. Take screenshots/videos of bugs
5. Update bug summary

### End of Day
1. Update test results document
2. Communicate findings to developers
3. Plan next day's testing focus
4. Backup test data/results

---

## Communication with Developers

### Bug Report Notification
When you find a critical or high-severity bug:
1. Create detailed bug report (as documented above)
2. Update bug summary
3. Notify developers with:
   - Bug ID and title
   - Severity
   - Link to bug report
   - Brief description

### Testing Status Updates
Provide regular updates:
- Daily: Quick status (X tests passed, Y bugs found)
- Weekly: Detailed test results summary
- Ad-hoc: Critical bugs immediately

### Feedback on Fixes
When developers fix bugs:
1. Retest the specific bug
2. Test related functionality (regression)
3. Update bug status (fixed/reopened)
4. Verify fix doesn't introduce new bugs

---

## Success Criteria

Your testing is successful when:

- ✅ All implemented features tested comprehensively
- ✅ 100+ test cases executed
- ✅ All bugs documented with clear reproduction steps
- ✅ Bug reports include screenshots/videos
- ✅ Test results documented and up-to-date
- ✅ Automated E2E test suite created (optional but recommended)
- ✅ Cross-browser testing completed
- ✅ Responsive design validated
- ✅ Accessibility compliance verified
- ✅ Performance metrics collected

---

## Tools & Resources

### Browser Tools
- **Chrome DevTools** (F12) - Console, Network, Elements, Application
- **Firefox Developer Tools** (F12)
- **Responsive Design Mode** - Ctrl+Shift+M (Chrome/Firefox)

### Browser Extensions
- **WAVE** - Accessibility evaluation
- **Axe DevTools** - Accessibility testing
- **Lighthouse** - Performance, accessibility, SEO audit
- **React DevTools** - React component inspection

### Testing Tools
- **Playwright** - E2E testing (recommended)
- **Cypress** - Alternative E2E testing
- **Postman** - API testing
- **Loom** - Screen recording for bug reports

### Documentation Tools
- **Markdown editors** - VS Code, Obsidian, Typora
- **Screenshot tools** - Greenshot, Flameshot, Snipping Tool
- **Video recording** - OBS Studio, Loom, ShareX

---

## FAQs

**Q: What if I find a bug in the backend?**
A: Document it in your bug report and note that it's a backend issue. Provide API request/response details. The developer will triage and fix appropriately.

**Q: Should I test features that aren't fully implemented?**
A: No. Focus only on the implemented features listed in this document. If you're unsure, check with the developer.

**Q: Can I suggest UX improvements?**
A: Yes! Document them as Low severity bugs or create a separate suggestions document. But don't implement them yourself.

**Q: How do I handle intermittent bugs?**
A: Document them with "Intermittent" in the title. Note the frequency (e.g., "happens 3 out of 10 times"). Provide as much detail as possible to help reproduce.

**Q: What if the backend is down?**
A: Notify the developer. You can still test frontend components in isolation, but full integration testing requires the backend.

**Q: Should I test on all browsers every time?**
A: For comprehensive testing, yes. But prioritize Chrome/Firefox for daily testing. Do full browser compatibility testing before releases.

---

**Good luck with your testing! Remember: Your goal is to find bugs so developers can fix them and deliver a high-quality product. Be thorough, be detailed, and don't hesitate to report even minor issues.**
