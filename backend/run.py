#!/usr/bin/env python
"""
Production-ready application runner for Render deployment
Ensures proper initialization with detailed error reporting
Execute: python run.py
"""

import os
import sys
from pathlib import Path

# ============== SETUP PATH ==============
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

print("\n" + "=" * 80)
print("SHOPPING PLATFORM API - STARTUP SEQUENCE", file=sys.stderr)
print("=" * 80, file=sys.stderr)
print(f"Started at: {backend_dir}", file=sys.stderr)
print(f"Python {sys.version.split()[0]} from {sys.executable}", file=sys.stderr)
print("=" * 80 + "\n", file=sys.stderr)

# ============== LOAD ENVIRONMENT ==============
print("[1/4] Loading environment...", file=sys.stderr)
try:
    from dotenv import load_dotenv
    env_file = backend_dir / ".env"
    if env_file.exists():
        print(f"  ✓ Loading {env_file}", file=sys.stderr)
        load_dotenv(env_file)
    else:
        print(f"  ⓘ {env_file} not present (using environment variables)", file=sys.stderr)
    
    # Show key env vars
    for key in ['DATABASE_URL', 'DEBUG', 'PORT', 'UPLOAD_DIR']:
        val = os.environ.get(key)
        if val:
            display = val[:40] + "..." if len(val) > 40 else val
            print(f"    {key}: {display}", file=sys.stderr)
except Exception as e:
    print(f"  ✗ Error loading environment: {e}", file=sys.stderr)
    sys.exit(1)

# ============== INITIALIZE APP ==============
print("\n[2/4] Initializing FastAPI application...", file=sys.stderr)
try:
    from main import app
    print(f"  ✓ Application created: {app.title}", file=sys.stderr)
except Exception as e:
    print(f"  ✗ Failed to import app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

# ============== DATABASE SETUP ==============
print("\n[3/4] Setting up database...", file=sys.stderr)
try:
    from app.database.database import Base, engine, SessionLocal
    print("  ✓ Database engine initialized", file=sys.stderr)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("  ✓ Database tables created", file=sys.stderr)
    
    # Test connection
    try:
        db = SessionLocal()
        db.close()
        print("  ✓ Database connection working", file=sys.stderr)
    except Exception as db_error:
        print(f"  ⚠ Warning: Database connection issue: {db_error}", file=sys.stderr)
        print("    (App will start but database operations may fail)", file=sys.stderr)
except Exception as e:
    print(f"  ✗ Database setup failed: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    print("\n  ⚠ Continuing anyway - app may work without database", file=sys.stderr)

# ============== VERIFY APP ==============
print("\n[4/4] Verifying application...", file=sys.stderr)
try:
    assert app is not None, "App is None"
    assert hasattr(app, 'routes'), "App missing routes"
    assert len(app.routes) > 0, "No routes registered"
    print(f"  ✓ App verified ({len(app.routes)} routes)", file=sys.stderr)
except Exception as e:
    print(f"  ✗ App verification failed: {e}", file=sys.stderr)
    sys.exit(1)

# ============== START SERVER ==============
print("\n" + "=" * 80, file=sys.stderr)
print("✓✓✓ STARTUP SEQUENCE COMPLETE - STARTING SERVER ✓✓✓", file=sys.stderr)
print("=" * 80 + "\n", file=sys.stderr)

try:
    import uvicorn
    
    port = int(os.environ.get('PORT', '8000'))
    host = "0.0.0.0"
    
    # Print connection info
    print(f"Server starting on http://{host}:{port}", file=sys.stderr)
    print(f"API Documentation: http://localhost:{port}/docs", file=sys.stderr)
    print("Press CTRL+C to stop\n", file=sys.stderr)
    
    # Run uvicorn
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True,
        interface="asgi3"
    )
    
except KeyboardInterrupt:
    print("\n\nShutdown requested by user", file=sys.stderr)
    sys.exit(0)
except Exception as e:
    print(f"\n✗ FATAL ERROR: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
