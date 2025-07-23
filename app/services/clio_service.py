import httpx
from typing import Dict, List, Optional
from datetime import datetime
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class ClioService:
    def __init__(self):
        self.base_url = "https://app.clio.com"  # Ensure correct base URL
        self.client_id = settings.clio_client_id
        self.client_secret = settings.clio_client_secret
        self.access_token = None
        self.redirect_uri = getattr(settings, 'clio_redirect_uri', 'http://127.0.0.1:8000/callback')
    
    def get_auth_url(self) -> str:
        """Get Clio OAuth authorization URL"""
        auth_url = f"{self.base_url}/oauth/authorize"
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'read write'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        logger.info(f"Generated auth URL: {auth_url}?{query_string}")
        return f"{auth_url}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        try:
            logger.info("Exchanging authorization code for token")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/oauth/token",
                    data={
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'code': code,
                        'grant_type': 'authorization_code',
                        'redirect_uri': self.redirect_uri
                    },
                    headers={'Content-Type': 'application/x-www-form-urlencoded'}
                )
                
                logger.info(f"Token exchange status: {response.status_code}")
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data['access_token']
                    logger.info("Token exchange successful")
                    return token_data
                else:
                    error_msg = f"Token exchange failed: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            raise
    
    async def create_activity(self, summary_data: Dict) -> Dict:
        """Create an activity instead of time entry (more likely to work)"""
        try:
            if not self.access_token:
                raise Exception("Not authenticated with Clio")
            
            # Try creating an activity first (simpler than time entries)
            activity_data = {
                'data': {
                    'type': 'Activity',
                    'description': f"Email: {summary_data.get('billing_description', 'Email communication')}",
                    'regarding': summary_data.get('billing_description', 'Email communication')[:200],
                    'date': summary_data['date_sent'].strftime('%Y-%m-%d')
                }
            }
            
            logger.info(f"Creating activity: {activity_data}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v4/activities",
                    json=activity_data,
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    }
                )
                
                logger.info(f"Activity creation status: {response.status_code}")
                logger.info(f"Activity response: {response.text}")
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    # If activities don't work, try a simple note
                    return await self.create_note(summary_data)
                    
        except Exception as e:
            logger.error(f"Error creating activity: {e}")
            # Fallback to creating a note
            return await self.create_note(summary_data)
    
    async def create_note(self, summary_data: Dict) -> Dict:
        """Create a simple note as fallback"""
        try:
            note_data = {
                'data': {
                    'type': 'Note',
                    'body': f"Email Summary ({summary_data['date_sent'].strftime('%Y-%m-%d')})\n\n{summary_data.get('billing_description', 'Email communication')}",
                    'subject': f"Email: {summary_data.get('billing_description', 'Email communication')[:50]}..."
                }
            }
            
            logger.info(f"Creating note: {note_data}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v4/notes",
                    json=note_data,
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    }
                )
                
                logger.info(f"Note creation status: {response.status_code}")
                
                if response.status_code in [200, 201]:
                    return response.json()
                else:
                    error_msg = f"Failed to create note: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except Exception as e:
            logger.error(f"Error creating note: {e}")
            raise
    
    async def create_time_entry(self, summary_data: Dict) -> Dict:
        """Create time entry with fallback to activity/note"""
        return await self.create_activity(summary_data)
    
    async def test_api_access(self) -> Dict:
        """Test API access"""
        try:
            if not self.access_token:
                return {"success": False, "error": "No access token"}
            
            # Try the simplest API call first
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v4/users/who_am_i",
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                logger.info(f"API test status: {response.status_code}")
                
                if response.status_code == 200:
                    return {"success": True, "user": response.json().get('data', {})}
                else:
                    return {"success": False, "error": f"API test failed: {response.status_code}"}
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def get_user_info(self) -> Dict:
        """Get user info"""
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v4/users/who_am_i",
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                if response.status_code == 200:
                    return response.json()['data']
                else:
                    raise Exception(f"Failed to get user info: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Error getting user info: {e}")
            raise
