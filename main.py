import asyncio
import uvicorn
from src.discord_bot_stats.bot import DiscordBot
from src.telegram_bot_stats.bot import TelegramBot
from src.config.logging import ConfigLogger
from src.server.app import app
from src.database.core import init_models


async def run_fastapi():
    await init_models()
    config = uvicorn.Config(
        app=app, host="0.0.0.0", port=6000, log_level="info", reload=False
    )
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    ConfigLogger()
    telegram = TelegramBot()
    discord = DiscordBot()
    task_fastapi = asyncio.create_task(run_fastapi())

    task_one = asyncio.create_task(telegram.start_bot())
    task_two = asyncio.create_task(discord.start_bot())
    await asyncio.gather(task_one, task_two, task_fastapi)


if __name__ == "__main__":
    asyncio.run(main())
