from rest_framework import serializers
from api.models import StrategicGoals


class StrategicGoalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StrategicGoals
        fields = "__all__"
