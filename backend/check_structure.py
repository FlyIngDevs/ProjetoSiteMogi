#!/usr/bin/env python
"""
Script para verificar estrutura dos arquivos
Execute: python check_structure.py
"""

import os
from pathlib import Path

print("=" * 60)
print("CHECKING PROJECT STRUCTURE")
print("=" * 60)

# Get backend directory
backend_dir = Path(__file__).parent
print(f"\nBackend directory: {backend_dir}")
print(f"Backend exists: {backend_dir.exists()}")

# Check critical files
critical_files = [
    "main.py",
    "requirements.txt",
    ".env",
    "app/__init__.py",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/database/__init__.py",
    "app/database/database.py",
    "app/models/__init__.py",
    "app/models/user.py",
    "app/routes/__init__.py",
    "app/routes/auth.py",
]

print("\nCritical files:")
missing = []
for file in critical_files:
    file_path = backend_dir / file
    exists = file_path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {file}")
    if not exists:
        missing.append(file)

if missing:
    print(f"\n✗ Missing {len(missing)} critical files!")
    for f in missing:
        print(f"    - {f}")
else:
    print(f"\n✓ All critical files present!")

# Check directory structure
print("\nDirectory structure:")
for root, dirs, files in os.walk(backend_dir):
    # Skip __pycache__ and venv
    dirs[:] = [d for d in dirs if d not in ['__pycache__', 'venv', '.venv', 'env', '.env']]
    
    level = root.replace(str(backend_dir), '').count(os.sep)
    indent = ' ' * 2 * level
    print(f'{indent}{os.path.basename(root)}/')
    
    if level < 3:  # Only show first 3 levels
        file_indent = ' ' * 2 * (level + 1)
        for file in sorted(files)[:10]:  # Limit files shown
            if not file.startswith('.'):
                print(f'{file_indent}{file}')
        if len(files) > 10:
            print(f'{file_indent}... and {len(files) - 10} more files')

print("\n" + "=" * 60)
