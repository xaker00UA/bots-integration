from cProfile import label
import discord

from src.database.orm_model import OrmAccount
from src.service.processing import ProcessingSession


class SessionDropdown(discord.ui.Select):
    def __init__(self, sessions: list[OrmAccount], action: str):
        self.label_map = {
            session.session_id: session.name_session for session in sessions
        }

        options = [
            discord.SelectOption(label=label, value=value)
            for value, label in self.label_map.items()
        ]
        super().__init__(placeholder="Выберите сессию", options=options)
        self.action = action  # "set" / "delete" / "reset" / "get"

    async def callback(self, interaction: discord.Interaction):
        selected = self.values[0]
        service = ProcessingSession()
        label = self.label_map[selected]
        await interaction.response.defer(thinking=True)
        # Пример обработки разных действий
        if self.action == "set":
            await service.set_primary_session(selected)
            await interaction.followup.send(
                f"✅ Сессия `{label}` установлена как основная", ephemeral=True
            )

        elif self.action == "delete":
            await service.delete_session(selected)
            await interaction.followup.send(
                f"🗑️ Сессия `{label}` удалена", ephemeral=True
            )

        elif self.action == "reset":
            await service.reset_session(selected)
            await interaction.followup.send(
                f"📦 Сессия сброшена `{label}`", ephemeral=True
            )
        elif self.action == "get":
            embed = await service.get(session_id=selected)
            await interaction.followup.send(embed=embed)


class SessionView(discord.ui.View):
    def __init__(self, sessions: list[OrmAccount], action: str):
        super().__init__(timeout=60)
        self.add_item(SessionDropdown(sessions, action))

    @classmethod
    async def create(cls, discord_id, action: str):
        """Action Literal["set", "delete", "reset", "get"]"""
        sessions = await ProcessingSession().get_sessions(discord_id)
        return cls(sessions, action)
