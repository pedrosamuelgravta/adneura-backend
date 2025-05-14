from pydantic import EmailStr
from email_validator import validate_email
from uuid import UUID

from api.repositories.User import UserRepository
from api.models import User
from core.exceptions import *
from core.db import SessionDep


class UserService:
    @staticmethod
    async def get_all_users(session: SessionDep) -> list[User]:
        return await UserRepository.get_all_users(session)

    @staticmethod
    async def get_user_by_id(user_id: UUID, session: SessionDep) -> User:
        user = await UserRepository.get_user_by_id(user_id, session)
        if not user:
            raise NotFoundException(f"User with id {user_id} not found")
        return user
