# Phase 5: Conversation Practice - Comprehensive Test Plan

**Date:** 2026-01-20
**Module:** Conversation Practice
**Status:** Ready for Testing
**Test Environment:** http://192.168.178.100:5173
**Backend API:** http://192.168.178.100:8000

---

## 📋 Test Overview

### Scope
Phase 5 implements the Conversation Practice module with:
- **4 Pages:** ContextsPage, PracticePage, HistoryPage, SessionDetailPage
- **9 Components:** ChatInterface, MessageBubble, GrammarFeedbackPanel, etc.
- **10 API Endpoints:** 5 conversation + 5 context endpoints
- **420 lines** of state management (conversationStore)

### Test Categories
1. **Context Selection & Management** (15 tests)
2. **Conversation Practice - Main Flow** (20 tests)
3. **Grammar Feedback Panel** (10 tests)
4. **Vocabulary Highlighting** (8 tests)
5. **German Character Input** (6 tests)
6. **Session Persistence & Restore** (8 tests)
7. **Session History & Analysis** (10 tests)
8. **Keyboard Shortcuts** (6 tests)
9. **Mobile Responsiveness** (8 tests)
10. **Error Handling** (10 tests)

**Total Tests:** 101 test cases

---

## 🎯 Test Categories

### 1. Context Selection & Management (ContextsPage)

#### T5-C-001: Load Contexts Page
**Priority:** HIGH
**Steps:**
1. Login to application
2. Navigate to Conversation → Start Conversation
3. Observe contexts loading

**Expected:**
- ✅ Page loads without errors
- ✅ Grid of context cards displayed
- ✅ 12+ pre-configured contexts visible
- ✅ Category icons displayed (Briefcase/Coffee/Star)
- ✅ Difficulty badges shown (A1-C2)
- ✅ "Times used" count visible

---

#### T5-C-002: Filter by Category (Business)
**Priority:** HIGH
**Steps:**
1. On ContextsPage
2. Click "Business" category filter
3. Observe filtered results

**Expected:**
- ✅ Only business contexts displayed
- ✅ Daily contexts hidden
- ✅ Correct count shown in filter badge
- ✅ Smooth transition animation

---

#### T5-C-003: Filter by Category (Daily)
**Priority:** HIGH
**Steps:**
1. On ContextsPage
2. Click "Daily" category filter
3. Observe filtered results

**Expected:**
- ✅ Only daily contexts displayed
- ✅ Business contexts hidden
- ✅ Correct count shown in filter badge

---

#### T5-C-004: Filter by Difficulty (A1-A2)
**Priority:** MEDIUM
**Steps:**
1. On ContextsPage
2. Select "A1-A2" from difficulty dropdown
3. Observe filtered results

**Expected:**
- ✅ Only A1-A2 contexts displayed
- ✅ Higher difficulty contexts hidden
- ✅ Filter applied correctly

---

#### T5-C-005: Filter by Difficulty (B1-B2)
**Priority:** MEDIUM
**Steps:**
1. On ContextsPage
2. Select "B1-B2" from difficulty dropdown

**Expected:**
- ✅ Only B1-B2 contexts displayed
- ✅ User's level should be B2 (matches profile)

---

#### T5-C-006: Search Contexts by Name
**Priority:** HIGH
**Steps:**
1. On ContextsPage
2. Type "Meeting" in search box
3. Observe filtered results

**Expected:**
- ✅ Contexts with "Meeting" in name/description shown
- ✅ Real-time filtering as you type
- ✅ Other contexts hidden

---

#### T5-C-007: Clear All Filters
**Priority:** MEDIUM
**Steps:**
1. Apply category and difficulty filters
2. Click "Clear Filters" button
3. Observe reset

**Expected:**
- ✅ All filters cleared
- ✅ All contexts displayed again
- ✅ Dropdown and category buttons reset

---

#### T5-C-008: Start Conversation from Context Card
**Priority:** HIGH
**Steps:**
1. On ContextsPage
2. Click "Start Conversation" on any context card
3. Observe navigation

**Expected:**
- ✅ Navigate to /conversation/practice
- ✅ Session initialized with selected context
- ✅ Context info displayed in session header
- ✅ Chat interface ready

---

#### T5-C-009: Context Card Hover Effect
**Priority:** LOW
**Steps:**
1. On ContextsPage
2. Hover mouse over context card
3. Observe visual feedback

**Expected:**
- ✅ Card scales up slightly
- ✅ Shadow increases
- ✅ Smooth transition animation
- ✅ Button becomes more prominent

---

#### T5-C-010: Empty State (No Contexts)
**Priority:** LOW
**Steps:**
1. Apply filters that match no contexts
2. Observe empty state

