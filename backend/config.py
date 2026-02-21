"""
AI Travel Guardian+ — Application Configuration
Loads all settings from environment variables via .env file.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env from backend directory
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Groq LLM
    GROQ_API_KEY: str = "your_groq_api_key_here"
    GROQ_MODEL: str = "llama3-8b-8192"
    GROQ_SMART_MODEL: str = "mixtral-8x7b-32768"
    GROQ_MAX_RETRIES: int = 3
    GROQ_RETRY_DELAY: int = 2

    # Database
    DATABASE_URL: str = "sqlite:///./data/travel_guardian.db"
    SQLITE_DB_PATH: str = "./data/travel_guardian.db"

    # Security
    JWT_SECRET_KEY: str = "your-super-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 10080  # 7 days

    # App
    APP_ENV: str = "development"
    DEBUG: bool = True
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"

    # ML Model Paths
    MODEL_PATH: str = "./ml/models/xgboost_delay_model.pkl"
    ENCODER_PATH: str = "./ml/models/label_encoders.pkl"
    FAISS_FLIGHTS_PATH: str = "./data/faiss/flights"
    FAISS_HOTELS_PATH: str = "./data/faiss/hotels"
    FAISS_CITY_PATH: str = "./data/faiss/city"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def base_dir(self) -> Path:
        return Path(__file__).resolve().parent

    @property
    def data_dir(self) -> Path:
        return self.base_dir.parent / "data"

    @property
    def models_dir(self) -> Path:
        return self.base_dir / "ml" / "models"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
