# ==============================================================================
# AI KARMAYOGI — APPLICATION CONFIGURATION
# Pydantic v2 Settings for MongoDB Atlas + Groq AI
# ==============================================================================

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    # Application Info
    PROJECT_NAME: str = "AI Karmayogi"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = Field(default="development")

    # Security & JWT Tokens
    JWT_SECRET: str
    JWT_REFRESH_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60       # 1 hour
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7          # 7 days

    # MongoDB Atlas
    MONGODB_URI: str = Field(default="mongodb://localhost:27017")
    MONGODB_DATABASE: str = Field(default="ai_karmayogi")

    # LLM Provider ("groq" | "ollama")
    LLM_PROVIDER: str = Field(default="groq")
    GROQ_API_KEY: str = Field(default="")
    GROQ_MODEL: str = Field(default="qwen/qwen3.8-27b")

    # Local AI Engine — Ollama (optional fallback for embeddings + LLM)
    OLLAMA_BASE_URL: str = Field(default="http://localhost:11434")
    EMBEDDING_MODEL: str = "nomic-embed-text"
    LLM_MODEL: str = "qwen3:8b"
    OLLAMA_TIMEOUT_SECONDS: int = 120

    # File Upload Directory
    UPLOAD_DIR: str = Field(default="uploads")
    MAX_UPLOAD_SIZE_MB: int = 50

    # CORS Allowed Origins
    CORS_ORIGINS: list[str] = [
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
