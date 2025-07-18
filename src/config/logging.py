from typing import Any
from loguru import logger
from src.config.settings import settings
from sys import stdout


class ConfigLogger:
    def __init__(self, level=settings.LOG_LEVEL):
        self.level = level
        self._setup_logger()

    def _setup_logger(self):
        logger.remove()
        logger.add(
            "logs/telegram.log",
            rotation="10 MB",
            compression="zip",
            filter=lambda record: record["extra"].get("source") == "telegram"
            and record["level"].no < 40,
            serialize=True,
            enqueue=True,
            encoding="utf-8",
        )
        logger.add(
            "logs/discord.log",
            rotation="10 MB",
            compression="zip",
            filter=lambda record: record["extra"].get("source") == "discord"
            and record["level"].no < 40,
            enqueue=True,
            encoding="utf-8",
        )
        logger.add(
            stdout,
            colorize=True,
            level=self.level,
            enqueue=True,
            format=self.custom_format,
        )
        logger.add(
            "logs/error.log",
            rotation="10 MB",
            compression="zip",
            level="ERROR",
            enqueue=True,
            encoding="utf-8",
            backtrace=True,
            diagnose=True,
        )
        logger.info(f"Logger initialized with level: {self.level}")

    def custom_format(self, record):
        source = record["extra"].get("source", "root")
        return f"{{time:MM-DD HH:mm:ss!UTC}} | <level>{record['level']:^8}</level> | <b>{source:^8}</b> | {{message}} \n"


telegram_logger = logger.bind(source="telegram")
discord_logger = logger.bind(source="discord")
