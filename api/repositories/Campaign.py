from sqlmodel import select
from api.models import Campaign
from api.schemas import CampaignCreate, CampaignUpdate
from core.db import SessionDep
from uuid import UUID


class CampaignRepository:

    @staticmethod
    async def get_campaign_by_id(campaign_id: UUID, session: SessionDep) -> Campaign:
        statement = select(Campaign).where(Campaign.id == campaign_id)
        result = session.exec(statement)
        return result.one_or_none()

    @staticmethod
    async def get_campaigns_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> list[Campaign]:
        statement = select(Campaign).where(Campaign.brand_id == brand_id)
        result = session.exec(statement)
        return result.all()

    @staticmethod
    async def create_campaign(
        campaign: CampaignCreate, session: SessionDep
    ) -> Campaign:
        db_campaign = Campaign.model_validate(campaign)
        session.add(db_campaign)
        session.commit()
        session.refresh(db_campaign)
        return db_campaign

    @staticmethod
    async def update_campaign(
        campaign_id: UUID, campaign: CampaignUpdate, session: SessionDep
    ) -> Campaign:
        db_campaign = session.get(Campaign, campaign_id)
        db_campaign.sqlmodel_update(campaign.model_dump(exclude_unset=True))
        session.add(db_campaign)
        session.commit()
        session.refresh(db_campaign)
        return db_campaign

    @staticmethod
    async def delete_campaign(campaign_id: UUID, session: SessionDep) -> bool:
        db_campaign = session.get(Campaign, campaign_id)
        if not db_campaign:
            return False
        session.delete(db_campaign)
        session.commit()
        return True

    @staticmethod
    async def delete_all_campaigns_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> bool:
        statement = select(Campaign).where(Campaign.brand_id == brand_id)
        result = session.exec(statement)
        campaigns = result.all()
        if not campaigns:
            return False
        for campaign in campaigns:
            session.delete(campaign)
        session.commit()
        return True
