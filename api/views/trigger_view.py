from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.models import Audience, Brand, StrategicGoals, Trigger
from api.serializers import StrategicGoalsSerializer, TriggerSerializer

from django.conf import settings
from openai import OpenAI
import time


class TriggerView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def get(self, request):
        triggers = Trigger.objects.all()
        serializer = TriggerSerializer(triggers, many=True)
        return Response(serializer.data)

    def post(self, request):
        brand_id = request.data.get("brand_id")
        audience_id = request.data.get("audience_id")
        # Flag para identificar se é um rerun (atualização dos triggers existentes)
        rerun_flag = request.data.get("rerun", False)

        if brand_id is None:
            return Response(
                {"error": "Brand ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if audience_id is None:
            return Response(
                {"error": "Audience ID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            audience = Audience.objects.get(id=audience_id)
            brand = Brand.objects.get(id=brand_id)
            strategic_goals = StrategicGoals.objects.filter(brand_id=brand_id)
            strategic_goals_serializer = StrategicGoalsSerializer(
                strategic_goals, many=True
            )

            triggers_qs = Trigger.objects.filter(audience_id=audience_id)
            triggers_count = triggers_qs.count()

            # Se não for rerun e já houver 3 ou mais triggers, retorna erro
            if triggers_count >= 3 and not rerun_flag:
                return Response(
                    {"error": "Maximum number of triggers for this audience reached."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            start_time = time.time()
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": """
                            Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies. You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and market analysis.

                            Your task is to create a text according to the instructions provided by the user. Always return only the edited content, without any introductions, preambles, or explanations. The output should strictly contain the updated text as per the instructions, and nothing else.
                            """,
                    },
                    {
                        "role": "assistant",
                        "content": f"""
                            Considering {brand.name}, 
                            {brand.brand_info.about}, 
                            {brand.brand_info.category}, 
                            {brand.brand_info.key_characteristics}, 
                            {brand.brand_info.positioning}, 
                            the audience {audience.name} described as {audience.description}. 
                            Focus on the psychographics, attitudinal, self-concept and lifestyle.
                        """,
                    },
                    {
                        "role": "user",
                        "content": f"""
                            Create 3 very distinct and relevant message triggers for each {strategic_goals_serializer.data}. Pinpoint specific life events, emotions, or circumstances that move this audience towards the brand goals. These could range from seasonal needs to personal milestones.  
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
                    },
                ],
                max_tokens=2000,
                temperature=1,
                top_p=1,
            )
            end_time = time.time()
            print(f"A requisição da OPENAI levou {end_time - start_time:.2f} segundos.")

            content = response.choices[0].message.content
            content_list = content.split("Title:")
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

            if rerun_flag and triggers_count >= 3:
                # Se for rerun, atualize os triggers existentes
                existing_triggers = list(triggers_qs.order_by("id"))
                for i, sections in enumerate(parsed_triggers):
                    if i < len(existing_triggers):
                        trigger_obj = existing_triggers[i]
                        trigger_obj.name = sections["title"]
                        trigger_obj.description = sections["description"]
                        trigger_obj.image_prompt = sections["image_prompt"]
                        trigger_obj.save()
                    else:
                        # Caso venha um novo trigger e o total seja menor que 3
                        Trigger.objects.create(
                            name=sections["title"],
                            description=sections["description"],
                            audience=audience,
                            image_prompt=sections["image_prompt"],
                        )
            else:
                # Caso não seja rerun e ainda não atinja o limite, crie os triggers
                for sections in parsed_triggers:
                    Trigger.objects.create(
                        name=sections["title"],
                        description=sections["description"],
                        audience=audience,
                        image_prompt=sections["image_prompt"],
                    )

        except Audience.DoesNotExist:
            return Response(
                {"error": "Audience not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            {"content": "Triggered successfully."},
            status=status.HTTP_200_OK,
        )


class TriggerUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            trigger = Trigger.objects.get(id=pk)
        except Audience.DoesNotExist:
            return Response(
                {"error": "Trigger not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = TriggerSerializer(trigger, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "content": "Trigger updated successfully.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
