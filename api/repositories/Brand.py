from sqlmodel import select

from api.models import Brand
from api.schemas import BrandUpdate
from core.db import SessionDep
from core.exceptions import NotFoundException, InternalServerError, ConflictException
from uuid import UUID


class BrandRepository:
    @staticmethod
    async def get_all_brands(session: SessionDep) -> list[Brand]:
        return session.exec(select(Brand)).all()

    @staticmethod
    async def get_brand_by_id(brand_id: str, session: SessionDep) -> Brand | None:
        return session.exec(select(Brand).where(Brand.id == brand_id)).first()

    @staticmethod
    async def get_all_brands_by_user(user_id: str, session: SessionDep) -> list[Brand]:
        statement = select(Brand).where(Brand.user_id == user_id)
        brand = session.exec(statement)
        return brand.all()

    @staticmethod
    async def get_brand_by_name(name: str, session: SessionDep, user_id: str) -> Brand | None:
        return session.exec(select(Brand).where(Brand.name == name, Brand.user_id == user_id)).first()

    @staticmethod
    async def create_brand(brand: dict, session: SessionDep) -> Brand | None:
        brand = Brand(**brand)
        session.add(brand)
        session.commit()
        session.refresh(brand)
        return brand

    @staticmethod
    async def update_brand(brand_id: UUID, brand: BrandUpdate, session: SessionDep) -> Brand | None:
        existing_brand = session.get(Brand, brand_id)
        existing_brand.sqlmodel_update(brand)
        session.add(existing_brand)
        session.commit()
        session.refresh(existing_brand)
        return existing_brand
