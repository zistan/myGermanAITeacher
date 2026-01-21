"""
Tests for session management endpoints.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import status

from app.models.context import Context
from app.models.session import Session, ConversationTurn


@pytest.fixture
def test_context(db_session):
    """Create a test context."""
    context = Context(
        name="Test Context",
        category="business",
        difficulty_level="B2",
        description="Test description",
        system_prompt="You are a test assistant",
        is_active=True
    )
    db_session.add(context)
    db_session.commit()
    db_session.refresh(context)
    return context


class TestSessionEndpoints:
    """Test session management endpoints."""

    @patch('app.api.v1.sessions.ConversationAI')
    def test_start_session_without_context(self, mock_ai, client, auth_headers):
        """Test starting a session without a specific context."""
        # Mock AI service
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_response.return_value = "Guten Tag! Wie kann ich helfen?"
        mock_ai.return_value = mock_ai_instance

        response = client.post(
            "/api/sessions/start",
            json={"session_type": "conversation"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "id" in data
        assert data["session_type"] == "conversation"
        assert data["total_turns"] == 1  # Initial AI message
        # Schema change: context is now flat fields, not nested object
        assert "context_name" in data
        assert data["context_name"] == ""  # Empty when no context

    @patch('app.api.v1.sessions.ConversationAI')
    def test_start_session_with_context(self, mock_ai, client, auth_headers, test_context):
        """Test starting a session with a specific context."""
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_response.return_value = "Willkommen!"
        mock_ai.return_value = mock_ai_instance

        response = client.post(
            "/api/sessions/start",
            json={"context_id": test_context.id, "session_type": "conversation"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["context_id"] == test_context.id
        # Schema change: context fields are now flat, not nested
        assert "context_name" in data
        assert "context_description" in data
        assert "context_category" in data
        assert "context_difficulty" in data
        assert data["context_name"] == "Test Context"
        assert data["context_category"] == "business"
        assert data["context_difficulty"] == "B2"

    def test_start_session_invalid_context(self, client, auth_headers):
        """Test starting session with non-existent context."""
        response = client.post(
            "/api/sessions/start",
            json={"context_id": 99999, "session_type": "conversation"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_start_session_unauthorized(self, client):
        """Test starting session without authentication."""
        response = client.post(
            "/api/sessions/start",
            json={"session_type": "conversation"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @patch('app.api.v1.sessions.ConversationAI')
    def test_send_message_success(self, mock_ai, client, auth_headers, db_session, test_user):
        """Test sending a message in active session."""
        # Create session
        session = Session(
            user_id=test_user.id,
            session_type="conversation",
            ai_model_used="test-model"
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI service
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_response.return_value = "Das ist interessant!"
        mock_ai_instance.analyze_grammar.return_value = []
        mock_ai_instance.detect_vocabulary.return_value = []
        mock_ai.return_value = mock_ai_instance

        user_msg = "Hallo, wie geht es dir?"
        response = client.post(
            f"/api/sessions/{session.id}/message",
            json={"message": user_msg, "request_feedback": True},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Schema change: MessageResponse now includes user_message and turn_number
        assert "turn_id" in data
        assert "user_message" in data
        assert "ai_response" in data
        assert "turn_number" in data
        assert data["user_message"] == user_msg  # Echo back user message
        assert data["ai_response"] == "Das ist interessant!"
        assert isinstance(data["turn_number"], int)
        assert data["turn_number"] > 0
        assert "grammar_feedback" in data
        assert isinstance(data["grammar_feedback"], list)

    @patch('app.api.v1.sessions.ConversationAI')
    def test_send_message_with_grammar_errors(self, mock_ai, client, auth_headers, db_session, test_user):
        """Test sending message that has grammar errors."""
        session = Session(user_id=test_user.id, session_type="conversation")
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI service
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_response.return_value = "Verstehe!"
        mock_ai_instance.analyze_grammar.return_value = [
            {
                "error_type": "case",
                "incorrect_text": "der Mann",  # AI service returns old field names
                "corrected_text": "den Mann",  # AI service returns old field names
                "explanation": "Accusativo necessario",
                "severity": "moderate",
                "rule": "Akkusativ nach sehen"
            }
        ]
        mock_ai_instance.detect_vocabulary.return_value = []
        mock_ai.return_value = mock_ai_instance

        user_msg = "Ich sehe der Mann"
        response = client.post(
            f"/api/sessions/{session.id}/message",
            json={"message": user_msg, "request_feedback": True},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        # Schema change: Check new field names in MessageResponse
        assert "user_message" in data
        assert "turn_number" in data
        assert data["user_message"] == user_msg
        assert len(data["grammar_feedback"]) == 1
        # Schema change: Grammar feedback uses 'incorrect' and 'corrected' now
        feedback = data["grammar_feedback"][0]
        assert feedback["error_type"] == "case"
        assert "incorrect" in feedback  # New field name
        assert "corrected" in feedback  # New field name
        assert feedback["incorrect"] == "der Mann"
        assert feedback["corrected"] == "den Mann"

        # Verify session was updated
        db_session.refresh(session)
        assert session.grammar_errors == 1

    def test_send_message_session_not_found(self, client, auth_headers):
        """Test sending message to non-existent session."""
        response = client.post(
            "/api/sessions/99999/message",
            json={"message": "Test"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('app.api.v1.sessions.ConversationAI')
    def test_end_session_success(self, mock_ai, client, auth_headers, db_session, test_user):
        """Test ending a session."""
        session = Session(
            user_id=test_user.id,
            session_type="conversation",
            total_turns=10,
            grammar_errors=2
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.post(
            f"/api/sessions/{session.id}/end",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "session_summary" in data
        assert data["session_summary"]["total_turns"] == 10
        assert data["session_summary"]["duration_minutes"] >= 0

        # Verify session was updated
        db_session.refresh(session)
        assert session.ended_at is not None
        assert session.overall_score is not None

    def test_end_session_already_ended(self, client, auth_headers, db_session, test_user):
        """Test ending an already ended session."""
        from datetime import datetime

        session = Session(
            user_id=test_user.id,
            session_type="conversation",
            ended_at=datetime.utcnow()
        )
        db_session.add(session)
        db_session.commit()

        response = client.post(
            f"/api/sessions/{session.id}/end",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_session_history(self, client, auth_headers, db_session, test_user):
        """Test retrieving session history."""
        session = Session(user_id=test_user.id, session_type="conversation")
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Add conversation turns
        turn1 = ConversationTurn(
            session_id=session.id,
            turn_number=0,
            speaker="ai",
            message_text="Hallo!"
        )
        turn2 = ConversationTurn(
            session_id=session.id,
            turn_number=1,
            speaker="user",
            message_text="Guten Tag!"
        )
        db_session.add_all([turn1, turn2])
        db_session.commit()

        response = client.get(
            f"/api/sessions/{session.id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "session" in data
        assert "conversation" in data
        assert len(data["conversation"]) == 2
        assert data["conversation"][0]["speaker"] == "ai"

    def test_get_session_history_not_found(self, client, auth_headers):
        """Test getting history of non-existent session."""
        response = client.get(
            "/api/sessions/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
