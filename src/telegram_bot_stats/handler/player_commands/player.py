from aiogram import Router
from aiogram.filters import Command

player_router = Router(name="player_handler")


@player_router.message(Command("ping"))
async def ping(message):
    await message.answer("pong!")
