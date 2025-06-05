from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class StrategicGoalReturn(BaseModel):
    id: UUID
    strategic_goal: str
    strategic_goal_color: Optional[str] = None
    campaign_id: UUID
    is_active: bool = True


class StrategicGoalCreate(BaseModel):
    strategic_goal: str
    campaign_id: UUID
    strategic_goal_color: Optional[str] = None
    is_active: bool = True


class StrategicGoalUpdate(BaseModel):
    strategic_goal: Optional[str] = None
    strategic_goal_color: Optional[str] = None
    is_active: Optional[bool] = True


class StrategicGoalDelete(BaseModel):
    id: UUID


class StrategicGoalArchive(BaseModel):
    id: UUID
    is_active: bool = False
