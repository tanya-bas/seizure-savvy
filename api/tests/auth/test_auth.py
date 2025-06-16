import pytest
from api.app.schema import User


def test_register_success(register_user, valid_register_data):
    """Test that a user can be registered successfully."""
    response = register_user(valid_register_data)
    assert response.status_code == 201
    assert "success" in response.json["message"].lower()

    user = User.query.filter_by(email=valid_register_data["email"]).first()
    assert user is not None


def test_register_duplicate_email(register_user, valid_register_data):
    """Test that registering a user with an existing email fails."""
    # Register the user once
    register_user(valid_register_data)

    # Try to register the user again with the same email
    response = register_user(valid_register_data)
    assert response.status_code == 400
    assert "exists" in response.json["message"].lower()


def test_register_invalid_email(register_user, valid_register_data):
    """Test that registering a user with an invalid email fails."""
    # Change the email to an invalid one
    valid_register_data["email"] = "invalid-email"

    response = register_user(valid_register_data)
    assert response.status_code == 400
    assert "invalid" in response.json["message"].lower()


def test_login_success(
    register_user, login_user, valid_register_data, valid_login_data
):
    """Test that a user can log in successfully."""
    # First, register the user
    register_user(valid_register_data)

    # Then, log in the user
    response = login_user(valid_login_data)

    assert response.status_code == 200
    assert "success" in response.json["message"].lower()
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_with_invalid_password(
    register_user, login_user, valid_register_data, invalid_login_data
):
    """Test that logging in with an invalid password fails."""
    # First, register the user
    register_user(valid_register_data)

    # Try to log in with an invalid password
    response = login_user(invalid_login_data)
    assert response.status_code == 401
    assert "invalid" in response.json["message"].lower()


def test_refresh_token(client, register_user, valid_register_data, refresh_token):
    """Test that a refresh token can be used to get a new access token."""
    # First, register the user
    register_user(valid_register_data)

    # Then, send a POST request to the refresh token endpoint
    response = client.post(
        "/api/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )

    # Check the status code and the response body
    assert response.status_code == 200
    assert "access_token" in response.json


def test_token_expiry(authenticated_client, frozen_time_future):
    """Test that an expired token results in a 401 response."""
    # Freeze time at the current moment
    frozen_time_future()

    # Send a request with the expired token
    response = authenticated_client.get("/api/user/profile")

    # Check the status code
    assert response.status_code == 401
