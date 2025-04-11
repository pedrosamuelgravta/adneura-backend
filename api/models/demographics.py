from django.db import models
from django.utils import timezone
    
class Demographics(models.Model):
    audience = models.OneToOneField(
        'Audience',
        on_delete=models.CASCADE,
        related_name='demographics'
    )
    gender = models.JSONField(null=True, blank=True)
    age_bracket = models.CharField(max_length=50, choices=[
        ('18-24', '18-24'),
        ('25-34', '25-34'),
        ('35-44', '35-44'),
        ('45-54', '45-54'),
        ('55-64', '55-64'),
        ('64+', '64+')
    ], null=True, blank=True)
    hhi = models.CharField(max_length=50, 
    choices=[
        ('<75k', '<75k'),
        ('75k-100k', '75k-100k'),
        ('100k-150k', '100k-150k'),
        ('150k-250k', '150k-250k'),
        ('>250k', '>250k'),
    ]
    ,null=True, blank=True)
    race = models.JSONField(null=True, blank=True)
    education = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Demographics for {self.audience.name}"