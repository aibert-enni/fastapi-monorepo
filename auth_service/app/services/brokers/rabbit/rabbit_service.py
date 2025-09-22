from faststream.rabbit import RabbitBroker

from app.services.brokers.base import BaseBrokerService

from app.core.settings import settings

class RabbitBrokerService(BaseBrokerService):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker

    async def start(self) -> None:
        if settings.rabbit.ENABLE:
            await self.broker.start()

    async def publish(self, data, routing_key) -> None:
        if settings.rabbit.ENABLE:
            await self.broker.publish(data, routing_key)

    async def publish_user_created(self, user) -> None:
        if settings.rabbit.ENABLE:
            await self.publish(user, "user.created")

    async def stop(self) -> None:
        if settings.rabbit.ENABLE:
            await self.broker.stop()

    async def health_check(self) -> bool:
        if settings.rabbit.ENABLE:
            return await self.broker.ping(timeout=5)
        else:
            return False