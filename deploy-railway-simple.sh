#!/bin/bash

echo "🚂 Fixed Railway Deployment"
echo "=========================="

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "Please login to Railway..."
railway login

# Initialize project if not already done
if [ ! -f "railway.toml" ]; then
    echo "Initializing Railway project..."
    railway init
fi

# Set environment variables
echo "Setting basic environment variables..."
railway variables set PORT=8000
railway variables set RAILWAY_ENVIRONMENT=production

# Deploy
echo "Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📝 Important next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Set these environment variables:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - CLIO_CLIENT_ID=your_clio_client_id"
echo "   - CLIO_CLIENT_SECRET=your_clio_client_secret"
echo "   - SECRET_KEY=$(openssl rand -base64 32)"
echo ""
echo "3. Get your Railway URL from the dashboard"
echo "4. Update Clio redirect URI: https://your-app.up.railway.app/callback"
echo "5. Test your deployment at the Railway URL"
echo ""
echo "🔗 Railway Dashboard: https://railway.app/dashboard"
