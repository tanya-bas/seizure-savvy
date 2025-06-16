from datetime import datetime, timedelta

import pytest
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from api.app.schema import User, Medication


class TestAddMedication:
    """Test suite for adding a new medication. POST /api/medications/"""

    def test_add_medication(self, authenticated_client: FlaskClient, sample_user: User):
        """Test adding a new medication to the user's list."""
        med_data = {
            "name": "NewMed",
            "dosage_mg": 250,
            "frequency": 1,
            "start_date": "2023-01-01",
            "first_dose": "08:00",
            "end_date": None,
            "reason_for_stop": "",
            "is_stopped": False,
        }
        response = authenticated_client.post("/api/medications/", json=med_data)
        assert response.status_code == 201
        assert "success" in response.json["message"].lower()

        # Extra assertions to verify that the medication is added correctly
        # Fetch the newly added medication to verify all fields were saved correctly
        med_id = response.json["id"]
        medication = Medication.query.get(med_id)
        assert medication.name == "NewMed"
        assert medication.dosage_mg == 250
        assert medication.frequency == 1
        assert medication.first_dose.strftime("%H:%M") == "08:00"
        assert medication.start_date.strftime("%Y-%m-%d") == "2023-01-01"
        assert medication.end_date is None
        assert medication.reason_for_stop == ""
        assert not medication.is_stopped


class TestGetMedications:
    """Test suite for fetching medications. GET /api/medications/"""

    def test_get_medications_empty(
        self, authenticated_client: FlaskClient, sample_user: User
    ):
        """Test fetching medications for a user with no medications."""
        response = authenticated_client.get("/api/medications/")
        assert response.status_code == 404
        assert "No medications" in response.json["message"]

    def test_get_medications_success(
        self,
        authenticated_client: FlaskClient,
        sample_user: User,
        sample_medication: Medication,
    ):
        """Test fetching medications successfully with correct pagination."""
        response = authenticated_client.get("/api/medications/")
        assert response.status_code == 200
        assert "data" in response.json
        assert "pagination" in response.json
        assert response.json["pagination"]["total_items"] == 1


class TestUpdateMedication:
    """Test suite for updating a medication. PUT /api/medications/<med_id>"""

    def test_update_medication(
        self,
        authenticated_client: FlaskClient,
        sample_user: User,
        sample_medication: Medication,
    ):
        """Test updating an existing medication."""
        updates = {
            "dosage_mg": 1000,
            "first_dose": "09:00",
            "end_date": "2023-12-31",
            "reason_for_stop": "Completed course",
            "is_stopped": True,
        }
        response = authenticated_client.put(
            f"/api/medications/{sample_medication.id}", json=updates
        )
        assert response.status_code == 200
        # Fetch updated data to verify
        updated_med = Medication.query.get(sample_medication.id)
        assert updated_med.dosage_mg == 1000
        assert updated_med.first_dose.strftime("%H:%M") == "09:00"
        assert updated_med.end_date.strftime("%Y-%m-%d") == "2023-12-31"
        assert updated_med.reason_for_stop == "Completed course"
        assert updated_med.is_stopped is True


class TestDeleteMedication:
    """Test suite for deleting a medication. DELETE /api/medications/<med_id>"""

    def test_delete_medication_success(
        self,
        authenticated_client: FlaskClient,
        sample_user: User,
        sample_medication: Medication,
    ):
        """Test deleting an existing medication."""
        response = authenticated_client.delete(
            f"/api/medications/{sample_medication.id}"
        )
        assert response.status_code == 204
        assert response.data == b""


class TestStopMedication:
    """Tests for stopping a medication using PUT on the medication stop endpoint."""

    def test_stop_medication_success(
        self,
        authenticated_client: FlaskClient,
        sample_user: User,
        sample_medication: Medication,
    ):
        """Ensure stopping a medication updates the database correctly."""
        stop_date = datetime.now().strftime("%Y-%m-%d")
        response = authenticated_client.put(
            f"/api/medications/{sample_medication.id}/stop",
            json={"reason_for_stop": "No longer needed", "end_date": stop_date},
        )
        assert response.status_code == 200
        assert "stopped successfully" in response.json["message"].lower()

        # Verify that the medication was updated
        updated_med = Medication.query.get(sample_medication.id)
        assert updated_med.is_stopped == True
        assert updated_med.reason_for_stop == "No longer needed"
        assert updated_med.end_date.strftime("%Y-%m-%d") == stop_date

    def test_stop_medication_already_stopped(
        self,
        authenticated_client: FlaskClient,
        sample_user: User,
        sample_medication: Medication,
        db_session: Session,
    ):
        """Check handling for already stopped medications."""
        # Setup: stop the medication first
        sample_medication.is_stopped = True
        sample_medication.reason_for_stop = "Already stopped"
        sample_medication.end_date = datetime.now().date()
        db_session.commit()

        # Attempt to stop again
        response = authenticated_client.put(
            f"/api/medications/{sample_medication.id}/stop",
            json={
                "reason_for_stop": "Try again",
                "end_date": datetime.now().strftime("%Y-%m-%d"),
            },
        )
        assert response.status_code == 400
        assert "already stopped" in response.json["message"].lower()

    def test_stop_medication_not_found(self, authenticated_client: FlaskClient):
        """Ensure proper handling when the medication does not exist."""
        response = authenticated_client.put(
            "/api/medications/999999/stop",
            json={"reason_for_stop": "Not applicable", "end_date": "2023-05-01"},
        )
        assert response.status_code == 404
        assert "not found" in response.json["message"].lower()

    def test_stop_medication_invalid_data(
        self, authenticated_client: FlaskClient, sample_medication: Medication
    ):
        """Validate response for incorrect data formats."""
        response = authenticated_client.put(
            f"/api/medications/{sample_medication.id}/stop",
            json={"reason_for_stop": "Needed", "end_date": "invalid-date"},
        )
        assert response.status_code == 400
        assert "invalid date format" in response.json["message"].lower()
