import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""

    # Project Info
    PROJECT_NAME: str = "app-management-sop-agent"
    VERSION: str = "0.1.0"

    # LLM Configuration (Gemini)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    MODEL_NAME: str = "models/gemini-2.0-flash"

    # Vector DB Configuration (LanceDB)
    LANCEDB_URI: str = "data/lancedb"

    # Observability (LangSmith / Arize)
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
