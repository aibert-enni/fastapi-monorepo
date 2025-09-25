from celery.schedules import crontab

from app.core.settings import settings


class CeleryConfig:
    broker_url = settings.rabbit.URL
    backend = 'rpc://'

    # # Task Execution Settings
    task_serializer = 'json' 
    accept_content = ['json']
    result_serializer = 'json'
    timezone = 'UTC'
    enable_utc = True

    # Worker Configuration
    worker_concurrency = 4
    worker_prefetch_multiplier = 1  # Critical: prevents memory issues
    worker_max_tasks_per_child = 1000  # Restart workers to prevent memory leaks
    worker_disable_rate_limits = False

    beat_schedule = {
        "send-outbox-every-minute": {
            "task": "app.services.celery.tasks.outbox_tasks.send_outbox_message",
            "schedule": crontab(minute="*/5"),  # every 5 minutes
        },
    }

    # Reliability Settings - These are crucial for production
    task_acks_late = True  # Acknowledge tasks only after completion
    task_reject_on_worker_lost = True  # Retry if worker crashes
    task_track_started = True  # Track when tasks actually start

    # Result Configuration
    result_expires = 3600

    # Retry Configuration
    task_default_retry_delay = 60  # Wait 1 minute before retry
    task_max_retries = 3
    task_default_queue = 'celery'

    # Monitoring and Logging
    worker_send_task_events = True
    task_send_sent_event = True

    # Security (important for production)
    task_always_eager = False  # Never set to True in production
    task_store_eager_result = True