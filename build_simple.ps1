# Build Executable - Simple Version
# Eng. Hamza Damra

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Building Background Remover        " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (!(Test-Path "venv")) {
    Write-Host "ERROR: Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first." -ForegroundColor Yellow
    exit 1
}

Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# Install PyInstaller if needed
Write-Host "Checking PyInstaller..." -ForegroundColor Green
$pyinstaller = pip list | Select-String "pyinstaller"
if (!$pyinstaller) {
    Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
    pip install pyinstaller
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Green
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build executable
Write-Host ""
Write-Host "Building executable..." -ForegroundColor Cyan
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

pyinstaller --clean bgremover.spec

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Executable location: .\dist\BGRemover\" -ForegroundColor Cyan
    Write-Host ""
    
    # Copy additional files
    Write-Host "Copying additional files..." -ForegroundColor Green
    Copy-Item "README_AR.md" "dist\BGRemover\" -ErrorAction SilentlyContinue
    Copy-Item "LICENSE" "dist\BGRemover\" -ErrorAction SilentlyContinue
    Copy-Item "CREDITS.md" "dist\BGRemover\" -ErrorAction SilentlyContinue
    
    # Create models directory
    New-Item -ItemType Directory -Path "dist\BGRemover\models" -Force | Out-Null
    
    Write-Host "Done!" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}
