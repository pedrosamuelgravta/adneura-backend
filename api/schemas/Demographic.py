from typing import Optional

from pydantic import BaseModel
from uuid import UUID


class DemographicReturn(BaseModel):
    id: UUID
    gender: Optional[str] = None
    age_bracket: Optional[str] = None
    hhi: Optional[str] = None
    ethnicity: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
    audience_id: UUID


class DemographicCreate(BaseModel):
    gender: str
    age_bracket: str
    hhi: str
    ethnicity: str
    education: str
    location: str
    audience_id: UUID


class DemographicUpdate(BaseModel):
    gender: Optional[str] = None
    age_bracket: Optional[str] = None
    hhi: Optional[str] = None
    ethnicity: Optional[str] = None
    education: Optional[str] = None
    location: Optional[str] = None
