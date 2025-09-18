from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent.parent


class DBSettings(BaseModel):
    URL: str


class RabbitSettings(BaseModel):
    URL: str


class S3Settings(BaseModel):
    access_key: str
    secret_key: str
    endpoint_url: str
    bucket_name: str

class GRPCSettings(BaseModel):
    port: str

class FileSettings(BaseModel):
    default_expire_seconds: int = 3600 # 1 hour

class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_nested_delimiter="__",
    )
    grpc: GRPCSettings
    db: DBSettings
    rabbit: RabbitSettings
    s3: S3Settings
    file: FileSettings = FileSettings()


settings = CommonSettings()  # type: ignore
