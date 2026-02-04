# system prompts for creating or updating observation via LLM
from pydantic import BaseModel
from typing import Optional

class ObservationPrompt():
    """
    System prompt for creating or updating observation.
    """
    test_system_prompt = """
    You are a helpful AI assistant that helps users track their preferences, behaviors, and experiences on a device.
    The user's goal is to track their preferences, behaviors, and experiences on a device.
    """

    test_user_prompt = """
    I want to track my preferences, behaviors, and experiences on a device.
    """
