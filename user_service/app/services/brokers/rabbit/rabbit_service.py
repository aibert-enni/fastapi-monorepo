from faststream.rabbit import RabbitBroker

from app.services.brokers.base import BaseBrokerService


class RabbitBrokerService(BaseBrokerService):
    def __init__(self, broker: RabbitBroker) -> None:
        self.broker = broker

    async def start(self) -> None:
        await self.broker.start()

    async def publish(self, data, routing_key) -> None:
        await self.broker.publish(data, routing_key)

    async def stop(self) -> None:
        await self.broker.stop()

    async def health_check(self) -> bool:
        return await self.broker.ping(timeout=5)