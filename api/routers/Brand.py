from typing import Optional, List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from uuid import UUID

from api.services import BrandService
from api.schemas import BrandCreate, BrandReturn, BrandUpdate, UserReturn
from api.dependencies import get_current_active_user
from core.db import SessionDep

brand_router = APIRouter(prefix="/brand", tags=["Brand"])


@brand_router.get("/", response_model=List[BrandReturn])
async def get_all_brands(session: SessionDep, user_id: UUID = None, current_user: BrandReturn = Depends(get_current_active_user)) -> List[BrandReturn]:
    if user_id:
        return await BrandService.get_all_brands_by_user(user_id, session)
    return await BrandService.get_all_brands(session)


@brand_router.get("/{brand_id}", response_model=BrandReturn)
async def get_brand_by_id(brand_id: UUID, session: SessionDep, current_user: BrandReturn = Depends(get_current_active_user)) -> BrandReturn:
    return await BrandService.get_brand_by_id(brand_id, session)


@brand_router.post("/", response_model=BrandReturn)
async def create_brand(brand: BrandCreate, session: SessionDep, current_user: UserReturn = Depends(get_current_active_user)) -> BrandReturn:
    return await BrandService.create_brand(brand, session, current_user)


@brand_router.put("/{brand_id}", response_model=BrandReturn)
async def update_brand(brand_id: UUID, brand: BrandUpdate, session: SessionDep, current_user: BrandReturn = Depends(get_current_active_user)) -> BrandReturn:
    return await BrandService.update_brand(brand_id, brand, session)


@brand_router.delete("/{brand_id}", response_model=BrandReturn)
async def delete_brand(brand_id: UUID, session: SessionDep, current_user: BrandReturn = Depends(get_current_active_user)) -> BrandReturn:
    return await BrandService.delete_brand(brand_id, session)
