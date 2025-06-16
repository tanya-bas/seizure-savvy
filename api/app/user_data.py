# user_data.py
# Import Statements
import random
from datetime import datetime, timedelta
import numpy as np

from faker import Faker
from werkzeug.security import generate_password_hash
from __init__ import db
from .schema import (
    User,
    Medication,
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

fake = Faker()


# Function to generate fake users
def generate_fake_users(n):
    for _ in range(n):
        # Generate a random birthdate between 18 and 100 years ago
        birthdate = fake.date_between(start_date="-100y", end_date="-18y")
        # Assume 50% of the users may want to track menstruation
        menstruation = random.choice([True, False])
        user = User(
            email=fake.email(),
            password_hash=generate_password_hash("password"),
            birthdate=birthdate,
            has_menstruation=menstruation,
        )
        db.session.add(user)
    db.session.commit()


# Function to generate fake medications
def generate_fake_medications(n):
    users = User.query.all()
    for user in users:
        for _ in range(n):
            medication = Medication(
                user_id=user.id,
                name=fake.word(),
                dosage_mg=random.randint(1, 500),
                frequency=random.uniform(0.5, 3),
                start_date=fake.date_between(start_date="-1y", end_date="today"),
                end_date=(
                    fake.date_between(start_date="today", end_date="+1y")
                    if random.choice([True, False])
                    else None
                ),
                reason_for_stop=fake.text(max_nb_chars=200),
            )
            db.session.add(medication)
    db.session.commit()


# Function to generate fake user logs
def generate_fake_logs(n):
    users = User.query.all()
    for user in users:
        for _ in range(n):
            log = UserLog(
                user_id=user.id,
                log_time=fake.date_time_between(start_date="-1y", end_date="now"),
            )
            db.session.add(log)
    db.session.commit()


# Function to add prodromes
def add_prodromes():
    prodrome_data = {
        "Headache": "A painful sensation in any part of the head, ranging from sharp to dull, that may occur with other symptoms.",
        "Numbness or tingling": "A loss of sensation or feeling in a part of your body, often felt in extremities.",
        "Tremor": "An involuntary, rhythmic muscle contraction leading to shaking movements in one or more parts of the body.",
        "Dizziness": "A sensation of spinning around and losing one’s balance.",
        "Nausea": "A feeling of sickness with an inclination to vomit.",
        "Anxiety": "A feeling of worry, nervousness, or unease about something with an uncertain outcome.",
        "Mood Changes": "Variations in a person’s mood or emotional state.",
        "Insomnia": "Difficulty falling asleep or staying asleep as long as desired.",
        "Difficulty Focusing": "A hard time maintaining attention or concentrating on tasks.",
        "Gastrointestinal Disturbances": "Problems with the gastrointestinal tract, including stomach pain, constipation, or diarrhea.",
    }
    for name, description in prodrome_data.items():
        prodrome = Prodrome(name=name, description=description)
        db.session.add(prodrome)
    db.session.commit()


# Function to generate fake user prodromes
def add_user_prodromes():
    users = User.query.all()
    prodromes = Prodrome.query.all()
    for user in users:
        for _ in range(100):
            log_date = datetime.today() - timedelta(days=100)
            log = UserLog(user_id=user.id, log_time=log_date)
            db.session.add(log)
            db.session.flush()  # To get the log_id for the UserProdrome
            for prodrome in prodromes:
                intensity = generate_prodrome_intensity(prodrome.name)
                if intensity > 0:
                    user_prodrome = UserProdrome(
                        log_id=log.id, prodrome_id=prodrome.id, intensity=intensity
                    )
                    db.session.add(user_prodrome)
        db.session.commit()


# Function to generate prodrome intensity
def generate_prodrome_intensity(name):
    if name in [
        "Headache",
        "Anxiety",
        "Mood changes",
        "Insomnia",
        "Difficulty focusing",
    ]:
        return np.random.choice(
            [i for i in range(6, 11)] + [i for i in range(6)], p=[0.14] * 5 + [0.05] * 6
        )
    elif name in ["gastrointestinal disturbances", "tremor"]:
        return np.random.choice(range(11), p=[0.85] + [0.015] * 10)
    elif name == "dizziness" or name == "nausea":
        return np.random.choice(range(11), p=[0.75] + [0.025] * 10)
    else:  # 'numbness or tingling'
        return np.random.choice(range(11), p=[0.7] + [0.03] * 10)


# Function to add auras
def add_auras():
    aura_data = {
        "Visual Disturbances": "Vision difficulties, colored or flashing lights, or hallucinations (seeing something that isn’t actually there).",
        "Hearing Sounds": "Ear ringing or buzzing, or sound hallucinations.",
        "Unusual Smell or Taste": "Perceiving strange smells or tastes without an apparent source.",
        "A ‘rising’ Feeling in the Stomach": "A sensation similar to the feeling of butterflies in the stomach that seems to rise upwards.",
        "Feeling of Déjà Vu or Jamais Vu": "Sensing that something has been experienced before (Déjà Vu) or feeling as if everything is unfamiliar (Jamais Vu).",
    }
    for name, description in aura_data.items():
        aura = Aura(name=name, description=description)
        db.session.add(aura)
    db.session.commit()


# Function to generate fake user auras
def add_user_auras():
    users = User.query.all()
    auras = Aura.query.all()
    for user in users:
        for _ in range(100):
            log_date = datetime.today() - timedelta(days=100)
            log = UserLog(user_id=user.id, log_time=log_date)
            db.session.add(log)
            db.session.flush()  # To get the log_id for the UserAura
            for aura in auras:
                if random.random() < 0.1:  # 10% chance of experiencing aura
                    user_aura = UserAura(log_id=log.id, aura_id=aura.id)
                    db.session.add(user_aura)
        db.session.commit()


# Function to add triggers
def add_triggers():
    trigger_data = {
        "Sleep quality": "Quality of sleep experienced by the user.",
        "Sleep duration": "Duration of sleep experienced by the user.",
        "Stress level": "Level of stress experienced by the user.",
        "Alcohol consumption today": "Amount of alcohol consumed by the user on the current day.",
        "Caffeine consumption today": "Amount of caffeine consumed by the user on the current day.",
        "Drugs consumption today": "Consumption of drugs by the user on the current day.",
        "Smoking": "Smoking activity of the user.",
        "Missing a meal": "Occurrence of missing a meal by the user.",
        "Fevers": "Occurrence of fevers experienced by the user.",
        "Steps": "Number of steps taken by the user.",
        "High intensity minutes": "Duration of high-intensity physical activity experienced by the user.",
        "Flashing light": "Exposure to flashing lights experienced by the user.",
        "Monthly periods": "Menstrual periods experienced by the user.",
        "Adherence to prescribed medication regimen": "Adherence to the prescribed medication regimen by the user.",
        "Changes in medication dosage or type": "Changes in medication dosage or type experienced by the user.",
    }
    for name, description in trigger_data.items():
        trigger = Trigger(name=name, description=description)
        db.session.add(trigger)
    db.session.commit()


# Function to generate fake user triggers
def add_user_triggers():
    users = User.query.all()
    triggers = Trigger.query.all()
    for user in users:
        for _ in range(100):
            log_date = datetime.today() - timedelta(days=100)
            log = UserLog(user_id=user.id, log_time=log_date)
            db.session.add(log)
            db.session.flush()  # To get the log_id for the UserTrigger
            for trigger in triggers:
                if trigger.name in [
                    "Drugs consumption today",
                    "Fevers",
                    "Missing a meal",
                    "Flashing light",
                    "Adherence to prescribed medication regimen",
                    "Changes in medication dosage or type",
                ]:
                    value_boolean = np.random.choice([True, False], p=[0.05, 0.95])
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_boolean=value_boolean,
                    )
                elif trigger.name == "Sleep quality":
                    value_numeric = np.random.choice(
                        [i for i in range(6, 11)] + [i for i in range(5)],
                        p=[0.15] * 5 + [0.05] * 5,
                    )
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Sleep duration":
                    value_numeric = np.random.normal(7, 1.5).clip(0, 12)
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Stress level":
                    value_numeric = np.random.choice(
                        [i for i in range(4, 11)] + [i for i in range(4)],
                        p=[0.12] * 7 + [0.04] * 4,
                    )
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Alcohol consumption today":
                    value_numeric = np.random.choice(
                        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        p=[
                            0.4,
                            0.15,
                            0.1,
                            0.1,
                            0.05,
                            0.05,
                            0.05,
                            0.025,
                            0.025,
                            0.025,
                            0.025,
                        ],
                    )
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Caffeine consumption today":
                    value_numeric = np.random.choice(
                        range(5), p=[0.2, 0.3, 0.25, 0.15, 0.1]
                    )
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Smoking":
                    value_numeric = np.random.choice(range(21), p=[0.4] + [0.03] * 20)
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Steps":
                    value_numeric = np.random.normal(5000, 2500).clip(0)
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "High intensity minutes":
                    value_numeric = np.random.normal(30, 15).clip(0, 150)
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                elif trigger.name == "Monthly periods":
                    value_numeric = np.random.randint(1, 29)
                    user_trigger = UserTrigger(
                        log_id=log.id,
                        trigger_id=trigger.id,
                        value_numeric=value_numeric,
                    )
                db.session.add(user_trigger)
    db.session.commit()


