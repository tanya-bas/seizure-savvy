from datetime import date, timedelta, time

import pytest
from sqlalchemy.exc import IntegrityError

from api.app.schema import Medication, Prodrome, User, UserLog, UserProdrome


class TestUser:

    def test_register_user_success(self, sample_user):
        """Test a typical user registration."""
        user = sample_user

        # Check that the user's attributes are set correctly
        assert user.first_name == "Common"
        assert user.last_name == "User"
        assert user.full_name is not None

        # Check that the email is validated and set correctly
        assert user.validate_email()
        assert user.email == "user@example.com"

        # Check that the password is hashed and set correctly
        assert user.check_password("password")
        assert user.age == date.today().year - 2000
        assert not user.has_menstruation

    def test_register_user_invalid_email(self, sample_user):
        """Test that an invalid email is rejected."""
        user = sample_user
        user.email = "invalidemail"
        assert not user.validate_email()

    def test_password_hashing(self, sample_user):
        """Test that the password is hashed and not stored in plain text."""
        user = sample_user
        user.email = "hash@example.com"
        user.set_password("testpassword")
        assert user.password_hash != "testpassword"
        assert user.check_password("testpassword")


# TODO: Add test to check underage users


class TestMedication:

    def test_medication_addition_success(self, sample_user, medication_factory):
        """Test a typical medication addition."""
        first_dose_time = time(8, 0)  # 8:00 AM
        medication = medication_factory(
            user=sample_user,
            name="Med1",
            dosage_mg=500,
            frequency=2,
            first_dose=first_dose_time,
        )
        assert medication.user == sample_user
        assert medication.name == "Med1"
        assert medication.dosage_mg == 500
        assert medication.frequency == 2
        assert medication.first_dose == first_dose_time
        assert not medication.is_stopped
        assert medication.end_date is None
        assert medication.reason_for_stop == ""

    def test_medication_invalid_dosage(self, sample_user, medication_factory):
        """Test that an invalid dosage is rejected."""
        with pytest.raises(IntegrityError):
            medication_factory(user=sample_user, name="Med2", dosage_mg=-1, frequency=2)

    def test_medication_invalid_frequency(self, sample_user, medication_factory):
        """Test constraint that daily frequency must be greater than 0."""
        with pytest.raises(IntegrityError):
            medication_factory(
                user=sample_user, name="Med3", dosage_mg=500, frequency=-1
            )

    def test_medication_end_date_before_start(self, sample_user, medication_factory):
        """Test constraint that end date must be after start date."""
        start_date = date.today()
        end_date = start_date - timedelta(days=1)
        with pytest.raises(IntegrityError):
            medication_factory(
                user=sample_user,
                name="Med4",
                dosage_mg=500,
                frequency=1,
                start_date=start_date,
                end_date=end_date,
            )

    def test_medication_deletion_with_user(
        self, sample_user, medication_factory, db_session
    ):
        """Test that deleting a user also deletes their medications."""
        medication = medication_factory(
            user=sample_user, name="Med5", dosage_mg=500, frequency=2
        )

        db_session.add(sample_user)
        db_session.add(medication)
        db_session.commit()

        db_session.delete(sample_user)
        db_session.commit()

        deleted_medication = Medication.query.filter_by(name="Med5").first()
        assert deleted_medication is None

        def test_medication_stopped_logic(self, sample_user, medication_factory):
            """Test logic when medication is marked as stopped."""
            medication = medication_factory(
                user=sample_user,
                name="MedStop",
                dosage_mg=250,
                frequency=1,
                is_stopped=True,
                reason_for_stop="No longer needed",
                end_date=date.today(),
            )
            assert medication.is_stopped
            assert medication.reason_for_stop == "No longer needed"
            assert medication.end_date == date.today()

    def test_medication_first_dose_timing(self, sample_user, medication_factory):
        """Test correct storage and retrieval of the first dose timing."""
        first_dose_time = time(9, 30)  # 9:30 AM
        medication = medication_factory(
            user=sample_user,
            name="MedTime",
            dosage_mg=100,
            frequency=1,
            first_dose=first_dose_time,
        )
        assert medication.first_dose == first_dose_time


