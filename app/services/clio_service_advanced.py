import httpx
from typing import Dict, List, Optional
from datetime import datetime
import logging
from ..core.config import settings

logger = logging.getLogger(__name__)

class AdvancedClioService:
    def __init__(self):
        self.base_url = settings.clio_base_url
        self.client_id = settings.clio_client_id
        self.client_secret = settings.clio_client_secret
        self.access_token = None
        self.redirect_uri = getattr(settings, 'clio_redirect_uri', 'http://127.0.0.1:8000/callback')
        self.default_matter_id = None
        self.user_id = None
    
    def get_auth_url(self) -> str:
        """Get Clio OAuth authorization URL with comprehensive scopes"""
        auth_url = f"{self.base_url}/oauth/authorize"
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': 'read write time_entries:write time_entries:read users:read matters:read activities:read'
        }
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        logger.info(f"Generated auth URL with comprehensive scopes")
        return f"{auth_url}?{query_string}"
    
    async def exchange_code_for_token(self, code: str) -> Dict:
        """Exchange authorization code for access token"""
        try:
            logger.info(f"Exchanging code for token")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/oauth/token",
                    data={
                        'client_id': self.client_id,
                        'client_secret': self.client_secret,
                        'code': code,
                        'grant_type': 'authorization_code',
                        'redirect_uri': self.redirect_uri
                    }
                )
                
                logger.info(f"Token exchange response status: {response.status_code}")
                
                if response.status_code == 200:
                    token_data = response.json()
                    self.access_token = token_data['access_token']
                    
                    # Initialize user info and default matter
                    await self.initialize_user_data()
                    
                    logger.info("Successfully exchanged code for access token")
                    return token_data
                else:
                    error_msg = f"Token exchange failed: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except httpx.RequestError as e:
            logger.error(f"Network error during token exchange: {e}")
            raise Exception(f"Network error: {e}")
        except Exception as e:
            logger.error(f"Error exchanging code for token: {e}")
            raise
    
    async def initialize_user_data(self):
        """Initialize user data and find default matter"""
        try:
            # Get user info
            user_info = await self.get_user_info_safe()
            if user_info:
                self.user_id = user_info.get('id')
            
            # Get default matter
            matters = await self.get_matters_safe()
            if matters and len(matters) > 0:
                # Use first active matter as default
                for matter in matters:
                    if matter.get('status') == 'Open':
                        self.default_matter_id = matter.get('id')
                        break
                
                # If no open matter, use first matter
                if not self.default_matter_id:
                    self.default_matter_id = matters[0].get('id')
            
            logger.info(f"Initialized: user_id={self.user_id}, default_matter={self.default_matter_id}")
            
        except Exception as e:
            logger.warning(f"Could not initialize user data: {e}")
    
    async def create_time_entry_advanced(self, summary_data: Dict) -> Dict:
        """Create a time entry with advanced error handling and fallbacks"""
        try:
            if not self.access_token:
                raise Exception("Not authenticated with Clio")
            
            # Prepare time entry data
            time_entry_data = {
                'data': {
                    'date': summary_data['date_sent'].strftime('%Y-%m-%d'),
                    'quantity': float(summary_data['billing_hours']),
                    'price': 250.00,  # Default rate - make configurable
                    'description': summary_data['billing_description'][:500],  # Limit description length
                    'type': 'TimeEntry'
                }
            }
            
            # Add user if available
            if self.user_id:
                time_entry_data['data']['user'] = {'id': self.user_id}
            
            # Add matter if available
            if self.default_matter_id:
                time_entry_data['data']['matter'] = {'id': self.default_matter_id}
            
            logger.info(f"Creating time entry: {time_entry_data}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v4/time_entries",
                    json=time_entry_data,
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    }
                )
                
                logger.info(f"Time entry response: {response.status_code} - {response.text}")
                
                if response.status_code in [200, 201]:
                    logger.info("Time entry created successfully")
                    return response.json()
                elif response.status_code == 422:
                    # Validation error - try with minimal data
                    return await self.create_minimal_time_entry(summary_data)
                else:
                    error_msg = f"Failed to create time entry: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except httpx.RequestError as e:
            logger.error(f"Network error creating time entry: {e}")
            raise Exception(f"Network error: {e}")
        except Exception as e:
            logger.error(f"Error creating time entry: {e}")
            raise
    
    async def create_minimal_time_entry(self, summary_data: Dict) -> Dict:
        """Create time entry with minimal required fields only"""
        try:
            minimal_data = {
                'data': {
                    'date': summary_data['date_sent'].strftime('%Y-%m-%d'),
                    'quantity': float(summary_data['billing_hours']),
                    'description': summary_data['billing_description'][:200],
                    'type': 'TimeEntry'
                }
            }
            
            logger.info(f"Creating minimal time entry: {minimal_data}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/v4/time_entries",
                    json=minimal_data,
                    headers={
                        'Authorization': f'Bearer {self.access_token}',
                        'Content-Type': 'application/json'
                    }
                )
                
                if response.status_code in [200, 201]:
                    logger.info("Minimal time entry created successfully")
                    return response.json()
                else:
                    error_msg = f"Failed to create minimal time entry: {response.status_code} - {response.text}"
                    logger.error(error_msg)
                    raise Exception(error_msg)
                    
        except Exception as e:
            logger.error(f"Error creating minimal time entry: {e}")
            raise
    
    async def get_user_info_safe(self) -> Optional[Dict]:
        """Safely get user info with fallbacks"""
        try:
            if not self.access_token:
                return None
                
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v4/users/who_am_i",
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                if response.status_code == 200:
                    return response.json()['data']
                else:
                    logger.warning(f"Could not get user info: {response.status_code}")
                    return None
                    
        except Exception as e:
            logger.warning(f"Error getting user info: {e}")
            return None
    
    async def get_matters_safe(self) -> List[Dict]:
        """Safely get matters list"""
        try:
            if not self.access_token:
                return []
                
            async with httpx.AsyncClient(timeout=15.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v4/matters?limit=50",
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                if response.status_code == 200:
                    return response.json()['data']
                else:
                    logger.warning(f"Could not get matters: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.warning(f"Error getting matters: {e}")
            return []
    
    async def test_connection(self) -> Dict:
        """Test the Clio connection and return status"""
        try:
            if not self.access_token:
                return {"connected": False, "error": "No access token"}
            
            # Test basic API access
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/api/v4/time_entries?limit=1",
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                if response.status_code == 200:
                    return {
                        "connected": True,
                        "message": "Connection successful",
                        "user_id": self.user_id,
                        "default_matter": self.default_matter_id
                    }
                else:
                    return {
                        "connected": False,
                        "error": f"API test failed: {response.status_code}"
                    }
                    
        except Exception as e:
            return {
                "connected": False,
                "error": str(e)
            }
