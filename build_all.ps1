# Complete Build and Package Script
# بناء وتجهيز البرنامج بالكامل
# المهندس حمزة ضمرة - Eng. Hamza Damra

param(
    [switch]$SkipBuild = $false,
    [switch]$CreateMSI = $false
)

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  Background Remover Pro - Build Tool   " -ForegroundColor Cyan
Write-Host "  المهندس حمزة ضمرة                     " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Build Executable
if (!$SkipBuild) {
    Write-Host "Step 1: Building Executable" -ForegroundColor Yellow
    Write-Host "=====================================" -ForegroundColor Gray
    Write-Host ""
    
    & ".\build_exe.ps1"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host ""
        Write-Host "❌ Build failed! Cannot continue." -ForegroundColor Red
        exit 1
    }
    
    Write-Host ""
} else {
    Write-Host "⏭️  Skipping build (using existing executable)" -ForegroundColor Yellow
    Write-Host ""
}

# Step 2: Create Installer Package
Write-Host "Step 2: Creating Installer Package" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Gray
Write-Host ""

if ($CreateMSI) {
    Write-Host "Creating MSI installer..." -ForegroundColor Cyan
    & ".\create_msi.ps1"
} else {
    Write-Host "Creating simple installer..." -ForegroundColor Cyan
    & ".\create_installer_simple.ps1"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Installer creation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "  ✅ All Done! جاهز للتوزيع!          " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📦 Your distribution package is ready!" -ForegroundColor Green
Write-Host ""

# Show summary
Write-Host "Summary / الملخص:" -ForegroundColor Yellow
Write-Host "  • Executable: .\dist\BGRemover\BGRemover.exe" -ForegroundColor White
if ($CreateMSI) {
    Write-Host "  • MSI Installer: .\BGRemover_Setup.msi" -ForegroundColor White
} else {
    Write-Host "  • ZIP Package: .\BGRemover_Setup_v1.0.0.zip" -ForegroundColor White
    Write-Host "  • Folder: .\BGRemover_Installer\" -ForegroundColor White
}
Write-Host ""
Write-Host "Developer: Eng. Hamza Damra - المهندس حمزة ضمرة" -ForegroundColor Cyan
Write-Host ""
