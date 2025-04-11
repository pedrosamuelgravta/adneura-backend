from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import BrandInfo, Brand
from api.serializers import BrandInfoSerializer, BrandSerializer
from openai import OpenAI
from django.conf import settings


class BrandInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        brand_id = request.query_params.get("id")
        if brand_id is not None:
            try:
                brand = Brand.objects.get(id=brand_id)
                brand_serializer = BrandSerializer(brand)
                brand_info = BrandInfo.objects.get(
                    id=brand_serializer.data["brand_info"]
                )
                serializer = BrandInfoSerializer(brand_info)

                if brand_info.first_access == False:
                    status = "in_progress"
                    brand_info.first_access = True
                    brand_info.save()
                else:
                    is_complete = all(
                        getattr(brand_info, field.name)
                        for field in BrandInfo._meta.fields
                    )
                    status = "complete" if is_complete else "in_progress"

                return Response({"brand_info": serializer.data, "status": status})
            except BrandInfo.DoesNotExist:
                return Response(
                    {"error": "Brand info not found."}, status=status.HTTP_404_NOT_FOUND
                )

        return Response(
            {"error": "Brand info ID is required."}, status=status.HTTP_400_BAD_REQUEST
        )

    def post(self, request):
        brand_id = request.data.get("brand_id")
        brand = Brand.objects.get(id=brand_id)
        brand_name = brand.name
        brand_info = BrandInfo.objects.get(id=brand.brand_info.id)
        is_complete = all(
            getattr(brand_info, field.name) for field in BrandInfo._meta.fields
        )

        if is_complete:
            brand_info.first_access = True
            brand_info.save()
            return Response(
                {"message": "Brand info already complete."}, status=status.HTTP_200_OK
            )

        prompts = {
            "about": f"Write {brand_name}'s history, mission, and core values in one or two concise paragraphs. Do not include any analysis or explanation.",
            "key_characteristics": f"List 3 to 4 bullet points highlighting {brand_name}'s defining qualities. Use only the bullet points with no explanation or introduction.",
            "category": f"Provide the primary industry of {brand_name} in one or two words, e.g., 'luxury fashion', 'consumer electronics'. Do not explain.",
            "positioning": f"In one or two sentences, describe how {brand_name} is positioned in the market. Do not add any introduction or explanation.",
            "target_audience": f"List 3 to 4 bullet points describing {brand_name}'s key demographics and psychographics. Do not include any explanation.",
            "key_competitors": f"List up to 3 major competitors for {brand_name}, each with a brief description of what differentiates them. Do not include any introduction or explanation.",
        }

        client = OpenAI()
        client.api_key = settings.OPENAI_API_KEY

        for field, prompt in prompts.items():
            if not getattr(brand_info, field):
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": """
                                Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies. 
                                You have extensive experience in analyzing brands, crafting positioning strategies, and evaluating the effectiveness of ad 
                                campaigns with a sharp focus on consumer insights and strategic creativity.
                            """,
                        },
                        {
                            "role": "assistant",
                            "content": f"""
                                You are tasked with generating content for {brand_name}. 
                                Refer to the brand's official website at {brand.brand_url} 
                                for desambiguation and accuracy, but, search for information in an broad array of sources.
                                If any section lacks data, mark it as "INSIGHTS NEEDED" for the client to complete.
                            """,
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )

                content = response.choices[0].message.content
                setattr(brand_info, field, content)

        brand_info.save()

        return Response(
            {
                "brand_name": brand_name,
                "status": "in_progress",
                "full_data": BrandInfoSerializer(brand_info).data,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        id = request.data.get("id")
        step = request.data.get("step")
        prompt = request.data.get("prompt")
        content = request.data.get("content")
        brand_name = request.data.get("brand_name")
        if not id or not step:
            return Response(
                {"error": "id, step, and prompt are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            brand_info = BrandInfo.objects.get(id=id)

            if content is not None:
                setattr(brand_info, step, content)
                brand_info.save()
                return Response(
                    {
                        "message": "Data updated successfully.",
                        "data": {"id": id, "step": step, "content": content},
                    },
                    status=status.HTTP_200_OK,
                )

            if not prompt:
                return Response(
                    {"error": "prompt is required for new changes."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            client = OpenAI()
            client.api_key = settings.OPENAI_API_KEY

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """
                            Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies.
                            You have extensive experience in analyzing brands, crafting positioning strategies, and evaluating the effectiveness of ad
                            campaigns with a sharp focus on consumer insights and strategic creativity.

                        """,
                    },
                    {
                        "role": "assistant",
                        "content": f"""
                            You are tasked with generating content for {brand_name}. 
                            Consider {brand_info.about} to complete your task. The {brand_info.about} 
                            will work as a guideline and disambiguation factor.
                        """,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                max_tokens=2000,
                temperature=0.8,
                top_p=1,
            )

            content = response.choices[0].message.content

            return Response(
                {
                    "message": "Data processed successfully.",
                    "data": {
                        "id": id,
                        "step": step,
                        "prompt": prompt,
                        "edited_content": content,
                    },
                },
                status=status.HTTP_200_OK,
            )

        except BrandInfo.DoesNotExist:
            return Response(
                {"error": "Brand info not found."}, status=status.HTTP_404_NOT_FOUND
            )

    def patch(self, request):
        brand_id = request.data.get("id")
        rerun = request.data.get("rerun", False)
        update_step = request.data.get("step", "about").lower()
        print({"brand_id": brand_id, "rerun": rerun, "update_step": update_step})
        if not brand_id:
            return Response(
                {"error": "Brand ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            brand = Brand.objects.get(id=brand_id)
            brand_info = BrandInfo.objects.get(id=brand.brand_info.id)
        except (Brand.DoesNotExist, BrandInfo.DoesNotExist):
            return Response(
                {"error": "Brand not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if rerun:
            fields_to_update = []
            if update_step == "about":
                fields_to_update = [
                    "key_characteristics",
                    "category",
                    "positioning",
                    "target_audience",
                    "key_competitors",
                ]
            elif update_step == "positioning":
                fields_to_update = ["target_audience", "key_competitors"]
            elif update_step == "target_audience":
                fields_to_update = ["key_competitors"]

            # Define a guideline com base no step atualizado
            if update_step == "positioning":
                guideline_field = "positioning"
                guideline_text = brand_info.positioning
            elif update_step == "target audience":
                guideline_field = "target audience"
                guideline_text = brand_info.target_audience
            else:
                guideline_field = "about"
                guideline_text = brand_info.about

            brand_name = brand.name
            prompts = {
                "about": f"Write {brand_name}'s history, mission, and core values in one or two concise paragraphs. Do not include any analysis or explanation.",
                "key_characteristics": f"List 3 to 4 bullet points highlighting {brand_name}'s defining qualities. Use only the bullet points with no explanation or introduction.",
                "category": f"Provide the primary industry of {brand_name} in one or two words, e.g., 'luxury fashion', 'consumer electronics'. Do not explain.",
                "positioning": f"In one or two sentences, describe how {brand_name} is positioned in the market. Do not add any introduction or explanation.",
                "target_audience": f"List 3 to 4 bullet points describing {brand_name}'s key demographics and psychographics. Do not include any explanation.",
                "key_competitors": f"List up to 3 major competitors for {brand_name}, each with a brief description of what differentiates them. Do not include any introduction or explanation.",
            }
            print(fields_to_update)
            prompts = {field: prompts[field] for field in fields_to_update}
            client = OpenAI()
            client.api_key = settings.OPENAI_API_KEY

            for field, prompt in prompts.items():

                # Gera novo conteúdo usando a API do OpenAI
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": f"""
                                Imagine you are a seasoned strategic planner with extensive
                                experience in analyzing brands and crafting positioning strategies.
                            """,
                        },
                        {
                            "role": "assistant",
                            "content": f"""
                                You are tasked with generating content for {brand.name}.
                                Considering the updated {guideline_field} of the brand: '{guideline_text}', 
                                please use this as a guideline and disambiguation factor to complete your task.""",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.7,
                    max_tokens=500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                # Atualiza cada campo com o novo conteúdo gerado
                setattr(brand_info, field, response.choices[0].message.content)
            brand_info.save()
            return Response(
                {
                    "message": "Brand Summary re-run successfully.",
                    "brand_info": BrandInfoSerializer(brand_info).data,
                },
                status=status.HTTP_200_OK,
            )

        # else, retorna os dados atuais
        serializer = BrandInfoSerializer(brand_info)
        return Response({"brand_info": serializer.data}, status=status.HTTP_200_OK)
