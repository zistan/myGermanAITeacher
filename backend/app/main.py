"""
Main FastAPI application module.
Configures the API with middleware, CORS, and routes.
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
import logging
from logging.handlers import RotatingFileHandler
import os

from app.config import settings
from app.database import get_db

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
async def health_check(db: Session = Depends(get_db)):
    """Health check endpoint for monitoring."""

    # Check database connection
    db_status = "disconnected"
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check AI service configuration
    ai_status = "configured" if settings.ANTHROPIC_API_KEY and settings.ANTHROPIC_API_KEY.startswith("sk-ant-") else "not_configured"

    return {
        "status": "healthy" if db_status == "connected" else "degraded",
        "environment": settings.ENVIRONMENT,
        "database": db_status,
        "ai_service": ai_status
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
