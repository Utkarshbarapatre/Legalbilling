#!/usr/bin/env python3
"""
Simple startup script for Legal Billing Email Summarizer
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

def main():
    """Main startup function"""
    # Load environment variables
    load_dotenv()
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    
    # Always use 127.0.0.1 for consistency
    host = "127.0.0.1"
    server_url = f"http://127.0.0.1:{port}"
    
    print("🚀 Starting Legal Billing Email Summarizer")
    print(f"📍 Server will run on: {server_url}")
    print(f"📚 API Documentation: {server_url}/docs")
    print(f"🔧 Health Check: {server_url}/health")
    print(f"🔗 OAuth Callback: {server_url}/callback")
    print(f"⚙️  Config Test: {server_url}/config-test")
    print(f"🔄 Redirect URI: http://127.0.0.1:{port}/callback")
    print("\n🔑 Configured APIs:")
    print(f"   • OpenAI: {'✓' if os.getenv('OPENAI_API_KEY') else '❌'}")
    print(f"   • Clio: {'✓' if os.getenv('CLIO_CLIENT_ID') else '❌'}")
    print(f"   • Google: {'✓' if os.path.exists('client_secret.json') else '❌'}")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
