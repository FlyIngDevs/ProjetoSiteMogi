#!/bin/bash
set -e

echo "================================"
echo "Shopping Platform API - Startup"
echo "================================"
echo ""
echo "Environment:"
echo "  Python: $(python --version)"
echo "  PID: $$"
echo "  Directory: $(pwd)"
echo "  DEBUG: ${DEBUG:-false}"
echo "  PORT: ${PORT:-8000}"
echo ""

echo "Running pre-startup checks..."
python test_import.py
if [ $? -ne 0 ]; then
    echo "ERROR: Import test failed!"
    exit 1
fi

echo ""
echo "Starting uvicorn server..."
exec uvicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8000} \
    --log-level info \
    --access-log
