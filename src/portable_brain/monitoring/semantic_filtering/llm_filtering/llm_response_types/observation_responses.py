# semantic observation LLM responses
from pydantic import BaseModel
from typing import Optional
from enum import Enum

class NewObservationLLMResponse(BaseModel):
    observation_edge: str # relationship between source and target
    observation_node: str # semantic meaning of this observation

class TestObservationLLMResponse(BaseModel):
    observation_edge: str # relationship between source and target
    observation_node: str # semantic meaning of this observation
