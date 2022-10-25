from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from core.config import app_config

engine = create_async_engine(app_config.DATABASE_URL, echo=False, future=True)
sync_engine = create_engine(app_config.SYNC_DATABASE_URL, echo=False)


def _get_session():
    return sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


def _get_sync_session():
    return Session(sync_engine)


async def get_session() -> AsyncSession:
    async_session = _get_session()
    async with async_session() as session:
        yield session


async def get_sync_session() -> Session:
    session = _get_sync_session()
    try:
        yield session
    finally:
        session.close()
