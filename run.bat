@echo off
echo ========================================
echo   BNPL Risk Scoring Engine - Startup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.11 or higher
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

echo [2/3] Navigating to backend folder...
cd backend
echo.

echo [3/3] Starting backend server...
echo.
echo The dashboard will open automatically in your browser!
echo URL: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python main.py

pause
