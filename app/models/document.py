

from sqlalchemy import Column, Integer, String, Date
from app.database import Base
from datetime import date


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, index=True)
    filename = Column(String)
    filepath = Column(String)

    doc_type = Column(String, index=True)
    visit_date = Column(Date, index=True)
