"""
Tests for context management endpoints.
"""
import pytest
from fastapi import status

from app.models.context import Context


@pytest.fixture
def test_contexts(db_session):
    """Create multiple test contexts."""
    contexts = [
        Context(
            name="Business Meeting",
            category="business",
            difficulty_level="C1",
            description="Professional business discussion",
            system_prompt="You are a business executive",
            is_active=True
        ),
        Context(
            name="Restaurant",
            category="daily",
            difficulty_level="B1",
            description="Ordering food",
            system_prompt="You are a waiter",
            is_active=True
        ),
        Context(
            name="Inactive Context",
            category="business",
            difficulty_level="B2",
            description="This is inactive",
            system_prompt="Test",
            is_active=False
        )
    ]
    for context in contexts:
        db_session.add(context)
    db_session.commit()
    for context in contexts:
        db_session.refresh(context)
    return contexts


class TestContextEndpoints:
    """Test context management endpoints."""

    def test_list_all_contexts(self, client, db_session, test_contexts):
        """Test listing all active contexts."""
        response = client.get("/api/contexts")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2  # Only active contexts
        assert all(ctx["is_active"] for ctx in data)

    def test_list_contexts_filter_by_category(self, client, test_contexts):
        """Test filtering contexts by category."""
        response = client.get("/api/contexts?category=business")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(ctx["category"] == "business" for ctx in data)
        assert len(data) == 1  # Only active business context

    def test_list_contexts_filter_by_difficulty(self, client, test_contexts):
        """Test filtering contexts by difficulty."""
        response = client.get("/api/contexts?difficulty=B1")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert all(ctx["difficulty_level"] == "B1" for ctx in data)
        assert len(data) == 1

    def test_list_contexts_include_inactive(self, client, test_contexts):
        """Test listing contexts including inactive ones."""
        response = client.get("/api/contexts?active_only=false")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 3  # All contexts including inactive

    def test_get_context_by_id(self, client, auth_headers, test_contexts):
        """Test getting a specific context."""
        context_id = test_contexts[0].id

        response = client.get(
            f"/api/contexts/{context_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == context_id
        assert data["name"] == "Business Meeting"
        assert "times_used" in data

    def test_get_context_not_found(self, client, auth_headers):
        """Test getting non-existent context."""
        response = client.get(
            "/api/contexts/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_context_success(self, client, auth_headers):
        """Test creating a new context."""
        new_context = {
            "name": "New Test Context",
            "category": "business",
            "difficulty_level": "B2",
            "description": "Test description",
            "system_prompt": "You are a helpful assistant",
            "suggested_vocab": [1, 2, 3],
            "is_active": True
        }

        response = client.post(
            "/api/contexts",
            json=new_context,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == "New Test Context"
        assert data["category"] == "business"
        assert "id" in data

    def test_create_context_invalid_category(self, client, auth_headers):
        """Test creating context with invalid category."""
        invalid_context = {
            "name": "Test",
            "category": "invalid_category",
            "system_prompt": "Test prompt"
        }

        response = client.post(
            "/api/contexts",
            json=invalid_context,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_context_unauthorized(self, client):
        """Test creating context without authentication."""
        response = client.post(
            "/api/contexts",
            json={"name": "Test", "category": "business", "system_prompt": "Test"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_context_success(self, client, auth_headers, test_contexts):
        """Test updating an existing context."""
        context_id = test_contexts[0].id

        update_data = {
            "name": "Updated Business Meeting",
            "description": "Updated description"
        }

        response = client.put(
            f"/api/contexts/{context_id}",
            json=update_data,
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["name"] == "Updated Business Meeting"
        assert data["description"] == "Updated description"
        # Other fields should remain unchanged
        assert data["category"] == "business"

    def test_update_context_not_found(self, client, auth_headers):
        """Test updating non-existent context."""
        response = client.put(
            "/api/contexts/99999",
            json={"name": "Test"},
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_context_success(self, client, auth_headers, test_contexts):
        """Test deleting (deactivating) a context."""
        context_id = test_contexts[0].id

        response = client.delete(
            f"/api/contexts/{context_id}",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify context is deactivated, not deleted
        verify_response = client.get(
            f"/api/contexts/{context_id}",
            headers=auth_headers
        )
        assert verify_response.json()["is_active"] is False

    def test_delete_context_not_found(self, client, auth_headers):
        """Test deleting non-existent context."""
        response = client.delete(
            "/api/contexts/99999",
            headers=auth_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