# Function to add seizure types
def add_seizure_types():
    seizure_types = [
        "Generalized Tonic-Clonic",
        "Absence",
        "Myoclonic",
        "Atonic",
        "Focal",
    ]
    for seizure_type in seizure_types:
        type_obj = SeizureType(name=seizure_type)
        db.session.add(type_obj)
    db.session.commit()


# Function to generate fake seizure episodes
def add_seizure_episodes():
    users = User.query.all()
    seizure_types = SeizureType.query.all()
    for user in users:
        for _ in range(10):
            seizure_date = fake.date_time_between(start_date="-1y", end_date="now")
            seizure_type = random.choice(seizure_types)
            seizure_duration = random.randint(10, 300)  # Duration in seconds
            seizure_notes = fake.text(max_nb_chars=200)
            requires_emergency_intervention = fake.boolean(chance_of_getting_true=10)
            postictal_confusion_duration = random.uniform(0, 60)
            postictal_confusion_intensity = random.randint(0, 10)
            postictal_headache_duration = random.uniform(0, 60)
            postictal_headache_intensity = random.randint(0, 10)
            postictal_fatigue_duration = random.uniform(0, 60)
            postictal_fatigue_intensity = random.randint(0, 10)
            episode = SeizureEpisode(
                log_id=user.log.id,
                seizure_type_id=seizure_type.id,
                duration_sec=seizure_duration,
                frequency=1,  # Default frequency
                requires_emergency_intervention=requires_emergency_intervention,
                postictal_confusion_duration=postictal_confusion_duration,
                postictal_confusion_intensity=postictal_confusion_intensity,
                postictal_headache_duration=postictal_headache_duration,
                postictal_headache_intensity=postictal_headache_intensity,
                postictal_fatigue_duration=postictal_fatigue_duration,
                postictal_fatigue_intensity=postictal_fatigue_intensity,
                note=seizure_notes,
            )
            db.session.add(episode)
    db.session.commit()
