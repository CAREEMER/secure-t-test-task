from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, create_engine

from core.config import app_config

sync_engine = create_engine(app_config.SYNC_DATABASE_URL, echo=False)
engine = create_async_engine(app_config.DATABASE_URL, echo=False, future=True)


@lru_cache()
def get_sync_session():
    return Session(sync_engine)


@lru_cache()
def get_async_session():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async_session = get_async_session()
    async with async_session() as session:
        yield session
