# Quick Start Prompt for Resuming API Testing

## Copy and paste this prompt to Claude Code when resuming testing:

---

I need you to continue comprehensive API testing for the German Learning Application backend.

**Your Role**: Testing agent - you can ONLY modify test scripts, NOT backend code.

**What to do**:
1. Read `backend/TEST_STATUS.md` for complete status and instructions
2. We've completed Phases 1-6 (75% done)
3. Implement and run Phase 7 (Analytics - 14 endpoints)
4. Then implement and run Phase 8 (Integration - 3 endpoints)

**Key Constraints**:
- You are a TESTING AGENT - report backend bugs, don't fix them
- You CAN fix test script issues (test_api_manual.py)
- When you find backend bugs, provide detailed bug reports with location and fix suggestions

**Current Progress**:
- ✅ Phase 1: Health (100%)
- ✅ Phase 2: Auth (82%)
- ✅ Phase 3: Contexts (100%)
- ✅ Phase 4: Conversations (100%)
- ✅ Phase 5: Grammar (100%)
- ✅ Phase 6: Vocabulary (94%)
- ⏳ Phase 7: Analytics (NEXT - implement tests)
- ⏳ Phase 8: Integration (pending)

**Server**: http://192.168.178.100:8000

Start by reviewing TEST_STATUS.md, then implement Phase 7 tests following the pattern from Phase 6.

---