class TestProdrome:

    def test_create_prodrome_success(self, prodrome_factory):
        prodrome = prodrome_factory(name="Fatigue", description="Feeling tired")
        assert prodrome.name == "Fatigue"
        assert prodrome.description == "Feeling tired"

    def test_create_prodrome_missing_description(self, prodrome_factory):
        prodrome = prodrome_factory(name="Headache")
        assert prodrome.name == "Headache"
        assert prodrome.description is None


class TestUserProdrome:

    def test_link_user_prodrome_success(
        self, sample_log, prodrome_factory, user_prodrome_factory
    ):
        prodrome = prodrome_factory(name="Nausea")
        user_prodrome = user_prodrome_factory(
            user_log=sample_log, prodrome=prodrome, intensity=5
        )

        assert user_prodrome.log_id == sample_log.id
        assert user_prodrome.prodrome_id == prodrome.id
        assert user_prodrome.intensity == 5

    def test_user_prodrome_intensity_bounds(
        self,
        db_session,
        sample_log,
        prodrome_factory,
        user_prodrome_factory,
    ):
        user_log = sample_log
        prodrome = prodrome_factory(name="Dizziness")

        # Test for an intensity out of bounds, e.g., below 0.
        with pytest.raises(IntegrityError):
            user_prodrome_factory(user_log=user_log, prodrome=prodrome, intensity=-1)
            db_session.flush()  # Manually trigger the flush to catch the IntegrityError

        # Rollback to ensure the session is clean for the next test
        db_session.rollback()

        # Test for an intensity out of bounds, e.g., above 10.
        with pytest.raises(IntegrityError):
            user_prodrome_factory(user_log=user_log, prodrome=prodrome, intensity=11)
            db_session.flush()

        db_session.rollback()  # Final rollback


# TODO: add more tests to cover other aspects like updating or deleting a UserProdrome.


class TestAura:

    def test_create_aura_success(self, aura_factory):
        aura = aura_factory(name="Visual Disturbances", description="Seeing spots")
        assert aura.name == "Visual Disturbances"
        assert aura.description == "Seeing spots"

    def test_create_aura_missing_description(self, aura_factory):
        aura = aura_factory(name="Sensory Changes")
        assert aura.name == "Sensory Changes"
        assert aura.description is None


class TestUserAura:

    def test_link_user_aura_success(
        self,
        sample_log,
        aura_factory,
        user_aura_factory,
    ):
        aura = aura_factory(name="Visual Disturbances")
        user_aura = user_aura_factory(user_log=sample_log, aura=aura, is_present=True)

        assert user_aura.log_id == sample_log.id
        assert user_aura.aura_id == aura.id
        assert user_aura.is_present

    def test_aura_is_present(self, sample_log, aura_factory, user_aura_factory):
        aura = aura_factory(name="Sensory Changes")
        user_aura = user_aura_factory(user_log=sample_log, aura=aura)

        assert user_aura.is_present is False


class TestTrigger:

    def test_create_trigger_success(self, trigger_factory):
        trigger = trigger_factory(name="Lack of Sleep", description="Not enough rest")
        assert trigger.name == "Lack of Sleep"
        assert trigger.description == "Not enough rest"

    def test_create_trigger_missing_description(self, trigger_factory):
        trigger = trigger_factory(name="Stress")
        assert trigger.name == "Stress"
        assert trigger.description is None


class TestUserTrigger:

    def test_link_user_trigger_boolean(
        self,
        sample_log,
        trigger_factory,
        user_trigger_factory,
    ):
        user_log = sample_log
        trigger = trigger_factory(name="Lack of Sleep")
        user_trigger = user_trigger_factory(
            user_log=user_log, trigger=trigger, value_boolean=True
        )

        assert user_trigger.log_id == user_log.id
        assert user_trigger.trigger_id == trigger.id
        assert user_trigger.value_boolean

    def test_link_user_trigger_numeric(
        self, sample_log, trigger_factory, user_trigger_factory, user_log_factory
    ):
        user_log = sample_log
        trigger = trigger_factory(name="Stress")
        user_trigger = user_trigger_factory(
            user_log=user_log, trigger=trigger, value_numeric=7.5
        )

        assert user_trigger.log_id == user_log.id
        assert user_trigger.trigger_id == trigger.id
        assert user_trigger.value_numeric == 7.5


