# Quick Start Script
# Run this to start the application

Write-Host "🎨 Background Remover - Starting..." -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor Yellow
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Check if dependencies are installed
Write-Host "✓ Checking dependencies..." -ForegroundColor Green
$installed = pip list | Select-String "PySide6"
if (!$installed) {
    Write-Host "❌ Dependencies not installed!" -ForegroundColor Red
    Write-Host "Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

# Run application
Write-Host ""
Write-Host "🚀 Starting application..." -ForegroundColor Cyan
Write-Host ""
python -m bgremover.app.main

Write-Host ""
Write-Host "✓ Application closed." -ForegroundColor Green