**Expected:**
- ✅ Empty state message displayed
- ✅ Helpful message suggesting to clear filters
- ✅ No error console messages

---

#### T5-C-011: Loading State
**Priority:** MEDIUM
**Steps:**
1. Navigate to ContextsPage
2. Observe loading state before contexts load

**Expected:**
- ✅ Loading spinner or skeleton displayed
- ✅ No "no contexts" flash before data loads
- ✅ Smooth transition to loaded state

---

#### T5-C-012: Context Card Data Accuracy
**Priority:** HIGH
**Steps:**
1. Select a specific context (e.g., "Business Meeting")
2. Verify all displayed data

**Expected:**
- ✅ Context name correct
- ✅ Description accurate
- ✅ Category matches backend
- ✅ Difficulty level correct
- ✅ Times used count accurate

---

#### T5-C-013: Multiple Category Filters (Edge Case)
**Priority:** LOW
**Steps:**
1. Click "Business" filter
2. Then click "Daily" filter
3. Observe behavior

**Expected:**
- ✅ Only one category active at a time (toggle behavior)
- ✅ OR: Show contexts from both categories (if multi-select)
- ✅ Clear expected behavior

---

#### T5-C-014: Difficulty Dropdown Behavior
**Priority:** MEDIUM
**Steps:**
1. Click difficulty dropdown
2. Select an option
3. Open dropdown again

**Expected:**
- ✅ Dropdown shows current selection
- ✅ Can change selection
- ✅ "All Levels" option available

---

#### T5-C-015: Grid Layout Responsiveness
**Priority:** MEDIUM
**Steps:**
1. Resize browser window to various widths
2. Observe grid adaptation

**Expected:**
- ✅ Desktop: 3 columns
- ✅ Tablet: 2 columns
- ✅ Mobile: 1 column
- ✅ No horizontal scroll

---

### 2. Conversation Practice - Main Flow (PracticePage)

#### T5-P-001: Start New Conversation
**Priority:** HIGH ⭐
**Steps:**
1. Select context "Business Meeting"
2. Click "Start Conversation"
3. Observe conversation initialization

**Expected:**
- ✅ Navigate to /conversation/practice
- ✅ Session header shows context name
- ✅ Timer starts (00:00)
- ✅ Message count shows 0
- ✅ Chat input enabled
- ✅ AI sends initial greeting message
- ✅ Grammar feedback panel visible (desktop)

---

#### T5-P-002: Send First Message
**Priority:** HIGH ⭐
**Steps:**
1. In active conversation
2. Type: "Guten Morgen! Ich möchte über das Projekt sprechen."
3. Press Enter or click Send

**Expected:**
- ✅ Message appears in chat as user bubble
- ✅ Typing indicator appears (AI thinking)
- ✅ AI responds within 5-10 seconds
- ✅ AI response appears as AI bubble
- ✅ Message count increments
- ✅ Chat auto-scrolls to bottom

---

#### T5-P-003: Send Message with Grammar Error
**Priority:** HIGH ⭐
**Steps:**
1. Type message with intentional error: "Ich gehen zum Büro."
2. Check "Request Feedback" checkbox
3. Send message

**Expected:**
- ✅ Message sent
- ✅ AI responds
- ✅ Grammar feedback appears in panel
- ✅ Error highlighted with severity (high/medium/low)
- ✅ Correction shown: "Ich gehe zum Büro"
- ✅ Explanation provided

---

#### T5-P-004: Send Multiple Messages (Conversation Flow)
**Priority:** HIGH
**Steps:**
1. Send 5-10 messages back and forth
2. Observe conversation flow

**Expected:**
- ✅ All messages displayed correctly
- ✅ User messages right-aligned (blue)
- ✅ AI messages left-aligned (white/gray)
- ✅ Timestamps shown
- ✅ Auto-scroll works
- ✅ No lag or stuttering

---

#### T5-P-005: Character Limit (5000 chars)
**Priority:** MEDIUM
**Steps:**
1. Type very long message (>5000 characters)
2. Observe character counter

**Expected:**
- ✅ Character counter shows "5000/5000"
- ✅ Send button disabled when over limit
- ✅ Visual warning (red counter)
- ✅ Cannot type beyond limit

---

#### T5-P-006: Empty Message Prevention
**Priority:** MEDIUM
**Steps:**
1. Try to send empty message
2. Try to send only spaces
3. Observe validation

**Expected:**
- ✅ Send button disabled for empty input
- ✅ Send button disabled for whitespace-only
- ✅ No empty messages sent

---

#### T5-P-007: Shift+Enter for Newline
**Priority:** MEDIUM
**Steps:**
1. Type message
2. Press Shift+Enter
3. Type more text
4. Observe behavior

