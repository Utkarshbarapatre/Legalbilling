#!/bin/bash

echo "🚂 Simple Railway Deployment"
echo "============================"

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "Installing Railway CLI..."
    npm install -g @railway/cli
fi

# Login to Railway
echo "Please login to Railway..."
railway login

# Initialize project
echo "Initializing Railway project..."
railway init

# Set environment variables
echo "Setting environment variables..."
railway variables set PORT=8000
railway variables set NODE_ENV=production

# Deploy
echo "Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "1. Set your environment variables in Railway dashboard:"
echo "   - OPENAI_API_KEY"
echo "   - CLIO_CLIENT_ID" 
echo "   - CLIO_CLIENT_SECRET"
echo "   - SECRET_KEY"
echo ""
echo "2. Update your Clio redirect URI with the Railway URL"
echo "3. Test your application"
