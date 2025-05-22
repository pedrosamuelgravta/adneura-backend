from typing import List
from uuid import UUID

from core.db import SessionDep
from api.repositories import StrategicGoalRepository
from api.schemas import (
    StrategicGoalUpdate,
    StrategicGoalCreate,
    StrategicGoalArchive,
    StrategicGoalReturn,
)
from core.exceptions import *


class StrategicGoalService:
    @staticmethod
    async def get_all_strategic_goals(session: SessionDep) -> List[StrategicGoalReturn]:
        return await StrategicGoalRepository.get_all_strategic_goals(session)

    @staticmethod
    async def get_all_strategic_goals_by_user(
        user_id: UUID, session: SessionDep
    ) -> List[StrategicGoalReturn]:
        return await StrategicGoalRepository.get_strategic_goals_by_user(
            user_id, session
        )

    @staticmethod
    async def get_strategic_goal_by_id(
        strategic_goal_id: UUID, session: SessionDep
    ) -> StrategicGoalReturn:
        strategic_goal = await StrategicGoalRepository.get_strategic_goal_by_id(
            strategic_goal_id, session
        )
        if not strategic_goal:
            raise NotFoundException(
                f"Strategic goal with id {strategic_goal_id} not found"
            )
        return strategic_goal

    @staticmethod
    async def get_strategic_goals_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[StrategicGoalReturn]:
        return await StrategicGoalRepository.get_strategic_goals_by_brand_id(
            brand_id, session
        )

    @staticmethod
    async def create_strategic_goal(
        strategic_goal: StrategicGoalCreate, session: SessionDep
    ) -> StrategicGoalReturn:
        return await StrategicGoalRepository.create_strategic_goal(
            strategic_goal, session
        )

    @staticmethod
    async def update_strategic_goal(
        strategic_goal_id: UUID,
        strategic_goal: StrategicGoalUpdate,
        session: SessionDep,
    ) -> StrategicGoalReturn:
        return await StrategicGoalRepository.update_strategic_goal(
            strategic_goal_id, strategic_goal, session
        )

    @staticmethod
    async def archive_strategic_goal(
        strategic_goal: StrategicGoalArchive,
        session: SessionDep,
    ) -> StrategicGoalReturn:
        print("archive_strategic_goal", strategic_goal)
        return await StrategicGoalRepository.archive_strategic_goal(
            strategic_goal, session
        )

    @staticmethod
    async def delete_strategic_goal(
        strategic_goal_id: UUID, session: SessionDep
    ) -> StrategicGoalReturn:
        return await StrategicGoalRepository.delete_strategic_goal(
            strategic_goal_id, session
        )

    @staticmethod
    async def delete_all_strategic_goals_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[StrategicGoalReturn]:
        return await StrategicGoalRepository.delete_all_strategic_goals_by_brand_id(
            brand_id, session
        )
