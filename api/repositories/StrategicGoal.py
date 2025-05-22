from typing import List
from sqlmodel import select
from api.models import StrategicGoal
from api.schemas import StrategicGoalUpdate, StrategicGoalCreate, StrategicGoalArchive
from core.db import SessionDep
from uuid import UUID


class StrategicGoalRepository:
    @staticmethod
    async def get_all_strategic_goals(session: SessionDep) -> List[StrategicGoal]:
        return session.exec(select(StrategicGoal)).all()

    @staticmethod
    async def get_strategic_goal_by_id(
        strategic_goal_id: UUID, session: SessionDep
    ) -> StrategicGoal | None:
        return session.exec(
            select(StrategicGoal).where(StrategicGoal.id == strategic_goal_id)
        ).first()

    @staticmethod
    async def get_strategic_goals_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[StrategicGoal]:
        return session.exec(
            select(StrategicGoal).where(StrategicGoal.brand_id == brand_id)
        ).all()

    @staticmethod
    async def get_strategic_goals_by_user(
        user_id: UUID, session: SessionDep
    ) -> List[StrategicGoal]:
        return session.exec(
            select(StrategicGoal).where(StrategicGoal.user_id == user_id)
        ).all()

    @staticmethod
    async def create_strategic_goal(
        strategic_goal: StrategicGoalCreate, session: SessionDep
    ) -> StrategicGoal:
        strategic_goal = StrategicGoal.model_validate(strategic_goal)
        session.add(strategic_goal)
        session.commit()
        session.refresh(strategic_goal)
        return strategic_goal

    @staticmethod
    async def update_strategic_goal(
        strategic_goal_id: UUID,
        strategic_goal: StrategicGoalUpdate,
        session: SessionDep,
    ) -> StrategicGoal | None:
        existing_strategic_goal = session.get(StrategicGoal, strategic_goal_id)
        existing_strategic_goal.sqlmodel_update(strategic_goal)
        session.add(existing_strategic_goal)
        session.commit()
        session.refresh(existing_strategic_goal)
        return existing_strategic_goal

    @staticmethod
    async def archive_strategic_goal(
        strategic_goal: StrategicGoalArchive, session: SessionDep
    ) -> StrategicGoal | None:
        existing_strategic_goal = session.get(StrategicGoal, strategic_goal.id)
        existing_strategic_goal.sqlmodel_update(strategic_goal)
        session.add(existing_strategic_goal)
        session.commit()
        session.refresh(existing_strategic_goal)
        return existing_strategic_goal

    @staticmethod
    async def delete_strategic_goal(
        strategic_goal_id: UUID, session: SessionDep
    ) -> StrategicGoal | None:
        strategic_goal = session.get(StrategicGoal, strategic_goal_id)
        if strategic_goal:
            session.delete(strategic_goal)
            session.commit()
            return strategic_goal
        return None

    @staticmethod
    async def delete_all_strategic_goals_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[StrategicGoal]:
        strategic_goals = session.exec(
            select(StrategicGoal).where(StrategicGoal.brand_id == brand_id)
        ).all()
        for strategic_goal in strategic_goals:
            session.delete(strategic_goal)
        session.commit()
        return strategic_goals
