"""
Integration API endpoints for cross-module workflows.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict

from app.database import get_db
from app.models.user import User
from app.services.integration_service import IntegrationService
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/v1/integration/session-analysis/{session_id}")
def analyze_conversation_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Analyze a conversation session and get grammar/vocabulary recommendations.

    This endpoint analyzes a completed conversation session and provides:
    - Session summary (duration, message count, context)
    - Detected grammar topics and vocabulary words
    - Personalized recommendations for practice
    - Next steps for learning

    Args:
        session_id: ID of the conversation session to analyze

    Returns:
        Comprehensive session analysis with recommendations
    """
    integration = IntegrationService(db)
    analysis = integration.analyze_conversation_session(session_id, current_user.id)

    if "error" in analysis:
        raise HTTPException(status_code=404, detail=analysis["error"])

    return analysis


@router.get("/v1/integration/learning-path")
def get_personalized_learning_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get personalized learning path across all modules.

    This endpoint generates a comprehensive learning plan including:
    - Focus areas based on current progress and errors
    - Daily study plan (60-90 minutes)
    - Weekly study goals
    - Recommended conversation contexts
    - Motivation message

    Returns:
        Personalized learning path with daily and weekly plans
    """
    integration = IntegrationService(db)
    learning_path = integration.get_personalized_learning_path(current_user.id)
    return learning_path


@router.get("/v1/integration/dashboard")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> Dict:
    """Get comprehensive dashboard data combining all modules.

    This is the main dashboard endpoint that provides:
    - Overall progress across all modules
    - Personalized learning path
    - Items due for review today (grammar + vocabulary)
    - Recent activity (last 7 days)
    - Achievements close to completion
    - Quick action recommendations

    Returns:
        Complete dashboard data for the user
    """
    integration = IntegrationService(db)
    dashboard = integration.get_dashboard_data(current_user.id)
    return dashboard
