from src.models.model import RestUser
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
                    "start_day": (datetime.now() - timedelta(days=1)).timestamp() - 25,
                    "end_day": datetime.now().timestamp(),
                },
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return RestUser.model_validate(data)
                elif response.status < 500:
                    data = await response.json()
                    return data["detail"]
                else:
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
                    return "Ошибка сервера"

    async def reset_session(self, session_id: str):
        async with ClientSession(headers=self.header) as session:
            async with session.post(
                f"{self.base_url}/client/reset", json={"session_id": session_id}
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    return data["session_id"]

    async def login(self): ...
