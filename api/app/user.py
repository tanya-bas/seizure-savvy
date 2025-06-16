"""This module contains the routes for user-related operations,
such as updating the user profile, changing the password.
"""

from datetime import date, datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import raiseload

from . import db
from .schema import User

user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def get_current_user():
    """Get the current user Object from the database."""
    current_user_email = get_jwt_identity()

    # Load the user object
    user = db.session.execute(
        db.select(User).filter_by(email=current_user_email)
    ).scalar_one_or_none()
    return user


@user_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_user_profile():
    """Retrieve the details of the logged-in user."""
    user = get_current_user()

    if not user:
        return {"message": "User not found."}, 404

    user_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "birthdate": user.birthdate.isoformat() if user.birthdate else None,
        "has_menstruation": user.has_menstruation,
    }

    return {"data": user_data, "message": "User profile retrieved successfully."}, 200


@user_bp.route("/profile", methods=["PUT"])
@jwt_required()
def update_user_profile():
    """Update the personal details of the logged-in user."""
    user = get_current_user()

    if not user:
        return {"message": "User not found."}, 404

    data = request.get_json()

    try:
        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)
        user.has_menstruation = data.get("has_menstruation", user.has_menstruation)

        birthdate_str = data.get("birthdate")
        if birthdate_str:
            user.birthdate = datetime.fromisoformat(birthdate_str).date()
            if not user.is_adult():
                return {"message": "You must be at least 18 years old."}, 400

        db.session.commit()

    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "An error occurred while updating the profile."}, 500

    return {"message": "Profile updated successfully."}, 200


@user_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    """Change the password of the logged-in user."""
    try:
        user = get_current_user()

        if not user:
            return {"message": "User not found."}, 404

        data = request.get_json()
        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not user.check_password(old_password):
            return {"message": "Old password is incorrect."}, 401
        elif old_password == new_password:
            return {
                "message": "New password should be different from the old password."
            }, 400

        user.set_password(new_password)
        db.session.commit()

        return {"message": "Password changed successfully."}, 200
    except Exception as e:
        db.session.rollback()
        return {"message": str(e)}, 500


@user_bp.route("/delete-account", methods=["DELETE"])
@jwt_required()
def delete_account():
    """Delete the account of the logged-in user."""

    user = get_current_user()

    if not user:
        return {"message": "User not found."}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "Account deleted successfully."}, 200

    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "An error occurred while deleting the account."}, 500
    except Exception as e:
        return {"message": str(e)}, 500
