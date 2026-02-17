# test route to execute natural language queries on device via droidrun

from fastapi import APIRouter, Depends
from portable_brain.common.logging.logger import logger
from portable_brain.core.dependencies import get_tool_calling_agent
from portable_brain.agent_service.core_agent.tool_calling_agent import ToolCallingAgent

router = APIRouter(prefix="/execution-test", tags=["Tests"])

@router.post("/tool-call-device-name")
async def test_tool_call(
    tool_calling_agent: ToolCallingAgent = Depends(get_tool_calling_agent)
):
    """
    Baseline test: Gemini tool-calls DroidRun's execute_command to answer a simple query.
    """
    result = await tool_calling_agent.test_tool_call()
    logger.info(f"Tool call test result: {result}")
    return {"result": result}
