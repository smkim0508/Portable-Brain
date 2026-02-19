# output types for execution agent

from pydantic import BaseModel, Field
from typing import Optional

class ExecutionLLMOutput(BaseModel):
    """
    Structured output from the execution agent after attempting a device command.
    Consumed by the orchestrator to determine success or trigger re-retrieval.
    """
    success: bool = Field(description="Whether the execution completed successfully.")
    result_summary: str = Field(description="Plain language summary of what happened on the device.")
    failure_reason: Optional[str] = Field(default=None, description="Why execution failed. None if successful.")
    missing_information: Optional[str] = Field(default=None, description="Specific information that was missing and prevented successful execution. None if successful.")
