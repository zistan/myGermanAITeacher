"""
Tests for analytics and progress tracking endpoints.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.models.user import User
from app.models.achievement import Achievement, UserAchievement, UserStats
from app.models.session import ConversationSession
from app.models.grammar import GrammarSession, UserGrammarProgress, GrammarTopic
from app.models.vocabulary import VocabularyReview, UserVocabularyProgress


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
def test_user_stats():
    """Create test user stats."""
    stats = UserStats(
        id=1,
        user_id=1,
        total_study_time_minutes=300,
        total_sessions=25,
        current_streak_days=5,
        longest_streak_days=10,
        conversation_sessions=15,
        total_messages_sent=150,
        grammar_sessions=10,
        grammar_exercises_completed=100,
        grammar_exercises_correct=80,
        grammar_topics_mastered=5,
        average_grammar_accuracy=80,
        vocabulary_words_learned=100,
        vocabulary_words_mastered=20,
        vocabulary_reviews_completed=200,
        vocabulary_reviews_correct=180,
        average_vocabulary_accuracy=90,
        total_achievement_points=500,
        achievements_earned=5,
        updated_at=datetime.utcnow()
    )
    return stats


@pytest.fixture
def test_achievement():
    """Create a test achievement."""
    achievement = Achievement(
        id=1,
        name="First Steps",
        description="Complete your first conversation session",
        category="conversation",
        badge_icon="chat",
        badge_color="#94a3b8",
        criteria_type="conversation_sessions",
        criteria_value=1,
        tier="bronze",
        points=10,
        is_active=True
    )
    return achievement


@pytest.fixture
def mock_get_current_user(test_user):
    """Mock get_current_user dependency."""
    with patch('app.api.v1.analytics.get_current_user', return_value=test_user):
        yield


# ========== OVERALL PROGRESS TESTS ==========

@patch('app.api.v1.analytics.AnalyticsService')
def test_get_overall_progress_success(mock_analytics_service, mock_db, test_user, mock_get_current_user):
    """Test getting overall progress."""
    # Mock analytics service
    mock_analytics = Mock()
    mock_analytics.get_overall_progress.return_value = {
        "user_id": 1,
        "overall_score": 75,
        "last_updated": datetime.utcnow(),
        "conversation": {
            "total_sessions": 15,
            "total_messages": 150,
            "average_session_duration_minutes": 20.5,
            "unique_contexts_practiced": 5,
            "sessions_last_7_days": 3,
            "estimated_conversation_hours": 5.0
        },
        "grammar": {
            "topics_practiced": 10,
            "topics_mastered": 5,
            "total_exercises_attempted": 100,
            "overall_accuracy_percentage": 80.0,
            "average_mastery_level": 3.2,
            "weak_areas": [],
            "strong_areas": []
        },
        "vocabulary": {
            "total_words_learned": 100,
            "words_mastered": 20,
            "total_reviews": 200,
            "overall_accuracy_percentage": 90.0,
            "words_by_cefr_level": {"A1": 30, "A2": 40, "B1": 30},
            "personal_vocabulary_lists": 2,
            "current_streak_days": 5
        },
        "activity": {
            "total_study_days": 20,
            "current_streak_days": 5,
            "longest_streak_days": 10,
            "average_sessions_per_week": 5.5
        },
        "weekly_goal_progress": {
            "sessions_this_week": 4,
            "goal_sessions": 5,
            "goal_percentage": 80,
            "goal_met": False
        }
    }
    mock_analytics_service.return_value = mock_analytics

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/progress",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["overall_score"] == 75
    assert data["conversation"]["total_sessions"] == 15
    assert data["grammar"]["topics_mastered"] == 5
    assert data["vocabulary"]["total_words_learned"] == 100


@patch('app.api.v1.analytics.AnalyticsService')
def test_get_progress_comparison(mock_analytics_service, mock_db, test_user, mock_get_current_user):
    """Test comparing progress between periods."""
    mock_analytics = Mock()
    mock_analytics.get_progress_comparison.return_value = {
        "period_days": 30,
        "current_period": {
            "total_sessions": 15,
            "conversation_sessions": 10,
            "grammar_sessions": 5,
            "exercises_completed": 50,
            "exercise_accuracy": 85.0,
            "vocabulary_reviews": 100
        },
        "previous_period": {
            "total_sessions": 10,
            "conversation_sessions": 6,
            "grammar_sessions": 4,
            "exercises_completed": 40,
            "exercise_accuracy": 80.0,
            "vocabulary_reviews": 80
        },
        "changes": {
            "total_sessions_change_percent": 50.0,
            "total_sessions_trend": "up",
            "exercise_accuracy_change_percent": 6.25,
            "exercise_accuracy_trend": "up"
        }
    }
    mock_analytics_service.return_value = mock_analytics

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/progress/comparison?period_days=30",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["period_days"] == 30
    assert data["current_period"]["total_sessions"] == 15
    assert data["changes"]["total_sessions_trend"] == "up"


# ========== ERROR PATTERN ANALYSIS TESTS ==========

@patch('app.api.v1.analytics.AnalyticsService')
def test_analyze_error_patterns(mock_analytics_service, mock_db, test_user, mock_get_current_user):
    """Test error pattern analysis."""
    mock_analytics = Mock()
    mock_analytics.analyze_error_patterns.return_value = {
        "analysis_period_days": 30,
        "total_errors": 25,
        "top_error_topics": [
            {"topic": "Akkusativ", "count": 10},
            {"topic": "Dativ", "count": 8}
        ],
        "recurring_mistakes": [
            {
                "topic_id": 1,
                "topic_name": "Akkusativ",
                "error_count": 10,
                "severity": "high"
            }
        ],
        "improvement_trends": [
            {
                "topic_id": 2,
                "topic_name": "Präsens",
                "trend": "improving",
                "improvement_percentage": 15.5
            }
        ],
        "recommendations": [
            "Focus on 'Akkusativ' - this is your most frequent error area"
        ]
    }
    mock_analytics_service.return_value = mock_analytics

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/errors?days=30",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["analysis_period_days"] == 30
    assert data["total_errors"] == 25
    assert len(data["top_error_topics"]) == 2
    assert len(data["recurring_mistakes"]) == 1


# ========== ACHIEVEMENT TESTS ==========

def test_get_all_achievements(mock_db, test_user, test_achievement, mock_get_current_user):
    """Test getting all available achievements."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [test_achievement]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/achievements",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "First Steps"
    assert data[0]["tier"] == "bronze"


