# test route to retrieve relevant memory context from RetrievalAgent

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from portable_brain.common.logging.logger import logger

# agents
from portable_brain.agent_service.retrieval_agent.agent import RetrievalAgent
# droidrun
from portable_brain.common.services.droidrun_tools.droidrun_client import DroidRunClient

# dependencies
from portable_brain.core.dependencies import (
    get_retrieval_agent,
    get_droidrun_client
)

# request models
from portable_brain.api.request_models.tests import ToolCallRequest

# settings
from portable_brain.config.app_config import get_service_settings

settings = get_service_settings()

router = APIRouter(prefix="/retrieval-test", tags=["Agent Tests"])

@router.post("/retrieval-test")
async def test_tool_call(
    request: ToolCallRequest,
    retrieval_agent: RetrievalAgent = Depends(get_retrieval_agent)
):
    """
    Test route: retrieves relevant memory context from RetrievalAgent.
    """
    # NOTE: only fetches from text log memory
    result = await retrieval_agent.test_retrieve(request.user_request)
    # logger.info(f"Retrieval test result: {result}")
    return {"result": result}
