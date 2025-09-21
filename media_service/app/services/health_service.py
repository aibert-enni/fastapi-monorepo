from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.health_check import HealthCheckS
from app.services.s3_service import S3Client


class HealthService:
    def __init__(self, db_session: AsyncSession, s3_service: S3Client):
        self.db_session = db_session
        self.s3_service = s3_service

    async def health_check(self) -> HealthCheckS:
        try:
            db_result = await self.db_session.execute(text('SELECT 1'))
            db_healthy = db_result is not None
        except Exception:
            db_healthy = False
    
        try:
            broker_healthy = await self.s3_service.health_check()
        except Exception:
            broker_healthy = False
        
        overall_healthy = db_healthy and broker_healthy

        return HealthCheckS(
            status="healthy" if overall_healthy else "unhealthy",
            checks={
                "db": "healthy" if db_healthy else "unhealthy",
                "s3 storage": "healthy" if broker_healthy else "unhealthy",
            }
        )