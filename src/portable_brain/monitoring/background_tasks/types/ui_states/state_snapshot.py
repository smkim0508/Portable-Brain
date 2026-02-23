# DTO for a single snapshot of UI state
# this is what's used for observation inference

from pydantic import BaseModel
from typing import Union, Literal, Optional
from enum import Enum
from datetime import datetime, timezone, timedelta
import time

from portable_brain.monitoring.background_tasks.types.ui_states.ui_state import UIActivity

class UIStateSnapshot(BaseModel):
    """
    Canonical representation of a single UI State Snapshot.
    - Holds only essential information to inference an observation via LLM
    """
    formatted_text: str # cleaned, formatted text model of UI state
    activity: UIActivity # NOTE: not explicitly provided in formatted_text
    package: str # already part of formatted_text, but here for filtering
    timestamp: datetime
    is_app_switch: bool = False
    app_switch_info: Optional[str] = None # if is_app_switch is True, carries a short description of app 1 -> app 2

    def to_inference_text(self) -> str:
        """
        Format this snapshot into the text representation used for LLM observation inference.
        Includes the denoised UI text, activity, and timestamp.
        """
        ts_label = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return (
            f"{self.formatted_text}\n"
            f" • **Activity:** {self.activity.activity_name}\n"
            f" • **Timestamp:** {ts_label}"
        )
