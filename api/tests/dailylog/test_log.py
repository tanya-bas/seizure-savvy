# api/tests/dailylog/test_log.py
import pytest
from api.app.schema import (
    UserLog,
    Prodrome,
    UserProdrome,
    Aura,
    UserAura,
    Trigger,
    UserTrigger,
    SeizureType,
    SeizureEpisode,
)
from flask_jwt_extended import create_access_token
from datetime import datetime, timedelta
from sqlalchemy.orm import Session


class TestCreateUserProdrome:
    def test_route_accessibility(self, authenticated_client):
        response = authenticated_client.get("/api/datalog/user-prodromes")
        assert response.status_code != 404, "Route is not accessible"

    def test_create_user_prodrome_success(
        self, authenticated_client, sample_user, sample_log, sample_prodrome
    ):

        # Check if log and prodrome exist in the database
        log_exists = UserLog.query.get(sample_log.id) is not None
        prodrome_exists = Prodrome.query.get(sample_prodrome.id) is not None
        print(f"Log exists: {log_exists}, Prodrome exists: {prodrome_exists}")

        prodrome_data = {
            "log_id": sample_log.id,
            "prodrome_id": sample_prodrome.id,
            "intensity": 5,
            "note": "Test note",
        }
        response = authenticated_client.post(
            "/api/datalog/user-prodromes", json=prodrome_data
        )

        print("Response:", response.data)
        assert response.status_code == 201
        assert "UserProdrome created successfully" in response.json["message"]

    def test_create_user_prodrome_missing_data(
        self, authenticated_client, sample_user, sample_prodrome
    ):
        prodrome_data = {
            "log_id": sample_prodrome.id,
            "prodrome_id": sample_prodrome.id,
            # 'intensity' is missing
        }
        response = authenticated_client.post(
            "/api/datalog/user-prodromes", json=prodrome_data
        )
        assert response.status_code == 400
        assert "Missing" in response.json["message"]

    def test_create_user_prodrome_not_found(self, authenticated_client, sample_user):
        prodrome_data = {
            "log_id": 99999,  # Assuming this ID does not exist
            "prodrome_id": 99999,  # Assuming this ID does not exist
            "intensity": 5,
        }
        response = authenticated_client.post(
            "/api/datalog/user-prodromes", json=prodrome_data
        )
        assert response.status_code == 404
        assert "not found" in response.json["message"].lower()


class TestCreateUserAura:
    def test_create_user_aura_success(
        self, authenticated_client, sample_user, sample_log, sample_aura
    ):
        aura_data = {
            "log_id": sample_log.id,
            "aura_id": sample_aura.id,
            "is_present": True,
            "note": "Test note about aura",
        }
        response = authenticated_client.post("/api/datalog/user-auras", json=aura_data)
        assert response.status_code == 201
        assert "UserAura created successfully" in response.json["message"]

    def test_create_user_aura_missing_data(
        self, authenticated_client, sample_user, sample_log
    ):
        aura_data = {"log_id": sample_log.id, "is_present": True}  # missing aura_id
        response = authenticated_client.post("/api/datalog/user-auras", json=aura_data)
        assert response.status_code == 400
        assert "Missing" in response.json["message"]

    def test_create_user_aura_not_found(self, authenticated_client, sample_user):
        aura_data = {
            "log_id": 999,  # Non-existent log ID
            "aura_id": 999,  # Non-existent aura ID
            "is_present": True,
        }
        response = authenticated_client.post("/api/datalog/user-auras", json=aura_data)
        assert response.status_code == 404
        assert "not found" in response.json["message"]

    def test_create_user_aura_unauthorized(self, client, sample_log, sample_aura):
        # Assuming there's no logged-in user
        aura_data = {
            "log_id": sample_log.id,
            "aura_id": sample_aura.id,
            "is_present": True,
            "note": "Unauthorized test note",
        }
        response = client.post("/api/datalog/user-auras", json=aura_data)
        assert response.status_code == 401  # Unauthorized status code


