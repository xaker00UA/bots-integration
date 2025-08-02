from typing import Callable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from typing import Any, Awaitable, Callable, Dict
from src.config.logging import telegram_logger as log
from src.error.exception import *


class ExceptionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ):
        try:
            return await handler(event, data)
        except BaseCustomException as e:
            if isinstance(event, CallbackQuery):
                await event.message.answer(str(e))
            else:
                await event.answer(str(e))

        except Exception as e:
            log.exception(e)
            if isinstance(event, CallbackQuery):
                await event.message.answer("Попробуйте позже")
            else:
                await event.answer("Попробуйте позже")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data,
    ):
        user_id = getattr(event.from_user, "id", "неизвестно")
        event_type = type(event).__name__
        log.info(f"Получено событие {event_type} от пользователя id:{user_id}")
        return await handler(event, data)
