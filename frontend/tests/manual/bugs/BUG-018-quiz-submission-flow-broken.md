# BUG-018: Quiz Submission Flow Broken

**Date Reported:** 2026-01-19
**Reporter:** Automated E2E Test Suite (Phase 1)
**Severity:** 🔴 HIGH
**Priority:** P0 - Critical
**Status:** Open
**Module:** Vocabulary - Quiz
**Affects:** Quiz functionality, Scoring, Progress tracking

---

## Summary

Vocabulary quiz submission flow is broken. Users cannot submit answers, questions don't advance, feedback is not displayed, and scoring doesn't work. Multiple quiz types (multiple choice, fill-in-blank, matching) are all affected.

---

## Expected Behavior

1. **Multiple Choice Questions:**
   - Display question with 4 options
   - Click option to select
   - Submit button activates
   - Submit → immediate feedback (correct/incorrect)
   - Advance to next question

2. **Fill-in-Blank Questions:**
   - Display sentence with blank
   - Type answer in input field
   - Submit button enabled when text entered
   - Submit → show correct answer comparison
   - Advance to next question

3. **Matching Questions:**
   - Display two columns (words and definitions)
   - Click to create matches
   - Submit all matches together
   - Show which matches correct/incorrect
   - Advance to next question

4. **Immediate Feedback:**
   - Green checkmark for correct
   - Red X for incorrect
   - Show correct answer if wrong
   - Display explanation (optional)

5. **Progress Tracking:**
   - Update question counter (1/10)
   - Calculate score in real-time
   - Show progress bar
   - Display results at end

---

## Actual Behavior

- ❌ Cannot submit answers (no API call)
- ❌ Questions don't advance
- ❌ No feedback displayed
- ❌ Score not calculated
- ❌ Progress not tracked
- ❌ Results page doesn't show quiz data

---

## Test Results

**7 tests failing (out of 10):**
1. ❌ `should submit multiple choice answer`
2. ❌ `should display correct/incorrect feedback`
3. ❌ `should advance to next question after submission`
4. ❌ `should submit fill-in-blank answer`
5. ❌ `should submit matching question answers`
6. ❌ `should calculate score correctly`
7. ❌ `should display quiz results at end`
8. ✅ `should display multiple choice options` (UI exists but not functional)
9. ✅ `should enable submit button when answer selected` (partial)
10. ✅ `should show progress indicator` (partial - if quiz starts)

**Pass Rate:** 30% (3/10) - UI exists but functionality broken

---

## Steps to Reproduce

**Test 1: Multiple Choice**
1. Navigate to `/vocabulary/quiz`
2. Start quiz session
3. Click option A
4. Click "Submit" button
5. **Expected:** See feedback, advance to next question
6. **Actual:** Nothing happens, no API call

**Test 2: Fill-in-Blank**
1. Start quiz
2. Type answer in input field
3. Click "Submit"
4. **Expected:** See correct answer comparison, advance
5. **Actual:** No submission occurs

**Test 3: Scoring**
1. Start quiz with 10 questions
2. Answer 7 correctly, 3 incorrectly
3. Complete quiz
4. **Expected:** See "Score: 7/10 (70%)"
5. **Actual:** No score calculated or displayed

---

## Impact Assessment

**User Impact:** 🔴 CRITICAL
- Cannot use quiz feature at all
- No way to test vocabulary knowledge
- Missing key assessment tool
- No feedback on learning progress

**Technical Impact:**
- API integration incomplete
- State management broken
- Quiz state machine not implemented
- Results calculation missing

**Business Impact:**
- Vocabulary quiz module unusable
- Assessment feature non-functional
- Users cannot track knowledge
- Major feature completely broken

---

## Root Cause Analysis

**Missing Components:**
1. **Answer Submission:**
   - No API call to POST /api/v1/vocabulary/quiz/{quiz_id}/answer
   - No submitAnswer action in store

2. **Question Advancement:**
   - No logic to fetch next question
   - State doesn't update after submission

3. **Feedback Display:**
   - No feedback component
   - No correct/incorrect indication
   - Correct answer not shown

4. **Score Calculation:**
   - No tracking of correct answers
   - No percentage calculation
   - Results page doesn't receive quiz data

5. **Quiz State Machine:**
   - States: idle → in_progress → feedback → next_question → completed
   - Transitions not implemented

---

## Proposed Solution

### 1. Add Quiz State to Store

