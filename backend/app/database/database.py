from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from app.core.config import settings


def normalize_database_url(database_url: str) -> str:
    """Normalize Render/Postgres URLs for SQLAlchemy."""
    database_url = (database_url or "").strip()

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not set. Configure a valid PostgreSQL connection string in the deployment environment."
        )

    if "${{" in database_url or "Postgres.DATABASE_URL" in database_url:
        raise RuntimeError(
            "DATABASE_URL appears to be an unresolved placeholder. Replace it with a real environment reference/value in the deployment platform."
        )

    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)

    if (
        database_url.startswith("postgresql://")
        and "+psycopg" not in database_url
        and "+psycopg2" not in database_url
    ):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)

    if database_url.startswith("sqlite:///"):
        return database_url

    if "://" not in database_url:
        raise RuntimeError(
            "DATABASE_URL is invalid. Expected a full SQLAlchemy/PostgreSQL URL such as postgresql://user:pass@host:5432/dbname."
        )

    return database_url


DATABASE_URL = normalize_database_url(settings.database_url)

# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
    pool_pre_ping=True,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db() -> Session:
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
