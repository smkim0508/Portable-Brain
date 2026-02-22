from pydantic import BaseModel
from typing import Union, Literal, Optional
from enum import Enum

class StateChangeType(str, Enum):
    """
    Classification for whether there is a meaningful state change or not.
    Only APP_SWITCH is determinstic, so this is stored and later appened to snapshot history.
    """
    APP_SWITCH = "app_switch"
    NO_CHANGE = "no_change"
    CHANGED = "changed"

class SemanticStateChangeType(str, Enum):
    """
    Low-level classifications for different UI changes.
    Used to infer high-level actions.
    NOTE: depracted right now, left for potential future usage
    """
    APP_SWITCH = "app_switch"
    SCREEN_CHANGE = "screen_change"
    MAJOR_LAYOUT_CHANGE = "major_layout_change"
    MINOR_LAYOUT_CHANGE = "minor_layout_change"
    SCREEN_NAVIGATION = "screen_navigation"
    CONTENT_NAVIGATION = "content_navigation"
    TEXT_INPUT = "text_input"
    NO_CHANGE = "no_change"
    UNKNOWN = "unknown"