```typescript
// store/vocabularyStore.ts
interface QuizState {
  quizId: string | null;
  currentQuestion: QuizQuestion | null;
  currentQuestionIndex: number;
  totalQuestions: number;
  userAnswers: Map<number, any>; // question_id → answer
  correctAnswers: number;
  isShowingFeedback: boolean;
  lastAnswerCorrect: boolean | null;
}

interface VocabularyStore {
  quiz: QuizState;
  submitQuizAnswer: (answer: any) => Promise<void>;
  advanceToNextQuestion: () => void;
  completeQuiz: () => void;
}

export const useVocabularyStore = create<VocabularyStore>((set, get) => ({
  quiz: {
    quizId: null,
    currentQuestion: null,
    currentQuestionIndex: 0,
    totalQuestions: 0,
    userAnswers: new Map(),
    correctAnswers: 0,
    isShowingFeedback: false,
    lastAnswerCorrect: null,
  },

  submitQuizAnswer: async (answer: any) => {
    const { quiz } = get();
    if (!quiz.quizId || !quiz.currentQuestion) return;

    try {
      // Submit answer to API
      const response = await axios.post(
        `/api/v1/vocabulary/quiz/${quiz.quizId}/answer`,
        {
          question_id: quiz.currentQuestion.id,
          answer: answer,
        }
      );

      // Update state with feedback
      const isCorrect = response.data.is_correct;
      set({
        quiz: {
          ...quiz,
          userAnswers: new Map(quiz.userAnswers).set(quiz.currentQuestion.id, answer),
          correctAnswers: quiz.correctAnswers + (isCorrect ? 1 : 0),
          isShowingFeedback: true,
          lastAnswerCorrect: isCorrect,
        },
      });

      // Auto-advance after 2 seconds
      setTimeout(() => {
        get().advanceToNextQuestion();
      }, 2000);
    } catch (error) {
      console.error('Failed to submit quiz answer:', error);
    }
  },

  advanceToNextQuestion: () => {
    const { quiz } = get();
    const nextIndex = quiz.currentQuestionIndex + 1;

    if (nextIndex >= quiz.totalQuestions) {
      get().completeQuiz();
      return;
    }

    // Fetch next question from API or local cache
    // ... (implementation depends on API structure)

    set({
      quiz: {
        ...quiz,
        currentQuestionIndex: nextIndex,
        isShowingFeedback: false,
        lastAnswerCorrect: null,
      },
    });
  },

  completeQuiz: () => {
    const { quiz } = get();
    // Navigate to results page or show results modal
    // Calculate final score
    const score = (quiz.correctAnswers / quiz.totalQuestions) * 100;
    console.log(`Quiz complete! Score: ${score}%`);
  },
}));
```

### 2. Create Feedback Component

```typescript
// components/vocabulary/QuizFeedback.tsx
import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/solid';

interface QuizFeedbackProps {
  isCorrect: boolean;
  correctAnswer: string;
  userAnswer: string;
  explanation?: string;
}

export function QuizFeedback({ isCorrect, correctAnswer, userAnswer, explanation }: QuizFeedbackProps) {
  return (
    <div
      className={`p-4 rounded-lg mt-4 ${
        isCorrect ? 'bg-green-100 border-green-500' : 'bg-red-100 border-red-500'
      } border-2`}
      data-testid="quiz-feedback"
    >
      <div className="flex items-center gap-2 mb-2">
        {isCorrect ? (
          <>
            <CheckCircleIcon className="w-6 h-6 text-green-600" />
            <span className="font-bold text-green-800" data-testid="feedback-correct">
              Correct!
            </span>
          </>
        ) : (
          <>
            <XCircleIcon className="w-6 h-6 text-red-600" />
            <span className="font-bold text-red-800" data-testid="feedback-incorrect">
              Incorrect
            </span>
          </>
        )}
      </div>

      {!isCorrect && (
        <div className="text-sm">
          <p className="text-gray-700">
            <span className="font-semibold">Your answer:</span> {userAnswer}
          </p>
          <p className="text-gray-700 mt-1">
            <span className="font-semibold">Correct answer:</span> {correctAnswer}
          </p>
        </div>
      )}

      {explanation && (
        <p className="text-sm text-gray-600 mt-2 italic">{explanation}</p>
      )}
    </div>
  );
}
```

### 3. Create Quiz Question Components

