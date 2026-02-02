from typing import Annotated

from fastapi import Depends

from app.core.dependencies import (
    AdminUserDep,
    ApiKeyDep,
    CurrentUserDep,
    OptionalUserDep,
    SettingsDep,
)
from app.services.auth import AuthService, get_auth_service

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

__all__ = [
    "AdminUserDep",
    "ApiKeyDep",
    "AuthServiceDep",
    "CurrentUserDep",
    "OptionalUserDep",
    "SettingsDep",
]
