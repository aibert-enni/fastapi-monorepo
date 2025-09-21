import logging

from app.core.dependencies import get_auth_service
from app.core.settings import print_settings, settings
from app.schemas.auth import AuthCreateS

logger = logging.getLogger(__name__)

async def setup() -> None:
    print_settings()
    try:
        async with get_auth_service() as auth_service:
            await auth_service.create_auth(AuthCreateS(username=settings.admin.USERNAME, email=settings.admin.EMAIL, password=settings.admin.PASSWORD, is_active=True, is_superuser=True))
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")