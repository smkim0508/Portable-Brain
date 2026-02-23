# CRUD for interpersonal_relationships memory
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import select, func
from portable_brain.common.db.models.memory.people import InterpersonalRelationship
from portable_brain.common.db.session import get_async_session_maker
from portable_brain.common.logging.logger import logger
from datetime import datetime
from typing import Optional

async def save_person_relationship(
    person_id: str,
    first_name: str,
    full_name: str,
    relationship_description: str,
    relationship_vector: list[float],
    main_db_engine: AsyncEngine,
    last_name: Optional[str] = None,
    platform: Optional[str] = None,
    platform_handle: Optional[str] = None,
    created_at: Optional[datetime] = None,
) -> None:
    """
    Persist a new interpersonal relationship record to the database.
    The caller is responsible for generating the embedding vector before calling this.

    Args:
        person_id: Unique identifier for this person record
        first_name: Person's first name
        full_name: Denormalized full name used for trigram GIN index lookup
        relationship_description: Natural language description of the relationship
        relationship_vector: Pre-computed embedding vector for relationship_description
        main_db_engine: Async database engine
        last_name: Person's last name (optional for mononyms)
        platform: Communication platform e.g. "instagram", "email" (optional)
        platform_handle: Handle on that platform e.g. "@sarah" (optional)
        created_at: Timestamp (defaults to now)
    """
    session_maker = get_async_session_maker(main_db_engine)
    now = created_at or datetime.now()

    try:
        async with session_maker() as session:
            record = InterpersonalRelationship(
                id=person_id,
                first_name=first_name,
                last_name=last_name,
                full_name=full_name,
                platform=platform,
                platform_handle=platform_handle,
                relationship_description=relationship_description,
                relationship_vector=relationship_vector,
                created_at=now,
                updated_at=now,
            )
            session.add(record)
            await session.commit()
            logger.info(f"Saved person relationship for '{full_name}' (id={person_id})")
    except Exception as e:
        logger.error(f"Failed to save person relationship for '{full_name}': {e}")
        raise


async def get_person_by_id(
    person_id: str,
    main_db_engine: AsyncEngine,
) -> Optional[InterpersonalRelationship]:
    """
    Retrieve an interpersonal relationship record by its primary key.

    Args:
        person_id: The person's unique identifier
        main_db_engine: Async database engine

    Returns:
        InterpersonalRelationship or None if not found
    """
    session_maker = get_async_session_maker(main_db_engine)

    try:
        async with session_maker() as session:
            stmt = select(InterpersonalRelationship).where(InterpersonalRelationship.id == person_id)
            result = await session.execute(stmt)
            return result.scalar_one_or_none()
    except Exception as e:
        logger.error(f"Failed to get person by id '{person_id}': {e}")
        raise


async def find_person_by_name(
    name: str,
    main_db_engine: AsyncEngine,
    similarity_threshold: float = 0.3,
    limit: int = 10,
) -> list[tuple[InterpersonalRelationship, float]]:
    """
    Fuzzy name lookup using PostgreSQL trigram similarity (pg_trgm).
    Results are ordered by descending similarity score.

    Args:
        name: The name to search for (handles typos, partial names, nicknames)
        main_db_engine: Async database engine
        similarity_threshold: Minimum similarity score 0–1 to include a result (default 0.3)
        limit: Maximum number of results to return

    Returns:
        List of tuples (InterpersonalRelationship, similarity_score)
    """
    session_maker = get_async_session_maker(main_db_engine)
    similarity = func.similarity(InterpersonalRelationship.full_name, name)

    try:
        async with session_maker() as session:
            stmt = (
                select(
                    InterpersonalRelationship,
                    similarity.label("similarity_score"),
                )
                .filter(similarity > similarity_threshold)
                .order_by(similarity.desc())
                .limit(limit)
            )
            result = await session.execute(stmt)
            rows = result.all()
            logger.info(f"Found {len(rows)} people matching name '{name}'")
            return [(row[0], row[1]) for row in rows]
    except Exception as e:
        logger.error(f"Failed to find person by name '{name}': {e}")
        raise


async def find_similar_relationships(
    query_vector: list[float],
    limit: int,
    main_db_engine: AsyncEngine,
) -> list[tuple[InterpersonalRelationship, float]]:
    """
    Find the most semantically similar relationship descriptions using cosine distance.

    Args:
        query_vector: The query embedding vector
        limit: Maximum number of results to return
        main_db_engine: Async database engine

    Returns:
        List of tuples (InterpersonalRelationship, cosine_distance)
    """
    session_maker = get_async_session_maker(main_db_engine)

    try:
        async with session_maker() as session:
            stmt = (
                select(
                    InterpersonalRelationship,
                    InterpersonalRelationship.relationship_vector.cosine_distance(query_vector).label("distance")
                )
                .order_by("distance")
                .limit(limit)
            )
            result = await session.execute(stmt)
            rows = result.all()
            logger.info(f"Found {len(rows)} similar person relationships")
            return [(row[0], row[1]) for row in rows]
    except Exception as e:
        logger.error(f"Failed to find similar relationships: {e}")
        raise
