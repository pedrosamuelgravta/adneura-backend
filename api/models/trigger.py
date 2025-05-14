from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models.audience import Audience


class Trigger(SQLModel, table=True):
    __tablename__ = "triggers"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
    image_prompt: str
    trigger_img: Optional[str] = Field(default=None, nullable=True)
    territory: Optional[str] = Field(default=None, nullable=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    audience_id: UUID = Field(foreign_key="audiences.id")
    audience: "Audience" = Relationship(back_populates="triggers")
