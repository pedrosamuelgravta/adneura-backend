from typing import Optional
from pydantic import BaseModel
from uuid import UUID
from .StrategicGoal import StrategicGoalReturn
from datetime import datetime


class CampaignReturn(BaseModel):
    id: UUID
    campaign: str
    is_active: bool
    is_completed: bool
    strategic_goals: Optional[list[StrategicGoalReturn]] = None
    created_at: Optional[datetime] = None


class CampaignCreate(BaseModel):
    campaign: str
    is_active: bool = True
    is_completed: bool = False
    brand_id: UUID


class CampaignUpdate(BaseModel):
    campaign: Optional[str] = None
    is_active: Optional[bool] = None
    is_completed: Optional[bool] = None


class CampaignDelete(BaseModel):
    id: UUID
    is_active: bool = False
