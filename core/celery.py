from celery import Celery
from core.config import get_settings

settings = get_settings()

celery_app = Celery('adneura_tasks',
                    broker=f"{settings.REDIS_STRING}/0",
                    backend=f"{settings.REDIS_STRING}/1",)

celery_app.autodiscover_tasks(['tasks'])
