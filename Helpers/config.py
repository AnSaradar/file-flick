from pydantic_settings import BaseSettings , SettingsConfigDict
from typing import List

class Settings(BaseSettings):

    IMAGES: List[str]
    VIDEOS: List[str]
    DOCUMENTS: List[str]

    class Config(SettingsConfigDict):
        env_file = ".env"

def get_settings():
    return Settings()