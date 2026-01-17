"""
Session management API endpoints for conversation practice.
"""
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.session import Session as SessionModel, ConversationTurn
from app.models.context import Context
from app.models.progress import GrammarCorrection
from app.schemas.session import (
    SessionStart,
    SessionResponse,
    SessionWithContext,
    MessageSend,
    MessageResponse,
    SessionEndResponse,
    SessionHistoryResponse,
    SessionSummary,
    GrammarFeedbackItem,
    VocabularyItem
)
from app.api.deps import get_current_active_user
from app.services.ai_service import ConversationAI, AIServiceError

router = APIRouter()


@router.post("/start", response_model=SessionWithContext, status_code=status.HTTP_201_CREATED)
def start_session(
    session_data: SessionStart,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Start a new practice session.

    Args:
        session_data: Session configuration
        current_user: Authenticated user
        db: Database session

    Returns:
        SessionWithContext: Created session with context details and initial AI message
    """
    # Validate context if provided
    context = None
    if session_data.context_id:
        context = db.query(Context).filter(
            Context.id == session_data.context_id,
            Context.is_active == True
        ).first()
        if not context:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Context not found or inactive"
            )

    # Create session
    new_session = SessionModel(
        user_id=current_user.id,
        context_id=session_data.context_id,
        session_type=session_data.session_type,
        ai_model_used="claude-3-5-sonnet-20241022"
    )

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # Generate initial AI message
    ai_service = ConversationAI()
    context_prompt = context.system_prompt if context else "Have a general conversation in German."

    try:
        initial_message = ai_service.generate_response(
            context_prompt=context_prompt,
            conversation_history=[],
            user_message="[Start conversation with a greeting]",
            user_level=current_user.proficiency_level
        )

        # Save AI's initial turn
        ai_turn = ConversationTurn(
            session_id=new_session.id,
            turn_number=0,
            speaker="ai",
            message_text=initial_message
        )
        db.add(ai_turn)
        new_session.total_turns = 1
        db.commit()

    except AIServiceError as e:
        # If AI fails, use fallback
        initial_message = "Guten Tag! Wie kann ich Ihnen heute helfen?"

    # Prepare response
    response = SessionWithContext(
        **new_session.__dict__,
        context={"name": context.name, "description": context.description} if context else None
    )

    return response


@router.post("/{session_id}/message", response_model=MessageResponse)
def send_message(
    session_id: int,
    message_data: MessageSend,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a message in an active conversation session.

    Args:
        session_id: Session ID
        message_data: Message content and options
        current_user: Authenticated user
        db: Database session

    Returns:
        MessageResponse: AI response with feedback
    """
    # Get session
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id,
        SessionModel.ended_at == None
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found or already ended"
        )

    # Get context
    context = None
    if session.context_id:
        context = db.query(Context).filter(Context.id == session.context_id).first()

    # Get conversation history
    turns = db.query(ConversationTurn).filter(
        ConversationTurn.session_id == session_id
    ).order_by(ConversationTurn.turn_number).all()

    conversation_history = []
    for turn in turns:
        role = "assistant" if turn.speaker == "ai" else "user"
        conversation_history.append({"role": role, "content": turn.message_text})

    # Save user's turn
    user_turn_number = len(turns)
    user_turn = ConversationTurn(
        session_id=session_id,
        turn_number=user_turn_number,
        speaker="user",
        message_text=message_data.message
    )
    db.add(user_turn)
    db.commit()
    db.refresh(user_turn)

    # Analyze grammar if requested
    grammar_feedback = []
    if message_data.request_feedback:
        ai_service = ConversationAI()
        errors = ai_service.analyze_grammar(
            user_message=message_data.message,
            user_level=current_user.proficiency_level,
            context_name=context.name if context else "general"
        )

        # Save grammar corrections
        for error in errors:
            correction = GrammarCorrection(
                turn_id=user_turn.id,
                user_id=current_user.id,
                error_type=error.get("error_type", "other"),
                incorrect_text=error.get("incorrect_text", ""),
                corrected_text=error.get("corrected_text", ""),
                explanation=error.get("explanation", ""),
                severity=error.get("severity", "minor"),
                rule_reference=error.get("rule", "")
            )
            db.add(correction)

            grammar_feedback.append(GrammarFeedbackItem(
                error_type=error.get("error_type", "other"),
                incorrect_text=error.get("incorrect_text", ""),
                corrected_text=error.get("corrected_text", ""),
                explanation=error.get("explanation", ""),
                severity=error.get("severity", "minor"),
                rule=error.get("rule"),
                grammar_topic_hint=error.get("grammar_topic_hint")
            ))

        # Update session error count
        session.grammar_errors += len(errors)

    # Detect vocabulary
    vocabulary_detected = []
    ai_service = ConversationAI()
    vocab_items = ai_service.detect_vocabulary(
        text=message_data.message,
        user_level=current_user.proficiency_level,
        context_name=context.name if context else "general"
    )

    for vocab in vocab_items:
        vocabulary_detected.append(VocabularyItem(
            word=vocab.get("word", ""),
            familiarity_score=0.0,  # Will be calculated based on user progress
            is_new=True  # Will check against user_vocabulary
        ))

    # Generate AI response
    context_prompt = context.system_prompt if context else "Have a general conversation in German."

    try:
        ai_response = ai_service.generate_response(
            context_prompt=context_prompt,
            conversation_history=conversation_history,
            user_message=message_data.message,
            user_level=current_user.proficiency_level
        )
    except AIServiceError:
        ai_response = "Entschuldigung, ich habe gerade technische Probleme. Können Sie das bitte wiederholen?"

    # Save AI's turn
    ai_turn = ConversationTurn(
        session_id=session_id,
        turn_number=user_turn_number + 1,
        speaker="ai",
        message_text=ai_response,
        grammar_feedback=[fb.dict() for fb in grammar_feedback] if grammar_feedback else None,
        vocabulary_used=[v.dict() for v in vocabulary_detected] if vocabulary_detected else None
    )
    db.add(ai_turn)

    # Update session
    session.total_turns += 2  # User + AI
    db.commit()

    return MessageResponse(
        turn_id=ai_turn.id,
        ai_response=ai_response,
        grammar_feedback=grammar_feedback,
        vocabulary_detected=vocabulary_detected,
        suggestions=[]
    )


