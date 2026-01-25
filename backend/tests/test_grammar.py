"""
Tests for grammar learning endpoints and functionality.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import status
from datetime import datetime, timedelta

from app.models.grammar import (
    GrammarTopic,
    GrammarExercise,
    UserGrammarProgress,
    GrammarSession
)


@pytest.fixture
def test_grammar_topics(db_session):
    """Create test grammar topics."""
    topics = [
        GrammarTopic(
            name_de="Akkusativ",
            name_en="Accusative Case",
            category="cases",
            subcategory="accusative",
            difficulty_level="A2",
            order_index=2,
            description_de="Der Akkusativ wird für direkte Objekte verwendet.",
            explanation_de="Der Akkusativ bezeichnet das direkte Objekt..."
        ),
        GrammarTopic(
            name_de="Modalverben",
            name_en="Modal Verbs",
            category="verbs",
            subcategory="modal_verbs",
            difficulty_level="A2",
            order_index=14,
            description_de="Modalverben drücken Möglichkeit aus.",
            explanation_de="Modalverben modifizieren die Bedeutung..."
        ),
        GrammarTopic(
            name_de="Konjunktiv II",
            name_en="Subjunctive II",
            category="verbs",
            subcategory="subjunctive_ii",
            difficulty_level="B2",
            order_index=15,
            description_de="Der Konjunktiv II drückt Irreales aus.",
            explanation_de="Der Konjunktiv II wird für irreale Bedingungen verwendet..."
        )
    ]

    for topic in topics:
        db_session.add(topic)
    db_session.commit()

    for topic in topics:
        db_session.refresh(topic)

    return topics


@pytest.fixture
def test_grammar_exercises(db_session, test_grammar_topics):
    """Create test grammar exercises."""
    exercises = [
        GrammarExercise(
            topic_id=test_grammar_topics[0].id,  # Akkusativ
            exercise_type="fill_blank",
            difficulty_level="A2",
            question_text="Ich sehe ____ Mann.",
            correct_answer="den",
            alternative_answers=[],
            explanation_de="'Den Mann' ist direktes Objekt (Akkusativ).",
            hints=["Wen oder was siehst du?"],
            context_category="general"
        ),
        GrammarExercise(
            topic_id=test_grammar_topics[0].id,
            exercise_type="multiple_choice",
            difficulty_level="A2",
            question_text="Ich brauche ____.",
            correct_answer="einen Stift",
            alternative_answers=["ein Stift", "einer Stift", "einem Stift"],
            explanation_de="'Stift' ist maskulin. Im Akkusativ: ein → einen.",
            hints=["Stift = maskulin"],
            context_category="general"
        ),
        GrammarExercise(
            topic_id=test_grammar_topics[1].id,  # Modalverben
            exercise_type="fill_blank",
            difficulty_level="A2",
            question_text="Ich ____ schwimmen. (können)",
            correct_answer="kann",
            alternative_answers=[],
            explanation_de="'Können' im Präsens: ich kann.",
            hints=["ich kann"],
            context_category="general"
        )
    ]

    for exercise in exercises:
        db_session.add(exercise)
    db_session.commit()

    for exercise in exercises:
        db_session.refresh(exercise)

    return exercises


class TestGrammarTopicEndpoints:
    """Test grammar topic endpoints."""

    def test_list_grammar_topics(self, client, test_grammar_topics):
        """Test listing all grammar topics."""
        response = client.get("/api/grammar/topics")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3
        assert data[0]["name_de"] == "Akkusativ"

    def test_list_topics_filter_by_category(self, client, test_grammar_topics):
        """Test filtering topics by category."""
        response = client.get("/api/grammar/topics?category=cases")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["category"] == "cases"

    def test_list_topics_filter_by_difficulty(self, client, test_grammar_topics):
        """Test filtering topics by difficulty."""
        response = client.get("/api/grammar/topics?difficulty=B2")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["difficulty_level"] == "B2"

    def test_get_grammar_topic(self, client, auth_headers, test_grammar_topics):
        """Test getting a specific topic with stats."""
        topic_id = test_grammar_topics[0].id

        response = client.get(
            f"/api/grammar/topics/{topic_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == topic_id
        assert data["name_de"] == "Akkusativ"
        assert "user_accuracy" in data
        assert "total_attempts" in data

    def test_get_topic_not_found(self, client, auth_headers):
        """Test getting non-existent topic."""
        response = client.get(
            "/api/grammar/topics/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_topic_exercises(self, client, test_grammar_topics, test_grammar_exercises):
        """Test getting exercises for a topic."""
        topic_id = test_grammar_topics[0].id

        response = client.get(f"/api/grammar/topics/{topic_id}/exercises")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2  # Two Akkusativ exercises

    def test_get_topic_exercises_filter_type(self, client, test_grammar_topics, test_grammar_exercises):
        """Test filtering exercises by type."""
        topic_id = test_grammar_topics[0].id

        response = client.get(
            f"/api/grammar/topics/{topic_id}/exercises?exercise_type=fill_blank"
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["exercise_type"] == "fill_blank"


class TestGrammarPracticeEndpoints:
    """Test grammar practice session endpoints."""

    def test_start_practice_session(self, client, auth_headers, test_grammar_exercises):
        """Test starting a practice session."""
        response = client.post(
            "/api/grammar/practice/start",
            json={
                "exercise_count": 5,
                "difficulty_level": "A2",
                "use_spaced_repetition": False
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "session_id" in data
        assert data["total_exercises"] > 0
        assert data["current_exercise_number"] == 1
        assert isinstance(data["topics_included"], list)

    def test_start_practice_filter_topics(self, client, auth_headers, test_grammar_topics, test_grammar_exercises):
        """Test starting practice with specific topics."""
        topic_ids = [test_grammar_topics[0].id]  # Only Akkusativ

        response = client.post(
            "/api/grammar/practice/start",
            json={
                "topic_ids": topic_ids,
                "exercise_count": 2
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_exercises"] == 2

    def test_start_practice_no_exercises(self, client, auth_headers):
        """Test starting practice with no matching exercises."""
        response = client.post(
            "/api/grammar/practice/start",
            json={
                "difficulty_level": "C2",  # No C2 exercises
                "exercise_count": 5
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_submit_exercise_answer_correct(
        self,
        mock_ai_service,
        client,
        auth_headers,
        db_session,
        test_user,
        test_grammar_exercises
    ):
        """Test submitting a correct answer."""
        # Create a session first
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=3
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI evaluation
        mock_ai_instance = MagicMock()
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": True,
            "is_partially_correct": False,
            "feedback_de": "Richtig! Sehr gut gemacht.",
            "specific_errors": [],
            "suggestions": []
        }
        mock_ai_service.return_value = mock_ai_instance

        exercise_id = test_grammar_exercises[0].id

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": exercise_id,
                "user_answer": "den",
                "time_spent_seconds": 30
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "feedback" in data
        assert data["feedback"]["is_correct"] is True
        assert data["feedback"]["points_earned"] > 0
        assert "session_progress" in data

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_submit_exercise_answer_incorrect(
        self,
        mock_ai_service,
        client,
        auth_headers,
        db_session,
        test_user,
        test_grammar_exercises
    ):
        """Test submitting an incorrect answer."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=3
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI evaluation
        mock_ai_instance = MagicMock()
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": False,
            "is_partially_correct": False,
            "feedback_de": "Nicht ganz. Der richtige Artikel ist 'den'.",
            "specific_errors": ["Falscher Artikel verwendet"],
            "suggestions": ["Denk an den Akkusativ für direkte Objekte"]
        }
        mock_ai_service.return_value = mock_ai_instance

        exercise_id = test_grammar_exercises[0].id

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": exercise_id,
                "user_answer": "der",
                "time_spent_seconds": 45
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["feedback"]["is_correct"] is False
        assert data["feedback"]["points_earned"] == 0
        assert len(data["feedback"]["specific_errors"]) > 0

    def test_submit_answer_session_not_found(self, client, auth_headers, test_grammar_exercises):
        """Test submitting answer to non-existent session."""
        response = client.post(
            "/api/grammar/practice/99999/answer",
            json={
                "exercise_id": test_grammar_exercises[0].id,
                "user_answer": "test"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_submit_multiple_choice_incorrect_never_partial(
        self,
        mock_ai_service,
        client,
        auth_headers,
        db_session,
        test_user,
        test_grammar_exercises
    ):
        """Test that multiple choice incorrect answers are never partially correct."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=3
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI evaluation - for multiple choice, should NEVER return is_partially_correct=true
        mock_ai_instance = MagicMock()
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": False,
            "is_partially_correct": False,  # Must always be False for multiple_choice
            "feedback_de": "Falsch. Die richtige Antwort ist 'einen Stift'.",
            "specific_errors": ["Falsche Option gewählt"],
            "suggestions": ["Bei maskulinen Nomen im Akkusativ: ein → einen"]
        }
        mock_ai_service.return_value = mock_ai_instance

        # Use the multiple choice exercise (test_grammar_exercises[1])
        exercise_id = test_grammar_exercises[1].id

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": exercise_id,
                "user_answer": "ein Stift",  # Wrong answer
                "time_spent_seconds": 20
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify AI was called with exercise_type parameter
        mock_ai_instance.evaluate_answer.assert_called_once()
        call_args = mock_ai_instance.evaluate_answer.call_args
        assert call_args[1]["exercise_type"] == "multiple_choice"

        # Verify response never shows partial correctness
        assert data["feedback"]["is_correct"] is False
        assert data["feedback"]["is_partially_correct"] is False
        assert data["feedback"]["points_earned"] == 0

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_submit_fill_blank_can_be_partially_correct(
        self,
        mock_ai_service,
        client,
        auth_headers,
        db_session,
        test_user,
        test_grammar_exercises
    ):
        """Test that fill_blank exercises can be partially correct (e.g., spelling errors)."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=3
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI evaluation - for fill_blank, can be partially correct
        mock_ai_instance = MagicMock()
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": False,
            "is_partially_correct": True,  # Can be True for fill_blank
            "feedback_de": "Fast richtig! Die Grammatik stimmt, aber die Schreibweise ist 'den' nicht 'denn'.",
            "specific_errors": ["Rechtschreibfehler: 'denn' → 'den'"],
            "suggestions": ["Achte auf die Rechtschreibung: 'den' ist der Artikel"]
        }
        mock_ai_service.return_value = mock_ai_instance

        # Use the fill_blank exercise (test_grammar_exercises[0])
        exercise_id = test_grammar_exercises[0].id

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": exercise_id,
                "user_answer": "denn",  # Spelling error but grammatically would be correct
                "time_spent_seconds": 25
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify AI was called with exercise_type parameter
        mock_ai_instance.evaluate_answer.assert_called_once()
        call_args = mock_ai_instance.evaluate_answer.call_args
        assert call_args[1]["exercise_type"] == "fill_blank"

        # Verify response shows partial correctness
        assert data["feedback"]["is_correct"] is False
        assert data["feedback"]["is_partially_correct"] is True
        assert data["feedback"]["points_earned"] == 1  # Partial points

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_submit_fill_blank_full_sentence_correct(
        self,
        mock_ai_service,
        client,
        auth_headers,
        db_session,
        test_user,
        test_grammar_exercises
    ):
        """Test that fill_blank accepts BOTH just the missing words OR the full correct sentence."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=3
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Mock AI evaluation - full sentence with correct missing words should be CORRECT
        mock_ai_instance = MagicMock()
        mock_ai_instance.evaluate_answer.return_value = {
            "is_correct": True,  # Should be True when full sentence is correct
            "is_partially_correct": False,
            "feedback_de": "Perfekt! Du hast entweder nur die fehlenden Wörter oder den kompletten richtigen Satz geschrieben.",
            "specific_errors": [],
            "suggestions": []
        }
        mock_ai_service.return_value = mock_ai_instance

        exercise_id = test_grammar_exercises[0].id

        response = client.post(
            f"/api/grammar/practice/{session.id}/answer",
            json={
                "exercise_id": exercise_id,
                "user_answer": "Ich sehe den Mann",  # Full correct sentence
                "time_spent_seconds": 20
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Verify AI was called with exercise_type parameter
        mock_ai_instance.evaluate_answer.assert_called_once()
        call_args = mock_ai_instance.evaluate_answer.call_args
        assert call_args[1]["exercise_type"] == "fill_blank"

        # Verify response shows CORRECT for full sentence with correct missing words
        assert data["feedback"]["is_correct"] is True
        assert data["feedback"]["is_partially_correct"] is False
        assert data["feedback"]["points_earned"] > 0  # Points for correct answer

    def test_end_grammar_session(self, client, auth_headers, db_session, test_user):
        """Test ending a grammar practice session."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=5,
            total_attempted=5,
            total_correct=4
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.post(
            f"/api/grammar/practice/{session.id}/end",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "summary" in data
        assert data["summary"]["total_exercises"] == 5
        assert data["summary"]["correct"] == 4
        assert data["summary"]["accuracy"] == 80

    def test_end_session_already_ended(self, client, auth_headers, db_session, test_user):
        """Test ending an already ended session."""
        from app.models.grammar import GrammarSession
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=5,
            ended_at=datetime.utcnow()
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.post(
            f"/api/grammar/practice/{session.id}/end",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_get_next_exercise_first_exercise(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test getting the first exercise when no attempts exist."""
        from app.models.grammar import GrammarSession

        # Create a session with exercise_ids in metadata
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=3,
            grammar_metadata={
                "target_level": "A2",
                "topic_ids": [test_grammar_exercises[0].topic_id],
                "exercise_ids": [ex.id for ex in test_grammar_exercises[:3]],
                "use_spaced_repetition": False
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_grammar_exercises[0].id
        assert "question_text" in data
        assert "correct_answer" in data
        assert "explanation_de" in data

    def test_get_next_exercise_second_exercise(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test getting second exercise after first is answered."""
        from app.models.grammar import GrammarSession, GrammarExerciseAttempt

        # Create session
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=3,
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [ex.id for ex in test_grammar_exercises[:3]]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Answer first exercise
        attempt = GrammarExerciseAttempt(
            grammar_session_id=session.id,
            user_id=test_user.id,
            exercise_id=test_grammar_exercises[0].id,
            user_answer="den",
            is_correct=True,
            time_spent_seconds=30
        )
        db_session.add(attempt)
        db_session.commit()

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_grammar_exercises[1].id  # Should be second exercise

    def test_get_next_exercise_all_completed(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test that 404 is returned when all exercises are answered."""
        from app.models.grammar import GrammarSession, GrammarExerciseAttempt

        # Create session with 2 exercises
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=2,
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [test_grammar_exercises[0].id, test_grammar_exercises[1].id]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Answer both exercises
        for ex in test_grammar_exercises[:2]:
            attempt = GrammarExerciseAttempt(
                grammar_session_id=session.id,
                user_id=test_user.id,
                exercise_id=ex.id,
                user_answer="answer",
                is_correct=True,
                time_spent_seconds=30
            )
            db_session.add(attempt)
        db_session.commit()

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "complete" in response.json()["detail"].lower()

    def test_get_next_exercise_session_not_found(self, client, auth_headers):
        """Test that 404 is returned for invalid session_id."""
        response = client.get(
            "/api/grammar/practice/99999/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"].lower()

    def test_get_next_exercise_wrong_user(self, client, auth_headers, db_session, test_grammar_exercises):
        """Test that user cannot access another user's session."""
        from app.models.grammar import GrammarSession
        from app.models.user import User

        # Create another user
        other_user = User(
            email="other@example.com",
            hashed_password="hashed",
            full_name="Other User",
            proficiency_level="B1",
            native_language="en"
        )
        db_session.add(other_user)
        db_session.commit()
        db_session.refresh(other_user)

        # Create session for other user
        session = GrammarSession(
            user_id=other_user.id,
            session_type="practice",
            total_exercises=2,
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [test_grammar_exercises[0].id]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Try to access with current user's auth
        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_next_exercise_ended_session(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test that 400 is returned when session is already ended."""
        from app.models.grammar import GrammarSession

        # Create ended session
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=2,
            ended_at=datetime.utcnow(),
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [test_grammar_exercises[0].id]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "ended" in response.json()["detail"].lower()

    def test_get_next_exercise_partial_progress(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test getting correct exercise in middle of session."""
        from app.models.grammar import GrammarSession, GrammarExerciseAttempt

        # Create session with 3 exercises
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=3,
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [ex.id for ex in test_grammar_exercises[:3]]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        # Answer first two exercises
        for ex in test_grammar_exercises[:2]:
            attempt = GrammarExerciseAttempt(
                grammar_session_id=session.id,
                user_id=test_user.id,
                exercise_id=ex.id,
                user_answer="answer",
                is_correct=True,
                time_spent_seconds=30
            )
            db_session.add(attempt)
        db_session.commit()

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == test_grammar_exercises[2].id  # Should be third exercise

    def test_get_next_exercise_response_format(self, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test that response matches GrammarExerciseResponse schema."""
        from app.models.grammar import GrammarSession

        # Create session
        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            total_exercises=1,
            grammar_metadata={
                "target_level": "A2",
                "exercise_ids": [test_grammar_exercises[0].id]
            }
        )
        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        response = client.get(
            f"/api/grammar/practice/{session.id}/next",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Validate all required fields exist
        required_fields = [
            "id", "exercise_type", "difficulty_level", "question_text",
            "correct_answer", "alternative_answers", "explanation_de",
            "hints", "context_category", "topic_id", "created_at"
        ]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"

        # Validate field types
        assert isinstance(data["id"], int)
        assert isinstance(data["exercise_type"], str)
        assert isinstance(data["alternative_answers"], list)
        assert isinstance(data["hints"], list)


class TestGrammarProgressEndpoints:
    """Test grammar progress tracking endpoints."""

    def test_get_progress_summary(self, client, auth_headers, db_session, test_user, test_grammar_topics):
        """Test getting overall progress summary."""
        # Create some progress data
        from app.models.grammar import UserGrammarProgress, GrammarSession

        progress = UserGrammarProgress(
            user_id=test_user.id,
            topic_id=test_grammar_topics[0].id,
            total_attempts=10,
            correct_attempts=8,
            mastery_level="advanced"
        )
        db_session.add(progress)

        session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            target_level="A2",
            total_exercises=10,
            total_attempted=10,
            total_correct=8,
            ended_at=datetime.utcnow()
        )
        db_session.add(session)
        db_session.commit()

        response = client.get(
            "/api/grammar/progress/summary",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "total_exercises_completed" in data
        assert "overall_accuracy" in data
        assert "topics_mastered" in data
        assert "current_streak_days" in data
        assert "level_progress" in data

    def test_get_topic_progress_detail(self, client, auth_headers, db_session, test_user, test_grammar_topics):
        """Test getting detailed progress for a topic."""
        from app.models.grammar import UserGrammarProgress

        progress = UserGrammarProgress(
            user_id=test_user.id,
            topic_id=test_grammar_topics[0].id,
            total_attempts=15,
            correct_attempts=12,
            mastery_level="advanced",
            last_practiced_at=datetime.utcnow()
        )
        db_session.add(progress)
        db_session.commit()

        response = client.get(
            f"/api/grammar/progress/topics/{test_grammar_topics[0].id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["topic"]["id"] == test_grammar_topics[0].id
        assert data["total_attempts"] == 15
        assert data["correct_attempts"] == 12
        assert data["accuracy"] == 80.0
        assert data["mastery_level"] == "advanced"

    def test_get_topic_progress_not_started(self, client, auth_headers, test_grammar_topics):
        """Test getting progress for a topic not yet practiced."""
        response = client.get(
            f"/api/grammar/progress/topics/{test_grammar_topics[0].id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total_attempts"] == 0
        assert data["mastery_level"] == "not_started"

    def test_get_weak_areas(self, client, auth_headers, db_session, test_user, test_grammar_topics):
        """Test getting weak areas with recommendations."""
        from app.models.grammar import UserGrammarProgress

        # Create progress with low accuracy
        progress = UserGrammarProgress(
            user_id=test_user.id,
            topic_id=test_grammar_topics[0].id,
            total_attempts=10,
            correct_attempts=5,  # 50% accuracy
            mastery_level="beginner"
        )
        db_session.add(progress)
        db_session.commit()

        response = client.get(
            "/api/grammar/progress/weak-areas",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "weak_topics" in data
        assert "recommended_practice_plan" in data
        assert "estimated_time_to_improve" in data
        assert len(data["weak_topics"]) >= 1

    def test_get_review_queue(self, client, auth_headers, db_session, test_user, test_grammar_topics):
        """Test getting spaced repetition review queue."""
        from app.models.grammar import UserGrammarProgress

        # Create progress with due review
        progress = UserGrammarProgress(
            user_id=test_user.id,
            topic_id=test_grammar_topics[0].id,
            total_attempts=5,
            correct_attempts=4,
            mastery_level="intermediate",
            next_review_date=datetime.utcnow() - timedelta(days=2)  # Overdue
        )
        db_session.add(progress)
        db_session.commit()

        response = client.get(
            "/api/grammar/progress/review-queue",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "overdue_count" in data
        assert "due_today_count" in data
        assert "upcoming_count" in data
        assert "overdue_items" in data
        assert data["overdue_count"] >= 1


class TestAIGenerationEndpoints:
    """Test AI exercise generation endpoints."""

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_generate_exercises(self, mock_ai_service, client, auth_headers, test_grammar_topics):
        """Test generating exercises with AI."""
        # Mock AI service
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_exercises.return_value = [
            {
                "exercise_type": "fill_blank",
                "difficulty_level": "A2",
                "question_text": "Ich kaufe ____ Buch.",
                "correct_answer": "ein",
                "alternative_answers": [],
                "explanation_de": "Neutrum, Akkusativ.",
                "hints": ["Buch = neutrum"],
                "context_category": "general"
            }
        ]
        mock_ai_service.return_value = mock_ai_instance

        response = client.post(
            "/api/grammar/generate/exercises",
            json={
                "topic_id": test_grammar_topics[0].id,
                "count": 1,
                "exercise_type": "fill_blank",
                "context_category": "general"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "generated_count" in data
        assert "exercises" in data
        assert data["generated_count"] == 1

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_generate_exercises_failure(self, mock_ai_service, client, auth_headers, test_grammar_topics):
        """Test handling AI generation failure."""
        # Mock AI service to return empty
        mock_ai_instance = MagicMock()
        mock_ai_instance.generate_exercises.return_value = []
        mock_ai_service.return_value = mock_ai_instance

        response = client.post(
            "/api/grammar/generate/exercises",
            json={
                "topic_id": test_grammar_topics[0].id,
                "count": 5,
                "exercise_type": "fill_blank"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR

    def test_generate_exercises_topic_not_found(self, client, auth_headers):
        """Test generating exercises for non-existent topic."""
        response = client.post(
            "/api/grammar/generate/exercises",
            json={
                "topic_id": 99999,
                "count": 5,
                "exercise_type": "fill_blank"
            },
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    # ========== SESSION DEDUPLICATION TESTS ==========

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_start_practice_with_active_session_conflict(self, mock_ai, client, auth_headers, db_session, test_grammar_exercises, test_user):
        """Test that starting practice fails when active session exists."""
        # Create an active session
        first_response = client.post(
            "/api/grammar/practice/start",
            headers=auth_headers,
            json={"difficulty_level": "A2", "use_spaced_repetition": False}
        )
        assert first_response.status_code == status.HTTP_201_CREATED
        first_session_id = first_response.json()["session_id"]

        # Try to create second session - should fail with 409
        second_response = client.post(
            "/api/grammar/practice/start",
            headers=auth_headers,
            json={"difficulty_level": "A2", "use_spaced_repetition": False}
        )
        assert second_response.status_code == status.HTTP_409_CONFLICT

        detail = second_response.json()["detail"]
        assert detail["message"] == "Active grammar session already exists"
        assert detail["session_id"] == first_session_id
        assert "started_at" in detail
        assert "age_hours" in detail

        # Verify only 1 session exists in DB
        sessions = db_session.query(GrammarSession).filter(
            GrammarSession.user_id == test_user.id,
            GrammarSession.ended_at.is_(None)
        ).all()
        assert len(sessions) == 1
        assert sessions[0].id == first_session_id

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_cleanup_abandoned_grammar_session(self, mock_ai, client, auth_headers, db_session, test_grammar_exercises, test_user):
        """Test deletion of abandoned grammar session."""
        # Create session
        response = client.post(
            "/api/grammar/practice/start",
            headers=auth_headers,
            json={"difficulty_level": "A2"}
        )
        assert response.status_code == status.HTTP_201_CREATED
        session_id = response.json()["session_id"]

        # Delete session
        delete_response = client.delete(
            f"/api/grammar/practice/{session_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == status.HTTP_204_NO_CONTENT

        # Verify deletion
        session = db_session.query(GrammarSession).filter(GrammarSession.id == session_id).first()
        assert session is None

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_cleanup_completed_session_fails(self, mock_ai, client, auth_headers, db_session, test_grammar_exercises):
        """Test that cleanup of completed session fails."""
        # Create and complete session
        start_response = client.post(
            "/api/grammar/practice/start",
            headers=auth_headers,
            json={"difficulty_level": "A2"}
        )
        session_id = start_response.json()["session_id"]

        # End the session
        client.post(
            f"/api/grammar/practice/{session_id}/end",
            headers=auth_headers
        )

        # Try to delete completed session - should fail
        delete_response = client.delete(
            f"/api/grammar/practice/{session_id}",
            headers=auth_headers
        )
        assert delete_response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Cannot delete completed session" in delete_response.json()["detail"]

    @patch('app.api.v1.grammar.GrammarAIService')
    def test_stale_session_auto_cleanup(self, mock_ai, client, auth_headers, db_session, test_user, test_grammar_exercises):
        """Test that stale sessions (>24h) are auto-cleaned."""
        # Create stale session (25 hours old)
        stale_session = GrammarSession(
            user_id=test_user.id,
            session_type="practice",
            started_at=datetime.utcnow() - timedelta(hours=25),
            total_exercises=10,
            grammar_metadata={"exercise_ids": []}
        )
        db_session.add(stale_session)
        db_session.commit()
        db_session.refresh(stale_session)
        stale_session_id = stale_session.id

        # Start new session - should auto-cleanup stale one
        response = client.post(
            "/api/grammar/practice/start",
            headers=auth_headers,
            json={"difficulty_level": "A2"}
        )
        assert response.status_code == status.HTTP_201_CREATED

        # Verify stale session was deleted
        sessions = db_session.query(GrammarSession).filter(
            GrammarSession.user_id == test_user.id,
            GrammarSession.ended_at.is_(None)
        ).all()
        assert len(sessions) == 1
        assert sessions[0].id != stale_session_id

    def test_cleanup_nonexistent_session(self, client, auth_headers):
        """Test cleanup of non-existent session returns 404."""
        delete_response = client.delete(
            "/api/grammar/practice/99999",
            headers=auth_headers
        )
        assert delete_response.status_code == status.HTTP_404_NOT_FOUND
