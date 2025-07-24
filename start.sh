#!/bin/bash

# Start script for Railway deployment
echo "🚀 Starting Legal Billing Email Summarizer"

# Start Python FastAPI server in background
echo "📡 Starting FastAPI server..."
cd /app
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait a moment for FastAPI to start
sleep 5

# Start Next.js server
echo "🌐 Starting Next.js server..."
npm start &
NEXTJS_PID=$!

# Function to handle shutdown
shutdown() {
    echo "🛑 Shutting down services..."
    kill $FASTAPI_PID $NEXTJS_PID
    wait $FASTAPI_PID $NEXTJS_PID
    echo "✅ Services stopped"
    exit 0
}

# Trap signals
trap shutdown SIGTERM SIGINT

# Wait for both processes
wait $FASTAPI_PID $NEXTJS_PID
