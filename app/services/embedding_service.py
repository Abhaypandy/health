

from sentence_transformers import SentenceTransformer
import numpy as np

# Load once at startup (IMPORTANT)
MODEL_NAME = "all-MiniLM-L6-v2"
model = SentenceTransformer(MODEL_NAME)

EMBEDDING_DIM = 384  # must match pgvector column

def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(
        text,
        normalize_embeddings=True  # IMPORTANT for cosine similarity
    )
    return embedding.tolist()


