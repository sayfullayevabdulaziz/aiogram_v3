from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import PostgresDsn, RedisDsn, field_validator
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    # Bot config
    BOT_TOKEN: str
    ADMINS: list[int]
    USE_REDIS: bool
    POSTGRES_DSN: PostgresDsn

    @field_validator("POSTGRES_DSN", mode="after")
    def to_str(cls, v: str | MultiHostUrl) -> str:
        if isinstance(v, MultiHostUrl):
            return v.__str__()
        return v

    # Docker config
    BOT_CONTAINER_NAME: Optional[str]
    BOT_IMAGE_NAME: Optional[str]
    BOT_NAME: Optional[str]
    PG_CONTAINER_NAME: Optional[str]

    # Redis config
    REDIS_DSN: Optional[RedisDsn]


@lru_cache()
def get_config():
    return Config()


load_config = get_config()
