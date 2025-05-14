from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from api.services import UserService
from api.schemas import UserCreate, UserReturn
from api.dependencies import get_current_active_user, get_current_user
from core.db import SessionDep

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.get("/", response_model=List[UserReturn])
async def get_all_users(session: SessionDep, current_user: UserReturn = Depends(get_current_active_user)) -> UserReturn:
    return await UserService.get_all_users(session)


@user_router.get("/{user_id}", response_model=UserReturn)
async def get_user_by_id(user_id: UUID, session: SessionDep, current_user: UserReturn = Depends(get_current_active_user)) -> UserReturn:
    return await UserService.get_user_by_id(user_id, session)