**Expected:**
- ✅ Newline inserted (not sent)
- ✅ Can type multi-line message
- ✅ Press Enter alone sends message

---

#### T5-P-008: Textarea Auto-Resize
**Priority:** LOW
**Steps:**
1. Type long message with multiple lines
2. Observe textarea height

**Expected:**
- ✅ Textarea grows as you type
- ✅ Maximum 5 lines visible
- ✅ Scroll appears after 5 lines
- ✅ Shrinks when text deleted

---

#### T5-P-009: Copy Message Text
**Priority:** MEDIUM
**Steps:**
1. Send a message
2. Click copy button on message bubble
3. Paste into text editor

**Expected:**
- ✅ Copy button visible on hover
- ✅ Click copies text to clipboard
- ✅ Toast: "Copied to clipboard"
- ✅ Text pasted correctly

---

#### T5-P-010: Session Timer Accuracy
**Priority:** MEDIUM
**Steps:**
1. Start conversation
2. Wait 1 minute
3. Check timer display

**Expected:**
- ✅ Timer shows 01:00 (or close)
- ✅ Timer updates every second
- ✅ Format: MM:SS

---

#### T5-P-011: Message Count Accuracy
**Priority:** MEDIUM
**Steps:**
1. Start conversation
2. Send 5 messages
3. Check message count

**Expected:**
- ✅ Count shows "10" (5 user + 5 AI, including initial greeting)
- ✅ Updates after each message

---

#### T5-P-012: Typing Indicator Display
**Priority:** MEDIUM
**Steps:**
1. Send message
2. Observe AI response

**Expected:**
- ✅ Typing indicator appears (three dots)
- ✅ Bouncing animation
- ✅ Disappears when AI responds
- ✅ Message replaces indicator

---

#### T5-P-013: Auto-Scroll Behavior
**Priority:** HIGH
**Steps:**
1. Send 10+ messages to fill chat
2. Scroll up to read old messages
3. Send new message

**Expected:**
- ✅ Does NOT auto-scroll if user scrolled up
- ✅ Shows "scroll to bottom" indicator
- ✅ Click indicator scrolls to bottom
- ✅ Auto-resumes when near bottom

---

#### T5-P-014: Request Feedback Checkbox
**Priority:** HIGH
**Steps:**
1. Toggle "Request Feedback" checkbox
2. Send message with checkbox ON
3. Send message with checkbox OFF

**Expected:**
- ✅ Checkbox toggles correctly
- ✅ WITH feedback: Grammar errors highlighted
- ✅ WITHOUT feedback: No grammar feedback panel updates
- ✅ State persists between messages

---

#### T5-P-015: End Session Button Click
**Priority:** HIGH
**Steps:**
1. Start conversation
2. Send 3-5 messages
3. Click "End Session" button in header
4. Observe confirmation modal

**Expected:**
- ✅ Confirmation modal appears
- ✅ Modal asks: "Are you sure you want to end?"
- ✅ Two buttons: "Cancel" and "End Session"
- ✅ Cancel closes modal, session continues
- ✅ End Session terminates conversation

---

#### T5-P-016: End Session via Escape Key
**Priority:** MEDIUM
**Steps:**
1. In active conversation
2. Press Escape key
3. Observe behavior

**Expected:**
- ✅ Confirmation modal appears (same as button)
- ✅ Session can be ended via keyboard

---

#### T5-P-017: Session Summary After End
**Priority:** HIGH
**Steps:**
1. End session (via button or Escape)
2. Confirm end in modal
3. Observe session summary

**Expected:**
- ✅ SessionSummary modal appears
- ✅ Overall score displayed (0-100)
- ✅ Stats: Turns, Duration, Accuracy, Vocabulary
- ✅ "Areas for Improvement" listed (top 3)
- ✅ Grammar topics to practice with counts
- ✅ "View Full Analysis" button
- ✅ "Start New Conversation" button

---

#### T5-P-018: Timestamp Display
**Priority:** LOW
**Steps:**
1. Send messages
2. Check timestamps on message bubbles

**Expected:**
- ✅ Timestamps shown (e.g., "10:30 AM")
- ✅ Accurate to minute
- ✅ Format consistent

---

#### T5-P-019: Message Bubble Styling
**Priority:** LOW
**Steps:**
1. Observe user and AI message bubbles
2. Compare styling

**Expected:**
- ✅ User messages: Blue background, right-aligned
- ✅ AI messages: White/gray background, left-aligned
- ✅ Avatar/icon displayed
- ✅ Readable contrast
- ✅ Proper spacing

---

#### T5-P-020: Empty Chat State
**Priority:** LOW
**Steps:**
1. Start new conversation
2. Before AI sends initial greeting, observe chat

