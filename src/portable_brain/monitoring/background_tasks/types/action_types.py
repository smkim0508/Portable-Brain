from pydantic import BaseModel
from enum import Enum

class ActionType(str, Enum):
    """
    High-level inference for what "action" was done by the user.
    Inferred based on low-level UI change signals.
    TODO: think how to implement action type + action descriptions
    ...since something like app switch should hold signal about which apps were switched.
    """
    pass

class ChangeType(str, Enum):
    """
    Low-level classifications for different UI changes.
    Used to infer high-level actions.
    """
    APP_SWITCH = "app_switch"
    SCREEN_CHANGE = "screen_change"
    MAJOR_LAYOUT_CHANGE = "major_layout_change"
    MINOR_LAYOUT_CHANGE = "minor_layout_change"

def format_action(action_type: ActionType):
    """
    May be used to structure actions in canonical format
    """
    pass