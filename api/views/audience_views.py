from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.models import Audience, Demographics, Brand, BrandInfo, Trigger
from api.serializers import AudienceMiniSerializer, AudienceSerializer
from openai import OpenAI
from django.conf import settings
import requests
import time
import os

class AudienceListView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def get(self, request):
      brand_id = request.query_params.get('brand_id')
      audience_id = request.query_params.get('audience_id')
      if brand_id is not None:
        audiences = Audience.objects.filter(brand_id=brand_id).order_by('id')
        serializer = AudienceMiniSerializer(audiences, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
      else:
        audience = Audience.objects.get(id=audience_id)
        serializer = AudienceSerializer(audience)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
      brand_id = request.data.get('brand_id')
      
      if brand_id is None:
        return Response({"error": "Brand ID is required."}, status=status.HTTP_400_BAD_REQUEST)
      
      try:
        brand = Brand.objects.get(id=brand_id)
        brand_info = BrandInfo.objects.get(id=brand.brand_info.id)
        audience_count = Audience.objects.filter(brand_id=brand_id).count()
        # remaining_audiences = 9 - audience_count

        # if audience_count >= 9:
        #   return Response({"error": "Maximum number of audiences for this brand reached."}, status=status.HTTP_400_BAD_REQUEST)
        
      except Brand.DoesNotExist:
        return Response({"error": "Brand not found."}, status=status.HTTP_404_NOT_FOUND)
      
      print('entrou')
      start_time = time.time()
      response = self.client.chat.completions.create(
        model="gpt-4o",
        messages=[
          {"role": "system", "content": """
            You are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies. 
           
            You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and and marker analysis.
          """},
          {"role": "assistant", "content": f"Considering {brand.name}'s {brand_info.about}, {brand_info.category}, {brand_info.key_characteristics}, and {brand_info.positioning}."},
          {"role": "user", "content": f"""
            Create 9 distinct audience segments for {brand.name} for the USA. For each audience, follow this exact structure:  

            Name: [Audience name]  
            Short Description: [2 sentences summarizing the audience's key traits, max 280 characters]  
            Image Prompt: [generate a prompt to be used in text to image software to create a thumbnail for each audience. Make sure it generates a low detailed image, Iconography and landscape oriented]

           **Output Instructions**:  
            - Do not include introductions, explanations, or headers.  
            - Start directly with the first audience segment.  
            - Use plain text formatting (no bold, asterisks, or quotation marks).  
            - Avoid repeating any part of the user's input.  
            - Follow the structure strictly and consistently.
          """}
        ],
        max_tokens=2000,
        temperature=1,
        top_p=1,
      )

      end_time = time.time()

      # Calcular o tempo gasto
      duration = end_time - start_time
      print(f"A requisição levou {duration:.2f} segundos.")

      content = response.choices[0].message.content
      content_list = content.split("Name:")
      audiences = []
      for i in range(1, len(content_list)):
        audience = content_list[i]
        if i < len(content_list) - 1:
          audience = audience[:audience.find("Name:")]
        audiences.append(audience.strip())

      for i, audience in enumerate(audiences):
        audience = audience.strip()
        sections = {
          "name": audience.split("Short Description:")[0].strip(),
          "short_description": audience.split("Short Description:")[1].split("Image Prompt:")[0].strip(),
          "image_prompt": audience.split("Image Prompt:")[1].strip()
        }

        audience_obj = {
          "name": sections["name"],
          "description": sections["short_description"],
          "brand_id": brand_id,
          "image_prompt": sections["image_prompt"],
        }

        audience = Audience.objects.create(**audience_obj)
        
      return Response({"content": 'Audiences created successfully.'}, status=status.HTTP_200_OK)

    def patch(self, request):
      audience_id = request.data.get('audience_id')

      if audience_id is None:
        return Response({"error": "Audience ID is required."}, status=status.HTTP_400_BAD_REQUEST)
      
      start_time = time.time()
      try:
        audience = Audience.objects.get(id=audience_id)
        brand = Brand.objects.get(id=audience.brand_id)

      except Audience.DoesNotExist:
        return Response({"error": "Audience not found."}, status=status.HTTP_404_NOT_FOUND)
      
      if all([audience.psycho_graphic, audience.attitudinal, audience.self_concept, audience.lifestyle, audience.media_habits, audience.general_keywords, audience.brand_keywords]):
        return Response({"content": "Audience already analyzed."}, status=status.HTTP_200_OK)
      
      start_time = time.time()
      response = self.client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
          {"role": "system", "content": """
            You are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies. 
           
            You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and and marker analysis.
           
            **Formatting Instructions**:
            - Always include "Demographics:" as a header before the demographic details.
            - Follow the exact structure provided in the user's input.
            - Do not include any introductions, explanations, or additional headers beyond what is specified.
            - Ensure consistency across all sections.
            - Use plain text formatting (no bold, asterisks, or quotation marks).
            - Avoid repeating any part of the user's input.
          """},
          {"role": "assistant", "content": f"""
            Audience Name: {audience.name}
            Short Description: {audience.description}
          """},
          {"role": "user", "content": f"""
            Based on the audience information provided, generate a detailed analysis for the specified audience segment, following this exact structure:

            Demographics:
            - Gender: [ Gender of the audience ]
            - Age Bracket: [18-24, 25-34, 35-44, 45-54, 55-64, 65+]
            - HHI: [<75k, 75k-100k, 100k-150k, 150k-250k, >250k]
            - Race: [e.g., White, Black, Hispanic, Asian, etc.]
            - Education: [e.g., College Graduate, High School, etc.]
            - Location: [e.g., Urban areas like NYC, LA, etc.]

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
          """}
          
        ],
        max_tokens=2000,
        temperature=1,
        top_p=1,
      )

      end_time = time.time()
      print(f"A requisição da OPENAI levou {end_time - start_time:.2f} segundos.")

      content = response.choices[0].message.content
      sections = {
        "demographics": content.split("Demographics:")[1].split("Psychographics:")[0].strip(),
        "psychographics": content.split("Psychographics:")[1].split("Attitudinal:")[0].strip(),
        "attitudinal": content.split("Attitudinal:")[1].split("Self-Concept:")[0].strip(),
        "self_concept": content.split("Self-Concept:")[1].split("Lifestyle:")[0].strip(),
        "lifestyle": content.split("Lifestyle:")[1].split("Media Habits:")[0].strip(),
        "media_habits": content.split("Media Habits:")[1].split("General Audience Keywords:")[0].strip(),
        "general_keywords": content.split("General Audience Keywords:")[1].split("Brand Audience Keywords:")[0].strip(),
        "brand_keywords": content.split("Brand Audience Keywords:")[1].strip()
      }
      
      demographics_lines = sections["demographics"].split("\n")
      demographics = {}
      for line in demographics_lines:
        key_value = line.split(":")
        if len(key_value) == 2:
          key = key_value[0].lstrip('- ').strip().lower()
          value = key_value[1].strip()
          demographics[key] = value

      audience_obj = {
        "psycho_graphic": sections["psychographics"],
        "attitudinal": sections["attitudinal"],
        "self_concept": sections["self_concept"],
        "lifestyle": sections["lifestyle"],
        "media_habits": sections["media_habits"],
        "general_keywords": sections["general_keywords"],
        "brand_keywords": sections["brand_keywords"]
      }
      
      demographics_obj = {
        "gender": demographics["gender"],
        "age_bracket": demographics["age bracket"],
        "hhi": demographics["hhi"],
        "race": demographics["race"],
        "education": demographics["education"],
        "location": demographics["location"],
        "audience": audience
      }     


      Audience.objects.filter(id=audience_id).update(**audience_obj)

      Demographics.objects.create(**demographics_obj)

      return Response({"content": 'Audience updated successfully.'}, status=status.HTTP_200_OK)

class GenerateImageAudienceView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def post(self, request):
        text = request.data.get('text')
        brand_id = request.data.get('brand_id')
        audience_id = request.data.get('audience_id')

        if not text or not brand_id or audience_id is None:
            return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)
        print({
            "text": text,
            "brand_id": brand_id,
            "audience_id": audience_id
        })
        try:
            import time
            retries = 5
            for i in range(retries):
                try:
                    start_time = time.time()
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=text,
                        size="1024x1024",
                        n=1,
                    )
                    end_time = time.time()

                    duration = end_time - start_time
                    print(f"A geração da imagem levou {duration:.2f} segundos.")

                    image_url = response.data[0].url
                    break
                except Exception as e:
                    if i < retries - 1 and 'rate_limit_exceeded' in str(e):
                        wait_time = (2 ** i) * 10  # Exponential backoff
                        print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise e

            output_folder = "./images/"
            output_file = f"B{brand_id}A{audience_id}img.jpg"
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, output_file)

            with open(file_path, "wb") as file:
                file.write(requests.get(image_url).content)
            print('Image saved on DB')

            Audience.objects.filter(id=audience_id).update(audience_img=output_file)

            return Response({"image_url": file_path}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error generating image: {e}")
            return Response({"error": "Image generation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class TriggerView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def get(self, request):
      return Response({"content": 'Triggered successfully.'}, status=status.HTTP_200_OK)
    
    def post(self, request):
      brand_id = request.data.get('brand_id')
      audience_id = request.data.get('audience_id')

      if brand_id is None:
        return Response({"error": "Brand ID is required."}, status=status.HTTP_400_BAD_REQUEST)

      if audience_id is None:
        return Response({"error": "Audience ID is required."}, status=status.HTTP_400_BAD_REQUEST)

      try:
        audience = Audience.objects.get(id=audience_id)
        brand = Brand.objects.get(id=brand_id)
        triggers_count = Trigger.objects.filter(audience_id=audience_id).count()
        triggers_remaining = 3 - triggers_count

        if triggers_count >= 3:
          return Response({"error": "Maximum number of triggers for this audience reached."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        start_time = time.time()
        response = self.client.chat.completions.create(
          model="gpt-4o-mini",
          messages=[
            {"role": "system", "content": """
              Imagine you are a seasoned strategic planner, inspired by industry legends like Jon Steel, Rosie Yakob, and Russell Davies. You have extensive experience in analyzing brands and crafting positioning strategies with a sharp focus on consumer insights and and marker analysis.

              Your task is to create a text according to the instructions provided by the user. Always return only the edited content, without any introductions, preambles, or explanations. The output should strictly contain the updated text as per the instructions, and nothing else. I suggest you find references in various and reliable sources. 
            """},
            {"role": "assistant", "content": f"""
              Brand: {brand.name}
              Audience: {audience.name}
              Audience Description: {audience.description}
            """},
            {"role": "user", "content": f"""
              Considering the {brand.name}, the audience called {audience.name} and described as {audience.description}. Create {triggers_remaining} very distinct and relevant message triggers. Pinpoint specific life events, emotions, or circumstances that lead to interaction with your brand or category. These could range from seasonal needs to personal milestones. For each trigger, describe the trigger and how it will motivate the specific audience. Create an amazing title for it. Create an scene description that best describes each trigger. Also, bring the scene in prompt format to be used in a text to image GenAI. For each trigger, follow this exact structure:
             
              Title: [Trigger Title]
              Description: [1 paragraph describing the trigger]
              Image Prompt: [ generate a prompt to be used in text to image GenAI to create a scene that best describes the trigger. Make sure it represents the trigger and its target audience. Generate a detailed image and landscape oriented, 16:9]
              
              Output Instructions:  
              - Do not include introductions, explanations, or headers.  
              - Start directly with the first demographic detail.  
              - Use plain text formatting (no bold, asterisks, or quotation marks).  
              - Avoid repeating any part of the user's input.  
              - Follow the structure strictly and consistently.
            """}
            
          ],
          max_tokens=2000,
          temperature=1,
          top_p=1,
        )

        end_time = time.time()
        print(f"A requisição da OPENAI levou {end_time - start_time:.2f} segundos.")



        content = response.choices[0].message.content
        content_list = content.split("Title:")
        triggers = []
        for i in range(1, len(content_list)):
          trigger = content_list[i]
          if i < len(content_list) - 1:
            trigger = trigger[:trigger.find("Title:")]
          triggers.append(trigger.strip())
        print(triggers)
        for i, trigger in enumerate(triggers):
          trigger = trigger.strip()
          sections = {
            "title": trigger.split("Description:")[0].strip(),
            "description": trigger.split("Description:")[1].split("Image Prompt:")[0].strip(),
            "image_prompt": trigger.split("Image Prompt:")[1].strip()
          }

          trigger_obj = {
            "name": sections["title"],
            "description": sections["description"],
            "audience": audience,
            "image_prompt": sections["image_prompt"]
          }

          trigger = Trigger.objects.create(**trigger_obj)

        

      except Audience.DoesNotExist:
        return Response({"error": "Audience not found."}, status=status.HTTP_404_NOT_FOUND)

        
      return Response({"content": 'Triggered successfully.'}, status=status.HTTP_200_OK)

class GenerateImageTriggerView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def post(self, request):
        text = request.data.get('text')
        brand_id = request.data.get('brand_id')
        audience_id = request.data.get('audience_id')
        trigger_id = request.data.get('trigger_id')

        if not text or not brand_id or audience_id is None or trigger_id is None:
            return Response({"error": "Missing required parameters."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            import time
            retries = 5
            for i in range(retries):
                try:
                    start_time = time.time()
                    response = self.client.images.generate(
                        model="dall-e-3",
                        prompt=text,
                        size="1024x1024",
                        n=1,
                    )
                    end_time = time.time()

                    duration = end_time - start_time
                    print(f"A geração da imagem levou {duration:.2f} segundos.")

                    image_url = response.data[0].url
                    break
                except Exception as e:
                    if i < retries - 1 and 'rate_limit_exceeded' in str(e):
                        wait_time = (2 ** i) * 10  # Exponential backoff
                        print(f"Rate limit exceeded. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        raise e

            output_folder = "./images/"
            output_file = f"B{brand_id}A{audience_id}T{trigger_id}img.jpg"
            os.makedirs(output_folder, exist_ok=True)
            file_path = os.path.join(output_folder, output_file)

            with open(file_path, "wb") as file:
                file.write(requests.get(image_url).content)
            print('Image saved on DB')

            Trigger.objects.filter(id=trigger_id).update(trigger_img=output_file)

            return Response({"image_url": file_path}, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error generating image: {e}")
            return Response({"error": "Image generation failed."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)