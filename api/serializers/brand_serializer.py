from rest_framework import serializers
from api.models import Brand

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [ 'id', 'name', 'brand_url', 'user', 'brand_info', 'ad_legacy', 'created_at', 'updated_at']