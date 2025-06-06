from functools import lru_cache
from pydantic_settings import BaseSettings

from typing import Optional


class __Settings__(BaseSettings):
    DATABASE_STRING: str = "postgresql://user:password@db:5432/db"
    OPENAI_API_KEY: str = "your_openai_api_key"
    DATABASE_STRING_NAME: Optional[str] = "db"
    ACCESS_TOKEN_EXPIRE_MINUTE: Optional[int] = 10
    REFRESH_TOKEN_EXPIRE_DAY: Optional[int] = 7
    SECRET_KEY: str = "my_secret_key"
    ALGORITHM: str = "HS256"
    TIMEZONE: Optional[int] = 0

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> __Settings__:
    return __Settings__()
