"""
Tests for integration endpoints and cross-module workflows.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.models.session import ConversationSession
from app.models.context import Context
from app.models.grammar import GrammarTopic, UserGrammarProgress
from app.models.vocabulary import VocabularyWord, UserVocabularyProgress


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
        proficiency_level="B2"
    )
    return user


@pytest.fixture
def test_context():
    """Create a test context."""
    context = Context(
        id=1,
        name="Banking Meeting - Payment Solutions",
        category="business",
        difficulty_level="C1",
        description="Discussion about payment processing",
        system_prompt="You are a banking executive...",
        is_active=True
    )
    return test_context


@pytest.fixture
def test_conversation_session(test_context):
    """Create a test conversation session."""
    session = ConversationSession(
        id=1,
        user_id=1,
        context_id=1,
        started_at=datetime.utcnow() - timedelta(minutes=30),
        ended_at=datetime.utcnow(),
        grammar_topics_detected=["Akkusativ", "Präsens"],
        vocabulary_words_detected=["die Zahlung", "der Vertrag"]
    )
    return session


@pytest.fixture
def mock_get_current_user(test_user):
    """Mock get_current_user dependency."""
    with patch('app.api.v1.integration.get_current_user', return_value=test_user):
        yield


# ========== SESSION ANALYSIS TESTS ==========

@patch('app.api.v1.integration.IntegrationService')
def test_analyze_conversation_session_success(mock_integration_service, mock_db, test_user, test_context, mock_get_current_user):
    """Test analyzing a conversation session."""
    # Mock integration service
    mock_integration = Mock()
    mock_integration.analyze_conversation_session.return_value = {
        "session_id": 1,
        "started_at": datetime.utcnow() - timedelta(minutes=30),
        "ended_at": datetime.utcnow(),
        "duration_minutes": 30.0,
        "context": {
            "id": 1,
            "name": "Banking Meeting - Payment Solutions",
            "category": "business",
            "difficulty_level": "C1"
        },
        "message_count": 15,
        "grammar_topics_detected": ["Akkusativ", "Präsens"],
        "vocabulary_words_detected": ["die Zahlung", "der Vertrag"],
        "recommendations": {
            "grammar": [
                {
                    "topic_id": 1,
                    "topic_name": "Akkusativ",
                    "category": "cases",
                    "current_mastery": 2.5,
                    "priority": "high",
                    "reason": "Detected in conversation - current mastery: 2.5/5.0"
                }
            ],
            "vocabulary": [
                {
                    "word": "die Zahlung",
                    "status": "not_learned",
                    "priority": "high",
                    "reason": "Used in conversation but not yet in your vocabulary"
                }
            ],
            "next_steps": [
                "Practice grammar: Akkusativ",
                "Learn 2 new words from this conversation"
            ]
        }
    }
    mock_integration_service.return_value = mock_integration

    with patch('app.api.v1.integration.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/integration/session-analysis/1",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == 1
    assert data["duration_minutes"] == 30.0
    assert len(data["grammar_topics_detected"]) == 2
    assert len(data["recommendations"]["grammar"]) == 1
    assert len(data["recommendations"]["next_steps"]) == 2


@patch('app.api.v1.integration.IntegrationService')
def test_analyze_conversation_session_not_found(mock_integration_service, mock_db, test_user, mock_get_current_user):
    """Test analyzing a non-existent session."""
    mock_integration = Mock()
    mock_integration.analyze_conversation_session.return_value = {
        "error": "Session not found"
    }
    mock_integration_service.return_value = mock_integration

    with patch('app.api.v1.integration.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/integration/session-analysis/999",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 404


# ========== LEARNING PATH TESTS ==========

@patch('app.api.v1.integration.IntegrationService')
def test_get_personalized_learning_path(mock_integration_service, mock_db, test_user, mock_get_current_user):
    """Test getting personalized learning path."""
    mock_integration = Mock()
    mock_integration.get_personalized_learning_path.return_value = {
        "user_id": 1,
        "generated_at": datetime.utcnow(),
        "focus_areas": [
            {
                "module": "grammar",
                "area": "Akkusativ",
                "priority": "high",
                "reason": "Low mastery (2.5/5.0)"
            },
            {
                "module": "vocabulary",
                "area": "Build vocabulary foundation",
                "priority": "high",
                "reason": "Fewer than 100 words learned"
            }
        ],
        "daily_plan": {
            "total_duration_minutes": 75,
            "activities": [
                {
                    "time_of_day": "morning",
                    "activity": "vocabulary_review",
                    "duration_minutes": 15,
                    "description": "Review vocabulary flashcards",
                    "priority": "high"
                },
                {
                    "time_of_day": "midday",
                    "activity": "grammar_practice",
                    "topic": "Akkusativ",
                    "duration_minutes": 30,
                    "description": "Practice Akkusativ",
                    "priority": "high"
                },
                {
                    "time_of_day": "evening",
                    "activity": "conversation",
                    "duration_minutes": 30,
                    "description": "Conversation practice in varied contexts",
                    "priority": "medium"
                }
            ]
        },
        "weekly_plan": {
            "goal_sessions": 5,
            "focus_distribution": {
                "conversation": 2,
                "grammar": 2,
                "vocabulary": 1
            },
            "milestones": [
                "Complete 5+ total sessions",
                "Practice all identified weak areas"
            ]
        },
        "recommended_contexts": [
            {
                "context_id": 1,
                "name": "Banking Meeting",
                "category": "business",
                "difficulty_level": "C1",
                "times_practiced": 0,
                "priority": "high",
                "reason": "Not yet practiced"
            }
        ],
        "motivation_message": "Sehr gut! You're on the right track!"
    }
    mock_integration_service.return_value = mock_integration

    with patch('app.api.v1.integration.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/integration/learning-path",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["focus_areas"]) == 2
    assert data["daily_plan"]["total_duration_minutes"] == 75
    assert len(data["daily_plan"]["activities"]) == 3
    assert data["weekly_plan"]["goal_sessions"] == 5
    assert len(data["recommended_contexts"]) == 1


# ========== DASHBOARD TESTS ==========

@patch('app.api.v1.integration.IntegrationService')
def test_get_dashboard_data(mock_integration_service, mock_db, test_user, mock_get_current_user):
    """Test getting comprehensive dashboard data."""
    mock_integration = Mock()
    mock_integration.get_dashboard_data.return_value = {
        "user_id": 1,
        "last_updated": datetime.utcnow(),
        "overall_progress": {
            "user_id": 1,
            "overall_score": 75,
            "conversation": {
                "total_sessions": 15,
                "total_messages": 150
            },
            "grammar": {
                "topics_practiced": 10,
                "topics_mastered": 5
            },
            "vocabulary": {
                "total_words_learned": 100,
                "words_mastered": 20
            },
            "activity": {
                "current_streak_days": 5,
                "longest_streak_days": 10
            },
            "weekly_goal_progress": {
                "sessions_this_week": 4,
                "goal_sessions": 5,
                "goal_met": False
            }
        },
        "learning_path": {
            "focus_areas": [],
            "daily_plan": {"total_duration_minutes": 75, "activities": []},
            "weekly_plan": {"goal_sessions": 5},
            "recommended_contexts": []
        },
        "due_items": {
            "grammar_topics": [
                {
                    "topic_id": 1,
                    "topic_name": "Akkusativ",
                    "mastery_level": 2.5,
                    "days_overdue": 2
                }
            ],
            "vocabulary_words": [
                {
                    "word_id": 1,
                    "word": "die Zahlung",
                    "translation_it": "il pagamento",
                    "mastery_level": 3,
                    "days_overdue": 1
                }
            ],
            "total_due": 2
        },
        "recent_activity": [
            {
                "type": "conversation",
                "timestamp": datetime.utcnow(),
                "description": "Conversation: Banking Meeting",
                "details": {"session_id": 1}
            },
            {
                "type": "grammar",
                "timestamp": datetime.utcnow() - timedelta(hours=2),
                "description": "Grammar practice: Akkusativ",
                "details": {"session_id": 1, "exercises_completed": 10}
            }
        ],
        "close_achievements": [
            {
                "achievement_name": "Week Warrior",
                "progress_percent": 71,
                "current_value": 5,
                "target_value": 7,
                "tier": "bronze",
                "points": 50
            }
        ],
        "quick_actions": [
            {
                "action": "review_due_items",
                "label": "Review 2 due items",
                "priority": "high",
                "icon": "clock"
            },
            {
                "action": "start_conversation",
                "label": "Practice: Banking Meeting",
                "priority": "medium",
                "icon": "chat",
                "context_id": 1
            }
        ]
    }
    mock_integration_service.return_value = mock_integration

    with patch('app.api.v1.integration.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/integration/dashboard",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert "overall_progress" in data
    assert "learning_path" in data
    assert "due_items" in data
    assert "recent_activity" in data
    assert "close_achievements" in data
    assert "quick_actions" in data
    assert data["due_items"]["total_due"] == 2
    assert len(data["recent_activity"]) == 2
    assert len(data["quick_actions"]) == 2


# ========== INTEGRATION SERVICE UNIT TESTS ==========

def test_integration_service_analyze_conversation_session(mock_db, test_user, test_conversation_session, test_context):
    """Test IntegrationService analyze_conversation_session method."""
    from app.services.integration_service import IntegrationService
    from app.models.session import Message

    # Mock database queries
    mock_session_query = Mock()
    mock_session_query.filter.return_value = mock_session_query
    mock_session_query.first.return_value = test_conversation_session

    mock_message_query = Mock()
    mock_message_query.filter.return_value = mock_message_query
    mock_message_query.order_by.return_value = mock_message_query
    mock_message_query.all.return_value = [
        Message(id=1, session_id=1, role="user", content="Hallo"),
        Message(id=2, session_id=1, role="assistant", content="Guten Tag"),
        Message(id=3, session_id=1, role="user", content="Wie geht's?")
    ]

    mock_context_query = Mock()
    mock_context_query.filter.return_value = mock_context_query
    mock_context_query.first.return_value = test_context

    # Set up query returns
    def query_side_effect(model):
        if model == ConversationSession:
            return mock_session_query
        elif model == Message:
            return mock_message_query
        elif model == Context:
            return mock_context_query
        else:
            mock = Mock()
            mock.filter.return_value = mock
            mock.first.return_value = None
            mock.all.return_value = []
            return mock

    mock_db.query.side_effect = query_side_effect

    service = IntegrationService(mock_db)
    result = service.analyze_conversation_session(1, test_user.id)

    assert result["session_id"] == 1
    assert result["context"]["name"] == "Banking Meeting - Payment Solutions"
    assert result["message_count"] == 2  # Only user messages
    assert "recommendations" in result


def test_integration_service_personalized_learning_path(mock_db, test_user):
    """Test IntegrationService get_personalized_learning_path method."""
    from app.services.integration_service import IntegrationService

    # Mock analytics service
    with patch('app.services.integration_service.AnalyticsService') as mock_analytics_class:
        mock_analytics = Mock()
        mock_analytics.get_overall_progress.return_value = {
            "conversation": {"total_sessions": 5, "unique_contexts_practiced": 2},
            "grammar": {"weak_areas": [{"topic_id": 1, "topic_name": "Akkusativ", "mastery": 2.0}],
                       "topics_practiced": 5, "overall_accuracy_percentage": 70},
            "vocabulary": {"total_words_learned": 50, "words_mastered": 10},
            "activity": {"current_streak_days": 3, "longest_streak_days": 5},
            "weekly_goal_progress": {"sessions_this_week": 3, "goal_sessions": 5},
            "overall_score": 60
        }
        mock_analytics.analyze_error_patterns.return_value = {
            "recurring_mistakes": []
        }
        mock_analytics_class.return_value = mock_analytics

        # Mock database queries
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.all.return_value = []

        mock_db.query.return_value = mock_query

        service = IntegrationService(mock_db)
        result = service.get_personalized_learning_path(test_user.id)

        assert result["user_id"] == test_user.id
        assert "focus_areas" in result
        assert "daily_plan" in result
        assert "weekly_plan" in result
        assert "recommended_contexts" in result
        assert "motivation_message" in result


def test_integration_service_dashboard_data(mock_db, test_user):
    """Test IntegrationService get_dashboard_data method."""
    from app.services.integration_service import IntegrationService

    # Mock analytics service
    with patch('app.services.integration_service.AnalyticsService') as mock_analytics_class:
        mock_analytics = Mock()
        mock_analytics.get_overall_progress.return_value = {
            "user_id": 1,
            "overall_score": 75,
            "conversation": {"total_sessions": 10, "unique_contexts_practiced": 3},
            "grammar": {"weak_areas": [], "topics_practiced": 8, "overall_accuracy_percentage": 80},
            "vocabulary": {"total_words_learned": 100, "words_mastered": 25},
            "activity": {"current_streak_days": 5},
            "weekly_goal_progress": {"sessions_this_week": 4}
        }
        mock_analytics_class.return_value = mock_analytics

        # Mock database queries
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        mock_query.join.return_value = mock_query
        mock_query.order_by.return_value = mock_query
        mock_query.group_by.return_value = mock_query
        mock_query.limit.return_value = mock_query
        mock_query.all.return_value = []
        mock_query.first.return_value = None

        mock_db.query.return_value = mock_query

        service = IntegrationService(mock_db)
        result = service.get_dashboard_data(test_user.id)

        assert result["user_id"] == test_user.id
        assert "overall_progress" in result
        assert "learning_path" in result
        assert "due_items" in result
        assert "recent_activity" in result
        assert "quick_actions" in result
