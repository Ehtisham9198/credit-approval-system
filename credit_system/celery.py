import os
from celery import Celery

# set default Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "credit_system.settings")

# create Celery app
app = Celery("credit_system")

# load settings from Django settings.py, using CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# auto-discover tasks.py in all installed apps
app.autodiscover_tasks()
