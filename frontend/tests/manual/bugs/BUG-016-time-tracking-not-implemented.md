# BUG-016: Time Tracking Not Implemented

**Date Reported:** 2026-01-19
**Reporter:** Automated E2E Test Suite (Phase 1)
**Severity:** 🟡 MEDIUM
**Priority:** P1 - High
**Status:** Open
**Module:** Grammar Practice
**Affects:** Session statistics, User insights, Results page

---

## Summary

Time tracking functionality is not fully implemented. While elapsed time may be tracked internally, it is not displayed in the UI, does not account for paused time correctly, and is not formatted for user readability.

---

## Expected Behavior

1. **Display Elapsed Time:**
   - Show timer in session header
   - Update every second
   - Format: "MM:SS" for < 60 min, "HH:MM:SS" for 60+ min

2. **Pause Support:**
   - Freeze timer when session paused
   - Resume from paused time
   - Do NOT count paused time toward total

3. **Per-Exercise Tracking:**
   - Track time spent on each exercise
   - Display in results breakdown
   - Highlight slowest/fastest exercises

4. **Results Display:**
   - Show total session time
   - Show average time per exercise
   - Show time distribution chart (optional)

5. **Accuracy:**
   - Precise to 1 second
   - Account for page visibility changes
   - Persist across page reloads (with session)

---

## Actual Behavior

- ❌ No timer displayed in UI
- ❌ Paused time not accounted for correctly
- ❌ Time not formatted for display
- ❌ Per-exercise time not tracked
- ❌ Results page doesn't show timing data

---

## Test Results

**4 tests failing (out of 4):**
1. ❌ `should display elapsed time in session header`
2. ❌ `should pause timer when session paused`
3. ❌ `should format time correctly (MM:SS)`
4. ❌ `should track time per exercise`

**Pass Rate:** 0% (0/4)

---

## Steps to Reproduce

**Test 1: Display Timer**
1. Start practice session
2. Look at session header
3. **Expected:** See "05:23" timer updating every second
4. **Actual:** No timer displayed

**Test 2: Pause Support**
1. Start practice session
2. Wait 10 seconds
3. Press P to pause
4. Wait 5 seconds
5. Press P to resume
6. **Expected:** Timer shows ~10 seconds (not 15)
7. **Actual:** Timer may include paused time or not exist

**Test 3: Time Formatting**
1. Start session, wait for timer
2. **Expected:** "00:05" format after 5 seconds
3. **Actual:** No formatted time visible

---

## Impact Assessment

**User Impact:** 🟡 MEDIUM
- Cannot see how long they've been practicing
- No awareness of time spent per exercise
- Missing productivity insights
- Reduced self-awareness during practice

**Technical Impact:**
- Timer hook needed
- Pause integration required
- Formatting utilities missing

**Business Impact:**
- Missing analytics data
- Cannot track engagement duration
- No time-based achievements possible

---

## Root Cause Analysis

**Missing Components:**
1. **Timer Hook:**
   - No useSessionTimer hook
   - No interval management
   - No pause/resume support

2. **UI Display:**
   - No Timer component
   - No formatted time in header
   - No real-time updates

3. **State Integration:**
   - Timer doesn't sync with pause state
   - No per-exercise timing
   - No persistence in session state

4. **Formatting:**
   - No formatTime utility
   - No MM:SS / HH:MM:SS logic

---

## Proposed Solution

### 1. Create Timer Hook

```typescript
// hooks/useSessionTimer.ts
import { useState, useEffect, useRef } from 'react';
import { useGrammarStore } from '@/store/grammarStore';

interface TimerState {
  elapsedTime: number; // in milliseconds
  isRunning: boolean;
}

export function useSessionTimer() {
  const { isPaused, startTime, totalPausedTime } = useGrammarStore();
  const [elapsedTime, setElapsedTime] = useState(0);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (!startTime) return;

    const updateTimer = () => {
      if (isPaused) return;

      const now = Date.now();
      const elapsed = now - startTime - totalPausedTime;
      setElapsedTime(elapsed);
    };

    // Update immediately
    updateTimer();

    // Update every second
    intervalRef.current = setInterval(updateTimer, 1000);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [startTime, isPaused, totalPausedTime]);

  return { elapsedTime, isRunning: !isPaused };
}
```

