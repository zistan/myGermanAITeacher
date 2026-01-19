"""
Tests for vocabulary learning endpoints.
"""
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.models.vocabulary import (
    Vocabulary, UserVocabularyProgress, UserVocabularyList,
    VocabularyListWord, VocabularyReview, FlashcardSession, VocabularyQuiz
)


client = TestClient(app)


# ========== FIXTURES ==========

@pytest.fixture
def mock_db():
    """Mock database session."""
    return Mock()


@pytest.fixture
def test_user():
    """Create a test user."""
    user = User(
        id=1,
        email="test@example.com",
        username="testuser",
        full_name="Test User",
        german_level="B2"
    )
    return user


@pytest.fixture
def test_word():
    """Create a test vocabulary word."""
    word = Vocabulary(
        id=1,
        word="die Arbeit",
        translation_it="il lavoro",
        part_of_speech="noun",
        gender="feminine",
        plural_form="die Arbeiten",
        difficulty="A1",
        category="business",
        example_de="Ich gehe zur Arbeit.",
        example_it="Vado al lavoro.",
        pronunciation="dee AR-bait",
        definition_de="Eine Tätigkeit oder ein Job",
        usage_notes="Common word for work",
        synonyms=["der Job", "die Tätigkeit"],
        antonyms=["die Freizeit"],
        is_idiom=False,
        is_compound=False,
        is_separable_verb=False,
        created_at=datetime.utcnow()
    )
    return word


@pytest.fixture
def mock_auth_headers():
    """Mock authentication headers."""
    return {"Authorization": "Bearer mock_token"}


@pytest.fixture
def mock_get_current_user(test_user):
    """Mock get_current_user dependency."""
    with patch('app.api.v1.vocabulary.get_current_user', return_value=test_user):
        yield


# ========== VOCABULARY WORD ENDPOINT TESTS ==========

