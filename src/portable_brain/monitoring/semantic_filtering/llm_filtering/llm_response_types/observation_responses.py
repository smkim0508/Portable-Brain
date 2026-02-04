# semantic observation LLM responses
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class NewObservationLLMResponse(BaseModel):
    """
    LLM response schema for creating a new observation.
    NOTE: the observation edge will be inferenced later when retrieving similar observations.
    """
    observation_node: str # semantic meaning of this observation
    reasoning: str # step-by-step reasoning

class TestObservationLLMResponse(BaseModel):
    """
    Test LLM response schema for creating a new observation.
    """
    observation_edge: str # relationship between source and target
    observation_node: str # semantic meaning of this observation
    reasoning: str