class TestSeizureType:

    def test_create_seizure_type_success(self, seizure_type_factory):
        seizure_type = seizure_type_factory(
            name="Tonic-Clonic", description="Grand mal"
        )
        assert seizure_type.name == "Tonic-Clonic"
        assert seizure_type.description == "Grand mal"

    def test_create_seizure_type_missing_description(self, seizure_type_factory):
        seizure_type = seizure_type_factory(name="Absence")
        assert seizure_type.name == "Absence"
        assert seizure_type.description is None


class TestSeizureEpisode:

    def test_create_seizure_episode_success(
        self,
        sample_log,
        seizure_type_factory,
        seizure_episode_factory,
    ):
        user_log = sample_log
        seizure_type = seizure_type_factory(name="Tonic-Clonic")
        seizure_episode = seizure_episode_factory(
            user_log=user_log, seizure_type=seizure_type, duration_sec=30
        )

        assert seizure_episode.seizure_type == seizure_type
        assert seizure_episode.duration_sec == 30

    def test_seizure_episode_invalid_duration(
        self, sample_log, seizure_type_factory, seizure_episode_factory
    ):
        seizure_type = seizure_type_factory(name="Absence")
        with pytest.raises(IntegrityError):
            seizure_episode_factory(
                user_log=sample_log, seizure_type=seizure_type, duration_sec=-1
            )


class TestUserLog:

    def test_create_user_log_success(self, sample_user, user_log_factory):
        user_log = user_log_factory(user=sample_user)

        assert user_log.user_id == sample_user.id
        assert user_log.log_time is not None
        assert len(user_log.prodromes) == 0
        assert len(user_log.auras) == 0
        assert len(user_log.triggers) == 0
        assert len(user_log.seizures) == 0

    def test_user_log_with_seizures(
        self,
        sample_user,
        user_log_factory,
        seizure_type_factory,
        seizure_episode_factory,
    ):
        seizure_type = seizure_type_factory(name="Type1")
        user_log = user_log_factory(user=sample_user)

        seizure_episode_factory(
            user_log=user_log, seizure_type=seizure_type, duration_sec=30
        )

        # Test hybrid property
        assert user_log.total_episodes == 1
        assert user_log.has_seizures

    def test_user_log_without_seizures(self, sample_user, user_log_factory):
        user_log = user_log_factory(user=sample_user)

        assert user_log.total_episodes == 0
        assert not user_log.has_seizures

    def test_user_log_with_prodromes(
        self, sample_user, user_log_factory, prodrome_factory, user_prodrome_factory
    ):
        user_log = user_log_factory(user=sample_user)
        prodrome1 = prodrome_factory(name="Dizziness")
        prodrome2 = prodrome_factory(name="Nausea")

        user_prodrome_factory(user_log=user_log, prodrome=prodrome1, intensity=4)
        user_prodrome_factory(user_log=user_log, prodrome=prodrome2, intensity=5)

        assert len(user_log.prodromes) == 2
        assert any(p.prodrome_id == prodrome1.id for p in user_log.prodromes)
        assert any(p.prodrome_id == prodrome2.id for p in user_log.prodromes)

    def test_user_log_with_auras(
        self, sample_user, user_log_factory, aura_factory, user_aura_factory
    ):
        user_log = user_log_factory(user=sample_user)
        aura1 = aura_factory(name="Visual Disturbances")
        aura2 = aura_factory(name="Sensory Changes")

        user_aura_factory(user_log=user_log, aura=aura1, is_present=True)
        user_aura_factory(user_log=user_log, aura=aura2, is_present=False)

        assert len(user_log.auras) == 2
        assert any(a.aura_id == aura1.id and a.is_present for a in user_log.auras)
        assert any(a.aura_id == aura2.id and not a.is_present for a in user_log.auras)

    def test_user_log_with_triggers(
        self, sample_user, user_log_factory, trigger_factory, user_trigger_factory
    ):
        user_log = user_log_factory(user=sample_user)
        trigger1 = trigger_factory(name="Lack of Sleep")
        trigger2 = trigger_factory(name="Stress")

        user_trigger_factory(user_log=user_log, trigger=trigger1, value_boolean=True)
        user_trigger_factory(user_log=user_log, trigger=trigger2, value_numeric=7.5)

        assert len(user_log.triggers) == 2
        assert any(
            t.trigger_id == trigger1.id and t.value_boolean for t in user_log.triggers
        )
        assert any(
            t.trigger_id == trigger2.id and t.value_numeric == 7.5
            for t in user_log.triggers
        )
