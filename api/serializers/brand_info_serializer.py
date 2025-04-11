from rest_framework import serializers
from api.models import BrandInfo


class BrandInfoSerializer(serializers.ModelSerializer):
    brand_name = serializers.SerializerMethodField()

    class Meta:
        model = BrandInfo
        fields = [
            "id",
            "brand_name",
            "about",
            "key_characteristics",
            "category",
            "positioning",
            "target_audience",
            "key_competitors",
            "first_access",
            "updated_at",
        ]

    def get_brand_name(self, obj):
        return obj.brand.name
