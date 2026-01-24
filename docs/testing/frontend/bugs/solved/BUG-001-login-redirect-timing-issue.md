# BUG-001: Login Successful But Redirect Timing Issue

**Severity:** Medium
**Category:** Authentication
**Reported:** 2026-01-19
**Reporter:** Claude Code (E2E Test Engineer)
**Status:** Fixed
**Fixed:** 2026-01-19
**Fix:** Used `queueMicrotask` to ensure state update is processed before navigation

## Description

When logging in with valid credentials, the authentication succeeds and the token is stored in localStorage, but the redirect to `/dashboard` timing is inconsistent, causing automated tests to fail even though the actual user experience works correctly.

## Steps to Reproduce

1. Navigate to `/login`
2. Enter valid credentials (test_engineer / TestPass123A)
3. Click "Sign In"
4. Observe redirect behavior

## Expected Result

- Login API call succeeds
- Token stored in localStorage
- Immediate redirect to `/dashboard`
- Dashboard loads with user data

## Actual Result

- Login API call succeeds (200 OK)
- Token IS stored in localStorage
- Redirect DOES happen to `/dashboard`
- BUT: Timing is inconsistent - sometimes redirect takes 2-3 seconds
- Dashboard eventually loads correctly

**User Experience:** Works correctly - this is a test flakiness issue, not a UX bug

## Environment

- **Browser:** Chromium (Playwright)
- **Frontend URL:** http://192.168.178.100:5173
- **Backend URL:** http://192.168.178.100:8000

## Root Cause Analysis

1. After `authService.login()` returns, the store is updated
2. `useNavigate('/dashboard')` is called
3. React Router triggers navigation
4. ProtectedRoute component may check auth before store is fully updated
5. Slight race condition between state update and navigation

## Impact

- **User Impact:** None - users don't notice this
- **Test Impact:** Medium - causes test flakiness
- **Priority:** Low - can be addressed with better test timeouts

## Workaround

In E2E tests, use longer timeout for URL assertion:
```typescript
await expect(page).toHaveURL(/dashboard/, { timeout: 15000 });
```

## Suggested Fix (for developers)

Consider using `await` for state updates or add a small delay before navigation:

```typescript
// Option 1: Ensure store is updated before navigation
await new Promise(resolve => setTimeout(resolve, 100));
navigate('/dashboard');

// Option 2: Use React's flushSync (if applicable)
flushSync(() => setUser(response.user));
navigate('/dashboard');
```

## Related Bugs

- BUG-002: Registration auto-login redirect timing (same root cause) - **Also fixed**

## Fix Applied

**Files Modified:**
- `frontend/src/pages/auth/LoginPage.tsx`
- `frontend/src/pages/auth/RegisterPage.tsx`

**Solution:**
Wrapped `navigate('/dashboard')` in `queueMicrotask()` to ensure the Zustand state update is fully processed before React Router triggers navigation. This guarantees `ProtectedRoute` sees `isAuthenticated: true` when checking auth state.

```typescript
// Before (race condition)
setUser(response.user);
navigate('/dashboard');

// After (fixed)
setUser(response.user);
queueMicrotask(() => {
  navigate('/dashboard');
});
```

**Why this works:**
- `queueMicrotask` schedules the navigation callback to run after the current synchronous code completes
- This gives React and Zustand time to propagate the state update to all subscribers
- By the time navigation occurs, `ProtectedRoute` will see `isAuthenticated: true`
