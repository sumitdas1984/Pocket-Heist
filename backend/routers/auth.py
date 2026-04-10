"""
Authentication API endpoints
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas import UserCreate, UserResponse, TokenResponse
from backend.user_service import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    - **username**: Unique username for the account
    - **password**: Password (minimum 8 characters)

    Returns the created user data (without password)
    """
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(username: str, password: str, db: Session = Depends(get_db)):
    """
    Login with username and password

    - **username**: Your username
    - **password**: Your password

    Returns a JWT access token for authenticated requests
    """
    return authenticate_user(db, username, password)
