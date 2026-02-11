# helpers to generate text embeddings
from portable_brain.monitoring.embedding_manager.embedding_repository import EmbeddingRepository
from portable_brain.common.db.crud.memory.text_embeddings_crud import save_text_embedding_log
from portable_brain.common.logging.logger import logger

# TODO: to be updated, minimal test for now
class EmbeddingGenerator(EmbeddingRepository):
    """
    Helper to generate and persist text embeddings for observation nodes.
    NOTE: inherits from ObservationRepository for dependencies.
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
        """
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
