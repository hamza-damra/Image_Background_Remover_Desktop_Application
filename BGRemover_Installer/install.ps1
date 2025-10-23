# Background Remover Pro - Installer
# Eng. Hamza Damra

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Background Remover Pro Installer  " -ForegroundColor Cyan
Write-Host "  Eng. Hamza Damra                  " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Host "Running without administrator privileges" -ForegroundColor Yellow
    Write-Host "Installation will be for current user only" -ForegroundColor Yellow
    Write-Host ""
}

# Get installation directory
$defaultPath = "$env:LOCALAPPDATA\Programs\BGRemover"
if ($isAdmin) {
    $defaultPath = "$env:ProgramFiles\Hamza Damra\Background Remover Pro"
}

Write-Host "Installation location:" -ForegroundColor Cyan
Write-Host $defaultPath -ForegroundColor White
Write-Host ""
$confirm = Read-Host "Continue? (Y/N)"

if ($confirm -ne "Y" -and $confirm -ne "y") {
    Write-Host "Installation cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Installing Background Remover Pro..." -ForegroundColor Cyan

# Create installation directory
if (!(Test-Path $defaultPath)) {
    New-Item -ItemType Directory -Path $defaultPath -Force | Out-Null
}

# Copy files
Write-Host "  Copying files..." -ForegroundColor Yellow
$currentDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Copy-Item -Path "$currentDir\*" -Destination $defaultPath -Recurse -Force -Exclude "install.ps1"

# Create desktop shortcut
Write-Host "  Creating desktop shortcut..." -ForegroundColor Yellow
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut("$env:USERPROFILE\Desktop\Background Remover.lnk")
$Shortcut.TargetPath = "$defaultPath\BGRemover.exe"
$Shortcut.WorkingDirectory = $defaultPath
$Shortcut.Description = "Background Remover Pro - AI Background Removal"
$Shortcut.Save()

# Create start menu shortcut
Write-Host "  Creating start menu shortcut..." -ForegroundColor Yellow
$startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs"
if ($isAdmin) {
    $startMenuPath = "$env:ProgramData\Microsoft\Windows\Start Menu\Programs"
}
$startMenuFolder = "$startMenuPath\Background Remover Pro"
if (!(Test-Path $startMenuFolder)) {
    New-Item -ItemType Directory -Path $startMenuFolder -Force | Out-Null
}
$Shortcut = $WshShell.CreateShortcut("$startMenuFolder\Background Remover.lnk")
$Shortcut.TargetPath = "$defaultPath\BGRemover.exe"
$Shortcut.WorkingDirectory = $defaultPath
$Shortcut.Description = "Background Remover Pro"
$Shortcut.Save()

# Create uninstaller
Write-Host "  Creating uninstaller..." -ForegroundColor Yellow
$uninstallScript = @"
# Uninstaller for Background Remover Pro

`$installPath = "$defaultPath"
`$shortcuts = @(
    "`$env:USERPROFILE\Desktop\Background Remover.lnk",
    "$startMenuFolder\Background Remover.lnk"
)

Write-Host "Uninstalling Background Remover Pro..." -ForegroundColor Yellow

foreach (`$shortcut in `$shortcuts) {
    if (Test-Path `$shortcut) {
        Remove-Item -Path `$shortcut -Force
        Write-Host "  Removed shortcut: `$shortcut" -ForegroundColor Gray
    }
}

if (Test-Path `$installPath) {
    Remove-Item -Path `$installPath -Recurse -Force
    Write-Host "  Removed application files" -ForegroundColor Gray
}

if (Test-Path "$startMenuFolder") {
    Remove-Item -Path "$startMenuFolder" -Recurse -Force
}

Write-Host ""
Write-Host "Background Remover Pro has been uninstalled." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
"@
$uninstallScript | Out-File -FilePath "$defaultPath\uninstall.ps1" -Encoding UTF8

Write-Host ""
Write-Host "Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run Background Remover from:" -ForegroundColor Cyan
Write-Host "  - Desktop shortcut" -ForegroundColor White
Write-Host "  - Start menu" -ForegroundColor White
Write-Host "  - $defaultPath\BGRemover.exe" -ForegroundColor White
Write-Host ""
Write-Host "To uninstall, run: $defaultPath\uninstall.ps1" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"
