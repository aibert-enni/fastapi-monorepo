from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseModel):
    URL: str


class RabbitSettings(BaseModel):
    URL: str


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )
    db: DBSettings
    rabbit: RabbitSettings


settings = CommonSettings()
