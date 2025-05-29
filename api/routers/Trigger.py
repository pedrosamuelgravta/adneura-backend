from typing import List
from fastapi import APIRouter, Depends
from core.db import SessionDep

from api.services import TriggerService
from api.dependencies import get_current_active_user
from uuid import UUID

from api.schemas import (
    TriggerCreate,
    TriggerCreateWithGoal,
    TriggerReturn,
    TriggerUpdate,
    UserReturn,
)

trigger_router = APIRouter(
    prefix="/trigger", tags=["Trigger"]
)


@trigger_router.get("/", response_model=List[TriggerReturn])
async def get_all_triggers(
    session: SessionDep,
    audience_id: UUID = None,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[TriggerReturn]:
    if audience_id:
        return await TriggerService.get_all_triggers_by_audience(audience_id, session)
    return await TriggerService.get_all_triggers(session)


@trigger_router.get("/{trigger_id}", response_model=TriggerReturn)
async def get_trigger_by_id(
    trigger_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.get_trigger_by_id(trigger_id, session)


@trigger_router.get("/{brand_id}", response_model=List[TriggerReturn])
async def get_triggers_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[TriggerReturn]:
    return await TriggerService.get_triggers_by_brand_id(brand_id, session)


@trigger_router.post("/", response_model=TriggerReturn)
async def create_trigger(
    trigger: TriggerCreate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.create_trigger(trigger, session)


@trigger_router.put("/{trigger_id}", response_model=TriggerReturn)
async def update_trigger(
    trigger_id: UUID,
    trigger: TriggerUpdate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.update_trigger(trigger_id, trigger, session)


@trigger_router.delete("/{trigger_id}", response_model=TriggerReturn)
async def delete_trigger(
    trigger_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.delete_trigger(trigger_id, session)


@trigger_router.delete("/delete_all/{audience_id}", response_model=List[TriggerReturn])
async def delete_all_triggers_by_audience(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[TriggerReturn]:
    return await TriggerService.delete_all_triggers_by_audience(audience_id, session)


@trigger_router.post("/ai_generate", response_model=TriggerReturn)
async def generate_triggers_with_ai(
    audience_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.generate_initial_triggers(audience_id, session)


@trigger_router.post("/ai_generate_with_goal", response_model=TriggerReturn)
async def generate_triggers_with_goal(
    body: TriggerCreateWithGoal,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> TriggerReturn:
    return await TriggerService.generate_triggers_with_goal(body, session)
