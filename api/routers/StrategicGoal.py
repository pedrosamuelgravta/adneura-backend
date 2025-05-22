from fastapi import APIRouter, Depends
from core.db import SessionDep
from api.schemas import (
    StrategicGoalCreate,
    StrategicGoalReturn,
    StrategicGoalUpdate,
    StrategicGoalArchive,
    UserReturn,
)
from api.services import StrategicGoalService
from api.dependencies import get_current_active_user
from uuid import UUID
from typing import List

strategic_goal_router = APIRouter(prefix="/strategic_goal", tags=["StrategicGoal"])


@strategic_goal_router.get("/", response_model=List[StrategicGoalReturn])
async def get_all_strategic_goals(
    session: SessionDep,
    user_id: UUID = None,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[StrategicGoalReturn]:
    if user_id:
        return await StrategicGoalService.get_all_strategic_goals_by_user(
            user_id, session
        )
    return await StrategicGoalService.get_all_strategic_goals(session)


@strategic_goal_router.get("/{strategic_goal_id}", response_model=StrategicGoalReturn)
async def get_strategic_goal_by_id(
    strategic_goal_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> StrategicGoalReturn:
    return await StrategicGoalService.get_strategic_goal_by_id(
        strategic_goal_id, session
    )


@strategic_goal_router.get("/brand", response_model=List[StrategicGoalReturn])
async def get_strategic_goals_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[StrategicGoalReturn]:
    return await StrategicGoalService.get_strategic_goals_by_brand_id(brand_id, session)


@strategic_goal_router.post("/", response_model=StrategicGoalReturn)
async def create_strategic_goal(
    strategic_goal: StrategicGoalCreate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> StrategicGoalReturn:
    return await StrategicGoalService.create_strategic_goal(strategic_goal, session)


@strategic_goal_router.put("/{strategic_goal_id}", response_model=StrategicGoalReturn)
async def update_strategic_goal(
    strategic_goal_id: UUID,
    strategic_goal: StrategicGoalUpdate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> StrategicGoalReturn:
    return await StrategicGoalService.update_strategic_goal(
        strategic_goal_id, strategic_goal, session
    )


@strategic_goal_router.patch("/", response_model=StrategicGoalReturn)
async def archive_strategic_goal(
    strategic_goal: StrategicGoalArchive,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> StrategicGoalReturn:
    return await StrategicGoalService.archive_strategic_goal(strategic_goal, session)


@strategic_goal_router.delete(
    "/{strategic_goal_id}", response_model=StrategicGoalReturn
)
async def delete_strategic_goal(
    strategic_goal_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> StrategicGoalReturn:
    return await StrategicGoalService.delete_strategic_goal(strategic_goal_id, session)


@strategic_goal_router.delete(
    "/delete_all/{brand_id}", response_model=List[StrategicGoalReturn]
)
async def delete_all_strategic_goals_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[StrategicGoalReturn]:
    return await StrategicGoalService.delete_all_strategic_goals_by_brand_id(
        brand_id, session
    )
