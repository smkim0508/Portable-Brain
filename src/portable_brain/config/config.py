# main app settings/configs
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from portable_brain.config.settings_mixins import (
    GoogleGenAISettingsMixin,
    MainDBSettingsMixin
)
from portable_brain.common.logging.logger import logger

# Determine which environment we're in. Default to 'dev'.
APP_ENV = os.getenv("APP_ENV", "dev")

# Define the path to the .env file relative to this config file's location.
# This file is in src/rec_service/core/, so we go up two levels to src/rec_service/
SERVICE_ROOT = Path(__file__).resolve().parents[1]
env_file_path = SERVICE_ROOT / f".env.{APP_ENV}"
logger.info(f"APP_ENV: {APP_ENV}")

class CommonSettings(BaseSettings):
    """
    The baseline, default settings that govern common functionalities.
    Universal, low-levell settings and pydantic config for parsing .env files.
    Passed in last to set low priority.
    """
    # This base config ensures that if a service-specific settings class
    # doesn't define its own model_config, it will still have these safe defaults.
    model_config = SettingsConfigDict(env_file_encoding="utf-8", extra="ignore")
    
    # The application environment is the only truly universal setting.
    APP_ENV: str = os.getenv("APP_ENV", "dev")

class MainSettings(
    MainDBSettingsMixin,
    GoogleGenAISettingsMixin,
    CommonSettings # passed in last to set low priority
):
    """
    The main app settings.
    Setting mix-ins are passed in for different services/clients.
    """
    # generic rate limit settings, not tied to any LLM client
    RATE_LIMITS_ENABLED: bool = True

    model_config = SettingsConfigDict(
        env_file=env_file_path, env_file_encoding="utf-8", extra="ignore", env_nested_delimiter="__"
    )