def test_get_all_achievements_filtered_by_category(mock_db, test_user, test_achievement, mock_get_current_user):
    """Test getting achievements filtered by category."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [test_achievement]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/achievements?category=conversation",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1


def test_get_user_achievements(mock_db, test_user, test_achievement, mock_get_current_user):
    """Test getting user's earned achievements."""
    user_achievement = UserAchievement(
        id=1,
        user_id=test_user.id,
        achievement_id=test_achievement.id,
        earned_at=datetime.utcnow(),
        is_completed=True
    )
    user_achievement.achievement = test_achievement

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [user_achievement]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/achievements/earned",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["is_completed"] is True


@patch('app.api.v1.analytics.AnalyticsService')
@patch('app.api.v1.analytics._calculate_achievement_progress')
def test_get_achievement_progress(mock_calc_progress, mock_analytics_service, mock_db, test_user, test_achievement, mock_get_current_user):
    """Test getting achievement progress."""
    # Mock analytics
    mock_analytics = Mock()
    mock_analytics.get_overall_progress.return_value = {
        "conversation": {"total_sessions": 5},
        "grammar": {"topics_mastered": 2, "overall_accuracy_percentage": 75},
        "vocabulary": {"total_words_learned": 50, "words_mastered": 10},
        "activity": {"current_streak_days": 3}
    }
    mock_analytics_service.return_value = mock_analytics

    # Mock calculation
    mock_calc_progress.return_value = 5

    # Mock queries
    achievements_query = Mock()
    achievements_query.filter.return_value = achievements_query
    achievements_query.all.return_value = [test_achievement]

    user_achievement_query = Mock()
    user_achievement_query.filter.return_value = user_achievement_query
    user_achievement_query.first.return_value = None

    mock_db.query.side_effect = [achievements_query, user_achievement_query]

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/achievements/progress",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


def test_showcase_achievement_success(mock_db, test_user, test_achievement, mock_get_current_user):
    """Test showcasing an achievement."""
    user_achievement = UserAchievement(
        id=1,
        user_id=test_user.id,
        achievement_id=test_achievement.id,
        is_completed=True,
        is_showcased=False
    )

    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = user_achievement

    mock_db.query.return_value = mock_query

    request_data = {
        "achievement_id": 1,
        "is_showcased": True
    }

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/analytics/achievements/1/showcase",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    assert user_achievement.is_showcased is True


def test_showcase_achievement_not_earned(mock_db, test_user, mock_get_current_user):
    """Test showcasing an achievement that hasn't been earned."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None

    mock_db.query.return_value = mock_query

    request_data = {
        "achievement_id": 1,
        "is_showcased": True
    }

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/analytics/achievements/1/showcase",
            json=request_data,
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 404


# ========== USER STATS TESTS ==========

def test_get_user_stats_existing(mock_db, test_user, test_user_stats, mock_get_current_user):
    """Test getting existing user stats."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = test_user_stats

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/stats",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["total_sessions"] == 25
    assert data["current_streak_days"] == 5


