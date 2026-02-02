from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthenticationError, NotFoundError
from app.core.password import hash_password, verify_password
from app.models.user import User


class UserService:
    """Service for user management and authentication"""
    
    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """Get user by email"""
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def create_user(
        self,
        session: AsyncSession,
        email: str,
        password: str,
        full_name: Optional[str] = None,
    ) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = await self.get_user_by_email(session, email)
        if existing_user:
            raise AuthenticationError("User with this email already exists")
        
        # Create new user
        hashed_password = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_verified=False,  # In development, skip email verification
        )
        
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
    
    async def authenticate_user(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> User:
        """Authenticate a user with email and password"""
        user = await self.get_user_by_email(session, email)
        if not user:
            raise AuthenticationError("Invalid email or password")
        
        if not user.is_active:
            raise AuthenticationError("User account is inactive")
        
        if not verify_password(password, user.hashed_password):
            raise AuthenticationError("Invalid email or password")
        
        return user
    
    async def update_user_password(
        self,
        session: AsyncSession,
        user_id: UUID,
        new_password: str,
    ) -> User:
        """Update user password"""
        user = await self.get_user_by_id(session, user_id)
        if not user:
            raise NotFoundError("User not found")
        
        user.hashed_password = hash_password(new_password)
        await session.commit()
        await session.refresh(user)
        return user


def get_user_service() -> UserService:
    return UserService()
