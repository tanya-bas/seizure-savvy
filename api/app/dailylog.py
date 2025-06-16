from flask import Blueprint, request, jsonify, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from . import db
from datetime import datetime, timedelta
from .schema import User, UserLog, Prodrome, UserProdrome, Aura, UserAura
from .schema import Trigger, UserTrigger, SeizureEpisode, SeizureType
from sqlalchemy.exc import SQLAlchemyError

datalog_bp = Blueprint("datalog", __name__, url_prefix="/api/datalog")


@datalog_bp.route("/user-prodromes", methods=["POST"])
@jwt_required()
def create_user_prodrome():
    app.logger.debug("Received request for user-prodrome creation")
    # Get the identity of the current user
    current_user_email = get_jwt_identity()

    # Query the database for the current user
    user = User.query.filter_by(email=current_user_email).first()

    # If the user is not found, return an error
    if not user:
        app.logger.debug("User not found: %s", current_user_email)  # Debug log
        return jsonify({"message": "User not found"}), 404

    # Get the data from the request
    data = request.get_json()

    # Validate the provided log_id and prodrome_id
    log_id = data.get("log_id")
    prodrome_id = data.get("prodrome_id")
    intensity = data.get("intensity")
    note = data.get("note", "")  # Note is optional

    if not log_id or not prodrome_id or intensity is None:
        return jsonify({"message": "Missing log_id, prodrome_id, or intensity"}), 400

    # Check if the provided log_id and prodrome_id exist
    log = UserLog.query.get(log_id)
    prodrome = Prodrome.query.get(prodrome_id)
    # Log fetched items
    app.logger.debug("Log: %s, Prodrome: %s", log, prodrome)

    if not log or not prodrome:
        return jsonify({"message": "Log or Prodrome not found"}), 404

    # Ensure the log belongs to the current user
    if log.user_id != user.id:
        return jsonify({"message": "This log does not belong to the current user"}), 403

    # Create a new UserProdrome instance
    new_user_prodrome = UserProdrome(
        log_id=log.id, prodrome_id=prodrome.id, intensity=intensity, note=note
    )

    # Add the new UserProdrome to the database session and commit
    try:
        db.session.add(new_user_prodrome)
        db.session.commit()
        # Return a success message with the ID of the new UserProdrome
        return (
            jsonify(
                {
                    "message": "UserProdrome created successfully",
                    "user_prodrome_id": new_user_prodrome.id,
                }
            ),
            201,
        )
    except Exception as e:
        # In case of an exception, roll back the session and return an error
        db.session.rollback()
        return (
            jsonify({"message": "Failed to create UserProdrome", "error": str(e)}),
            500,
        )


@datalog_bp.route("/user-auras", methods=["POST"])
@jwt_required()
def create_user_aura():
    # Get the identity of the current user
    current_user_email = get_jwt_identity()

    # Query the database for the current user
    user = User.query.filter_by(email=current_user_email).first()

    # If the user is not found, return an error
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the data from the request
    data = request.get_json()

    # Validate the provided log_id and aura_id
    log_id = data.get("log_id")
    aura_id = data.get("aura_id")
    is_present = data.get("is_present")
    note = data.get("note", "")  # Note is optional

    if not log_id or not aura_id or is_present is None:
        return jsonify({"message": "Missing log_id, aura_id, or is_present"}), 400

    # Check if the provided log_id and aura_id exist
    log = UserLog.query.get(log_id)
    aura = Aura.query.get(aura_id)

    if not log or not aura:
        return jsonify({"message": "Log or Aura not found"}), 404

    # Ensure the log belongs to the current user
    if log.user_id != user.id:
        return jsonify({"message": "This log does not belong to the current user"}), 403

    # Create a new UserAura instance
    new_user_aura = UserAura(
        log_id=log.id, aura_id=aura.id, is_present=is_present, note=note
    )

    # Add the new UserAura to the database session and commit
    try:
        db.session.add(new_user_aura)
        db.session.commit()
        # Return a success message with the ID of the new UserAura
        return (
            jsonify(
                {
                    "message": "UserAura created successfully",
                    "user_aura_id": new_user_aura.id,
                }
            ),
            201,
        )
    except Exception as e:
        # In case of an exception, roll back the session and return an error
        db.session.rollback()
        return jsonify({"message": "Failed to create UserAura", "error": str(e)}), 500


