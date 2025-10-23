# Install WiX Toolset Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   WiX Toolset Installer" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script requires administrator privileges." -ForegroundColor Red
    Write-Host "Please right-click and select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Check if WiX is already installed
Write-Host "Checking for existing WiX installation..." -ForegroundColor Yellow

$wixPath = Get-Command candle.exe -ErrorAction SilentlyContinue

if ($wixPath) {
    Write-Host "WiX Toolset is already installed at: $($wixPath.Source)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press any key to continue..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

# Install WiX using winget
Write-Host "Installing WiX Toolset v3.14..." -ForegroundColor Green
Write-Host ""

try {
    # Download WiX installer
    $wixUrl = "https://github.com/wixtoolset/wix3/releases/download/wix3141rtm/wix314.exe"
    $wixInstaller = "$env:TEMP\wix314.exe"
    
    Write-Host "Downloading WiX Toolset..." -ForegroundColor Yellow
    Invoke-WebRequest -Uri $wixUrl -OutFile $wixInstaller -UseBasicParsing
    
    Write-Host "Installing WiX Toolset..." -ForegroundColor Yellow
    Start-Process -FilePath $wixInstaller -ArgumentList "/install", "/quiet", "/norestart" -Wait
    
    # Clean up
    Remove-Item $wixInstaller -Force
    
    # Add WiX to PATH
    $wixBinPath = "${env:ProgramFiles(x86)}\WiX Toolset v3.14\bin"
    
    if (Test-Path $wixBinPath) {
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        if ($currentPath -notlike "*$wixBinPath*") {
            [Environment]::SetEnvironmentVariable("Path", "$currentPath;$wixBinPath", "Machine")
            $env:Path += ";$wixBinPath"
        }
        
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "   WiX Toolset Installed Successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "Installation path: $wixBinPath" -ForegroundColor White
        Write-Host ""
        Write-Host "Please restart your PowerShell terminal for changes to take effect." -ForegroundColor Yellow
    } else {
        Write-Host "Installation completed but WiX path not found." -ForegroundColor Yellow
        Write-Host "You may need to manually add WiX to your PATH." -ForegroundColor Yellow
    }
    
} catch {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   Installation Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please download and install WiX manually from:" -ForegroundColor Yellow
    Write-Host "https://github.com/wixtoolset/wix3/releases" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
