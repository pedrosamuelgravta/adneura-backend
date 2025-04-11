from django.db import models
from django.utils import timezone


class Trigger(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    audience = models.ForeignKey(
        "Audience", on_delete=models.CASCADE, related_name="triggers"
    )
    image_prompt = models.TextField(null=True, blank=True)
    trigger_img = models.TextField(null=True, blank=True)
    territory = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