### 2. Create Timer Component

```typescript
// components/grammar/SessionTimer.tsx
import { useSessionTimer } from '@/hooks/useSessionTimer';
import { formatTime } from '@/utils/timeUtils';

export function SessionTimer() {
  const { elapsedTime, isRunning } = useSessionTimer();

  return (
    <div
      className="flex items-center gap-2 font-mono text-lg"
      data-testid="session-timer"
    >
      <span className={isRunning ? 'text-blue-600' : 'text-gray-500'}>
        ⏱️
      </span>
      <span className="font-semibold">
        {formatTime(elapsedTime)}
      </span>
    </div>
  );
}
```

### 3. Create Time Formatting Utility

```typescript
// utils/timeUtils.ts

/**
 * Format milliseconds to MM:SS or HH:MM:SS
 * @param ms - Elapsed time in milliseconds
 * @returns Formatted time string
 */
export function formatTime(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const pad = (num: number) => num.toString().padStart(2, '0');

  if (hours > 0) {
    return `${hours}:${pad(minutes)}:${pad(seconds)}`;
  }

  return `${pad(minutes)}:${pad(seconds)}`;
}

/**
 * Format milliseconds to human-readable duration
 * @param ms - Duration in milliseconds
 * @returns Human-readable string (e.g., "5 min 23 sec")
 */
export function formatDuration(ms: number): string {
  const totalSeconds = Math.floor(ms / 1000);
  const hours = Math.floor(totalSeconds / 3600);
  const minutes = Math.floor((totalSeconds % 3600) / 60);
  const seconds = totalSeconds % 60;

  const parts: string[] = [];
  if (hours > 0) parts.push(`${hours} hr`);
  if (minutes > 0) parts.push(`${minutes} min`);
  if (seconds > 0 || parts.length === 0) parts.push(`${seconds} sec`);

  return parts.join(' ');
}
```

### 4. Add Timer State to Store

```typescript
// grammarStore.ts
interface GrammarStore {
  startTime: number | null;
  totalPausedTime: number; // in milliseconds
  exerciseStartTime: number | null;
  exerciseTimes: Map<number, number>; // exerciseId -> duration in ms

  startSession: () => void;
  startExercise: (exerciseId: number) => void;
  endExercise: (exerciseId: number) => void;
}

export const useGrammarStore = create<GrammarStore>((set, get) => ({
  startTime: null,
  totalPausedTime: 0,
  exerciseStartTime: null,
  exerciseTimes: new Map(),

  startSession: () => {
    set({
      startTime: Date.now(),
      totalPausedTime: 0,
      exerciseTimes: new Map(),
    });
  },

  startExercise: (exerciseId: number) => {
    set({ exerciseStartTime: Date.now() });
  },

  endExercise: (exerciseId: number) => {
    const { exerciseStartTime, exerciseTimes, isPaused, totalPausedTime } = get();
    if (!exerciseStartTime) return;

    const now = Date.now();
    const duration = now - exerciseStartTime;

    exerciseTimes.set(exerciseId, duration);
    set({
      exerciseTimes: new Map(exerciseTimes),
      exerciseStartTime: null,
    });
  },
}));
```

### 5. Add to SessionHeader

```typescript
// components/grammar/SessionHeader.tsx
import { SessionTimer } from './SessionTimer';

export function SessionHeader() {
  return (
    <header className="flex items-center justify-between p-4">
      <div className="flex items-center gap-4">
        <SessionTimer />
        {/* other components */}
      </div>
    </header>
  );
}
```

### 6. Display in Results Page

