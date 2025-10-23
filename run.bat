@echo off
echo ========================================
echo Background Remover - Starting...
echo ========================================
echo.

REM Check if venv exists
if not exist venv (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    echo.
    pause
    exit /b 1
)

REM Activate and run
call venv\Scripts\activate.bat
python -m bgremover.app.main

echo.
echo Application closed.
pause
