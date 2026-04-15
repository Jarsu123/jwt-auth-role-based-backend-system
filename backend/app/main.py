from fastapi import FastAPI
from .database import engine, Base
from .routers import user, notes
from fastapi.middleware.cors import CORSMiddleware
from .logging_config import setup_logging

# Initialize logging
logger = setup_logging()

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Notes API",
    description="Scalable REST API with Authentication & Role-Based Access",
    version="1.0.0"
)

# CORS configuration for Frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with explicit versioning
app.include_router(user.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["Notes"])

@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")