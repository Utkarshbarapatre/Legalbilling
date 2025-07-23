from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict
import logging
from datetime import datetime

from ..core.database import get_db, EmailSummary
from ..services.openai_service import OpenAIService

router = APIRouter()
logger = logging.getLogger(__name__)

openai_service = OpenAIService()

@router.post("/capture-email")
async def capture_email_from_extension(
    email_data: Dict,
    db: Session = Depends(get_db)
):
    """Capture email data from Chrome extension"""
    try:
        # Generate a unique ID for the email
        email_id = f"ext_{hash(email_data.get('url', '') + email_data.get('captured_at', ''))}"
        
        # Check if email already exists
        existing = db.query(EmailSummary).filter(
            EmailSummary.email_id == email_id
        ).first()
        
        if existing:
            return {
                "success": True,
                "message": "Email already captured",
                "email_id": email_id
            }
        
        # Parse date
        try:
            if email_data.get('date_sent'):
                date_sent = datetime.fromisoformat(email_data['date_sent'].replace('Z', '+00:00'))
            else:
                date_sent = datetime.now()
        except:
            date_sent = datetime.now()
        
        # Create email summary record
        email_summary = EmailSummary(
            email_id=email_id,
            subject=email_data.get('subject', 'No Subject'),
            sender=email_data.get('sender', 'Unknown'),
            recipient=email_data.get('recipient', 'Unknown'),
            date_sent=date_sent,
            original_content=email_data.get('body', '')
        )
        
        db.add(email_summary)
        db.commit()
        
        logger.info(f"Captured email from extension: {email_id}")
        
        return {
            "success": True,
            "message": "Email captured successfully",
            "email_id": email_id
        }
        
    except Exception as e:
        logger.error(f"Error capturing email from extension: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-summarize")
async def auto_summarize_latest(db: Session = Depends(get_db)):
    """Automatically summarize the latest unsummarized email"""
    try:
        # Get the latest email without a summary
        email = db.query(EmailSummary).filter(
            EmailSummary.summary.is_(None)
        ).order_by(EmailSummary.created_at.desc()).first()
        
        if not email:
            return {
                "success": True,
                "message": "No emails need summarization"
            }
        
        # Generate summary
        email_data = {
            'subject': email.subject,
            'sender': email.sender,
            'recipient': email.recipient,
            'date_sent': email.date_sent,
            'body': email.original_content
        }
        
        summary_result = await openai_service.generate_billing_summary(email_data)
        
        # Update email with summary
        email.summary = summary_result['summary']
        email.billing_hours = summary_result['billing_hours']
        email.billing_description = summary_result['billing_description']
        
        db.commit()
        
        logger.info(f"Auto-summarized email: {email.email_id}")
        
        return {
            "success": True,
            "message": "Email summarized successfully",
            "summary": summary_result
        }
        
    except Exception as e:
        logger.error(f"Error auto-summarizing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats")
async def get_extension_stats(db: Session = Depends(get_db)):
    """Get statistics for the extension"""
    try:
        total_emails = db.query(EmailSummary).count()
        total_summaries = db.query(EmailSummary).filter(
            EmailSummary.summary.isnot(None)
        ).count()
        
        recent_emails = db.query(EmailSummary).filter(
            EmailSummary.created_at >= datetime.now().replace(hour=0, minute=0, second=0)
        ).count()
        
        return {
            "total_emails": total_emails,
            "total_summaries": total_summaries,
            "recent_emails": recent_emails,
            "success": True
        }
        
    except Exception as e:
        logger.error(f"Error getting extension stats: {e}")
        raise HTTPException(status_code=500, detail=str(e))
