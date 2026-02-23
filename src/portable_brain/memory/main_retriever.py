# the main memory retriever layer/interface for the agent to interact with

from sqlalchemy.ext.asyncio import AsyncEngine
from typing import Optional

from portable_brain.common.db.models.memory.structured_storage import StructuredMemory
from portable_brain.common.db.models.memory.text_embeddings import TextEmbeddingLogs
from portable_brain.common.db.models.memory.people import InterpersonalRelationship
from portable_brain.common.services.embedding_service.text_embedding.dispatcher import TypedTextEmbeddingClient

# structured memory fetch operations
from portable_brain.common.db.crud.memory.structured_memory_crud import (
    get_observations_by_memory_type,
    get_observations_by_entity,
    fulltext_search_observations,
    get_most_relevant_observations,
)
# text embeddings fetch operations
from portable_brain.common.db.crud.memory.text_embeddings_crud import (
    find_similar_embeddings,
    get_embedding_by_observation_id,
)
# people embeddings fetch operations
from portable_brain.common.db.crud.memory.people_crud import (
    get_person_by_id,
    find_person_by_name,
    find_similar_relationships,
)

class MemoryRetriever():
    """
    Implements helper methods for the retriever agent to access different memory.
    Handles internal operations like embedding natural language input to text embeddings, so the agent can freely call without overhead.
    - Tool-called by retriever agent.
    - Wraps CRUD read operations with semantically intuitive method names.
    - Each method specifies the memory type it targets.

    TODO: just baseline right now, memory to be refined.
    """

    def __init__(self, main_db_engine: AsyncEngine, text_embedding_client: TypedTextEmbeddingClient):
        self.main_db_engine = main_db_engine
        self.text_embedding_client = text_embedding_client

    # =====================================================================
    # Structured Memory — Long-Term People (inter-personal relationships)
    # =====================================================================

    async def get_people_relationships(
        self,
        person_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Retrieve long-term people observations (relationships, contacts)."""
        return await get_observations_by_memory_type(
            memory_type="long_term_people",
            main_db_engine=self.main_db_engine,
            target_entity_id=person_id,
            limit=limit,
        )

    # =====================================================================
    # Structured Memory — Long-Term Preferences (recurring user patterns)
    # =====================================================================

    async def get_long_term_preferences(
        self,
        source_app_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Retrieve long-term preference observations (habitual usage patterns)."""
        return await get_observations_by_memory_type(
            memory_type="long_term_preferences",
            main_db_engine=self.main_db_engine,
            source_entity_id=source_app_id,
            limit=limit,
        )

    # =====================================================================
    # Structured Memory — Short-Term Preferences (recent user patterns)
    # =====================================================================

    async def get_short_term_preferences(
        self,
        source_app_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Retrieve short-term preference observations (recent behavioural signals)."""
        return await get_observations_by_memory_type(
            memory_type="short_term_preferences",
            main_db_engine=self.main_db_engine,
            source_entity_id=source_app_id,
            limit=limit,
        )

    # =====================================================================
    # Structured Memory — Short-Term Content (recently viewed media/docs)
    # =====================================================================

    async def get_recent_content(
        self,
        source_id: Optional[str] = None,
        content_id: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Retrieve short-term content observations (recently viewed documents/media)."""
        return await get_observations_by_memory_type(
            memory_type="short_term_content",
            main_db_engine=self.main_db_engine,
            source_entity_id=source_id,
            target_entity_id=content_id,
            limit=limit,
        )

    # =====================================================================
    # Structured Memory — Cross-type queries
    # =====================================================================

    async def get_all_observations_about_entity(
        self,
        entity_id: str,
        entity_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Find all observations mentioning a specific entity across all memory types."""
        return await get_observations_by_entity(
            entity_id=entity_id,
            main_db_engine=self.main_db_engine,
            entity_type=entity_type,
            limit=limit,
        )

    async def search_memories(
        self,
        query: str,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[tuple[StructuredMemory, float]]:
        """Full-text search across observation content. Returns (memory, rank) tuples."""
        return await fulltext_search_observations(
            search_query=query,
            main_db_engine=self.main_db_engine,
            memory_type=memory_type,
            limit=limit,
        )

    async def get_top_relevant_memories(
        self,
        memory_type: Optional[str] = None,
        limit: int = 10,
    ) -> list[StructuredMemory]:
        """Retrieve highest-relevance observations ranked by importance * recurrence."""
        return await get_most_relevant_observations(
            main_db_engine=self.main_db_engine,
            memory_type=memory_type,
            limit=limit,
        )

    # =====================================================================
    # People Embeddings — Interpersonal relationship memory
    # =====================================================================

    async def get_person_by_id(
        self,
        person_id: str,
    ) -> Optional[InterpersonalRelationship]:
        """Look up a specific person's relationship record by their unique ID."""
        return await get_person_by_id(
            person_id=person_id,
            main_db_engine=self.main_db_engine,
        )

    async def find_person_by_name(
        self,
        name: str,
        similarity_threshold: float = 0.3,
        limit: int = 10,
    ) -> list[dict]:
        """
        Fuzzy name lookup using trigram similarity. Handles typos, nicknames, and
        partial names. Returns dicts with full_name, relationship_description, and
        similarity_score, ordered by best match.
        """
        return await find_person_by_name(
            name=name,
            main_db_engine=self.main_db_engine,
            similarity_threshold=similarity_threshold,
            limit=limit,
        )

    async def find_similar_person_relationships(
        self,
        query: str,
        limit: int = 5,
    ) -> list[tuple[InterpersonalRelationship, float]]:
        """
        Semantic search over relationship descriptions using natural language.
        Embeds the query internally and returns (record, cosine_distance) tuples.
        """
        query_vectors = await self.text_embedding_client.aembed_text(text=[query])
        return await find_similar_relationships(
            query_vector=query_vectors[0],
            limit=limit,
            main_db_engine=self.main_db_engine,
        )

    # =====================================================================
    # Text Embeddings — Semantic similarity search
    # =====================================================================

    async def find_semantically_similar(
        self,
        query: str,
        limit: int = 5,
        distance_metric: str = "cosine",
    ) -> list[str]:
        """Semantic search across all embedded observations using natural language. Embeds the query internally. Returns a list of observation text strings ordered by similarity."""
        query_vectors = await self.text_embedding_client.aembed_text(text=[query])
        results = await find_similar_embeddings(
            query_vector=query_vectors[0],
            limit=limit,
            main_db_engine=self.main_db_engine,
            distance_metric=distance_metric,
        )
        return [record.observation_text for record, _ in results]

    async def get_embedding_for_observation(
        self,
        observation_id: str,
    ) -> Optional[TextEmbeddingLogs]:
        """Look up the stored embedding for a specific observation by ID."""
        return await get_embedding_by_observation_id(
            observation_id=observation_id,
            main_db_engine=self.main_db_engine,
        )
