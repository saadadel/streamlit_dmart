""" Application Settings """

import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings class"""

    dmart_url: str = "http://localhost:8282"
    
    model_config = SettingsConfigDict(
        env_file=os.getenv("BACKEND_ENV", "config.env"), env_file_encoding="utf-8"
    )


settings = Settings()
# Uncomment this when you have a problem running the app to see if you have a problem with the env file
# print(settings.model_dump_json())
