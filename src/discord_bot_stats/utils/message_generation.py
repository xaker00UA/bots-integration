from discord import Colour, Embed

from src.models.model import RestUser
from src.config.logging import discord_logger as log


def generate_player_stats_embed(user: RestUser | str) -> Embed:
    if isinstance(user, str):
        return Embed(title=user, color=Colour.dark_red())
    message = Embed(
        title=f"Сессия игрока: {user.name} {user.region.value}", color=Colour.dark_red()
    )
    message.add_field(name="\u200b", value="\u200b", inline=False)
    if user.general.session is not None and user.general.session.all is not None:

        for tank in user.tanks.session:  # type: ignore
            message.add_field(
                name=f"{tank.name}",
                value=(
                    f"```"
                    f"Уровень: {tank.level}, "
                    f"Боев: {tank.all.battles}, "  # type: ignore
                    f"Побед: {tank.all.winrate}, "  # type: ignore
                    f"Урон: {tank.all.damage}, "  # type: ignore
                    f"Точность: {tank.all.accuracy}, "  # type: ignore
                    f"Выживаемость: {tank.all.survival}, "  # type: ignore
                    f"```"
                ),
                inline=False,
            )

        message.add_field(name="\u200b", value="\u200b", inline=False)

        message.add_field(
            name="Общая сессия в рандоме",
            value=(
                f"```"
                f"Боев: {user.general.session.all.battles}, "
                f"Побед: {user.general.session.all.winrate}, "
                f"Урон: {user.general.session.all.damage}, "
                f"Точность: {user.general.session.all.accuracy}, "
                f"Выживаемость: {user.general.session.all.survival}"
                f"```"
            ),
            inline=False,
        )
        message.add_field(name="\u200b", value="\u200b", inline=False)
    if user.general.session is not None and user.general.session.rating is not None:
        message.add_field(
            name="Статистика по рейтингу",
            value=(
                f"```"
                f"Боев: {user.general.session.rating.battles}, "
                f"Побед: {user.general.session.rating.winrate}, "
                f"Урон: {user.general.session.rating.damage}, "
                f"Точность: {user.general.session.rating.accuracy}, "
                f"Выживаемость: {user.general.session.rating.survival} "
                f"Очки: {user.general.session.rating.score} "
                f"Место: {user.general.session.rating.number}"
                f"```"
            ),
            inline=False,
        )

        message.add_field(name="\u200b", value="\u200b", inline=False)
        message.add_field(
            name="Рейтинг, текущий сезон:",
            value=f"```"
            f"Очки: {user.general.now.rating.score} "  # type: ignore
            f"Место: {user.general.now.rating.number}"  # type: ignore
            f"```",
            inline=False,
        )
    if len(message) > 6000:
        log.bind(player_name=user.name).error("Слишком длинное сообщение")
        message.clear_fields()
        message.add_field(
            name="",
            value="Слишком много данных для отображения посетите сайт для просмотра статистики",
        )
    return message
