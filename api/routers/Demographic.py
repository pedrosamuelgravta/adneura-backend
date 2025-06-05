from fastapi import APIRouter, Depends
from uuid import UUID

from core.db import SessionDep

from api.schemas import DemographicCreate, DemographicUpdate, DemographicReturn, UserReturn
from api.services import DemographicService
from api.dependencies import get_current_active_user

demographic_router = APIRouter(
    prefix="/demographic", tags=["Demographic"]
)


@demographic_router.get("/", response_model=DemographicReturn)
async def get_demographic_by_audience(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> DemographicReturn:
    return await DemographicService.get_demographic_by_audience(audience_id, session)


@demographic_router.get("/{demographic_id}", response_model=DemographicReturn)
async def get_demographic_by_id(
    demographic_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> DemographicReturn:
    return await DemographicService.get_demographic_by_id(demographic_id, session)


@demographic_router.post("/", response_model=DemographicReturn)
async def create_demographic(
    demographic: DemographicCreate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> DemographicReturn:
    return await DemographicService.create_demographic(demographic, session)


@demographic_router.patch("/{demographic_id}", response_model=DemographicReturn)
async def update_demographic(
    demographic_id: UUID,
    demographic: DemographicUpdate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> DemographicReturn:
    return await DemographicService.update_demographic(demographic_id, demographic, session)


@demographic_router.delete("/{demographic_id}", response_model=DemographicReturn)
async def delete_demographic(
    demographic_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> DemographicReturn:
    return await DemographicService.delete_demographic(demographic_id, session)
