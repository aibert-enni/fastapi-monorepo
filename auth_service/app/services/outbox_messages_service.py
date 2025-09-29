from datetime import datetime, timezone
import json

from app.repositories.outbox_messages_repository import OutboxMessagesRepository
from app.schemas.outbox_messages import OutboxMessagesCreateS, OutboxMessagesS
from app.services.brokers.base import BrokerService
from app.services.brokers.rabbit.rabbit_service import RabbitBrokerService
from app.services.brokers.dummy_broker_service import DummyBrokerService
from app.services.brokers.broker_manager import BrokersType

class OutboxMessagesService:
    BATCH_SIZE = 10

    def __init__(self, outbox_messages_repository: OutboxMessagesRepository, broker_service: BrokerService) -> None:
        self.outbox_messages_repository = outbox_messages_repository
        self.broker_service = broker_service

    async def create(self, create_schema: OutboxMessagesCreateS) -> OutboxMessagesS:
        outbox_message = await self.outbox_messages_repository.save(create_schema)
        return outbox_message
    
    async def send_fallback_message(self, data, routing_key, broker_name) -> bool:
        if broker_name.lower() == BrokersType.RABBIT.value and isinstance(self.broker_service, RabbitBrokerService):
            return await self.broker_service.publish(json.loads(data), routing_key, save_fallback_message=False)
        elif broker_name == "dummy" and isinstance(self.broker_service, DummyBrokerService):
            return await self.broker_service.publish(data, routing_key, save_fallback_message=False)
        else:
            return False
        
    async def send_fallback_messages(self):
        outbox_messages = await self.outbox_messages_repository.get_all_by_is_not_sent()
        batch = set()
        for outbox_message in outbox_messages:
            if not self.broker_service.is_alive:
                break
            response_status = await self.send_fallback_message(outbox_message.data, outbox_message.routing_key, outbox_message.broker_name)
            if response_status:
                batch.add(outbox_message.id)
            if len(batch) >= self.BATCH_SIZE:
                await self.outbox_messages_repository.update_sent_at_by_ids(list(batch), datetime.now(timezone.utc))
                await self.outbox_messages_repository.session.commit()
                batch.clear()
        
        if len(batch) > 0:
            await self.outbox_messages_repository.update_sent_at_by_ids(list(batch), datetime.now(timezone.utc))
            await self.outbox_messages_repository.session.commit()