# observation DTOs
from pydantic import BaseModel
from enum import Enum
from typing import Optional, Union
from datetime import datetime

class BehaviorType(str, Enum):
    """
    Classification for common behavior types, helps to identify node structure in memory.
    """
    RECURRING_TIME = "recurring_time"
    RECURRING_SEQUENTIAL = "recurring_sequential"
    TARGET_CLARIFICATION = "target_classification"
    UNKNOWN = "unknown"
    # TODO: add more

class MemoryType(str, Enum):
    """
    Classification for which memory data structure this observation is associated with.
    - Default classification is current session.
    """
    LONG_TERM_PEOPLE = "long_term_people" # inter-personal relationships
    LONG_TERM_PREFERENCES = "long_term_preferences" # user preferences, or user-object relationships
    SHORT_TERM_CONTENT = "short_term_content" # short term content context storage
    # for now, current session is simply metadata pulled without memory
    CURRENT_SESSION = "current_session" # current session context
    # TODO: open to expansion

class LongTermPeopleObservation(BaseModel):
    """
    Observation for inter-personal relationships, which is a long term memory.
    """
    id: str # unique identifier
    memory_type: MemoryType = MemoryType.LONG_TERM_PEOPLE
    target_id: str # id of the target person, as a unique identifier
    edge: str # semantic classification of the node type w.r.t. target
    node: str # semantic description of the relationship/observation
    importance: float
    created_at: datetime # used to dynamically calculate recency
    primary_communication_channel: str

class LongTermPreferencesObservation(BaseModel):
    """
    Observation for user preferences, which is a long term memory.
    """
    id: str # unique identifier
    memory_type: MemoryType = MemoryType.LONG_TERM_PREFERENCES
    target_id: str # id of the target object (e.g. app), as a unique identifier
    edge: str # semantic classification of the node type w.r.t. target
    node: str # semantic description of the relationship/observation
    importance: float
    created_at: datetime # used to dynamically calculate recency

class ShortTermContentObservation(BaseModel):
    """
    Observation for short term content context, which is a short term memory.
    """
    id: str # unique identifier
    memory_type: MemoryType = MemoryType.SHORT_TERM_CONTENT
    source_id: str # unique identifier of the source of the content
    content_id: str # unique identifier of the content 
    node: str # semantic description of the content
    importance: float
    created_at: datetime # used to dynamically calculate recency / update node in memory

# class Observation(BaseModel):
#     """
#     High-level inference of user behavior, derived from a union of low-level actions.
#     Each observation holds semantic inference and additional metadata.
#     NOTE: shared across agent-executed action observation and user-inferred observations
#     """
#     description: str # semantic inference
#     importance: float # temporarily defined here
#     timestamp: datetime
#     behavior_type: BehaviorType # type of behavior, like recurring w.r.t. time/sequence of actions

Observation = Union[
    LongTermPeopleObservation,
    LongTermPreferencesObservation,
    ShortTermContentObservation
    # TODO: add more
]