@datalog_bp.route("/user-triggers", methods=["POST"])
@jwt_required()
def create_user_trigger():
    # Get the identity of the current user
    current_user_email = get_jwt_identity()

    # Query the database for the current user
    user = User.query.filter_by(email=current_user_email).first()

    # If the user is not found, return an error
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the data from the request
    data = request.get_json()

    # Validate the provided log_id and trigger_id
    log_id = data.get("log_id")
    trigger_id = data.get("trigger_id")
    value_numeric = data.get("value_numeric")
    value_boolean = data.get("value_boolean")
    note = data.get("note", "")  # Note is optional

    # Basic validation checks
    if not log_id or not trigger_id:
        return jsonify({"message": "Missing log_id or trigger_id"}), 400
    if value_numeric is None and value_boolean is None:
        return jsonify({"message": "Missing value for the trigger"}), 400

    # Check if the provided log_id and trigger_id exist
    log = UserLog.query.get(log_id)
    trigger = Trigger.query.get(trigger_id)

    if not log or not trigger:
        return jsonify({"message": "Log or Trigger not found"}), 404

    # Ensure the log belongs to the current user
    if log.user_id != user.id:
        return jsonify({"message": "This log does not belong to the current user"}), 403

    # Create a new UserTrigger instance
    new_user_trigger = UserTrigger(
        log_id=log.id,
        trigger_id=trigger.id,
        value_numeric=value_numeric,
        value_boolean=value_boolean,
        note=note,
    )

    # Add the new UserTrigger to the database session and commit
    try:
        db.session.add(new_user_trigger)
        db.session.commit()
        # Return a success message with the ID of the new UserTrigger
        return (
            jsonify(
                {
                    "message": "UserTrigger created successfully",
                    "user_trigger_id": new_user_trigger.id,
                }
            ),
            201,
        )
    except Exception as e:
        # In case of an exception, roll back the session and return an error
        db.session.rollback()
        return (
            jsonify({"message": "Failed to create UserTrigger", "error": str(e)}),
            500,
        )


@datalog_bp.route("/seizure-episodes", methods=["POST"])
@jwt_required()
def create_seizure_episode():
    # Get the identity of the current user
    current_user_email = get_jwt_identity()

    # Query the database for the current user
    user = User.query.filter_by(email=current_user_email).first()

    # If the user is not found, return an error
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Get the data from the request
    data = request.get_json()

    # Validate the provided log_id and seizure_type_id
    log_id = data.get("log_id")
    seizure_type_id = data.get("seizure_type_id")
    duration_sec = data.get("duration_sec")
    frequency = data.get("frequency", 1)  # Default to 1 if not provided
    requires_emergency_intervention = data.get("requires_emergency_intervention", False)
    note = data.get("note", "")  # Note is optional

    # Extract postictal attributes
    postictal_confusion_duration = data.get("postictal_confusion_duration")
    postictal_confusion_intensity = data.get("postictal_confusion_intensity")
    postictal_headache_duration = data.get("postictal_headache_duration")
    postictal_headache_intensity = data.get("postictal_headache_intensity")
    postictal_fatigue_duration = data.get("postictal_fatigue_duration")
    postictal_fatigue_intensity = data.get("postictal_fatigue_intensity")

    # Perform other necessary validations and parsing here...

    if not log_id or not seizure_type_id or duration_sec is None:
        return (
            jsonify({"message": "Missing log_id, seizure_type_id, or duration_sec"}),
            400,
        )

    # Check if the provided log_id and seizure_type_id exist
    log = UserLog.query.get(log_id)
    seizure_type = SeizureType.query.get(seizure_type_id)

    if not log or not seizure_type:
        return jsonify({"message": "Log or SeizureType not found"}), 404

    # Ensure the log belongs to the current user
    if log.user_id != user.id:
        return jsonify({"message": "This log does not belong to the current user"}), 403

    # Create a new SeizureEpisode instance with all attributes
    new_seizure_episode = SeizureEpisode(
        log_id=log.id,
        seizure_type_id=seizure_type.id,
        duration_sec=duration_sec,
        frequency=frequency,
        requires_emergency_intervention=requires_emergency_intervention,
        note=note,
        postictal_confusion_duration=postictal_confusion_duration,
        postictal_confusion_intensity=postictal_confusion_intensity,
        postictal_headache_duration=postictal_headache_duration,
        postictal_headache_intensity=postictal_headache_intensity,
        postictal_fatigue_duration=postictal_fatigue_duration,
        postictal_fatigue_intensity=postictal_fatigue_intensity,
    )

    # Add the new SeizureEpisode to the database session and commit
    try:
        db.session.add(new_seizure_episode)
        db.session.commit()
        # Return a success message with the ID of the new SeizureEpisode
        return (
            jsonify(
                {
                    "message": "SeizureEpisode created successfully",
                    "seizure_episode_id": new_seizure_episode.id,
                }
            ),
            201,
        )
    except Exception as e:
        # In case of an exception, roll back the session and return an error
        db.session.rollback()
        return (
            jsonify({"message": "Failed to create SeizureEpisode", "error": str(e)}),
            500,
        )


