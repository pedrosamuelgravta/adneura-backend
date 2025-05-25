from uuid import UUID
from typing import List, Optional

from core.db import SessionDep
from core.exceptions import *
from api.schemas import (
    CampaignCreate,
    CampaignReturn,
    CampaignUpdate,
    UserReturn,
)

from api.repositories import CampaignRepository


class CampaignService:

    @staticmethod
    async def get_campaign_by_id(
        campaign_id: UUID, session: SessionDep
    ) -> CampaignReturn:
        campaign = await CampaignRepository.get_campaign_by_id(campaign_id, session)
        if not campaign:
            raise NotFoundException(f"Campaign with id {campaign_id} not found")
        return campaign

    @staticmethod
    async def get_campaigns_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[CampaignReturn]:
        print(brand_id)
        campaigns = await CampaignRepository.get_campaigns_by_brand_id(
            brand_id, session
        )
        if not campaigns:
            raise NotFoundException(f"No campaigns found for brand {brand_id}")
        print(campaigns)
        return campaigns

    @staticmethod
    async def create_campaign(
        campaign: CampaignCreate, session: SessionDep
    ) -> CampaignReturn:
        print(f"Campaign: {campaign}")
        campaign = await CampaignRepository.create_campaign(campaign, session)
        if not campaign:
            raise NotFoundException(f"Campaign with id {campaign.id} not found")
        return campaign

    @staticmethod
    async def update_campaign(
        campaign_id: UUID,
        campaign: CampaignUpdate,
        session: SessionDep,
    ) -> CampaignReturn:
        campaign = await CampaignRepository.update_campaign(
            campaign_id, campaign, session
        )
        if not campaign:
            raise NotFoundException(f"Campaign with id {campaign_id} not found")
        return campaign

    @staticmethod
    async def delete_campaign(campaign_id: UUID, session: SessionDep) -> bool:
        campaign = await CampaignRepository.delete_campaign(campaign_id, session)
        if not campaign:
            raise NotFoundException(f"Campaign with id {campaign_id} not found")
        return campaign

    @staticmethod
    async def delete_all_campaigns_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> bool:
        campaigns = await CampaignRepository.delete_all_campaigns_by_brand_id(
            brand_id, session
        )
        if not campaigns:
            raise NotFoundException(f"No campaigns found for brand {brand_id}")
        return campaigns
