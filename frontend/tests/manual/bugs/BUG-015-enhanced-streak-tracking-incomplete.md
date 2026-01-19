# BUG-015: Enhanced Streak Tracking Incomplete

**Date Reported:** 2026-01-19
**Reporter:** Automated E2E Test Suite (Phase 1)
**Severity:** 🟡 MEDIUM
**Priority:** P1 - High
**Status:** Open
**Module:** Grammar Practice
**Affects:** User motivation, Gamification, Session UI

---

## Summary

Enhanced streak tracking features are incomplete. While basic streak tracking works (correct answers increment, incorrect answers reset), visual feedback and milestone notifications are missing.

---

## Expected Behavior

1. **Streak Increment:**
   - ✅ Increment streak on correct answer (WORKING)
   - ✅ Display current streak with fire emoji 🔥 (WORKING)

2. **Streak Reset:**
   - ✅ Reset streak to 0 on incorrect answer (WORKING)

3. **Milestone Notifications:**
   - ❌ Show notification at streak milestones (3, 5, 10, 15, 20)
   - ❌ Display achievement message ("You're on fire!" at 5)
   - ❌ Celebrate with animation or confetti effect

4. **Visual Feedback:**
   - ❌ Pulse animation when streak increments
   - ❌ Color change at high streaks (orange → red)
   - ❌ Larger icon at milestone streaks

5. **Streak Persistence:**
   - ❌ Maintain streak across exercises
   - ❌ Save streak in session state
   - ❌ Display in results page

---

## Actual Behavior

- ✅ Streak increments correctly
- ✅ Streak resets correctly
- ✅ Fire emoji displays
- ❌ No milestone notifications
- ❌ No visual animations
- ❌ No color changes at high streaks

---

## Test Results

**3 tests failing (out of 5):**
1. ✅ `should increment streak on correct answer` (PASSING)
2. ✅ `should reset streak on incorrect answer` (PASSING)
3. ❌ `should show milestone notification at streak 5`
4. ❌ `should display fire icon with pulse animation`
5. ❌ `should change streak color at milestone (streak 10+)`

**Pass Rate:** 40% (2/5)

---

## Steps to Reproduce

**Test 1: Milestone Notification**
1. Start practice session
2. Answer 5 exercises correctly in a row
3. **Expected:** See notification "You're on fire! 5 correct in a row!"
4. **Actual:** Streak shows "🔥 5" but no notification

**Test 2: Visual Feedback**
1. Answer exercise correctly
2. **Expected:** Fire icon pulses briefly
3. **Actual:** No animation, static display

**Test 3: Color Change**
1. Build streak to 10+
2. **Expected:** Streak color changes (orange → red)
3. **Actual:** Same color regardless of streak value

---

## Impact Assessment

**User Impact:** 🟡 MEDIUM
- Reduced motivation and engagement
- Missing positive reinforcement
- Less satisfying UX during practice
- No celebration of achievements

**Technical Impact:**
- Minor - feature partially implemented
- Animation system needs integration
- Notification component required

**Business Impact:**
- Lower user engagement
- Missed gamification opportunity
- Reduced session completion rates

---

## Root Cause Analysis

**Partial Implementation:**
1. **Basic Logic Works:**
   - Streak state management is correct
   - Increment/reset logic functional
   - Display shows current value

2. **Missing Visual Components:**
   - No notification/toast component
   - No animation CSS or library integration
   - No conditional styling based on streak value

3. **Missing Milestone Logic:**
   - No check for milestone values (3, 5, 10, 15, 20)
   - No trigger for notifications
   - No celebration effects

---

## Proposed Solution

### 1. Add Milestone Detection

```typescript
// grammarStore.ts
const STREAK_MILESTONES = [3, 5, 10, 15, 20, 25, 30];

interface GrammarStore {
  currentStreak: number;
  lastMilestone: number;
  showMilestoneNotification: (streak: number) => void;
  incrementStreak: () => void;
}

incrementStreak: () => {
  const newStreak = get().currentStreak + 1;
  set({ currentStreak: newStreak });

  // Check for milestone
  if (STREAK_MILESTONES.includes(newStreak) && newStreak > get().lastMilestone) {
    get().showMilestoneNotification(newStreak);
    set({ lastMilestone: newStreak });
  }
},
```

### 2. Create Milestone Notification Component

```typescript
// components/grammar/MilestoneNotification.tsx
import { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface MilestoneNotificationProps {
  streak: number;
  onDismiss: () => void;
}

const MILESTONE_MESSAGES = {
  3: "Great start! 🎯",
  5: "You're on fire! 🔥",
  10: "Unstoppable! 💪",
  15: "Amazing streak! ⭐",
  20: "Legendary! 👑",
  25: "Phenomenal! 🚀",
  30: "Master level! 🏆",
};

export function MilestoneNotification({ streak, onDismiss }: MilestoneNotificationProps) {
  useEffect(() => {
    const timer = setTimeout(onDismiss, 3000);
    return () => clearTimeout(timer);
  }, [onDismiss]);

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0, y: -50, scale: 0.8 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        exit={{ opacity: 0, y: -50, scale: 0.8 }}
        className="fixed top-20 left-1/2 -translate-x-1/2 z-50"
        data-testid="milestone-notification"
      >
        <div className="bg-gradient-to-r from-orange-500 to-red-500 text-white px-6 py-4 rounded-lg shadow-2xl">
          <p className="text-2xl font-bold text-center">
            {MILESTONE_MESSAGES[streak] || `${streak} in a row! 🎉`}
          </p>
          <p className="text-sm text-center mt-1 opacity-90">
            {streak} correct answers in a row!
          </p>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}
```

### 3. Add Pulse Animation

