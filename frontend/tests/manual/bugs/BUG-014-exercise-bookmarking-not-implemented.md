# BUG-014: Exercise Bookmarking Not Implemented

**Date Reported:** 2026-01-19
**Reporter:** Automated E2E Test Suite (Phase 1)
**Severity:** 🔴 HIGH
**Priority:** P0 - Critical
**Status:** Open
**Module:** Grammar Practice
**Affects:** Session management, User experience, Results page

---

## Summary

Exercise bookmarking functionality is not implemented. Users cannot bookmark difficult exercises for later review using the B key or bookmark button. Bookmarks are not persisted or displayed in results.

---

## Expected Behavior

1. **Bookmark with B Key:**
   - Press `B` key during exercise to toggle bookmark
   - Icon should change from outline to filled
   - Bookmark state should persist

2. **Bookmark Button UI:**
   - Star icon visible in exercise header
   - Click to toggle bookmark state
   - Visual feedback (outline → filled)

3. **Bookmark Persistence:**
   - Bookmarks saved to localStorage
   - Persist across exercises in session
   - Available after session ends

4. **Bookmarks in Results:**
   - Display bookmarked exercises count
   - Show list of bookmarked exercises
   - Allow navigation to bookmarked topics

5. **Multi-Exercise Bookmarking:**
   - Support multiple bookmarks per session
   - Track bookmark status per exercise
   - Clear indication of bookmarked state

---

## Actual Behavior

- ❌ No bookmark button in UI
- ❌ B key handler not implemented
- ❌ No bookmark icon (outline or filled)
- ❌ Bookmarks not persisted
- ❌ Bookmarks not displayed in results
- ❌ No bookmark state management

---

## Test Results

**6 tests failing (out of 6):**
1. ❌ `should bookmark exercise with B key`
2. ❌ `should toggle bookmark with star button`
3. ❌ `should persist bookmarks across exercises`
4. ❌ `should show filled star icon when bookmarked`
5. ❌ `should display bookmarked exercises in results`
6. ❌ `should unbookmark exercise with B key`

**Pass Rate:** 0% (0/6)

---

## Steps to Reproduce

1. Navigate to `/grammar/practice`
2. Start a practice session
3. Press `B` key on first exercise
4. **Expected:** Star icon fills, exercise bookmarked
5. **Actual:** Nothing happens, no visual feedback

**Alternative:**
1. Start practice session
2. Look for bookmark button in header
3. **Expected:** Star icon button visible
4. **Actual:** No bookmark button exists

---

## Impact Assessment

**User Impact:** 🔴 HIGH
- Cannot mark difficult exercises for review
- No way to track challenging topics
- Poor UX for targeted practice
- Reduces learning efficiency

**Technical Impact:**
- Core UX feature missing
- State management incomplete
- Results page integration needed

**Business Impact:**
- Users cannot personalize learning
- Reduced engagement with grammar practice
- Missing key study tool

---

## Root Cause Analysis

**Missing Components:**
1. **Bookmark Button UI:**
   - No star icon component
   - No button in SessionHeader
   - No filled/outline state management

2. **Keyboard Handler:**
   - No B key listener
   - No bookmark toggle logic

3. **State Management:**
   - No bookmarkedExercises array in store
   - No toggleBookmark action
   - No persistence in localStorage

4. **Results Integration:**
   - Results page doesn't display bookmarks
   - No list of bookmarked exercises
   - No count or summary

---

## Proposed Solution

### 1. Add Bookmark State to Store

```typescript
// grammarStore.ts
interface GrammarStore {
  bookmarkedExercises: Set<number>; // exercise IDs
  toggleBookmark: (exerciseId: number) => void;
  isExerciseBookmarked: (exerciseId: number) => boolean;
}

export const useGrammarStore = create<GrammarStore>((set, get) => ({
  bookmarkedExercises: new Set(),

  toggleBookmark: (exerciseId: number) => {
    const bookmarks = new Set(get().bookmarkedExercises);
    if (bookmarks.has(exerciseId)) {
      bookmarks.delete(exerciseId);
    } else {
      bookmarks.add(exerciseId);
    }
    set({ bookmarkedExercises: bookmarks });
  },

  isExerciseBookmarked: (exerciseId: number) => {
    return get().bookmarkedExercises.has(exerciseId);
  },
}));
```

### 2. Create Bookmark Button Component

```typescript
// components/grammar/BookmarkButton.tsx
import { StarIcon } from '@heroicons/react/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/react/24/solid';

interface BookmarkButtonProps {
  exerciseId: number;
  isBookmarked: boolean;
  onToggle: () => void;
}

export function BookmarkButton({ exerciseId, isBookmarked, onToggle }: BookmarkButtonProps) {
  return (
    <button
      onClick={onToggle}
      data-testid="bookmark-button"
      className="p-2 hover:bg-gray-100 rounded-full transition"
      title={isBookmarked ? "Remove bookmark" : "Bookmark exercise"}
    >
      {isBookmarked ? (
        <StarIconSolid
          className="w-6 h-6 text-yellow-500"
          data-testid="bookmark-icon-filled"
        />
      ) : (
        <StarIcon
          className="w-6 h-6 text-gray-400"
          data-testid="bookmark-icon-outline"
        />
      )}
    </button>
  );
}
```

