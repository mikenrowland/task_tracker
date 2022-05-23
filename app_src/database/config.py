import logging
from typing import Callable
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from starlette.config import Config
from starlette.datastructures import Secret

logger = logging.getLogger(__name__)

config = Config(".env")


MODELS = ["models.base", "models.register", "models.task", "aerich.models"]

POSTGRES_USER = config("POSTGRES_USER", cast=Secret)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_HOST = config("POSTGRES_HOST", cast=Secret)
POSTGRES_PORT = config("POSTGRES_PORT", cast=Secret)
POSTGRES_DB = config("POSTGRES_DB", cast=Secret)


async def init_db(app: FastAPI) -> None:
    """Initialize database."""
    try:
        register_tortoise(
            app,
            db_url=f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
            modules={"models": MODELS},
            generate_schemas=True,
            add_exception_handlers=True,
        )
        logger.warning("--- DB CONNECTION WAS SUCCESSFUL ---")
    except Exception as e:
        logger.warning("--- DB CONNECTION ERROR ---")
        logger.warning(e)
        logger.warning("--- DB CONNECTION ERROR ---")


def app_start_up_handler(app: FastAPI) -> Callable:
    async def start_app() -> None:
        await init_db(app)

    return start_app
