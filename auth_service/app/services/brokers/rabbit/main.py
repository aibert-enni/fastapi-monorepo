from faststream.rabbit import RabbitBroker

from app.core.settings import settings

from .rabbit_service import RabbitBrokerService

broker = RabbitBroker(url=settings.rabbit.URL)

rabbit_broker_service = RabbitBrokerService(broker)
