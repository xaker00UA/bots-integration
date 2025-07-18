from abc import abstractmethod, ABC
from aiohttp import ClientSession, BasicAuth
from src.config.settings import settings
from src.config.logging import (
    discord_logger as discord_log,
    telegram_logger as telegram_log,
)


class OAuth2(ABC):
    ...

    @abstractmethod
    async def get_user_me(self): ...

    @abstractmethod
    async def auth_user(self): ...


class DiscordAuth(OAuth2):
    async def get_user_me(self):
        headers = {
            "Authorization": "Bearer MTIxMTk2NjM2MDMyMjU3MjMzMA.rCb0iFxdJFk92JBbZJwHKYZMcPfR6g"
        }
        async with ClientSession() as session:
            async with session.get(
                "https://discord.com/api/v10/users/@me", headers=headers
            ) as response:
                try:
                    data = await response.json()
                    return data
                except Exception as e:
                    discord_log.exception(e)
                    return None

    async def get_token(self, code):
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.BOTS.DISCORD.REDIRECT_URL,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with ClientSession() as session:
            async with session.post(
                "https://discord.com/api/v10/oauth2/token",
                data=data,
                headers=headers,
                auth=BasicAuth(
                    str(settings.BOTS.DISCORD.CLIENT_ID),
                    settings.BOTS.DISCORD.CLIENT_SECRET,
                ),
            ) as response:
                try:
                    data = await response.json()
                    return data
                except Exception as e:
                    discord_log.exception(e)
                    return None

    async def auth_user(self):
        auth_url = (
            f"https://discord.com/oauth2/authorize?"
            f"client_id={settings.BOTS.DISCORD.CLIENT_ID}&"
            f"redirect_uri={settings.BOTS.DISCORD.REDIRECT_URL}&"
            f"response_type=code&"
            f"scope=identify&"
            f"state={settings.BOTS.DISCORD.CLIENT_SECRET}"
        )
        return auth_url


class TelegramAuth(OAuth2):
    async def get_user_me(self):
        pass

    async def auth_user(self):
        pass
