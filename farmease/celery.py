from __future__ import absolute_import
import os
from .settings import CELERY_RESULT_BACKEND, CELERY_TASK_TRACK_STARTED,BROKER_URL,INSTALLED_APPS
from celery import Celery
# from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'farmease.settings')

app = Celery('farmease',broker=BROKER_URL,
CELERY_RESULT_BACKEND=BROKER_URL,CELERY_TASK_TRACK_STARTED=True)

app.config_from_object('django.conf:settings')

# Load task modules from all registered Django apps.lambda: settings.INSTALLED_APPS
app.autodiscover_tasks(INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')