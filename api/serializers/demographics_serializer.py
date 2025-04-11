from rest_framework import serializers
from api.models import Demographics


class DemographicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demographics
        fields = [
            "id",
            "gender",
            "age_bracket",
            "hhi",
            "race",
            "education",
            "audience",
            "created_at",
            "updated_at",
        ]
