"""
Application Configuration
Centralizes all environment variables and settings
"""

from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    APP_NAME: str = "SmartResume Analyzer"
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    
    # CORS - Allow frontend origins
    CORS_ORIGINS: str = Field(
        default="http://localhost:5173,http://localhost:3000",
        env="CORS_ORIGINS"
    )
    
    # AI Configuration
    AI_PROVIDER: str = Field(default="openai", env="AI_PROVIDER")  # openai, anthropic, gemini, mock
    AI_API_KEY: str = Field(default="", env="AI_API_KEY")
    AI_MODEL: str = Field(default="gpt-4", env="AI_MODEL")
    AI_MAX_TOKENS: int = Field(default=1000, env="AI_MAX_TOKENS")
    AI_TEMPERATURE: float = Field(default=0.3, env="AI_TEMPERATURE")
    
    # File Upload Limits
    MAX_FILE_SIZE_MB: int = Field(default=10, env="MAX_FILE_SIZE_MB")
    ALLOWED_EXTENSIONS: str = Field(default="pdf", env="ALLOWED_EXTENSIONS")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS_ORIGINS string to list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def allowed_extensions_list(self) -> List[str]:
        """Convert ALLOWED_EXTENSIONS string to list"""
        return [ext.strip() for ext in self.ALLOWED_EXTENSIONS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()
