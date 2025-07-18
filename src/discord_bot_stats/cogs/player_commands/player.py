import discord
from src.database.core import get_session
from src.models.model import Region
from src.service.api import APIBackendServer
from src.config.logging import discord_logger as log
from src.discord_bot_stats.utils.message_generation import generate_player_stats_embed
from src.database.repo import Repository
