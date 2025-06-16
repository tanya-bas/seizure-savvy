import numpy as np
from tensorflow.keras.models import load_model
from .dailylog import get_user_logs_by_date
from api.app import app
from datetime import datetime
from flask import jsonify, request

# Load the LSTM model outside of the endpoint
lstm_model_loaded = load_model("lstm_model.h5")


def fetch_logs_for_today():
    # Get today's date
    today_date = datetime.now().strftime("%Y-%m-%d")

    # Call the imported function with today's date
    logs_response, status_code = get_user_logs_by_date(today_date)

    # Check the status code
    if status_code == 200:
        # If status code is 200, return the logs data
        return logs_response
    else:
        # If status code is not 200, return an error response
        return jsonify({"error": logs_response}), status_code


def prepare_data_for_lstm(logs_data):
    # Initialize lists to store triggers and prodromes data
    triggers_data = []
    prodromes_data = []

    # Iterate over each log
    for log in logs_data:
        # Extract triggers data
        for trigger in log["triggers"]:
            # Assuming triggers can be either numeric or boolean
            if "value_numeric" in trigger:
                triggers_data.append(
                    [
                        trigger["value_numeric"],
                        0,  # For boolean value (not present in this case)
                    ]
                )
            elif "value_boolean" in trigger:
                triggers_data.append(
                    [
                        0,  # For numeric value (not present in this case)
                        int(trigger["value_boolean"]),
                    ]
                )

        # Extract prodromes data
        for prodrome in log["prodromes"]:
            prodromes_data.append(prodrome["intensity"])

    # Convert lists to numpy arrays
    triggers_data = np.array(triggers_data)
    prodromes_data = np.array(prodromes_data)

    # Combine triggers and prodromes data into one array
    combined_data = np.concatenate((triggers_data, prodromes_data), axis=1)
    reshaped_data = combined_data.reshape((1, 1, combined_data.shape[0]))

    return reshaped_data


# API endpoint for LSTM model output
@app.route("/api/predictions_lstm", methods=["GET"])
def get_lstm_predictions():
    # Fetch logs for today
    logs_data = fetch_logs_for_today()

    # Prepare data for LSTM model
    model_input = prepare_data_for_lstm(logs_data)

    # Make predictions using the loaded LSTM model
    prediction_lstm = lstm_model_loaded.predict(model_input)
    prediction_lstm_float = float(prediction_lstm)

    # Return the predictions
    return jsonify({"prediction_lstm": prediction_lstm_float})