class TestCreateUserTrigger:
    def test_create_user_trigger_success(
        self, authenticated_client, sample_user, sample_log, sample_trigger
    ):
        trigger_data = {
            "log_id": sample_log.id,
            "trigger_id": sample_trigger.id,
            "value_numeric": 5.5,
            "value_boolean": True,
            "note": "Trigger test note",
        }
        response = authenticated_client.post(
            "/api/datalog/user-triggers", json=trigger_data
        )
        assert response.status_code == 201
        assert "UserTrigger created successfully" in response.json["message"]

    def test_create_user_trigger_missing_data(
        self, authenticated_client, sample_user, sample_log
    ):
        trigger_data = {
            "log_id": sample_log.id,
            # Missing trigger_id and values
        }
        response = authenticated_client.post(
            "/api/datalog/user-triggers", json=trigger_data
        )
        assert response.status_code == 400
        assert "Missing" in response.json["message"]

    def test_create_user_trigger_not_found(self, authenticated_client, sample_user):
        trigger_data = {
            "log_id": 999,  # Non-existent log ID
            "trigger_id": 999,  # Non-existent trigger ID
            "value_numeric": 5.5,
            "value_boolean": True,
        }
        response = authenticated_client.post(
            "/api/datalog/user-triggers", json=trigger_data
        )
        assert response.status_code == 404
        assert "not found" in response.json["message"]

    def test_create_user_trigger_unauthorized(self, client, sample_log, sample_trigger):
        # Assuming there's no logged-in user
        trigger_data = {
            "log_id": sample_log.id,
            "trigger_id": sample_trigger.id,
            "value_numeric": 5.5,
            "value_boolean": True,
            "note": "Unauthorized test note",
        }
        response = client.post("/api/datalog/user-triggers", json=trigger_data)
        assert response.status_code == 401  # Unauthorized status code


class TestCreateSeizureEpisode:
    def test_create_seizure_episode_success(
        self, authenticated_client, sample_user, sample_log, sample_seizure_type
    ):
        episode_data = {
            "log_id": sample_log.id,
            "seizure_type_id": sample_seizure_type.id,
            "duration_sec": 120,
            "frequency": 2,
            "requires_emergency_intervention": True,
            "note": "Severe episode",
            "postictal_confusion_duration": 30,
            "postictal_confusion_intensity": 7,
            "postictal_headache_duration": 45,
            "postictal_headache_intensity": 5,
            "postictal_fatigue_duration": 60,
            "postictal_fatigue_intensity": 6,
        }
        response = authenticated_client.post(
            "/api/datalog/seizure-episodes", json=episode_data
        )
        assert response.status_code == 201
        assert "SeizureEpisode created successfully" in response.json["message"]

    def test_create_seizure_episode_missing_data(
        self, authenticated_client, sample_user, sample_seizure_type
    ):
        episode_data = {
            # Missing duration_sec
            "log_id": sample_seizure_type.id,
            "seizure_type_id": sample_seizure_type.id,
            # 'duration_sec' is intentionally missing to test error handling
        }
        response = authenticated_client.post(
            "/api/datalog/seizure-episodes", json=episode_data
        )
        assert response.status_code == 400
        assert (
            "Missing log_id, seizure_type_id, or duration_sec"
            in response.json["message"]
        )

    def test_create_seizure_episode_not_found(self, authenticated_client, sample_user):
        episode_data = {
            "log_id": 999,  # Non-existing log
            "seizure_type_id": 999,  # Non-existing type
            "duration_sec": 60,
        }
        response = authenticated_client.post(
            "/api/datalog/seizure-episodes", json=episode_data
        )
        assert response.status_code == 404
        assert "not found" in response.json["message"]

    def test_create_seizure_episode_unauthorized(
        self, client, sample_log, sample_seizure_type
    ):
        # No logged-in user scenario
        episode_data = {
            "log_id": sample_log.id,
            "seizure_type_id": sample_seizure_type.id,
            "duration_sec": 150,
        }
        response = client.post("/api/datalog/seizure-episodes", json=episode_data)
        assert response.status_code == 401  # Unauthorized status code


@pytest.mark.usefixtures("client", "db_session")
class TestUpdateUserProdrome:
    def test_update_user_prodrome_not_found_user(self, client, sample_user):
        """Test updating a user prodrome when the user does not exist."""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        response = client.put(
            "/api/datalog/user-prodromes/1",
            json={"intensity": 5, "note": "Updated note"},
        )
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]

    def test_update_user_prodrome_not_found_prodrome(
        self, authenticated_client, sample_user
    ):
        """Test updating a non-existent user prodrome."""
        response = authenticated_client.put(
            "/api/datalog/user-prodromes/999",
            json={"intensity": 5, "note": "Updated note"},
        )
        assert response.status_code == 404
        assert (
            "UserProdrome not found or access denied" in response.get_json()["message"]
        )

    def test_update_user_prodrome_access_denied(
        self, authenticated_client, add_user_prodrome, another_user_log
    ):
        """Test updating a user prodrome not for the authenticated user."""
        # Setup a UserProdrome linked to a log of another user
        user_prodrome = add_user_prodrome(log=another_user_log)
        update_data = {"intensity": 7, "note": "Updated note"}

        # Try to update this user_prodrome
        response = authenticated_client.put(
            f"/api/datalog/user-prodromes/{user_prodrome.id}", json=update_data
        )
        assert response.status_code == 404
        assert "access denied" in response.json["message"].lower()

    def test_update_user_prodrome_success(
        self, authenticated_client, sample_user, sample_log, add_user_prodrome
    ):
        """Test successfully updating a user prodrome."""
        user_prodrome = add_user_prodrome()
        response = authenticated_client.put(
            f"/api/datalog/user-prodromes/{user_prodrome.id}",
            json={"intensity": 10, "note": "New note"},
        )
        assert response.status_code == 200
        assert "UserProdrome updated successfully" in response.get_json()["message"]
        # Verify changes were made
        updated_prodrome = UserProdrome.query.get(user_prodrome.id)
        assert updated_prodrome.intensity == 10
        assert updated_prodrome.note == "New note"


