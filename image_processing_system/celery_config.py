import os
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'image_processing_system.settings')

# Create the Celery app
app = Celery('image_processing_system')

# Load task modules from all registered Django apps
app.autodiscover_tasks()

# Configure Celery using settings from Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')
