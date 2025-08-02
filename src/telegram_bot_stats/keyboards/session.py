from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.orm_model import OrmAccount


def session_keyboards(action: str, items: list[OrmAccount]):
    builder = InlineKeyboardBuilder()
    for item in items:
        builder.add(
            InlineKeyboardButton(
                text=item.name_session, callback_data=f"{action}:{item.session_id}"
            )
        )
    builder.adjust(2)
    return builder.as_markup()


add_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Добавить сессию", callback_data="add_session"),
        ]
    ]
)
