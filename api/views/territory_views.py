from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from api.models import Audience, BrandInfo, Trigger
from api.serializers import (
    AudiencesFilteredSerializer,
    DemographicsSerializer,
)

from django.conf import settings
from openai import OpenAI


class TerritoriesView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def post(self, request):
        brand_id = request.data.get("brand_id")

        try:

            brand_info = BrandInfo.objects.get(id=brand_id)
            # brand_info_serializer = BrandInfoSerializer(brand_info).data

            audiences = Audience.objects.filter(brand_id=brand_id)
            audiences_serializer = AudiencesFilteredSerializer(
                audiences, many=True
            ).data
            audiences_data = []

            all_triggers_set = set()

            for audience in audiences:
                audience_info = {
                    "name": audience.name,
                    "description": audience.description,
                    "demographics": DemographicsSerializer(audience.demographics).data,
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
                        for trigger in audience.triggers.all()  # Certifique-se que triggers é um relacionamento ManyToMany ou ForeignKey
                    ],
                }
                for trigger in audience.triggers.all():
                    all_triggers_set.add(trigger.name)

                audiences_data.append(audience_info)

            # Convertendo a estrutura para string formatada
            formatted_audiences = "\n\n".join(
                f"### Audience: {audience['name']}\n"
                f"Description: {audience['description']}\n"
                f"Demographics: {audience['demographics']}\n"
                f"Key Tags: {audience['key_tags']}\n"
                f"Psycho-graphic: {audience['psycho_graphic']}\n"
                f"Attitudinal: {audience['attitudinal']}\n"
                f"Self Concept: {audience['self_concept']}\n"
                f"Lifestyle: {audience['lifestyle']}\n"
                f"Media Habits: {audience['media_habits']}\n"
                f"General Keywords: {audience['general_keywords']}\n"
                f"Brand Keywords: {audience['brand_keywords']}\n"
                f"Triggers:\n"
                + "\n".join(
                    f"- {trigger['name']}: {trigger['description']}"
                    for trigger in audience["triggers"]
                )
                for audience in audiences_data
            )

            # Agora use 'formatted_audiences' no assistant

            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": f"""
            You are a seasoned strategic planner, inspired by industry
            legends like Jon Steel, Rosie Yakob, and Russell Davies.
            You have extensive experience in analyzing brands and crafting
            positioning strategies with a sharp focus on consumer insights
            and marker analysis.
            """,
                    },
                    {
                        "role": "assistant",
                        "content": f"""
            Considering the following Audiences details:
                Target Audiences: {brand_info.target_audience}  
                {formatted_audiences}
            """,
                    },
                    {
                        "role": "user",
                        "content": f"""
            Group the triggers into 6-8 distinctive groups. Group triggers that are alike or have the same motivations.
			Each and every trigger must be designed to a group.
		    Name the groupd with a one or two main words' title different from the name of the triggers. 
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

            ```plaintext
            Brand Territory: [Group Name]  
            Relevance: [Short description of the group's strategic role]  
            Opportunities: [How the brand can communicate within this group]  
            Triggers:  
            - [Trigger Name] ([Audience Name])
            """,
                    },
                ],
                max_tokens=4000,
                temperature=1,
                top_p=1,
            )

            content = response.choices[0].message.content

            territories = content.split("Brand Territory:")
            territories = territories[1:]

            sections = []
            applied_triggers_set = set()
            for i, territory in enumerate(territories):

                section = {
                    "name": territory.split("Relevance:")[0].strip(),
                    "relevance": territory.split("Relevance:")[1]
                    .split("Opportunities:")[0]
                    .strip(),
                    "opportunities": territory.split("Opportunities:")[1]
                    .split("Triggers:")[0]
                    .strip(),
                    "triggers": [
                        trigger.split("(")[0].strip("- `").strip()
                        for trigger in territory.split("Triggers:")[1]
                        .strip()
                        .split("\n")
                        if trigger.split("(")[0].strip("- `").strip()
                        != ""  # Garante que strings vazias sejam ignoradas
                    ],
                }
                if section["triggers"] != "":
                    applied_triggers_set.update(section["triggers"])
                    sections.append(section)

            missing_triggers = list(all_triggers_set - applied_triggers_set)

            matched_triggers = []
            # print(sections)
            # print(audiences_serializer)
            for audience in audiences_serializer:
                for trigger in audience["triggers"]:
                    # print(trigger)

                    trigger_name = trigger["name"]
                    audience_id = audience["id"]

                    for section in sections:
                        if trigger_name in section["triggers"]:

                            matched_triggers.append(
                                {
                                    "audience_id": audience_id,
                                    "trigger_id": trigger["id"],
                                    "trigger_name": trigger_name,
                                    "territory": section["name"],
                                }
                            )

                            trigger_obj = Trigger.objects.get(id=trigger["id"])
                            trigger_obj.territory = section["name"]
                            trigger_obj.save()

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        matched_triggers_sorted = sorted(
            matched_triggers, key=lambda x: x["audience_id"]
        )
        return Response(
            {
                "content": sections,
                "summary": {
                    "total_triggers": len(all_triggers_set),
                    "applied_triggers": len(applied_triggers_set),
                    "missing_triggers": missing_triggers,
                },
                "matched_triggers": matched_triggers_sorted,
            },
            status=status.HTTP_200_OK,
        )
