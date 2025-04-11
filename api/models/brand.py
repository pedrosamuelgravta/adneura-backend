from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .brand_info import BrandInfo
from .advertising_legacy import AdvertisingLegacy

class Brand(models.Model):
    name = models.CharField(max_length=255)
    brand_url = models.URLField(null=True, blank=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='brands'
    )
    brand_info = models.OneToOneField(
        'BrandInfo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='brand'
    )
    ad_legacy = models.OneToOneField(
        'AdvertisingLegacy',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='brand'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.brand_info:
            self.brand_info = BrandInfo.objects.create()
        if not self.ad_legacy:
            self.ad_legacy = AdvertisingLegacy.objects.create()
        super().save(*args, **kwargs)