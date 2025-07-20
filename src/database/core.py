from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.orm_model import Base
from src.config.settings import settings
from contextlib import asynccontextmanager
from loguru import logger as log


engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.DATABASE.SQLITE_PATH}", echo=True
)


SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, autoflush=False)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
            log.debug("✅ Коммит выполнен")
        except Exception as e:
            await session.rollback()
            log.warning(f"⏪ Rollback из-за ошибки: {e}", exc_info=True)
            raise e
        finally:
            await session.close()
            log.debug("🔒 Сессия закрыта")


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
