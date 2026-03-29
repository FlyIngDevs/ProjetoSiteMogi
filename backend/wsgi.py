#!/usr/bin/env python
"""
WSGI application wrapper for Render deployment
This provides a fallback if uvicorn has import issues
Execute: gunicorn wsgi:app
"""

import os
import sys
from pathlib import Path

# Ensure proper path
backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

# Load environment
from dotenv import load_dotenv
env_file = backend_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)

print("=" * 70)
print("WSGI Application Wrapper", file=sys.stderr)
print(f"Directory: {backend_dir}", file=sys.stderr)
print(f"Python: {sys.version.split()[0]}", file=sys.stderr)
print("=" * 70, file=sys.stderr)

# Import the FastAPI app
try:
    from main import app
    print("✓ FastAPI app imported successfully", file=sys.stderr)
except Exception as e:
    print(f"✗ ERROR: Failed to import app: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

# Export for WSGI servers
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv('PORT', '8000'))
    uvicorn.run(app, host="0.0.0.0", port=port)
