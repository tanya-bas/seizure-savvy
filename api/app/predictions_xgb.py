# predictions_xgb.py
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, func, case
from . import db
from flask import jsonify, request, abort
import xgboost as xgb
from api.app import app
from .schema import UserLog, UserProdrome, UserTrigger, SeizureEpisode


# Load the XGBoost model
model_xgb = xgb.XGBClassifier()
model_xgb.load_model("xgboost_model.json")


@app.route("/api/predictions/xgboost", methods=["GET"])
def get_xgboost_predictions():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            abort(400, "User ID is required.")

        # Prepare data for XGBoost model
        model_input = prepare_data_for_xgboost(user_id)

        # Retrain the XGBoost model using all user data
        fine_tune_xgboost_model(model_xgb, *model_input)

        # Get the list of most relevant features from the retrained model
        feature_importance = get_feature_importance(model_xgb)

        # Return the list of most relevant features
        return jsonify({"feature_importance": feature_importance})
    except Exception as e:
        abort(500, str(e))


def prepare_data_for_xgboost(user_id):
    # Connect to the database
    engine = db.engine
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query user data including prodromes, triggers, and seizure occurrences for the specified user
    user_data = (
        session.query(
            UserProdrome.log_id,
            UserProdrome.prodrome_id,
            UserProdrome.intensity,
            UserTrigger.trigger_id,
            UserTrigger.value_boolean,
            UserTrigger.value_numeric,
            func.exists()
            .where(SeizureEpisode.log_id == UserProdrome.log_id)
            .label("has_seizures"),
        )
        .join(UserProdrome.log)
        .outerjoin(UserTrigger, UserProdrome.log_id == UserTrigger.log_id)
        .filter(UserLog.user_id == user_id)
        .group_by(UserProdrome.log_id)
        .all()
    )

    # Close the session
    session.close()

    # Create lists to store features (X_train) and target variable (y_train)
    X_train = []
    y_train = []

    # Iterate over the query results
    for (
        log_id,
        prodrome_id,
        intensity,
        trigger_id,
        value_boolean,
        value_numeric,
        has_seizures,
    ) in user_data:
        # Store features in a list
        features = []

        # Store prodrome intensity if available
        if prodrome_id is not None:
            features.append(intensity)

        # Store trigger value if available
        if trigger_id is not None:
            # Check if the trigger value is boolean or numeric
            if value_boolean is not None:
                features.append(value_boolean)
            elif value_numeric is not None:
                features.append(value_numeric)

        # Append features to X_train
        X_train.append(features)

        # Append seizure occurrence to y_train
        y_train.append(has_seizures)

    return X_train, y_train


def fine_tune_xgboost_model(model_xgb, user_x_train, user_y_train):
    # Retrain the XGBoost model using all user data
    model_xgb.partial_fit(user_x_train, user_y_train)


def get_feature_importance(model_xgb):
    # Get the list of most relevant features from the XGBoost model
    booster = model_xgb.get_booster()
    feature_importance = booster.get_score(importance_type="weight")
    features_list = list(feature_importance.keys())

    return features_list[:5]
