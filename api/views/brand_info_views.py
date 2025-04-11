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
                            Imagine you are a seasoned strategic planner, 
                            inspired by industry legends like Jon Steel, Rosie Yakob, 
                            and Russell Davies. 
                            You have extensive experience in analyzing brands, crafting positioning strategies, 
                            and evaluating the effectiveness of ad campaigns with a sharp focus on consumer insights and strategic creativity.
                            """,
                        },
                        {
                            "role": "assistant",
                            "content": f"""
                            You are tasked with generating content for the brand {brand_name}. Refer to the brand's official website at {brand.brand_url} for accurate and up-to-date information. Ensure that the content aligns with the brand's identity and values as presented on their website.
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
        id = request.data.get("id")  # brand_info id
        step = request.data.get("step")  # field name
        prompt = request.data.get("prompt")  # prompt
        base_value = request.data.get("base_value")  # original text
        content = request.data.get("content")  # edited text
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
            print(step, prompt, base_value, brand_name)
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """
                        Imagine you are a creative strategist, specializing in crafting and refining brand texts, inspired by renowned professionals such as Jon Steel, Rosie Yakob, and Russell Davies. Your role is to follow the user's instructions precisely, applying a direct, analytical, and creative approach.

                        When completing a task:
                        - Focus solely on the specific part of the text mentioned by the user.
                        - Do not include comments, explanations, or preambles. Return only the edited text.
                        - If the instructions are ambiguous or incomplete, inform the user clearly.

                        Additional context:
                        - The current text refers to the brand {brand_name}.
                        - The step to be edited is {step}.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""
                        Original text: {base_value}

                        Instructions: {prompt}

                        Rules:
                        - Respect the structure and context of the original text.
                        - Strictly follow the instructions, such as "rewrite the second paragraph" or "add an example at the end of the text."
                        - Return only the updated text, without introductions or additional explanations.
                        """,
                    },
                ],
                max_tokens=2000,
                temperature=0.8,
                top_p=1,
            )

            content = response.choices[0].message.content
            # new_entry = {step: content, "prompt": prompt}

            return Response(
                {
                    "message": "Data processed successfully.",
                    "data": {
                        "id": id,
                        "step": step,
                        "prompt": prompt,
                        "edited_content": content,
                        # "new_entry": new_entry
                    },
                },
                status=status.HTTP_200_OK,
            )

        except BrandInfo.DoesNotExist:
            return Response(
                {"error": "Brand info not found."}, status=status.HTTP_404_NOT_FOUND
            )
