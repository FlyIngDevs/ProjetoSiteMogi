#!/usr/bin/env python
"""
Quick pre-flight check before deployment to Render
Run this locally to verify everything works before pushing
Execute: python preflight.py
"""

import sys
import os
from pathlib import Path

backend_dir = Path(__file__).parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

print("\n" + "=" * 80)
print("PRE-FLIGHT CHECK FOR RENDER DEPLOYMENT")
print("=" * 80 + "\n")

checks_passed = 0
checks_failed = 0

def check(name, fn):
    """Run a single check"""
    global checks_passed, checks_failed
    print(f"  Checking {name}...", end=" ", flush=True)
    try:
        fn()
        print("✓")
        checks_passed += 1
        return True
    except Exception as e:
        print(f"✗ {e}")
        checks_failed += 1
        return False

# Critical Files
print("1. PROJECT STRUCTURE")
check("main.py exists", lambda: (backend_dir / "main.py").exists() or (_ for _ in ()).throw(Exception("main.py not found")))
check("app folder exists", lambda: (backend_dir / "app").is_dir() or (_ for _ in ()).throw(Exception("app/ not found")))
check("app/__init__.py exists", lambda: (backend_dir / "app" / "__init__.py").exists() or (_ for _ in ()).throw(Exception("app/__init__.py not found")))
check("requirements.txt exists", lambda: (backend_dir / "requirements.txt").exists() or (_ for _ in ()).throw(Exception("requirements.txt not found")))

# Environment
print("\n2. ENVIRONMENT")
check("Python version", lambda: sys.version.split()[0] >= "3.10" or (_ for _ in ()).throw(Exception(f"Python {sys.version.split()[0]} - need 3.10+")))

# Imports
print("\n3. MODULE IMPORTS")
check("fastapi", lambda: __import__('fastapi'))
check("sqlalchemy", lambda: __import__('sqlalchemy'))
check("pydantic", lambda: __import__('pydantic'))
check("pydantic_settings", lambda: __import__('pydantic_settings'))
check("uvicorn", lambda: __import__('uvicorn'))
check("boto3", lambda: __import__('boto3'))

# Configuration
print("\n4. APPLICATION CONFIG")
check("Config loads", lambda: __import__('app.core.config', fromlist=['settings']).settings)
check("Database init", lambda: __import__('app.database.database', fromlist=['Base', 'engine']))

# Models
print("\n5. MODELS")
check("User model", lambda: __import__('app.models.user', fromlist=['User']))
check("All models available", lambda: (
    __import__('app.models.annotator', fromlist=['Annotator']),
    __import__('app.models.job', fromlist=['Job']),
    __import__('app.models.carousel', fromlist=['Carousel']),
    __import__('app.models.sponsorship', fromlist=['Sponsorship']),
    __import__('app.models.site_setting', fromlist=['SiteSetting'])
))

# Routes
print("\n6. API ROUTES")
check("Auth routes", lambda: __import__('app.routes.auth', fromlist=['router']))
check("All routes", lambda: (
    __import__('app.routes.admin', fromlist=['router']),
    __import__('app.routes.annotators', fromlist=['router']),
    __import__('app.routes.jobs', fromlist=['router']),
    __import__('app.routes.carousel', fromlist=['router']),
    __import__('app.routes.sponsors', fromlist=['router']),
    __import__('app.routes.site_config', fromlist=['router'])
))

# Main App
print("\n7. FASTAPI APPLICATION")
def check_main_app():
    from main import app
    assert app is not None
    assert app.title == "Bom Contato API"
    assert len(app.routes) > 0
    return app

app = None
if check("Main app imports", lambda: check_main_app()):
    try:
        from main import app
        print(f"    App routes registered: {len(app.routes)}")
        print(f"    App title: {app.title}")
    except:
        pass

# Results
print("\n" + "=" * 80)
print(f"RESULTS: {checks_passed} passed, {checks_failed} failed")
print("=" * 80)

if checks_failed == 0:
    print("\n✓✓✓ ALL CHECKS PASSED ✓✓✓")
    print("\nYou can safely deploy to Render!")
    print("\nNext steps:")
    print("  1. git add -A")
    print("  2. git commit -m 'chore: Ready for Render deployment'")
    print("  3. git push")
    print("  4. Check Render dashboard for deployment status\n")
    sys.exit(0)
else:
    print(f"\n✗✗✗ {checks_failed} CHECK(S) FAILED ✗✗✗")
    print("\nFix the issues above, then try again.\n")
    sys.exit(1)
