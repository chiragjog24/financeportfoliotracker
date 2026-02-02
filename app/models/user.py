from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.db.base import BaseModel


class User(BaseModel, table=True):
    """User model for local authentication"""
    
    __tablename__ = "users"
    
    email: str = Field(unique=True, index=True, nullable=False, description="User email address")
    hashed_password: str = Field(nullable=False, description="Hashed password")
    is_active: bool = Field(default=True, nullable=False, description="Whether user account is active")
    is_verified: bool = Field(default=False, nullable=False, description="Whether email is verified")
    full_name: Optional[str] = Field(default=None, nullable=True, description="User's full name")
    
    # Timestamps are inherited from BaseModel (created_at, updated_at)
    
    def __repr__(self) -> str:
        return f"<User {self.email}>"
