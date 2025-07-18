import discord
from discord import app_commands
from src.config.settings import settings
from src.config.logging import discord_logger as log
from src.discord_bot_stats.cogs.setup import base_router


class DiscordBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        self.synced = False
        self.added = False
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        for router in base_router:
            self.tree.add_command(router)
            log.info(f"Register {router.name}")

        array_commands = await self.tree.sync()
        for command in array_commands:
            log.info(command.name)
        log.info("Syncing commands to global guild")

    async def start_bot(self):
        log.info("Bot started")
        await self.start(settings.TOKENS.DISCORD_TOKEN)
        log.info("Bot stopped")
        self.on_error



if __name__ == "__main__":
    bot = DiscordBot()
    bot.run(settings.TOKENS.DISCORD_TOKEN)
    log.info("Bot started")
