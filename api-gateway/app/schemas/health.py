from pydantic import BaseModel


class HealthCheckServiceS(BaseModel):
    status: str
    checks: dict[str, str]

class HealthCheckServicesS(BaseModel):
    status: str
    user: HealthCheckServiceS
    media: HealthCheckServiceS
    auth: HealthCheckServiceS

class HealthCheckS(BaseModel):
    status: str
    services: HealthCheckServicesS