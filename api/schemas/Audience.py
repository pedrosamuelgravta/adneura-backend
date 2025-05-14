from typing import Optional, List
import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID

from api.models import Trigger, Demographic


class AudienceReturn(BaseModel):
    id: UUID
    name: str
    description: str
    image_url: str
    key_tags: str
    psycho_graphic: str
    attitudinal: str
    self_concept: str
    lifestyle: str
    media_habits: str
    general_keywords: str
    brand_keywords: str
    triggers: List["Trigger"]
    demographics: "Demographic"


class AudienceCreate(BaseModel):
    name: str
    description: Optional[str] = Field(default=None, nullable=True)
    image_prompt: Optional[str] = Field(default=None, nullable=True)
    image_url: Optional[str] = Field(default=None, nullable=True)
    key_tags: Optional[str] = Field(default=None, nullable=True)
    psycho_graphic: Optional[str] = Field(default=None, nullable=True)
    attitudinal: Optional[str] = Field(default=None, nullable=True)
    self_concept: Optional[str] = Field(default=None, nullable=True)
    lifestyle: Optional[str] = Field(default=None, nullable=True)
    media_habits: Optional[str] = Field(default=None, nullable=True)
    general_keywords: Optional[str] = Field(default=None, nullable=True)
    brand_keywords: Optional[str] = Field(default=None, nullable=True)


class AudienceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = Field(default=None, nullable=True)
    image_prompt: Optional[str] = Field(default=None, nullable=True)
    image_url: Optional[str] = Field(default=None, nullable=True)
    key_tags: Optional[str] = Field(default=None, nullable=True)
    psycho_graphic: Optional[str] = Field(default=None, nullable=True)
    attitudinal: Optional[str] = Field(default=None, nullable=True)
    self_concept: Optional[str] = Field(default=None, nullable=True)
    lifestyle: Optional[str] = Field(default=None, nullable=True)
    media_habits: Optional[str] = Field(default=None, nullable=True)
    general_keywords: Optional[str] = Field(default=None, nullable=True)
    brand_keywords: Optional[str] = Field(default=None, nullable=True)


class AudienceDelete(BaseModel):
    id: UUID
    name: str
    description: str
