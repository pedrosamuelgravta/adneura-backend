from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse

from core.db import SessionDep
from api.services import OpenAiService
from api.repositories import TriggerRepository, AudienceRepository, BrandRepository, StrategicGoalRepository
from api.schemas import TriggerUpdate, TriggerCreate, TriggerReturn
from core.exceptions import *


class TriggerService:
    @staticmethod
    async def get_all_triggers(session: SessionDep) -> List[TriggerReturn]:
        return await TriggerRepository.get_all_triggers(session)

    @staticmethod
    async def get_all_triggers_by_audience(audience_id: UUID, session: SessionDep) -> List[TriggerReturn]:
        return await TriggerRepository.get_all_triggers_by_audience(audience_id, session)

    @staticmethod
    async def get_trigger_by_id(trigger_id: UUID, session: SessionDep) -> TriggerReturn:
        trigger = await TriggerRepository.get_trigger_by_id(trigger_id, session)
        if not trigger:
            raise NotFoundException(f"Trigger with id {trigger_id} not found")
        return trigger

    @staticmethod
    async def get_triggers_by_brand_id(brand_id: UUID, session: SessionDep) -> List[TriggerReturn]:
        return await TriggerRepository.get_triggers_by_brand_id(brand_id, session)

    @staticmethod
    async def create_trigger(trigger: TriggerCreate, session: SessionDep) -> TriggerReturn:
        trigger_obj = await TriggerRepository.create_trigger(trigger, session)
        if not trigger_obj:
            raise NotFoundException(
                f"Trigger with id {trigger_obj.id} not found")
        return trigger_obj

    @staticmethod
    async def generate_initial_triggers(
        audience_id: UUID, session: SessionDep
    ) -> JSONResponse:
        audience = await AudienceRepository.get_audience_by_id(
            audience_id, session
        )
        if not audience:
            raise NotFoundException(
                f"Audience with id {audience_id} not found"
            )
        brand = await BrandRepository.get_brand_by_id(
            audience.brand_id, session
        )
        if not brand:
            raise NotFoundException(
                f"Brand with id {audience.brand_id} not found"
            )
        strategic_goals = await StrategicGoalRepository.get_strategic_goals_by_brand_id(
            audience.brand_id, session
        )
        if not strategic_goals:
            raise NotFoundException(
                f"Strategic goals with brand id {audience.brand_id} not found"
            )

        response = OpenAiService.chat(
            system=f"""
                    Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies.
                    You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and market analysis.
                    Your task is to create a text according to the instructions provided by the user. Always return only the edited content,
                    without any introductions, preambles, or explanations. The output should strictly contain the updated text as per the
                    instructions, and nothing else.
                    """,
            user=f"""
                Considering
                {brand.name},
                {brand.about},
                {brand.category},
                {brand.key_characteristics},
                {brand.positioning},
                the audience {audience.name} described as {audience.description}.
                Focus on the psychographics, attitudinal, self-concept and lifestyle.

                Create 3 very distinct and relevant message triggers for each {strategic_goals}. Pinpoint specific life events, emotions, or circumstances that move this audience towards the brand goals. These could range from seasonal needs to personal milestones.
                For each trigger, describe the trigger and how it will motivate the specific audience.
                Create an amazing title for it. But, if what moves that audience is the same as another audience, keep the same trigger name.
                Create a scene description that best describes each trigger.
                Also, bring the scene in prompt format to be used in a text to image GenAI.
                For each trigger, follow this exact structure:

                Title: [Trigger Title]
                Description: [1 paragraph describing the trigger]
                Image Prompt: [generate a prompt to be used in text to image GenAI to create a scene that best describes the trigger. Make sure it represents the trigger and its target audience. Generate a detailed image and landscape oriented, 16:9]

                Output Instructions:
                - Do not include introductions, explanations, or headers.
                - Start directly with the first demographic detail.
                - Use plain text formatting (no bold, asterisks, or quotation marks).
                - Avoid repeating any part of the user's input.
                - Follow the structure strictly and consistently.

                """,
        )

        content_list = response.split("Title:")
        new_triggers = []
        for i in range(1, len(content_list)):
            trigger_text = content_list[i]
            if i < len(content_list) - 1:
                trigger_text = trigger_text[: trigger_text.find("Title:")]
            new_triggers.append(trigger_text.strip())

        parsed_triggers = []
        for trigger_text in new_triggers:
            sections = {
                "title": trigger_text.split("Description:")[0].strip(),
                "description": trigger_text.split("Description:")[1]
                .split("Image Prompt:")[0]
                .strip(),
                "image_prompt": trigger_text.split("Image Prompt:")[1].strip(),
            }
            parsed_triggers.append(sections)

        for trigger in parsed_triggers:
            trigger_obj = {
                "title": trigger["title"],
                "description": trigger["description"],
                "image_prompt": trigger["image_prompt"],
                "audience_id": audience_id,
            }

            await TriggerRepository.create_trigger(
                trigger_obj, session
            )

        return JSONResponse(
            content={"message": "Triggers created successfully"},
            status_code=201,
        )

    @staticmethod
    async def update_trigger(
        trigger_id: UUID, trigger: TriggerUpdate, session: SessionDep
    ) -> TriggerReturn:
        return await TriggerRepository.update_trigger(trigger_id, trigger, session)

    @staticmethod
    async def delete_trigger(
        trigger_id: UUID, session: SessionDep
    ) -> TriggerReturn:
        return await TriggerRepository.delete_trigger(trigger_id, session)

    @staticmethod
    async def delete_all_triggers_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> List[TriggerReturn]:
        return await TriggerRepository.delete_all_triggers_by_audience(audience_id, session)
