from os import name
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    DeclarativeBase,
    relationship,
    validates,
)
from sqlalchemy.types import BigInteger, String
from datetime import time


class Base(DeclarativeBase):
    pass


class OrmUserDiscord(Base):
    __tablename__ = "users_discord"

    discord_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )
    name: Mapped[str]

    accounts: Mapped[list["OrmAccount"]] = relationship()


class OrmUserTelegram(Base):
    __tablename__ = "users_telegram"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, autoincrement=True
    )

    accounts: Mapped[list["OrmAccount"]] = relationship()


class OrmAccount(Base):
    __tablename__ = "accounts"

    session_id: Mapped[str] = mapped_column(primary_key=True)

    discord_user_id: Mapped[int] = mapped_column(
        ForeignKey("users_discord.discord_id"), nullable=True
    )
    telegram_user_id: Mapped[int] = mapped_column(
        ForeignKey("users_telegram.telegram_id"), nullable=True
    )

    primary: Mapped[bool] = mapped_column(default=False, nullable=False)
    name_session: Mapped[str] = mapped_column(String, default=None, nullable=True)

    player_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    region: Mapped[str] = mapped_column(String, nullable=False)
    access_token: Mapped[str] = mapped_column(String, nullable=True)

    time_auto_session: Mapped[time] = mapped_column(nullable=True)

    def validate_user(
        self,
    ):
        if not (self.discord_user_id or self.telegram_user_id):
            raise ValueError(
                "Аккаунт должен быть связан либо с Discord, либо с Telegram пользователем"
            )
        if not self.name_session:
            self.name_session = self.name
