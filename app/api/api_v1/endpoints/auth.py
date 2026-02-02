from typing import Any, Dict

from fastapi import APIRouter

from app.api.deps import AuthServiceDep, CurrentUserDep, OptionalUserDep
from app.models.auth import AuthStatusResponse, TokenValidationResponse, UserInfo

router = APIRouter()


@router.get(
    "/me",
    response_model=UserInfo,
    summary="Get Current User",
    description="Returns information about the currently authenticated user",
)
async def get_current_user_info(
    current_user: CurrentUserDep,
) -> UserInfo:
    return UserInfo(
        sub=current_user["sub"],
        email=current_user.get("email"),
        username=current_user.get("username"),
        groups=current_user.get("groups", []),
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
    if current_user:
        return AuthStatusResponse(
            authenticated=True,
            user=UserInfo(
                sub=current_user["sub"],
                email=current_user.get("email"),
                username=current_user.get("username"),
                groups=current_user.get("groups", []),
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
    auth_service: AuthServiceDep,
    current_user: CurrentUserDep,
) -> TokenValidationResponse:
    return TokenValidationResponse(
        valid=True,
        user=UserInfo(
            sub=current_user["sub"],
            email=current_user.get("email"),
            username=current_user.get("username"),
            groups=current_user.get("groups", []),
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
    return {
        "message": "You have accessed a protected route",
        "user_sub": current_user["sub"],
    }