**Expected:**
- ✅ Empty state message: "Start typing to begin..."
- ✅ Helpful tips displayed
- ✅ No errors

---

### 3. Grammar Feedback Panel

#### T5-G-001: Grammar Panel Visibility (Desktop)
**Priority:** HIGH
**Steps:**
1. Start conversation on desktop (>1024px width)
2. Send message with grammar error
3. Observe panel

**Expected:**
- ✅ Panel visible on right side (30% width)
- ✅ Chat interface 70% width
- ✅ Panel shows feedback sections

---

#### T5-G-002: Toggle Grammar Panel (Ctrl+/)
**Priority:** MEDIUM
**Steps:**
1. In conversation
2. Press Ctrl+/
3. Observe panel toggle

**Expected:**
- ✅ Panel collapses (hidden)
- ✅ Chat expands to full width
- ✅ Press again to show panel
- ✅ State toggles correctly

---

#### T5-G-003: Feedback Severity Grouping
**Priority:** HIGH
**Steps:**
1. Send message with multiple errors (high, medium, low)
2. Check grammar panel

**Expected:**
- ✅ Errors grouped by severity: High, Medium, Low
- ✅ Count badges showing error counts per severity
- ✅ High severity errors shown first
- ✅ Expandable sections

---

#### T5-G-004: Expand/Collapse Severity Sections
**Priority:** MEDIUM
**Steps:**
1. Click on "High Severity" section header
2. Observe expansion

**Expected:**
- ✅ Section expands showing error details
- ✅ Click again to collapse
- ✅ Multiple sections can be open simultaneously
- ✅ Smooth accordion animation

---

#### T5-G-005: Grammar Error Details
**Priority:** HIGH
**Steps:**
1. Expand a feedback section
2. Read error details

**Expected:**
- ✅ Error type displayed (e.g., "Verb Conjugation")
- ✅ Incorrect text shown
- ✅ Corrected text shown
- ✅ Explanation provided
- ✅ Link to practice grammar topic

---

#### T5-G-006: Click to Practice Grammar Topic
**Priority:** MEDIUM
**Steps:**
1. In grammar panel, find error with topic link
2. Click "Practice This Topic" link
3. Observe navigation

**Expected:**
- ✅ Navigate to /grammar/practice?topics={id}
- ✅ Leaves conversation (with confirmation?)
- ✅ Grammar practice starts with that topic

---

#### T5-G-007: Empty Feedback State
**Priority:** LOW
**Steps:**
1. Send grammatically perfect message
2. Check grammar panel

**Expected:**
- ✅ Empty state message: "No grammar errors detected!"
- ✅ Positive feedback icon
- ✅ No error sections

---

#### T5-G-008: Feedback Accumulation
**Priority:** MEDIUM
**Steps:**
1. Send message with error
2. Send another message with different error
3. Check panel

**Expected:**
- ✅ Both errors visible in panel
- ✅ Errors from all messages accumulated
- ✅ OR: Only showing errors from current message (check design)

---

#### T5-G-009: Color Coding by Severity
**Priority:** LOW
**Steps:**
1. Send message with errors of all severities
2. Check color coding

**Expected:**
- ✅ High severity: Red color
- ✅ Medium severity: Yellow/orange color
- ✅ Low severity: Blue/gray color
- ✅ Consistent with MessageBubble inline feedback

---

#### T5-G-010: Panel Scroll Behavior
**Priority:** LOW
**Steps:**
1. Accumulate many grammar errors (10+)
2. Observe panel scrolling

**Expected:**
- ✅ Panel scrollable independently
- ✅ Chat scrolls separately
- ✅ No layout breaking

---

### 4. Vocabulary Highlighting

#### T5-V-001: Vocabulary Highlighting Display
**Priority:** HIGH
**Steps:**
1. Send message with vocabulary words
2. Observe highlighting

**Expected:**
- ✅ Vocabulary words underlined
- ✅ Dotted underline style
- ✅ Color-coded (maybe by difficulty)
- ✅ Not intrusive

---

#### T5-V-002: Hover for Vocabulary Tooltip
**Priority:** HIGH
**Steps:**
1. Hover mouse over highlighted vocabulary word
2. Observe tooltip

**Expected:**
- ✅ Tooltip appears
- ✅ Shows German word
- ✅ Shows Italian translation
- ✅ Shows difficulty level (A1-C2)
- ✅ Tooltip disappears on mouse leave

---

#### T5-V-003: New Vocabulary Badge
**Priority:** MEDIUM
**Steps:**
1. Find a vocabulary word marked as "new"
2. Observe badge

**Expected:**
- ✅ "New" badge displayed
- ✅ Distinctive color (e.g., green)
- ✅ Positioned near word

