from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """Application settings and configuration"""
    
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE) if ENV_FILE.exists() else None,
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore'
    )

    # Database
    database_url: str = "sqlite:///./shopping.db"

    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Server
    debug: bool = False
    api_title: str = "Bom Contato API"
    api_version: str = "1.0.0"
    api_description: str = "Plataforma Bom Contato com micro sites para anunciantes"
    upload_dir: str = str(BASE_DIR / "uploads")

    # Email / job applications
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "Bom Contato"
    smtp_use_tls: bool = True
    smtp_use_ssl: bool = False
    job_application_max_resume_size_mb: int = 5

    # Object storage
    storage_endpoint_url: str = ""
    storage_bucket_name: str = ""
    storage_access_key_id: str = ""
    storage_secret_access_key: str = ""
    storage_region: str = "auto"
    storage_public_base_url: str = ""

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

    @field_validator("allowed_origins", mode="before")
    @classmethod
    def validate_allowed_origins(cls, value):
        if isinstance(value, str):
            stripped = value.strip()
            if stripped.startswith("[") and stripped.endswith("]"):
                import json
                return json.loads(stripped)
            return [item.strip() for item in stripped.split(",") if item.strip()]
        return value


settings = Settings()
