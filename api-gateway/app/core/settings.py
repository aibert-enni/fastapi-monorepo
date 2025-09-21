import json
import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent

logger = logging.getLogger("fastapi")

class GRPCSettings(BaseModel):
    auth_url: str
    media_url: str
    user_url: str

class JwtSettings(BaseModel):
    PUBLIC_KEY_PATH: Path = BASE_DIR / "certs" / "jwt-public.pem"
    ALGORITHM: str = "RS256"

class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )
    jwt: JwtSettings = JwtSettings()
    grpc: GRPCSettings
    

 
settings = CommonSettings() # type: ignore

def log_settings():
    logger.info(json.dumps(settings.model_dump(), indent=2, default=str))