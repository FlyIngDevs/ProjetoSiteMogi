from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Application settings and configuration"""

    # Database
    database_url: str = "sqlite:///./shopping.db"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Server
    debug: bool = False
    api_title: str = "Shopping Platform API"
    api_version: str = "1.0.0"
    api_description: str = "Platform de shopping online com micro sites para anunciantes"
    upload_dir: str = str(BASE_DIR / "uploads")

    # Email / job applications
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "ShoppingHub"
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    job_application_max_resume_size_mb: int = 5

    # CORS
    allowed_origins: List[str] = Field(default_factory=lambda: [
        "null",
        "http://localhost:3000",
        "http://localhost:8080",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8000",
    ])

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        case_sensitive=False
    )


settings = Settings()
