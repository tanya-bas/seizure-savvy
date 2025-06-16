import re
from datetime import date, datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy import and_, or_, func
from sqlalchemy.ext.hybrid import hybrid_property
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()
# Declaring a base class for declarative class definitions
Base = db.Model


# Database model for storing user information
class User(Base):
    """Store user information"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    logs = db.relationship("UserLog", back_populates="user")

    # Using birthdate to calculate age dynamically
    birthdate = db.Column(db.Date, nullable=False)

    # Asking users if they experience menstruation instead of gender
    # Because the app needs this information and it might not match gender
    has_menstruation = db.Column(db.Boolean, default=False, nullable=False)

    # Relationship to UserLogs; delete logs when user is deleted
    logs = db.relationship(
        "UserLog", back_populates="user", cascade="all, delete-orphan"
    )
    medications = db.relationship(
        "Medication",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",  # Lazy loading
    )

    def validate_email(self):
        """Check if the email follows the correct format."""
        pattern = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        return re.match(pattern, self.email) is not None

    def set_password(self, password):
        """Set the password hash."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check the password hash."""
        return check_password_hash(self.password_hash, password)

    @hybrid_property
    def full_name(self):
        """Return the full name of the user."""
        return f"{self.first_name} {self.last_name}"

    @full_name.expression
    def full_name(cls):
        return cls.first_name + " " + cls.last_name

    @hybrid_property  # For class and instance level
    def age(self):
        """Calculate age based on birthdate."""
        today = date.today()
        return (
            today.year
            - self.birthdate.year
            - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        )

    @age.expression  # For SQL expression level
    def age(cls):
        return func.extract("year", func.current_date()) - func.extract(
            "year", cls.birthdate
        )

    def is_adult(self):
        """Check if the user is at least 18 years old."""
        return self.age >= 18


class Medication(Base):
    """Tracks medications associated with a user."""

    __tablename__ = "medications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)

    # Dosage in mg
    dosage_mg = db.Column(db.Float, nullable=False)
    reason_for_stop = db.Column(db.String(1000), nullable=True, default="")

    # Frequency in times per day, 1-5
    frequency = db.Column(db.Integer, nullable=False)
    first_dose = db.Column(db.Time, nullable=True)  # Time of the first dose
    start_date = db.Column(db.Date, nullable=False, default=date.today())
    end_date = db.Column(db.Date, nullable=True, default=None)

    # Track if the medication is stopped
    is_stopped = db.Column(db.Boolean, default=False, nullable=False)

    user = db.relationship("User", back_populates="medications")

    __table_args__ = (
        # non-negative integer between 0 and 150
        CheckConstraint("dosage_mg >= 0", name="check_dosage"),
        CheckConstraint("frequency >= 0 and frequency <= 5", name="check_frequency"),
        # start date must be before end date
        CheckConstraint(
            or_(end_date.is_(None), and_(end_date.isnot(None), start_date < end_date)),
            name="check_start_before_end",
        ),
    )


class Prodrome(Base):
    """Stores prodrome details, to describe early symptoms."""

    __tablename__ = "prodromes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Relationship to UserProdromes
    user_prodromes = db.relationship("UserProdrome", back_populates="prodrome")


class UserProdrome(Base):
    """Links prodromes to specific user logs, necessary for many-to-many relationships."""

    __tablename__ = "user_prodromes"

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("user_logs.id"), nullable=False)
    prodrome_id = db.Column(db.Integer, db.ForeignKey("prodromes.id"), nullable=False)

    intensity = db.Column(db.Integer, nullable=False, default=0)
    note = db.Column(db.Text)

    # Many-to-many relationship
    log = db.relationship("UserLog", back_populates="prodromes")
    prodrome = db.relationship("Prodrome", back_populates="user_prodromes")

    __table_args__ = (
        CheckConstraint("intensity >= 0 and intensity <= 10", name="check_intensity"),
    )


class Aura(Base):
    """Contains details about auras, which are sensory disturbances that can precede a seizure."""

    __tablename__ = "auras"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Relationship to UserAura
    user_auras = db.relationship("UserAura", back_populates="aura")


class UserAura(Base):
    """Links auras to specific user logs, necessary for many-to-many relationships."""

    __tablename__ = "user_auras"

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("user_logs.id"), nullable=False)
    aura_id = db.Column(db.Integer, db.ForeignKey("auras.id"), nullable=False)
    # Whether the aura is present or not. The default is False.
    is_present = db.Column(db.Boolean, nullable=False, default=False)
    note = db.Column(db.Text)

    # Many-to-many relationship
    log = db.relationship("UserLog", back_populates="auras")
    aura = db.relationship("Aura", back_populates="user_auras")


