from typing import Dict

from app.core.jwt import verify_token


async def verify_jwt_token(token: str) -> Dict[str, str]:
    """Verify a JWT access token and return user info"""
    payload = verify_token(token, token_type="access")
    return {
        "sub": payload.get("sub"),
        "email": payload.get("email"),
    }


def extract_user_info(token_payload: Dict[str, str]) -> Dict[str, str]:
    """Extract user info from token payload"""
    return {
        "sub": token_payload.get("sub"),
        "email": token_payload.get("email"),
    }


def validate_api_key(api_key: str) -> bool:
    if not settings.api_keys:
        return False
    return api_key in settings.api_keys
