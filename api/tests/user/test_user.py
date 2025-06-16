"""This module contains the tests for user-related operations
jwt_required() decorator is used to protect the routes.
"""

from datetime import datetime

import pytest
from flask.testing import FlaskClient

from api.app.schema import User


class TestUserProfile:
    def test_get_user_profile(
        self, authenticated_client: FlaskClient, sample_user: User
    ):
        """Test getting user profile should be successful."""
        response = authenticated_client.get("/api/user/profile")
        print(response.json)
        assert response.status_code == 200
        assert "success" in response.json["message"].lower()
        assert response.json["data"]["first_name"] == sample_user.first_name
        assert response.json["data"]["email"] == sample_user.email

    def test_update_user_profile(
        self, authenticated_client: FlaskClient, sample_user: User
    ):
        """Test updating user profile should be successful."""
        new_data = {"first_name": "UpdatedName"}
        response = authenticated_client.put("/api/user/profile", json=new_data)
        assert response.status_code == 200
        assert "success" in response.json["message"].lower()

    def test_get_user_profile_unauthorized(self, client: FlaskClient):
        """Test unauthorized access to user profile."""
        response = client.get("/api/user/profile")
        assert response.status_code == 401

    def test_update_user_profile_unauthorized(self, client: FlaskClient):
        """Test unauthorized access to user profile."""
        response = client.put("/api/user/profile", json={"first_name": "ShouldFail"})
        assert response.status_code == 401


class TestUserPassword:
    def test_change_password(self, authenticated_client: FlaskClient):
        """Test correct password change."""
        response = authenticated_client.put(
            "/api/user/change-password",
            json={"old_password": "password", "new_password": "newsecurepassword"},
        )
        assert response.status_code == 200
        assert "success" in response.json["message"].lower()

    def test_change_password_invalid_old_password(
        self, authenticated_client: FlaskClient
    ):
        """Test changing password with invalid old password."""
        response = authenticated_client.put(
            "/api/user/change-password",
            json={
                "old_password": "invalidpassword",
                "new_password": "newsecurepassword",
            },
        )
        assert response.status_code == 401
        assert "incorrect" in response.json["message"].lower()

    def test_change_password_unauthorized(self, client: FlaskClient):
        """Test unauthorized access to change password."""
        response = client.put(
            "/api/user/change-password",
            json={"old_password": "password", "new_password": "newsecurepassword"},
        )
        assert response.status_code == 401


class TestUserAccount:

    def test_delete_account(
        self,
        authenticated_client: FlaskClient,
        db_session,
        sample_user: User,
    ):
        """Test successful account deletion."""

        response = authenticated_client.delete("/api/user/delete-account")
        assert response.status_code == 200
        assert response.json["message"] == "Account deleted successfully."
        assert db_session.query(User).filter(User.id == sample_user.id).first() is None

    def test_delete_account_unauthorized(self, client: FlaskClient):
        """Test unauthorized access to delete account."""
        response = client.delete("/api/user/delete-account")
        assert response.status_code == 401
