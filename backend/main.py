from pathlib import Path

# DEBUG: Print import information immediately
import sys
import os
print("=" * 70, file=sys.stderr)
print("DEBUG: Starting main.py import", file=sys.stderr)
print(f"  Python: {sys.version.split()[0]}", file=sys.stderr)
print(f"  CWD: {os.getcwd()}", file=sys.stderr)
print(f"  __file__: {__file__}", file=sys.stderr)
print(f"  sys.path[0]: {sys.path[0]}", file=sys.stderr)
print("=" * 70, file=sys.stderr)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text

print("✓ FastAPI imports successful", file=sys.stderr)

try:
    from app.core.config import settings
    print("✓ Config imported", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR importing config: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

try:
    from app.database.database import Base, engine
    print("✓ Database imported", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR importing database: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

try:
    from app.routes import admin, auth, annotators, jobs, carousel, sponsors, site_config
    print("✓ Routes imported", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR importing routes: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

print("=" * 70, file=sys.stderr)
print("✓ All imports successful!", file=sys.stderr)
print("=" * 70, file=sys.stderr)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOADS_DIR = Path(settings.upload_dir).resolve()
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Create database tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")


def ensure_annotator_gallery_columns() -> None:
    try:
        inspector = inspect(engine)
        if "annotators" not in inspector.get_table_names():
            return

        existing_columns = {column["name"] for column in inspector.get_columns("annotators")}
        required_columns = [
            "photo_1_url",
            "photo_2_url",
            "photo_3_url",
            "photo_4_url",
        ]

        with engine.begin() as connection:
            for column_name in required_columns:
                if column_name not in existing_columns:
                    connection.execute(text(f"ALTER TABLE annotators ADD COLUMN {column_name} VARCHAR"))
    except Exception as e:
        print(f"Warning: Could not ensure annotator gallery columns: {e}")


try:
    ensure_annotator_gallery_columns()
except Exception as e:
    print(f"Warning: Error during database setup: {e}")

# Initialize FastAPI app
try:
    app = FastAPI(
        title=settings.api_title,
        description=settings.api_description,
        version=settings.api_version,
        debug=settings.debug
    )
    print("✓ FastAPI app created", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR creating FastAPI app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

# Add CORS middleware
try:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    print("✓ CORS middleware added", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR adding CORS middleware: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

try:
    app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")
    print("✓ Uploads mount added", file=sys.stderr)
except Exception as e:
    print(f"⚠ WARNING mounting uploads: {e}", file=sys.stderr)

# Include routes
try:
    app.include_router(auth.router)
    app.include_router(admin.router)
    app.include_router(annotators.router)
    app.include_router(jobs.router)
    app.include_router(carousel.router)
    app.include_router(sponsors.router)
    app.include_router(site_config.router)
    print("✓ All routes included", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR including routes: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

print("=" * 70, file=sys.stderr)
print("✓✓✓ MAIN.PY INITIALIZATION COMPLETE ✓✓✓", file=sys.stderr)
print("=" * 70, file=sys.stderr)


@app.get("/api")
async def root():
    """API info endpoint"""
    return {
        "message": "Bom Contato API",
        "version": settings.api_version,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "healthy"}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
