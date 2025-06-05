from typing import Optional, TYPE_CHECKING, List

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models.campaign import Campaign
    from api.models.trigger import Trigger


class StrategicGoal(SQLModel, table=True):
    __tablename__ = "strategic_goals"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    strategic_goal: str
    is_active: bool = Field(default=True)
    strategic_goal_color: Optional[str] = Field(
        default=None, nullable=True, description="Color associated with the strategic goal"
    )
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )

    campaign_id: UUID = Field(foreign_key="campaigns.id")
    campaign: Optional["Campaign"] = Relationship(
        back_populates="strategic_goals")

    triggers: List["Trigger"] = Relationship(
        back_populates="strategic_goal"
    )
