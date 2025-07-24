from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager

from .routers import gmail, clio, summarizer, extension
from .core.config import settings
from .core.database import init_db, get_db, ClioToken
from .services.clio_service import ClioService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up Legal Billing Email Summarizer")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down")

app = FastAPI(
    title="Legal Billing Email Summarizer",
    description="Automatically fetch Gmail emails, generate AI summaries, and integrate with Clio",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(gmail.router, prefix="/api/gmail", tags=["Gmail"])
app.include_router(clio.router, prefix="/api/clio", tags=["Clio"])
app.include_router(summarizer.router, prefix="/api/summarizer", tags=["Summarizer"])
app.include_router(extension.router, prefix="/api/extension", tags=["Extension"])

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# OAuth callback route at root level to match Clio configuration
@app.get("/callback")
async def oauth_callback(code: str = None, error: str = None, db: Session = Depends(get_db)):
    """Handle OAuth callback from Clio"""
    try:
        logger.info(f"OAuth callback received - code: {'present' if code else 'missing'}, error: {error}")
        
        # Check for OAuth errors
        if error:
            logger.error(f"OAuth error: {error}")
            return RedirectResponse(url="/?clio_error=true")
        
        if not code:
            logger.error("No authorization code received")
            return RedirectResponse(url="/?clio_error=no_code")
        
        logger.info(f"Received authorization code: {code[:10]}...")
        
        # Create Clio service and exchange code for token
        clio_service = ClioService()
        token_data = await clio_service.exchange_code_for_token(code)
        
        # Store token in database
        clio_token = ClioToken(
            access_token=token_data['access_token'],
            refresh_token=token_data.get('refresh_token', ''),
            expires_at=None
        )
        db.add(clio_token)
        db.commit()
        
        logger.info("Clio token stored successfully")
        return RedirectResponse(url="/?clio_connected=true")
        
    except Exception as e:
        logger.error(f"OAuth callback error: {e}")
        return RedirectResponse(url=f"/?clio_error={str(e)}")

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main application page"""
    try:
        with open("static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
            <head>
                <title>Legal Billing Email Summarizer</title>
                <style>
                    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
                    .header { text-align: center; margin-bottom: 30px; }
                    .status { background: #f0f9ff; border: 1px solid #0ea5e9; padding: 15px; border-radius: 8px; margin: 20px 0; }
                    .links { display: flex; gap: 15px; justify-content: center; margin: 20px 0; }
                    .links a { background: #3b82f6; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; }
                    .links a:hover { background: #2563eb; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>⚖️ Legal Billing Email Summarizer</h1>
                    <p>FastAPI backend is running successfully!</p>
                </div>
                
                <div class="status">
                    <h3>🚀 Application Status</h3>
                    <p>✅ FastAPI server is running</p>
                    <p>📁 Static files not found - using fallback interface</p>
                    <p>🔗 API documentation available below</p>
                </div>
                
                <div class="links">
                    <a href="/docs">📚 API Documentation</a>
                    <a href="/health">🔧 Health Check</a>
                    <a href="/clio-test">🧪 Clio Test</a>
                </div>
                
                <div style="margin-top: 30px;">
                    <h3>📋 Next Steps:</h3>
                    <ol>
                        <li>Upload your static files to the <code>static/</code> directory</li>
                        <li>Configure your environment variables</li>
                        <li>Test the API endpoints above</li>
                        <li>Set up OAuth with Gmail and Clio</li>
                    </ol>
                </div>
            </body>
        </html>
        """)

@app.get("/clio-test", response_class=HTMLResponse)
async def clio_test():
    """Serve the Clio test page"""
    try:
        with open("static/clio-test.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Clio test page not found</h1><p><a href='/'>Back to home</a></p>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Legal Billing Email Summarizer",
        "version": "1.0.0",
        "port": os.getenv("PORT", "8000"),
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development")
    }

@app.get("/config-test")
async def config_test():
    """Test configuration endpoint"""
    return {
        "openai_configured": bool(os.getenv("OPENAI_API_KEY")),
        "clio_configured": bool(os.getenv("CLIO_CLIENT_ID")),
        "port": os.getenv("PORT", "8000"),
        "environment": os.getenv("RAILWAY_ENVIRONMENT", "development"),
        "database_url": settings.database_url,
        "clio_redirect_uri": settings.clio_redirect_uri
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=False
    )
