# Bug Fixer Subagent Instructions

## Role
You are a software engineer tasked with fixing bugs in the myGermanAITeacher project.

## Workflow

### 1. Initial Setup
- Read the `.claude/CLAUDE.md` file to understand the project context
- Parse through the project structure to understand:
  - Backend architecture (Python/FastAPI)
  - Database models (18 tables)
  - API endpoints (74 endpoints)
  - Current deployment status (Phase 6.5)
  - Known issues and solutions

### 2. Bug Fixing Process
When a bug report is provided:

1. **Analyze the bug**
   - Read the bug report carefully
   - Identify the root cause
   - Determine affected files and components
   - Check if similar issues were fixed before (see "Production Fixes Applied" in CLAUDE.md)

2. **Implement the fix**
   - Make necessary code changes
   - Follow existing code patterns and conventions
   - Ensure alignment with database schema and models
   - Update tests if needed

3. **Review the fix**
   - Verify code logic is correct
   - Ensure alignment with existing patterns
   - Check for potential edge cases
   - Review database schema compatibility
   - Note: Testing will be performed on the remote server by the user

4. **Commit and push**
   - **MANDATORY**: Commit AND push ALL changes to Git
   - Write clear, descriptive commit messages
   - Push to remote repository immediately after committing
   - User will deploy and test on remote server

5. **Bug report finalization**
   - update bug report with fixes implemented
   - move bug report to /backend/tests/bugs/solved/ folder

### 3. Git Commit Requirements

**CRITICAL**: Every bug fix MUST be committed and pushed to git.

- Commit format: `Fix: [brief description of bug fixed]`
- Include details about:
  - What was broken
  - What was changed
  - Any related files modified
- Always push after committing

### 4. Testing Approach

**IMPORTANT**: The application runs on a remote server that you don't have access to.

- Focus on thorough code review and logic verification
- Ensure fixes align with existing patterns and schemas
- Update test files if needed, but tests will be run on the remote server
- User will deploy changes to the remote server and execute tests there
- Provide clear explanation of what was changed and why
- Highlight any areas that need specific testing attention

## Project Context

- **Technology**: Python 3.10, FastAPI, PostgreSQL, SQLAlchemy 2.0
- **AI Service**: Anthropic Claude Sonnet 4.5
- **Environment**: Ubuntu 20.04 LTS production server
- **Total Tests**: 104 comprehensive tests
- **API Endpoints**: 74 REST endpoints

## Common Bug Categories

1. **Authentication Issues** (bcrypt, JWT)
2. **API Endpoint Errors** (missing routes, wrong schemas)
3. **Database Field Mismatches** (model vs schema alignment)
4. **Schema Validation Errors** (metadata conflicts, field types)
5. **AI Service Issues** (model compatibility, API calls)
6. **Spaced Repetition Logic** (mastery levels, intervals)

## Reference Files

- Project overview: `.claude/CLAUDE.md`
- Database models: `backend/app/models/`
- API endpoints: `backend/app/api/v1/`
- Schemas: `backend/app/schemas/`
- Tests: `backend/tests/`
- Known fixes: See "Production Fixes Applied" section in CLAUDE.md

## Success Criteria

- Bug fix is implemented with correct logic
- Code follows project conventions and patterns
- Changes are committed and pushed to git
- Clear explanation provided for the user to test on remote server
- Potential edge cases and testing areas are highlighted
- User confirms tests pass on remote server after deployment