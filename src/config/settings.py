from enum import Enum
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModeEnum(str, Enum):
    dev = "DEV"
    prod = "PROD"
    test = "TEST"


class TokensSettings(BaseModel):
    TELEGRAM_TOKEN: str
    DISCORD_TOKEN: str


class ServerSettings(BaseModel):
    PROTOCOL: str
    HOST: str
    PORT: int = 80
    PREFIX: str = "api"
    VERSION: str | None = None

    DISCORD_TOKEN: str
    TELEGRAM_TOKEN: str

    @property
    def base_url(self) -> str:
        if self.VERSION is None:
            return f"{self.PROTOCOL}://{self.HOST}:{self.PORT}/{self.PREFIX}"
        return f"{self.PROTOCOL}://{self.HOST}:{self.PORT}/{self.PREFIX}/{self.VERSION}"


class DataBaseSettings(BaseModel):
    SQLITE_PATH: str


class FrontendSettings(BaseModel):
    FRONTEND_URL: str


class AdminSettings(BaseModel):
    TELEGRAM_ADMIN_IDS: list[int] = []
    DISCORD_ADMIN_IDS: list[int] = []


class DiscordAuthSettings(BaseModel):
    CLIENT_ID: int
    CLIENT_SECRET: str
    REDIRECT_URL: str


class AuthSettings(BaseModel):
    DISCORD: DiscordAuthSettings


class Settings(BaseSettings):
    MODE: ModeEnum = ModeEnum.dev

    LOG_LEVEL: str = "INFO"

    TOKENS: TokensSettings

    SERVER: ServerSettings
    FRONTEND: FrontendSettings

    DATABASE: DataBaseSettings

    BOTS: AuthSettings

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".test.env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )


settings = Settings()  # type: ignore
