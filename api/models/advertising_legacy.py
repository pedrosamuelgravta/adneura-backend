from django.db import models
from django.utils import timezone


class AdvertisingLegacy(models.Model):
    about = models.TextField(null=True, blank=True)
    themes = models.TextField(null=True, blank=True)
    messaging = models.TextField(null=True, blank=True)
    style = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Legacy for {self.brand.name if hasattr(self, 'brand') else 'Unknown Brand'}"
