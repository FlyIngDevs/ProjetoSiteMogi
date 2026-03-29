#!/usr/bin/env python
"""
Script para testar se a aplicação consegue iniciar corretamente
Execute: python test_import.py
"""

import sys
import os
from pathlib import Path

print("=" * 60)
print("APPLICATION IMPORT TEST")
print("=" * 60)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Working directory: {Path.cwd()}")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"sys.path: {sys.path[:3]}")  # First 3 entries
print("=" * 60)

error_count = 0

# Step 1: Test configuration
print("\n[1/5] Testing configuration...")
try:
    from app.core.config import settings
    print(f"   ✓ Settings loaded")
    print(f"     - API Title: {settings.api_title}")
    print(f"     - Debug: {settings.debug}")
    print(f"     - Database: {settings.database_url[:50]}...")
except Exception as e:
    print(f"   ✗ Error loading config: {e}")
    import traceback
    traceback.print_exc()
    error_count += 1

# Step 2: Test database
print("\n[2/5] Testing database connection...")
try:
    from app.database.database import engine, Base, SessionLocal
    print(f"   ✓ Database engine created")
    # Try to test the connection
    try:
        with engine.connect() as conn:
            print(f"   ✓ Database connection successful")
    except Exception as db_error:
        print(f"   ⚠ Database connection warning: {db_error}")
except Exception as e:
    print(f"   ✗ Error with database setup: {e}")
    import traceback
    traceback.print_exc()
    error_count += 1

# Step 3: Test models
print("\n[3/5] Testing models...")
try:
    from app.models.user import User
    from app.models.annotator import Annotator
    from app.models.job import Job
    from app.models.carousel import Carousel
    from app.models.sponsorship import Sponsorship
    print(f"   ✓ All models imported successfully")
except Exception as e:
    print(f"   ✗ Error importing models: {e}")
    import traceback
    traceback.print_exc()
    error_count += 1

# Step 4: Test routes
print("\n[4/5] Testing routes...")
try:
    from app.routes import admin, auth, annotators, jobs, carousel, sponsors
    print(f"   ✓ All routes imported successfully")
except Exception as e:
    print(f"   ✗ Error importing routes: {e}")
    import traceback
    traceback.print_exc()
    error_count += 1

# Step 5: Test main app
print("\n[5/5] Testing main application...")
try:
    from main import app
    print(f"   ✓ Main application imported successfully")
    print(f"   ✓ FastAPI app: {app.title}")
except Exception as e:
    print(f"   ✗ Error importing main app: {e}")
    import traceback
    traceback.print_exc()
    error_count += 1

print("\n" + "=" * 60)
if error_count == 0:
    print("✓ ALL TESTS PASSED! Application should start correctly.")
    print("=" * 60)
    sys.exit(0)
else:
    print(f"✗ {error_count} TEST(S) FAILED!")
    print("=" * 60)
    sys.exit(1)
