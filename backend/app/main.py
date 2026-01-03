from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import logging

from .core.config import settings
from .db.mongo import connect_to_mongo, close_mongo_connection
from .routers import auth, complaints, officers, admin
from .ai import initialize_ai_engine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting AI Grievance Redressal API...")
    await connect_to_mongo()
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Initialize AI Engine
    try:
        logger.info("🤖 Loading AI Triage Engine...")
        initialize_ai_engine()
        logger.info("✅ AI Engine loaded successfully")
    except Exception as e:
        logger.error(f"❌ AI Engine failed to load: {e}")
        logger.warning("⚠️ System will use fallback triage")
    
    logger.info("✅ Application ready")
    yield
    
    # Shutdown
    await close_mongo_connection()
    logger.info("👋 Application shutdown complete")

app = FastAPI(
    title="AI Grievance Redressal API",
    description="PS12: AI-powered complaint management for public governance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(auth.router)
app.include_router(complaints.router)
app.include_router(officers.router)
app.include_router(admin.router)

@app.get("/")
async def root():
    return {
        "message": "AI Grievance Redressal API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational",
        "ai_enabled": True
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "ai": "enabled"}
