@echo off
REM Color codes are limited in Windows batch, so we'll just use text

echo === ShoppingHub Setup ===
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is required but not installed.
    pause
    exit /b 1
)

REM Backend setup
echo Setting up Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo .env file created. Please update it with your settings.
)

echo.
echo === Backend setup complete! ===
echo To start the backend server, run:
echo cd backend
echo venv\Scripts\activate.bat
echo uvicorn main:app --reload
echo.
echo Frontend is ready to serve!
echo To start the frontend, navigate to the frontend directory and use:
echo python -m http.server 8080
echo or use any HTTP server of your choice
echo.
echo === Setup Complete ===

pause
