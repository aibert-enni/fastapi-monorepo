import json
import logging
import time
from typing import Optional
from faststream.rabbit import RabbitBroker

from app.services.brokers.base import BrokerService
from app.schemas.outbox_messages import OutboxMessagesCreateS
from app.core.dependencies import get_outbox_messages_service

logger = logging.getLogger(__name__)

class RabbitBrokerService(BrokerService):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker
        self.is_alive = False
        self.timeout = 60
        self.last_failure_time: Optional[float] = None

    async def start(self) -> None:
        await self.broker.start()

    async def _save_fallback_message(self, data, routing_key):
        data_json = json.dumps(data)
        async with get_outbox_messages_service() as service:
            await service.create(OutboxMessagesCreateS(data=data_json, routing_key=routing_key, broker_name="Rabbit"))

    async def publish(self, data, routing_key) -> None:
        if self.last_failure_time is not None and self.last_failure_time + self.timeout > time.time():
            logging.error(f"Rabbit broker is not available, last failure time: {self.last_failure_time}")
            await self._save_fallback_message(data, routing_key)
            return
        try:
            await self.broker.publish(data, routing_key)
        except Exception as e:
            logger.error(f"Rabbit broker error for publish in {routing_key} for data: {data}: \n{e}")
            self.last_failure_time = time.time() + self.timeout
            await self._save_fallback_message(data, routing_key)

    async def publish_user_created(self, user) -> None:
        await self.publish(user, "user.created")

    async def stop(self) -> None:
        await self.broker.stop()

    async def health_check(self) -> bool:
        return await self.broker.ping(timeout=5)