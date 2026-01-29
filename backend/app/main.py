"""
SmartResume Analyzer - Main FastAPI Application
Entry point for the backend API server
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analyze
from app.core.config import settings
from app.utils.logger import logger

# Initialize FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered CV analysis platform that matches resumes with job descriptions",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(analyze.router, prefix="/api", tags=["Analysis"])


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"Starting {settings.APP_NAME} v1.0.0")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"AI Provider: {settings.AI_PROVIDER}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown"""
    logger.info(f"Shutting down {settings.APP_NAME}")


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "checks": {
            "api": "operational",
            "ai_service": "configured" if settings.AI_API_KEY else "missing_key",
        }
    }
