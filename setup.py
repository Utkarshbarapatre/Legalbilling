#!/usr/bin/env python3
"""
Setup script for Legal Billing Email Summarizer
Handles installation, configuration, and validation of the application
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from typing import List, Dict

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_colored(message: str, color: str = Colors.END):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.END}")

def print_header(title: str):
    """Print formatted header"""
    print_colored(f"\n{'='*60}", Colors.BLUE)
    print_colored(f"{title}", Colors.BOLD)
    print_colored(f"{'='*60}", Colors.BLUE)

def print_step(step: str, status: str = "info"):
    """Print step with appropriate color"""
    if status == "success":
        print_colored(f"✓ {step}", Colors.GREEN)
    elif status == "error":
        print_colored(f"❌ {step}", Colors.RED)
    elif status == "warning":
        print_colored(f"⚠️  {step}", Colors.YELLOW)
    else:
        print_colored(f"• {step}", Colors.BLUE)

def check_python_version():
    """Check if Python version is compatible"""
    print_step("Checking Python version...")
    
    if sys.version_info < (3, 8):
        print_step("Python 3.8 or higher is required", "error")
        print_colored(f"Current version: {sys.version}", Colors.RED)
        sys.exit(1)
    
    print_step(f"Python version: {sys.version.split()[0]}", "success")

def create_directories():
    """Create necessary directories"""
    print_step("Creating directories...")
    
    directories = [
        "logs",
        "static",
        "app",
        "app/core",
        "app/services",
        "app/routers"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print_step(f"Created directory: {directory}", "success")

def install_dependencies():
    """Install required dependencies"""
    print_step("Installing dependencies...")
    
    if not os.path.exists("requirements.txt"):
        print_step("requirements.txt not found", "error")
        sys.exit(1)
    
    try:
        # Upgrade pip first
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--upgrade", "pip"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Install requirements
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print_step("Dependencies installed successfully", "success")
        
    except subprocess.CalledProcessError as e:
        print_step("Failed to install dependencies", "error")
        print_colored(f"Error: {e}", Colors.RED)
        sys.exit(1)

def create_env_file():
    """Create .env file from template"""
    print_step("Setting up environment file...")
    
    if os.path.exists(".env"):
        print_step(".env file already exists", "success")
        return
    
    if os.path.exists(".env.example"):
        import shutil
        shutil.copy(".env.example", ".env")
        print_step("Created .env file from template", "success")
        print_step("Please edit .env file with your API keys", "warning")
    else:
        # Create basic .env file with correct format
        env_content = """# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# Google/Gmail Configuration
GOOGLE_CLIENT_SECRET_FILE=client_secret.json
GOOGLE_SCOPES=https://www.googleapis.com/auth/gmail.readonly

# Clio Configuration
CLIO_CLIENT_ID=your_clio_client_id_here
CLIO_CLIENT_SECRET=your_clio_client_secret_here
CLIO_BASE_URL=https://app.clio.com

# Application Configuration
SECRET_KEY=your-secret-key-change-in-production
DEBUG=false
PORT=8000

# Database Configuration
DATABASE_URL=sqlite:///./legal_billing.db
"""
        with open(".env", "w") as f:
            f.write(env_content)
        print_step("Created basic .env file", "success")
        print_step("Please edit .env file with your API keys", "warning")

def test_configuration():
    """Test configuration loading"""
    print_step("Testing configuration...")
    
    try:
        # Set test environment variables
        os.environ.setdefault('OPENAI_API_KEY', 'test-key')
        os.environ.setdefault('CLIO_CLIENT_ID', 'test-id')
        os.environ.setdefault('CLIO_CLIENT_SECRET', 'test-secret')
        
        # Test configuration loading
        subprocess.check_call([
            sys.executable, "test_config.py"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print_step("Configuration test passed", "success")
        return True
        
    except subprocess.CalledProcessError:
        print_step("Configuration test failed", "error")
        return False
    except Exception as e:
        print_step(f"Configuration test error: {e}", "warning")
        return False

def generate_secret_key():
    """Generate a secure secret key"""
    print_step("Generating secure secret key...")
    
    try:
        import secrets
        secret_key = secrets.token_urlsafe(32)
        
        # Update .env file
        if os.path.exists(".env"):
            with open(".env", "r") as f:
                content = f.read()
            
            # Replace the secret key line
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('SECRET_KEY='):
                    lines[i] = f'SECRET_KEY={secret_key}'
                    break
            
            with open(".env", "w") as f:
                f.write('\n'.join(lines))
            
            print_step("Secret key generated and updated in .env", "success")
        
    except Exception as e:
        print_step(f"Failed to generate secret key: {e}", "warning")

def print_next_steps():
    """Print next steps for the user"""
    print_header("Setup Complete!")
    
    print_colored("\n🎉 Legal Billing Email Summarizer is ready!", Colors.GREEN)
    
    print_colored("\n📋 Next Steps:", Colors.BOLD)
    print_colored("1. Configure API Keys:", Colors.BLUE)
    print_colored("   • Edit .env file with your API keys", Colors.END)
    print_colored("   • See API_SETUP_GUIDE.md for detailed instructions", Colors.END)
    
    print_colored("\n2. Download Google Credentials:", Colors.BLUE)
    print_colored("   • Download client_secret.json from Google Cloud Console", Colors.END)
    print_colored("   • Place it in the project root directory", Colors.END)
    
    print_colored("\n3. Start the Application:", Colors.BLUE)
    print_colored("   • Run: python run.py", Colors.END)
    print_colored("   • Or: uvicorn app.main:app --reload", Colors.END)
    print_colored("   • Visit: http://localhost:8000", Colors.END)
    
    print_colored("\n4. Test Configuration:", Colors.BLUE)
    print_colored("   • Run: python test_config.py", Colors.END)
    print_colored("   • Visit: http://localhost:8000/config-test", Colors.END)
    
    print_colored("\n📚 Documentation:", Colors.BOLD)
    print_colored("   • API_SETUP_GUIDE.md - Detailed API setup instructions", Colors.END)
    print_colored("   • README.md - Usage and deployment guide", Colors.END)
    
    print_colored(f"\n{'='*60}", Colors.BLUE)

def main():
    """Main setup function"""
    print_colored("🚀 Legal Billing Email Summarizer Setup", Colors.BOLD)
    print_colored("Automated setup and validation script", Colors.END)
    
    # Core setup steps
    print_header("Core Setup")
    check_python_version()
    create_directories()
    install_dependencies()
    create_env_file()
    
    # Generate secret key if needed
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            content = f.read()
            if "your-secret-key-change-in-production" in content:
                generate_secret_key()
    
    # Test configuration
    print_header("Validation")
    config_valid = test_configuration()
    
    # Summary
    print_header("Setup Summary")
    
    if config_valid:
        print_step("Setup completed successfully", "success")
    else:
        print_step("Setup completed with warnings", "warning")
    
    print_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_colored("\n\n❌ Setup interrupted by user", Colors.RED)
        sys.exit(1)
    except Exception as e:
        print_colored(f"\n\n❌ Setup failed with error: {e}", Colors.RED)
        sys.exit(1)
