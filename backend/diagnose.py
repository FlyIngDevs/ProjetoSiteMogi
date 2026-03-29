#!/usr/bin/env python
"""
Diagnosis script - Run this to identify import errors
If this works, the app works. If this fails, you see exactly where.
"""
import sys
import os
from pathlib import Path

# Setup path
backend = Path(__file__).parent
sys.path.insert(0, str(backend))
os.chdir(backend)

print("\n" + "="*70)
print("DIAGNOSTIC IMPORT TEST")
print("="*70)
print(f"CWD: {os.getcwd()}")
print(f"Python: {sys.version}")
print(f"Path[0]: {sys.path[0]}")
print("="*70 + "\n")

def test_import(name, code):
    """Test a single import"""
    print(f"Testing: {name}...", end=" ", flush=True)
    try:
        exec(code, globals())
        print("✓")
        return True
    except Exception as e:
        print(f"✗\n  Error: {e}")
        import traceback
        traceback.print_exc()
        return False

# Progressive imports
all_pass = True
all_pass &= test_import("fastapi", "from fastapi import FastAPI")
all_pass &= test_import("sqlalchemy", "from sqlalchemy import create_engine")
all_pass &= test_import("pydantic", "from pydantic import BaseModel")

print()
all_pass &= test_import("app.core.config", "from app.core.config import settings")
all_pass &= test_import("app.database", "from app.database.database import Base, engine")
all_pass &= test_import("app.models.user", "from app.models.user import User")

print()
all_pass &= test_import("app.routes.auth", "from app.routes.auth import router")
all_pass &= test_import("app.routes.admin", "from app.routes.admin import router")

print()
all_pass &= test_import("main module", "from main import app")

print("\n" + "="*70)
if all_pass:
    print("✓✓✓ ALL IMPORTS WORK ✓✓✓")
    print("="*70 + "\n")
    sys.exit(0)
else:
    print("✗✗✗ SOME IMPORTS FAILED ✗✗✗")
    print("="*70 + "\n")
    sys.exit(1)
