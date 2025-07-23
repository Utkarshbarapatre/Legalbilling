from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .config import settings

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class EmailSummary(Base):
    __tablename__ = "email_summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    email_id = Column(String, unique=True, index=True)
    subject = Column(String)
    sender = Column(String)
    recipient = Column(String)
    date_sent = Column(DateTime)
    original_content = Column(Text)
    summary = Column(Text)
    billing_hours = Column(String)
    billing_description = Column(Text)
    pushed_to_clio = Column(Boolean, default=False)
    clio_entry_id = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class ClioToken(Base):
    __tablename__ = "clio_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
