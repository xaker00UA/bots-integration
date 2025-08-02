from .user_commands.player import player_router
from aiogram.types import BotCommand


__all__ = ("base_router", "commands")

base_router = (player_router,)
commands = [
    BotCommand(command="help", description="Помощь"),
    BotCommand(command="get", description="Получить основную сессию"),
    BotCommand(command="set_primary", description="Установить основную сессию"),
    BotCommand(command="delete_session", description="Удалить сессию"),
    BotCommand(command="reset_session", description="Сбросить сессию"),
    BotCommand(command="get_session", description="Получить сессию по имени"),
]
