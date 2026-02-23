# helpers to generate text embeddings
import uuid
from typing import Optional
from portable_brain.monitoring.embedding_manager.embedding_repository import EmbeddingRepository
from portable_brain.common.db.crud.memory.text_embeddings_crud import save_text_embedding_log
from portable_brain.common.db.crud.memory.people_crud import save_person_relationship
from portable_brain.common.logging.logger import logger

# TODO: to be updated, minimal test for now
class EmbeddingGenerator(EmbeddingRepository):
    """
    Helper to generate and persist text embeddings for observation nodes.
    NOTE: inherits from EmbeddingRepository for dependencies.

    TODO: connect w/ actual pipeline to generate embedding from observation and store into db
    """

    async def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generates embedding vectors for a list of text strings.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (one per input text)
        """
        embeddings = await self.embedding_client.aembed_text(texts)
        logger.info(f"Generated {len(embeddings)} embeddings")
        return embeddings

    async def generate_and_save_embedding(
        self,
        observation_id: str,
        observation_text: str,
    ) -> list[float]:
        """
        Generates an embedding for a single observation text and persists it to the DB.

        Args:
            observation_id: Unique identifier for the observation
            observation_text: The observation text to embed and store

        Returns:
            The embedding vector

        NOTE: this is just a temporary helper for convenience during testing.
        In the future, should invoke generator and saver separately.
        """
        # embeds only one observation, so take the first element from list of size 1
        embeddings = await self.embedding_client.aembed_text([observation_text])
        embedding_vector = embeddings[0]

        await save_text_embedding_log(
            observation_id=observation_id,
            observation_text=observation_text,
            embedding_vector=embedding_vector,
            main_db_engine=self.main_db_engine,
        )

        logger.info(f"Generated and saved embedding for observation {observation_id}")
        return embedding_vector

    async def generate_and_save_person_embedding(
        self,
        first_name: str,
        relationship_description: str,
        last_name: Optional[str] = None,
        person_id: Optional[str] = None,
        platform: Optional[str] = None,
        platform_handle: Optional[str] = None,
    ) -> list[float]:
        """
        Generates an embedding for a relationship description and persists the
        interpersonal relationship record to the DB.

        Args:
            first_name: Person's first name
            relationship_description: Natural language description of the relationship
            last_name: Person's last name (optional for mononyms)
            person_id: Unique identifier — defaults to a random UUID if not provided
            platform: Communication platform e.g. "instagram", "email" (optional)
            platform_handle: Handle on that platform e.g. "@sarah" (optional)

        Returns:
            The relationship embedding vector
        """
        person_id = person_id or str(uuid.uuid4())
        full_name = f"{first_name} {last_name}".strip() if last_name else first_name

        embeddings = await self.embedding_client.aembed_text([relationship_description])
        relationship_vector = embeddings[0]

        await save_person_relationship(
            person_id=person_id,
            first_name=first_name,
            last_name=last_name,
            full_name=full_name,
            relationship_description=relationship_description,
            relationship_vector=relationship_vector,
            platform=platform,
            platform_handle=platform_handle,
            main_db_engine=self.main_db_engine,
        )

        logger.info(f"Generated and saved person embedding for '{full_name}' (id={person_id})")
        return relationship_vector
