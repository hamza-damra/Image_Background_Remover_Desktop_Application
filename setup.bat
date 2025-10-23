@echo off
echo ========================================
echo Background Remover - Windows Setup
echo ========================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    echo.
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
) else (
    python -m venv venv
    echo [OK] Virtual environment created
)
echo.

REM Activate and install
echo Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed
echo.

REM Create directories
echo Creating directories...
if not exist models mkdir models
if not exist samples mkdir samples
if not exist build mkdir build
if not exist tests mkdir tests
echo [OK] Directories created
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Double-click run.bat
echo   2. Or: venv\Scripts\activate.bat then python -m bgremover.app.main
echo.
echo For more information, see README.md
echo.
pause
