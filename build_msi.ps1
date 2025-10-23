# Build MSI Installer Script
# This script creates a Windows MSI installer for BGRemover

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BGRemover MSI Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
if (Test-Path "build") {
    Remove-Item -Recurse -Force "build"
}
if (Test-Path "dist") {
    Remove-Item -Recurse -Force "dist"
}

# Build MSI
Write-Host ""
Write-Host "Building MSI installer..." -ForegroundColor Green
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

python setup_msi.py bdist_msi

# Check if build succeeded
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   MSI Build Completed Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Find the MSI file
    $msiFile = Get-ChildItem -Path "dist" -Filter "*.msi" | Select-Object -First 1
    
    if ($msiFile) {
        Write-Host "MSI Installer created:" -ForegroundColor Cyan
        Write-Host "  File: $($msiFile.Name)" -ForegroundColor White
        Write-Host "  Path: $($msiFile.FullName)" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($msiFile.Length / 1MB, 2)) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "You can now distribute this MSI file!" -ForegroundColor Green
        Write-Host "Users can double-click to install BGRemover." -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   Build Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
