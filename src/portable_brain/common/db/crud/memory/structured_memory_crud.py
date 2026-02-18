# crud for structured memory in db

# sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import select, func, text
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import Optional

# Canonical DTOs for db model and observation
from portable_brain.common.db.models.memory.structured_storage import StructuredMemory, ObservationEntity
from portable_brain.monitoring.background_tasks.types.observation.observations import (
    Observation,
    LongTermPeopleObservation,
    LongTermPreferencesObservation,
    ShortTermPreferencesObservation,
    ShortTermContentObservation,
)
# async sessionmaker
from portable_brain.common.db.session import get_async_session_maker
# logger
from portable_brain.common.logging.logger import logger

async def save_observation_to_structured_memory(observation: Observation, main_db_engine: AsyncEngine) -> None:
    """
    Helper to save observation node to structured memory in SQL db.
    - Parses Observation DTO into StructuredMemory ORM based on observation subtype.
    - Uses async sessionmaker to create session.
    - SQLAlchemy allows ORM mapped operations.
    """

    # Parse Observation DTO into StructuredMemory ORM by subtype case work
    if isinstance(observation, LongTermPeopleObservation):
        orm_obj = StructuredMemory(
            id=observation.id,
            memory_type=observation.memory_type.value,
            node_content=observation.node,
            edge_type=observation.edge,
            source_entity_id="me",
            source_entity_type="user",
            target_entity_id=observation.target_id,
            target_entity_type="person",
            created_at=observation.created_at,
            updated_at=observation.created_at,
            importance=observation.importance,
            recurrence=1,
        )
    elif isinstance(observation, (LongTermPreferencesObservation, ShortTermPreferencesObservation)):
        orm_obj = StructuredMemory(
            id=observation.id,
            memory_type=observation.memory_type.value,
            node_content=observation.node,
            edge_type=observation.edge,
            source_entity_id=observation.source_id,
            source_entity_type="app",
            target_entity_id=None,
            target_entity_type=None,
            created_at=observation.created_at,
            updated_at=observation.created_at,
            importance=observation.importance,
            recurrence=observation.recurrence,
        )
    elif isinstance(observation, ShortTermContentObservation):
        orm_obj = StructuredMemory(
            id=observation.id,
            memory_type=observation.memory_type.value,
            node_content=observation.node,
            edge_type=None,
            source_entity_id=observation.source_id,
            source_entity_type="content_source",
            target_entity_id=observation.content_id,
            target_entity_type="content",
            created_at=observation.created_at,
            updated_at=observation.created_at,
            importance=observation.importance,
            recurrence=1,
        )
    else:
        logger.error(f"Unsupported observation type: {type(observation)}")
        raise TypeError(f"Unsupported observation type: {type(observation)}")

    session_maker = get_async_session_maker(main_db_engine)
    try:
        async with session_maker() as session:
            session.add(orm_obj)
            await session.commit()
            logger.info(f"Saved observation {observation.id} to structured memory")
    except Exception as e:
        logger.error(f"Failed to save observation to structured memory: {e}")
        raise


# =====================================================================
# READ operations for memory retrieval
# =====================================================================

async def get_observations_by_memory_type(
    memory_type: str,
    main_db_engine: AsyncEngine,
    source_entity_id: Optional[str] = None,
    target_entity_id: Optional[str] = None,
    limit: int = 10,
) -> list[StructuredMemory]:
    """
    Retrieve observations filtered by memory type, optionally by source/target entity.
    Ordered by relevance_score (importance * recurrence) descending.

    Args:
        memory_type: One of "long_term_people", "long_term_preferences", "short_term_preferences", "short_term_content"
        main_db_engine: Async database engine
        source_entity_id: Optional filter by source entity (app package, "me", etc.)
        target_entity_id: Optional filter by target entity (person name, content id, etc.)
        limit: Max results
    """
    session_maker = get_async_session_maker(main_db_engine)
    try:
        async with session_maker() as session:
            stmt = select(StructuredMemory).where(StructuredMemory.memory_type == memory_type)
            if source_entity_id:
                stmt = stmt.where(StructuredMemory.source_entity_id == source_entity_id)
            if target_entity_id:
                stmt = stmt.where(StructuredMemory.target_entity_id == target_entity_id)
            stmt = stmt.order_by(StructuredMemory.relevance_score.desc()).limit(limit)

            result = await session.execute(stmt)
            return list(result.scalars().all())
    except Exception as e:
        logger.error(f"Failed to get observations by memory type '{memory_type}': {e}")
        raise


