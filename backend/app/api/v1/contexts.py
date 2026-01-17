"""
Context management API endpoints for conversation scenarios.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional

from app.database import get_db
from app.models.context import Context
from app.models.session import Session as SessionModel
from app.schemas.context import (
    ContextCreate,
    ContextUpdate,
    ContextResponse,
    ContextListItem,
    ContextWithStats
)
from app.api.deps import get_current_active_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[ContextListItem])
def list_contexts(
    category: Optional[str] = Query(None, regex="^(business|daily|finance|social|technical|general|all)$"),
    difficulty: Optional[str] = Query(None, regex="^(A1|A2|B1|B2|C1|C2)$"),
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """
    List all available conversation contexts.

    Args:
        category: Filter by category (business, daily, etc.) or 'all'
        difficulty: Filter by difficulty level (A1-C2)
        active_only: Only return active contexts
        db: Database session

    Returns:
        List[ContextListItem]: List of contexts
    """
    query = db.query(
        Context,
        func.count(SessionModel.id).label('times_used')
    ).outerjoin(
        SessionModel, SessionModel.context_id == Context.id
    ).group_by(Context.id)

    # Apply filters
    if active_only:
        query = query.filter(Context.is_active == True)

    if category and category != "all":
        query = query.filter(Context.category == category)

    if difficulty:
        query = query.filter(Context.difficulty_level == difficulty)

    # Execute query
    results = query.all()

    # Build response
    contexts = []
    for context, times_used in results:
        contexts.append(ContextListItem(
            id=context.id,
            name=context.name,
            category=context.category,
            difficulty_level=context.difficulty_level,
            description=context.description,
            times_used=times_used,
            is_active=context.is_active
        ))

    return contexts


@router.get("/{context_id}", response_model=ContextWithStats)
def get_context(
    context_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific context.

    Args:
        context_id: Context ID
        current_user: Authenticated user
        db: Database session

    Returns:
        ContextWithStats: Context with usage statistics
    """
    # Get context
    context = db.query(Context).filter(Context.id == context_id).first()

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context not found"
        )

    # Get usage stats for this user
    sessions = db.query(SessionModel).filter(
        SessionModel.context_id == context_id,
        SessionModel.user_id == current_user.id,
        SessionModel.ended_at.isnot(None)
    ).all()

    times_used = len(sessions)
    average_score = None
    last_used = None

    if sessions:
        scores = [s.overall_score for s in sessions if s.overall_score is not None]
        if scores:
            average_score = sum(scores) / len(scores)

        last_used = max(s.started_at for s in sessions)

    return ContextWithStats(
        **context.__dict__,
        times_used=times_used,
        average_score=average_score,
        last_used=last_used
    )


@router.post("", response_model=ContextResponse, status_code=status.HTTP_201_CREATED)
def create_context(
    context_data: ContextCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new custom conversation context.

    Args:
        context_data: Context configuration
        current_user: Authenticated user (must be authenticated to create contexts)
        db: Database session

    Returns:
        ContextResponse: Created context
    """
    # Create context
    new_context = Context(
        name=context_data.name,
        category=context_data.category,
        difficulty_level=context_data.difficulty_level,
        description=context_data.description,
        system_prompt=context_data.system_prompt,
        suggested_vocab=context_data.suggested_vocab,
        is_active=context_data.is_active
    )

    db.add(new_context)
    db.commit()
    db.refresh(new_context)

    return new_context


@router.put("/{context_id}", response_model=ContextResponse)
def update_context(
    context_id: int,
    context_data: ContextUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Update an existing context.

    Args:
        context_id: Context ID
        context_data: Updated context data
        current_user: Authenticated user
        db: Database session

    Returns:
        ContextResponse: Updated context
    """
    # Get context
    context = db.query(Context).filter(Context.id == context_id).first()

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context not found"
        )

    # Update fields
    update_data = context_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(context, field, value)

    db.commit()
    db.refresh(context)

    return context


@router.delete("/{context_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_context(
    context_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Delete (deactivate) a context.
    Note: We don't actually delete, just set is_active=False to preserve historical data.

    Args:
        context_id: Context ID
        current_user: Authenticated user
        db: Database session
    """
    # Get context
    context = db.query(Context).filter(Context.id == context_id).first()

    if not context:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Context not found"
        )

    # Deactivate instead of delete
    context.is_active = False
    db.commit()

    return None