@datalog_bp.route("/user-prodromes/<int:user_prodrome_id>", methods=["PUT"])
@jwt_required()
def update_user_prodrome(user_prodrome_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_prodrome = UserProdrome.query.get(user_prodrome_id)
    if not user_prodrome or user_prodrome.log.user_id != user.id:
        return jsonify({"message": "UserProdrome not found or access denied"}), 404

    data = request.get_json()
    intensity = data.get("intensity")
    note = data.get("note")

    if intensity is not None:
        user_prodrome.intensity = intensity
    if note is not None:
        user_prodrome.note = note

    db.session.commit()
    return jsonify({"message": "UserProdrome updated successfully"}), 200


@datalog_bp.route("/user-auras/<int:user_aura_id>", methods=["PUT"])
@jwt_required()
def update_user_aura(user_aura_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_aura = UserAura.query.get(user_aura_id)
    if not user_aura or user_aura.log.user_id != user.id:
        return jsonify({"message": "UserAura not found or access denied"}), 404

    data = request.get_json()
    is_present = data.get("is_present")
    note = data.get("note")

    if is_present is not None:
        user_aura.is_present = is_present
    if note is not None:
        user_aura.note = note

    db.session.commit()
    return jsonify({"message": "UserAura updated successfully"}), 200


@datalog_bp.route("/user-triggers/<int:user_trigger_id>", methods=["PUT"])
@jwt_required()
def update_user_trigger(user_trigger_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_trigger = UserTrigger.query.get(user_trigger_id)
    if not user_trigger or user_trigger.log.user_id != user.id:
        return jsonify({"message": "UserTrigger not found or access denied"}), 404

    data = request.get_json()
    value_numeric = data.get("value_numeric")
    value_boolean = data.get("value_boolean")
    note = data.get("note")

    if value_numeric is not None:
        user_trigger.value_numeric = value_numeric
    if value_boolean is not None:
        user_trigger.value_boolean = value_boolean
    if note is not None:
        user_trigger.note = note

    db.session.commit()
    return jsonify({"message": "UserTrigger updated successfully"}), 200


@datalog_bp.route("/seizure-episodes/<int:seizure_episode_id>", methods=["PUT"])
@jwt_required()
def update_seizure_episode(seizure_episode_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    seizure_episode = SeizureEpisode.query.get(seizure_episode_id)
    if not seizure_episode or seizure_episode.log.user_id != user.id:
        return jsonify({"message": "SeizureEpisode not found or access denied"}), 404

    data = request.get_json()
    # Update fields as provided
    for field in [
        "duration_sec",
        "frequency",
        "note",
        "requires_emergency_intervention",
        "postictal_confusion_duration",
        "postictal_confusion_intensity",
        "postictal_headache_duration",
        "postictal_headache_intensity",
        "postictal_fatigue_duration",
        "postictal_fatigue_intensity",
    ]:
        if field in data:
            setattr(seizure_episode, field, data[field])

    db.session.commit()
    return jsonify({"message": "SeizureEpisode updated successfully"}), 200


@datalog_bp.route("/user-prodromes/<int:user_prodrome_id>", methods=["DELETE"])
@jwt_required()
def delete_user_prodrome(user_prodrome_id):
    # Get the identity of the current user from the JWT
    current_user_email = get_jwt_identity()

    # Retrieve the current user's object from the database
    user = User.query.filter_by(email=current_user_email).first()

    # Check if the user was found
    if not user:
        return jsonify({"message": "User not found"}), 404

    # Retrieve the UserProdrome object to be deleted
    user_prodrome = UserProdrome.query.get(user_prodrome_id)

    # Check if the UserProdrome exists and belongs to the current user
    if not user_prodrome or user_prodrome.log.user_id != user.id:
        return jsonify({"message": "UserProdrome not found or access denied"}), 404

    try:
        # Delete the UserProdrome from the database
        db.session.delete(user_prodrome)
        db.session.commit()
        # Return a success message
        return jsonify({"message": "UserProdrome deleted successfully"}), 200
    except SQLAlchemyError as e:
        # In case of database error, rollback the transaction and log the error
        db.session.rollback()
        return (
            jsonify({"message": "Failed to delete UserProdrome", "error": str(e)}),
            500,
        )


@datalog_bp.route("/user-auras/<int:user_aura_id>", methods=["DELETE"])
@jwt_required()
def delete_user_aura(user_aura_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_aura = UserAura.query.get(user_aura_id)
    if not user_aura or user_aura.log.user_id != user.id:
        return jsonify({"message": "UserAura not found or access denied"}), 404

    try:
        db.session.delete(user_aura)
        db.session.commit()
        return jsonify({"message": "UserAura deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Failed to delete UserAura", "error": str(e)}), 500


@datalog_bp.route("/user-triggers/<int:user_trigger_id>", methods=["DELETE"])
@jwt_required()
def delete_user_trigger(user_trigger_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_trigger = UserTrigger.query.get(user_trigger_id)
    if not user_trigger or user_trigger.log.user_id != user.id:
        return jsonify({"message": "UserTrigger not found or access denied"}), 404

    try:
        db.session.delete(user_trigger)
        db.session.commit()
        return jsonify({"message": "UserTrigger deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify({"message": "Failed to delete UserTrigger", "error": str(e)}),
            500,
        )


@datalog_bp.route("/seizure-episodes/<int:seizure_episode_id>", methods=["DELETE"])
@jwt_required()
def delete_seizure_episode(seizure_episode_id):
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    seizure_episode = SeizureEpisode.query.get(seizure_episode_id)
    if not seizure_episode or seizure_episode.log.user_id != user.id:
        return jsonify({"message": "SeizureEpisode not found or access denied"}), 404

    try:
        db.session.delete(seizure_episode)
        db.session.commit()
        return jsonify({"message": "SeizureEpisode deleted successfully"}), 200
    except SQLAlchemyError as e:
        db.session.rollback()
        return (
            jsonify({"message": "Failed to delete SeizureEpisode", "error": str(e)}),
            500,
        )


# This endpoint fetches all logs for the authenticated user,
# including the associated Prodromes, Auras, Triggers, and SeizureEpisodes.
@datalog_bp.route("/logs", methods=["GET"])
@jwt_required()
def get_user_logs():
    try:
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return jsonify({"message": "User not found"}), 404

        user_logs = UserLog.query.filter_by(user_id=user.id).all()

        logs_data = []
        for log in user_logs:
            logs_data.append(
                {
                    "log_id": log.id,
                    "log_time": log.log_time,
                    "prodromes": [
                        {"id": prod.prodrome_id, "intensity": prod.intensity}
                        for prod in log.prodromes
                    ],
                    "auras": [
                        {"id": aura.aura_id, "is_present": aura.is_present}
                        for aura in log.auras
                    ],
                    "triggers": [
                        {
                            "id": trigger.trigger_id,
                            "value_numeric": trigger.value_numeric,
                            "value_boolean": trigger.value_boolean,
                        }
                        for trigger in log.triggers
                    ],
                    "seizure_episodes": [
                        {
                            "id": seizure.id,
                            "seizure_type_id": seizure.seizure_type_id,
                            "duration_sec": seizure.duration_sec,
                            "frequency": seizure.frequency,
                            "requires_emergency_intervention": seizure.requires_emergency_intervention,
                            "note": seizure.note,
                            "postictal_confusion_duration": seizure.postictal_confusion_duration,
                            "postictal_confusion_intensity": seizure.postictal_confusion_intensity,
                            "postictal_headache_duration": seizure.postictal_headache_duration,
                            "postictal_headache_intensity": seizure.postictal_headache_intensity,
                            "postictal_fatigue_duration": seizure.postictal_fatigue_duration,
                            "postictal_fatigue_intensity": seizure.postictal_fatigue_intensity,
                        }
                        for seizure in log.seizures
                    ],
                }
            )

        return jsonify(logs_data), 200

    except SQLAlchemyError as e:
        # Log the error internally, optionally
        return (
            jsonify(
                {
                    "message": "An error occurred accessing the database",
                    "details": str(e),
                }
            ),
            500,
        )


# Endpoint to Get UserLogs by Date
@datalog_bp.route("/logs/date", methods=["GET"])
@jwt_required()
def get_user_logs_by_date():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if not user:
        return jsonify({"message": "User not found"}), 404

    # Extract date from query parameters
    date_str = request.args.get("date", None)
    if not date_str:
        return jsonify({"message": "No date provided"}), 400

    try:
        # Assuming the date is in the format YYYY-MM-DD
        log_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format, expected YYYY-MM-DD"}), 400

    # Fetch logs for the given date
    user_logs = UserLog.query.filter(
        UserLog.user_id == user.id, db.func.date(UserLog.log_time) == log_date
    ).all()

    logs_data = []
    for log in user_logs:
        log_data = {
            "log_id": log.id,
            "log_time": log.log_time,
            "prodromes": [
                {"id": prod.prodrome_id, "intensity": prod.intensity}
                for prod in log.prodromes
            ],
            "auras": [
                {"id": aura.aura_id, "is_present": aura.is_present}
                for aura in log.auras
            ],
            "triggers": [
                {
                    "id": trigger.trigger_id,
                    "value_numeric": trigger.value_numeric,
                    "value_boolean": trigger.value_boolean,
                }
                for trigger in log.triggers
            ],
            "seizure_episodes": [
                {
                    "id": seizure.id,
                    "seizure_type_id": seizure.seizure_type_id,
                    "duration_sec": seizure.duration_sec,
                    "frequency": seizure.frequency,
                    "requires_emergency_intervention": seizure.requires_emergency_intervention,
                    "note": seizure.note,
                    "postictal_confusion_duration": seizure.postictal_confusion_duration,
                    "postictal_confusion_intensity": seizure.postictal_confusion_intensity,
                    "postictal_headache_duration": seizure.postictal_headache_duration,
                    "postictal_headache_intensity": seizure.postictal_headache_intensity,
                    "postictal_fatigue_duration": seizure.postictal_fatigue_duration,
                    "postictal_fatigue_intensity": seizure.postictal_fatigue_intensity,
                }
                for seizure in log.seizures
            ],
        }
        logs_data.append(log_data)

    return jsonify(logs_data), 200


# Helper function to process triggers
def process_triggers(triggers):
    trigger_descriptions = []
    for user_trigger in triggers:
        # Directly use attributes from UserTrigger instance
        if (
            user_trigger.trigger.name == "Sleep Quality"
            and user_trigger.value_numeric <= 5
        ):
            trigger_descriptions.append("Poor Sleep")
        elif (
            user_trigger.trigger.name == "Stress Level"
            and user_trigger.value_numeric >= 6
        ):
            trigger_descriptions.append("Stress")
        elif (
            user_trigger.trigger.name == "Sleep Duration"
            and user_trigger.value_numeric <= 6
        ):
            trigger_descriptions.append("Lack of Sleep")
        elif user_trigger.trigger.name == "Caffeine" and user_trigger.value_boolean:
            trigger_descriptions.append("Caffeine")
        elif user_trigger.trigger.name == "Alcohol" and user_trigger.value_boolean:
            trigger_descriptions.append("Alcohol")
        elif user_trigger.trigger.name == "Smoking" and user_trigger.value_boolean:
            trigger_descriptions.append("Smoking")
        elif user_trigger.trigger.name == "Drugs" and user_trigger.value_boolean:
            trigger_descriptions.append("Drugs")
        elif user_trigger.trigger.name == "Menstruation" and user_trigger.value_boolean:
            trigger_descriptions.append("Menstruation")
        elif user_trigger.trigger.name == "Skipped Meal" and user_trigger.value_boolean:
            trigger_descriptions.append("Skipped Meal")
        elif user_trigger.trigger.name == "Fever" and user_trigger.value_boolean:
            trigger_descriptions.append("Fever")
        elif (
            user_trigger.trigger.name == "Physical Exertion"
            and user_trigger.value_numeric >= 5
        ):
            trigger_descriptions.append("Physical Exertion")
        elif (
            user_trigger.trigger.name == "Flashing Lights"
            and user_trigger.value_boolean
        ):
            trigger_descriptions.append("Flashing Lights")
        elif (
            user_trigger.trigger.name == "Skipped Medication"
            and user_trigger.value_boolean
        ):
            trigger_descriptions.append("Skipped Medication")
        elif (
            user_trigger.trigger.name == "Change in Medication"
            and user_trigger.value_boolean
        ):
            trigger_descriptions.append("Change in Medication")
    return trigger_descriptions


# Helper function to format postictal symptoms
def format_postictal_symptoms(seizure):
    symptoms = []
    # Check if postictal_confusion_duration is not None and greater than 2
    if (
        seizure.postictal_confusion_duration
        and seizure.postictal_confusion_duration > 2
    ):
        intensity = (
            seizure.postictal_confusion_intensity
            if seizure.postictal_confusion_intensity
            else 0
        )
        symptoms.append(
            f"{intensity}/10 confusion for {seizure.postictal_confusion_duration} minutes"
        )

    # Check if postictal_headache_duration is not None and greater than 2
    if seizure.postictal_headache_duration and seizure.postictal_headache_duration > 2:
        intensity = (
            seizure.postictal_headache_intensity
            if seizure.postictal_headache_intensity
            else 0
        )
        symptoms.append(
            f"{intensity}/10 headache for {seizure.postictal_headache_duration} minutes"
        )

    # Check if postictal_fatigue_duration is not None and greater than 2
    if seizure.postictal_fatigue_duration and seizure.postictal_fatigue_duration > 2:
        intensity = (
            seizure.postictal_fatigue_intensity
            if seizure.postictal_fatigue_intensity
            else 0
        )
        symptoms.append(
            f"{intensity}/10 fatigue for {seizure.postictal_fatigue_duration} minutes"
        )

    # Join all symptoms into a single string, or note absence of significant symptoms
    return ", ".join(symptoms) if symptoms else "No significant postictal symptoms"


@datalog_bp.route("/weekly-logs", methods=["GET"])
@jwt_required()
def get_weekly_logs():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    one_week_ago = datetime.utcnow() - timedelta(days=7)
    user_logs = (
        UserLog.query.filter(
            UserLog.user_id == user.id, UserLog.log_time >= one_week_ago
        )
        .order_by(UserLog.log_time.desc())
        .all()
    )

    formatted_logs = []
    for log in user_logs:
        log_entry = {
            "date": log.log_time.strftime("%Y-%m-%d"),
            "triggers": process_triggers(log.triggers),
            "prodromes": [
                prod.prodrome.name for prod in log.prodromes if prod.intensity > 2
            ],
            "auras": [aura.aura.name for aura in log.auras if aura.is_present],
            "notes": log.note if log.note else "",
            "seizure": [],
        }

        # Add seizure information if any
        for seizure in log.seizures:
            seizure_details = {
                "type": seizure.seizure_type.name,
                "duration": seizure.duration_sec,
                "frequency": seizure.frequency,
                "emergencyIntervention": seizure.requires_emergency_intervention,
                "postictalSymptoms": format_postictal_symptoms(seizure),
                "note": seizure.note,
            }
            log_entry["seizure"].append(seizure_details)

        formatted_logs.append(log_entry)

    return jsonify(formatted_logs), 200
