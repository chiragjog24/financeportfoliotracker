from typing import Annotated, Any, Dict, Optional

from fastapi import Depends, Header

from app.core.config import Settings, get_settings
from app.core.exceptions import AuthenticationError, ForbiddenError
from app.core.security import (
    extract_user_info,
    validate_api_key,
    verify_cognito_token,
)


async def get_token_from_header(
    authorization: Annotated[Optional[str], Header()] = None,
) -> str:
    if not authorization:
        raise AuthenticationError("Authorization header missing")

    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise AuthenticationError("Invalid authorization header format")

    return parts[1]


async def get_current_user(
    token: Annotated[str, Depends(get_token_from_header)],
) -> Dict[str, Any]:
    token_payload = await verify_cognito_token(token)
    return extract_user_info(token_payload)


async def get_current_user_optional(
    authorization: Annotated[Optional[str], Header()] = None,
) -> Optional[Dict[str, Any]]:
    if not authorization:
        return None

    try:
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None
        token = parts[1]
        token_payload = await verify_cognito_token(token)
        return extract_user_info(token_payload)
    except Exception:
        return None


async def verify_api_key(
    settings: Annotated[Settings, Depends(get_settings)],
    x_api_key: Annotated[Optional[str], Header()] = None,
) -> str:
    if not x_api_key:
        raise AuthenticationError("API key missing")

    if not validate_api_key(x_api_key):
        raise AuthenticationError("Invalid API key")

    return x_api_key


async def require_admin(
    current_user: Annotated[Dict[str, Any], Depends(get_current_user)],
) -> Dict[str, Any]:
    groups = current_user.get("groups", [])
    if "admin" not in groups:
        raise ForbiddenError("Admin access required")
    return current_user


SettingsDep = Annotated[Settings, Depends(get_settings)]
CurrentUserDep = Annotated[Dict[str, Any], Depends(get_current_user)]
OptionalUserDep = Annotated[Optional[Dict[str, Any]], Depends(get_current_user_optional)]
AdminUserDep = Annotated[Dict[str, Any], Depends(require_admin)]
ApiKeyDep = Annotated[str, Depends(verify_api_key)]
