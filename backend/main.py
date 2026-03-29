from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import inspect, text


from app.core.config import settings
from app.database.database import Base, engine
from app.routes import admin, auth, annotators, jobs, carousel, sponsors

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent / "frontend"
UPLOADS_DIR = Path(settings.upload_dir).resolve()
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

# Create database tables
Base.metadata.create_all(bind=engine)


def ensure_annotator_gallery_columns() -> None:
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


ensure_annotator_gallery_columns()

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

# Include routes
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(annotators.router)
app.include_router(jobs.router)
app.include_router(carousel.router)
app.include_router(sponsors.router)


@app.get("/api")
async def root():
    """API info endpoint"""
    return {
        "message": "Shopping Platform API",
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
