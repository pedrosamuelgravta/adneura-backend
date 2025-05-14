from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models import Brand
    from api.models import Trigger
    from api.models import Demographic


class Audience(SQLModel, table=True):
    __tablename__ = "audiences"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
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

    triggers: List["Trigger"] = Relationship(
        back_populates="audience", cascade_delete=True)

    demographics: "Demographic" = Relationship(
        back_populates="audience", cascade_delete=True)

    brand_id: UUID = Field(foreign_key="brands.id")
    brand: "Brand" = Relationship(back_populates="audiences")

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