class TestUpdateUserAura:
    def test_user_not_found(self, client):
        """User not found."""
        # Setup client with a valid token but a non-existing user ID for aura
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + create_access_token(
            identity="nonexistentuser@example.com"
        )
        response = client.put(
            "/api/datalog/user-auras/1",
            json={"is_present": True, "note": "Updated Note"},
        )
        assert (
            response.status_code == 404
        ), "Expected 404 for non-existing user but got {}".format(response.status_code)

    def test_user_aura_not_found(self, authenticated_client):
        """UserAura not found."""
        response = authenticated_client.put(
            "/api/datalog/user-auras/999",
            json={"is_present": True, "note": "Updated Note"},
        )
        assert response.status_code == 404
        assert "UserAura not found" in response.get_json()["message"]

    def test_access_denied(
        self, authenticated_client, add_user_aura, another_user_log, sample_user
    ):
        """Access to UserAura denied because it belongs to another user."""
        # Setup a UserAura linked to a log of another user
        user_aura = add_user_aura(log=another_user_log)
        # Authenticate as the original sample_user
        authenticated_client.environ_base["HTTP_AUTHORIZATION"] = (
            "Bearer " + create_access_token(identity=sample_user.email)
        )
        response = authenticated_client.put(
            f"/api/datalog/user-auras/{user_aura.id}",
            json={"is_present": False, "note": "Should Fail"},
        )

        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_valid_update(self, authenticated_client, add_user_aura):
        """Valid update of UserAura."""
        user_aura = add_user_aura()
        response = authenticated_client.put(
            f"/api/datalog/user-auras/{user_aura.id}",
            json={"is_present": False, "note": "New Note"},
        )
        assert response.status_code == 200
        assert "updated successfully" in response.get_json()["message"].lower()

    def test_partial_update(self, authenticated_client, add_user_aura):
        """Partial update of UserAura, only updating the note."""
        user_aura = add_user_aura()
        response = authenticated_client.put(
            f"/api/datalog/user-auras/{user_aura.id}",
            json={"note": "Partially Updated Note"},
        )
        assert response.status_code == 200
        assert "updated successfully" in response.get_json()["message"].lower()


