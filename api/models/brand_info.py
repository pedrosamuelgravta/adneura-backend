from django.db import models
from django.utils import timezone

class BrandInfo(models.Model):
    about = models.TextField(null=True, blank=True)
    key_characteristics = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    positioning = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    key_competitors = models.TextField(null=True, blank=True)
    first_access = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Brand Info for {self.brand.name if hasattr(self, 'brand') else 'Unknown Brand'}" 