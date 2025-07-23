from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Dict

from ..core.database import get_db, ClioToken, EmailSummary
from ..services.clio_service import ClioService
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

clio_service = ClioService()

@router.get("/auth")
async def clio_auth():
    """Initiate Clio OAuth flow"""
    try:
        auth_url = clio_service.get_auth_url()
        logger.info(f"Generated Clio auth URL: {auth_url}")
        return {"auth_url": auth_url}
    except Exception as e:
        logger.error(f"Clio auth error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/callback")
async def clio_callback(code: str = None, error: str = None, db: Session = Depends(get_db)):
    """Handle Clio OAuth callback"""
    try:
        # Check for OAuth errors
        if error:
            logger.error(f"OAuth error: {error}")
            return RedirectResponse(url="/?clio_error=true")
        
        if not code:
            logger.error("No authorization code received")
            return RedirectResponse(url="/?clio_error=no_code")
        
        logger.info(f"Received authorization code: {code[:10]}...")
        
        # Exchange code for token
        token_data = await clio_service.exchange_code_for_token(code)
        
        # Store token in database
        clio_token = ClioToken(
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token', ''),
            expires_at=None  # Calculate from expires_in if provided
        )
        db.add(clio_token)
        db.commit()
        
        logger.info("Clio token stored successfully")
        return RedirectResponse(url="/?clio_connected=true")
        
    except Exception as e:
        logger.error(f"Clio callback error: {e}")
        return RedirectResponse(url=f"/?clio_error={str(e)}")

@router.get("/test")
async def test_clio_connection(db: Session = Depends(get_db)):
    """Test Clio API connection"""
    try:
        token = db.query(ClioToken).order_by(ClioToken.created_at.desc()).first()
        
        if not token:
            return {"connected": False, "message": "No token found"}
        
        # Set token in service and test connection
        clio_service.access_token = token.access_token
        
        # Test API access
        test_result = await clio_service.test_api_access()
        
        return {
            "connected": test_result["success"],
            "message": test_result.get("message", test_result.get("error", "Unknown")),
            "user": test_result.get("user", {})
        }
            
    except Exception as e:
        logger.error(f"Error testing Clio connection: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def clio_status(db: Session = Depends(get_db)):
    """Check Clio connection status"""
    try:
        token = db.query(ClioToken).order_by(ClioToken.created_at.desc()).first()
        
        if not token:
            return {"connected": False, "message": "No token found"}
        
        # Set token in service and test connection
        clio_service.access_token = token.access_token
        
        try:
            user_info = await clio_service.get_user_info()
            return {
                "connected": True,
                "user": user_info.get('name', 'Unknown'),
                "message": "Connected successfully"
            }
        except Exception as e:
            return {
                "connected": False,
                "message": f"Token invalid: {str(e)}"
            }
            
    except Exception as e:
        logger.error(f"Error checking Clio status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/push-entries")
async def push_to_clio(db: Session = Depends(get_db)):
    """Push email summaries to Clio as time entries"""
    try:
        # Get latest token
        token = db.query(ClioToken).order_by(ClioToken.created_at.desc()).first()
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated with Clio")
        
        clio_service.access_token = token.access_token
        
        # Test API access first
        api_test = await clio_service.test_api_access()
        if not api_test["success"]:
            raise HTTPException(status_code=401, detail=f"Clio API access failed: {api_test['error']}")
        
        # Get unsent summaries
        summaries = db.query(EmailSummary).filter(
            EmailSummary.pushed_to_clio == False,
            EmailSummary.summary.isnot(None)
        ).all()
        
        if not summaries:
            return {
                "success": True,
                "message": "No summaries to push",
                "pushed_count": 0,
                "total_summaries": 0
            }
        
        pushed_count = 0
        errors = []
        
        for summary in summaries:
            try:
                summary_data = {
                    'date_sent': summary.date_sent,
                    'billing_hours': summary.billing_hours or '0.25',
                    'billing_description': summary.billing_description or summary.summary[:200]
                }
                
                result = await clio_service.create_time_entry(summary_data)
                
                # Update summary as pushed
                summary.pushed_to_clio = True
                summary.clio_entry_id = str(result.get('data', {}).get('id', ''))
                db.commit()
                
                pushed_count += 1
                logger.info(f"Pushed summary {summary.id} to Clio")
                
            except Exception as e:
                error_msg = f"Email {summary.email_id}: {str(e)}"
                errors.append(error_msg)
                logger.error(f"Error pushing summary {summary.id}: {e}")
        
        return {
            "success": True,
            "pushed_count": pushed_count,
            "total_summaries": len(summaries),
            "errors": errors
        }
        
    except Exception as e:
        logger.error(f"Error pushing to Clio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matters")
async def get_matters(db: Session = Depends(get_db)):
    """Get Clio matters/cases"""
    try:
        token = db.query(ClioToken).order_by(ClioToken.created_at.desc()).first()
        if not token:
            raise HTTPException(status_code=401, detail="Not authenticated with Clio")
        
        clio_service.access_token = token.access_token
        matters = await clio_service.get_matters()
        
        return {"matters": matters}
        
    except Exception as e:
        logger.error(f"Error getting matters: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/disconnect")
async def disconnect_clio(db: Session = Depends(get_db)):
    """Disconnect from Clio by removing stored tokens"""
    try:
        # Delete all tokens
        db.query(ClioToken).delete()
        db.commit()
        
        # Clear service token
        clio_service.access_token = None
        
        logger.info("Clio disconnected successfully")
        return {"success": True, "message": "Disconnected from Clio"}
        
    except Exception as e:
        logger.error(f"Error disconnecting from Clio: {e}")
        raise HTTPException(status_code=500, detail=str(e))
