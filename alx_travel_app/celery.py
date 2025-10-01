import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alx_travel_app.settings')

# Create a Celery app instance named 'alx_travel_app'
app = Celery('alx_travel_app')

# Configure Celery using settings from the Django settings.py file.
# The namespace='CELERY' means all Celery config keys should start with CELERY_
app.config_from_object('django.conf:settings', namespace='CELERY')

# Automatically discover and load task modules from all registered Django apps.
app.autodiscover_tasks()