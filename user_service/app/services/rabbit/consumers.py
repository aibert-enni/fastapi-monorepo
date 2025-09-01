import logging

from faststream import Depends

from app.schemas.user import UserCreateS, UserS
from app.services.rabbit.dependencies import get_user_service
from app.services.rabbit.main import broker
from app.services.user_service import UserService

logger = logging.getLogger(__name__)


@broker.subscriber("user.created")
async def get_created_user(
    user: UserS, user_service: UserService = Depends(get_user_service)
):
    logger.info(user)
    user_schema = UserCreateS(
        id=user.id,
    )
    try:
        await user_service.create_user(user_schema)
    except Exception as e:
        logger.error(e)
