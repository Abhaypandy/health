# app/services/ingestion_service.py

from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding

def embed_and_store_chunk(
    *,
    db: Session,
    chunk_text: str,
    document_id: int,
    chunk_index: int
):
    embedding = generate_embedding(chunk_text)

    chunk = DocumentChunk(
        document_id=document_id,
        chunk_index=chunk_index,
        content=chunk_text,
        embedding=embedding
    )

    db.add(chunk)
