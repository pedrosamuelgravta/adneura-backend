from typing import Optional

from pydantic import BaseModel
from uuid import UUID

from api.models import Audience, StrategicGoal


class TriggerReturn(BaseModel):
    id: UUID
    name: str
    description: str
    core_idea: Optional[str]
    narrative_hook: Optional[str]
    why_it_works: Optional[str]
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    image_prompt: str
    audience_id: UUID
    strategic_goal_id: UUID


class TriggerCreate(BaseModel):
    name: str
    description: str
    core_idea: Optional[str] = None
    narrative_hook: Optional[str] = None
    why_it_works: Optional[str] = None
    image_prompt: str
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    audience_id: UUID
    strategic_goal_id: UUID


class TriggerCreateWithGoal(BaseModel):
    audience_id: UUID
    strategic_goal_id: UUID
    brand_id: UUID


class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    core_idea: Optional[str] = None
    narrative_hook: Optional[str] = None
    why_it_works: Optional[str] = None
    image_prompt: Optional[str] = None
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    strategic_goal_id: Optional[UUID] = None


class TriggerDelete(BaseModel):
    id: UUID


class TriggerAllDelete(BaseModel):
    audience_id: UUID


class GenerateTriggerImageRequest(BaseModel):
    brand_id: UUID
    trigger_id: UUID | None = None
