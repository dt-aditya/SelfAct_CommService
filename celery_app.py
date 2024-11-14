# celery_app.py
from celery import Celery
from celery.schedules import crontab
import app.tasks.message_tasks
from app.services.message_service import send_message_task
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery_app = Celery("app", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery_app.conf.beat_schedule = {
    "flush-log-buffer-every-minute": {
        "task": "app.tasks.message_tasks.flush_log_buffer_task",
        "schedule": crontab(minute="*"),
    },
}

celery_app.conf.timezone = "UTC"