class Trigger(Base):
    """Contains details about triggers, which are factors that can increase the likelihood of a seizure."""

    __tablename__ = "triggers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Relationship to UserTriggers
    user_triggers = db.relationship("UserTrigger", back_populates="trigger")


class UserTrigger(Base):
    """Links triggers to specific user logs, necessary for many-to-many relationships."""

    __tablename__ = "user_triggers"

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("user_logs.id"), nullable=False)
    trigger_id = db.Column(db.Integer, db.ForeignKey("triggers.id"), nullable=False)

    # For numeric values, e.g. sleep quality
    value_numeric = db.Column(db.Float, nullable=True)
    # For boolean values, like skipped medication
    value_boolean = db.Column(db.Boolean, nullable=True, default=False)

    note = db.Column(db.Text)

    log = db.relationship("UserLog", back_populates="triggers")
    trigger = db.relationship("Trigger")

    __table_args__ = (
        CheckConstraint("value_numeric >= 0", name="positive_trigger_value_numeric"),
    )


class SeizureType(Base):
    """Store seizure types"""

    __tablename__ = "seizure_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    # Relationship to SeizureEpisode
    SeizureEpisode = db.relationship("SeizureEpisode", back_populates="seizure_type")


class SeizureEpisode(Base):
    """Connects seizure incidents to user logs and seizure types."""

    __tablename__ = "seizure_episodes"

    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey("user_logs.id"), nullable=False)
    seizure_type_id = db.Column(
        db.Integer, db.ForeignKey("seizure_types.id"), nullable=False
    )
    duration_sec = db.Column(db.Integer, nullable=True)
    frequency = db.Column(db.Integer, nullable=True, default=1)
    requires_emergency_intervention = db.Column(
        db.Boolean, nullable=False, default=False
    )
    postictal_confusion_duration = db.Column(db.Float)
    postictal_confusion_intensity = db.Column(db.Integer)
    postictal_headache_duration = db.Column(db.Float)
    postictal_headache_intensity = db.Column(db.Integer)
    postictal_fatigue_duration = db.Column(db.Float)
    postictal_fatigue_intensity = db.Column(db.Integer)
    note = db.Column(db.Text)

    log = db.relationship("UserLog", back_populates="seizures")
    seizure_type = db.relationship("SeizureType")

    __table_args__ = (
        CheckConstraint("duration_sec >= 0", name="check_duration_positive"),
        CheckConstraint("frequency >= 1", name="check_frequency_positive"),
        CheckConstraint(
            "postictal_confusion_duration >= 0",
            name="check_postictal_confusion_duration_positive",
        ),
        CheckConstraint(
            "postictal_headache_duration >= 0",
            name="check_postictal_headache_duration_positive",
        ),
        CheckConstraint(
            "postictal_fatigue_duration >= 0",
            name="check_postictal_fatigue_duration_positive",
        ),
        CheckConstraint(
            "postictal_confusion_intensity BETWEEN 0 AND 10",
            name="check_postictal_confusion_intensity",
        ),
        CheckConstraint(
            "postictal_headache_intensity BETWEEN 0 AND 10",
            name="check_postictal_headache_intensity",
        ),
        CheckConstraint(
            "postictal_fatigue_intensity BETWEEN 0 AND 10",
            name="check_postictal_fatigue_intensity",
        ),
    )


class UserLog(Base):
    """Daily survey for users to record incidents or observations, linked to other tables like UserProdrome, UserAura, UserTrigger, SeizureEpisode"""

    __tablename__ = "user_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    log_time = db.Column(db.DateTime, default=datetime.now())

    user = db.relationship("User", back_populates="logs")
    prodromes = db.relationship("UserProdrome", back_populates="log")
    auras = db.relationship("UserAura", back_populates="log")
    triggers = db.relationship("UserTrigger", back_populates="log")
    seizures = db.relationship("SeizureEpisode", back_populates="log")
    note = db.Column(db.String, nullable=True)

    @hybrid_property
    def total_episodes(self):
        """Calculate the total number of episodes."""
        return len(self.seizures)

    @total_episodes.expression
    def total_episodes(cls):
        return (
            db.select([db.func.count(SeizureEpisode.id)])
            .where(SeizureEpisode.log_id == cls.id)
            .label("total_episodes")
        )

    @hybrid_property
    def has_seizures(self):
        """Check if there are any seizures."""
        return self.total_episodes > 0

    @has_seizures.expression
    def has_seizures(cls):
        return cls.total_episodes > 0
