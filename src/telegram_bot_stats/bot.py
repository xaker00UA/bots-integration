from aiogram import Bot, Dispatcher
from src.config.settings import settings
from src.config.logging import telegram_logger as log
import asyncio
from src.telegram_bot_stats.handler.setup import base_router


class TelegramBot(Bot):
    def __init__(self):
        super().__init__(token=settings.TOKENS.TELEGRAM_TOKEN)
        self.dp = Dispatcher()
        self.dp.startup.register(self.setup_hook)

    async def setup_hook(self):
        for router in base_router:
            self.dp.include_router(router)
            log.info(f"Register {router.name}")

    async def start_bot(self):
        log.info("Bot started")
        await self.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self)
        log.info("Bot stopped")


if __name__ == "__main__":
    bot = TelegramBot()
    asyncio.run(bot.start_bot())
