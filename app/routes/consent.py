from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.consent import Consent
from app.models.audit_log import AuditLog


router = APIRouter(prefix="/consent", tags=["Consent"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/grant")
def grant_consent(patient_id: int, doctor_id: int, db: Session = Depends(get_db)):
    consent = Consent(
        patient_id=patient_id,
        doctor_id=doctor_id,
        consent_given=True
    )
    db.add(consent)

    audit = AuditLog(
        user_id=doctor_id,
        action="GRANT_CONSENT",
        resource=f"patient:{patient_id}"
    )
    db.add(audit)

    db.commit()
    return {"message": "Consent granted"}

@router.post("/revoke")
def revoke_consent(patient_id: int, doctor_id: int, db: Session = Depends(get_db)):
    consent = db.query(Consent).filter(
        Consent.patient_id == patient_id,
        Consent.doctor_id == doctor_id,
        Consent.consent_given == True
    ).first()

    if not consent:
        raise HTTPException(status_code=403, detail="No Consent")

    consent.consent_given = False

    audit = AuditLog(
        user_id=doctor_id,
        action="REVOKE_CONSENT",
        resource=f"patient:{patient_id}"
    )
    db.add(audit)

    db.commit()
    return {"message": "Consent revoked"}
