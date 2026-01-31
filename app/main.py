from fastapi import FastAPI
from app.database import Base, engine
from app.routes import auth, consent, audit
from app.routes import documents
from app.routes import retrieval

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthcare AI Agent")

app.include_router(auth.router)
app.include_router(consent.router)
app.include_router(audit.router)
app.include_router(documents.router)
app.include_router(retrieval.router)
