# supported applications
from enum import Enum
from pydantic import BaseModel

class AndroidApp(str, Enum):
    """
    Android Applications Currently Supported for App-specific Tracking.
    """
    INSTAGRAM = "com.instagram.android"
    WHATSAPP = "com.whatsapp"
    SLACK = "com.slack"
    SETTINGS = "com.android.settings"

    