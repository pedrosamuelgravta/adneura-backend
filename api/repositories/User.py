from pydantic import EmailStr
from sqlmodel import select

from api.models import User
from core.security import get_password_hash
from api.schemas import UserCreate
from core.db import SessionDep


class UserRepository:
    @staticmethod
    async def get_all_users(session: SessionDep) -> list[User]:
        return session.exec(select(User)).all()

    @staticmethod
    async def get_user_by_id(user_id: str, session: SessionDep) -> User | None:
        return session.exec(select(User).where(User.id == user_id)).first()

    @staticmethod
    async def get_user_by_email(email: EmailStr, session: SessionDep) -> User | None:
        statement = select(User).where(User.email == email)
        user = session.exec(statement)
        return user.first()

    @staticmethod
    async def create_user(user: UserCreate, session: SessionDep) -> User | None:
        user = User(username=user.username,
                    email=user.email, hashed_password=get_password_hash(user.password))
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    async def update_user_name(user: User, name: str) -> User | None:
        user.name = name
        await user.save()
        return user

    @staticmethod
    async def update_user_password(user: User, plain_password: str) -> User | None:
        user.hashed_password = get_password_hash(plain_password)
        await user.save()
        return user

    @staticmethod
    async def activate_user(user: User) -> User | None:
        user.is_active = True
        await user.save()
        return user

    @staticmethod
    async def deactivate_user(user: User) -> User | None:
        user.is_active = False
        await user.save()
        return user

    @staticmethod
    async def superuser_user(user: User) -> User | None:
        user.is_superuser = True
        await user.save()
        return user

    @staticmethod
    async def unsuperuser_user(user: User) -> User | None:
        user.is_superuser = False
        await user.save()
        return user

    @staticmethod
    async def verify_user(user: User) -> User | None:
        user.is_verified = True
        await user.save()
        return user

    @staticmethod
    async def unverify_user(user: User) -> User | None:
        user.is_verified = False
        await user.save()
        return user
