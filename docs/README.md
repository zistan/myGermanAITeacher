# German Learning Application - Documentation

**Last Updated:** 2026-01-22

Welcome to the centralized documentation for the German Learning Application (myGermanAITeacher). This directory contains all project documentation organized by category.

## Documentation Structure

### 📚 [GUIDES/](GUIDES/)
User guides, setup instructions, and how-to documentation:
- **[Setup](GUIDES/setup/)** - Installation and quickstart guides
- **[Deployment](GUIDES/deployment/)** - Production deployment guides and checklists
- **[Troubleshooting](GUIDES/troubleshooting/)** - Common issues and solutions
- **[Frontend](GUIDES/frontend/)** - Frontend-specific documentation
- **[Backend](GUIDES/backend/)** - Backend-specific documentation
- **[Content](GUIDES/content/)** - Content creation and expansion guides

### 🗺️ [CODEMAPS/](CODEMAPS/)
Architecture documentation and code structure maps:
- System architecture overview
- Module dependencies
- Data flow diagrams
- API structure maps

*Note: Codemaps are generated from the actual codebase and will be created by the documentation specialist.*

### 🧪 [testing/](testing/)
Testing documentation, test reports, and bug tracking:
- **[Backend Testing](testing/backend/)** - Backend test reports, bugs, and regression analysis
- **[Frontend Testing](testing/frontend/)** - Frontend test results, manual test plans, and bug reports

### 📖 Additional Documentation
- **[AGENT_INSTRUCTIONS.md](AGENT_INSTRUCTIONS.md)** - Instructions for AI agents working on this project

## Quick Links

### For Developers
- [Project Root README](../README.md) - Project overview and quick start
- [Frontend README](GUIDES/frontend/README.md) - Frontend development guide
- [Backend API Documentation](http://192.168.178.100:8000/docs) - Swagger UI (production server)

### For Deployment
- [Deployment Guide](GUIDES/deployment/DEPLOYMENT_GUIDE.md) - Complete deployment walkthrough
- [Deployment Checklist](GUIDES/deployment/DEPLOYMENT_CHECKLIST.md) - Step-by-step deployment tasks
- [Ubuntu Quickstart](GUIDES/setup/QUICKSTART_UBUNTU.md) - Quick setup guide for Ubuntu

### For Testing
- [Backend Test Status](testing/backend/TEST_STATUS.md) - Current backend test coverage
- [Frontend Test Summary](testing/frontend/TEST_RESULTS_SUMMARY.md) - Frontend test results
- [Bug Reports](testing/) - All bug reports and resolutions

### For Content Creation
- [Content Expansion Plan](GUIDES/content/CONTENT_EXPANSION_PLAN.md) - Plan for expanding learning content
- [Vocabulary Seeds Guide](GUIDES/content/vocabulary-seeds/README.md) - How to create vocabulary seed data

## Project Information

**Backend URL (Production):** http://192.168.178.100:8000
**Frontend URL (Production):** http://192.168.178.100:5173
**API Documentation:** http://192.168.178.100:8000/docs

**Technology Stack:**
- Backend: Python 3.10, FastAPI, PostgreSQL, SQLAlchemy
- Frontend: React 18, TypeScript, Vite, Tailwind CSS
- AI: Anthropic Claude Sonnet 4.5

**Project Status:**
- Backend: ✅ Fully implemented (74 endpoints, 104 tests, 20 models)
- Frontend: 🚀 60% complete (5 of 8 phases done)
- Deployment: ✅ Production server operational

## Documentation Principles

1. **Single Source of Truth** - Documentation is generated from actual code
2. **Freshness** - All docs include last updated timestamps
3. **Organization** - Clear structure with GUIDES, CODEMAPS, and testing separation
4. **Accessibility** - Easy navigation with index files and cross-references
5. **Accuracy** - Regular updates to match codebase changes

## Contributing to Documentation

When updating documentation:
1. Use the document-manager agent for systematic updates
2. Always update timestamps
3. Verify all file paths and links work
4. Keep codemaps under 500 lines for token efficiency
5. Follow the established directory structure

---

**For questions or issues with documentation, please refer to the project's main README or contact the development team.**
