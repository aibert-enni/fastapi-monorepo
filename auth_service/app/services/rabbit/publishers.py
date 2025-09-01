from app.schemas.user import UserS

from .main import broker


async def publish_create_user(user: UserS) -> None:
    await broker.publish(user, "user.created")
