# Pre-Build Check Script
# فحص ما قبل البناء
# المهندس حمزة ضمرة - Eng. Hamza Damra

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Pre-Build Checklist                " -ForegroundColor Cyan
Write-Host "  فحص ما قبل البناء                 " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check 1: Python
Write-Host "1. Checking Python..." -ForegroundColor Yellow
$python = Get-Command python -ErrorAction SilentlyContinue
if ($python) {
    $version = python --version
    Write-Host "   ✓ $version" -ForegroundColor Green
} else {
    Write-Host "   ❌ Python not found!" -ForegroundColor Red
    $allGood = $false
}

# Check 2: Virtual Environment
Write-Host "2. Checking virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "   ✓ Virtual environment exists" -ForegroundColor Green
} else {
    Write-Host "   ❌ Virtual environment not found!" -ForegroundColor Red
    Write-Host "      Run: .\setup.ps1" -ForegroundColor Yellow
    $allGood = $false
}

# Check 3: Main application file
Write-Host "3. Checking application files..." -ForegroundColor Yellow
if (Test-Path "bgremover\app\main.py") {
    Write-Host "   ✓ Main application found" -ForegroundColor Green
} else {
    Write-Host "   ❌ Main application not found!" -ForegroundColor Red
    $allGood = $false
}

# Check 4: Assets
Write-Host "4. Checking assets..." -ForegroundColor Yellow
$assetsPath = "bgremover\app\ui\assets"
if (Test-Path $assetsPath) {
    Write-Host "   ✓ Assets directory exists" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Assets directory not found" -ForegroundColor Yellow
    Write-Host "      Creating..." -ForegroundColor Gray
    New-Item -ItemType Directory -Path $assetsPath -Force | Out-Null
}

# Check 5: i18n files
Write-Host "5. Checking translations..." -ForegroundColor Yellow
if (Test-Path "bgremover\app\ui\i18n\ar.json") {
    Write-Host "   ✓ Arabic translations found" -ForegroundColor Green
} else {
    Write-Host "   ❌ Arabic translations not found!" -ForegroundColor Red
    $allGood = $false
}

# Check 6: Build files
Write-Host "6. Checking build configuration..." -ForegroundColor Yellow
if (Test-Path "bgremover.spec") {
    Write-Host "   ✓ PyInstaller spec found" -ForegroundColor Green
} else {
    Write-Host "   ❌ PyInstaller spec not found!" -ForegroundColor Red
    $allGood = $false
}

# Check 7: Dependencies
Write-Host "7. Checking key dependencies..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
$packages = @("PySide6", "rembg", "Pillow", "numpy")
$missingPackages = @()

foreach ($package in $packages) {
    $installed = pip list | Select-String $package
    if ($installed) {
        Write-Host "   ✓ $package installed" -ForegroundColor Green
    } else {
        Write-Host "   ❌ $package not installed!" -ForegroundColor Red
        $missingPackages += $package
        $allGood = $false
    }
}

# Check 8: Disk space
Write-Host "8. Checking disk space..." -ForegroundColor Yellow
$drive = Get-PSDrive -Name C
$freeGB = [math]::Round($drive.Free / 1GB, 2)
if ($freeGB -gt 2) {
    Write-Host "   ✓ Sufficient space: ${freeGB}GB free" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Low disk space: ${freeGB}GB free" -ForegroundColor Yellow
    Write-Host "      Recommended: 2GB+ free" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "  ✅ All checks passed!            " -ForegroundColor Green
    Write-Host "  Ready to build!                  " -ForegroundColor Green
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You can now run:" -ForegroundColor Cyan
    Write-Host "  .\build_all.ps1" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host "  ❌ Some checks failed!           " -ForegroundColor Red
    Write-Host "=====================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please fix the issues above before building." -ForegroundColor Yellow
    Write-Host ""
    
    if ($missingPackages.Count -gt 0) {
        Write-Host "To install missing packages:" -ForegroundColor Yellow
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  pip install -r requirements.txt" -ForegroundColor White
        Write-Host ""
    }
}

Write-Host "Developer: Eng. Hamza Damra" -ForegroundColor Cyan
Write-Host ""
