import os
from celery import Celery

# Define a variável de ambiente para o settings do Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("adneura-api")

# Carrega as configurações do Django para o Celery com um namespace 'CELERY'
app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobre automaticamente os tasks de cada app Django
app.autodiscover_tasks()
