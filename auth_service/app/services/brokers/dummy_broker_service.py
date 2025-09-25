import logging

from app.services.brokers.base import BrokerService

logger = logging.getLogger(__name__)

class DummyBrokerService(BrokerService):
    is_alive = False

    async def start(self) -> None:
        logging.info("Dummy broker: service started")
        self.is_alive = True

    async def publish(self, data: dict, routing_key: str, save_fallback_message: bool = True) -> bool:
        logging.info(f"Dummy broker: published {data} to {routing_key}")
        return True

    async def publish_user_created(self, user: dict) -> bool:
        logging.info(f"Dummy broker: published {user} to user.created")
        return await self.publish(user, "user.created")

    async def stop(self) -> None:
        logging.info("Dummy broker: service stopped")
        self.is_alive = False

    async def health_check(self) -> bool:
        return self.is_alive