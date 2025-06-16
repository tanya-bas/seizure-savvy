import tensorflow as tf
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from jwt import ExpiredSignatureError

from .config import Config
from .schema import db

# TODO: Load the model
# model = tf.keras.models.load_model("model.h5")

jwt = JWTManager()
migrate = Migrate()


def create_app(config_class=Config):
    """
    Create and configure the Flask app.
    Args:
        config_class (Config): The configuration class to use.
    Returns:
        Flask: The configured Flask app.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(
        app,
        supports_credentials=True,
        resources={r"/api/*": {"origins": "*"}},
    )
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        db.create_all()
        migrate.init_app(app, db)

    # Import parts of our core Flask app
    from .auth import auth_bp
    from .user import user_bp
    from .medication import medication_bp
    from .dailylog import datalog_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(medication_bp)
    app.register_blueprint(datalog_bp)

    return app