---

#### T5-V-004: Toggle Vocabulary Highlighting
**Priority:** MEDIUM
**Steps:**
1. In conversation, find vocabulary toggle button
2. Click to disable highlighting
3. Click again to enable

**Expected:**
- ✅ Highlighting can be toggled on/off
- ✅ Tooltip button in header or panel
- ✅ State persists during session

---

#### T5-V-005: Multiple Vocabulary Words in One Message
**Priority:** MEDIUM
**Steps:**
1. Send message with multiple vocabulary words
2. Observe all highlights

**Expected:**
- ✅ All vocabulary words highlighted
- ✅ Each word independently hoverable
- ✅ Tooltips work for all words

---

#### T5-V-006: Vocabulary in AI Responses
**Priority:** MEDIUM
**Steps:**
1. AI responds with vocabulary words
2. Check if highlighted

**Expected:**
- ✅ AI message vocabulary also highlighted
- ✅ OR: Only user message vocabulary highlighted (check design)
- ✅ Consistent behavior

---

#### T5-V-007: Click to Add to List (Future Feature)
**Priority:** LOW
**Steps:**
1. Click on highlighted vocabulary word
2. Observe behavior

**Expected:**
- ✅ (If implemented) Modal to add to list
- ✅ (If not implemented) No action or tooltip only

---

#### T5-V-008: Vocabulary Tooltip Positioning
**Priority:** LOW
**Steps:**
1. Hover on vocabulary word near top of screen
2. Hover on word near bottom
3. Check tooltip positioning

**Expected:**
- ✅ Tooltip doesn't overflow screen
- ✅ Positioned above or below based on space
- ✅ Always readable

---

### 5. German Character Input

#### T5-I-001: German Character Buttons Display
**Priority:** HIGH
**Steps:**
1. In chat input, observe German character buttons
2. Check visibility

**Expected:**
- ✅ 4 buttons visible: ä, ö, ü, ß
- ✅ Positioned inline near textarea
- ✅ Compact design
- ✅ Clear labels

---

#### T5-I-002: Click ä Button
**Priority:** HIGH
**Steps:**
1. Focus on chat input
2. Click "ä" button
3. Observe insertion

**Expected:**
- ✅ "ä" character inserted at cursor position
- ✅ Cursor moves after inserted character
- ✅ Can continue typing normally

---

#### T5-I-003: Click ö, ü, ß Buttons
**Priority:** HIGH
**Steps:**
1. Test clicking each button individually
2. Type message: "Übung für Größe"

**Expected:**
- ✅ All characters insert correctly
- ✅ Can be used in middle of words
- ✅ Can be used at start/end of words

---

#### T5-I-004: Keyboard Shortcut Alt+A for ä
**Priority:** MEDIUM
**Steps:**
1. Focus on chat input
2. Press Alt+A
3. Observe insertion

**Expected:**
- ✅ "ä" inserted
- ✅ Same behavior as clicking button

---

#### T5-I-005: Keyboard Shortcuts Alt+O, Alt+U, Alt+S
**Priority:** MEDIUM
**Steps:**
1. Test Alt+O → ö
2. Test Alt+U → ü
3. Test Alt+S → ß

**Expected:**
- ✅ All shortcuts work
- ✅ Characters inserted correctly
- ✅ Shortcuts shown in tooltips

---

#### T5-I-006: German Characters in Sent Messages
**Priority:** HIGH
**Steps:**
1. Type message with German characters: "Schöne Grüße!"
2. Send message
3. Check display

**Expected:**
- ✅ Characters display correctly in message bubble
- ✅ No encoding issues
- ✅ Backend receives and processes correctly

---

### 6. Session Persistence & Restore

#### T5-S-001: Session Persistence to localStorage
**Priority:** HIGH
**Steps:**
1. Start conversation
2. Send 3-5 messages
3. Open DevTools → Application → Local Storage
4. Check for conversation session data

**Expected:**
- ✅ Session data stored in localStorage
- ✅ Key: conversation-related (e.g., 'conversation-session')
- ✅ Contains sessionId, context, messages

---