```typescript
// components/grammar/StreakDisplay.tsx
import { motion } from 'framer-motion';

interface StreakDisplayProps {
  streak: number;
  shouldPulse?: boolean;
}

export function StreakDisplay({ streak, shouldPulse = false }: StreakDisplayProps) {
  const getStreakColor = (streak: number) => {
    if (streak >= 20) return 'text-red-600';
    if (streak >= 10) return 'text-orange-600';
    if (streak >= 5) return 'text-orange-500';
    return 'text-orange-400';
  };

  const getStreakSize = (streak: number) => {
    if (streak >= 20) return 'text-3xl';
    if (streak >= 10) return 'text-2xl';
    return 'text-xl';
  };

  return (
    <motion.div
      className={`flex items-center gap-1 ${getStreakColor(streak)} ${getStreakSize(streak)}`}
      animate={shouldPulse ? { scale: [1, 1.2, 1] } : {}}
      transition={{ duration: 0.5 }}
      data-testid="streak-display"
    >
      <span className="fire-emoji">🔥</span>
      <span className="font-bold">{streak}</span>
    </motion.div>
  );
}
```

### 4. Integrate in PracticeSessionPage

```typescript
// PracticeSessionPage.tsx
const [showMilestone, setShowMilestone] = useState(false);
const [milestoneStreak, setMilestoneStreak] = useState(0);
const [streakPulse, setStreakPulse] = useState(false);

const { currentStreak } = useGrammarStore();

useEffect(() => {
  const MILESTONES = [3, 5, 10, 15, 20, 25, 30];
  if (MILESTONES.includes(currentStreak)) {
    setMilestoneStreak(currentStreak);
    setShowMilestone(true);
  }

  // Trigger pulse animation
  setStreakPulse(true);
  setTimeout(() => setStreakPulse(false), 500);
}, [currentStreak]);

return (
  <div>
    {showMilestone && (
      <MilestoneNotification
        streak={milestoneStreak}
        onDismiss={() => setShowMilestone(false)}
      />
    )}

    <StreakDisplay streak={currentStreak} shouldPulse={streakPulse} />

    {/* rest of component */}
  </div>
);
```

### 5. Add Confetti Effect (Optional)

```bash
npm install react-confetti canvas-confetti
```

```typescript
// Use canvas-confetti for milestone celebrations
import confetti from 'canvas-confetti';

const celebrateMilestone = (streak: number) => {
  const duration = streak >= 20 ? 3000 : 2000;
  const animationEnd = Date.now() + duration;

  const interval = setInterval(() => {
    const timeLeft = animationEnd - Date.now();
    if (timeLeft <= 0) {
      return clearInterval(interval);
    }

    confetti({
      particleCount: 3,
      angle: 60,
      spread: 55,
      origin: { x: 0 },
      colors: ['#f97316', '#ea580c', '#dc2626'],
    });

    confetti({
      particleCount: 3,
      angle: 120,
      spread: 55,
      origin: { x: 1 },
      colors: ['#f97316', '#ea580c', '#dc2626'],
    });
  }, 250);
};
```

---

## Implementation Checklist

- [ ] Install framer-motion for animations
- [ ] Create MilestoneNotification component
- [ ] Add milestone detection logic to store
- [ ] Create StreakDisplay component with animations
- [ ] Add color gradient based on streak value
- [ ] Add size scaling for high streaks
- [ ] Add pulse animation on increment
- [ ] Integrate milestone notifications in PracticeSessionPage
- [ ] Add data-testid attributes for testing
- [ ] (Optional) Add confetti celebration effect
- [ ] Add sound effect for milestones (optional)
- [ ] Update TypeScript types

---

## Verification Steps

After implementation:
1. Start practice session
2. Answer 3 correctly → see "Great start! 🎯" notification
3. Continue to 5 → see "You're on fire! 🔥" notification
4. Verify fire icon pulses on each correct answer
5. Build streak to 10 → notice color changes to darker orange
6. Build streak to 20 → notice color changes to red, larger size
7. Answer incorrectly → streak resets to 0, no animation

---

## Test Files Affected

- `frontend/tests/e2e/grammar-practice.spec.ts` (lines 689-747)
- Helper: `frontend/tests/e2e/helpers/grammar-helpers.ts` (lines 69-77)

---

## Related Issues

- None (standalone feature enhancement)

---

## Design Considerations

**UI/UX:**
- Notifications should not block exercise content
- Auto-dismiss after 3 seconds
- Smooth animations without distraction
- Color progression (orange → red) indicates intensity

**Accessibility:**
- Respect prefers-reduced-motion setting
- Screen reader announcements for milestones
- Keyboard navigation support

**Gamification:**
- Celebrate achievements without being annoying
- Progressive difficulty (harder to reach higher milestones)
- Visual feedback reinforces positive behavior

**Performance:**
- Use CSS animations where possible
- Debounce animation triggers
- Cleanup timers on unmount

---

## Milestone Values

| Streak | Message | Color | Icon Size |
|--------|---------|-------|-----------|
| 3 | Great start! 🎯 | Orange 400 | Normal |
| 5 | You're on fire! 🔥 | Orange 500 | Normal |
| 10 | Unstoppable! 💪 | Orange 600 | Large |
| 15 | Amazing streak! ⭐ | Orange 700 | Large |
| 20 | Legendary! 👑 | Red 600 | XL |
| 25 | Phenomenal! 🚀 | Red 700 | XL |
| 30+ | Master level! 🏆 | Red 800 | 2XL |

---

## Notes

- Consider adding streak history to session results
- Could add "Best Streak" badge to achievements
- Future: daily streak tracking across sessions
- Consider sound effects for milestones (toggle in settings)
- Add haptic feedback on mobile devices

---

**Last Updated:** 2026-01-19
**Next Review:** After implementation
