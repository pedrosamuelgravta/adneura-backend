from uuid import UUID

from api.repositories import AudienceRepository
from api.models import Audience, User
from api.schemas import AudienceCreate, AudienceReturn, AudienceUpdate
from core.exceptions import *
from core.db import SessionDep


class AudienceService:
    @staticmethod
    async def get_all_audiences(session: SessionDep) -> list[AudienceReturn]:
        return await AudienceRepository.get_all_audiences(session)

    @staticmethod
    async def get_all_audiences_by_user(user_id: UUID, session: SessionDep) -> list[AudienceReturn]:
        return await AudienceRepository.get_all_audiences_by_user(user_id, session)

    @staticmethod
    async def get_audience_by_id(audience_id: UUID, session: SessionDep) -> AudienceReturn:
        audience = await AudienceRepository.get_audience_by_id(audience_id, session)
        if not audience:
            raise NotFoundException("Audience not found")
        return audience

    @staticmethod
    async def create_audience(audience: AudienceCreate, session: SessionDep, current_user: User) -> AudienceReturn:
        ...

    @staticmethod
    async def generate_initial_audiences(
        audience_number: int,
        session: SessionDep,
        current_user: User,
    ) -> list[AudienceReturn]:
        ...

    @staticmethod
    async def analyze_audience(
        audience_id: UUID,
        session: SessionDep,
        current_user: User,
    ) -> AudienceReturn:
        ...
