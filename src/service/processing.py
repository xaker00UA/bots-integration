from functools import wraps
import inspect

from src.database.repo import Repository
from src.database.core import get_session
from src.service.api import APIBackendServer
from src.error.exception import *
from src.discord_bot_stats.utils.message_generation import generate_player_stats_embed
from src.config.logging import discord_logger as log
from loguru import logger as log

from src.telegram_bot_stats.utils.message_generation import GenerateStatsMessage


def log_call(method):
    @wraps(method)
    async def wrapper(*args, **kwargs):
        sig = inspect.signature(method)
        bound = sig.bind(*args, **kwargs)
        bound.apply_defaults()

        caller = args[0].__class__.__name__
        log.debug(f"[{caller}.{method.__name__}] called with: {dict(bound.arguments)}")
        return await method(*args, **kwargs)

    return wrapper


class ProcessingSession:
    def __init__(self) -> None:
        self.api = APIBackendServer()

    @log_call
    async def create_session(
        self,
        user_name: str,
        name: str,
        region: str,
        discord_id: int,
        name_session: str | None,
    ):
        async with get_session() as session:
            user = await Repository(session).get_user_discord(discord_id)
            primary = False
            if not user:
                await Repository(session).create_user_discord(
                    discord_id=discord_id, name=user_name
                )
                primary = True
            else:
                if len(user.accounts) >= 5:
                    raise ToManySessions()
            user = await self.api.add_session(name, region)
            await Repository(session).add_account(
                **user,
                discord_user_id=discord_id,
                name_session=name_session,
                primary=primary,
            )

    async def get_sessions(self, _id: int, type: str = "discord"):
        async with get_session() as session:
            if type == "discord":
                res = await Repository(session).get_user_discord(_id)
            else:
                res = await Repository(session).get_user_telegram(_id)
            if not res:
                raise UserError()
            if len(res.accounts) == 0:
                raise AccountError()
            return res.accounts

    @log_call
    async def reset_session(self, session_id: str):
        await self.api.reset_session(session_id)

    @log_call
    async def delete_session(self, session_id: str):
        async with get_session() as session:
            await self.api.delete_session(session_id)
            await Repository(session).delete_account(session_id)

    @log_call
    async def set_primary_session(self, session_id: str):
        async with get_session() as session:
            try:
                await Repository(session).set_primary_account(session_id)
            except Exception as e:
                log.exception(e)

    @log_call
    async def get(
        self,
        /,
        name: str | None = None,
        region: str | None = None,
        session_id: str | None = None,
        type: str | None = None,
        user_id: int | None = None,
    ):
        if session_id:
            response = await self.api.get_session_by_id(session_id)
        if name and region:
            response = await self.api.get_session_by_name_and_region(name, region)
        if type and user_id:
            async with get_session() as session:
                primary_ses = await Repository(session).get_primary_account_by_user_id(
                    type, user_id
                )
                if not primary_ses:
                    raise AccountError()
                response = await self.api.get_session_by_id(primary_ses.session_id)
        embed = generate_player_stats_embed(response)
        return embed

    @log_call
    async def get_top_rating(self):
        data = await self.api.get_top_rating()
        return data


class TelegramProcessing(ProcessingSession):
    def __init__(self) -> None:
        self.api = APIBackendServer(type="telegram")
        self.service_generate_message = GenerateStatsMessage()

    @log_call
    async def create_session(
        self,
        user_name: str,
        name: str,
        region: str,
        telegram_id: int,
        name_session: str | None,
    ):
        async with get_session() as session:
            user = await Repository(session).get_user_telegram(telegram_id)
            primary = False
            if not user:
                await Repository(session).create_user_telegram(
                    telegram_id=telegram_id, name=user_name
                )
                primary = True
            else:
                if len(user.accounts) >= 5:
                    raise ToManySessions()
            user = await self.api.add_session(name, region)
            await Repository(session).add_account(
                **user,
                telegram_user_id=telegram_id,
                name_session=name_session,
                primary=primary,
            )

    async def get_sessions(self, _id, type="telegram"):
        return await super().get_sessions(_id, type)

    @log_call
    async def get(
        self,
        /,
        name: str | None = None,
        region: str | None = None,
        session_id: str | None = None,
        type: str | None = None,
        user_id: int | None = None,
    ) -> str:
        if session_id:
            response = await self.api.get_session_by_id(session_id)
        if name and region:
            response = await self.api.get_session_by_name_and_region(name, region)
        if type and user_id:
            async with get_session() as session:
                primary_ses = await Repository(session).get_primary_account_by_user_id(
                    type, user_id
                )
                if not primary_ses:
                    raise AccountError()
                response = await self.api.get_session_by_id(primary_ses.session_id)
        text = self.service_generate_message.send_message(response)
        return text

    async def get_top_rating(self):
        data = await super().get_top_rating()
        return self.service_generate_message.top_rating_player(data)
