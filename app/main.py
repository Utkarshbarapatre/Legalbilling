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
    """Handle OAuth callback from Clio (matches redirect URI: http://127.0.0.1:8000/callback)"""
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
            expires_at=None  # Calculate from expires_in if provided
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
        <html>
            <head><title>Legal Billing Email Summarizer</title></head>
            <body>
                <h1>Legal Billing Email Summarizer</h1>
                <p>Static files not found. Please ensure static/index.html exists.</p>
                <p>API is running at <a href="/docs">/docs</a></p>
                <p>OAuth callback: <a href="/callback">/callback</a></p>
                <p>Clio Test: <a href="/clio-test">Clio Test Page</a></p>
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
        return HTMLResponse(content="<h1>Clio test page not found</h1>")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Legal Billing Email Summarizer",
        "version": "1.0.0",
        "port": settings.port,
        "clio_redirect_uri": settings.clio_redirect_uri
    }

@app.get("/config-test")
async def config_test():
    """Test configuration endpoint"""
    return {
        "openai_model": settings.openai_model,
        "port": settings.port,
        "database_url": settings.database_url,
        "google_scopes": settings.google_scopes_list,
        "clio_base_url": settings.clio_base_url,
        "clio_redirect_uri": settings.clio_redirect_uri,
        "clio_client_id": settings.clio_client_id[:10] + "..." if settings.clio_client_id else "Not set"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=settings.port,
        reload=True
    )
