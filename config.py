from functools import lru_cache
from pydantic import BaseSettings, BaseModel


class Settings(BaseSettings):
    tv_trend_csv_download_path: str
    chrome_driver_path: str
    env: str
    database_url: str
    mail_username: str
    mail_password: str
    mail_from: str
    mail_from_name: str
    mail_port: int
    mail_server: str
    api_key: str
    api_secret: str

    class Config:
        env_file = ".env"


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "csvfastapi"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | [%(filename)s:%(lineno)d] | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": "api.log",
            "encoding": 'utf-8',
        },
    }
    loggers = {
        "csvfastapi": {"handlers": ["default", "file"], "level": LOG_LEVEL},
    }


@lru_cache()
def get_settings():
    return Settings()


@lru_cache()
def get_log_config():
    return LogConfig()
