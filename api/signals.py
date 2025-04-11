from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from api.seeders.seeder import run_seed_for_user


@receiver(post_save, sender=User)
def create_default_brand(sender, instance, created, **kwargs):
    if created:
        run_seed_for_user(instance)
