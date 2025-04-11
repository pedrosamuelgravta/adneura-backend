from rest_framework import serializers
from api.models import Audience
from api.serializers.trigger_serializer import TriggerSerializer
from api.serializers.demographics_serializer import DemographicsSerializer

class AudienceSerializer(serializers.ModelSerializer):
    triggers = TriggerSerializer(many=True, read_only=True)  
    demographics = DemographicsSerializer(read_only=True)  
    class Meta:
        model = Audience
        fields = ['id', 'name', 'description', 'psycho_graphic', 'attitudinal','self_concept', 'brand', 'triggers', 'demographics',
                  'lifestyle', 'media_habits', 'general_keywords', 'brand_keywords', 'image_prompt',
                   'audience_img', 'created_at', 'updated_at']

class AudienceMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audience
        fields = ['id', 'name', 'description', 'image_prompt', 'audience_img']