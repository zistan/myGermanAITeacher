"""
Tests for database models.
"""
import pytest
from datetime import datetime

from app.models.user import User
from app.models.vocabulary import Vocabulary, UserVocabulary
from app.models.context import Context
from app.models.session import Session, ConversationTurn
from app.models.grammar import GrammarTopic, GrammarExercise, UserGrammarProgress
from app.models.progress import ProgressSnapshot, GrammarCorrection


class TestUserModel:
    """Test User model."""

    def test_create_user(self, db_session):
        """Test creating a user."""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            native_language="it",
            target_language="de",
            proficiency_level="B2"
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.created_at is not None
        assert user.settings == {}

    def test_user_unique_constraints(self, db_session):
        """Test that username and email must be unique."""
        user1 = User(
            username="user1",
            email="user1@example.com",
            password_hash="hash1"
        )
        db_session.add(user1)
        db_session.commit()

        # Try to create user with same username
        user2 = User(
            username="user1",  # Duplicate
            email="different@example.com",
            password_hash="hash2"
        )
        db_session.add(user2)

        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestVocabularyModel:
    """Test Vocabulary models."""

    def test_create_vocabulary(self, db_session):
        """Test creating a vocabulary item."""
        vocab = Vocabulary(
            word_de="das Haus",
            word_it="la casa",
            word_en="the house",
            part_of_speech="noun",
            gender="das",
            difficulty_level="A1",
            context_category="daily"
        )

        db_session.add(vocab)
        db_session.commit()
        db_session.refresh(vocab)

        assert vocab.id is not None
        assert vocab.word_de == "das Haus"
        assert vocab.gender == "das"

    def test_user_vocabulary_progress(self, db_session, test_user):
        """Test tracking user vocabulary progress."""
        vocab = Vocabulary(
            word_de="die Zahlung",
            word_it="il pagamento",
            context_category="business"
        )
        db_session.add(vocab)
        db_session.commit()

        user_vocab = UserVocabulary(
            user_id=test_user.id,
            vocabulary_id=vocab.id,
            familiarity_score=0.7,
            times_encountered=5,
            times_correct=4,
            times_incorrect=1
        )
        db_session.add(user_vocab)
        db_session.commit()
        db_session.refresh(user_vocab)

        assert user_vocab.id is not None
        assert user_vocab.familiarity_score == 0.7
        assert user_vocab.times_correct == 4


class TestContextModel:
    """Test Context model."""

    def test_create_context(self, db_session):
        """Test creating a conversation context."""
        context = Context(
            name="Banking Meeting",
            category="business",
            difficulty_level="C1",
            description="Discussion about payment solutions",
            system_prompt="You are a banking executive...",
            suggested_vocab=[1, 2, 3],
            is_active=True
        )

        db_session.add(context)
        db_session.commit()
        db_session.refresh(context)

        assert context.id is not None
        assert context.name == "Banking Meeting"
        assert context.category == "business"
        assert context.suggested_vocab == [1, 2, 3]


class TestSessionModels:
    """Test Session and ConversationTurn models."""

    def test_create_session(self, db_session, test_user):
        """Test creating a practice session."""
        session = Session(
            user_id=test_user.id,
            session_type="conversation",
            total_turns=5,
            grammar_errors=2,
            overall_score=0.85
        )

        db_session.add(session)
        db_session.commit()
        db_session.refresh(session)

        assert session.id is not None
        assert session.user_id == test_user.id
        assert session.total_turns == 5

    def test_create_conversation_turn(self, db_session, test_user):
        """Test creating a conversation turn."""
        session = Session(user_id=test_user.id, session_type="conversation")
        db_session.add(session)
        db_session.commit()

        turn = ConversationTurn(
            session_id=session.id,
            turn_number=1,
            speaker="user",
            message_text="Ich möchte über Zahlungen sprechen.",
            grammar_feedback=[{"error": "none"}],
            vocabulary_used=[1, 2]
        )

        db_session.add(turn)
        db_session.commit()
        db_session.refresh(turn)

        assert turn.id is not None
        assert turn.session_id == session.id
        assert turn.speaker == "user"


class TestGrammarModels:
    """Test Grammar-related models."""

    def test_create_grammar_topic(self, db_session):
        """Test creating a grammar topic."""
        topic = GrammarTopic(
            name_de="Dativ mit Präpositionen",
            name_en="Dative with Prepositions",
            category="cases",
            subcategory="dative",
            difficulty_level="B1",
            explanation_de="Bestimmte Präpositionen verlangen immer den Dativ..."
        )

        db_session.add(topic)
        db_session.commit()
        db_session.refresh(topic)

        assert topic.id is not None
        assert topic.category == "cases"

    def test_create_grammar_exercise(self, db_session):
        """Test creating a grammar exercise."""
        topic = GrammarTopic(
            name_de="Akkusativ",
            category="cases",
            difficulty_level="A2"
        )
        db_session.add(topic)
        db_session.commit()

        exercise = GrammarExercise(
            topic_id=topic.id,
            exercise_type="fill_blank",
            difficulty_level="A2",
            question_text="Ich sehe ___ Mann.",
            question_data={"blank_position": 2},
            correct_answer="den",
            explanation_de="Das Verb 'sehen' verlangt den Akkusativ."
        )

        db_session.add(exercise)
        db_session.commit()
        db_session.refresh(exercise)

        assert exercise.id is not None
        assert exercise.exercise_type == "fill_blank"
        assert exercise.topic_id == topic.id

    def test_user_grammar_progress(self, db_session, test_user):
        """Test tracking user grammar progress."""
        topic = GrammarTopic(name_de="Perfekt", category="verbs")
        db_session.add(topic)
        db_session.commit()

        progress = UserGrammarProgress(
            user_id=test_user.id,
            topic_id=topic.id,
            mastery_level=0.75,
            total_exercises_attempted=20,
            total_exercises_correct=15,
            total_exercises_incorrect=5
        )

        db_session.add(progress)
        db_session.commit()
        db_session.refresh(progress)

        assert progress.id is not None
        assert progress.mastery_level == 0.75
        assert progress.total_exercises_attempted == 20


class TestProgressModels:
    """Test Progress tracking models."""

    def test_create_progress_snapshot(self, db_session, test_user):
        """Test creating a progress snapshot."""
        snapshot = ProgressSnapshot(
            user_id=test_user.id,
            total_sessions=10,
            total_practice_minutes=300,
            vocabulary_learned=50,
            grammar_topics_mastered=5,
            avg_grammar_accuracy=0.82
        )

        db_session.add(snapshot)
        db_session.commit()
        db_session.refresh(snapshot)

        assert snapshot.id is not None
        assert snapshot.total_sessions == 10
        assert snapshot.vocabulary_learned == 50

    def test_create_grammar_correction(self, db_session, test_user):
        """Test creating a grammar correction."""
        session = Session(user_id=test_user.id, session_type="conversation")
        db_session.add(session)
        db_session.commit()

        turn = ConversationTurn(
            session_id=session.id,
            turn_number=1,
            speaker="user",
            message_text="Test"
        )
        db_session.add(turn)
        db_session.commit()

        correction = GrammarCorrection(
            turn_id=turn.id,
            user_id=test_user.id,
            error_type="case",
            incorrect_text="der Mann",
            corrected_text="den Mann",
            explanation="Akkusativ erforderlich",
            severity="moderate"
        )

        db_session.add(correction)
        db_session.commit()
        db_session.refresh(correction)

        assert correction.id is not None
        assert correction.error_type == "case"
        assert correction.severity == "moderate"