def test_get_user_stats_create_if_missing(mock_db, test_user, mock_get_current_user):
    """Test creating stats if they don't exist."""
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = None

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/stats",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    mock_db.add.assert_called_once()


@patch('app.api.v1.analytics.AnalyticsService')
def test_refresh_user_stats(mock_analytics_service, mock_db, test_user, test_user_stats, mock_get_current_user):
    """Test refreshing user stats."""
    # Mock analytics
    mock_analytics = Mock()
    mock_analytics.get_overall_progress.return_value = {
        "conversation": {"total_sessions": 20, "total_messages": 200},
        "grammar": {"total_sessions": 15, "total_exercises_attempted": 150, "topics_mastered": 8, "overall_accuracy_percentage": 85},
        "vocabulary": {"total_words_learned": 150, "words_mastered": 30, "total_reviews": 300, "overall_accuracy_percentage": 92},
        "activity": {"current_streak_days": 7, "longest_streak_days": 15}
    }
    mock_analytics_service.return_value = mock_analytics

    # Mock query
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.first.return_value = test_user_stats

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.post(
            "/api/v1/analytics/stats/refresh",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    mock_db.commit.assert_called()


# ========== LEADERBOARD TESTS ==========

def test_get_leaderboard_overall(mock_db, test_user, test_user_stats, mock_get_current_user):
    """Test getting overall leaderboard."""
    # Create mock users and stats
    user2 = User(id=2, username="user2", email="user2@test.com")
    stats2 = UserStats(user_id=2, total_sessions=30, total_achievement_points=600)

    user3 = User(id=3, username="user3", email="user3@test.com")
    stats3 = UserStats(user_id=3, total_sessions=20, total_achievement_points=400)

    mock_query = Mock()
    mock_query.join.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [
        (user2, stats2),
        (test_user, test_user_stats),
        (user3, stats3)
    ]
    mock_query.count.return_value = 3

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/leaderboard/overall",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["leaderboard_type"] == "overall"
    assert len(data["entries"]) == 3
    assert data["user_rank"] == 2


# ========== HEATMAP TESTS ==========

def test_get_activity_heatmap(mock_db, test_user, mock_get_current_user):
    """Test getting activity heatmap."""
    # Mock session counts
    mock_conv_query = Mock()
    mock_conv_query.filter.return_value = mock_conv_query
    mock_conv_query.count.return_value = 2

    mock_grammar_query = Mock()
    mock_grammar_query.filter.return_value = mock_grammar_query
    mock_grammar_query.count.return_value = 1

    mock_vocab_query = Mock()
    mock_vocab_query.filter.return_value = mock_vocab_query
    mock_vocab_query.count.return_value = 3

    # Mock AnalyticsService
    with patch('app.api.v1.analytics.AnalyticsService') as mock_analytics_service:
        mock_analytics = Mock()
        mock_analytics.get_overall_progress.return_value = {
            "activity": {"current_streak_days": 5}
        }
        mock_analytics_service.return_value = mock_analytics

        mock_db.query.side_effect = [mock_conv_query, mock_grammar_query, mock_vocab_query] * 365

        with patch('app.api.v1.analytics.get_db', return_value=mock_db):
            response = client.get(
                "/api/v1/analytics/heatmap/activity?days=365",
                headers={"Authorization": "Bearer test_token"}
            )

    assert response.status_code == 200
    data = response.json()
    assert "cells" in data
    assert data["total_days"] == 365


@patch('app.api.v1.analytics.AnalyticsService')
def test_get_grammar_heatmap(mock_analytics_service, mock_db, test_user, mock_get_current_user):
    """Test getting grammar mastery heatmap."""
    topic1 = GrammarTopic(id=1, name_de="Akkusativ", category="cases")
    progress1 = UserGrammarProgress(
        user_id=test_user.id,
        topic_id=1,
        mastery_level=3.5,
        last_practiced=datetime.utcnow()
    )

    topic2 = GrammarTopic(id=2, name_de="Präsens", category="verb_conjugation")
    progress2 = UserGrammarProgress(
        user_id=test_user.id,
        topic_id=2,
        mastery_level=4.5,
        last_practiced=datetime.utcnow()
    )

    mock_query = Mock()
    mock_query.join.return_value = mock_query
    mock_query.filter.return_value = mock_query
    mock_query.all.return_value = [(progress1, topic1), (progress2, topic2)]

    mock_db.query.return_value = mock_query

    with patch('app.api.v1.analytics.get_db', return_value=mock_db):
        response = client.get(
            "/api/v1/analytics/heatmap/grammar",
            headers={"Authorization": "Bearer test_token"}
        )

    assert response.status_code == 200
    data = response.json()
    assert len(data["topics"]) == 2
    assert "cases" in data["categories"]
    assert "verb_conjugation" in data["categories"]
    assert data["overall_mastery"] > 0
