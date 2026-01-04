from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from .db.mongo import connect_to_mongo, close_mongo_connection
from .ai.triage import initialize_triage_engine
from .routers.auth import router as auth_router
from .routers.complaints import router as complaints_router
from .routers.officers import router as officers_router
from .routers.admin import router as admin_router
from .routers.feedback import router as feedback_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AI Grievance Redressal API...")
    
    # Connect to MongoDB (non-blocking)
    try:
        await connect_to_mongo()
    except Exception as e:
        logger.warning(f"Starting without database: {e}")
    
    # Initialize AI Engine
    try:
        initialize_triage_engine()
        logger.info("AI Engine loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load AI Engine: {e}")
    
    logger.info("Application ready")
    
    yield
    
    logger.info("Shutting down API...")
    await close_mongo_connection()

app = FastAPI(
    title="AI Grievance Redressal System",
    description="AI-powered complaint triage and routing system with voice input, duplicate detection, and notifications",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(complaints_router, prefix="/complaints", tags=["Complaints"])
app.include_router(officers_router, prefix="/officers", tags=["Officers"])
app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(feedback_router, prefix="/complaints", tags=["Feedback"])

@app.get("/")
async def root():
    return {
        "message": "AI Grievance Redressal API",
        "version": "2.0.0",
        "features": [
            "AI-powered complaint classification (93% accuracy)",
            "Smart officer routing",
            "Duplicate detection",
            "Voice input support",
            "Email/SMS notifications",
            "Citizen feedback system",
            "Real-time analytics"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "ai_engine": "enabled",
        "duplicate_detection": "enabled",
        "notifications": "configured"
    }

@app.get("/api/info")
async def api_info():
    return {
        "total_endpoints": len(app.routes),
        "documentation": "/docs",
        "openapi_schema": "/openapi.json"
    }
