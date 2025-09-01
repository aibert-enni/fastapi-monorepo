from faststream.rabbit import RabbitBroker

from app.core.settings import settings

broker = RabbitBroker(url=settings.rabbit.URL)

from .consumers import *  # noqa: F403,F401,E402
