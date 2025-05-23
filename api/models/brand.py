from typing import Optional, List, TYPE_CHECKING

from sqlmodel import Field, SQLModel, Relationship
from uuid import UUID, uuid4

from datetime import datetime, timezone

if TYPE_CHECKING:
    from api.models.user import User
    from api.models.audience import Audience
    from api.models.campaign import Campaign


class Brand(SQLModel, table=True):
    __tablename__ = "brands"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    website_url: Optional[str] = None

    about: Optional[str] = Field(default=None, nullable=True)
    key_characteristics: Optional[str] = Field(default=None, nullable=True)
    category: Optional[str] = Field(default=None, nullable=True)
    positioning: Optional[str] = Field(default=None, nullable=True)
    target_audience: Optional[str] = Field(default=None, nullable=True)
    key_competitors: Optional[str] = Field(default=None, nullable=True)
    first_access: bool = Field(default=False)

    brand_summary_active: bool = Field(default=False, nullable=True)
    ad_legacy_active: bool = Field(default=False, nullable=True)
    strategic_goals_active: bool = Field(default=False, nullable=True)
    audience_active: bool = Field(default=False, nullable=True)
    brand_universe_active: bool = Field(default=False, nullable=True)

    user_id: UUID = Field(foreign_key="users.id")
    user: Optional["User"] = Relationship(back_populates="brands")
    audiences: List["Audience"] = Relationship(
        back_populates="brand", cascade_delete=True
    )
    campaigns: List["Campaign"] = Relationship(
        back_populates="brand", cascade_delete=True
    )

    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
