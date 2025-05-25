from typing import List
from fastapi import APIRouter, Depends
from uuid import UUID
from api.schemas import (
    CampaignCreate,
    CampaignReturn,
    CampaignUpdate,
    UserReturn,
)
from api.dependencies import get_current_active_user
from core.db import SessionDep
from api.services import CampaignService

campaign_router = APIRouter(prefix="/campaign", tags=["Campaign"])


@campaign_router.get("/{campaign_id}", response_model=CampaignReturn)
async def get_campaign_by_id(
    campaign_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> CampaignReturn:
    return await CampaignService.get_campaign_by_id(campaign_id, session)


@campaign_router.get("/", response_model=List[CampaignReturn])
async def get_campaigns_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> List[CampaignReturn]:
    print(f"Brand ID: {brand_id}")
    return await CampaignService.get_campaigns_by_brand_id(brand_id, session)


@campaign_router.post("/", response_model=CampaignReturn)
async def create_campaign(
    campaign: CampaignCreate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> CampaignReturn:
    return await CampaignService.create_campaign(campaign, session)


@campaign_router.put("/{campaign_id}", response_model=CampaignReturn)
async def update_campaign(
    campaign_id: UUID,
    campaign: CampaignUpdate,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> CampaignReturn:
    return await CampaignService.update_campaign(campaign_id, campaign, session)


@campaign_router.delete("/{campaign_id}")
async def delete_campaign(
    campaign_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> bool:
    return await CampaignService.delete_campaign(campaign_id, session)


@campaign_router.delete("/delete_all/{brand_id}")
async def delete_all_campaigns_by_brand_id(
    brand_id: UUID,
    session: SessionDep,
    current_user: UserReturn = Depends(get_current_active_user),
) -> bool:
    return await CampaignService.delete_all_campaigns_by_brand_id(brand_id, session)
