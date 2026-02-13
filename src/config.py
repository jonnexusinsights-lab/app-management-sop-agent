import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration settings."""

    # Project Info
    PROJECT_NAME: str = "app-management-sop-agent"
    VERSION: str = "0.1.0"

    # LLM Configuration (Ollama)
    # Default to localhost for local Ollama instance
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    # Default model is llama3, but can be changed via env var
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3")

    # Deprecated: Google API Key (kept for reference or fallback if needed)
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # Vector DB Configuration (LanceDB)
    LANCEDB_URI: str = "data/lancedb"

    # Observability (LangSmith / Arize)
    LANGCHAIN_TRACING_V2: str = "true"
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
