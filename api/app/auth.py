from datetime import date, datetime

from flask import Blueprint, current_app, jsonify, make_response, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required, 
)
from werkzeug.exceptions import BadRequest

from . import db
from .schema import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    """Register a new user."""
    try:
        data = request.get_json()

        # Validate required fields
        for field in ["first_name", "last_name", "email", "password"]:
            if field not in data:
                return {"message": f"{field} is required."}, 400

        first_name = data["first_name"]
        last_name = data["last_name"]
        email = data["email"]
        password = data["password"]  # Password check is done in the frontend
        birthdate_str = data.get("birthdate")  # returns None if not found
        has_menstruation = data.get("has_menstruation")

        user = User.query.filter_by(email=email).first()

        if user:
            return {"message": "Email address already exists!"}, 400

        # Convert birthdate string to date object
        if birthdate_str:
            birthdate = datetime.fromisoformat(birthdate_str).date()

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            birthdate=birthdate,
            has_menstruation=has_menstruation,
        )

        # Validate email format
        if not new_user.validate_email():
            return {"message": "Invalid email format."}, 400

        # Set password and add to database
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.flush()  # To get database-level variables, like age and ID

        # Validate age
        if not new_user.is_adult():
            db.session.rollback()
            return {"message": "You must be at least 18 years old."}, 400

        # Persist changes to database
        db.session.commit()

        return {"message": "Successfully registered! Please login."}, 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(e)
        return {"message": "An error occurred. Please try again"}, 500


from werkzeug.exceptions import BadRequest


@auth_bp.route("/login", methods=["POST"])
def login():
    """Log in a user."""
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password are required."}, 400

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid email or password. Login again."}, 401

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)

        response = {
            "message": "Successful login!",
            "access_token": access_token,
            "refresh_token": refresh_token,
        }, 200

        return response
    except BadRequest:
        return {"message": "Invalid request. Please provide valid JSON."}, 400
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Unexpected error"}, 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    """Refresh the access token."""
    try:
        current_user_email = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user_email)

        response = {
            "message": "Access token refreshed.",
            "access_token": new_access_token,
        }, 200

        return response
    except BadRequest:
        return {"message": "Invalid request. Please provide valid JSON."}, 400
    except Exception as e:
        current_app.logger.error(e)
        return {"message": "Unexpected error:"}, 500