def test_get_vocabulary_words_success(mock_db, test_user, test_word, mock_get_current_user):
    """Test getting vocabulary words with filters."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [test_word]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/words?category=business&difficulty=A1",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["word"] == "die Arbeit"
    assert data[0]["category"] == "business"


def test_get_vocabulary_word_with_progress(mock_db, test_user, test_word, mock_get_current_user):
    """Test getting a single word with user's progress."""
    progress = UserVocabularyProgress(
        id=1,
        user_id=test_user.id,
        word_id=test_word.id,
        mastery_level=3,
        times_reviewed=10,
        times_correct=8,
        accuracy_rate=80.0,
        last_reviewed=datetime.utcnow(),
        next_review_due=datetime.utcnow() + timedelta(days=7)
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [test_word, progress]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/words/1",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["word"] == "die Arbeit"
    assert data["mastery_level"] == 3
    assert data["times_reviewed"] == 10
    assert data["accuracy_rate"] == 80.0


def test_get_vocabulary_word_not_found(mock_db, test_user, mock_get_current_user):
    """Test getting a word that doesn't exist."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/words/999",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_create_vocabulary_word_success(mock_db, test_user, mock_get_current_user):
    """Test creating a new vocabulary word."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None  # Word doesn't exist yet

    mock_db.query.return_value = mock_query

    word_data = {
        "word": "der Computer",
        "translation_it": "il computer",
        "part_of_speech": "noun",
        "gender": "masculine",
        "difficulty": "A1",
        "category": "technology",
        "example_de": "Ich arbeite am Computer.",
        "example_it": "Lavoro al computer."
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/words",
            json=word_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_create_vocabulary_word_duplicate(mock_db, test_user, test_word, mock_get_current_user):
    """Test creating a word that already exists."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = test_word  # Word exists

    mock_db.query.return_value = mock_query

    word_data = {
        "word": "die Arbeit",
        "translation_it": "il lavoro",
        "part_of_speech": "noun",
        "gender": "feminine",
        "difficulty": "A1",
        "category": "business",
        "example_de": "Test",
        "example_it": "Test"
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/words",
            json=word_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()


# ========== FLASHCARD ENDPOINT TESTS ==========

@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_start_flashcard_session_success(mock_ai_service, mock_db, test_user, test_word, mock_get_current_user):
    """Test starting a flashcard session."""
    # Mock AI service
    mock_ai = Mock()
    mock_ai.generate_flashcard_content.return_value = {
        "front": "Was bedeutet: die Arbeit",
        "back": "il lavoro",
        "hint": "(noun)"
    }
    mock_ai_service.return_value = mock_ai

    # Mock database
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [test_word]
    mock_query.first.return_value = None  # No progress yet

    mock_db.query.return_value = mock_query

    request_data = {
        "category": "business",
        "card_count": 5,
        "use_spaced_repetition": True
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/flashcards/start",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "session_id" in data
    assert data["total_cards"] >= 1
    assert "current_card" in data


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_start_flashcard_session_no_words(mock_ai_service, mock_db, test_user, mock_get_current_user):
    """Test starting a flashcard session with no matching words."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = []

    mock_db.query.return_value = mock_query

    request_data = {
        "category": "nonexistent",
        "card_count": 5
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/flashcards/start",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 404
    assert "no words found" in response.json()["detail"].lower()


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_start_multiple_flashcard_sessions_unique_ids(mock_ai_service, mock_db, test_user, test_word, mock_get_current_user):
    """Test that starting multiple flashcard sessions creates unique IDs (BUG-015 fix)."""
    # Mock AI service
    mock_ai = Mock()
    mock_ai.generate_flashcard_content.return_value = {
        "front": "Test front",
        "back": "Test back",
        "hint": ""
    }
    mock_ai_service.return_value = mock_ai

    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [test_word]
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_db.query.return_value = mock_query

    request_data = {
        "card_count": 1,
        "use_spaced_repetition": False
    }

    # Mock FlashcardSession database inserts
    mock_session_1 = Mock(id=1)
    mock_session_2 = Mock(id=2)

    # Start first session
    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response1 = client.post(
            "/api/v1/vocabulary/flashcards/start",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response1.status_code == 200
    session_id_1 = response1.json()["session_id"]

    # Start second session
    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response2 = client.post(
            "/api/v1/vocabulary/flashcards/start",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response2.status_code == 200
    session_id_2 = response2.json()["session_id"]

    # Verify IDs are unique and sequential
    assert session_id_1 == 1
    assert session_id_2 == 2
    assert session_id_1 != session_id_2


def test_submit_flashcard_answer_correct(mock_db, test_user, mock_get_current_user):
    """Test submitting a correct flashcard answer."""
    import json

    # Mock FlashcardSession from database
    cards_data = [{
        "card_id": "abc123",
        "word_id": 1,
        "word": "die Arbeit",
        "card_type": "translation",
        "front": "Translate: die Arbeit",
        "back": "il lavoro",
        "hint": "",
        "difficulty": "A1"
    }]

    mock_session = FlashcardSession(
        id=1,
        user_id=test_user.id,
        total_cards=1,
        current_index=0,
        cards_data=json.dumps(cards_data),
        use_spaced_repetition=0
    )

    # Mock progress
    progress = UserVocabularyProgress(
        id=1,
        user_id=test_user.id,
        word_id=1,
        mastery_level=2,
        times_reviewed=5,
        times_correct=4,
        accuracy_rate=80.0
    )

    # Mock database queries
    def mock_query_side_effect(model):
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        if model == FlashcardSession:
            mock_query.first.return_value = mock_session
        else:  # UserVocabularyProgress
            mock_query.first.return_value = progress
        return mock_query

    mock_db.query.side_effect = mock_query_side_effect

    answer_data = {
        "card_id": "abc123",
        "user_answer": "il lavoro",
        "confidence_level": 4,
        "time_spent_seconds": 10
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/flashcards/1/answer",
            json=answer_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert "richtig" in data["feedback"].lower() or "perfekt" in data["feedback"].lower()
    assert data["next_review_interval_days"] > 0


def test_submit_flashcard_answer_incorrect(mock_db, test_user, mock_get_current_user):
    """Test submitting an incorrect flashcard answer."""
    import json

    # Mock FlashcardSession from database
    cards_data = [{
        "card_id": "abc123",
        "word_id": 1,
        "word": "die Arbeit",
        "card_type": "translation",
        "front": "Translate: die Arbeit",
        "back": "il lavoro",
        "hint": "",
        "difficulty": "A1"
    }]

    mock_session = FlashcardSession(
        id=1,
        user_id=test_user.id,
        total_cards=1,
        current_index=0,
        cards_data=json.dumps(cards_data),
        use_spaced_repetition=0
    )

    progress = UserVocabularyProgress(
        id=1,
        user_id=test_user.id,
        word_id=1,
        mastery_level=3,
        times_reviewed=10,
        times_correct=8
    )

    # Mock database queries
    def mock_query_side_effect(model):
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        if model == FlashcardSession:
            mock_query.first.return_value = mock_session
        else:  # UserVocabularyProgress
            mock_query.first.return_value = progress
        return mock_query

    mock_db.query.side_effect = mock_query_side_effect

    answer_data = {
        "card_id": "abc123",
        "user_answer": "wrong answer",
        "confidence_level": 2,
        "time_spent_seconds": 15
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/flashcards/1/answer",
            json=answer_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["correct_answer"] == "il lavoro"
    assert data["next_review_interval_days"] == 1  # Reset to 1 day


def test_submit_flashcard_answer_session_not_found(mock_db, test_user, mock_get_current_user):
    """Test submitting answer to non-existent session."""
    answer_data = {
        "card_id": "abc123",
        "user_answer": "test",
        "confidence_level": 3
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/flashcards/999/answer",
            json=answer_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 404


# ========== PERSONAL VOCABULARY LIST TESTS ==========

def test_create_vocabulary_list_success(mock_db, test_user, mock_get_current_user):
    """Test creating a personal vocabulary list."""
    list_data = {
        "name": "Business Vocabulary",
        "description": "Words for business contexts",
        "is_public": False
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/lists",
            json=list_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Business Vocabulary"
    assert data["word_count"] == 0
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_get_vocabulary_lists(mock_db, test_user, mock_get_current_user):
    """Test getting all personal vocabulary lists."""
    vocab_list = UserVocabularyList(
        id=1,
        user_id=test_user.id,
        name="My List",
        description="Test list",
        is_public=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [vocab_list]
    mock_query.count.return_value = 5

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/lists",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "My List"


def test_add_word_to_list_success(mock_db, test_user, test_word, mock_get_current_user):
    """Test adding a word to a personal list."""
    vocab_list = UserVocabularyList(
        id=1,
        user_id=test_user.id,
        name="My List"
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [vocab_list, test_word, None]  # List exists, word exists, not already added

    mock_db.query.return_value = mock_query

    request_data = {
        "word_id": 1,
        "notes": "Important word"
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/lists/1/words",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    assert "added" in response.json()["message"].lower()
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()


def test_add_word_to_list_already_exists(mock_db, test_user, test_word, mock_get_current_user):
    """Test adding a word that's already in the list."""
    vocab_list = UserVocabularyList(
        id=1,
        user_id=test_user.id,
        name="My List"
    )

    existing_list_word = VocabularyListWord(
        list_id=1,
        word_id=1
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [vocab_list, test_word, existing_list_word]

    mock_db.query.return_value = mock_query

    request_data = {
        "word_id": 1
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/lists/1/words",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 400
    assert "already in list" in response.json()["detail"].lower()


def test_remove_word_from_list_success(mock_db, test_user, mock_get_current_user):
    """Test removing a word from a list."""
    vocab_list = UserVocabularyList(
        id=1,
        user_id=test_user.id,
        name="My List"
    )

    list_word = VocabularyListWord(
        list_id=1,
        word_id=1
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.side_effect = [vocab_list, list_word]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.delete(
            "/api/v1/vocabulary/lists/1/words/1",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    assert "removed" in response.json()["message"].lower()
    mock_db.delete.assert_called_once()
    mock_db.commit.assert_called_once()


def test_delete_vocabulary_list_success(mock_db, test_user, mock_get_current_user):
    """Test deleting a vocabulary list."""
    vocab_list = UserVocabularyList(
        id=1,
        user_id=test_user.id,
        name="My List"
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = vocab_list

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.delete(
            "/api/v1/vocabulary/lists/1",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    assert "deleted" in response.json()["message"].lower()
    mock_db.delete.assert_called_once()


# ========== VOCABULARY QUIZ TESTS ==========

@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_generate_vocabulary_quiz_success(mock_ai_service, mock_db, test_user, test_word, mock_get_current_user):
    """Test generating a vocabulary quiz."""
    # Mock AI service
    mock_ai = Mock()
    mock_ai.generate_vocabulary_quiz.return_value = [
        {
            "question": "Was bedeutet 'die Arbeit'?",
            "correct_answer": "il lavoro",
            "options": ["il lavoro", "la casa", "il tempo", "la scuola"],
            "explanation": "Die Arbeit means work in Italian",
            "word_tested": "die Arbeit"
        }
    ]
    mock_ai_service.return_value = mock_ai

    # Mock database
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [test_word]

    mock_db.query.return_value = mock_query

    request_data = {
        "category": "business",
        "quiz_type": "multiple_choice",
        "question_count": 5
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/quiz/generate",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "quiz_id" in data
    assert len(data["questions"]) >= 1
    assert data["total_questions"] >= 1


def test_submit_quiz_answer_correct(mock_db, test_user, mock_get_current_user):
    """Test submitting a correct quiz answer."""
    import json

    # Mock VocabularyQuiz from database
    questions_data = [{
        "question": "Was bedeutet 'die Arbeit'?",
        "correct_answer": "il lavoro",
        "explanation": "Test explanation"
    }]

    mock_quiz = VocabularyQuiz(
        id=1,
        user_id=test_user.id,
        quiz_type="multiple_choice",
        total_questions=1,
        questions_data=json.dumps(questions_data)
    )

    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = mock_quiz
    mock_db.query.return_value = mock_query

    answer_data = {
        "question_id": "1_0",
        "user_answer": "il lavoro"
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/quiz/1/answer",
            json=answer_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is True
    assert data["points_earned"] == 10


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_generate_multiple_quizzes_unique_ids(mock_ai_service, mock_db, test_user, test_word, mock_get_current_user):
    """Test that generating multiple quizzes creates unique IDs (BUG-016 fix)."""
    # Mock AI service
    mock_ai = Mock()
    mock_ai.generate_vocabulary_quiz.return_value = [
        {
            "question": "Test question",
            "correct_answer": "answer",
            "options": ["a", "b", "c", "d"],
            "explanation": "explanation",
            "word_tested": "word"
        }
    ]
    mock_ai_service.return_value = mock_ai

    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.limit.return_value.all.return_value = [test_word]
    mock_db.query.return_value = mock_query

    quiz_data = {
        "word_ids": [1],
        "quiz_type": "multiple_choice",
        "question_count": 1,
        "difficulty": "B2"
    }

    # Generate first quiz
    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response1 = client.post(
            "/api/v1/vocabulary/quiz/generate",
            json=quiz_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response1.status_code == 200
    quiz_id_1 = response1.json()["quiz_id"]

    # Generate second quiz
    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response2 = client.post(
            "/api/v1/vocabulary/quiz/generate",
            json=quiz_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response2.status_code == 200
    quiz_id_2 = response2.json()["quiz_id"]

    # Verify IDs are unique and sequential
    assert quiz_id_1 == 1
    assert quiz_id_2 == 2
    assert quiz_id_1 != quiz_id_2


@patch('app.api.v1.vocabulary.vocabulary_quizzes', {1: {
    "user_id": 1,
    "questions": [{
        "question": "Was bedeutet 'die Arbeit'?",
        "correct_answer": "il lavoro",
        "explanation": "Test explanation"
    }]
}})
def test_submit_quiz_answer_incorrect(mock_db, test_user, mock_get_current_user):
    """Test submitting an incorrect quiz answer."""
    answer_data = {
        "question_id": "1_0",
        "user_answer": "wrong answer"
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/quiz/1/answer",
            json=answer_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["is_correct"] is False
    assert data["points_earned"] == 0
    assert data["correct_answer"] == "il lavoro"


# ========== VOCABULARY PROGRESS TESTS ==========

def test_get_vocabulary_progress_summary(mock_db, test_user, test_word, mock_get_current_user):
    """Test getting vocabulary progress summary."""
    progress1 = UserVocabularyProgress(
        user_id=test_user.id,
        word_id=1,
        mastery_level=3,
        times_reviewed=10,
        next_review_due=datetime.utcnow() - timedelta(days=1)
    )

    progress2 = UserVocabularyProgress(
        user_id=test_user.id,
        word_id=2,
        mastery_level=5,
        times_reviewed=20,
        next_review_due=datetime.utcnow() + timedelta(days=5)
    )

    word1 = Vocabulary(id=1, difficulty="A1", category="business", word="test1")
    word2 = Vocabulary(id=2, difficulty="B2", category="daily", word="test2")

    review1 = VocabularyReview(
        user_id=test_user.id,
        word_id=1,
        time_spent_seconds=120,
        reviewed_at=datetime.utcnow()
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.side_effect = [[progress1, progress2], [review1]]
    mock_query.first.side_effect = [word1, word2, word1, word2]
    mock_query.scalar.return_value = 300
    mock_query.count.side_effect = [1, 2]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/progress/summary",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["total_words_learned"] == 2
    assert "words_by_level" in data
    assert "words_by_category" in data
    assert "mastery_breakdown" in data


def test_get_vocabulary_review_queue(mock_db, test_user, test_word, mock_get_current_user):
    """Test getting review queue with spaced repetition."""
    overdue_progress = UserVocabularyProgress(
        user_id=test_user.id,
        word_id=1,
        mastery_level=2,
        times_reviewed=5,
        next_review_due=datetime.utcnow() - timedelta(days=2)
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.side_effect = [[overdue_progress], [], []]
    mock_query.limit.return_value = mock_query
    mock_query.first.return_value = test_word

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/vocabulary/progress/review-queue",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "overdue_count" in data
    assert "due_today_count" in data
    assert "upcoming_count" in data
    assert "overdue_words" in data


# ========== AI-POWERED ANALYSIS TESTS ==========

@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_analyze_word_success(mock_ai_service, test_user, mock_get_current_user):
    """Test analyzing a word with AI."""
    mock_ai = Mock()
    mock_ai.analyze_word.return_value = {
        "word": "die Arbeit",
        "translation_it": "il lavoro",
        "part_of_speech": "noun",
        "gender": "feminine",
        "difficulty_level": "A1",
        "pronunciation": "dee AR-bait",
        "definition_de": "Eine Tätigkeit",
        "synonyms": ["der Job"],
        "antonyms": ["die Freizeit"],
        "examples": [{"de": "Ich gehe zur Arbeit.", "it": "Vado al lavoro."}],
        "collocations": ["zur Arbeit gehen"],
        "is_compound": False,
        "is_separable": False,
        "register": "neutral",
        "frequency": "very_common"
    }
    mock_ai_service.return_value = mock_ai

    request_data = {
        "word": "die Arbeit",
        "include_examples": True,
        "include_synonyms": True
    }

    response = client.post(
        "/api/v1/vocabulary/analyze",
        json=request_data,
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["word"] == "die Arbeit"
    assert data["translation_it"] == "il lavoro"
    assert data["part_of_speech"] == "noun"


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_analyze_word_with_missing_fields(mock_ai_service, test_user, mock_get_current_user):
    """Test analyzing a word when AI returns incomplete data."""
    mock_ai = Mock()
    # Return minimal analysis with missing optional fields
    mock_ai.analyze_word.return_value = {
        "word": "Zahlung",
        "translation_it": "pagamento",
        "part_of_speech": "noun"
        # Missing: pronunciation, definition_de, synonyms, etc.
    }
    mock_ai_service.return_value = mock_ai

    request_data = {
        "word": "Zahlung",
        "include_examples": True
    }

    response = client.post(
        "/api/v1/vocabulary/analyze",
        json=request_data,
        headers={"Authorization": "Bearer test_token"}
    )

    # Should succeed with defaults for missing fields
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == "Zahlung"
    assert data["translation_it"] == "pagamento"
    assert data["part_of_speech"] == "noun"
    assert data["pronunciation"] == ""  # Default
    assert data["synonyms"] == []  # Default
    assert data["antonyms"] == []  # Default
    assert data["examples"] == []  # Default
    assert data["is_compound"] == False  # Default
    assert data["is_separable"] == False  # Default
    assert data["register"] == "neutral"  # Default
    assert data["frequency"] == "common"  # Default


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_analyze_word_ai_error(mock_ai_service, test_user, mock_get_current_user):
    """Test analyzing a word when AI service returns an error."""
    mock_ai = Mock()
    # Simulate AI service returning error response
    mock_ai.analyze_word.return_value = {
        "word": "TestWort",
        "error": "API error: Rate limit exceeded",
        "translation_it": "Errore API",
        "part_of_speech": "unknown",
        "difficulty_level": "B2",
        "pronunciation": "",
        "definition_de": "Analyse aufgrund eines API-Fehlers fehlgeschlagen",
        "synonyms": [],
        "antonyms": [],
        "examples": [],
        "collocations": [],
        "is_compound": False,
        "is_separable": False,
        "register": "neutral",
        "frequency": "common"
    }
    mock_ai_service.return_value = mock_ai

    request_data = {
        "word": "TestWort",
        "include_examples": True
    }

    response = client.post(
        "/api/v1/vocabulary/analyze",
        json=request_data,
        headers={"Authorization": "Bearer test_token"}
    )

    # Should return 500 error when AI service indicates failure
    assert response.status_code == 500
    assert "Word analysis failed" in response.json()["detail"]


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_analyze_word_exception_handling(mock_ai_service, test_user, mock_get_current_user):
    """Test analyzing a word when AI service throws an exception."""
    mock_ai = Mock()
    # Simulate exception being raised
    mock_ai.analyze_word.side_effect = Exception("Unexpected error occurred")
    mock_ai_service.return_value = mock_ai

    request_data = {
        "word": "TestWort",
        "include_examples": True
    }

    response = client.post(
        "/api/v1/vocabulary/analyze",
        json=request_data,
        headers={"Authorization": "Bearer test_token"}
    )

    # Should return 500 error with proper error message
    assert response.status_code == 500
    assert "Error analyzing word" in response.json()["detail"]


@patch('app.api.v1.vocabulary.VocabularyAIService')
def test_detect_vocabulary_from_text(mock_ai_service, test_user, mock_get_current_user):
    """Test detecting vocabulary from German text."""
    mock_ai = Mock()
    mock_ai.detect_vocabulary_from_text.return_value = [
        {
            "word": "die Arbeit",
            "lemma": "Arbeit",
            "translation_it": "il lavoro",
            "part_of_speech": "noun",
            "difficulty": "A1",
            "context_in_text": "Ich gehe zur Arbeit.",
            "why_important": "Common everyday word"
        }
    ]
    mock_ai_service.return_value = mock_ai

    request_data = {
        "text": "Ich gehe jeden Tag zur Arbeit und arbeite am Computer.",
        "min_difficulty": "A1",
        "max_words": 10
    }

    response = client.post(
        "/api/v1/vocabulary/detect",
        json=request_data,
        headers={"Authorization": "Bearer test_token"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "detected_words" in data
    assert data["total_detected"] >= 1


def test_get_word_recommendations(mock_db, test_user, test_word, mock_get_current_user):
    """Test getting personalized word recommendations."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.side_effect = [[], [test_word]]

    mock_db.query.return_value = mock_query

    request_data = {
        "category": "business",
        "difficulty": "A1",
        "count": 10,
        "recommendation_type": "next_to_learn"
    }

    with patch('app.api.v1.vocabulary.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/vocabulary/recommend",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert "recommended_words" in data
    assert "reason" in data
