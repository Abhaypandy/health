from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.consent import Consent
from app.models.document import Document
from app.services.semantic_retrieval import semantic_search
from datetime import date
from app.services.access_control import get_accessible_document_ids
from app.services.rag_service import generate_answer # Moved import up top


router = APIRouter(prefix="/retrieve", tags=["Retrieval"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/retrieve/patient/{patient_id}/semantic")
def retrieve_patient_semantic_chunks(
    patient_id: int,
    doctor_id: int,
    query: str,
    top_k: int = 5,
    doc_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db)
):
    # 👇 Everything below this line must be indented 👇
    doc_ids = get_accessible_document_ids(
        db, patient_id, doctor_id
    )
    results = semantic_search(
        db=db,
        doc_ids=doc_ids,
        query_text=query,
        top_k=top_k,
        doc_type=doc_type,
        start_date=start_date,
        end_date=end_date
    )

    # Note: I moved the 'from app.services.rag_service import generate_answer' 
    # to the top of the file where imports typically belong.

    answer = generate_answer(
        query,
        [r["content"] for r in results]
    )

    return {
        "answer": answer,
        "sources": results
    }
