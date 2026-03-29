#!/usr/bin/env python
"""
Alternative application runner - Ensures proper initialization and error handling
Execute: python run.py
"""

import os
import sys
from pathlib import Path

# Setup path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Load environment
print("=" * 70)
print("Shopping Platform API - Starting")
print("=" * 70)

from dotenv import load_dotenv
env_file = backend_dir / ".env"
if env_file.exists():
    print(f"Loading environment from {env_file}")
    load_dotenv(env_file)
else:
    print(f"Note: {env_file} not found (using environment variables)")

print(f"Python: {sys.version.split()[0]}")
print(f"Directory: {backend_dir}")
print(f"sys.path[0]: {sys.path[0]}")
print("=" * 70)

# Run pre-startup checks
print("\nRunning pre-startup checks...")
try:
    # Check 1: Import test
    print("  [1/3] Testing imports...", end=" ", flush=True)
    from main import app
    print("✓")
    
    # Check 2: Database setup
    print("  [2/3] Setting up database...", end=" ", flush=True)
    from app.database.database import Base, engine
    Base.metadata.create_all(bind=engine)
    print("✓")
    
    # Check 3: Settings
    print("  [3/3] Verifying configuration...", end=" ", flush=True)
    from app.core.config import settings
    assert settings.api_title, "API title not set"
    print("✓")
    
except Exception as e:
    print("\n✗ PRE-STARTUP CHECK FAILED")
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Start uvicorn
print("\nStarting uvicorn server...")
print("-" * 70)

try:
    import uvicorn
    
    port = int(os.getenv('PORT', '8000'))
    host = "0.0.0.0"
    
    # Configuration
    config = {
        "app": app,
        "host": host,
        "port": port,
        "log_level": "info",
        "access_log": True,
        "use_colors": True,
    }
    
    print(f"Starting: http://{host}:{port}")
    print(f"API Docs: http://{host}:{port}/docs")
    print("-" * 70)
    
    uvicorn.run(**config)
    
except KeyboardInterrupt:
    print("\n\nShutdown requested")
    sys.exit(0)
except Exception as e:
    print(f"\n✗ FAILED TO START: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
