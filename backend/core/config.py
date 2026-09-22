from typing import List

from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str = ""
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOWED_ORIGIN: str = ""
    OPENAI_API_KEY : str 
