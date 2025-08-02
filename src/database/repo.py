from src.error.exception import AccountError
from src.database.orm_model import OrmUserDiscord, OrmUserTelegram, OrmAccount
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_, update
from sqlalchemy.orm import joinedload


class Repository:
    def __init__(self, session):
        self.session: AsyncSession = session

    async def get_user_discord(self, discord_id: int) -> OrmUserDiscord | None:
        stmt = (
            select(OrmUserDiscord)
            .options(joinedload(OrmUserDiscord.accounts))
            .where(OrmUserDiscord.discord_id == discord_id)
        )

        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def create_user_discord(self, discord_id: int, name) -> OrmUserDiscord:
        user = OrmUserDiscord(discord_id=discord_id, name=name)
        self.session.add(user)
        return user

    async def get_user_telegram(self, telegram_id: int) -> OrmUserTelegram | None:
        stmt = (
            select(OrmUserTelegram)
            .options(joinedload(OrmUserTelegram.accounts))
            .where(OrmUserTelegram.telegram_id == telegram_id)
        )
        result = await self.session.execute(stmt)
        return result.unique().scalar_one_or_none()

    async def create_user_telegram(
        self, telegram_id: int, name: str
    ) -> OrmUserTelegram:
        user = OrmUserTelegram(telegram_id=telegram_id, name=name)
        self.session.add(user)
        return user

    async def add_account(
        self,
        session_id: str,
        player_id: int,
        name: str,
        region: str,
        discord_user_id: int | None = None,
        telegram_user_id: int | None = None,
        name_session: str | None = None,
        primary: bool = False,
        access_token: str | None = None,
        **kwargs,
    ):
        account = OrmAccount(
            session_id=session_id,
            player_id=player_id,
            name=name,
            region=region,
            discord_user_id=discord_user_id,
            telegram_user_id=telegram_user_id,
            name_session=name_session,
            primary=primary,
            access_token=access_token,
        )
        account.validate_user()
        self.session.add(account)

    async def get_primary_account_by_user_id(
        self, type: str, _id: int
    ) -> OrmAccount | None:
        if type == "discord":
            stmt = select(OrmAccount).where(
                and_(OrmAccount.discord_user_id == _id, OrmAccount.primary == True)
            )
        else:
            stmt = select(OrmAccount).where(
                and_(OrmAccount.telegram_user_id == _id, OrmAccount.primary == True)
            )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def set_primary_account(self, session_id: str):
        stmt = select(OrmAccount).where(OrmAccount.session_id == session_id)
        result = await self.session.execute(stmt)
        result = result.scalar_one()
        primary_ac = await self.get_primary_account_by_user_id(
            "discord" if result.discord_user_id else "telegram",
            (result.telegram_user_id or result.discord_user_id),
        )
        if not primary_ac:
            raise AccountError()
        primary_ac.primary = False
        stmt = (
            update(OrmAccount)
            .where(OrmAccount.session_id == session_id)
            .values(primary=True)
        )
        await self.session.execute(stmt)

    async def delete_account(self, session_id: str):
        stmt = delete(OrmAccount).where(OrmAccount.session_id == session_id)
        result = await self.session.execute(stmt)


async def crate_user_discord(self): ...
async def crate_user_telegram(self): ...


async def add_account(self): ...


async def delete_account(self): ...


async def get_account_by_user_id(self): ...


async def get_user_by_discord_id(self): ...


async def get_user_by_telegram_id(self): ...
