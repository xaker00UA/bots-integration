from discord import app_commands, Interaction

from src.discord_bot_stats.cogs.user_commands.ui import SessionView
from src.database.core import get_session
from src.database.repo import Repository
from src.models.model import Region
from src.service.api import APIBackendServer
from src.config.logging import discord_logger as log
from src.discord_bot_stats.utils.message_generation import generate_player_stats_embed
from src.service.processing import ProcessingSession


class UserCommands(app_commands.Group):
    def __init__(self):
        super().__init__(name="player", description="Комадны для игрока")
        self.error(self._error_handler)  # Вот вызов!

    @app_commands.command(name="reset", description="Сброс сессии")
    async def reset_session(self, interaction: Interaction):
        view = await SessionView.create(interaction.user.id, "reset")
        await interaction.response.send_message(
            "👇 Выберите сессию для сброса:", view=view, ephemeral=True
        )

    @app_commands.command(name="add_session", description="Добавить сессию")
    async def add_session(
        self,
        interaction: Interaction,
        name: str,
        region: Region = Region.eu,
        name_session: str | None = None,
    ):
        await interaction.response.defer(thinking=True)

        service = ProcessingSession()
        await service.create_session(
            discord_id=interaction.user.id,
            name=name,
            region=region.value,
            name_session=name_session,
        )
        await interaction.followup.send("✅ Сессия добавлена", ephemeral=True)

    @app_commands.command(name="set_primary", description="Установить основную сессию")
    async def set_primary_session(self, interaction: Interaction):
        view = await SessionView.create(interaction.user.id, "set")
        await interaction.response.send_message(
            "👇 Выберите сессию для установки:", view=view, ephemeral=True
        )

    @app_commands.command(name="delete", description="Удалить сессию")
    async def delete_session(self, interaction: Interaction):
        view = await SessionView.create(interaction.user.id, "delete")
        await interaction.response.send_message(
            "👇 Выберите сессию для удаления:", view=view, ephemeral=True
        )

    @app_commands.command(name="get_session", description="Удалить сессию")
    async def get_session_player(self, interaction: Interaction):
        view = await SessionView.create(interaction.user.id, "get")
        await interaction.response.send_message(
            "👇 Выберите сессию для отображения:", view=view, ephemeral=True
        )

    @app_commands.command(name="get", description="Получение сессии игрока")
    async def get_session(
        self,
        interaction: Interaction,
        name: str | None = None,
        region: Region = Region.eu,
    ):
        await interaction.response.defer(thinking=True)
        embed = await ProcessingSession().get(
            name=name, region=region.value, user_id=interaction.user.id
        )
        await interaction.followup.send(embed=embed)

    async def _error_handler(
        self, interaction: Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.CommandInvokeError):
            if interaction.response.is_done():
                await interaction.followup.send(
                    f"⚠️ Локальная ошибка: {str(error.original)}", ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    f"⚠️ Локальная ошибка:{str(error.original)}", ephemeral=True
                )
        log.exception(
            f"Ошибка в команде: {type(error).__name__} — {error}",
            exc_info=True,
        )


# Создаём объект группы
user_group = UserCommands()
