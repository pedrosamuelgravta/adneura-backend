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
from api.schemas import (
    TriggerUpdate,
    TriggerCreate,
    TriggerReturn,
    TriggerCreateWithGoal,
)
from core.exceptions import *

from tasks.image import image_generation


class TriggerService:
    @staticmethod
    async def get_all_triggers(session: SessionDep) -> List[TriggerReturn]:
        return await TriggerRepository.get_all_triggers(session)

    @staticmethod
    async def get_all_triggers_by_audience(
        audience_id: UUID, session: SessionDep
    ) -> List[TriggerReturn]:
        print(audience_id)
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
        print("mapping strategic goals",
              list(map(lambda goal: {
                  "goal_name": goal["goal_name"],
                  "campaign_name": goal["campaign_name"],
              }, strategic_goals)))
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

                Create 3 very distinct and relevant message triggers for each {list(map(lambda goal: {
                "goal_name": goal["goal_name"],
                "campaign_name": goal["campaign_name"],
            }, strategic_goals))}.
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

        if len(parsed_triggers) != 3:
            print(
                f"Expected 3 triggers, but got {len(parsed_triggers)}. Retrying generation...")
            return await TriggerService.generate_initial_triggers(audience_id, session)

        for trigger in parsed_triggers:

            strategic_goal_filtered = next(
                (goal for goal in strategic_goals if goal["goal_name"] == trigger["goal"]),
                None,
            )
            if not strategic_goal_filtered:
                continue

            trigger_obj = {
                "name": trigger["title"],
                "description": trigger["description"],
                "core_idea": trigger["core_idea"],
                "narrative_hook": trigger["narrative_hook"],
                "why_it_works": trigger["why_it_works"],
                "image_prompt": trigger["image_prompt"],
                "audience_id": audience_id,
                "strategic_goal_id": strategic_goal_filtered["goal_id"]
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
        body: TriggerCreateWithGoal, session: SessionDep
    ) -> JSONResponse:
        audience = await AudienceRepository.get_audience_by_id(
            body.audience_id, session
        )
        if not audience:
            raise NotFoundException(
                f"Audience with id {body.audience_id} not found")

        brand = await BrandRepository.get_brand_by_id(audience.brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {audience.brand_id} not found")

        strategic_goal = await StrategicGoalRepository.get_strategic_goal_by_id(
            body.strategic_goal_id, session
        )
        if not strategic_goal:
            raise NotFoundException(
                f"Strategic goal with id {body.strategic_goal_id} not found")
        all_triggers = await TriggerRepository.get_triggers_by_brand_id(body.brand_id, session)
        unique_territories = set()
        for trigger in all_triggers:
            if trigger.territory:
                unique_territories.add(trigger.territory)

        unique_territories = list(unique_territories)

        prompt = f"""
                Considering
                {brand.name},
                {brand.about},
                {brand.category},
                {brand.key_characteristics},
                {brand.positioning},
                territory list: {unique_territories},
                the audience {audience.name} described as {audience.description}.
                Focus on the psychographics, attitudinal, self-concept and lifestyle.

                Create a relevant message trigger for this goal: {strategic_goal.strategic_goal}.
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
                Image Prompt: [generate a prompt to be used in text to image GenAI to create a scene that best describes the message trigger. Make sure it represents the trigger and its target audience. Generate a detailed image and include the best product, service or brand best fit for the audience]
                territory: [pick one of the territories from the list above and output exactly that territory name]

                Output Instructions:
                - Do not include introductions, explanations, or headers.
                - Start directly with the first demographic detail.
                - Use plain text formatting (no bold, asterisks, or quotation marks).
                - Avoid repeating any part of the user's input.
                - Follow the structure strictly and consistently.
                - use the exact name of the territory from the list above.
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
                .split("Image Prompt:")[0]
                .strip(),
                "image_prompt": trigger_text.split("Image Prompt:")[1]
                .split("territory:")[0]
                .strip(),
                "territory": trigger_text.split("territory:")[1].strip(),
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
                "image_prompt": trigger["image_prompt"],
                "territory": trigger["territory"],
                "audience_id": body.audience_id,
                "strategic_goal_id": body.strategic_goal_id
            }
            created_trigger = await TriggerRepository.create_trigger(
                trigger_obj, session
            )
            created.append(created_trigger.model_dump())

        return JSONResponse(
            content={
                "message": f"Triggers for Audience ID {body.audience_id} created successfully",
                "trigger_id": [str(trigger["id"]) for trigger in created],
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
        return await TriggerRepository.delete_all_triggers_by_audience_id(
            audience_id, session
        )

    @staticmethod
    async def generate_trigger_image(
        brand_id: UUID,
        session: SessionDep,
        trigger_id: UUID = None,
    ) -> JSONResponse:
        scheduled = 0
        audiences = await AudienceRepository.get_all_audiences_by_brand_id(
            brand_id, session
        )

        if not audiences:
            raise NotFoundException(
                f"No audiences found for brand with id {brand_id}")

        for audience in audiences:
            triggers_qs = await TriggerRepository.get_all_triggers_by_audience(
                audience.id, session
            )

            if trigger_id:
                triggers_qs = [
                    trigger for trigger in triggers_qs if trigger.id == trigger_id
                ]

            for trigger in triggers_qs:
                t_id = trigger.id
                has_img = bool(trigger.trigger_img)

                if not has_img:
                    file_name = f"B{brand_id}A{audience.id}T{t_id}img.jpg"
                    image_generation.delay(
                        trigger.image_prompt, file_name, "trigger", str(t_id)
                    )

                    scheduled += 1
                    print(
                        f"   • Agendada task para trigger {t_id} (total agendadas: {scheduled})"
                    )

        return JSONResponse(
            content={
                "message": f"Image generation tasks scheduled for {scheduled} triggers."
            },
            status_code=200,
        )

    @staticmethod
    async def group_triggers_into_territories(
        brand_id: UUID, session: SessionDep
    ) -> JSONResponse:
        audiences = await AudienceRepository.get_all_audiences_by_brand_id(
            brand_id, session
        )
        if not audiences:
            raise NotFoundException(
                f"No audiences found for brand with id {brand_id}")

        brand = await BrandRepository.get_brand_by_id(brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {brand_id} not found")

        # Get all triggers across all audiences
        all_triggers_list = []
        audiences_data = []
        all_triggers_set = set()

        for audience in audiences:
            triggers = await TriggerRepository.get_all_triggers_by_audience(
                audience.id, session
            )
            audience_info = {
                "name": audience.name,
                "description": audience.description,
                "key_tags": audience.key_tags,
                "psycho_graphic": audience.psycho_graphic,
                "attitudinal": audience.attitudinal,
                "self_concept": audience.self_concept,
                "lifestyle": audience.lifestyle,
                "media_habits": audience.media_habits,
                "general_keywords": audience.general_keywords,
                "brand_keywords": audience.brand_keywords,
                "triggers": [
                    {"name": trigger.name, "description": trigger.description}
                    for trigger in triggers
                ],
            }
            for trigger in triggers:
                all_triggers_set.add(trigger.name)
                all_triggers_list.append({
                    "id": trigger.id,
                    "name": trigger.name,
                    "audience_name": audience.name
                })

            audiences_data.append(audience_info)

        # Format audiences data for the prompt
        formatted_audiences = "\n\n".join(
            f"### Audience: {audience['name']}\n"
            f"Description: {audience['description']}\n"
            f"Key Tags: {audience['key_tags']}\n"
            f"Psycho-graphic: {audience['psycho_graphic']}\n"
            f"Attitudinal: {audience['attitudinal']}\n"
            f"Self Concept: {audience['self_concept']}\n"
            f"Lifestyle: {audience['lifestyle']}\n"
            f"Media Habits: {audience['media_habits']}\n"
            f"Triggers:\n"
            + "\n".join(
                f"- {trigger['name']}: {trigger['description']}"
                for trigger in audience["triggers"]
            )
            for audience in audiences_data
        )

        response = await OpenAiService.chat(
            system=f"""
            You are a seasoned strategic planner, inspired by industry
            legends like Jon Steel, Rosie Yakob, and Russell Davies.
            You have extensive experience in analyzing brands and crafting
            positioning strategies with a sharp focus on consumer insights
            and market analysis.
            """,
            assistant=f"""
            Considering the following Audiences details:
                Target Audiences: {brand.traditional_target_audience}  
                {formatted_audiences}
            """,
            user=f"""
            Group the triggers into 6-8 distinctive groups. Group triggers that are alike or have the same motivations.
            Each and every trigger must be assigned to a group.
            Name the groups with a one or two main words' title different from the name of the triggers. 
            Describe each group relevance and the opportunities the brand has to communicate within it. 
            List the territories and each trigger that belongs to it indicating in parenthesis its Audience.
            *you must assign all of the following triggers exactly once*:  
            {all_triggers_set} 

            ### *Output Instructions*  
            - No trigger must be placed in two or more groups.
            - Do not give a group the same name of an existing trigger.
            - Do not create new triggers.
            - Do not include introductions, explanations, or headers.  
            - Follow this structure *exactly* for each brand territory:  

            Brand Territory: [Group Name]  
            Relevance: [Short description of the group's strategic role]  
            Opportunities: [How the brand can communicate within this group]  
            Triggers:  
            - [Trigger Name] ([Audience Name])
            """,
            session=session,
        )

        # Handle OpenAI response directly since it's already a string
        content = response

        territories = content.split("Brand Territory:")
        territories = territories[1:]  # Remove empty first element

        sections = []
        applied_triggers_set = set()

        for territory in territories:
            section = {
                "name": territory.split("Relevance:")[0].strip(),
                "relevance": territory.split("Relevance:")[1]
                .split("Opportunities:")[0]
                .strip(),
                "opportunities": territory.split("Opportunities:")[1]
                .split("Triggers:")[0]
                .strip(),
                "triggers": [
                    trigger.split("(")[0].strip("- ").strip()
                    for trigger in territory.split("Triggers:")[1]
                    .strip()
                    .split("\n")
                    if trigger.strip("- ").strip() != ""
                ],
            }
            if section["triggers"]:
                applied_triggers_set.update(section["triggers"])
                sections.append(section)

        missing_triggers = list(all_triggers_set - applied_triggers_set)

        # Update territory field for all triggers
        matched_triggers = []
        for audience in audiences:
            triggers = await TriggerRepository.get_all_triggers_by_audience(
                audience.id, session
            )
            for trigger in triggers:
                for section in sections:
                    if trigger.name in section["triggers"]:
                        matched_triggers.append({
                            # Convert UUID to string
                            "audience_id": str(audience.id),
                            # Convert UUID to string
                            "trigger_id": str(trigger.id),
                            "trigger_name": trigger.name,
                            "territory": section["name"]
                        })
                        # Update only the territory field
                        update_data = TriggerUpdate(territory=section["name"])
                        await TriggerRepository.update_trigger(
                            trigger.id,
                            update_data,
                            session
                        )

        matched_triggers_sorted = sorted(
            matched_triggers, key=lambda x: x["audience_id"]
        )

        return JSONResponse(
            content={
                "content": sections,
                "summary": {
                    "total_triggers": len(all_triggers_set),
                    "applied_triggers": len(applied_triggers_set),
                    "missing_triggers": missing_triggers,
                },
                "matched_triggers": matched_triggers_sorted,
            },
            status_code=200,
        )
