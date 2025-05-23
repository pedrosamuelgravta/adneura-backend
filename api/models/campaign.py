from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models.brand import Brand
    from api.models.strategic_goal import StrategicGoal


class Campaign(SQLModel, table=True):
    __tablename__ = "campaigns"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    campaign: str
    is_active: bool = Field(default=True)
    is_completed: bool = Field(default=False)
    brand_id: UUID = Field(foreign_key="brands.id")
    brand: Optional["Brand"] = Relationship(back_populates="campaigns")
    strategic_goals: List["StrategicGoal"] = Relationship(
        back_populates="campaign", cascade_delete=True
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
