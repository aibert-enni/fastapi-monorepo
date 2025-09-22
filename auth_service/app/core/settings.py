import json
import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent

logger = logging.getLogger(__name__)

class AdminSettings(BaseModel):
    USERNAME: str
    EMAIL: str
    PASSWORD: str

class DBSettings(BaseModel):
    URL: str


class RabbitSettings(BaseModel):
    URL: str
    ENABLE: bool = True


class JwtSettings(BaseModel):
    PRIVATE_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-private.pem"
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1

class GRPCSetttings(BaseSettings):
    port: str

class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )
    admin: AdminSettings
    db: DBSettings
    rabbit: RabbitSettings
    jwt: JwtSettings = JwtSettings()
    grpc: GRPCSetttings


settings = CommonSettings() # type: ignore

def print_settings():
    logger.info(json.dumps(settings.model_dump(), indent=2, default=str))