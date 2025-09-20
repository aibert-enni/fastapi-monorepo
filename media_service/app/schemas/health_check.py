from pydantic import BaseModel


class HealthCheckS(BaseModel):
    status: str
    checks: dict