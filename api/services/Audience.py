from uuid import UUID
from typing import List
from api.repositories import AudienceRepository, BrandRepository, DemographicRepository
from api.models import User
from api.schemas import (
    AudienceCreate,
    AudienceReturn,
    AudienceUpdate,
    AudienceAiGenerate,
    AudienceGenerateResponse,
)
from core.exceptions import *
from core.db import SessionDep

from api.services import OpenAiService
from fastapi.responses import JSONResponse
from tasks.image import image_generation


class AudienceService:
    @staticmethod
    async def get_all_audiences_by_brand_id(
        brand_id: UUID, session: SessionDep
    ) -> List[AudienceReturn]:
        return await AudienceRepository.get_all_audiences_by_brand_id(brand_id, session)

    @staticmethod
    async def get_all_audiences_by_user(
        user_id: UUID, session: SessionDep
    ) -> List[AudienceReturn]:
        return await AudienceRepository.get_all_audiences_by_user(user_id, session)

    @staticmethod
    async def get_audience_by_id(
        audience_id: UUID, session: SessionDep
    ) -> AudienceReturn:
        audience = await AudienceRepository.get_audience_by_id(audience_id, session)
        if not audience:
            raise NotFoundException("Audience not found")
        return audience

    @staticmethod
    async def create_audience(
        audience: AudienceCreate, session: SessionDep, current_user: User
    ) -> AudienceReturn:
        print(audience)
        audience_data = audience.model_dump()
        new_audience = await AudienceRepository.create_audience(audience_data, session)
        return new_audience

    @staticmethod
    async def update_audience(
        audience_id: UUID, audience: AudienceUpdate, session: SessionDep
    ) -> AudienceReturn:
        audience_data = await AudienceRepository.get_audience_by_id(
            audience_id, session
        )
        if not audience_data:
            raise NotFoundException(
                f"Audience with id {audience_id} not found")

        updated_audience = await AudienceRepository.update_audience(
            audience_id, audience, session
        )
        return updated_audience

    @staticmethod
    async def generate_initial_audiences(
        request: AudienceAiGenerate,
        session: SessionDep,
    ) -> AudienceGenerateResponse | None:
        brand = await BrandRepository.get_brand_by_id(request.brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {request.brand_id} not found")

        response = await OpenAiService.chat(
            system="""
                    You are an audience strategist inspired by Susan Fournier, B. Joseph Pine II, and Alessandro Michel. 
                    You specialize in decoding cultural and behavioral signals to create sharp, persona-driven audience segments. 
                    You view consumers as layered individuals shaped by emotion, environment, and identity. You balance human truth with market relevance.
           
                    You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and and marker analysis.
                    """,
            assistant="",
            user=f"""
                    Considering 
                    Brand name: {brand.name}'s,
                    Brand about: {brand.about},
                    Brand category: {brand.category},
                    Brand key characteristics: {brand.key_characteristics} and
                    Brand positioning: {brand.positioning}.

                    Create {request.audience_number} distinct audience segments for {brand.name} for the USA. 
                    For each audience, follow this exact structure:

                    Name: [Audience name]
                    Short Description: [2 sentences summarizing the audience's key traits, max 280 characters]
                    Image Prompt: [generate a prompt to be used in text to image software to create a thumbnail for each audience. Make sure it generates photographic detailed image, and landscape oriented, 16:9]

                    **Output Instructions**:
                    - Do not include introductions, explanations, or headers.
                    - Start directly with the first audience segment.
                    - Use plain text formatting (no bold, asterisks, or quotation marks).
                    - Avoid repeating any part of the user's input.
                    - Follow the structure strictly and consistently.
                    """,
            session=session,
        )
        raw_audiences = response.split("Name:")
        audiences_count = 0

        for i in range(1, len(raw_audiences)):
            text = raw_audiences[i]
            if i < len(raw_audiences) - 1 and "Name:" in text:
                text = text[: text.find("Name:")]

            name = text.split("Short Description:")[0].strip()
            short_description = (
                text.split("Short Description:")[1].split(
                    "Image Prompt:")[0].strip()
            )
            image_prompt = text.split("Image Prompt:")[1].strip()

            audience_data = {
                "name": name,
                "description": short_description,
                "image_prompt": image_prompt,
                "brand_id": request.brand_id,
            }

            await AudienceRepository.create_audience(audience_data, session)
            audiences_count += 1

        return JSONResponse(
            content={
                "message": f"Generated {audiences_count} audiences for brand {brand.name}",
                "audiences": audiences_count,
            },
            status_code=200,
        )

    @staticmethod
    async def analyze_audience(
        audience_id: UUID,
        session: SessionDep,
    ) -> AudienceReturn:
        audience = await AudienceRepository.get_audience_by_id(audience_id, session)
        if not audience:
            raise NotFoundException(
                f"Audience with id {audience_id} not found")
        brand = await BrandRepository.get_brand_by_id(audience.brand_id, session)
        if not brand:
            raise NotFoundException(
                f"Brand with id {audience.brand_id} not found")

        if all(
            [
                audience.psycho_graphic,
                audience.attitudinal,
                audience.self_concept,
                audience.lifestyle,
                audience.media_habits,
                audience.general_keywords,
                audience.brand_keywords,
            ]
        ):
            raise AudienceAlreadyAnalyzedException(
                f"Audience with id {audience_id} already analyzed"
            )

        response = await OpenAiService.chat(
            system="""
                    You are a cultural anthropologist and audience profiler, inspired by Sherry Turkle, Jan Chipchase, and Emmanuel Probst. 
                    You break down people’s lives, motivations, and self-concepts into structured yet emotionally intelligent descriptions. 
                    You connect identity, behavior, and cultural cues to help brands understand not just who people are — but why they act.
           
                    **Formatting Instructions**:
                    - Always include "Demographics:" as a header before the demographic details.
                    - Follow the exact structure provided in the user's input.
                    - Do not include any introductions, explanations, or additional headers beyond what is specified.
                    - Ensure consistency across all sections.
                    - Use plain text formatting (no bold, asterisks, or quotation marks).
                    - Avoid repeating any part of the user's input.
                    """,
            assistant="",
            user=f"""
                Considering 
                - Audience Name: {audience.name}
                - Short Description: {audience.description}

                Based on the audience information provided, generate a detailed analysis for the specified audience segment, following this exact structure:

                Demographics:
                - Gender: [ Gender of the audience ]
                - Age Bracket: [18-24, 25-34, 35-44, 45-54, 55-64, 65+]
                - HHI: [<75k, 75k-100k, 100k-150k, 150k-250k, >250k]
                - Race: [e.g., White, Black, Hispanic, Asian, etc.]
                - Education: [e.g., College Graduate, High School, etc.]
                - Location: [e.g., Urban areas like NYC, LA, etc.]

                Key Tags: [Provide 3 key tags that represent the audience]
                Psychographics: [e.g., Value experiences over possessions, prioritize sustainability, etc.]
                Attitudinal: [e.g., Open to innovation, driven by purpose, etc.]
                Self-Concept: [e.g., Perceive themselves as trendsetters and eco-conscious individuals, etc.]
                Lifestyle: [e.g., Prefer outdoor activities, enjoy premium and sustainable products, etc.]
                Media Habits: [e.g., High engagement with TikTok and Instagram, prefer visual content, etc.]
                General Audience Keywords: [Provide 10 keywords that represent the audience]
                Brand Audience Keywords: [Provide 10 keywords that represent the audience with {brand.name}]

                **Output Instructions**:
                - Do not include introductions, explanations, or headers.
                - Start directly with the first demographic detail.
                - Use plain text formatting (no bold, asterisks, or quotation marks).
                - Avoid repeating any part of the user's input.
                - Follow the structure strictly and consistently.
                """,
            session=session,
        )

        sections = {
            "demographics": response.split("Demographics:")[1]
            .split("Key Tags:")[0]
            .strip(),
            "key_tags": response.split("Key Tags:")[1]
            .split("Psychographics:")[0]
            .strip(),
            "psychographics": response.split("Psychographics:")[1]
            .split("Attitudinal:")[0]
            .strip(),
            "attitudinal": response.split("Attitudinal:")[1]
            .split("Self-Concept:")[0]
            .strip(),
            "self_concept": response.split("Self-Concept:")[1]
            .split("Lifestyle:")[0]
            .strip(),
            "lifestyle": response.split("Lifestyle:")[1]
            .split("Media Habits:")[0]
            .strip(),
            "media_habits": response.split("Media Habits:")[1]
            .split("General Audience Keywords:")[0]
            .strip(),
            "general_keywords": response.split("General Audience Keywords:")[1]
            .split("Brand Audience Keywords:")[0]
            .strip(),
            "brand_keywords": response.split("Brand Audience Keywords:")[1].strip(),
        }

        demographics_lines = sections["demographics"].split("\n")
        demographics = {}
        for line in demographics_lines:
            key_value = line.split(":")
            if len(key_value) == 2:
                key = key_value[0].lstrip("- ").strip().lower()
                value = key_value[1].strip()
                demographics[key] = value

        audience_data = {
            "key_tags": sections["key_tags"],
            "psycho_graphic": sections["psychographics"],
            "attitudinal": sections["attitudinal"],
            "self_concept": sections["self_concept"],
            "lifestyle": sections["lifestyle"],
            "media_habits": sections["media_habits"],
            "general_keywords": sections["general_keywords"],
            "brand_keywords": sections["brand_keywords"],
        }

        demographic_data = {
            "gender": demographics["gender"],
            "age_bracket": demographics["age bracket"],
            "hhi": demographics["hhi"],
            "race": demographics["race"],
            "education": demographics["education"],
            "location": demographics["location"],
            "audience_id": audience.id,
        }
        await DemographicRepository.create_demographic(demographic_data, session)
        await AudienceRepository.update_analyze_audience(audience_id, audience_data, session)

        return JSONResponse(
            content={
                "message": f"Audience {audience.name} analyzed",
            },
            status_code=200,
        )

    @staticmethod
    async def generate_audience_image(
        brand_id: UUID,
        session: SessionDep,
        audience_id: UUID = None,
    ) -> JSONResponse:
        scheduled = 0
        audiences = await AudienceRepository.get_all_audiences_by_brand_id(
            brand_id, session
        )

        if not audiences:
            raise NotFoundException(
                f"No audiences found for brand with id {brand_id}")

        if audience_id:
            audiences = [
                audience for audience in audiences if audience.id == audience_id
            ]

            if not audiences:
                raise NotFoundException(
                    f"Audience with id {audience_id} not found for brand with id {brand_id}"
                )

        for audience in audiences:
            audience_id = audience.id
            has_img = bool(audience.image_url)
            if not has_img:
                file_name = f"B{brand_id}A{audience_id}img.jpg"
                image_generation.delay(
                    audience.image_prompt, file_name, "audience", str(
                        audience_id)
                )
                scheduled += 1
                print(
                    f"   • Agendada task para audience {audience.id}: {file_name} - (total agendadas: {scheduled})"
                )

        return JSONResponse(
            content={
                "message": f"Scheduled {scheduled} image generation tasks for brand {brand_id}",
                "scheduled": scheduled,
            },
            status_code=200,
        )
