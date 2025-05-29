from typing import List
from uuid import UUID
from fastapi.responses import JSONResponse

from core.db import SessionDep
from api.services import OpenAiService, StrategicGoalService
from api.repositories import (
    TriggerRepository,
    AudienceRepository,
    BrandRepository,
    StrategicGoalRepository,
)
from api.schemas import TriggerUpdate, TriggerCreate, TriggerReturn, TriggerCreateWithGoal
from core.exceptions import *


class TriggerService:
    @staticmethod
    async def get_all_triggers(session: SessionDep) -> List[TriggerReturn]:
        return await TriggerRepository.get_all_triggers(session)

    @staticmethod
    async def get_all_triggers_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> List[TriggerReturn]:
        return await TriggerRepository.get_all_triggers_by_audience(
            audience_id, session
        )

    @staticmethod
    async def get_trigger_by_id(trigger_id: UUID, session: SessionDep) -> TriggerReturn:
        trigger = await TriggerRepository.get_trigger_by_id(trigger_id, session)
        if not trigger:
            raise NotFoundException(f"Trigger with id {trigger_id} not found")
        return trigger

    @staticmethod
    async def get_triggers_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[TriggerReturn]:
        return await TriggerRepository.get_triggers_by_brand_id(brand_id, session)

    @staticmethod
    async def create_trigger(
        trigger: TriggerCreate, session: SessionDep
    ) -> TriggerReturn:
        trigger_obj = await TriggerRepository.create_trigger(trigger, session)
        if not trigger_obj:
            raise NotFoundException(
                f"Trigger with id {trigger_obj.id} not found")
        return trigger_obj

    @staticmethod
    async def generate_initial_triggers(
        audience_id: UUID, session: SessionDep
    ) -> JSONResponse:
        audience = await AudienceRepository.get_audience_by_id(audience_id, session)
        if not audience:
            raise NotFoundException(
                f"Audience with id {audience_id} not found")
        brand = await BrandRepository.get_brand_by_id(audience.brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {audience.brand_id} not found")
        strategic_goals = (
            await StrategicGoalService.get_all_strategic_goals_by_brand_id(
                audience.brand_id, session
            )
        )
        if not strategic_goals:
            raise NotFoundException(
                f"Strategic goals with brand id {audience.brand_id} not found"
            )

        response = await OpenAiService.chat(
            system=f"""
                    You are a behavioral strategist and emotional narrative expert, influenced by Rory Sutherland, Lisa Feldman Barrett, and Les Binet.
                    Your job is to surface key emotional moments, habits, or unmet needs that make people act — and frame how brands can authentically show up.
                    You are equal parts behavioral economist and creative planner.
                    """,
            assistant=f"",
            user=f"""
                Considering
                {brand.name},
                {brand.about},
                {brand.category},
                {brand.key_characteristics},
                {brand.positioning},
                the audience {audience.name} described as {audience.description}.
                Focus on the psychographics, attitudinal, self-concept and lifestyle.

                Create 3 very distinct and relevant message triggers for each {strategic_goals}.
                Pinpoint specific life events, emotions, or circumstances that move this audience towards the brand goals. These could range from seasonal needs to personal milestones.

                For each trigger, describe the trigger and how it will motivate the specific audience.
                Create an amazing title for it with one or two main words.
                Imporant, if the trigger of one audience is the same of another audience use the exactly same name to keep consistency. If they are similar, but the motiffs are different, use different names.
                Create a scene description that best describes each trigger.
                Also, bring the scene in prompt format to be used in a text to image GenAI.

                For each trigger, follow this exact structure:


                Title: [Trigger Title]
                Description: [1 paragraph summarizing the message trigger]
                Core Idea: [1 paragraph describing the core idea behind the message trigger]
                Narrative Hook: [1 paragraph describing how the brand, service or product is part of the audience routine]
                Why it Works: [1 paragraph explaining why this message trigger will work with this audience]
                Goal: [pick the most appropriate goal_name from the list above and output **only** that exact goal_name string]
                Campaign Name: [output exactly the campaign_name string from the current strategic_goals object]
                Image Prompt: [generate a prompt to be used in text to image GenAI to create a scene that best describes the message trigger. Make sure it represents the trigger and its target audience. Generate a detailed image and include the best product, service or brand best fit for the audience]

                Output Instructions:
                - Do not include introductions, explanations, or headers.
                - Start directly with the first demographic detail.
                - Use plain text formatting (no bold, asterisks, or quotation marks).
                - Avoid repeating any part of the user's input.
                - Follow the structure strictly and consistently.

                """,
            session=session,
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
                .split("Core Idea:")[0]
                .strip(),
                "core_idea": trigger_text.split("Core Idea:")[1]
                .split("Narrative Hook:")[0]
                .strip(),
                "narrative_hook": trigger_text.split("Narrative Hook:")[1]
                .split("Why it Works:")[0]
                .strip(),
                "why_it_works": trigger_text.split("Why it Works:")[1]
                .split("Goal:")[0]
                .strip(),
                "goal": trigger_text.split("Goal:")[1]
                .split("Campaign Name:")[0]
                .strip(),
                "campaign_name": trigger_text.split("Campaign Name:")[1]
                .split("Image Prompt:")[0]
                .strip(),
                "image_prompt": trigger_text.split("Image Prompt:")[1].strip(),
            }
            parsed_triggers.append(sections)

        color_map = ["#3FE2E8", "#FF36C3", "#FFD036"]

        for idx, trigger in enumerate(parsed_triggers):

            color = color_map[idx % len(color_map)]

            trigger_obj = {
                "name": trigger["title"],
                "description": trigger["description"],
                "core_idea": trigger["core_idea"],
                "narrative_hook": trigger["narrative_hook"],
                "why_it_works": trigger["why_it_works"],
                "goal": trigger["goal"],
                "campaign_name": trigger["campaign_name"],
                "goal_color": color.replace("#", ""),
                "image_prompt": trigger["image_prompt"],
                "audience_id": audience_id,
            }

            await TriggerRepository.create_trigger(trigger_obj, session)

        return JSONResponse(
            content={
                "message": f"Triggers to Audience ID {audience_id} created successfully"
            },
            status_code=201,
        )

    @staticmethod
    async def generate_triggers_with_goal(
        body: TriggerCreateWithGoal,
        session: SessionDep
    ) -> JSONResponse:
        audience = await AudienceRepository.get_audience_by_id(body.audience_id, session)
        if not audience:
            raise NotFoundException(
                f"Audience with id {body.audience_id} not found")

        brand = await BrandRepository.get_brand_by_id(audience.brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {audience.brand_id} not found")

        prompt = f"""
                Considering
                {brand.name},
                {brand.about},
                {brand.category},
                {brand.key_characteristics},
                {brand.positioning},
                the audience {audience.name} described as {audience.description}.
                Focus on the psychographics, attitudinal, self-concept and lifestyle.

                Create a relevant message trigger for this goal: {body.goal}.
                Pinpoint specific life events, emotions, or circumstances that move this audience towards the brand goals. These could range from seasonal needs to personal milestones.

                For trigger, describe the trigger and how it will motivate the specific audience.
                Create an amazing title for it with one or two main words.
                Imporant, if the trigger of one audience is the same of another audience use the exactly same name to keep consistency. If they are similar, but the motiffs are different, use different names.
                Create a scene description that best describes trigger.
                Also, bring the scene in prompt format to be used in a text to image GenAI.

                For trigger, follow this exact structure:


                Title: [Trigger Title]
                Description: [1 paragraph summarizing the message trigger]
                Core Idea: [1 paragraph describing the core idea behind the message trigger]
                Narrative Hook: [1 paragraph describing how the brand, service or product is part of the audience routine]
                Why it Works: [1 paragraph explaining why this message trigger will work with this audience]
                Goal: [use exactly the name of the goal referenced above]
                Image Prompt: [generate a prompt to be used in text to image GenAI to create a scene that best describes the message trigger. Make sure it represents the trigger and its target audience. Generate a detailed image and include the best product, service or brand best fit for the audience]

                Output Instructions:
                - Do not include introductions, explanations, or headers.
                - Start directly with the first demographic detail.
                - Use plain text formatting (no bold, asterisks, or quotation marks).
                - Avoid repeating any part of the user's input.
                - Follow the structure strictly and consistently.

        """

        response = await OpenAiService.chat(
            system="You are a behavioral strategist creating emotionally resonant triggers.",
            assistant="",
            user=prompt,
            session=session,
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
                "description": trigger_text.split("Description:")[1].split("Core Idea:")[0].strip(),
                "core_idea": trigger_text.split("Core Idea:")[1].split("Narrative Hook:")[0].strip(),
                "narrative_hook": trigger_text.split("Narrative Hook:")[1].split("Why it Works:")[0].strip(),
                "why_it_works": trigger_text.split("Why it Works:")[1].split("Goal:")[0].strip(),
                "goal": trigger_text.split("Goal:")[1].split("Image Prompt:")[0].strip(),
                "image_prompt": trigger_text.split("Image Prompt:")[1].strip(),
            }
            parsed_triggers.append(sections)

        created = []
        for trigger in parsed_triggers:
            trigger_obj = {
                "name": trigger["title"],
                "description": trigger["description"],
                "core_idea": trigger["core_idea"],
                "narrative_hook": trigger["narrative_hook"],
                "why_it_works": trigger["why_it_works"],
                "goal": trigger["goal"],
                "image_prompt": trigger["image_prompt"],
                "campaign_name": body.campaign_name,
                "goal_color": body.goal_color,
                "audience_id": body.audience_id,
            }
            print(trigger_obj)
            created_trigger = await TriggerRepository.create_trigger(trigger_obj, session)
            created.append(created_trigger)

        return JSONResponse(
            content={
                "message": f"Triggers for Audience ID {body.audience_id} created successfully"
            },
            status_code=201,
        )

    @staticmethod
    async def update_trigger(
        trigger_id: UUID, trigger: TriggerUpdate, session: SessionDep
    ) -> TriggerReturn:
        return await TriggerRepository.update_trigger(trigger_id, trigger, session)

    @staticmethod
    async def delete_trigger(trigger_id: UUID, session: SessionDep) -> TriggerReturn:
        return await TriggerRepository.delete_trigger(trigger_id, session)

    @staticmethod
    async def delete_all_triggers_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> List[TriggerReturn]:
        return await TriggerRepository.delete_all_triggers_by_audience(
            audience_id, session
        )
