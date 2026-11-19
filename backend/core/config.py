from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    DATABASE_URL: str = " "
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = " "
    OPENAI_API_KEY: str = ""

    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v:str) -> List[str]:
        return v.split(",") if v else[]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="UTF-8",
        case_sensitive=True,
        extra="ignore"
    )
#instansiate
settings = Settings()
