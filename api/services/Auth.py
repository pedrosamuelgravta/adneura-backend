from fastapi.security import OAuth2PasswordRequestForm
from api.repositories.User import UserRepository
from api.schemas import UserCreate, UserReturn
from core.exceptions import *
from core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token,
)
from core.db import SessionDep
from core.types import TokenType
from datetime import timedelta

from core.config import get_settings

settings = get_settings()


class AuthService:
    @staticmethod
    async def login(form_data: OAuth2PasswordRequestForm, session: SessionDep) -> dict:
        user = await UserRepository.get_user_by_email(form_data.username, session)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise UnauthorizedException("Invalid credentials")

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE)
        access_token = create_access_token(
            data={"sub": str(user.id), "is_superuser": user.is_superuser},
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(
            data={"sub": str(user.id), "is_superuser": user.is_superuser}
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    @staticmethod
    async def register_user(user: UserCreate, session: SessionDep) -> UserReturn:
        existing_user = await UserRepository.get_user_by_email(user.email, session)
        if existing_user:
            raise ConflictException("User already exists")
        user = await UserRepository.create_user(user, session)

        return user

    @staticmethod
    async def refresh_access_token(refresh_token: str):
        token_data = verify_token(
            token=refresh_token, token_type=TokenType.REFRESH)
        if not token_data:
            raise UnauthorizedException("Invalid refresh token")

        access_token_expires = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTE)
        access_token = create_access_token(
            data={"sub": token_data.get("sub")}, expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }
