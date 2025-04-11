from adrf.views import APIView  # type: ignore
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models import Trigger

from django.conf import settings

from openai import OpenAI

from api.tasks import generate_trigger_image, generate_audience_image


class GenerateImageTriggerView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def post(self, request):
        text = request.data.get("text")
        brand_id = request.data.get("brand_id")
        audience_id = request.data.get("audience_id")
        trigger_id = request.data.get("trigger_id")

        if not text or not brand_id or audience_id is None or trigger_id is None:
            return Response(
                {"error": "Missing required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            trigger = Trigger.objects.get(id=trigger_id)
        except Trigger.DoesNotExist:
            return Response(
                {"error": "Trigger not found."}, status=status.HTTP_404_NOT_FOUND
            )

        if trigger.trigger_img:
            return Response(
                {"error": "Trigger já possui uma imagem."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        triggers_da_audiencia = Trigger.objects.filter(audience_id=audience_id)
        if triggers_da_audiencia.count() >= 3:
            return Response(
                {
                    "error": "Número máximo de triggers para essa audiência já foi atingido."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        generate_trigger_image.delay(text, brand_id, audience_id, trigger_id)

        return Response(
            {"message": "Image generation started in background"},
            status=status.HTTP_200_OK,
        )


class GenerateImageAudienceView(APIView):
    permission_classes = [IsAuthenticated]
    client = OpenAI()
    client.api_key = settings.OPENAI_API_KEY

    def post(self, request):
        text = request.data.get("text")
        brand_id = request.data.get("brand_id")
        audience_id = request.data.get("audience_id")

        if not text or not brand_id or audience_id is None:
            return Response(
                {"error": "Missing required parameters."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        generate_audience_image.delay(text, brand_id, audience_id)

        return Response(
            {"message": "Image generation started in background"},
            status=status.HTTP_200_OK,
        )
