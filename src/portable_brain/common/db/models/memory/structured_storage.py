# canonical ORM representation of structured, relational, memory in "normal" db
from portable_brain.common.db.models.base import MainDB_Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, Text, ForeignKey, Index, Computed
from sqlalchemy.dialects.postgresql import TSVECTOR
from datetime import datetime
from typing import Optional

class StructuredMemory(MainDB_Base):
    """
    Structured memory data structure to store semantic observation nodes as entities.
    No explicit, semantic relationship between nodes (no edges), but holds type of edge.

    Retrieval possibilities:
    - Entity-based: Query by source_entity_id or target_entity_id
    - Temporal: Query by created_at, time_of_day
    - Memory type: Query by memory_type (long_term_people, short_term_preferences, etc.)
    - Relevance: Order by computed relevance_score (importance * recurrence)
    - Full-text: Search node_content using PostgreSQL FTS

    TODO: subject to change as memory storage evolves
    """
    __tablename__ = "structured_memory"

    # Primary key
    id: Mapped[str] = mapped_column(String, primary_key=True)

    # Memory classification
    memory_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Options: "long_term_people", "long_term_preferences", "short_term_preferences", "short_term_content"

    # Core observation content
    node_content: Mapped[str] = mapped_column(Text, nullable=False)
    # Semantic description of the observed pattern

    edge_type: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    # Relationship type (e.g., "communicates_with", "uses_app", "prefers")

    # Entity indexing - THE KEY TO FAST RETRIEVAL
    source_entity_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Primary entity this observation is about (e.g., "com.instagram.android", "me")

    source_entity_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Type of source entity: "app", "user", "location", "device"

    target_entity_id: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    # Secondary entity (e.g., person name, app name)

    target_entity_type: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    # Type of target entity: "person", "app", "content_source"

    # Temporal metadata
    created_at: Mapped[datetime] = mapped_column(DateTime, index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now, nullable=False)

    time_of_day: Mapped[Optional[str]] = mapped_column(String, index=True, nullable=True)
    # "morning", "work_hours", "evening", "night" - for temporal pattern queries

    # Relevance scoring
    recurrence: Mapped[int] = mapped_column(Integer, default=1, index=True, nullable=False)
    # Number of times this pattern has been observed

    importance: Mapped[float] = mapped_column(Float, index=True, nullable=False)
    # Importance score (0.0 - 1.0)

    relevance_score: Mapped[float] = mapped_column(
        Float,
        Computed("importance * recurrence", persisted=True),
        index=True
    )
    # Computed relevance for ranking

    # Full-text search on observation content
    search_vector: Mapped[Optional[str]] = mapped_column(
        TSVECTOR,
        Computed("to_tsvector('english', node_content)", persisted=True)
    )

    # Relationships to linked tables
    entities: Mapped[list["ObservationEntity"]] = relationship(
        back_populates="observation",
        cascade="all, delete-orphan"
    )

    contexts: Mapped[list["ObservationContext"]] = relationship(
        back_populates="observation",
        cascade="all, delete-orphan"
    )

    # Composite indexes for common query patterns
    __table_args__ = (
        # Query: "Get all observations about a specific app"
        Index('idx_source_memory', 'source_entity_id', 'memory_type'),

        # Query: "Get all observations between two entities"
        Index('idx_source_target', 'source_entity_id', 'target_entity_id'),

        # Query: "Get recent observations of a specific type"
        Index('idx_memory_recency', 'memory_type', 'created_at'),

        # Query: "Get most relevant observations"
        Index('idx_relevance', 'relevance_score', 'created_at'),

        # Query: "Get observations by source entity type"
        Index('idx_source_entity_type', 'source_entity_type', 'source_entity_id'),

        # Query: "Get temporal patterns"
        Index('idx_temporal', 'time_of_day', 'source_entity_id'),

        # Full-text search index
        Index('idx_search_vector', 'search_vector', postgresql_using='gin'),
    )

class ObservationEntity(MainDB_Base):
    """
    Junction table for many-to-many entity relationships.
    Allows querying observations by ANY mentioned entity, not just source/target.

    Example use case:
    - Find all observations mentioning "sarah_smith" (as source, target, or mentioned)
    - Find all observations involving Instagram (as platform, source, or context)
    """
    __tablename__ = "structured_observation_entities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    observation_id: Mapped[str] = mapped_column(ForeignKey("structured_memory.id"), index=True, nullable=False)

    entity_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # "person", "app", "location", "content_source", "workspace", "channel"

    entity_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # Actual identifier (e.g., "sarah_smith", "com.instagram.android")

    role: Mapped[str] = mapped_column(String, nullable=False)
    # "source", "target", "mentioned", "platform"

    observation: Mapped["StructuredMemory"] = relationship(back_populates="entities")

    __table_args__ = (
        # Query: "Find all observations mentioning sarah_smith"
        Index('idx_entity_lookup', 'entity_type', 'entity_id'),

        # Query: "Get all entities in an observation"
        Index('idx_entity_obs', 'entity_id', 'observation_id'),
    )

class ObservationContext(MainDB_Base):
    """
    Stores additional contextual metadata for observations.
    Enables querying by app context, temporal patterns, location, etc.

    Example contexts:
    - {"context_type": "app", "context_value": "com.instagram.android"}
    - {"context_type": "time_of_day", "context_value": "morning"}
    - {"context_type": "location", "context_value": "home"}
    - {"context_type": "workspace", "context_value": "TechCorp"}
    - {"context_type": "day_of_week", "context_value": "monday"}
    """
    __tablename__ = "structured_observation_contexts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    observation_id: Mapped[str] = mapped_column(ForeignKey("structured_memory.id"), index=True, nullable=False)

    context_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    # "app", "time_of_day", "location", "workspace", "channel", "day_of_week"

    context_value: Mapped[str] = mapped_column(String, index=True, nullable=False)

    observation: Mapped["StructuredMemory"] = relationship(back_populates="contexts")

    __table_args__ = (
        # Query: "Find observations in morning time"
        Index('idx_context_lookup', 'context_type', 'context_value'),

        # Query: "Get all contexts for an observation"
        Index('idx_context_obs', 'observation_id', 'context_type'),
    )
