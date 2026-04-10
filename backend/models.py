from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database import Base
from backend.enums import Difficulty, HeistStatus


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to heists created by this user
    heists = relationship("Heist", back_populates="creator")


class Heist(Base):
    __tablename__ = "heists"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    target = Column(String, nullable=False)
    difficulty = Column(SQLEnum(Difficulty), nullable=False)
    assignee_username = Column(String, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    deadline = Column(DateTime, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(HeistStatus), default=HeistStatus.active, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship to creator
    creator = relationship("User", back_populates="heists")
