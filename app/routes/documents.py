import os
import base64
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.document import Document
from app.models.audit_log import AuditLog
from app.models.document_chunk import DocumentChunk
from app.utils.chunker import chunk_text
from app.services.ingestion_service import embed_and_store_chunk
from datetime import date



UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/documents", tags=["Documents"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload_base64")
def upload_document_base64(
    owner_id: int,
    filename: str,
    file_base64: str,
    doc_type: str,
    visit_date: date,
    db: Session = Depends(get_db)
):
    file_bytes = base64.b64decode(file_base64.encode())
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(file_bytes)

    doc = Document(
    owner_id=owner_id,
    filename=filename,
    filepath=filepath,
    doc_type=doc_type,
    visit_date=visit_date
)
    db.add(doc)

    audit = AuditLog(
        user_id=owner_id,
        action="UPLOAD_DOCUMENT",
        resource=f"document:{filename}"
    )
    db.add(audit)

    db.commit()
    return {"message": "Document uploaded (base64)"}
from app.services.ingestion_service import embed_and_store_chunk

@router.post("/process/{document_id}")
def process_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    # ✅ READ FILE CONTENT
    with open(document.filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    # ✅ CHUNK ACTUAL TEXT
    chunks = chunk_text(text)

    # ✅ SAFETY: clear old chunks (optional but recommended)
    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document.id
    ).delete()

    # ✅ STORE CHUNKS + EMBEDDINGS
    for idx, chunk in enumerate(chunks):
        embed_and_store_chunk(
            db=db,                      # ❗ you forgot this earlier
            chunk_text=chunk,
            document_id=document.id,
            chunk_index=idx,
        )

    db.commit()

    return {
        "document_id": document.id,
        "chunks_created": len(chunks)
    }
