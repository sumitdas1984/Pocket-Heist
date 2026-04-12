import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from backend.database import engine, Base
from backend.routers import auth, heists
from backend.dependencies import get_current_user
from backend.models import User

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pocket Heist API",
    description="A gamified task-assignment API with a spy/heist aesthetic",
    version="1.0.0"
)

# Configure CORS - allow localhost for dev + production origins from env
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite React dev server
    "http://localhost:8501",  # Streamlit default port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8501",
]

# Add production origins from environment variable (comma-separated)
env_origins = os.getenv("ALLOWED_ORIGINS", "")
if env_origins:
    allowed_origins.extend([origin.strip() for origin in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(heists.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Pocket Heist API"}


@app.get("/protected-test")
def protected_test(current_user: User = Depends(get_current_user)):
    """Test endpoint to verify authentication dependency works"""
    return {
        "message": "Authentication successful",
        "user": {
            "id": current_user.id,
            "username": current_user.username
        }
    }
