from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional

from backend.enums import Difficulty, HeistStatus


class UserCreate(BaseModel):
    """Schema for user registration"""
    username: str
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: int
    username: str
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str = "bearer"


class HeistCreate(BaseModel):
    """Schema for creating a new heist"""
    title: str
    target: str
    difficulty: Difficulty
    assignee_username: str
    deadline: datetime
    description: Optional[str] = None

    @field_validator("deadline")
    @classmethod
    def deadline_must_be_future(cls, v: datetime) -> datetime:
        """Validate that deadline is in the future"""
        # Make comparison timezone-aware to handle both naive and aware datetimes
        now = datetime.now(timezone.utc)
        # If incoming datetime is naive, make it aware (assume UTC)
        if v.tzinfo is None:
            v = v.replace(tzinfo=timezone.utc)
        if v <= now:
            raise ValueError("deadline must be in the future")
        return v


class HeistResponse(BaseModel):
    """Schema for heist data in responses"""
    id: int
    title: str
    target: str
    difficulty: Difficulty
    assignee_username: str
    creator_username: str
    deadline: datetime
    description: Optional[str]
    status: HeistStatus
    created_at: datetime

    class Config:
        from_attributes = True
