from faststream.rabbit import RabbitBroker

from app.core.settings import settings

from .rabbit_service import RabbitBrokerService

broker = RabbitBroker(url=settings.rabbit.URL)

rabbit_service = RabbitBrokerService(broker)

from .consumers import *  # noqa: F403,F401,E402
