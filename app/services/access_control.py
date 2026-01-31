from sqlalchemy.orm import Session
from app.models.consent import Consent
from app.models.document import Document

def get_accessible_document_ids(
    db: Session,
    patient_id: int,
    doctor_id: int
) -> list[int]:
    consent = db.query(Consent).filter(
        Consent.patient_id == patient_id,
        Consent.doctor_id == doctor_id,
        Consent.consent_given == True
    ).first()

    if not consent:
        return []

    docs = db.query(Document.id).filter(
        Document.owner_id == patient_id
    ).all()

    return [d.id for d in docs]
