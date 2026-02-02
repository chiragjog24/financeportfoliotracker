from typing import Any, Dict, Optional

import httpx
from jose import JWTError, jwt
from jose.exceptions import ExpiredSignatureError

from app.core.config import get_settings
from app.core.exceptions import (
    AuthenticationError,
    TokenExpiredError,
    TokenValidationError,
)

settings = get_settings()

_jwks_cache: Optional[Dict[str, Any]] = None


async def get_jwks() -> Dict[str, Any]:
    global _jwks_cache
    if _jwks_cache is None:
        async with httpx.AsyncClient() as client:
            response = await client.get(settings.cognito_jwks_url)
            response.raise_for_status()
            _jwks_cache = response.json()
    return _jwks_cache


def get_public_key(token: str, jwks: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    try:
        unverified_header = jwt.get_unverified_header(token)
    except JWTError:
        return None

    kid = unverified_header.get("kid")
    if not kid:
        return None

    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


async def verify_cognito_token(token: str) -> Dict[str, Any]:
    if not settings.cognito_user_pool_id or not settings.cognito_app_client_id:
        raise AuthenticationError("Cognito is not configured")

    jwks = await get_jwks()
    public_key = get_public_key(token, jwks)

    if not public_key:
        raise TokenValidationError("Unable to find appropriate key")

    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=settings.cognito_app_client_id,
            issuer=settings.cognito_issuer,
        )
    except ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError as e:
        raise TokenValidationError(f"Token validation failed: {str(e)}")

    return payload


def extract_user_info(token_payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sub": token_payload.get("sub"),
        "email": token_payload.get("email"),
        "username": token_payload.get("cognito:username"),
        "groups": token_payload.get("cognito:groups", []),
    }


def validate_api_key(api_key: str) -> bool:
    if not settings.api_keys:
        return False
    return api_key in settings.api_keys
