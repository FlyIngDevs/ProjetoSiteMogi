#!/usr/bin/env python
"""
Production-ready application runner for Render deployment.
Execute with: python run.py
"""

import os
import sys
from pathlib import Path

from sqlalchemy import text


backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


def log(message: str) -> None:
    print(message, file=sys.stderr)


log("\n" + "=" * 80)
log("SHOPPING PLATFORM API - STARTUP SEQUENCE")
log("=" * 80)
log(f"Started at: {backend_dir}")
log(f"Python {sys.version.split()[0]} from {sys.executable}")
log("=" * 80 + "\n")

log("[1/4] Loading environment...")
try:
    from dotenv import load_dotenv

    env_file = backend_dir / ".env"
    if env_file.exists():
        log(f"  OK Loading {env_file}")
        load_dotenv(env_file)
    else:
        log(f"  INFO {env_file} not present (using environment variables)")

    for key in ["DATABASE_URL", "DEBUG", "PORT", "UPLOAD_DIR"]:
        value = os.environ.get(key)
        if value:
            display = value[:40] + "..." if len(value) > 40 else value
            log(f"    {key}: {display}")
except Exception as exc:
    log(f"  ERROR loading environment: {exc}")
    sys.exit(1)

log("\n[2/4] Initializing FastAPI application...")
try:
    from main import app

    log(f"  OK Application created: {app.title}")
except Exception as exc:
    log(f"  ERROR importing app: {exc}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

log("\n[3/4] Setting up database...")
try:
    from app.database.database import Base, engine

    log("  OK Database engine initialized")
    Base.metadata.create_all(bind=engine)
    log("  OK Database tables created")

    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    log("  OK Database connection working")
except Exception as exc:
    log(f"  ERROR database setup failed: {exc}")
    import traceback

    traceback.print_exc()
    sys.exit(1)

log("\n[4/4] Verifying application...")
try:
    assert app is not None, "App is None"
    assert hasattr(app, "routes"), "App missing routes"
    assert len(app.routes) > 0, "No routes registered"
    log(f"  OK App verified ({len(app.routes)} routes)")
except Exception as exc:
    log(f"  ERROR app verification failed: {exc}")
    sys.exit(1)

log("\n" + "=" * 80)
log("STARTUP SEQUENCE COMPLETE - STARTING SERVER")
log("=" * 80 + "\n")

try:
    import uvicorn

    port = int(os.environ.get("PORT", "8000"))
    host = "0.0.0.0"

    log(f"Server starting on http://{host}:{port}")
    log(f"API documentation available at /docs")
    log("Press CTRL+C to stop\n")

    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        interface="asgi3",
    )
except KeyboardInterrupt:
    log("\n\nShutdown requested by user")
    sys.exit(0)
except Exception as exc:
    log(f"\nFATAL ERROR: {exc}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
