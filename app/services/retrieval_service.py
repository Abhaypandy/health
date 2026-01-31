from app.services.embedding_service import generate_embedding
from app.database import SessionLocal
from app.models.document_chunk import DocumentChunk
from sqlalchemy import text


def retrieve_similar_chunks(
    query: str,
    top_k: int = 5
):
    query_embedding = generate_embedding(query)

    db = SessionLocal()

    sql = text("""
        SELECT
            id,
            document_id,
            chunk_index,
            content,
            embedding <=> :query_embedding AS distance
        FROM document_chunks
        ORDER BY embedding <=> :query_embedding
        LIMIT :top_k
    """)

    results = db.execute(
        sql,
        {
            "query_embedding": query_embedding,
            "top_k": top_k
        }
    ).fetchall()

    db.close()

    return [
        {
            "document_id": row.document_id,
            "chunk_index": row.chunk_index,
            "content": row.content,
            "distance": row.distance
        }
        for row in results
    ]
