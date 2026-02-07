# base observation repository holding all necessary dependencies, intiialized in app lifespan
import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient
from portable_brain.common.types.android_apps import AndroidApp
from portable_brain.common.logging.logger import logger

# Canonical DTOs for UI state, inferred action, observations
from portable_brain.monitoring.background_tasks.types.ui_states.ui_state import UIState, UIActivity
from portable_brain.monitoring.background_tasks.types.ui_states.state_changes import UIStateChange, StateChangeSource
from portable_brain.monitoring.background_tasks.types.ui_states.state_change_types import StateChangeType
from portable_brain.monitoring.background_tasks.types.action.action_types import ActionType

# LLM for inference
from portable_brain.common.services.llm_service.llm_client import TypedLLMClient

# main db engine
from sqlalchemy.ext.asyncio import AsyncEngine

class ObservationRepository():
    """
    The absolute base class holding all dependencies required for observation tracking.
    Helper classes will inherit from this class.
    """

    def __init__(self, droidrun_client: DroidRunClient, llm_client: TypedLLMClient, main_db_engine: AsyncEngine):
        self.droidrun_client = droidrun_client
        self.llm_client = llm_client
        self.main_db_engine = main_db_engine
        # TODO: add more dependencies as service expands.
