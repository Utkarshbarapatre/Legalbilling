from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    
    # Google/Gmail Configuration
    google_client_secret_file: str = "client_secret.json"
    google_scopes: str = "https://www.googleapis.com/auth/gmail.readonly"
    
    # Clio Configuration
    clio_client_id: str
    clio_client_secret: str
    clio_base_url: str = "https://app.clio.com"
    clio_redirect_uri: str = "http://127.0.0.1:8000/callback"
    
    # Application Configuration
    secret_key: str = os.getenv("SECRET_KEY", "oU9X3RQYFs2xx68UDTnAmcxqE-ZhJOBetRYumTol8Q")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    port: int = int(os.getenv("PORT", "8000"))
    
    # Database Configuration
    database_url: str = "sqlite:///./legal_billing.db"
    
    @property
    def google_scopes_list(self) -> List[str]:
        """Convert google_scopes string to list"""
        if isinstance(self.google_scopes, str):
            return [self.google_scopes]
        return self.google_scopes
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        # Allow extra fields to prevent validation errors
        extra = "ignore"

settings = Settings()
