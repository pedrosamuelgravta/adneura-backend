from rest_framework import serializers
from api.models import AdvertisingLegacy

class AdvertisingLegacySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdvertisingLegacy
        fields = ['id', 'about', 'themes', 'messaging', 'style', 'created_at', 'updated_at']