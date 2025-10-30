import sys

from loguru import logger

from src.shared.config import settings


def setup_logger():
    logger.remove()

    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        level="DEBUG" if settings.DEBUG else "INFO",
        enqueue=True,
    )
