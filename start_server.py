#!/usr/bin/env python3
"""
Simple startup script with better error handling
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        "app/main.py",
        "static/index.html",
        "static/styles.css",
        "static/app.js",
        ".env"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def check_environment():
    """Check environment variables"""
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'CLIO_CLIENT_ID', 'CLIO_CLIENT_SECRET']
    missing_vars = []
    
    for var in required_vars:
        value = os.getenv(var)
        if not value or value.startswith('your_'):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠️  Missing or incomplete environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please edit your .env file with the correct values")
        return False
    
    print("✅ Environment variables configured")
    return True

def start_server():
    """Start the server"""
    try:
        print("🚀 Starting Legal Billing Email Summarizer...")
        print("📍 Server will be available at: http://127.0.0.1:8000")
        print("📚 API Documentation: http://127.0.0.1:8000/docs")
        print("🔧 Health Check: http://127.0.0.1:8000/health")
        print("\nPress Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "app.main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000", 
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the project directory")
        print("2. Check that all files exist")
        print("3. Verify your .env file is configured")
        print("4. Try: pip install -r requirements.txt")

def main():
    """Main function"""
    print("🔍 Checking system requirements...")
    
    if not check_requirements():
        print("\n❌ Setup incomplete. Please ensure all files are present.")
        return
    
    if not check_environment():
        print("\n⚠️  Environment not fully configured, but starting anyway...")
        print("You can configure it later in the .env file")
    
    start_server()

if __name__ == "__main__":
    main()