class TestUpdateUserTrigger:
    def test_trigger_not_found(self, authenticated_client):
        """Ensure appropriate error is returned when trigger does not exist."""
        response = authenticated_client.put(
            "/api/datalog/user-triggers/999",
            json={"value_numeric": 20, "value_boolean": False, "note": "Updated note"},
        )
        assert response.status_code == 404
        assert (
            "UserTrigger not found or access denied" in response.get_json()["message"]
        )

    def test_access_denied(
        self, authenticated_client, add_user_trigger, another_user_log
    ):
        """Test updating a trigger does not belong to authenticated user."""
        # This log belongs to another user
        user_trigger = add_user_trigger(log=another_user_log)
        response = authenticated_client.put(
            f"/api/datalog/user-triggers/{user_trigger.id}",
            json={
                "value_numeric": 20,
                "value_boolean": False,
                "note": "Should not update",
            },
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_successful_update(self, authenticated_client, add_user_trigger):
        """Test a successful trigger update."""
        user_trigger = add_user_trigger()
        response = authenticated_client.put(
            f"/api/datalog/user-triggers/{user_trigger.id}",
            json={
                "value_numeric": 15,
                "value_boolean": True,
                "note": "Successfully updated",
            },
        )
        assert response.status_code == 200
        assert "UserTrigger updated successfully" in response.get_json()["message"]
        # Optionally check if the data was actually updated in the database
        assert user_trigger.value_numeric == 15
        assert user_trigger.value_boolean is True
        assert user_trigger.note == "Successfully updated"

    def test_partial_data_update(self, authenticated_client, add_user_trigger):
        """Test updating the trigger with partial data (only numeric value)."""
        user_trigger = add_user_trigger()
        response = authenticated_client.put(
            f"/api/datalog/user-triggers/{user_trigger.id}", json={"value_numeric": 5}
        )
        assert response.status_code == 200
        assert user_trigger.value_numeric == 5  # Confirm the value was updated
        assert "updated successfully" in response.get_json()["message"].lower()


class TestUpdateSeizureEpisode:
    def test_user_not_found(self, client):
        """Ensure it returns 404 if user not found."""
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + create_access_token(
            identity="nonexistent@example.com"
        )
        response = client.put(
            "/api/datalog/seizure-episodes/1", json={"note": "Updated"}
        )
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]

    def test_seizure_episode_not_found_or_access_denied(
        self, authenticated_client, add_seizure_episode, another_user_log
    ):
        """Test access denied when seizure episode does not belong to user."""
        # Belongs to another user
        episode = add_seizure_episode(log=another_user_log)
        response = authenticated_client.put(
            f"/api/datalog/seizure-episodes/{episode.id}", json={"note": "Should fail"}
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_successful_update(self, authenticated_client, add_seizure_episode):
        """Test successful update of a seizure episode."""
        episode = add_seizure_episode()
        update_data = {
            "frequency": 2,
            "note": "Updated note",
            "postictal_headache_duration": 30,
        }
        response = authenticated_client.put(
            f"/api/datalog/seizure-episodes/{episode.id}", json=update_data
        )
        assert response.status_code == 200
        assert "updated successfully" in response.get_json()["message"].lower()
        # Fetch again to confirm updates
        updated_episode = SeizureEpisode.query.get(episode.id)
        assert updated_episode.frequency == 2
        assert updated_episode.note == "Updated note"
        assert updated_episode.postictal_headache_duration == 30

    def test_partial_update(self, authenticated_client, add_seizure_episode):
        """Test partial update works."""
        episode = add_seizure_episode()
        partial_update = {"note": "Partially updated note"}
        response = authenticated_client.put(
            f"/api/datalog/seizure-episodes/{episode.id}", json=partial_update
        )
        assert response.status_code == 200
        assert "updated successfully" in response.get_json()["message"].lower()
        # Confirm the update
        updated_episode = SeizureEpisode.query.get(episode.id)
        assert updated_episode.note == "Partially updated note"


class TestDeleteUserProdrome:
    def test_user_prodrome_deletion_success(
        self, authenticated_client, add_user_prodrome
    ):
        """Test successful deletion of a user prodrome entry"""
        user_prodrome = add_user_prodrome()
        response = authenticated_client.delete(
            f"/api/datalog/user-prodromes/{user_prodrome.id}"
        )
        assert response.status_code == 200
        assert "UserProdrome deleted successfully" in response.get_json()["message"]

        # Verify that the UserProdrome is actually deleted from the database
        assert UserProdrome.query.get(user_prodrome.id) is None

    def test_user_prodrome_deletion_unauthorized(
        self, client, sample_user, add_user_prodrome
    ):
        """Test deletion attempt without authentication"""
        user_prodrome = add_user_prodrome()
        response = client.delete(f"/api/datalog/user-prodromes/{user_prodrome.id}")
        assert response.status_code == 401  # Unauthorized access

    def test_user_prodrome_deletion_not_found(self, authenticated_client):
        """Test response for a non-existent user prodrome"""
        response = authenticated_client.delete(
            "/api/datalog/user-prodromes/99999"
        )  # Assuming ID does not exist
        assert response.status_code == 404
        assert (
            "UserProdrome not found or access denied" in response.get_json()["message"]
        )

    def test_user_prodrome_deletion_wrong_user(
        self, authenticated_client, add_user_prodrome, another_user_log
    ):
        """Test deletion of a userprodrome not for authenticated user"""
        # Create a user prodrome that belongs to another user
        user_prodrome = add_user_prodrome(log=another_user_log)
        response = authenticated_client.delete(
            f"/api/datalog/user-prodromes/{user_prodrome.id}"
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_user_prodrome_deletion_no_user_found(self, client):
        """Test deletion when the user does not exist in the database"""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        # Arbitrary ID
        response = client.delete("/api/datalog/user-prodromes/1")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]


class TestDeleteUserAura:
    def test_user_aura_deletion_success(self, authenticated_client, add_user_aura):
        """Test successful deletion of a user aura entry"""
        user_aura = add_user_aura()
        response = authenticated_client.delete(
            f"/api/datalog/user-auras/{user_aura.id}"
        )
        assert response.status_code == 200
        assert "UserAura deleted successfully" in response.get_json()["message"]

        # Verify that the UserAura is actually deleted from the database
        assert UserAura.query.get(user_aura.id) is None

    def test_user_aura_deletion_unauthorized(self, client, sample_user, add_user_aura):
        """Test deletion attempt without authentication"""
        user_aura = add_user_aura()
        response = client.delete(f"/api/datalog/user-auras/{user_aura.id}")
        assert response.status_code == 401  # Unauthorized access

    def test_user_aura_deletion_not_found(self, authenticated_client):
        """Test response for a non-existent user aura"""
        response = authenticated_client.delete(
            "/api/datalog/user-auras/99999"
        )  # Assuming ID does not exist
        assert response.status_code == 404
        assert "UserAura not found or access denied" in response.get_json()["message"]

    def test_user_aura_deletion_wrong_user(
        self, authenticated_client, add_user_aura, another_user_log
    ):
        """Test deletion of a user aura not for authenticated user"""
        # Create a user aura that belongs to another user
        user_aura = add_user_aura(log=another_user_log)
        response = authenticated_client.delete(
            f"/api/datalog/user-auras/{user_aura.id}"
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_user_aura_deletion_no_user_found(self, client):
        """Test deletion when the user does not exist in the database"""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        response = client.delete("/api/datalog/user-auras/1")  # Arbitrary ID
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]


class TestDeleteUserTrigger:
    def test_user_trigger_deletion_success(
        self, authenticated_client, add_user_trigger
    ):
        """Test successful deletion of a user trigger entry"""
        user_trigger = add_user_trigger()
        response = authenticated_client.delete(
            f"/api/datalog/user-triggers/{user_trigger.id}"
        )
        assert response.status_code == 200
        assert "UserTrigger deleted successfully" in response.get_json()["message"]

        # Verify that the UserTrigger is actually deleted from the database
        assert UserTrigger.query.get(user_trigger.id) is None

    def test_user_trigger_deletion_unauthorized(
        self, client, sample_user, add_user_trigger
    ):
        """Test deletion attempt without authentication"""
        user_trigger = add_user_trigger()
        response = client.delete(f"/api/datalog/user-triggers/{user_trigger.id}")
        assert response.status_code == 401  # Unauthorized access

    def test_user_trigger_deletion_not_found(self, authenticated_client):
        """Test response for a non-existent user trigger"""
        response = authenticated_client.delete(
            "/api/datalog/user-triggers/99999"
        )  # Assuming ID does not exist
        assert response.status_code == 404
        assert (
            "UserTrigger not found or access denied" in response.get_json()["message"]
        )

    def test_user_trigger_deletion_wrong_user(
        self, authenticated_client, add_user_trigger, another_user_log
    ):
        """Test deletion of a user trigger not for authenticated user"""
        # Create a user trigger that belongs to another user
        user_trigger = add_user_trigger(log=another_user_log)
        response = authenticated_client.delete(
            f"/api/datalog/user-triggers/{user_trigger.id}"
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_user_trigger_deletion_no_user_found(self, client):
        """Test deletion when the user does not exist in the database"""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        # Arbitrary ID
        response = client.delete("/api/datalog/user-triggers/1")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]


class TestDeleteSeizureEpisode:
    def test_seizure_episode_deletion_success(
        self, authenticated_client, add_seizure_episode
    ):
        """Test successful deletion of a seizure episode entry"""
        seizure_episode = add_seizure_episode()
        response = authenticated_client.delete(
            f"/api/datalog/seizure-episodes/{seizure_episode.id}"
        )
        assert response.status_code == 200
        assert "SeizureEpisode deleted successfully" in response.get_json()["message"]

        # Verify that the SeizureEpisode is actually deleted from the database
        assert SeizureEpisode.query.get(seizure_episode.id) is None

    def test_seizure_episode_deletion_unauthorized(
        self, client, sample_user, add_seizure_episode
    ):
        """Test deletion attempt without authentication"""
        seizure_episode = add_seizure_episode()
        response = client.delete(f"/api/datalog/seizure-episodes/{seizure_episode.id}")
        assert response.status_code == 401  # Unauthorized access

    def test_seizure_episode_deletion_not_found(self, authenticated_client):
        """Test response for a non-existent seizure episode"""
        response = authenticated_client.delete(
            "/api/datalog/seizure-episodes/99999"
        )  # Assuming ID doesnot exist
        assert response.status_code == 404
        assert (
            "SeizureEpisode not found or access denied"
            in response.get_json()["message"]
        )

    def test_seizure_episode_deletion_wrong_user(
        self, authenticated_client, add_seizure_episode, another_user_log
    ):
        """Test deletion of a seizure episode not for authenticated user"""
        # Create a seizure episode that belongs to another user
        seizure_episode = add_seizure_episode(log=another_user_log)
        response = authenticated_client.delete(
            f"/api/datalog/seizure-episodes/{seizure_episode.id}"
        )
        assert response.status_code == 404
        assert "access denied" in response.get_json()["message"].lower()

    def test_seizure_episode_deletion_no_user_found(self, client):
        """Test deletion when the user does not exist in the database"""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        # Arbitrary ID
        response = client.delete("/api/datalog/seizure-episodes/1")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]


