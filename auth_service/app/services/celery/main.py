import logging
import asyncio

from celery import Celery
from celery.signals import worker_process_init, worker_process_shutdown

from .config import CeleryConfig

from app.services.brokers.broker_manager import BrokersType, get_broker_manager

logger = logging.getLogger(__name__)

celery_app = Celery("celery_app")

celery_app.config_from_object(CeleryConfig())

celery_app.autodiscover_tasks([
    "app.services.celery.tasks.outbox_tasks",
])

@worker_process_init.connect
def on_worker_init(**kwargs):
    asyncio.get_event_loop().run_until_complete(get_broker_manager().initalize(BrokersType.RABBIT))
    logger.info("Broker initialized")


@worker_process_shutdown.connect
async def on_worker_shutdown(**kwargs):
    asyncio.get_event_loop().run_until_complete(get_broker_manager().shutdown())
    logger.info("Broker shutdown")
