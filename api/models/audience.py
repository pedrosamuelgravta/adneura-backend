from django.db import models
from django.utils import timezone


class Audience(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    key_tags = models.TextField(null=True, blank=True)
    psycho_graphic = models.TextField(null=True, blank=True)
    attitudinal = models.TextField(null=True, blank=True)
    self_concept = models.TextField(null=True, blank=True)
    lifestyle = models.TextField(null=True, blank=True)
    media_habits = models.TextField(null=True, blank=True)
    general_keywords = models.TextField(null=True, blank=True)
    brand_keywords = models.TextField(null=True, blank=True)
    image_prompt = models.TextField(null=True, blank=True)
    audience_img = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE, related_name="audiences"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
