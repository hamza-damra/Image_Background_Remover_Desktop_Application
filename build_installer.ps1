# Build Installer using Inno Setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BGRemover Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Inno Setup is installed
Write-Host "Checking for Inno Setup..." -ForegroundColor Yellow

$innoPath = "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe"

if (-not (Test-Path $innoPath)) {
    Write-Host "Inno Setup not found. Installing..." -ForegroundColor Yellow
    Write-Host ""
    
    # Download Inno Setup
    $innoUrl = "https://jrsoftware.org/download.php/is.exe"
    $innoInstaller = "$env:TEMP\innosetup.exe"
    
    Write-Host "Downloading Inno Setup..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri $innoUrl -OutFile $innoInstaller -UseBasicParsing
        
        Write-Host "Installing Inno Setup (this may take a minute)..." -ForegroundColor Yellow
        Start-Process -FilePath $innoInstaller -ArgumentList "/VERYSILENT", "/SUPPRESSMSGBOXES", "/NORESTART" -Wait
        
        Remove-Item $innoInstaller -Force
        
        if (Test-Path $innoPath) {
            Write-Host "Inno Setup installed successfully!" -ForegroundColor Green
        } else {
            Write-Host "ERROR: Inno Setup installation failed!" -ForegroundColor Red
            Write-Host "Please download and install manually from: https://jrsoftware.org/isinfo.php" -ForegroundColor Yellow
            exit 1
        }
    } catch {
        Write-Host "ERROR: Failed to download Inno Setup!" -ForegroundColor Red
        Write-Host "Please download and install manually from: https://jrsoftware.org/isinfo.php" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "Inno Setup found!" -ForegroundColor Green
}

# Check if PyInstaller build exists
Write-Host "Checking for application build..." -ForegroundColor Yellow

if (-not (Test-Path "dist\BGRemover\BGRemover.exe")) {
    Write-Host "ERROR: Application build not found!" -ForegroundColor Red
    Write-Host "Please run: .\build_simple.ps1 first" -ForegroundColor Yellow
    exit 1
}

Write-Host "Application build found!" -ForegroundColor Green
Write-Host ""

# Build installer
Write-Host "Building installer..." -ForegroundColor Green
Write-Host "This may take several minutes..." -ForegroundColor Yellow
Write-Host ""

& $innoPath "bgremover_setup.iss"

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Installer Created Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    $setupFile = Get-Item "BGRemover_Setup_v*.exe" | Select-Object -First 1
    
    if ($setupFile) {
        Write-Host "Setup File:" -ForegroundColor Cyan
        Write-Host "  Name: $($setupFile.Name)" -ForegroundColor White
        Write-Host "  Path: $($setupFile.FullName)" -ForegroundColor White
        Write-Host "  Size: $([math]::Round($setupFile.Length / 1MB, 2)) MB" -ForegroundColor White
        Write-Host ""
        Write-Host "Distribution Ready!" -ForegroundColor Green
        Write-Host "Users can double-click this file to install BGRemover." -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   Build Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
}

Write-Host ""
