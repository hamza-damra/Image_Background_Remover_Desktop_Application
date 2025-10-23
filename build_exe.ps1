# Build Executable Script
# بناء ملف تنفيذي للتطبيق
# المهندس حمزة ضمرة - Eng. Hamza Damra

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Background Remover - Build Tool   " -ForegroundColor Cyan
Write-Host "  المهندس حمزة ضمرة                 " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (!(Test-Path "venv")) {
    Write-Host "❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first." -ForegroundColor Yellow
    exit 1
}

# Activate virtual environment
Write-Host "✓ Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Install PyInstaller if not installed
Write-Host "✓ Checking PyInstaller..." -ForegroundColor Green
$pyinstaller = pip list | Select-String "pyinstaller"
if (!$pyinstaller) {
    Write-Host "  Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host "✓ Cleaning previous builds..." -ForegroundColor Green
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build executable
Write-Host ""
Write-Host "🔨 Building executable..." -ForegroundColor Cyan
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

pyinstaller --clean bgremover.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: .\dist\BGRemover\" -ForegroundColor Cyan
    Write-Host "Run: .\dist\BGRemover\BGRemover.exe" -ForegroundColor Cyan
    Write-Host ""
    
    # Copy additional files
    Write-Host "✓ Copying additional files..." -ForegroundColor Green
    Copy-Item "README_AR.md" "dist\BGRemover\" -ErrorAction SilentlyContinue
    Copy-Item "LICENSE" "dist\BGRemover\" -ErrorAction SilentlyContinue
    Copy-Item "CREDITS.md" "dist\BGRemover\" -ErrorAction SilentlyContinue
    
    # Create models directory
    New-Item -ItemType Directory -Path "dist\BGRemover\models" -Force | Out-Null
    
    Write-Host "✓ Additional files copied." -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 Ready for MSI creation!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Build failed!" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Yellow
    exit 1
}
