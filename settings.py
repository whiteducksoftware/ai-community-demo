"""Application Settings."""

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Settings for the application"""
    
    github_pat: str = Field(
        validation_alias="GITHUB_PERSONAL_ACCESS_TOKEN"
    )
    
    azure_api_key: str = Field(
        validation_alias="AZURE_API_KEY",
        description="API-Key for the azure models."
    )
    
    azure_api_version: str = Field(
        default="2025-01-01",
        validation_alias="AZURE_API_VERSION",
        description="API-Version of AzureOpenAI to use."
    )
    
    azure_api_base: str = Field(
        validation_alias="AZURE_API_BASE",
        description="BASE_URL for azure deployments."
    )
    
    default_model: str = Field(
        validation_alias="DEFAULT_MODEL",
        description="default model for agents."
    )
    
    default_model_temperature: float = Field(
        default=1.0,
        validation_alias="DEFAULT_MODEL_TEMPERATURE",
        description="Temperature Setting for default model."
    )
    
    default_model_max_tokens: int = Field(
        default=25000,
        validation_alias="DEFAULT_MODEL_MAX_TOKENS",
        description="Max output tokens for default model"
    )
    
    log_level: str = Field(
        default="DEBUG",
        validation_alias="LOG_LEVEL",
        description="Logging level"
    )
    
    log_dir: str = Field(
        default="logs",
        validation_alias="LOGGING_DIR",
        description="Directory for logs."
    )
    
    message_timeout: int = Field(
        default=60*5,
        validation_alias="MESSAGE_TIMEOUT",
        description="Timeout before undelivered messages are being sent to the db."
    )
    
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=str(Path(__file__).parent / ".env"),
        env_file_encoding="utf-8",
    )
    
APP_SETTINGS = AppSettings()