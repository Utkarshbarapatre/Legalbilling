# Complete API Setup Guide

This guide provides step-by-step instructions for obtaining all required API keys and credentials for the Legal Billing Email Summarizer.

## 📋 Required API Keys Checklist

- [ ] OpenAI API Key
- [ ] Google Gmail API Credentials
- [ ] Clio API Credentials
- [ ] Application Secret Key

---

## 🤖 OpenAI API Setup

### Step 1: Create OpenAI Account
1. Go to [https://platform.openai.com/](https://platform.openai.com/)
2. Click "Sign up" or "Log in" if you have an account
3. Complete the registration process
4. Verify your email address

### Step 2: Add Payment Method
1. Go to [Billing Settings](https://platform.openai.com/account/billing)
2. Click "Add payment method"
3. Add a credit card (required for API access)
4. Set up billing limits if desired

### Step 3: Generate API Key
1. Navigate to [API Keys](https://platform.openai.com/account/api-keys)
2. Click "Create new secret key"
3. Give it a name (e.g., "Legal Billing App")
4. Copy the API key immediately (you won't see it again)
5. Add to your `.env` file:
   \`\`\`
   OPENAI_API_KEY=sk-your-api-key-here
   \`\`\`

### Step 4: Test API Access
\`\`\`bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

---

## 📧 Google Gmail API Setup

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Legal Billing Summarizer"
4. Click "Create"

### Step 2: Enable Gmail API
1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Gmail API"
3. Click on "Gmail API" and click "Enable"

### Step 3: Configure OAuth Consent Screen
1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in required fields:
   - App name: "Legal Billing Email Summarizer"
   - User support email: your email
   - Developer contact: your email
4. Click "Save and Continue"
5. Add scopes: Click "Add or Remove Scopes"
   - Search and add: `https://www.googleapis.com/auth/gmail.readonly`
6. Add test users (your email address)
7. Click "Save and Continue"

### Step 4: Create OAuth Credentials
1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose "Desktop application"
4. Name: "Legal Billing Desktop Client"
5. Click "Create"
6. Download the JSON file
7. Rename it to `client_secret.json`
8. Place it in your project root directory

### Step 5: Update Environment Variables
\`\`\`env
GOOGLE_CLIENT_SECRET_FILE=client_secret.json
\`\`\`

---

## ⚖️ Clio API Setup

### Step 1: Contact Clio Support
1. Log into your Clio account
2. Contact Clio support via:
   - Email: support@clio.com
   - Phone: 1-888-858-2546
   - In-app chat support

### Step 2: Request API Access
Send this template email:

\`\`\`
Subject: API Access Request for Legal Billing Integration

Dear Clio Support Team,

I am requesting API access for my Clio account to integrate with a custom legal billing application.

Account Details:
- Account Name: [Your Firm Name]
- Account Email: [Your Clio Email]
- Subscription Plan: [Your Plan]

Integration Purpose:
- Automated time entry creation from email summaries
- Legal billing workflow automation
- Internal use only (not for resale)

Technical Details:
- Application Name: Legal Billing Email Summarizer
- Redirect URI: http://localhost:8000/api/clio/callback
- Required Scopes: read, write
- OAuth 2.0 flow

Please provide:
1. Client ID
2. Client Secret
3. API documentation access

Thank you for your assistance.

Best regards,
[Your Name]
[Your Title]
[Your Firm]
\`\`\`

### Step 3: Receive Credentials
Clio will provide:
- Client ID
- Client Secret
- API documentation access

### Step 4: Update Environment Variables
\`\`\`env
CLIO_CLIENT_ID=your_client_id_here
CLIO_CLIENT_SECRET=your_client_secret_here
CLIO_BASE_URL=https://app.clio.com
\`\`\`

### Step 5: Test Clio Connection
1. Start your application: `uvicorn app.main:app --reload`
2. Go to http://localhost:8000
3. Click "Connect Clio" button
4. Complete OAuth flow
5. Verify connection in application

---

## 🔐 Application Secret Key

### Generate Secure Secret Key

**Option 1: Using OpenSSL (Recommended)**
\`\`\`bash
openssl rand -base64 32
\`\`\`

**Option 2: Using Python**
```python
import secrets
print(secrets.token_urlsafe(32))