#### T5-S-002: Session Restore Prompt on Page Load
**Priority:** HIGH ⭐
**Steps:**
1. Start conversation
2. Send 2-3 messages (don't end session)
3. Navigate away (to /dashboard)
4. Return to /conversation/practice
5. Observe restore prompt

**Expected:**
- ✅ Modal appears: "Resume Previous Session?"
- ✅ Shows session details (context, time ago)
- ✅ Two buttons: "Resume" and "Start New"
- ✅ Modal blocks interaction until choice made

---

#### T5-S-003: Resume Previous Session
**Priority:** HIGH
**Steps:**
1. On restore prompt modal
2. Click "Resume Session"
3. Observe restoration

**Expected:**
- ✅ Conversation restored
- ✅ All previous messages visible
- ✅ Context matches original
- ✅ Can continue conversation
- ✅ Timer continues from where it left off

---

#### T5-S-004: Start New Session (Discard Previous)
**Priority:** HIGH
**Steps:**
1. On restore prompt modal
2. Click "Start New"
3. Observe behavior

**Expected:**
- ✅ Previous session cleared
- ✅ Navigate to context selection
- ✅ OR: Start new session with same context
- ✅ Old session data removed from localStorage

---

#### T5-S-005: Session Expiry (24 Hours)
**Priority:** MEDIUM
**Steps:**
1. Manually modify localStorage session timestamp to >24 hours ago
2. Reload page
3. Navigate to /conversation/practice

**Expected:**
- ✅ No restore prompt (session expired)
- ✅ Old session data cleared
- ✅ Starts fresh

---

#### T5-S-006: Multiple Browser Tabs (localStorage Sync)
**Priority:** LOW
**Steps:**
1. Open conversation in Tab A
2. Open same page in Tab B
3. Send message in Tab A
4. Refresh Tab B

**Expected:**
- ✅ Session data shared via localStorage
- ✅ Tab B can resume same session
- ✅ OR: One tab locks session (prevents conflicts)

---

#### T5-S-007: Session Persistence After Browser Close
**Priority:** HIGH
**Steps:**
1. Start conversation
2. Send messages
3. Close browser entirely
4. Reopen browser and navigate to app
5. Go to /conversation/practice

**Expected:**
- ✅ Restore prompt appears
- ✅ Session data persisted across browser restart
- ✅ Can resume successfully

---

#### T5-S-008: Clear Session After End
**Priority:** MEDIUM
**Steps:**
1. End session normally
2. Check localStorage

**Expected:**
- ✅ Session data cleared from localStorage
- ✅ Next visit starts fresh (no restore prompt)

---

### 7. Session History & Analysis

#### T5-H-001: Navigate to History Page
**Priority:** MEDIUM
**Steps:**
1. Navigate to Conversation → History
2. Observe page load

**Expected:**
- ✅ Page loads without errors
- ✅ List of past sessions displayed
- ✅ Sessions sorted by date (newest first)

---

#### T5-H-002: Session Card Information
**Priority:** MEDIUM
**Steps:**
1. On HistoryPage
2. Examine a session card

**Expected:**
- ✅ Context name displayed
- ✅ Date and time of session
- ✅ Duration (e.g., "15 min")
- ✅ Overall score (0-100)
- ✅ Grammar accuracy (%)
- ✅ "View Details" button

---

#### T5-H-003: Filter by Context
**Priority:** LOW
**Steps:**
1. On HistoryPage
2. Select context from filter dropdown
3. Observe filtered results

**Expected:**
- ✅ Only sessions with selected context shown
- ✅ Other sessions hidden
- ✅ Filter applied correctly

---

#### T5-H-004: Sort by Date
**Priority:** LOW
**Steps:**
1. On HistoryPage
2. Select "Sort by: Date" (if not default)
3. Observe sorting

**Expected:**
- ✅ Sessions sorted newest to oldest
- ✅ OR: Toggle ascending/descending
- ✅ Correct chronological order

---

#### T5-H-005: Sort by Score
**Priority:** LOW
**Steps:**
1. On HistoryPage
2. Select "Sort by: Score"
3. Observe sorting

**Expected:**
- ✅ Sessions sorted by overall score
- ✅ Highest score first (or lowest, check design)
- ✅ Correct score ordering

---

#### T5-H-006: View Session Detail
**Priority:** HIGH
**Steps:**
1. On HistoryPage
2. Click "View Details" on a session card
3. Observe navigation

**Expected:**
- ✅ Navigate to /conversation/session/{id}
- ✅ SessionDetailPage loads

---

#### T5-H-007: SessionDetailPage - Conversation Replay
**Priority:** HIGH
**Steps:**
1. On SessionDetailPage
2. Observe conversation display

**Expected:**
- ✅ All messages from session shown
- ✅ User and AI messages displayed
- ✅ Timestamps visible
- ✅ Matches original conversation

---

#### T5-H-008: SessionDetailPage - Session Stats
**Priority:** MEDIUM
**Steps:**
1. On SessionDetailPage
2. Check stats section

**Expected:**
- ✅ Overall score displayed
- ✅ Duration shown
- ✅ Turn count (number of messages)
- ✅ Grammar accuracy (%)
- ✅ Vocabulary used count

---

#### T5-H-009: SessionDetailPage - Areas for Improvement
**Priority:** MEDIUM
**Steps:**
1. On SessionDetailPage
2. Check "Areas for Improvement" section

**Expected:**
- ✅ Top 3 improvement areas listed
- ✅ Specific feedback provided
- ✅ Actionable suggestions

---

#### T5-H-010: SessionDetailPage - Practice Grammar Topics Link
**Priority:** HIGH
**Steps:**
1. On SessionDetailPage
2. Click "Practice Grammar Topics" button
3. Observe navigation

**Expected:**
- ✅ Navigate to /grammar/practice?topics={ids}
- ✅ Topic IDs from session analysis
- ✅ Grammar practice starts with those topics

---

### 8. Keyboard Shortcuts

#### T5-K-001: Escape to End Session
**Priority:** HIGH
**Steps:**
1. In active conversation
2. Press Escape key
3. Observe confirmation modal

**Expected:**
- ✅ "End session?" confirmation modal appears
- ✅ Can cancel with Escape again or click Cancel
- ✅ Can confirm with Enter or click End Session

---

#### T5-K-002: Ctrl+/ to Toggle Grammar Panel
**Priority:** MEDIUM
**Steps:**
1. In conversation
2. Press Ctrl+/
3. Observe panel toggle

**Expected:**
- ✅ Grammar panel collapses/expands
- ✅ Keyboard shortcut works
- ✅ Smooth transition

---

#### T5-K-003: Enter to Send Message
**Priority:** HIGH
**Steps:**
1. Type message
2. Press Enter
3. Observe send

**Expected:**
- ✅ Message sent
- ✅ Same behavior as clicking Send button

---

#### T5-K-004: Shift+Enter for Newline
**Priority:** MEDIUM
**Steps:**
1. Type text
2. Press Shift+Enter
3. Type more text
4. Press Enter

**Expected:**
- ✅ Shift+Enter adds newline (doesn't send)
- ✅ Enter sends message
- ✅ Multi-line message sent correctly

---

#### T5-K-005: Alt+A/O/U/S for German Characters
**Priority:** MEDIUM
**Steps:**
1. Test all Alt shortcuts in chat input
2. Verify character insertion

**Expected:**
- ✅ Alt+A → ä
- ✅ Alt+O → ö
- ✅ Alt+U → ü
- ✅ Alt+S → ß
- ✅ All work correctly

---

#### T5-K-006: Keyboard Shortcuts Don't Conflict
**Priority:** LOW
**Steps:**
1. Try various keyboard shortcuts
2. Check for conflicts with browser shortcuts

**Expected:**
- ✅ No conflicts with Ctrl+C/V/X (copy/paste/cut)
- ✅ No conflicts with Ctrl+T (new tab)
- ✅ Escape doesn't conflict with browser back

---

### 9. Mobile Responsiveness

#### T5-M-001: Mobile Layout (<768px)
**Priority:** HIGH
**Steps:**
1. Resize browser to mobile width (<768px)
2. Navigate to conversation
3. Observe layout

**Expected:**
- ✅ Chat interface full width
- ✅ Grammar panel inline (below messages)
- ✅ Session header stacks vertically
- ✅ No horizontal scroll

---

#### T5-M-002: Mobile - German Character Buttons
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Check German character input buttons

**Expected:**
- ✅ Buttons remain visible and accessible
- ✅ Compact layout
- ✅ Touch-friendly button size

---

#### T5-M-003: Mobile - Message Bubbles
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Send and receive messages
3. Observe bubble layout

**Expected:**
- ✅ Message bubbles fit screen width
- ✅ No overflow or cut-off text
- ✅ Readable font size

---

#### T5-M-004: Mobile - Chat Input
**Priority:** HIGH
**Steps:**
1. On mobile width
2. Focus on chat input
3. Type message

**Expected:**
- ✅ Textarea expands properly
- ✅ Virtual keyboard doesn't cover input
- ✅ Send button accessible
- ✅ Character count visible

---

#### T5-M-005: Mobile - Session Header
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Check session header

**Expected:**
- ✅ Context name visible
- ✅ Timer and message count stacked or hidden
- ✅ End session button accessible
- ✅ Hamburger menu for options (if applicable)

---

#### T5-M-006: Mobile - Grammar Panel Toggle
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Toggle grammar panel
3. Observe behavior

**Expected:**
- ✅ Panel shows inline (not sidebar)
- ✅ Can expand/collapse sections
- ✅ Doesn't break layout

---

#### T5-M-007: Mobile - Context Selection
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Navigate to ContextsPage
3. Observe grid layout

**Expected:**
- ✅ Single column grid
- ✅ Context cards full width
- ✅ Touch-friendly button size
- ✅ Smooth scrolling

---

#### T5-M-008: Mobile - Session History
**Priority:** MEDIUM
**Steps:**
1. On mobile width
2. Navigate to HistoryPage
3. Observe layout

**Expected:**
- ✅ Session cards stack vertically
- ✅ All information visible
- ✅ No horizontal scroll
- ✅ Touch-friendly interactions

---

### 10. Error Handling

#### T5-E-001: Network Error During Message Send
**Priority:** HIGH
**Steps:**
1. Disable network (DevTools → Network → Offline)
2. Try to send message
3. Observe error handling

**Expected:**
- ✅ Error toast displayed
- ✅ Message: "Failed to send message. Check your connection."
- ✅ Message not lost (can retry)
- ✅ Graceful degradation

---

#### T5-E-002: Session Not Found (404)
**Priority:** MEDIUM
**Steps:**
1. Manually change sessionId in localStorage to invalid value
2. Try to send message
3. Observe error

**Expected:**
- ✅ Error detected
- ✅ Session cleared
- ✅ Navigate to context selection
- ✅ Toast: "Session expired. Please start a new conversation."

---

#### T5-E-003: AI Service Timeout
**Priority:** MEDIUM
**Steps:**
1. Send message
2. If AI response takes >30 seconds
3. Observe timeout handling

**Expected:**
- ✅ Timeout error after 30 seconds
- ✅ Error message displayed
- ✅ Can retry sending message
- ✅ Session not corrupted

---

#### T5-E-004: Invalid Context Selection
**Priority:** LOW
**Steps:**
1. Try to start conversation with invalid context ID
2. Observe error

**Expected:**
- ✅ Error toast displayed
- ✅ Navigate back to context selection
- ✅ No session created

---

#### T5-E-005: Backend API Down
**Priority:** HIGH
**Steps:**
1. Stop backend server
2. Try to start conversation
3. Observe error handling

**Expected:**
- ✅ Error toast: "Failed to connect to server"
- ✅ Helpful message suggesting retry
- ✅ No crash or infinite loading

---

#### T5-E-006: Corrupted localStorage Data
**Priority:** LOW
**Steps:**
1. Manually corrupt conversation session in localStorage
2. Reload page
3. Observe error handling

**Expected:**
- ✅ Corrupted data detected
- ✅ localStorage cleared
- ✅ Starts fresh (no crash)
- ✅ Error logged to console

---

#### T5-E-007: Empty AI Response
**Priority:** LOW
**Steps:**
1. (If possible) Mock empty AI response from backend
2. Observe handling

**Expected:**
- ✅ Handles empty response gracefully
- ✅ Shows error or default message
- ✅ Doesn't break conversation

---

#### T5-E-008: Character Limit Exceeded (Edge Case)
**Priority:** LOW
**Steps:**
1. Try to bypass 5000 character limit (paste huge text)
2. Observe validation

**Expected:**
- ✅ Truncated to 5000 characters
- ✅ OR: Paste rejected with warning
- ✅ No backend error

---

#### T5-E-009: Grammar Feedback API Error
**Priority:** LOW
**Steps:**
1. Send message with "Request Feedback" checked
2. If grammar feedback API fails
3. Observe error handling

**Expected:**
- ✅ Message still sent and received
- ✅ Grammar panel shows error state
- ✅ Conversation continues normally

---

#### T5-E-010: Session End API Failure
**Priority:** MEDIUM
**Steps:**
1. End session while backend is unreachable
2. Observe error handling

**Expected:**
- ✅ Error toast displayed
- ✅ Session still cleared from frontend
- ✅ Can start new conversation
- ✅ No data loss

---

## 📊 Test Execution Tracking

### Legend:
- ✅ PASS
- ❌ FAIL
- ⚠️ WARNING (works but with issues)
- ⏭️ SKIPPED
- 🔄 RETEST

### Execution Plan:
1. **Day 1:** Test Categories 1-3 (Context, Practice Flow, Grammar Panel)
2. **Day 2:** Test Categories 4-7 (Vocabulary, German Input, Session Persistence, History)
3. **Day 3:** Test Categories 8-10 (Keyboard Shortcuts, Mobile, Error Handling)

---

## 🎯 Success Criteria

**Phase 5 is considered READY FOR PRODUCTION when:**
- ✅ All HIGH priority tests pass (80+ tests)
- ✅ 90%+ of MEDIUM priority tests pass
- ✅ No CRITICAL bugs found
- ✅ Mobile responsiveness works
- ✅ Error handling is robust
- ✅ Session persistence is reliable

---

**Last Updated:** 2026-01-20
**Next Action:** Execute test plan on Ubuntu server (http://192.168.178.100:5173)
