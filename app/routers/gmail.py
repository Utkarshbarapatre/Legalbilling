from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

from ..core.database import get_db, EmailSummary
from ..services.gmail_service import GmailService
from ..core.config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

gmail_service = GmailService(
    credentials_file=settings.google_client_secret_file,
    scopes=settings.google_scopes_list  # Use the property that returns a list
)

@router.post("/authenticate")
async def authenticate_gmail():
    """Authenticate with Gmail API"""
    try:
        success = gmail_service.authenticate()
        return {"success": success, "message": "Gmail authentication successful"}
    except Exception as e:
        logger.error(f"Gmail authentication error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emails")
async def fetch_emails(
    days_back: int = 7,
    max_results: int = 50,
    db: Session = Depends(get_db)
):
    """Fetch sent emails from Gmail"""
    try:
        emails = gmail_service.get_sent_emails(days_back, max_results)
        
        # Store emails in database
        stored_emails = []
        for email_data in emails:
            # Check if email already exists
            existing = db.query(EmailSummary).filter(
                EmailSummary.email_id == email_data['id']
            ).first()
            
            if not existing:
                email_summary = EmailSummary(
                    email_id=email_data['id'],
                    subject=email_data['subject'],
                    sender=email_data['sender'],
                    recipient=email_data['recipient'],
                    date_sent=email_data['date_sent'],
                    original_content=email_data['body']
                )
                db.add(email_summary)
                db.commit()
                stored_emails.append(email_data)
        
        return {
            "success": True,
            "emails_fetched": len(emails),
            "new_emails": len(stored_emails),
            "emails": emails
        }
        
    except Exception as e:
        logger.error(f"Error fetching emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/emails/stored")
async def get_stored_emails(db: Session = Depends(get_db)):
    """Get emails stored in database"""
    try:
        emails = db.query(EmailSummary).order_by(EmailSummary.date_sent.desc()).all()
        return {"emails": emails}
    except Exception as e:
        logger.error(f"Error getting stored emails: {e}")
        raise HTTPException(status_code=500, detail=str(e))
