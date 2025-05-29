from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class TriggerReturn(BaseModel):
    id: UUID
    name: str
    description: str
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    audience_id: UUID


class TriggerCreate(BaseModel):
    name: str
    description: str
    image_prompt: str
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    audience_id: UUID


class TriggerCreateWithGoal(BaseModel):
    audience_id: UUID
    campaign_name: str
    goal: str
    goal_color: str


class TriggerUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    image_prompt: Optional[str] = None
    trigger_img: Optional[str] = None
    territory: Optional[str] = None
    audience_id: Optional[UUID] = None


class TriggerDelete(BaseModel):
    id: UUID


class TriggerAllDelete(BaseModel):
    audience_id: UUID
