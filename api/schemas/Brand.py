from typing import Optional
import re

from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID


class BrandReturn(BaseModel):
    id: UUID
    name: str
    website_url: Optional[str] = None
    about: Optional[str] = Field(default=None, nullable=True)
    key_characteristics: Optional[str] = Field(default=None, nullable=True)
    category: Optional[str] = Field(default=None, nullable=True)
    positioning: Optional[str] = Field(default=None, nullable=True)
    traditional_target_audience: Optional[str] = Field(
        default=None, nullable=True)
    key_competitors: Optional[str] = Field(default=None, nullable=True)
    first_access: bool = Field(default=False)
    brand_summary_active: bool = Field(default=False, nullable=True)
    ad_legacy_active: bool = Field(default=False, nullable=True)
    strategic_goals_active: bool = Field(default=False, nullable=True)
    audience_active: bool = Field(default=False, nullable=True)
    brand_universe_active: bool = Field(default=False, nullable=True)
    user_id: UUID


class BrandCreate(BaseModel):
    name: str
    website_url: Optional[str] = None


class BrandUpdate(BaseModel):
    name: Optional[str] = None
    website_url: Optional[str] = None
    about: Optional[str] = Field(default=None, nullable=True)
    key_characteristics: Optional[str] = Field(default=None, nullable=True)
    category: Optional[str] = Field(default=None, nullable=True)
    positioning: Optional[str] = Field(default=None, nullable=True)
    traditional_target_audience: Optional[str] = Field(
        default=None, nullable=True)
    key_competitors: Optional[str] = Field(default=None, nullable=True)
    first_access: Optional[bool] = Field(default=False)
    brand_summary_active: Optional[bool] = Field(default=False, nullable=True)
    ad_legacy_active: Optional[bool] = Field(default=False, nullable=True)
    strategic_goals_active: Optional[bool] = Field(
        default=False, nullable=True)
    audience_active: Optional[bool] = Field(default=False, nullable=True)
    brand_universe_active: Optional[bool] = Field(default=False, nullable=True)
    prompt: Optional[str] = Field(default=None, nullable=True)
    rerun_step: Optional[str] = Field(default=None, nullable=True)
