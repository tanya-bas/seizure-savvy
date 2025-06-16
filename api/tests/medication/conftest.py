from datetime import datetime, time
import pytest

from sqlalchemy.orm import Session
from api.app.schema import Medication, User


@pytest.fixture
def sample_medication(db_session: Session, sample_user: User) -> Medication:
    """Create a medication for testing, linked to the sample user."""
    medication = Medication(
        user_id=sample_user.id,
        name="TestMed",
        dosage_mg=500,
        frequency=2,
        first_dose=time(8, 0),  # 08:00 AM
        start_date=datetime.strptime("2023-02-23", "%Y-%m-%d").date(),
        end_date=None,
        reason_for_stop="",
        is_stopped=False,
    )
    db_session.add(medication)
    db_session.commit()
    return medication