async def get_observations_by_entity(
    entity_id: str,
    main_db_engine: AsyncEngine,
    entity_type: Optional[str] = None,
    limit: int = 10,
) -> list[StructuredMemory]:
    """
    Find all observations mentioning a specific entity via the ObservationEntity junction table.
    Searches across all memory types.

    Args:
        entity_id: The entity identifier (e.g., "sarah_smith", "com.instagram.android")
        main_db_engine: Async database engine
        entity_type: Optional filter by entity type ("person", "app", "content_source", etc.)
        limit: Max results
    """
    session_maker = get_async_session_maker(main_db_engine)
    try:
        async with session_maker() as session:
            stmt = (
                select(StructuredMemory)
                .join(ObservationEntity, ObservationEntity.observation_id == StructuredMemory.id)
                .where(ObservationEntity.entity_id == entity_id)
            )
            if entity_type:
                stmt = stmt.where(ObservationEntity.entity_type == entity_type)
            stmt = stmt.order_by(StructuredMemory.relevance_score.desc()).limit(limit)

            result = await session.execute(stmt)
            return list(result.scalars().all())
    except Exception as e:
        logger.error(f"Failed to get observations by entity '{entity_id}': {e}")
        raise


async def fulltext_search_observations(
    search_query: str,
    main_db_engine: AsyncEngine,
    memory_type: Optional[str] = None,
    limit: int = 10,
) -> list[tuple[StructuredMemory, float]]:
    """
    Full-text search across observation node_content using PostgreSQL tsvector.
    Returns (StructuredMemory, fts_rank) tuples ordered by rank descending.

    Args:
        search_query: Natural language search query
        main_db_engine: Async database engine
        memory_type: Optional filter by memory type
        limit: Max results
    """
    session_maker = get_async_session_maker(main_db_engine)
    try:
        async with session_maker() as session:
            ts_query = func.plainto_tsquery("english", search_query)
            stmt = (
                select(
                    StructuredMemory,
                    func.ts_rank(StructuredMemory.search_vector, ts_query).label("rank"),
                )
                .where(StructuredMemory.search_vector.op("@@")(ts_query))
            )
            if memory_type:
                stmt = stmt.where(StructuredMemory.memory_type == memory_type)
            stmt = stmt.order_by(text("rank DESC")).limit(limit)

            result = await session.execute(stmt)
            return [(row[0], row[1]) for row in result.all()]
    except Exception as e:
        logger.error(f"Failed to fulltext search observations: {e}")
        raise


async def get_most_relevant_observations(
    main_db_engine: AsyncEngine,
    memory_type: Optional[str] = None,
    limit: int = 10,
) -> list[StructuredMemory]:
    """
    Retrieve highest-relevance observations (importance * recurrence).
    Optionally filtered by memory type.

    Args:
        main_db_engine: Async database engine
        memory_type: Optional filter by memory type
        limit: Max results
    """
    session_maker = get_async_session_maker(main_db_engine)
    try:
        async with session_maker() as session:
            stmt = select(StructuredMemory)
            if memory_type:
                stmt = stmt.where(StructuredMemory.memory_type == memory_type)
            stmt = stmt.order_by(StructuredMemory.relevance_score.desc()).limit(limit)

            result = await session.execute(stmt)
            return list(result.scalars().all())
    except Exception as e:
        logger.error(f"Failed to get most relevant observations: {e}")
        raise
