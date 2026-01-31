from datetime import date
from sqlalchemy import and_

from app.models.document_chunk import DocumentChunk
from app.models.document import Document
from app.services.embedding_service import generate_embedding


def semantic_search(
    db,
    doc_ids,
    query_text: str,
    top_k: int = 5,
    doc_type: str | None = None,
    start_date: date | None = None,
    end_date: date | None = None
):
    query_embedding = generate_embedding(query_text)

    distance = DocumentChunk.embedding.cosine_distance(
        query_embedding
    ).label("distance")

    q = (
        db.query(DocumentChunk, distance)
        .join(Document, Document.id == DocumentChunk.document_id)
        .filter(DocumentChunk.document_id.in_(doc_ids))
    )

    # ✅ STEP-2 filters
    if doc_type:
        q = q.filter(Document.doc_type == doc_type)

    if start_date:
        q = q.filter(Document.visit_date >= start_date)

    if end_date:
        q = q.filter(Document.visit_date <= end_date)

    results = (
        q.order_by(distance)
         .limit(top_k)
         .all()
    )

    return [
        {
            "document_id": chunk.document_id,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content,
            "distance": float(distance)
        }
        for chunk, distance in results
    ]
