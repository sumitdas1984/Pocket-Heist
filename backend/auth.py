"""
JWT authentication helpers
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt

# JWT Configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token

    Args:
        data: Dictionary containing claims to encode in the token
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    # Add issued at and expiration timestamps
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow()
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token

    Args:
        token: JWT token string to decode

    Returns:
        Dictionary containing decoded claims

    Raises:
        JWTError: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise


def verify_token(token: str) -> Optional[dict]:
    """
    Verify token and return payload if valid

    Args:
        token: JWT token string to verify

    Returns:
        Decoded payload dict if valid, None if invalid
    """
    try:
        payload = decode_access_token(token)
        return payload
    except JWTError:
        return None
