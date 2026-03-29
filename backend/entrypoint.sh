#!/bin/bash

# Script de inicialização para a aplicação
set -e

echo "Starting Shopping Platform API..."
echo "DEBUG=${DEBUG}"
echo "PORT=${PORT:-8000}"

# Run the application
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
