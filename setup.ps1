# Setup Script for Background Remover
# Run this first to set up the development environment

Write-Host "🎨 Background Remover - Setup" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "  $pythonVersion" -ForegroundColor Green

if ($pythonVersion -notmatch "Python 3\.[8-9]|Python 3\.1[0-9]") {
    Write-Host "❌ Python 3.8+ is required!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Python version OK" -ForegroundColor Green
Write-Host ""

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists, skipping..." -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "Installing dependencies (this may take a few minutes)..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Create necessary directories
Write-Host "Creating directories..." -ForegroundColor Yellow
$directories = @("models", "samples", "build", "tests")
foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}
Write-Host "✓ Directories ready" -ForegroundColor Green
Write-Host ""

# Summary
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✅ Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Run the application:" -ForegroundColor White
Write-Host "     .\run.ps1" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Or run manually:" -ForegroundColor White
Write-Host "     python -m bgremover.app.main" -ForegroundColor Yellow
Write-Host ""
Write-Host "  3. Run tests:" -ForegroundColor White
Write-Host "     pytest" -ForegroundColor Yellow
Write-Host ""
Write-Host "  4. Build executable:" -ForegroundColor White
Write-Host "     pyinstaller build/pyinstaller.spec" -ForegroundColor Yellow
Write-Host ""
Write-Host "For more information, see README.md and BUILD.md" -ForegroundColor Gray
Write-Host ""
