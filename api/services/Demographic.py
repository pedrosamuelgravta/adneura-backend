from api.schemas import DemographicCreate, DemographicReturn, DemographicUpdate
from api.repositories import DemographicRepository
from core.db import SessionDep
from core.exceptions import *
from uuid import UUID


class DemographicService:
    @staticmethod
    async def get_demographic_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> DemographicReturn:
        demographic = await DemographicRepository.get_demographic_by_audience(
            audience_id, session
        )
        if not demographic:
            raise NotFoundException(
                f"Demographic with audience id {audience_id} not found"
            )
        return demographic

    @staticmethod
    async def get_demographic_by_id(
        demographic_id: UUID, session: SessionDep
    ) -> DemographicReturn:
        demographic = await DemographicRepository.get_demographic_by_id(
            demographic_id, session
        )
        if not demographic:
            raise NotFoundException(
                f"Demographic with id {demographic_id} not found"
            )
        return demographic

    @staticmethod
    async def create_demographic(
        demographic: DemographicCreate, session: SessionDep
    ) -> DemographicReturn:
        demographic = await DemographicRepository.create_demographic(
            demographic, session
        )
        if not demographic:
            raise NotFoundException(
                f"Demographic with id {demographic.id} not found"
            )
        return demographic

    @staticmethod
    async def update_demographic(
        demographic_id: UUID, demographic: DemographicUpdate, session: SessionDep
    ) -> DemographicReturn:
        print(f"Updating demographic with id: {demographic_id}")
        print(f"Demographic data: {demographic}")
        demographic = await DemographicRepository.update_demographic(
            demographic_id, demographic, session
        )
        if not demographic:
            raise NotFoundException(
                f"Demographic with id {demographic_id} not found"
            )
        return demographic

    @staticmethod
    async def delete_demographic(
        demographic_id: UUID, session: SessionDep
    ) -> DemographicReturn:
        demographic = await DemographicRepository.delete_demographic(
            demographic_id, session
        )
        if not demographic:
            raise NotFoundException(
                f"Demographic with id {demographic_id} not found"
            )
        return demographic
