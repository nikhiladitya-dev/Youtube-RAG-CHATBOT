from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()
class Settings(BaseSettings):
    """
    Application configuration loaded from environment variables.
    """
    HF_TOKEN: str
    EMBEDDING_MODEL: str
    LLM_MODEL: str
    LLM_TEMPERATURE: float = 0.2
    LLM_MAX_NEW_TOKENS: int = 2048
    CHROMA_DB_PATH: str
    TRANSCRIPT_PATH: str
    CHROMA_COLLECTION_NAME: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Absolute paths
TRANSCRIPT_DIR = PROJECT_ROOT / settings.TRANSCRIPT_PATH
VECTOR_DB_DIR = PROJECT_ROOT / settings.CHROMA_DB_PATH