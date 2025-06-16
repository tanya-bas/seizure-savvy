"""
This module contains high-level test fixtures for the API tests.
"""

from datetime import date
from typing import Callable

import pytest
from flask import Flask
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy.orm import Session

from api.app import create_app, db
from api.app.config import TestConfig
from api.app.schema import User


@pytest.fixture()
def app() -> Flask:
    """Create and configure a new app instance for each test."""
    app = create_app(config_class=TestConfig)

    # Establish an application context before running the tests
    with app.app_context():
        # Create all the tables
        db.create_all()

        yield app

        # Teardown: drop all tables
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def db_session(app: Flask) -> Session:
    """A database session for tests"""
    with app.app_context():
        yield db.session


@pytest.fixture
def user_factory(db_session: Session) -> Callable:
    """A factory function to create user objects
      and commit them to the database."""

    def create_user(
        first_name: str,
        last_name: str,
        email: str,
        password: str,
        birthdate: date = date(2000, 1, 1),
        has_menstruation: bool = False,
    ):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            birthdate=birthdate,
            has_menstruation=has_menstruation,
        )
        user.set_password(password)
        db_session.add(user)
        db_session.commit()
        return user

    return create_user


@pytest.fixture
def sample_user(user_factory: Callable) -> User:
    """A sample user Object for testing."""
    return user_factory(
        first_name="Common",
        last_name="User",
        email="user@example.com",
        password="password",
        has_menstruation=False,
    )


@pytest.fixture
def access_token(sample_user: User) -> str:
    """Fixture to generate an access token for the sample user."""
    return create_access_token(identity=sample_user.email)


@pytest.fixture
def refresh_token(sample_user: User) -> str:
    """Fixture to generate a refresh token for the sample user."""
    return create_refresh_token(identity=sample_user.email)


@pytest.fixture
def authenticated_client(client: FlaskClient, access_token: str,
                         sample_user) -> FlaskClient:
    """A test client with authentication headers set for the sample user."""
    client.environ_base[
        'HTTP_AUTHORIZATION'] = 'Bearer ' + create_access_token(
            identity=sample_user.email)
    return client


"""
@pytest.fixture(autouse=True)
def _dump_routes(app):
    "Print all registered routes in the Flask app. For debugging purposes."
    print(app.url_map)
    yield
"""
