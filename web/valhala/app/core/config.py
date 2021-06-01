import logging
import os.path as path
import sys
from typing import List
from loguru import logger
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret

dotenv_path = path.abspath(path.join(__file__ ,"../../../.env"))
config = Config(dotenv_path)

API_PREFIX = "/api"
VERSION = "0.0.0"
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret)
PROJECT_NAME: str = config("PROJECT_NAME", default="Valhala")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default=""
)
# uvicorn configuration
UVICORN_HOST: str = config("UVICORN_HOST", default="0.0.0.0")
UVICORN_PORT: int = config("UVICORN_PORT", cast=int, default=5000)
UVICORN_RELOAD: bool = config("UVICORN_RELOAD", cast=bool, default=False)
UVICORN_ACCESS_LOG: bool = config("UVICORN_ACCESS_LOG", cast=bool, default=False)
UVICORN_LOG_LEVEL: str = "debug" if DEBUG else "info"
# logging configuration
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
logging.basicConfig(level=LOGGING_LEVEL)
logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])