class TestGetUserLogs:
    def test_access_unauthenticated(self, client):
        """Test that the endpoint requires user authentication."""
        response = client.get("/api/datalog/logs")
        assert (
            response.status_code == 401
        ), "Access should be restricted to authenticated users"

    def test_user_not_found(self, client):
        """Ensure it returns 404 if user not found."""
        # Set the authorization header to a token for a non-existent user
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + create_access_token(
            identity="nonexistent@example.com"
        )
        response = client.get("/api/datalog/logs")
        assert (
            response.status_code == 404
        ), f"Expected 404 but got {response.status_code}. \
                Response: {response.data}"
        json_data = response.get_json()
        assert json_data is not None, "Response should contain JSON data"
        assert (
            json_data["message"] == "User not found"
        ), "Error message should be 'User not found'"

    def test_fetch_all_logs(
        self,
        authenticated_client,
        sample_user,
        sample_log,
        add_user_prodrome,
        add_user_aura,
        add_user_trigger,
        add_seizure_episode,
    ):
        """Test fetching all logs for authenticated user with details."""
        add_user_prodrome(log=sample_log)
        add_user_aura(log=sample_log)
        add_user_trigger(log=sample_log)
        add_seizure_episode(log=sample_log)

        response = authenticated_client.get("/api/datalog/logs")
        assert response.status_code == 200, "Should successfully fetch logs"
        assert len(response.get_json()) == 1, "Expected number of logs not found"

    def test_no_logs_for_user(self, authenticated_client, sample_user):
        """Test the case where there are no logs for the user."""
        response = authenticated_client.get("/api/datalog/logs")
        assert (
            response.status_code == 200
        ), "Expected successful response indicating no logs available"
        assert len(response.get_json()) == 0, "No logs should be present"

    def test_fetch_all_logs_with_details(
        self,
        authenticated_client,
        sample_user,
        sample_log,
        add_user_prodrome,
        add_user_aura,
        add_user_trigger,
        add_seizure_episode,
    ):
        """Test fetching all logs for the authenticated user with details."""
        # Setup additional data in the logs
        user_prodrome = add_user_prodrome(log=sample_log)
        user_aura = add_user_aura(log=sample_log)
        user_trigger = add_user_trigger(log=sample_log)
        seizure_episode = add_seizure_episode(log=sample_log)

        # Fetch logs
        response = authenticated_client.get("/api/datalog/logs")
        assert response.status_code == 200, "Should successfully fetch logs"

        # Convert response to JSON and validate structure
        logs_data = response.get_json()
        assert isinstance(logs_data, list), "Response should be a list of logs"
        assert len(logs_data) == 1, "There should be one log entry"

        log_entry = logs_data[0]
        assert (
            log_entry["log_id"] == sample_log.id
        ), "Log ID should match the sample log"

        # Check for prodromes, auras, triggers, and seizure episodes details
        assert "prodromes" in log_entry, "Prodromes should be included in the log data"
        assert (
            log_entry["prodromes"][0]["id"] == user_prodrome.prodrome_id
        ), "Prodrome ID should match"

        assert "auras" in log_entry, "Auras should be included in the log data"
        assert log_entry["auras"][0]["id"] == user_aura.aura_id, "Aura ID should match"

        assert "triggers" in log_entry, "Triggers should be included in the log data"
        assert (
            log_entry["triggers"][0]["id"] == user_trigger.trigger_id
        ), "Trigger ID should match"

        assert (
            "seizure_episodes" in log_entry
        ), "Seizure episodes should be included in the log data"
        assert (
            log_entry["seizure_episodes"][0]["id"] == seizure_episode.id
        ), "Seizure episode ID should match"


