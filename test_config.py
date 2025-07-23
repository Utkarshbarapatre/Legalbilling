#!/usr/bin/env python3
"""
Test script to verify configuration loading
"""

def test_config():
    """Test configuration loading"""
    try:
        print("Testing configuration loading...")
        
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Test settings import
        from app.core.config import settings
        
        print("✓ Configuration loaded successfully")
        print(f"✓ OpenAI Model: {settings.openai_model}")
        print(f"✓ Port: {settings.port}")
        print(f"✓ Database URL: {settings.database_url}")
        print(f"✓ Google Scopes: {settings.google_scopes_list}")
        
        # Check required fields
        required_fields = ['openai_api_key', 'clio_client_id', 'clio_client_secret']
        missing_fields = []
        
        for field in required_fields:
            value = getattr(settings, field)
            if not value or value.startswith('your_'):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"⚠️  Missing configuration: {', '.join(missing_fields)}")
        else:
            print("✓ All required fields configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    test_config()
