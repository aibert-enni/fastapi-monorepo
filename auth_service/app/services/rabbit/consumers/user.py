import logging

from faststream import Depends

from app.schemas.auth import AuthCreateS
from app.schemas.user import UserS
from app.services.auth_service import AuthService
from app.services.rabbit.dependencies import get_auth_service
from app.services.rabbit.main import broker

logger = logging.getLogger(__name__)


@broker.subscriber("user.created")
async def get_created_user(
    user: UserS, auth_service: AuthService = Depends(get_auth_service)
):
    logger.info(user)
    auth_schema = AuthCreateS(
        user_id=user.id,
        password=user.password,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
    )
    try:
        await auth_service.create_auth(auth_schema)
    except Exception as e:
        logger.error(e)
