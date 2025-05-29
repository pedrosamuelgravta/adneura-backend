from typing import List
from fastapi import APIRouter, Depends
from core.db import SessionDep
from api.schemas import (
    AudienceCreate,
    AudienceReturn,
    AudienceUpdate,
    UserReturn,
    AudienceAiGenerate,
    AudienceGenerateResponse,
)
from api.services import AudienceService
from api.dependencies import get_current_active_user
from uuid import UUID
import time

from fastapi.responses import JSONResponse

audience_router = APIRouter(prefix="/audience", tags=["Audience"])


@audience_router.get("/", response_model=List[AudienceReturn])
async def get_all_audiences_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[AudienceReturn]:
    return await AudienceService.get_all_audiences_by_brand_id(brand_id, session)


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
    print(audience)
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


@audience_router.post("/ai_generate", response_model=AudienceGenerateResponse)
async def generate_audiences_with_ai(
    request: AudienceAiGenerate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceGenerateResponse | None:
    return await AudienceService.generate_initial_audiences(request, session)


@audience_router.post("/analyze", response_model=AudienceReturn)
async def analyze_audience(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> AudienceReturn:
    print("analyzing audience", audience_id)
    print("Input time", time.time())
    return await AudienceService.analyze_audience(audience_id, session)


@audience_router.post("/generate_image")
async def generate_audience_image(
    brand_id: UUID,
    session: SessionDep,
    audience_id: UUID = None,
    current_user: UserReturn = Depends(get_current_active_user),
) -> JSONResponse:
    return await AudienceService.generate_audience_image(
        brand_id, session, audience_id
    )
