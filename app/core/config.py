from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    UPLOAD_DIR: str = "uploads"
    LOG_DIR: str = "logs"
    ALLOWED_ORIGINS: str = "http://127.0.0.1:5500"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()