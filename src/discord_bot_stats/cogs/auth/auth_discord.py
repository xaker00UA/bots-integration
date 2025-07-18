import discord
from src.models.model import Region
from src.service.api import APIBackendServer
from src.config.logging import discord_logger as log
from src.discord_bot_stats.utils.message_generation import generate_player_stats_embed
from src.service.auth import DiscordAuth


import discord


class AuthView(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        self.add_item(
            discord.ui.Button(
                label="Авторизоваться через Discord",
                style=discord.ButtonStyle.link,
                url=url,
            )
        )


class AuthCommands(discord.app_commands.Group):
    def __init__(self):
        super().__init__(name="auth", description="Команды для авторизации")

    @discord.app_commands.command(name="auth", description="Авторизация")
    async def auth(self, interaction: discord.Interaction):
        url = await DiscordAuth().auth_user()
        log.info(f"Auth url: {url}")
        view = AuthView(url)
        await interaction.response.send_message(
            "Нажми кнопку ниже для авторизации:", view=view, ephemeral=True
        )


auth_group = AuthCommands()
