"""
Main FastAPI application module.
Configures the API with middleware, CORS, and routes.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import logging
from logging.handlers import RotatingFileHandler
import os

from app.config import settings

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=10485760,  # 10MB
    backupCount=5
)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered German learning application with conversation practice, grammar drilling, and vocabulary management",
    version="1.0.0",
    debug=settings.DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request, call_next):
    """Log all HTTP requests."""
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "status": "active",
        "message": "Welcome to the German Learning API"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "not_configured_yet",  # Will update after database setup
        "ai_service": "not_configured_yet"  # Will update after AI integration
    }


# API routes
from app.api.v1 import auth, sessions, contexts, grammar, vocabulary, analytics, integration

app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(contexts.router, prefix="/api/contexts", tags=["contexts"])
app.include_router(grammar.router, prefix="/api", tags=["grammar"])
app.include_router(vocabulary.router, prefix="/api", tags=["vocabulary"])
app.include_router(analytics.router, prefix="/api", tags=["analytics"])
app.include_router(integration.router, prefix="/api", tags=["integration"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
