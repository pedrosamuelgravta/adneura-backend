from django.db import models
from django.utils import timezone
import uuid


class StrategicGoals(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    goal = models.TextField(null=True, blank=True)
    brand_id = models.ForeignKey(
        "Brand", on_delete=models.CASCADE, related_name="strategic_goals"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.goal
