# base embedding repository holding all necessary dependencies, intiialized in app lifespan
# NOTE: initialized in lifespan not request-scope, since embeddings/observations are universal/core.
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient
from portable_brain.common.types.android_apps import AndroidApp
from portable_brain.common.logging.logger import logger

# Embedding client for inference
from portable_brain.common.services.embedding_service.text_embedding import TypedTextEmbeddingClient

# main db engine
from sqlalchemy.ext.asyncio import AsyncEngine

class EmbeddingRepository():
    """
    The absolute base class holding all dependencies required for embedding generation and management.
    Helper classes will inherit from this class.
    """

    def __init__(self, embedding_client: TypedTextEmbeddingClient, main_db_engine: AsyncEngine):
        self.embedding_client = embedding_client
        self.main_db_engine = main_db_engine
        # TODO: add more dependencies as service expands.
