from typing import Literal, Optional

from app.services.brokers.base import BrokerService


class BrokerManager:
    _instanse: Optional["BrokerManager"] = None
    _broker: Optional[BrokerService] = None

    def __new__(cls) -> "BrokerManager":
        if cls._instanse is None:
            cls._instanse = super().__new__(cls)
        return cls._instanse
    
    async def initalize(self, broker_type: Literal["dummy", "rabbit"]):
        if self._broker is None:
            if broker_type == "rabbit":
                from app.services.brokers.rabbit.rabbit_service import RabbitBrokerService
                from app.services.brokers.rabbit.main import broker
                self._broker = RabbitBrokerService(broker=broker)
            else:
                from app.services.brokers.dummy_broker_service import DummyBrokerService
                self._broker = DummyBrokerService()
            await self._broker.start()

    def get_broker(self) -> BrokerService:
        if self._broker is None:
            raise RuntimeError("Broker is not initalized")
        return self._broker
    
    async def shutdown(self):
        if self._broker is not None:
            await self._broker.stop()

def get_broker_manager() -> BrokerManager:
    return BrokerManager()