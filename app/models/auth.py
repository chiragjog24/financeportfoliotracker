from typing import List, Optional

from pydantic import BaseModel, EmailStr


class TokenData(BaseModel):
    sub: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    groups: List[str] = []


class UserInfo(BaseModel):
    sub: str
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    groups: List[str] = []


class TokenValidationResponse(BaseModel):
    valid: bool
    user: Optional[UserInfo] = None
    message: Optional[str] = None


class AuthStatusResponse(BaseModel):
    authenticated: bool
    user: Optional[UserInfo] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str


class DetailedHealthResponse(BaseModel):
    status: str
    version: str
    environment: str
    cognito_configured: bool
    api_keys_configured: bool
    database_configured: bool
    database_connected: bool
