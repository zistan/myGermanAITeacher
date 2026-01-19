# Test Engineer Report: Backend Engineer Subagent Instructions
**Date**: 2026-01-19
**Engineer**: Backend Software Engineer (Claude)
**Commit**: 7148855

## Summary
Created comprehensive instructions for the Backend Software Engineer subagent role. This documentation defines workflows, standards, and mandatory procedures for all future backend development work. This is a documentation-only change with no code modifications.

## Files Modified
- `.claude/subagents/backend-engineer-instructions.md` - New file created with complete backend engineer guidelines

## New Features/Endpoints
N/A - Documentation only

## Database Changes
N/A - No database changes

## Testing Requirements

### Unit Tests Needed
N/A - Documentation only, no code to test

### Integration Tests Needed
N/A - Documentation only, no code to test

### Test Data Requirements
N/A - Documentation only

## API Contract Changes
N/A - No API changes

## Dependencies
N/A - No new dependencies

## Configuration Changes
N/A - No configuration changes

## Known Issues/Limitations
None - Documentation is complete and comprehensive

## Frontend Integration Notes
N/A - This is documentation for backend engineers only

## Additional Notes

### Purpose of This Documentation
This instruction file establishes the standard operating procedures for all backend development work:

1. **Scope Boundaries**: Clearly defines that backend engineers ONLY work in `/backend` directory, never touching `/frontend`

2. **Mandatory Workflows**:
   - Git commit and push after EVERY modification
   - Create test engineer report for ALL changes
   - Follow conventional commit message format

3. **Reference Materials**:
   - Points to `/.claude/claude.md` for project documentation
   - Points to `/brd and planning documents/*.md` for requirements

4. **Development Standards**:
   - Minimum 80% test coverage requirement
   - Type hints and docstrings required
   - Security-first approach (OWASP guidelines)
   - Performance considerations (avoid N+1 queries)

5. **Code Patterns**: Provides templates for:
   - API endpoints
   - Service classes
   - Database models
   - Test structures
   - AI service integration

6. **Common Tasks**: Step-by-step procedures for:
   - Adding new API endpoints
   - Modifying existing features
   - Fixing bugs
   - Creating database models

### Usage
Future sessions should reference this file when:
- Starting new backend development tasks
- Modifying existing backend code
- Fixing backend bugs
- Adding new backend features

### Test Engineer Impact
This documentation creates a new requirement: backend engineers will now create detailed test reports in `/backend/tests/reports/` for every change. Test engineers should:
- Monitor this directory for new reports
- Use reports to understand what needs testing
- Reference the testing requirements section in each report
- Provide feedback if reports are incomplete

### Compliance Verification
To verify compliance with these instructions, check that:
- [ ] All backend changes are committed to git
- [ ] All commits are pushed to remote
- [ ] Test engineer reports exist for all changes
- [ ] No frontend files are modified by backend engineer
- [ ] Tests are written for all new code
- [ ] Code coverage remains above 80%

## Next Steps
1. Review this instruction file to ensure completeness
2. Share with team members working on backend
3. Use as reference for all future backend development
4. Update as needed when new patterns or requirements emerge

---

**Report Type**: Documentation
**Testing Priority**: N/A
**Production Impact**: None (Documentation only)
