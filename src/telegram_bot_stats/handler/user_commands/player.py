from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from src.config.settings import settings
from src.telegram_bot_stats.keyboards.session import session_keyboards, add_button
from src.service.processing import TelegramProcessing
import re

from src.telegram_bot_stats.filter.crud_filter import HandlerSessionFilter
from src.telegram_bot_stats.utils.message_generation import (
    GenerateStatsMessage,
    message_res,
)

player_router = Router(name="player_handler")


@player_router.message(CommandStart())
async def start(message: Message):
    await message.answer(message_res.get("start", "message"))


@player_router.message(Command("help"))
async def help(message: Message):
    await message.answer(text=message_res.get("help", "message"))


@player_router.message(Command("get"))
async def get(message: Message):
    text = message.text.removeprefix("/get").strip()
    name = None
    parts = re.split(r"[ ,;@\\]+", text)
    if len(parts) > 1:
        for part in parts:
            char = part.split("/")
            if len(char) >= 2:
                name = char[0]
        if not name:
            name = parts[0]
            region = parts[1] if len(parts) >= 2 else "eu"
        text = await TelegramProcessing().get(name=name, region=region)

    else:
        text = await TelegramProcessing().get(
            type="telegram", user_id=message.from_user.id
        )

    await message.answer(text=text, parse_mode="HTML")


@player_router.message(Command("add"))
async def add_session(message: Message):
    text = message.text.removeprefix("/add").strip()
    name = None
    parts = re.split(r"[ ,;@\\]+", text)
    if len(parts) >= 2:
        for part in parts:
            char = part.split("/")
            if len(char) >= 2:
                name = char[0]
        if not name:
            name, region = parts[0], parts[1]
        name_session = parts[2] if len(parts) >= 3 else None
        await TelegramProcessing().create_session(
            user_name=message.from_user.full_name,
            name=name,
            region=region,
            telegram_id=message.from_user.id,
            name_session=name_session,
        )
        await message.answer(
            text=message_res.get("add", "success").format(name=name, region=region),
            parse_mode="HTML",
        )
    else:
        await message.answer(text=message_res.get("add", "error"), parse_mode="HTML")


@player_router.message(Command("set_primary"))
async def set_primary(message: Message):
    sessions = await TelegramProcessing().get_sessions(message.from_user.id)
    await message.answer(
        text="Выберите сессию", reply_markup=session_keyboards("set_primary", sessions)
    )


@player_router.message(Command("delete_session"))
async def delete_session(message: Message):
    sessions = await TelegramProcessing().get_sessions(message.from_user.id)
    await message.answer(
        text="Выберите сессию", reply_markup=session_keyboards("delete", sessions)
    )


@player_router.message(Command("reset_session"))
async def reset_session(message: Message):
    sessions = await TelegramProcessing().get_sessions(message.from_user.id)
    await message.answer(
        text="Выберите сессию", reply_markup=session_keyboards("reset", sessions)
    )


@player_router.message(Command("get_session"))
async def get_session(message: Message):
    sessions = await TelegramProcessing().get_sessions(message.from_user.id)
    await message.answer(
        text="Выберите сессию", reply_markup=session_keyboards("get_session", sessions)
    )


@player_router.callback_query(HandlerSessionFilter())
async def callback_action(callback: CallbackQuery, action: str, session_id: int):
    match action:
        case "delete":
            response = await TelegramProcessing().delete_session(session_id)
            await callback.answer()
            await callback.message.edit_text(
                text=message_res.get("delete_session", "success")
            )
        case "reset":
            await TelegramProcessing().reset_session(session_id)
            await callback.answer()
            await callback.message.answer(
                text=message_res.get("reset_session", "success")
            )
        case "get_session":
            text = await TelegramProcessing().get(session_id=session_id)
            await callback.answer()
            await callback.message.answer(text=text, parse_mode="HTML")
        case "set_primary":
            await TelegramProcessing().set_primary_session(session_id)
            await callback.answer()
            await callback.message.answer(
                text=message_res.get("set_primary", "success"), parse_mode="HTML"
            )

        case _:
            ValueError("Неизвестное действие")


@player_router.message(Command("top"))
async def top_rating(message: Message):
    sent = await message.answer("Формируем топ...")
    text = await TelegramProcessing().get_top_rating()
    await sent.edit_text(text=text, parse_mode="HTML")


@player_router.message(Command("site"))
async def site(message: Message):
    await message.answer(text=settings.FRONTEND.FRONTEND_URL, parse_mode="HTML")
