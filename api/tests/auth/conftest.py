from datetime import timedelta

import pytest
from flask.testing import FlaskClient
from freezegun import freeze_time
from sqlalchemy.orm import Session
from typing import Dict, Callable

from api.app.auth import User


@pytest.fixture
def valid_register_data() -> Dict[str, str]:
    """Fixture to provide valid data for registration."""
    return {
        "first_name": "Test",
        "last_name": "User",
        "email": "testuser@example.com",
        "password": "strong_password",
        "birthdate": "1990-01-01",
    }


@pytest.fixture
def valid_login_data(sample_user: User) -> Dict[str, str]:
    """Fixture to provide valid login data."""
    return {
        "email": sample_user.email,
        "password": "password",
    }


@pytest.fixture
def invalid_login_data(valid_login_data: Dict[str, str]) -> Dict[str, str]:
    """Fixture to provide invalid login data."""
    return {
        "email": valid_login_data["email"],
        "password": "wrong_password",
    }


@pytest.fixture
def register_user(client: FlaskClient, valid_register_data: Dict[str, str]) -> Callable:
    """Fixture to register a user."""

    def do_register(data=None):
        if data is None:
            data = valid_register_data
        return client.post("/api/auth/register", json=data)

    return do_register


@pytest.fixture
def login_user(client: FlaskClient, valid_login_data: Dict[str, str]) -> Callable:
    """Fixture to log in a user."""

    def do_login(data=None):
        if data is None:
            data = valid_login_data
        return client.post("/api/auth/login", json=data)

    return do_login


@pytest.fixture
def frozen_time_now():
    """Fixture to freeze time at the current moment, to test time-sensitive operations,such as token expiration and daily logs."""
    with freeze_time() as frozen_datetime:
        yield frozen_datetime


@pytest.fixture
def frozen_time_future(hours=24):
    """Fixture to freeze time in the future."""
    with freeze_time() as frozen_datetime:
        future_time = frozen_datetime() + timedelta(hours=hours)
        frozen_datetime.move_to(future_time)
        yield frozen_datetime
