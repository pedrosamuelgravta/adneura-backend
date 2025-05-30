from pydantic import EmailStr
from email_validator import validate_email
from uuid import UUID
from fastapi.responses import JSONResponse

from api.services.OpenAi import OpenAiService
from api.repositories import BrandRepository
from api.models import Brand, User
from api.schemas import BrandCreate, BrandReturn, BrandUpdate
from core.exceptions import *
from core.db import SessionDep


class BrandService:

    system = """Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies.
                You have extensive experience in analyzing brands, crafting positioning strategies, and evaluating the effectiveness of ad
                campaigns with a sharp focus on consumer insights and strategic creativity."""

    @staticmethod
    async def get_all_brands(session: SessionDep) -> list[BrandReturn]:
        return await BrandRepository.get_all_brands(session)

    @staticmethod
    async def get_all_brands_by_user(user_id: UUID, session: SessionDep) -> list[BrandReturn]:
        return await BrandRepository.get_all_brands_by_user(user_id, session)

    @staticmethod
    async def get_brand_by_id(brand_id: UUID, session: SessionDep) -> BrandReturn:
        brand = await BrandRepository.get_brand_by_id(brand_id, session)
        if not brand:
            raise NotFoundException("Brand not found")
        return brand

    @staticmethod
    async def create_brand(brand: BrandCreate, session: SessionDep, current_user: User) -> BrandReturn:
        existing_brand = await BrandRepository.get_brand_by_name(brand.name, session, current_user.id)
        if existing_brand:
            raise ConflictException("Brand already exists")

        prompts = {
            "about": f"Write {brand.name}'s history, mission, and core values in one or two concise paragraphs. Do not include any analysis or explanation.",
            "key_characteristics": f"List 3 to 4 bullet points highlighting {brand.name}'s defining qualities. Use only the bullet points with no explanation or introduction.",
            "category": f"Provide the primary industry of {brand.name} in one or two words, e.g., 'luxury fashion', 'consumer electronics'. Do not explain.",
            "positioning": f"In one or two sentences, describe how {brand.name} is positioned in the market. Do not add any introduction or explanation.",
            "traditional_target_audience": f"List 3 to 4 bullet points describing {brand.name}'s key demographics and psychographics. Do not include any explanation.",
            "key_competitors": f"List up to 3 major competitors for {brand.name}, each with a brief description of what differentiates them. Do not include any introduction or explanation.",
        }
        brand_data = brand.model_dump()
        brand_data["user_id"] = current_user.id
        for key, prompt in prompts.items():
            response = await OpenAiService.chat(
                system=BrandService.system,
                assistant=f"""You are tasked with generating content for {brand.name}.
                    Refer to the brand's official website at {brand.website_url}
                    for desambiguation and accuracy, but, search for information in an broad array of sources.
                    If any section lacks data, mark it as "INSIGHTS NEEDED" for the client to complete.""",
                user=prompt,
                session=session,
            )
            brand_data[key] = response

        brand = await BrandRepository.create_brand(brand_data, session)
        if not brand:
            raise InternalServerError("Failed to create brand")

        return brand

    @staticmethod
    async def delete_brand(brand_id: UUID, session: SessionDep) -> BrandReturn:
        brand = await BrandRepository.get_brand_by_id(brand_id, session)
        if not brand:
            raise NotFoundException("Brand not found")

        deleted_brand = await BrandRepository.delete_brand(brand_id, session)
        if not deleted_brand:
            raise InternalServerError("Failed to delete brand")

        return deleted_brand

    @staticmethod
    async def update_brand(brand_id: UUID, brand: BrandUpdate, session: SessionDep) -> BrandReturn | JSONResponse:
        existing_brand = await BrandRepository.get_brand_by_id(brand_id, session)
        if not existing_brand:
            raise NotFoundException("Brand not found")

        update_data = brand.model_dump(exclude_unset=True)

        if brand.prompt:
            response = await BrandService.__update_step_with_prompt__(update_data, brand, session)
            return JSONResponse(response, status_code=202)

        if brand.rerun_step:
            response = await BrandService.__update_steps__(existing_brand, session)
            return JSONResponse(response, status_code=200)

        for key, value in update_data.items():
            setattr(brand, key, value)

        return await BrandRepository.update_brand(brand_id, update_data, session)

    @staticmethod
    async def __update_step_with_prompt__(update_data: str, brand: BrandUpdate, session: SessionDep) -> dict:
        update_data.pop("prompt", None)
        field = next(iter(update_data))
        response = await OpenAiService.chat(
            system=BrandService.system,
            assistant=f"""You are tasked with generating content for {brand.name}.
                        Consider {update_data} to complete your task. The {update_data}
                        will work as a guideline and disambiguation factor.
                        """,
            user=brand.prompt,
            session=session,
        )
        if not response:
            raise InternalServerError("Failed to update brand with prompt")

        return {
            "message": "Brand content updated with prompt. Save it if it looks good.",
            "data": {
                "content": response,
                "step": field
            }
        }

    @staticmethod
    async def __update_steps__(update_data: str, brand: Brand, session: SessionDep) -> dict:
        update_data.pop("rerun_step", None)
        field = next(iter(update_data))

        fields_to_update = []

        if field == "about":
            fields_to_update = [
                "key_characteristics",
                "category",
                "positioning",
                "traditional_target_audience",
                "key_competitors",
            ]
        elif field == "positioning":
            fields_to_update = [
                "traditional_target_audience", "key_competitors"]
        elif field == "traditional_target_audience":
            fields_to_update = ["key_competitors"]

        if field == "positioning":
            guideline_field = "positioning"
            guideline_text = brand.positioning
        elif field == "tradicional target audience":
            guideline_field = "tradicional target audience"
            guideline_text = brand.traditional_target_audience
        else:
            guideline_field = "about"
            guideline_text = brand.about

        prompts = {
            "about": f"Write {brand.name}'s history, mission, and core values in one or two concise paragraphs. Do not include any analysis or explanation.",
            "key_characteristics": f"List 3 to 4 bullet points highlighting {brand.name}'s defining qualities. Use only the bullet points with no explanation or introduction.",
            "category": f"Provide the primary industry of {brand.name} in one or two words, e.g., 'luxury fashion', 'consumer electronics'. Do not explain.",
            "positioning": f"In one or two sentences, describe how {brand.name} is positioned in the market. Do not add any introduction or explanation.",
            "traditional_target_audience": f"List 3 to 4 bullet points describing {brand.name}'s key demographics and psychographics. Do not include any explanation.",
            "key_competitors": f"List up to 3 major competitors for {brand.name}, each with a brief description of what differentiates them. Do not include any introduction or explanation.",
        }

        for field in fields_to_update:
            prompt = prompts[field]
            response = await OpenAiService.chat(
                system=BrandService.system,
                assistant=f"""
                            You are tasked with generating content for {brand.name}.
                            Considering the updated {guideline_field} of the brand: '{guideline_text}', 
                            please use this as a guideline and disambiguation factor to complete your task.
                            """,
                user=prompt,
                session=session,
            )
            if not response:
                raise InternalServerError("Failed to update brand with prompt")

            setattr(brand, field, response)

        print(brand)
        return {
            "message": "Brand content updated with prompt. Save it if it looks good.",
            "data": {
                "content": response,
                "step": field
            }
        }
