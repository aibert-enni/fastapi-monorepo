import asyncio
import logging
from app.services.celery.main import celery_app
from app.core.dependencies import get_outbox_messages_service

logger = logging.getLogger(__name__)

@celery_app.task
def send_outbox_message():
    async def _send_outbox_message():
        async with get_outbox_messages_service() as service:
            await service.send_fallback_messages()
    asyncio.get_event_loop().run_until_complete(_send_outbox_message())