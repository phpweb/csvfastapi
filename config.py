from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    tv_trend_csv_download_path: str
    chrome_driver_path: str
    env: str
    database_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
