import asyncio

from src.discord_bot_stats.bot import DiscordBot
from src.telegram_bot_stats.bot import TelegramBot
from src.config.logging import ConfigLogger


async def main():
    ConfigLogger()
    telegram = TelegramBot()
    discord = DiscordBot()

    task_one = asyncio.create_task(telegram.start_bot())
    task_two = asyncio.create_task(discord.start_bot())
    await asyncio.gather(task_one, task_two)


if __name__ == "__main__":
    asyncio.run(main())
