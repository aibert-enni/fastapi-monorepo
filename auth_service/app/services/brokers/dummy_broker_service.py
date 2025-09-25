import logging

from app.services.brokers.base import BrokerService

logger = logging.getLogger(__name__)

class DummyBrokerService(BrokerService):
    async def start(self) -> None:
        logging.info("Dummy broker: service started")

    async def publish(self, data: dict, routing_key: str) -> None:
        logging.info(f"Dummy broker: published {data} to {routing_key}")

    async def publish_user_created(self, user: dict) -> None:
        logging.info(f"Dummy broker: published {user} to user.created")

    async def stop(self) -> None:
        logging.info("Dummy broker: service stopped")

    async def health_check(self) -> bool:
        return True