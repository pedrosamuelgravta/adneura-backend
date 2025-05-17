from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models import Audience


class Demographic(SQLModel, table=True):
    __tablename__ = "demographics"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    audience_id: UUID = Field(foreign_key="audiences.id")
    audience: "Audience" = Relationship(back_populates="demographics")
    gender: Optional[str] = Field(default=None, nullable=True)
    age_bracket: Optional[str] = Field(default=None, nullable=True)
    hhi: Optional[str] = Field(default=None, nullable=True)
    ethnicity: Optional[str] = Field(default=None, nullable=True)
    education: Optional[str] = Field(default=None, nullable=True)
    location: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
