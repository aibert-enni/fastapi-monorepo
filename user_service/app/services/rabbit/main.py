from faststream.rabbit import RabbitBroker

from app.core.settings import settings

broker = RabbitBroker(url=settings.rabbit.URL)
