from datetime import date, datetime, time

import pytest

from api.app.schema import (
    User,
    Medication,
    Prodrome,
    UserProdrome,
    Aura,
    UserAura,
    Trigger,
    UserTrigger,
    SeizureType,
    SeizureEpisode,
    UserLog,
)


@pytest.fixture
def medication_factory(db_session):
    def create_medication(
        user: User,
        name: str,
        dosage_mg: float,
        frequency: float,
        first_dose: time = None,
        start_date: date = date.today(),
        end_date: date = None,
        reason_for_stop: str = "",
        is_stopped: bool = False,
    ):
        medication = Medication(
            user_id=user.id,
            name=name,
            dosage_mg=dosage_mg,
            frequency=frequency,
            first_dose=first_dose,
            start_date=start_date,
            end_date=end_date,
            reason_for_stop=reason_for_stop,
            is_stopped=is_stopped,
        )
        db_session.add(medication)
        db_session.commit()
        return medication

    return create_medication


@pytest.fixture
def prodrome_factory(db_session):
    def create_prodrome(name: str, description: str = None):
        prodrome = Prodrome(name=name, description=description)
        db_session.add(prodrome)
        db_session.commit()
        return prodrome

    return create_prodrome


@pytest.fixture
def user_prodrome_factory(db_session, user_log_factory, prodrome_factory):
    def create_user_prodrome(
        user_log: UserLog, prodrome: Prodrome, intensity: int = 0, note: str = None
    ):
        user_prodrome = UserProdrome(
            log_id=user_log.id, prodrome_id=prodrome.id, intensity=intensity, note=note
        )
        db_session.add(user_prodrome)
        db_session.commit()
        return user_prodrome

    return create_user_prodrome


@pytest.fixture
def aura_factory(db_session):
    def create_aura(name: str, description: str = None):
        aura = Aura(name=name, description=description)
        db_session.add(aura)
        db_session.commit()
        return aura

    return create_aura


@pytest.fixture
def user_aura_factory(db_session, user_log_factory, aura_factory):
    def create_user_aura(
        user_log: UserLog, aura: Aura, is_present: bool = False, note: str = None
    ):
        user_aura = UserAura(
            log_id=user_log.id, aura_id=aura.id, is_present=is_present, note=note
        )
        db_session.add(user_aura)
        db_session.commit()
        return user_aura

    return create_user_aura


@pytest.fixture
def trigger_factory(db_session):
    def create_trigger(name: str, description: str = None):
        trigger = Trigger(name=name, description=description)
        db_session.add(trigger)
        db_session.commit()
        return trigger

    return create_trigger


@pytest.fixture
def user_trigger_factory(db_session, user_log_factory, trigger_factory):
    def create_user_trigger(
        user_log: UserLog,
        trigger: Trigger,
        value_numeric: float = None,
        value_boolean: bool = None,
        note: str = None,
    ):
        user_trigger = UserTrigger(
            log_id=user_log.id,
            trigger_id=trigger.id,
            value_numeric=value_numeric,
            value_boolean=value_boolean,
            note=note,
        )
        db_session.add(user_trigger)
        db_session.commit()
        return user_trigger

    return create_user_trigger


@pytest.fixture
def seizure_type_factory(db_session):
    def create_seizure_type(name, description=None):
        seizure_type = SeizureType(name=name, description=description)
        db_session.add(seizure_type)
        db_session.commit()
        return seizure_type

    return create_seizure_type


@pytest.fixture
def seizure_episode_factory(db_session, user_factory, seizure_type_factory):

    def create_seizure_episode(
        user_log: UserLog,
        seizure_type: SeizureType,
        duration_sec: int = None,
        frequency: int = 1,
        requires_emergency_intervention: bool = False,
    ):
        seizure_episode = SeizureEpisode(
            log_id=user_log.id,
            seizure_type_id=seizure_type.id,
            duration_sec=duration_sec,
            frequency=frequency,
            requires_emergency_intervention=requires_emergency_intervention,
        )
        db_session.add(seizure_episode)
        db_session.commit()
        return seizure_episode

    return create_seizure_episode


@pytest.fixture
def user_log_factory(db_session, user_factory):
    def create_user_log(user: User, log_time: datetime = datetime.now()):
        user_log = UserLog(user_id=user.id, log_time=log_time)
        db_session.add(user_log)
        db_session.commit()
        return user_log

    return create_user_log


@pytest.fixture
def sample_log(user_log_factory, sample_user):
    return user_log_factory(user=sample_user)
