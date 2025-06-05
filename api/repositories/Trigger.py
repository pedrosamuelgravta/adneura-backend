from typing import List
from sqlmodel import select
from api.models import Trigger
from api.schemas import TriggerCreate, TriggerUpdate
from core.db import SessionDep
from uuid import UUID


class TriggerRepository:
    @staticmethod
    async def get_all_triggers(session: SessionDep) -> List[Trigger]:
        return session.exec(select(Trigger)).all()

    @staticmethod
    async def get_trigger_by_id(
        trigger_id: UUID, session: SessionDep
    ) -> Trigger | None:
        return session.exec(select(Trigger).where(Trigger.id == trigger_id)).first()

    @staticmethod
    async def get_triggers_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[Trigger]:
        return session.exec(select(Trigger).where(Trigger.brand_id == brand_id)).all()

    @staticmethod
    async def get_all_triggers_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> List[Trigger]:
        return session.exec(
            select(Trigger).where(Trigger.audience_id == audience_id)
        ).all()

    @staticmethod
    async def create_trigger(trigger: TriggerCreate, session: SessionDep) -> Trigger:
        trigger = Trigger.model_validate(trigger)
        session.add(trigger)
        session.commit()
        session.refresh(trigger)
        return trigger

    @staticmethod
    async def update_trigger(
        trigger_id: UUID, trigger: TriggerUpdate, session: SessionDep
    ) -> Trigger | None:
        existing_trigger = session.get(Trigger, trigger_id)
        existing_trigger.sqlmodel_update(trigger)
        session.add(existing_trigger)
        session.commit()
        session.refresh(existing_trigger)
        return existing_trigger

    @staticmethod
    def update_trigger_image_url(
        trigger_id: UUID, image_url: str, session: SessionDep
    ) -> Trigger | None:
        trigger = session.get(Trigger, trigger_id)
        if trigger:
            trigger.trigger_img = image_url
            session.add(trigger)
            session.commit()
            session.refresh(trigger)
            return trigger
        return None

    @staticmethod
    async def delete_trigger(trigger_id: UUID, session: SessionDep) -> Trigger | None:
        existing_trigger = session.get(Trigger, trigger_id)
        session.delete(existing_trigger)
        session.commit()
        return existing_trigger

    @staticmethod
    async def delete_all_triggers_by_audience_id(
        audience_id: UUID, session: SessionDep
    ) -> List[Trigger]:
        existing_triggers = session.exec(
            select(Trigger).where(Trigger.audience_id == audience_id)
        ).all()
        for trigger in existing_triggers:
            session.delete(trigger)
        session.commit()
        return existing_triggers

    @staticmethod
    async def delete_all_triggers_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[Trigger]:
        existing_triggers = session.exec(
            select(Trigger).where(Trigger.brand_id == brand_id)
        ).all()
        for trigger in existing_triggers:
            session.delete(trigger)
        session.commit()
        return existing_triggers
