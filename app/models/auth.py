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
    full_name: Optional[str] = None


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
    jwt_configured: bool
    api_keys_configured: bool
    database_configured: bool
    database_connected: bool


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
