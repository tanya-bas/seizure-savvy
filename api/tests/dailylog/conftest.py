# api/tests/dailylog/conftest.py
import pytest
from datetime import datetime, date
from api.app import db
from api.app.schema import (
    User,
    UserLog,
    Prodrome,
    Aura,
    Trigger,
    SeizureType,
    UserProdrome,
    UserAura,
    UserTrigger,
    SeizureEpisode,
)

# Import common fixtures
from api.tests.conftest import sample_user, db_session


@pytest.fixture
def sample_log(db_session, sample_user):
    """Fixture to create a sample log."""
    log = UserLog(user_id=sample_user.id, log_time=datetime.now())
    db_session.add(log)
    db_session.commit()
    return log


@pytest.fixture
def sample_prodrome(db_session):
    """Fixture to create a sample prodrome."""
    prodrome = Prodrome(name="Example Prodrome", description="headache")
    db_session.add(prodrome)
    db_session.commit()
    return prodrome


@pytest.fixture
def sample_aura(db_session):
    """Fixture to create a sample aura."""
    aura = Aura(name="Example Aura", description="Visual sensations")
    db_session.add(aura)
    db_session.commit()
    return aura


@pytest.fixture
def sample_trigger(db_session):
    """Fixture to create a sample trigger."""
    trigger = Trigger(name="Example Trigger", description="Stress")
    db_session.add(trigger)
    db_session.commit()
    return trigger


@pytest.fixture
def sample_seizure_type(db_session):
    """Fixture to create a sample seizure type."""
    seizure_type = SeizureType(name="Example SeizureType", description="Generalized")
    db_session.add(seizure_type)
    db_session.commit()
    return seizure_type


@pytest.fixture
def another_user_log(db_session):
    """Create another user and a log for testing access
    restrictions or multi-user scenarios."""
    another_user = User(
        first_name="Another",
        last_name="User",
        email="another@example.com",
        birthdate=date(1990, 1, 1),
        has_menstruation=False,
    )
    another_user.set_password("dummy_password")
    db_session.add(another_user)
    db_session.commit()

    log = UserLog(user_id=another_user.id, log_time=datetime.now())
    db_session.add(log)
    db_session.commit()
    return log


@pytest.fixture
def add_user_prodrome(db_session, sample_user, sample_prodrome):
    """Add a user prodrome to the database."""

    def _add_user_prodrome(log=None):
        if log is None:
            log = UserLog(user_id=sample_user.id, log_time=datetime.now())
            db_session.add(log)
            db_session.commit()

        user_prodrome = UserProdrome(
            log_id=log.id,
            prodrome_id=sample_prodrome.id,
            intensity=5,
            note="Initial note",
        )
        db_session.add(user_prodrome)
        db_session.commit()
        return user_prodrome

    return _add_user_prodrome


@pytest.fixture
def add_user_aura(db_session, sample_log, sample_aura):
    """Add a user aura to the database."""

    def _add_user_aura(log=sample_log):
        user_aura = UserAura(
            log_id=log.id, aura_id=sample_aura.id, is_present=True, note="Initial note"
        )
        db_session.add(user_aura)
        db_session.commit()
        return user_aura

    return _add_user_aura


@pytest.fixture
def add_user_trigger(db_session, sample_log, sample_trigger):
    """Add a user trigger to the database."""

    def _add_user_trigger(
        log=sample_log, value_numeric=10, value_boolean=True, note="Initial note"
    ):
        user_trigger = UserTrigger(
            log_id=log.id,
            trigger_id=sample_trigger.id,
            value_numeric=value_numeric,
            value_boolean=value_boolean,
            note=note,
        )
        db_session.add(user_trigger)
        db_session.commit()
        return user_trigger

    return _add_user_trigger


@pytest.fixture
def add_seizure_episode(db_session, sample_user, sample_log, sample_seizure_type):
    """Add a seizure episode to the database."""

    def _add_seizure_episode(log=sample_log):
        episode = SeizureEpisode(
            log_id=log.id,
            seizure_type_id=sample_seizure_type.id,
            duration_sec=120,
            frequency=1,
            note="Initial Episode",
            requires_emergency_intervention=False,
            postictal_confusion_duration=10,
            postictal_confusion_intensity=5,
            postictal_headache_duration=15,
            postictal_headache_intensity=5,
            postictal_fatigue_duration=20,
            postictal_fatigue_intensity=5,
        )
        db_session.add(episode)
        db_session.commit()
        return episode

    return _add_seizure_episode
