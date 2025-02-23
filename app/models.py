from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB  # Import PostgreSQL JSONB
from datetime import datetime
from .database import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, index=True)
    type = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    # payload = Column(String)  # JSON stored as string
    payload = Column(JSONB)  #  Change payload to JSONB

