from typing import Annotated, Any

from fastapi import Depends

from core.db import SessionDep
from core.exceptions import *
from core.security import oauth2_scheme, verify_token
from core.types import TokenType
from api.services import UserService
from api.schemas import UserReturn


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep
) -> dict[str, Any] | None:
    token_data = verify_token(token, TokenType.ACCESS)
    if token_data is None:
        raise UnauthorizedException("User not authenticated.")

    user_id = token_data.get("sub")
    if not user_id:
        raise UnauthorizedException("User not authenticated.")

    user = await UserService.get_user_by_id(user_id, session)

    if user:
        return UserReturn(**user.model_dump())

    raise UnauthorizedException("User not authenticated.")


async def get_current_active_user(
    current_user: Annotated[UserReturn, Depends(get_current_user)],
) -> UserReturn:
    if not current_user.is_active:
        raise ForbiddenException("Inactive user.")
    return current_user


async def get_current_active_verified_user(
    current_user: Annotated[UserReturn, Depends(get_current_active_user)],
) -> UserReturn:
    if not current_user.is_verified:
        raise ForbiddenException("Unverified user.")
    return current_user


async def get_current_active_verified_superuser_user(
    current_user: Annotated[UserReturn, Depends(get_current_active_verified_user)],
) -> UserReturn:
    if not current_user.is_superuser:
        raise ForbiddenException("User is not a superuser.")
    return current_user
