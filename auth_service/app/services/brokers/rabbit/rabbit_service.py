from faststream.rabbit import RabbitBroker

from app.services.brokers.base import BaseBrokerService


class RabbitBrokerService(BaseBrokerService):
    def __init__(self, broker: RabbitBroker):
        self.broker = broker

    async def start(self):
        await self.broker.start()

    async def publish(self, data, routing_key):
        await self.broker.publish(data, routing_key)

    async def publish_user_created(self, user):
        await self.publish(user, "user.created")

    async def stope(self):
        await self.broker.stop()
