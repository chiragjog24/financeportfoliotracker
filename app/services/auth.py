from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from app.core.config import get_settings
from app.core.exceptions import AuthenticationError, InternalServerError
from app.core.logging import get_logger
from app.core.security import verify_cognito_token, extract_user_info

settings = get_settings()
logger = get_logger("services.auth")


class AuthService:
    def __init__(self):
        self._cognito_client = None

    @property
    def cognito_client(self):
        if self._cognito_client is None:
            self._cognito_client = boto3.client(
                "cognito-idp",
                region_name=settings.aws_region,
            )
        return self._cognito_client

    async def validate_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = await verify_cognito_token(token)
            return extract_user_info(payload)
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error("token_validation_failed", error=str(e))
            raise AuthenticationError("Token validation failed")

    async def get_user_by_sub(self, sub: str) -> Optional[Dict[str, Any]]:
        if not settings.cognito_user_pool_id:
            raise InternalServerError("Cognito is not configured")

        try:
            response = self.cognito_client.list_users(
                UserPoolId=settings.cognito_user_pool_id,
                Filter=f'sub = "{sub}"',
                Limit=1,
            )

            users = response.get("Users", [])
            if not users:
                return None

            user = users[0]
            attributes = {
                attr["Name"]: attr["Value"]
                for attr in user.get("Attributes", [])
            }

            return {
                "sub": attributes.get("sub"),
                "email": attributes.get("email"),
                "username": user.get("Username"),
                "status": user.get("UserStatus"),
                "enabled": user.get("Enabled"),
            }
        except ClientError as e:
            logger.error("cognito_user_lookup_failed", error=str(e))
            raise InternalServerError("Failed to look up user")

    async def is_user_in_group(self, username: str, group_name: str) -> bool:
        if not settings.cognito_user_pool_id:
            raise InternalServerError("Cognito is not configured")

        try:
            response = self.cognito_client.admin_list_groups_for_user(
                UserPoolId=settings.cognito_user_pool_id,
                Username=username,
            )

            groups = [g["GroupName"] for g in response.get("Groups", [])]
            return group_name in groups
        except ClientError as e:
            logger.error("cognito_group_check_failed", error=str(e))
            raise InternalServerError("Failed to check user groups")


def get_auth_service() -> AuthService:
    return AuthService()
