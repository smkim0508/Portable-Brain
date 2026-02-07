# crud for structured memory in db

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine

# Canonical DTOs for db model and observation
from portable_brain.common.db.models.memory.structured_storage import StructuredMemory
from portable_brain.monitoring.background_tasks.types.observation.observations import Observation
# async sessionmaker
from portable_brain.common.db.session import get_async_session_maker
# logger
from portable_brain.common.logging.logger import logger

async def save_observation_to_structured_memory(observation: Observation, main_db_engine: AsyncEngine) -> None:
    """
    Helper to save observation node to structured memory in SQL db.
    - Uses async sessionmaker to create session.
    - SQLAlchemy allows ORM mapped operations.
    """
    main_session_maker = get_async_session_maker(main_db_engine)
    try:
        async with main_session_maker() as session:
            # TODO: validate the sqlalchemy db logic below
            session.add(observation)
            await session.commit()
            await session.refresh(observation)
    except Exception as e:
        logger.warning(f"Failed to save observation to database: {e}")