```typescript
// components/vocabulary/MultipleChoiceQuestion.tsx
interface MultipleChoiceQuestionProps {
  question: string;
  options: string[];
  selectedOption: string | null;
  onSelect: (option: string) => void;
  disabled?: boolean;
}

export function MultipleChoiceQuestion({
  question,
  options,
  selectedOption,
  onSelect,
  disabled = false,
}: MultipleChoiceQuestionProps) {
  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">{question}</h3>
      <div className="space-y-3">
        {options.map((option, index) => (
          <button
            key={index}
            onClick={() => onSelect(option)}
            disabled={disabled}
            data-testid={`option-${index}`}
            className={`w-full p-4 rounded-lg border-2 text-left transition ${
              selectedOption === option
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-300'
            } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
          >
            <span className="font-semibold mr-2">
              {String.fromCharCode(65 + index)}.
            </span>
            {option}
          </button>
        ))}
      </div>
    </div>
  );
}
```

```typescript
// components/vocabulary/FillBlankQuestion.tsx
interface FillBlankQuestionProps {
  sentence: string;
  blankPosition: number;
  userAnswer: string;
  onAnswerChange: (answer: string) => void;
  disabled?: boolean;
}

export function FillBlankQuestion({
  sentence,
  blankPosition,
  userAnswer,
  onAnswerChange,
  disabled = false,
}: FillBlankQuestionProps) {
  const parts = sentence.split('___');

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Fill in the blank:</h3>
      <div className="text-lg flex items-baseline gap-2">
        <span>{parts[0]}</span>
        <input
          type="text"
          value={userAnswer}
          onChange={(e) => onAnswerChange(e.target.value)}
          disabled={disabled}
          data-testid="fill-blank-input"
          className="border-2 border-blue-500 rounded px-3 py-1 min-w-[150px] focus:outline-none focus:ring-2 focus:ring-blue-300"
          placeholder="Type answer..."
        />
        <span>{parts[1]}</span>
      </div>
    </div>
  );
}
```

### 4. Integrate in Quiz Page

```typescript
// pages/vocabulary/VocabularyQuizPage.tsx
import { MultipleChoiceQuestion } from '@/components/vocabulary/MultipleChoiceQuestion';
import { FillBlankQuestion } from '@/components/vocabulary/FillBlankQuestion';
import { QuizFeedback } from '@/components/vocabulary/QuizFeedback';

