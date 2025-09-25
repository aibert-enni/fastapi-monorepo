import json
import logging
import time
from typing import Optional
from faststream.rabbit import RabbitBroker

from app.services.brokers.base import BrokerService
from app.schemas.outbox_messages import OutboxMessagesCreateS
from app.core.dependencies import get_outbox_messages_service
from app.services.brokers.broker_manager import BrokersType

logger = logging.getLogger(__name__)

class RabbitBrokerService(BrokerService):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker
        self.is_alive = False
        self.timeout = 60
        self.last_failure_time: Optional[float] = None

    async def start(self) -> None:
        await self.broker.start()
        self.is_alive = True

    async def _save_fallback_message(self, data, routing_key):
        data_json = json.dumps(data)
        async with get_outbox_messages_service() as service:
            await service.create(OutboxMessagesCreateS(data=data_json, routing_key=routing_key, broker_name=BrokersType.RABBIT.value))

    async def publish(self, data, routing_key, save_fallback_message: bool = True) -> bool:
        if self.last_failure_time is not None and self.last_failure_time + self.timeout > time.time():
            logging.error(f"Rabbit broker is not available, last failure time: {self.last_failure_time}")
            if save_fallback_message:
                await self._save_fallback_message(data, routing_key)
            return False
        try:
            await self.broker.publish(data, routing_key)
            if not self.is_alive:
                self.is_alive = True
        except Exception as e:
            logger.error(f"Rabbit broker error for publish in {routing_key} for data: {data}: \n{e}")
            self.last_failure_time = time.time() + self.timeout
            self.is_alive = False
            await self._save_fallback_message(data, routing_key)
            return False
        return True

    async def publish_user_created(self, user) -> bool:
        return await self.publish(user, "user.created")

    async def stop(self) -> None:
        await self.broker.stop()
        self.is_alive = False

    async def health_check(self) -> bool:
        return await self.broker.ping(timeout=5)