```typescript
// pages/grammar/ResultsPage.tsx
import { formatTime, formatDuration } from '@/utils/timeUtils';

export function ResultsPage() {
  const { startTime, totalPausedTime, exerciseTimes, exercises } = useGrammarStore();

  const totalTime = Date.now() - (startTime || 0) - totalPausedTime;
  const averageTime = totalTime / exercises.length;

  return (
    <div>
      <section data-testid="timing-summary">
        <h3>Session Duration</h3>
        <p data-testid="total-time">
          Total Time: {formatDuration(totalTime)}
        </p>
        <p data-testid="average-time">
          Average per Exercise: {formatDuration(averageTime)}
        </p>
      </section>

      <section data-testid="exercise-times">
        <h3>Time Per Exercise</h3>
        <ul>
          {exercises.map(ex => (
            <li key={ex.id} data-testid={`exercise-time-${ex.id}`}>
              Exercise {ex.id}: {formatDuration(exerciseTimes.get(ex.id) || 0)}
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
```

---

## Implementation Checklist

- [ ] Create useSessionTimer hook
- [ ] Create formatTime utility function
- [ ] Create formatDuration utility function
- [ ] Add timer state to grammarStore (startTime, totalPausedTime)
- [ ] Add per-exercise timing state (exerciseTimes Map)
- [ ] Create SessionTimer component
- [ ] Add SessionTimer to SessionHeader
- [ ] Integrate with pause/resume logic (BUG-013)
- [ ] Add timing display to ResultsPage
- [ ] Add average time calculation
- [ ] Add data-testid attributes for testing
- [ ] Handle edge cases (page visibility, timezone changes)
- [ ] Update TypeScript types
- [ ] Write unit tests for formatTime utility

---

## Verification Steps

After implementation:
1. Start practice session → timer shows "00:00"
2. Wait 5 seconds → timer shows "00:05"
3. Wait until 1 minute → timer shows "01:00"
4. Pause session → timer freezes at "01:15"
5. Wait 10 seconds (paused) → timer still shows "01:15"
6. Resume session → timer continues from "01:15"
7. Complete session → results show "Total Time: 2 min 30 sec"
8. Check per-exercise times → each exercise has duration

---

## Test Files Affected

- `frontend/tests/e2e/grammar-practice.spec.ts` (lines 749-800)
- Helper: `frontend/tests/e2e/helpers/grammar-helpers.ts` (lines 79-95)

---

## Related Issues

- BUG-013: Pause/Resume functionality (timer must account for paused time)
- BUG-012: Session Persistence (timer state should persist)

---

## Design Considerations

**UI/UX:**
- Monospace font for timer (consistent width)
- Blue when running, gray when paused
- Prominent but not distracting placement
- Real-time updates (1 second interval)

**Accuracy:**
- Use Date.now() for precision, not setInterval counting
- Account for tab visibility (requestAnimationFrame alternative)
- Handle system time changes gracefully

**Performance:**
- Clear intervals on unmount
- Don't re-render entire page on timer update
- Use selective Zustand subscriptions

**Data Structure:**
- Store timestamps (not durations) for accuracy
- Calculate elapsed time on each render
- Use Map for O(1) exercise time lookup

---

## Edge Cases

**Page Visibility:**
```typescript
// Handle tab backgrounding
useEffect(() => {
  const handleVisibilityChange = () => {
    if (document.hidden) {
      // Tab hidden - timer continues in background
    } else {
      // Tab visible - recalculate elapsed time
      updateTimer();
    }
  };

  document.addEventListener('visibilitychange', handleVisibilityChange);
  return () => document.removeEventListener('visibilitychange', handleVisibilityChange);
}, []);
```

**System Time Changes:**
- If user changes system time, timer may jump
- Consider using performance.now() for relative timing
- Reset timer if unrealistic jump detected

**Long Sessions:**
- Support hours (HH:MM:SS format)
- Consider warning for sessions > 2 hours

---

## Future Enhancements

- Time-based achievements ("Completed 100 exercises in under 30 min")
- Time distribution chart (show time spent per difficulty)
- Optimal time targets per exercise type
- Speed improvement tracking over time
- Daily/weekly time analytics

---

## Notes

- Consider adding "time per correct answer" metric
- Could show fastest/slowest exercises in results
- Future: compare time to average users
- Consider adding timer to focus mode overlay

---

**Last Updated:** 2026-01-19
**Next Review:** After implementation
