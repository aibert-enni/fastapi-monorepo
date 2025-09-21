import logging

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.health_check import HealthCheckS
from app.services.brokers.base import BaseBrokerService

logger = logging.getLogger(__name__)

class HealthService:
    def __init__(self, db_session: AsyncSession, broker_service: BaseBrokerService) -> None:
        self.db_session = db_session
        self.broker_service = broker_service

    async def health_check(self) -> HealthCheckS:
        try:
            db_result = await self.db_session.execute(text('SELECT 1'))
            db_healthy = db_result is not None
        except Exception:
            db_healthy = False
    
        try:
            broker_healthy = await self.broker_service.health_check()
        except Exception:
            broker_healthy = False
        
        overall_healthy = db_healthy and broker_healthy

        return HealthCheckS(
            status="healthy" if overall_healthy else "unhealthy",
            checks={
                "db": "healthy" if db_healthy else "unhealthy",
                "broker": "healthy" if broker_healthy else "unhealthy",
            }
        )