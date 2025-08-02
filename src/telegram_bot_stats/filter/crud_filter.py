from aiogram.filters import Filter
from aiogram.types import CallbackQuery


class HandlerSessionFilter(Filter):

    async def __call__(self, query: CallbackQuery) -> dict | bool:
        try:
            action, session_id = query.data.split(":")
            return {"action": action, "session_id": session_id}
        except (ValueError, AttributeError):
            return False
