from sqlmodel import select
from uuid import UUID

from api.models import Audience
from api.schemas import AudienceCreate, AudienceReturn, AudienceUpdate
from core.db import SessionDep


class AudienceRepository:
    @staticmethod
    async def get_all_audiences_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> list[Audience]:
        statement = select(Audience).where(Audience.brand_id == brand_id)
        audiences = session.exec(statement)
        return audiences.all()

    @staticmethod
    async def get_audience_by_id(
        audience_id: UUID, session: SessionDep
    ) -> Audience | None:
        return session.exec(select(Audience).where(Audience.id == audience_id)).first()

    @staticmethod
    async def get_audience_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> Audience | None:
        return session.exec(
            select(Audience).where(Audience.brand_id == brand_id)
        ).first()

    @staticmethod
    async def create_audience(
        audience_data: dict, session: SessionDep
    ) -> Audience | None:
        audience = Audience(**audience_data)
        session.add(audience)
        session.commit()
        session.refresh(audience)
        return audience

    @staticmethod
    async def update_audience(
        audience_id: UUID, audience: dict, session: SessionDep
    ) -> Audience | None:
        existing_audience = session.get(Audience, audience_id)
        existing_audience.sqlmodel_update(audience)
        session.add(existing_audience)
        session.commit()
        session.refresh(existing_audience)
        return existing_audience

    @staticmethod
    async def delete_audience(
        audience_id: UUID, session: SessionDep
    ) -> Audience | None:
        audience = session.get(Audience, audience_id)
        if audience:
            session.delete(audience)
            session.commit()
            return audience
        return None
