# Legal Billing Email Summarizer

A streamlined FastAPI application that automatically fetches Gmail emails, generates AI-powered summaries for legal billing, and integrates with Clio for time tracking.

## Features

- 📧 **Gmail Integration**: Automatically fetch sent emails using Gmail API
- 🤖 **AI Summarization**: Generate professional billing summaries using OpenAI
- ⚖️ **Clio Integration**: Push time entries directly to Clio
- 📱 **Modern UI**: Clean, responsive interface with real-time status updates
- 🔐 **OAuth Authentication**: Secure authentication for Gmail and Clio

## Quick Start

### 1. Setup
\`\`\`bash
git clone <repository-url>
cd legal-billing-summarizer
python setup.py
\`\`\`

### 2. Configure APIs
Edit `.env` file with your API keys:
- OpenAI API key from [platform.openai.com](https://platform.openai.com/)
- Clio client ID and secret (contact Clio support)
- Download `client_secret.json` from Google Cloud Console

### 3. Test Configuration
\`\`\`bash
# Test that all dependencies are installed
python -c "import fastapi, openai, google.auth; print('✓ All dependencies installed')"

# Test environment variables
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
required = ['OPENAI_API_KEY', 'CLIO_CLIENT_ID', 'CLIO_CLIENT_SECRET']
missing = [var for var in required if not os.getenv(var) or os.getenv(var).startswith('your_')]
if missing:
    print(f'⚠️  Missing variables: {missing}')
else:
    print('✓ All environment variables configured')
"
\`\`\`

### 4. Run
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

Visit http://localhost:8000

## Environment Variables

\`\`\`env
OPENAI_API_KEY=your_openai_api_key_here
CLIO_CLIENT_ID=your_clio_client_id_here
CLIO_CLIENT_SECRET=your_clio_client_secret_here
GOOGLE_CLIENT_SECRET_FILE=client_secret.json
SECRET_KEY=your-secret-key
\`\`\`

## API Setup Guide

### OpenAI API
1. Go to [platform.openai.com](https://platform.openai.com/)
2. Create account and add payment method
3. Generate API key in API Keys section
4. Add to `.env` file

### Google Gmail API
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop application)
5. Download as `client_secret.json`

### Clio API
1. Contact Clio support: support@clio.com
2. Request API access for your account
3. Provide redirect URI: `http://localhost:8000/api/clio/callback`
4. Add client ID and secret to `.env`

## Deployment

### Heroku
\`\`\`bash
chmod +x deploy-heroku.sh
./deploy-heroku.sh
\`\`\`

### VPS
\`\`\`bash
chmod +x deploy-vps.sh
./deploy-vps.sh
\`\`\`

### Railway
1. Connect GitHub repository
2. Add environment variables
3. Deploy automatically

## Usage

1. **Connect Services**: Click "Connect Gmail" and "Connect Clio"
2. **Fetch Emails**: Click "Fetch Emails" to get recent sent emails
3. **Generate Summaries**: Click "Generate Summaries" to create AI summaries
4. **Push to Clio**: Click "Push to Clio" to create time entries

## API Endpoints

- `POST /api/gmail/authenticate` - Authenticate with Gmail
- `GET /api/gmail/emails` - Fetch emails from Gmail
- `GET /api/gmail/emails/stored` - Get stored emails
- `POST /api/summarizer/generate` - Generate AI summaries
- `GET /api/summarizer/summaries` - Get all summaries
- `PUT /api/summarizer/summaries/{id}` - Update a summary
- `POST /api/clio/push-entries` - Push entries to Clio
- `GET /health` - Health check

## Troubleshooting

### Common Issues

**Application won't start:**
\`\`\`bash
# Check Python version (3.8+ required)
python --version

# Install dependencies
pip install -r requirements.txt

# Check environment variables
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('OPENAI_API_KEY:', 'SET' if os.getenv('OPENAI_API_KEY') else 'MISSING')"
\`\`\`

**OpenAI API errors:**
- Verify API key is correct
- Check billing status at platform.openai.com
- Ensure sufficient credits

**Gmail connection fails:**
- Verify `client_secret.json` exists in project root
- Check OAuth consent screen is configured
- Ensure Gmail API is enabled

**Clio integration issues:**
- Verify redirect URI matches exactly
- Check client ID and secret are correct
- Contact Clio support if needed

### Testing Individual Components

\`\`\`bash
# Test OpenAI connection
python -c "
import openai
import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
try:
    models = openai.Model.list()
    print('✓ OpenAI connection successful')
except Exception as e:
    print(f'❌ OpenAI error: {e}')
"

# Test application startup
python -c "
try:
    from app.main import app
    print('✓ Application imports successfully')
except Exception as e:
    print(f'❌ Import error: {e}')
"
\`\`\`

## Development

\`\`\`bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Check logs
tail -f logs/app.log  # if logging is configured
\`\`\`

## License

MIT License
\`\`\`

Let me also update the API_SETUP_GUIDE.md to remove references to the validation script:
