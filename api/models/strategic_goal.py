from typing import Optional, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models.brand import Brand


class StrategicGoal(SQLModel, table=True):
    __tablename__ = "strategic_goals"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    strategic_goal: str
    is_active: bool = Field(default=True)
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    brand_id: UUID = Field(foreign_key="brands.id")
    brand: "Brand" = Relationship(back_populates="strategic_goals")
