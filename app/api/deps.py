from typing import Annotated

from fastapi import Depends

from app.core.dependencies import (
    AdminUserDep,
    ApiKeyDep,
    CurrentUserDep,
    OptionalUserDep,
    SettingsDep,
)
from app.services.user import UserService, get_user_service

UserServiceDep = Annotated[UserService, Depends(get_user_service)]

__all__ = [
    "AdminUserDep",
    "ApiKeyDep",
    "UserServiceDep",
    "CurrentUserDep",
    "OptionalUserDep",
    "SettingsDep",
]
