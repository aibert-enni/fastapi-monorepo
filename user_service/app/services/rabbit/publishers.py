from app.schemas.user import UserS
from app.services.rabbit.main import broker

publisher = broker.publisher("user.created")


async def publish_user_created(user: UserS) -> None:
    await publisher.publish(user.model_dump())
