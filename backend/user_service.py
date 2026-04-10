"""
User service layer for registration and authentication
"""
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status

from backend.models import User
from backend.schemas import UserCreate, UserResponse, TokenResponse
from backend.auth import create_access_token

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def register_user(db: Session, user_data: UserCreate) -> UserResponse:
    """
    Register a new user

    Args:
        db: Database session
        user_data: User registration data

    Returns:
        UserResponse with created user data

    Raises:
        HTTPException 409: If username already exists
    """
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already registered"
        )

    # Hash the password
    hashed_password = hash_password(user_data.password)

    # Create new user
    db_user = User(
        username=user_data.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse.model_validate(db_user)


def authenticate_user(db: Session, username: str, password: str) -> TokenResponse:
    """
    Authenticate a user and return JWT token

    Args:
        db: Database session
        username: User's username
        password: User's password (plaintext)

    Returns:
        TokenResponse with access token

    Raises:
        HTTPException 401: If credentials are invalid
    """
    # Find user by username
    user = db.query(User).filter(User.username == username).first()

    # Check if user exists
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create JWT token
    token_data = {
        "sub": user.username,
        "user_id": user.id
    }
    access_token = create_access_token(data=token_data)

    return TokenResponse(access_token=access_token)
