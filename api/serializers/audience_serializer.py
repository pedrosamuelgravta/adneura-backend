from rest_framework import serializers
from api.models import Audience
from api.serializers.trigger_serializer import TriggerSerializer
from api.serializers.demographics_serializer import DemographicsSerializer


class AudienceSerializer(serializers.ModelSerializer):
    triggers = TriggerSerializer(many=True, read_only=True)
    demographics = DemographicsSerializer(read_only=True)

    class Meta:
        model = Audience
        fields = "__all__"


class AudiencesFilteredSerializer(serializers.ModelSerializer):
    triggers = TriggerSerializer(many=True, read_only=True)
    demographics = DemographicsSerializer(read_only=True)

    class Meta:
        model = Audience
        fields = [
            "triggers",
            "demographics",
            "name",
            "description",
            "key_tags",
            "psycho_graphic",
            "attitudinal",
            "self_concept",
            "lifestyle",
            "media_habits",
            "general_keywords",
            "brand_keywords",
            "id",
        ]
