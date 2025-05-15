from sqlmodel import select
from api.models import Demographic
from api.schemas import DemographicCreate, DemographicUpdate
from core.db import SessionDep
from uuid import UUID


class DemographicRepository:
    @staticmethod
    async def get_demographic_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> Demographic | None:
        return session.exec(
            select(Demographic).where(Demographic.audience_id == audience_id)
        ).first()

    @staticmethod
    async def get_demographic_by_id(
        demographic_id: UUID, session: SessionDep
    ) -> Demographic | None:
        return session.exec(
            select(Demographic).where(Demographic.id == demographic_id)
        ).first()

    @staticmethod
    async def create_demographic(
        demographic: DemographicCreate, session: SessionDep
    ) -> Demographic:
        demographic = Demographic.model_validate(demographic)
        session.add(demographic)
        session.commit()
        session.refresh(demographic)
        return demographic

    @staticmethod
    async def update_demographic(
        demographic_id: UUID, demographic: DemographicUpdate, session: SessionDep
    ) -> Demographic | None:
        existing_demographic = session.get(Demographic, demographic_id)
        existing_demographic.sqlmodel_update(demographic)
        session.add(existing_demographic)
        session.commit()
        session.refresh(existing_demographic)
        return existing_demographic

    @staticmethod
    async def delete_demographic(
        demographic_id: UUID, session: SessionDep
    ) -> Demographic | None:
        existing_demographic = session.get(Demographic, demographic_id)
        session.delete(existing_demographic)
        session.commit()
        return existing_demographic
