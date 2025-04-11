from rest_framework import serializers
from api.models import BrandInfo

class BrandInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandInfo
        fields = ['id', 'about', 'key_characteristics', 'category', 'positioning', 'target_audience', 'key_competitors', 'first_access','updated_at']