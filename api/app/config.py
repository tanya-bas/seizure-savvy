import os
from datetime import timedelta
from dotenv import load_dotenv

# move up one directory, to api/
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# search for .env in the project directory
load_dotenv(os.path.join(base_dir, "..", ".env"))


class Config:
    # Set the secret key for the Flask app and JWT
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(os.getenv("DATABASE_URI"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT config
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAME_SITE = "None"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # Disable CSRF protection in testing
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAME_SITE = "Lax"
