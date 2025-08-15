import asyncio
import re
from src.models.model import RestUser, TopPlayer
from src.config.settings import settings
from aiohttp import ClientSession
from loguru import logger as log
from datetime import datetime, timedelta


class APIBackendServer:
    def __init__(self, type: str = "discord") -> None:
        self.base_url = settings.SERVER.base_url
        if type == "discord":
            self.header = {"X-Token": settings.SERVER.DISCORD_TOKEN}
        else:
            self.header = {"X-Token": settings.SERVER.TELEGRAM_TOKEN}

    async def get_session_by_name_and_region(
        self, name: str, region: str
    ) -> RestUser | str:
        async with ClientSession() as session:

            async with session.get(
                f"{self.base_url}/{region}/player/period",
                params={
                    "name": name,
                    "start_day": int(
                        (datetime.now() - timedelta(days=1)).timestamp() - 25
                    ),
                    "end_day": int(datetime.now().timestamp()),
                },
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return RestUser.model_validate(data)
                elif response.status in [400, 404]:
                    data = await response.json()
                    if data["detail"].startswith(
                        "Игрок не отслеживается с аргументами"
                    ):
                        return await self.add_player(name, region)
                    if data["detail"].startswith("Игрок не отслеживаеться так долго"):
                        return "Попробуйте завтра снова"
                elif response.status < 500:
                    data = await response.json()
                    return data["detail"]
                else:
                    log.error(await response.json())
                    return "Ошибка сервера"

    async def add_player(self, name: str, region: str):
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{region}/player/get_session",
                params={
                    "name": name,
                },
            ) as response:
                if response.status == 404:
                    data = await response.json()
                    if data["detail"].startswith(
                        "Игрок не отслеживается с аргументами"
                    ):
                        return "Игрок добавлен, попробуйте завтра снова"
                elif response.status < 500:
                    data = await response.json()
                    return data["detail"]
                else:
                    log.error(await response.json())
                    return "Ошибка сервера"

    async def add_session(self, name: str, region: str):
        async with ClientSession(headers=self.header) as session:
            async with session.post(
                f"{self.base_url}/client/", json={"name": name, "region": region}
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    return data
                else:
                    data = await response.json()
                    log.bind(**data).error("Error add session")
                    raise Exception(data["detail"])

    async def delete_session(self, session_id: str):
        async with ClientSession(headers=self.header) as session:
            async with session.delete(
                f"{self.base_url}/client/", json={"session_id": session_id}
            ) as response:
                if response.status == 204:
                    return "Сессия удалена"
                else:
                    return "Ошибка сервера"

    async def get_session_by_id(self, session_id: str):
        async with ClientSession(headers=self.header) as session:
            async with session.get(
                f"{self.base_url}/client/", params={"session_id": session_id}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return RestUser.model_validate(data)
                elif response.status < 500:
                    data = await response.json()
                    return data["detail"]
                else:
                    log.error(await response.json())
                    return "Ошибка сервера"

    async def reset_session(self, session_id: str):
        async with ClientSession(headers=self.header) as session:
            async with session.post(
                f"{self.base_url}/client/reset", json={"session_id": session_id}
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    return data["session_id"]
                log.error(await response.json())

    async def fetch_top(
        self, session: ClientSession, base_url: str, parameter: str
    ) -> list[TopPlayer] | None:
        time = str(int((datetime.now() - timedelta(days=7)).timestamp()))
        params = {
            "limit": str(10),
            "parameter": parameter,
            "start_day": time,
        }
        async with session.get(f"{base_url}/top_players", params=params) as response:
            if response.status == 200:
                data = await response.json()
                return [TopPlayer.model_validate(player) for player in data]
            else:
                log.error(f"{parameter} failed: {await response.text()}")
                return None

    async def get_top_rating(self) -> dict[str, list[TopPlayer] | None]:
        async with ClientSession(headers=self.header) as session:
            metrics = ["battles", "damage", "wins"]
            tasks = [
                self.fetch_top(session, self.base_url, metric) for metric in metrics
            ]
            results = await asyncio.gather(*tasks)
            return dict(zip(metrics, results))

    async def login(self): ...
