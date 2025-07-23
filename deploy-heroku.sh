#!/bin/bash

# Heroku deployment script
echo "Deploying to Heroku..."

# Login to Heroku (if not already logged in)
heroku login

# Create Heroku app (replace 'your-app-name' with your desired app name)
heroku create your-legal-billing-app

# Set environment variables
heroku config:set OPENAI_API_KEY=$OPENAI_API_KEY
heroku config:set CLIO_CLIENT_ID=$CLIO_CLIENT_ID
heroku config:set CLIO_CLIENT_SECRET=$CLIO_CLIENT_SECRET
heroku config:set SECRET_KEY=$(openssl rand -base64 32)

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

echo "Deployment complete!"
echo "Your app is available at: https://your-legal-billing-app.herokuapp.com"
