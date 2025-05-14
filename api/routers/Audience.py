from typing import List
from fastapi import APIRouter, Depends
from core.db import SessionDep
from api.schemas import AudienceCreate, AudienceReturn, AudienceUpdate, UserReturn
from api.services import AudienceService
from api.dependencies import get_current_active_user
from uuid import UUID

audience_router = APIRouter(prefix="/audience", tags=["Audience"])


@audience_router.get("/", response_model=List[AudienceReturn])
async def get_all_audiences(
    session: SessionDep,
    user_id: UUID = None,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[AudienceReturn]:
    if user_id:
        return await AudienceService.get_all_audiences_by_user(user_id, session)
    return await AudienceService.get_all_audiences(session)


@audience_router.get("/{audience_id}", response_model=AudienceReturn)
async def get_audience_by_id(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    return await AudienceService.get_audience_by_id(audience_id, session)


@audience_router.post("/", response_model=AudienceReturn)
async def create_audience(
    audience: AudienceCreate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    return await AudienceService.create_audience(audience, session, current_user)


@audience_router.put("/{audience_id}", response_model=AudienceReturn)
async def update_audience(
    audience_id: UUID,
    audience: AudienceUpdate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    return await AudienceService.update_audience(audience_id, audience, session)


@audience_router.delete("/{audience_id}", response_model=AudienceReturn)
async def delete_audience(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    return await AudienceService.delete_audience(audience_id, session)


@audience_router.post("/ai_generate", response_model=List[AudienceReturn])
async def generate_audiences_with_ai(
    session: SessionDep,
    audiences_number: int = 9,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[AudienceReturn]:
    return await AudienceService.generate_initial_audiences(audiences_number, session, current_user)


@audience_router.post("/analyze", response_model=AudienceReturn)
async def analyze_audience(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    return await AudienceService.analyze_audience(audience_id, session, current_user)