@pytest.mark.usefixtures("db_session")
class TestGetUserLogsByDate:
    @pytest.fixture
    def log_date(self):
        return datetime.strptime("2022-04-01", "%Y-%m-%d").date()

    def test_access_unauthenticated(self, client):
        """Test access without authentication should fail."""
        response = client.get("/api/datalog/logs/date?date=2022-04-01")
        assert response.status_code == 401

    def test_user_not_found(self, client):
        """Test response when user is not found."""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        response = client.get("/api/datalog/logs/date?date=2022-04-01")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]

    def test_missing_date_parameter(self, authenticated_client):
        """Test error returned when no date parameter is provided."""
        response = authenticated_client.get("/api/datalog/logs/date")
        assert response.status_code == 400
        assert "No date provided" in response.get_json()["message"]

    def test_invalid_date_format(self, authenticated_client):
        """Test error for invalid date format."""
        response = authenticated_client.get("/api/datalog/logs/date" "?date=04-01-2022")
        assert response.status_code == 400
        assert "Invalid date format" in response.get_json()["message"]

    def test_logs_filtering_by_date(
        self, authenticated_client, sample_user, log_date, db_session
    ):
        """Test only logs from specific date are returned."""
        # Create logs on two different dates
        log1 = UserLog(user_id=sample_user.id, log_time=datetime(2022, 4, 1))
        log2 = UserLog(user_id=sample_user.id, log_time=datetime(2022, 4, 2))
        db_session.add_all([log1, log2])
        db_session.commit()

        url = "/api/datalog/logs/date?date=2022-04-01"
        response = authenticated_client.get(url)
        assert response.status_code == 200
        logs = response.get_json()
        assert len(logs) == 1
        assert logs[0]["log_id"] == log1.id

    def test_response_structure(
        self,
        authenticated_client,
        sample_user,
        add_user_prodrome,
        add_user_aura,
        add_user_trigger,
        add_seizure_episode,
        log_date,
        db_session,
    ):
        """Test that response contains all detailed elements correctly."""
        log = UserLog(
            user_id=sample_user.id,
            log_time=datetime.combine(log_date, datetime.min.time()),
        )
        db_session.add(log)
        db_session.commit()

        # Add detailed data to the log
        add_user_prodrome(log=log)
        add_user_aura(log=log)
        add_user_trigger(log=log)
        add_seizure_episode(log=log)

        url = f'/api/datalog/logs/date?date={log_date.strftime("%Y-%m-%d")}'
        response = authenticated_client.get(url)
        assert response.status_code == 200
        log_data = response.get_json()[0]
        assert "prodromes" in log_data
        assert "auras" in log_data
        assert "triggers" in log_data
        assert "seizure_episodes" in log_data