export function VocabularyQuizPage() {
  const { quiz, submitQuizAnswer } = useVocabularyStore();
  const [selectedAnswer, setSelectedAnswer] = useState<any>(null);

  const handleSubmit = () => {
    if (selectedAnswer !== null) {
      submitQuizAnswer(selectedAnswer);
    }
  };

  const canSubmit = selectedAnswer !== null && !quiz.isShowingFeedback;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <div className="mb-4 flex justify-between items-center">
        <span className="text-sm text-gray-600" data-testid="question-counter">
          Question {quiz.currentQuestionIndex + 1} of {quiz.totalQuestions}
        </span>
        <span className="text-sm text-gray-600" data-testid="current-score">
          Score: {quiz.correctAnswers}/{quiz.currentQuestionIndex}
        </span>
      </div>

      {quiz.currentQuestion?.type === 'multiple_choice' && (
        <MultipleChoiceQuestion
          question={quiz.currentQuestion.question}
          options={quiz.currentQuestion.options}
          selectedOption={selectedAnswer}
          onSelect={setSelectedAnswer}
          disabled={quiz.isShowingFeedback}
        />
      )}

      {quiz.currentQuestion?.type === 'fill_blank' && (
        <FillBlankQuestion
          sentence={quiz.currentQuestion.sentence}
          blankPosition={quiz.currentQuestion.blank_position}
          userAnswer={selectedAnswer || ''}
          onAnswerChange={setSelectedAnswer}
          disabled={quiz.isShowingFeedback}
        />
      )}

      {quiz.isShowingFeedback && quiz.lastAnswerCorrect !== null && (
        <QuizFeedback
          isCorrect={quiz.lastAnswerCorrect}
          correctAnswer={quiz.currentQuestion?.correct_answer || ''}
          userAnswer={selectedAnswer}
          explanation={quiz.currentQuestion?.explanation}
        />
      )}

      <button
        onClick={handleSubmit}
        disabled={!canSubmit}
        data-testid="submit-answer-button"
        className={`mt-6 w-full py-3 rounded-lg font-semibold transition ${
          canSubmit
            ? 'bg-blue-600 text-white hover:bg-blue-700'
            : 'bg-gray-300 text-gray-500 cursor-not-allowed'
        }`}
      >
        {quiz.isShowingFeedback ? 'Next Question...' : 'Submit Answer'}
      </button>
    </div>
  );
}
```

### 5. Create Results Page

```typescript
// pages/vocabulary/VocabularyQuizResultsPage.tsx
export function VocabularyQuizResultsPage() {
  const { quiz } = useVocabularyStore();
  const scorePercentage = (quiz.correctAnswers / quiz.totalQuestions) * 100;

  return (
    <div className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Quiz Complete!</h1>

      <div className="bg-blue-50 border-2 border-blue-500 rounded-lg p-6 mb-6">
        <div className="text-center">
          <p className="text-6xl font-bold text-blue-600" data-testid="final-score">
            {scorePercentage.toFixed(0)}%
          </p>
          <p className="text-xl text-gray-700 mt-2" data-testid="score-breakdown">
            {quiz.correctAnswers} out of {quiz.totalQuestions} correct
          </p>
        </div>
      </div>

      <div className="space-y-4">
        <h2 className="text-2xl font-semibold">Review Your Answers</h2>
        {/* Map through questions and show results */}
      </div>

      <button
        onClick={() => window.location.href = '/vocabulary'}
        className="mt-6 w-full py-3 bg-blue-600 text-white rounded-lg font-semibold"
      >
        Return to Vocabulary
      </button>
    </div>
  );
}
```

---

## Implementation Checklist

- [ ] Add quiz state to vocabularyStore
- [ ] Create submitQuizAnswer action with API call
- [ ] Create advanceToNextQuestion logic
- [ ] Create MultipleChoiceQuestion component
- [ ] Create FillBlankQuestion component
- [ ] Create MatchingQuestion component
- [ ] Create QuizFeedback component
- [ ] Add feedback display logic (2s auto-advance)
- [ ] Add score calculation
- [ ] Create QuizResultsPage
- [ ] Add progress indicator (X/Y questions)
- [ ] Add data-testid attributes for testing
- [ ] Handle loading/error states
- [ ] Add quiz state persistence (optional)
- [ ] Update TypeScript types
- [ ] Write unit tests

---

## Verification Steps

After implementation:
1. Start quiz with 5 questions
2. Answer first question (multiple choice) → see feedback
3. Wait 2s → advances to next question
4. Answer fill-in-blank question → see feedback
5. Complete all 5 questions
6. See results page with score percentage
7. Verify API calls were made for each submission
8. Check localStorage for quiz state persistence

---

## Test Files Affected

- `frontend/tests/e2e/vocabulary.spec.ts` (lines 542-680)
- Helper: `frontend/tests/e2e/helpers/vocabulary-helpers.ts` (lines 150-200)

---

## Related Issues

- None (standalone critical bug)

---

## API Specification

**Endpoint:** `POST /api/v1/vocabulary/quiz/{quiz_id}/answer`

**Request Body:**
```json
{
  "question_id": 42,
  "answer": "Option A"
}
```

**Response:**
```json
{
  "is_correct": true,
  "correct_answer": "Option A",
  "explanation": "This is the correct answer because...",
  "points_earned": 10,
  "current_score": 70
}
```

---

## Quiz State Machine

```
idle
  ↓ (start quiz)
in_progress
  ↓ (answer selected)
ready_to_submit
  ↓ (submit clicked)
showing_feedback
  ↓ (2s delay or next clicked)
next_question OR completed
```

---

## Design Considerations

**UI/UX:**
- Clear visual feedback (green/red)
- Disabled state during feedback display
- Auto-advance after 2 seconds
- Progress indicator always visible
- Large touch targets for mobile

**Accessibility:**
- Keyboard navigation (arrow keys + Enter)
- ARIA labels for screen readers
- Focus management
- Color + icon feedback (not color alone)

**Performance:**
- Debounce rapid submissions
- Preload next question
- Optimistic UI updates

**Data Integrity:**
- Validate answer format
- Handle network failures
- Prevent duplicate submissions
- Save progress locally

---

## Question Type Handling

| Type | Input Method | Validation | Scoring |
|------|--------------|------------|---------|
| Multiple Choice | Click option | Exact match | 1 point |
| Fill-in-Blank | Text input | Case-insensitive | 1 point |
| Matching | Click pairs | All correct | 1 point per pair |
| True/False | Click button | Exact match | 1 point |

---

## Notes

- Consider adding timer per question (optional challenge mode)
- Add review mode to see all questions after completion
- Consider partial credit for fill-in-blank (fuzzy matching)
- Add difficulty levels (easy/medium/hard)
- Track time per question for analytics
- Consider adaptive difficulty based on performance

---

**Last Updated:** 2026-01-19
**Next Review:** After implementation (highest priority)