### 3. Add Keyboard Handler

```typescript
// PracticeSessionPage.tsx
useEffect(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    if (e.key === 'b' || e.key === 'B') {
      const currentExercise = getCurrentExercise();
      if (currentExercise) {
        toggleBookmark(currentExercise.id);
      }
    }
  };

  window.addEventListener('keydown', handleKeyPress);
  return () => window.removeEventListener('keydown', handleKeyPress);
}, [getCurrentExercise, toggleBookmark]);
```

### 4. Add to SessionHeader

```typescript
// components/grammar/SessionHeader.tsx
const { toggleBookmark, isExerciseBookmarked } = useGrammarStore();
const currentExercise = useGrammarStore((state) => state.currentExercise);

<div className="flex items-center gap-2">
  <BookmarkButton
    exerciseId={currentExercise.id}
    isBookmarked={isExerciseBookmarked(currentExercise.id)}
    onToggle={() => toggleBookmark(currentExercise.id)}
  />
  {/* other buttons */}
</div>
```

### 5. Display in Results Page

```typescript
// pages/grammar/ResultsPage.tsx
const bookmarkedExercises = useGrammarStore((state) => state.bookmarkedExercises);
const exercises = useGrammarStore((state) => state.exercises);

const bookmarkedList = exercises.filter(ex => bookmarkedExercises.has(ex.id));

<section data-testid="bookmarked-section">
  <h3>Bookmarked Exercises ({bookmarkedList.length})</h3>
  {bookmarkedList.length > 0 ? (
    <ul>
      {bookmarkedList.map(exercise => (
        <li key={exercise.id} data-testid={`bookmarked-exercise-${exercise.id}`}>
          {exercise.question}
        </li>
      ))}
    </ul>
  ) : (
    <p data-testid="no-bookmarks">No bookmarked exercises</p>
  )}
</section>
```

### 6. Persist in localStorage

```typescript
// Add to Zustand persist middleware partialize
partialize: (state) => ({
  // ... existing fields
  bookmarkedExercises: Array.from(state.bookmarkedExercises), // Convert Set to Array
}),

// Add onRehydrateStorage to convert Array back to Set
onRehydrateStorage: () => (state) => {
  if (state && Array.isArray(state.bookmarkedExercises)) {
    state.bookmarkedExercises = new Set(state.bookmarkedExercises);
  }
},
```

---

## Implementation Checklist

- [ ] Add bookmarkedExercises Set to grammarStore
- [ ] Add toggleBookmark action
- [ ] Add isExerciseBookmarked selector
- [ ] Create BookmarkButton component
- [ ] Import Star icons from heroicons
- [ ] Add B key keyboard handler
- [ ] Add bookmark button to SessionHeader
- [ ] Add bookmarked section to ResultsPage
- [ ] Persist bookmarks in localStorage (Set ↔ Array conversion)
- [ ] Add data-testid attributes for testing
- [ ] Add hover states and transitions
- [ ] Update TypeScript types

---

## Verification Steps

After implementation:
1. Start practice session
2. Press `B` on first exercise → star fills yellow
3. Press `B` again → star outline gray
4. Click star button → same toggle behavior
5. Bookmark 2 exercises, complete session
6. Check results page → shows "Bookmarked Exercises (2)"
7. Reload page → bookmarks still present
8. Check localStorage → bookmarkedExercises array exists

---

## Test Files Affected

- `frontend/tests/e2e/grammar-practice.spec.ts` (lines 620-687)
- Helper: `frontend/tests/e2e/helpers/grammar-helpers.ts` (lines 127-145)

---

## Related Issues

- BUG-012: Session Persistence (prerequisite for bookmark persistence)
- BUG-015: Results page display

---

## Design Considerations

**UI/UX:**
- Use recognizable star icon (universal bookmark symbol)
- Yellow color for bookmarked state (familiar pattern)
- Smooth transition between states
- Tooltip on hover

**Accessibility:**
- ARIA label for screen readers
- Keyboard shortcut (B key)
- Clear visual feedback
- Focus states

**Data Structure:**
- Use Set for O(1) lookup performance
- Convert to Array for JSON serialization
- Store only exercise IDs (not full objects)

**Edge Cases:**
- What if exercise ID is undefined?
- Should bookmarks clear after session ends?
- Maximum number of bookmarks?
- Bookmark exercises from previous sessions?

---

## Performance Considerations

- Set operations are O(1) for add/delete/has
- Avoid re-rendering all exercises on bookmark toggle
- Use selective subscriptions in Zustand
- Debounce localStorage saves

---

## Notes

- Consider adding "Practice Bookmarked" quick action
- Could add bulk unbookmark in results page
- Future: sync bookmarks to backend for cross-device
- Consider bookmark categories (difficult, review, unsure)

---

**Last Updated:** 2026-01-19
**Next Review:** After implementation