@router.post("/{session_id}/end", response_model=SessionEndResponse)
def end_session(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    End an active session and get summary.

    Args:
        session_id: Session ID
        current_user: Authenticated user
        db: Database session

    Returns:
        SessionEndResponse: Session summary and recommendations
    """
    # Get session
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    if session.ended_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Session already ended"
        )

    # Calculate duration
    session.ended_at = datetime.utcnow()
    duration = (session.ended_at - session.started_at).total_seconds() / 60
    session.duration_minutes = int(duration)

    # Calculate grammar accuracy
    total_errors = session.grammar_errors
    grammar_accuracy = 1.0 - min(total_errors / max(session.total_turns, 1) * 0.5, 1.0)

    # Get grammar corrections for recommendations
    corrections = db.query(GrammarCorrection).join(ConversationTurn).filter(
        ConversationTurn.session_id == session_id
    ).all()

    # Group errors by type
    error_types = {}
    for correction in corrections:
        error_type = correction.error_type
        error_types[error_type] = error_types.get(error_type, 0) + 1

    # Create recommendations for practice
    grammar_topics_to_practice = []
    for error_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
        if count >= 2:  # At least 2 errors of same type
            grammar_topics_to_practice.append({
                "error_type": error_type,
                "error_count": count,
                "recommendation": f"Review {error_type} rules",
                "practice_available": True
            })

    # Update session scores
    session.overall_score = grammar_accuracy
    session.vocab_score = 0.85  # Placeholder
    session.fluency_score = 0.80  # Placeholder

    db.commit()

    # Create summary
    summary = SessionSummary(
        duration_minutes=session.duration_minutes,
        total_turns=session.total_turns,
        grammar_accuracy=grammar_accuracy,
        vocabulary_used_count=0,  # Will implement with vocabulary tracking
        new_vocabulary_count=0,
        overall_score=session.overall_score,
        achievements=[],
        areas_for_improvement=[
            {
                "area": topic["error_type"],
                "error_count": topic["error_count"],
                "recommendation": topic["recommendation"]
            }
            for topic in grammar_topics_to_practice[:3]  # Top 3
        ]
    )

    return SessionEndResponse(
        session_summary=summary,
        grammar_topics_to_practice=grammar_topics_to_practice
    )


@router.get("/history", response_model=List[SessionResponse])
def list_session_history(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    limit: int = 20,
    offset: int = 0
):
    """
    List user's session history.

    Args:
        current_user: Authenticated user
        db: Database session
        limit: Maximum number of sessions to return
        offset: Number of sessions to skip

    Returns:
        List[SessionResponse]: List of user's sessions
    """
    sessions = db.query(SessionModel).filter(
        SessionModel.user_id == current_user.id
    ).order_by(SessionModel.started_at.desc()).limit(limit).offset(offset).all()

    return [SessionResponse(**session.__dict__) for session in sessions]


@router.get("/{session_id}", response_model=SessionHistoryResponse)
def get_session_detail(
    session_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get session details with all conversation turns.

    Args:
        session_id: Session ID
        current_user: Authenticated user
        db: Database session

    Returns:
        SessionHistoryResponse: Session details with full conversation
    """
    # Get session
    session = db.query(SessionModel).filter(
        SessionModel.id == session_id,
        SessionModel.user_id == current_user.id
    ).first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )

    # Get conversation turns
    turns = db.query(ConversationTurn).filter(
        ConversationTurn.session_id == session_id
    ).order_by(ConversationTurn.turn_number).all()

    return SessionHistoryResponse(
        session=SessionResponse(**session.__dict__),
        conversation=turns
    )
