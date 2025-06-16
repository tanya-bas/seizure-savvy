"""This module contains endpoints to manage medications"""

from datetime import date, datetime

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy.exc import SQLAlchemyError

from . import db
from .schema import Medication
from .user import get_current_user

medication_bp = Blueprint("medication", __name__, url_prefix="/api/medications")


@medication_bp.route("/", methods=["GET"])
@jwt_required()
def get_medications():
    """Retrieve the list of medications for the user."""
    user = get_current_user()
    med_pagination = db.paginate(
        db.select(Medication)
        .filter_by(user_id=user.id)
        .order_by(Medication.start_date.desc()),
    )

    if not med_pagination.items:
        return {"message": "No medications."}, 404

    medications = [
        {
            "name": medication.name,
            "dosage_mg": medication.dosage_mg,
            "reason_for_stop": medication.reason_for_stop,
            "frequency": medication.frequency,
            "first_dose": (
                medication.first_dose.strftime("%H:%M")
                if medication.first_dose
                else None
            ),  # format time as HH:MM
            "start_date": medication.start_date.isoformat(),
            "end_date": (
                medication.end_date.isoformat() if medication.end_date else None
            ),
            "is_stopped": medication.is_stopped,  # include is_stopped status in the output
        }
        for medication in med_pagination.items
    ]
    return {
        "data": medications,
        "pagination": {
            "page": med_pagination.page,
            "total_pages": med_pagination.pages,
            "total_items": med_pagination.total,
        },
    }, 200


@medication_bp.route("/", methods=["POST"])
@jwt_required()
def add_medication():
    user = get_current_user()
    data = request.json
    try:
        if "start_date" in data:
            data["start_date"] = datetime.strptime(
                data["start_date"], "%Y-%m-%d"
            ).date()
        if "end_date" in data and data["end_date"] is not None:
            data["end_date"] = datetime.strptime(data["end_date"], "%Y-%m-%d").date()
        if "first_dose" in data and data["first_dose"] is not None:
            data["first_dose"] = datetime.strptime(data["first_dose"], "%H:%M").time()

        medication = Medication(user_id=user.id, **data)
        db.session.add(medication)
        db.session.commit()
        return {"message": "Medication added successfully.", "id": medication.id}, 201
    except ValueError as e:
        db.session.rollback()
        return {"message": f"Error processing date or time: {str(e)}"}, 400
    except SQLAlchemyError as e:
        db.session.rollback()
        return {"message": f"Database error: {str(e)}"}, 500
    except Exception as e:
        db.session.rollback()
        return {"message": f"Internal Server Error: {str(e)}"}, 500


@medication_bp.route("/<int:med_id>", methods=["PUT"])
@jwt_required()
def update_medication(med_id):
    """Update a user's medication in the database."""
    user = get_current_user()
    medication = (
        db.session.query(Medication).filter_by(id=med_id, user_id=user.id).first()
    )
    if not medication:
        return jsonify({"message": "Medication not found"}), 404

    data = request.get_json()
    try:
        # Handle date and time conversions
        for key, value in data.items():
            if key == "start_date" and value:
                medication.start_date = datetime.strptime(value, "%Y-%m-%d").date()
            elif key == "end_date" and value:
                medication.end_date = datetime.strptime(value, "%Y-%m-%d").date()
            elif key == "first_dose" and value:
                medication.first_dose = datetime.strptime(value, "%H:%M").time()
            else:
                setattr(medication, key, value)

        db.session.commit()
        return jsonify({"id": medication.id}), 200
    except ValueError as ve:
        db.session.rollback()
        return jsonify({"message": "Invalid date or time format: " + str(ve)}), 400
    except SQLAlchemyError as sae:
        db.session.rollback()
        return jsonify({"message": "Database error: " + str(sae)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Internal Server Error: " + str(e)}), 500


@medication_bp.route("/<int:med_id>", methods=["DELETE"])
@jwt_required()
def delete_medication(med_id: int):
    """Delete a user's medication from the database."""
    try:
        user = get_current_user()
        medication = db.session.execute(
            db.select(Medication).filter_by(id=med_id, user_id=user.id)
        ).scalar_one_or_none()
        if not medication:
            return {"message": "Medication not found."}, 404

        db.session.delete(medication)
        db.session.commit()
        return {}, 204
    except SQLAlchemyError:
        db.session.rollback()
        return {"message": "Database error"}, 500
    except Exception:
        db.session.rollback()
        return {"message": "Internal Server Error"}, 500


@medication_bp.route("/<int:med_id>/stop", methods=["PUT"])
@jwt_required()
def stop_medication(med_id):
    """Endpoint to mark a medication as stopped."""
    user = get_current_user()
    medication = (
        db.session.query(Medication).filter_by(id=med_id, user_id=user.id).first()
    )
    if not medication:
        return jsonify({"message": "Medication not found"}), 404

    if medication.is_stopped:
        return jsonify({"message": "Medication already stopped"}), 400

    try:
        data = request.get_json()
        # Validate the end_date format
        end_date = data.get("end_date")
        if end_date:
            try:
                valid_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                medication.end_date = valid_date
            except ValueError:
                return (
                    jsonify({"message": "Invalid date format, please use YYYY-MM-DD"}),
                    400,
                )

        medication.is_stopped = True
        medication.reason_for_stop = data.get(
            "reason_for_stop", medication.reason_for_stop
        )

        db.session.commit()
        return jsonify({"message": "Medication stopped successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
