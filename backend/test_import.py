#!/usr/bin/env python
"""
Script para testar se a aplicação consegue iniciar corretamente
Execute: python test_import.py
"""

import sys
from pathlib import Path

print("Testing application imports...")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Working directory: {Path.cwd()}")

try:
    print("\n1. Testing imports...")
    from app.core.config import settings
    print(f"   ✓ Settings loaded: {settings.api_title}")
    
    print("\n2. Testing database connection...")
    from app.database.database import engine, Base
    print("   ✓ Database engine created")
    
    print("\n3. Testing models...")
    from app.models.user import User
    from app.models.annotator import Annotator
    from app.models.job import Job
    from app.models.carousel import Carousel
    from app.models.sponsorship import Sponsorship
    print("   ✓ All models imported successfully")
    
    print("\n4. Testing routes...")
    from app.routes import admin, auth, annotators, jobs, carousel, sponsors
    print("   ✓ All routes imported successfully")
    
    print("\n5. Testing main app...")
    from main import app
    print("   ✓ Main application imported successfully")
    
    print("\n✓ All imports successful! Application should start correctly.")
    sys.exit(0)
    
except Exception as e:
    print(f"\n✗ Error during import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
