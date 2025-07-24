#!/bin/bash

echo "🚂 Fixed Railway Deployment (127.0.0.1 Compatible)"
echo "================================================="

# Test local configuration first
echo "🧪 Testing local configuration..."
if [ -f "test-local-first.sh" ]; then
    chmod +x test-local-first.sh
    ./test-local-first.sh
    
    read -p "Continue with Railway deployment? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Deployment cancelled."
        exit 1
    fi
fi

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

# Set environment variables with 127.0.0.1 configuration
echo "Setting environment variables..."
railway variables set PORT=8000
railway variables set RAILWAY_ENVIRONMENT=production
railway variables set CLIO_REDIRECT_URI="http://127.0.0.1:8000/callback"

# Deploy
echo "Deploying to Railway..."
railway up

echo ""
echo "✅ Deployment initiated!"
echo ""
echo "📝 Important next steps:"
echo "1. Go to your Railway dashboard"
echo "2. Get your Railway URL (e.g., https://your-app.up.railway.app)"
echo "3. Set these environment variables in Railway dashboard:"
echo "   - OPENAI_API_KEY=your_openai_key"
echo "   - CLIO_CLIENT_ID=your_clio_client_id"
echo "   - CLIO_CLIENT_SECRET=your_clio_client_secret"
echo "   - SECRET_KEY=$(openssl rand -base64 32)"
echo "   - CLIO_REDIRECT_URI=https://your-app.up.railway.app/callback"
echo ""
echo "4. Update Clio app settings with Railway URL:"
echo "   - Redirect URI: https://your-app.up.railway.app/callback"
echo ""
echo "5. Test your deployment:"
echo "   - Health: https://your-app.up.railway.app/health"
echo "   - Config: https://your-app.up.railway.app/config-test"
echo "   - Main app: https://your-app.up.railway.app/"
echo ""
echo "🔗 Railway Dashboard: https://railway.app/dashboard"
echo ""
echo "⚠️  Note: Local development uses 127.0.0.1:8000"
echo "   Production uses your Railway domain"
