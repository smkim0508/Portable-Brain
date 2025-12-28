from functools import lru_cache
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession, AsyncEngine
from contextlib import asynccontextmanager 
from typing import AsyncGenerator
import asyncio
from pydantic import BaseModel
# supabase connector

class DBSettings(BaseModel):
    """
    Portable DB settings class used to pass in configs for generic Postgres connection
    """
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800
    USER: str
    PW: str
    INSTANCE: str
    NAME: str

@asynccontextmanager
async def create_db_engine_context(
    db_settings: DBSettings
) -> AsyncGenerator[AsyncEngine, None]:
    """
    A generic, reusable asynchronous context manager for creating Supabase db engine and disposing connection.
    For now, only used for main db, but can be expanded.
    """ 
    # Use create_async_connector to ensure the Connector uses the current event loop.
    loop = asyncio.get_running_loop()
    async with Connector(loop=loop) as connector: # TODO: connect with supabase
    
        # Create the SQLAlchemy engine using the connector
        engine = create_async_engine(
            "postgresql+asyncpg://",
            async_creator=lambda: connector.connect_async(
                db_settings.INSTANCE, "asyncpg", user=db_settings.USER, password=db_settings.PW, db=db_settings.NAME
            ),
            pool_size=db_settings.POOL_SIZE,
            max_overflow=db_settings.MAX_OVERFLOW,
            pool_timeout=db_settings.POOL_TIMEOUT,
            pool_recycle=db_settings.POOL_RECYCLE,
            echo=False,
        )
        
        try:
            # Yield the engine for use within the `async with` block
            yield engine
        finally:
            # This cleanup is guaranteed to run when the `async with` block is exited
            await engine.dispose()

    """
    NOTE: Since the engine is now managed by the context manager, we create the session maker
    inside the `async with` block where the engine is available.
    Reusable session maker factory.
    """

def get_async_session_maker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """
    Returns a session maker for the given engine.
    """
    return async_sessionmaker(engine, expire_on_commit=False)