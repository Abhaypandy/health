from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.audit_log import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(AuditLog).all()