@pytest.mark.usefixtures("db_session")
class TestWeeklyLogs:
    def test_access_unauthenticated(self, client):
        """Test access without authentication should fail."""
        response = client.get("/api/datalog/weekly-logs")
        assert response.status_code == 401, "Should require authentication"

    def test_user_not_found(self, client):
        """Test response when user is not found."""
        access_token = create_access_token(identity="nonexistent@example.com")
        client.environ_base["HTTP_AUTHORIZATION"] = "Bearer " + access_token
        response = client.get("/api/datalog/weekly-logs")
        assert response.status_code == 404
        assert "User not found" in response.get_json()["message"]

    def test_no_logs_for_user(self, authenticated_client, sample_user):
        """Test the case where there are no logs for the user within the last week."""
        response = authenticated_client.get("/api/datalog/weekly-logs")
        assert response.status_code == 200
        assert (
            len(response.get_json()) == 0
        ), "Should return an empty list when no logs are present"

    def test_logs_within_last_week(self, authenticated_client, sample_user, db_session):
        """Test only logs from the last week are returned."""
        # Create logs within and outside the 7-day window
        recent_log = UserLog(user_id=sample_user.id, log_time=datetime.now())
        older_log = UserLog(
            user_id=sample_user.id, log_time=datetime.now() - timedelta(days=8)
        )
        db_session.add_all([recent_log, older_log])
        db_session.commit()

        response = authenticated_client.get("/api/datalog/weekly-logs")
        logs = response.get_json()
        assert response.status_code == 200
        assert len(logs) == 1, "Should return only one log"
        assert logs[0]["date"] == recent_log.log_time.strftime(
            "%Y-%m-%d"
        ), "The log date should match the recent log"

    def test_logs_returned_with_details(
        self, authenticated_client, sample_user, db_session
    ):
        """Test that logs returned include detailed prodrome data."""
        log = UserLog(
            user_id=sample_user.id, log_time=datetime.now() - timedelta(days=1)
        )
        db_session.add(log)
        prodrome = UserProdrome(
            log=log,
            prodrome=Prodrome(name="Severe Headache"),
            intensity=3,
            note="Very painful",
        )
        db_session.add(prodrome)

        # Create a UserAura instance
        aura = UserAura(
            log=log,
            aura=Aura(name="Visual Disturbances"),
            is_present=True,
            note="Blurred vision",
        )
        db_session.add(aura)

        # Create a UserTrigger instance (example: Caffeine consumption)
        trigger = UserTrigger(
            log=log,
            trigger=Trigger(name="Caffeine"),
            value_boolean=True,
            note="Had coffee",
        )
        db_session.add(trigger)

        # Create a SeizureEpisode instance
        seizure_episode = SeizureEpisode(
            log=log,
            seizure_type=SeizureType(name="Generalized Tonic-Clonic"),
            duration_sec=90,
            frequency=1,
            note="Very intense",
            requires_emergency_intervention=False,
        )
        db_session.add(seizure_episode)

        # Commit changes to the database
        db_session.commit()

        response = authenticated_client.get("/api/datalog/weekly-logs")
        assert response.status_code == 200
        logs = response.get_json()

        # Assert that one log is returned
        assert len(logs) == 1

        # Assert on prodrome data
        assert len(logs[0]["prodromes"]) == 1
        assert logs[0]["prodromes"][0] == "Severe Headache"

        # Assert on aura data
        assert len(logs[0]["auras"]) == 1
        assert logs[0]["auras"][0] == "Visual Disturbances"

        # Assert on trigger data - checking for presence and correctness
        assert len(logs[0]["triggers"]) == 1
        assert "Caffeine" in logs[0]["triggers"]

        # Assert on seizure episode data
        assert len(logs[0].get("seizure", [])) == 1
        assert logs[0].get("seizure", [{}])[0].get("note") == "Very intense"

    def test_logs_returned_with_multiple_details(
        self, authenticated_client, sample_user, db_session
    ):
        """Test that logs returned include detailed data for multiple prodromes, auras, and triggers."""
        log = UserLog(
            user_id=sample_user.id, log_time=datetime.now() - timedelta(days=1)
        )
        db_session.add(log)

        # Multiple prodromes
        prodrome = UserProdrome(
            log=log,
            prodrome=Prodrome(name="Severe Headache"),
            intensity=4,
            note="Very painful",
        )
        db_session.add(prodrome)

        prodrome = UserProdrome(
            log=log, prodrome=Prodrome(name="Nausea"), intensity=3, note="Felt nauseous"
        )
        db_session.add(prodrome)

        # Multiple auras
        aura = UserAura(
            log=log,
            aura=Aura(name="Visual Disturbances"),
            is_present=True,
            note="Blurred vision",
        )
        db_session.add(aura)

        aura = UserAura(
            log=log,
            aura=Aura(name="Auditory Distortion"),
            is_present=True,
            note="Hearing echoes",
        )
        db_session.add(aura)

        # Multiple triggers
        trigger = UserTrigger(
            log=log,
            trigger=Trigger(name="Caffeine"),
            value_boolean=True,
            note="Had coffee",
        )
        db_session.add(trigger)

        trigger = UserTrigger(
            log=log,
            trigger=Trigger(name="Stress Level"),
            value_numeric=6,
            note="High stress level",
        )
        db_session.add(trigger)

        db_session.commit()

        response = authenticated_client.get("/api/datalog/weekly-logs")
        assert response.status_code == 200
        logs = response.get_json()

        assert len(logs) == 1
        assert len(logs[0]["prodromes"]) == 2
        assert set(logs[0]["prodromes"]) == {"Severe Headache", "Nausea"}
        assert len(logs[0]["auras"]) == 2
        assert set(logs[0]["auras"]) == {"Visual Disturbances", "Auditory Distortion"}
        assert len(logs[0]["triggers"]) == 2
        assert set(logs[0]["triggers"]) == {"Caffeine", "Stress"}

    def test_multiple_logs_with_details(
        self, authenticated_client, sample_user, db_session
    ):
        """Test that multiple logs within the last week are returned with detailed information."""
        # Create multiple logs
        log1 = UserLog(
            user_id=sample_user.id,
            log_time=datetime.now() - timedelta(days=1),
            note="First log entry",
        )
        log2 = UserLog(
            user_id=sample_user.id,
            log_time=datetime.now() - timedelta(days=2),
            note="Second log entry",
        )
        db_session.add_all([log1, log2])
        db_session.commit()

        # Add multiple details to logs
        details = [
            (
                log1,
                "Severe Headache",
                4,
                "Very painful",
                "Visual Disturbances",
                True,
                "Blurred vision",
                "Caffeine",
                True,
                "Had coffee",
            ),
            (
                log2,
                "Mild Headache",
                3,
                "Manageable pain",
                "Auditory Distortion",
                True,
                "Hearing noises",
                "Skipped Medication",
                True,
                "High stress day",
            ),
        ]
        for (
            log,
            prod_name,
            intensity,
            note,
            aura_name,
            is_present,
            aura_note,
            trigger_name,
            value_boolean,
            trigger_note,
        ) in details:
            prodrome = UserProdrome(
                log=log,
                prodrome=Prodrome(name=prod_name),
                intensity=intensity,
                note=note,
            )
            aura = UserAura(
                log=log,
                aura=Aura(name=aura_name),
                is_present=is_present,
                note=aura_note,
            )
            trigger = UserTrigger(
                log=log,
                trigger=Trigger(name=trigger_name),
                value_boolean=value_boolean,
                note=trigger_note,
            )
            db_session.add_all([prodrome, aura, trigger])
        db_session.commit()

        # Fetch and assert
        response = authenticated_client.get("/api/datalog/weekly-logs")
        assert response.status_code == 200
        logs = response.get_json()
        assert len(logs) == 2, "Should return two logs"

        # Assert the order of logs (most recent first)
        assert logs[0]["date"] == log1.log_time.strftime(
            "%Y-%m-%d"
        ), "Most recent log should be first"
        assert logs[1]["date"] == log2.log_time.strftime(
            "%Y-%m-%d"
        ), "Older log should be second"

        # Assert details are correctly populated
        assert logs[0]["notes"] == "First log entry"
        assert logs[1]["notes"] == "Second log entry"
        assert "Severe Headache" in logs[0]["prodromes"]
        assert "Visual Disturbances" in logs[0]["auras"]
        assert "Caffeine" in logs[0]["triggers"]
        assert "Mild Headache" in logs[1]["prodromes"]
        assert "Auditory Distortion" in logs[1]["auras"]
        assert "Skipped Medication" in logs[1]["triggers"]
