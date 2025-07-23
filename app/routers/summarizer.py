from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db, EmailSummary
from ..services.openai_service import OpenAIService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

openai_service = OpenAIService()

@router.post("/generate")
async def generate_summaries(db: Session = Depends(get_db)):
    """Generate AI summaries for emails without summaries"""
    try:
        # Get emails without summaries
        emails = db.query(EmailSummary).filter(
            EmailSummary.summary.is_(None)
        ).all()
        
        if not emails:
            return {
                "success": True,
                "message": "No emails need summarization",
                "summaries_generated": 0
            }
        
        summaries_generated = 0
        errors = []
        
        for email in emails:
            try:
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
                summaries_generated += 1
                
            except Exception as e:
                error_msg = f"Email {email.email_id}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Error generating summary for email {email.id}: {e}")
        
        return {
            "success": True,
            "summaries_generated": summaries_generated,
            "total_emails": len(emails),
            "errors": errors
        }
        
    except Exception as e:
        logger.error(f"Error generating summaries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summaries")
async def get_summaries(db: Session = Depends(get_db)):
    """Get all email summaries"""
    try:
        summaries = db.query(EmailSummary).filter(
            EmailSummary.summary.isnot(None)
        ).order_by(EmailSummary.date_sent.desc()).all()
        
        return {"summaries": summaries}
        
    except Exception as e:
        logger.error(f"Error getting summaries: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/summaries/{summary_id}")
async def update_summary(
    summary_id: int,
    summary_data: dict,
    db: Session = Depends(get_db)
):
    """Update a specific summary"""
    try:
        summary = db.query(EmailSummary).filter(EmailSummary.id == summary_id).first()
        if not summary:
            raise HTTPException(status_code=404, detail="Summary not found")
        
        # Update fields
        if 'billing_description' in summary_data:
            summary.billing_description = summary_data['billing_description']
        if 'billing_hours' in summary_data:
            summary.billing_hours = summary_data['billing_hours']
        if 'summary' in summary_data:
            summary.summary = summary_data['summary']
        
        db.commit()
        
        return {"success": True, "message": "Summary updated"}
        
    except Exception as e:
        logger.error(f"Error updating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
