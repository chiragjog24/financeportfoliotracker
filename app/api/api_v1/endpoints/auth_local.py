from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import CurrentUserDep, OptionalUserDep
from app.db.deps import AsyncSessionDep
from app.core.exceptions import AuthenticationError
from app.core.jwt import create_token_pair, verify_token
from app.models.auth import (
    AuthStatusResponse,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    TokenResponse,
    TokenValidationResponse,
    UserInfo,
    UserLogin,
    UserRegister,
)
from app.services.user import UserService, get_user_service

router = APIRouter()


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register New User",
    description="Create a new user account and return access tokens",
)
async def register(
    user_data: UserRegister,
    session: AsyncSessionDep,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    """Register a new user"""
    try:
        user = await user_service.create_user(
            session=session,
            email=user_data.email,
            password=user_data.password,
            full_name=user_data.full_name,
        )
        
        tokens = create_token_pair(user_id=user.id, email=user.email)
        return TokenResponse(**tokens)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticate user and return access tokens",
)
async def login(
    credentials: UserLogin,
    session: AsyncSessionDep,
    user_service: UserService = Depends(get_user_service),
) -> TokenResponse:
    """Login user and return tokens"""
    try:
        user = await user_service.authenticate_user(
            session=session,
            email=credentials.email,
            password=credentials.password,
        )
        
        tokens = create_token_pair(user_id=user.id, email=user.email)
        return TokenResponse(**tokens)
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh Access Token",
    description="Get a new access token using a refresh token",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
) -> TokenResponse:
    """Refresh access token"""
    try:
        payload = verify_token(refresh_data.refresh_token, token_type="refresh")
        user_id = UUID(payload.get("sub"))
        email = payload.get("email")
        
        tokens = create_token_pair(user_id=user_id, email=email)
        return TokenResponse(**tokens)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


@router.post(
    "/password-reset",
    status_code=status.HTTP_200_OK,
    summary="Request Password Reset",
    description="Request a password reset token (development: returns token directly)",
)
async def request_password_reset(
    reset_request: PasswordResetRequest,
    session: AsyncSessionDep,
    user_service: UserService = Depends(get_user_service),
) -> Dict[str, str]:
    """Request password reset"""
    user = await user_service.get_user_by_email(session, reset_request.email)
    if not user:
        # Don't reveal if user exists for security
        return {"message": "If the email exists, a reset token has been sent"}
    
    # In development, we'll generate a simple reset token
    # In production, this should send an email
    from app.core.jwt import create_password_reset_token
    
    reset_token = create_password_reset_token(
        {"sub": str(user.id), "email": user.email},
    )
    
    # In development, return token directly (not secure for production!)
    return {"message": "Password reset token generated", "token": reset_token}


@router.post(
    "/password-reset/confirm",
    status_code=status.HTTP_200_OK,
    summary="Confirm Password Reset",
    description="Reset password using reset token",
)
async def confirm_password_reset(
    reset_data: PasswordResetConfirm,
    session: AsyncSessionDep,
    user_service: UserService = Depends(get_user_service),
) -> Dict[str, str]:
    """Confirm password reset"""
    try:
        payload = verify_token(reset_data.token, token_type="password_reset")
        user_id = UUID(payload.get("sub"))
        
        await user_service.update_user_password(
            session=session,
            user_id=user_id,
            new_password=reset_data.new_password,
        )
        
        return {"message": "Password reset successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )


@router.get(
    "/me",
    response_model=UserInfo,
    summary="Get Current User",
    description="Returns information about the currently authenticated user",
)
async def get_current_user_info(
    current_user: CurrentUserDep,
    session: AsyncSessionDep,
    user_service: UserService = Depends(get_user_service),
) -> UserInfo:
    """Get current user information"""
    user_id = UUID(current_user["sub"])
    user = await user_service.get_user_by_id(session, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserInfo(
        sub=current_user["sub"],
        email=user.email,
        full_name=user.full_name,
    )


@router.get(
    "/status",
    response_model=AuthStatusResponse,
    summary="Authentication Status",
    description="Check if the current request is authenticated",
)
async def auth_status(
    current_user: OptionalUserDep,
) -> AuthStatusResponse:
    """Check authentication status"""
    if current_user:
        return AuthStatusResponse(
            authenticated=True,
            user=UserInfo(
                sub=current_user["sub"],
                email=current_user.get("email"),
            ),
        )
    return AuthStatusResponse(authenticated=False)


@router.post(
    "/validate",
    response_model=TokenValidationResponse,
    summary="Validate Token",
    description="Validate a JWT token and return user information",
)
async def validate_token(
    current_user: CurrentUserDep,
) -> TokenValidationResponse:
    """Validate token"""
    return TokenValidationResponse(
        valid=True,
        user=UserInfo(
            sub=current_user["sub"],
            email=current_user.get("email"),
        ),
    )


@router.get(
    "/protected",
    summary="Protected Route Test",
    description="Test endpoint to verify authentication is working",
)
async def protected_route(
    current_user: CurrentUserDep,
) -> Dict[str, Any]:
    """Test protected route"""
    return {
        "message": "You have accessed a protected route",
        "user_sub": current_user["sub"],
    }
