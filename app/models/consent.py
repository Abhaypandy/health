from sqlalchemy import Column, Integer, Boolean, ForeignKey, DateTime
from datetime import datetime
from app.database import Base

class Consent(Base):
    __tablename__ = "consents"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, nullable=False)
    doctor_id = Column(Integer, nullable=False)
    consent_given = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
