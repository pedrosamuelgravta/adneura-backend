from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from core.db import SessionDep

from api.services import AuthService
from api.schemas import UserCreate, UserReturn
from core.exceptions import UnauthorizedException

from datetime import timedelta
from uuid import UUID
from api.dependencies import get_current_active_user

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login")
async def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep,
):
    print("entrou aqui")
    response_data = await AuthService.login(form_data, session)
    response.set_cookie(
        key="refresh_token",
        value=response_data["refresh_token"],
        httponly=True,
        secure=True,
        samesite="strict",
        path="/refresh",
        max_age=int(timedelta(days=10).total_seconds()),
    )

    return {
        "access_token": response_data["access_token"],
        "refresh_token": response_data["refresh_token"],
        "token_type": response_data["token_type"],
    }


@auth_router.post("/register", response_model=UserReturn)
async def register_user(user: UserCreate, session: SessionDep) -> UserReturn:
    return await AuthService.register_user(user, session)


@auth_router.post("/refresh")
async def refresh_access_token(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    print(refresh_token)
    if not refresh_token:
        raise UnauthorizedException("Refresh token not found")

    return await AuthService.refresh_access_token(refresh_token=refresh_token)


@auth_router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}


@auth_router.post("/add-seed/{user_id}")
async def add_seed_to_user(
    user_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> dict:
    return await AuthService.add_seed_to_user(user_id, session)
