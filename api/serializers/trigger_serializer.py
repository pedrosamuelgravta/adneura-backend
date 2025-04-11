from rest_framework import serializers
from api.models import Trigger


class TriggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trigger
        fields = [
            "id",
            "name",
            "description",
            "audience",
            "trigger_img",
            "image_prompt",
            "territory",
            "created_at",
            "updated_at",
        ]
