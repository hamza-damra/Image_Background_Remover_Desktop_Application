# Simple Installer Creator (Without WiX)
# إنشاء ملف تثبيت بسيط بدون WiX
# المهندس حمزة ضمرة - Eng. Hamza Damra

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Simple Installer Creation Tool    " -ForegroundColor Cyan
Write-Host "  المهندس حمزة ضمرة                 " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if executable exists
if (!(Test-Path "dist\BGRemover\BGRemover.exe")) {
    Write-Host "❌ Executable not found!" -ForegroundColor Red
    Write-Host "Please run build_exe.ps1 first." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run: .\build_exe.ps1" -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ Executable found" -ForegroundColor Green
Write-Host ""

# Create installer directory
$installerDir = "BGRemover_Installer"
Write-Host "📁 Creating installer package..." -ForegroundColor Cyan

if (Test-Path $installerDir) {
    Remove-Item -Recurse -Force $installerDir
}
New-Item -ItemType Directory -Path $installerDir | Out-Null

# Copy files
Write-Host "  Copying application files..." -ForegroundColor Yellow
Copy-Item -Path "dist\BGRemover\*" -Destination $installerDir -Recurse

# Create installer script
Write-Host "  Creating installation script..." -ForegroundColor Yellow
$installScript = @'
# Background Remover Pro - Installer
# المهندس حمزة ضمرة - Eng. Hamza Damra

$ErrorActionPreference = "Stop"

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Background Remover Pro Installer  " -ForegroundColor Cyan
Write-Host "  المهندس حمزة ضمرة                 " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check admin rights
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (!$isAdmin) {
    Write-Host "⚠️  Running without administrator privileges" -ForegroundColor Yellow
    Write-Host "   Installation will be for current user only" -ForegroundColor Yellow
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
Write-Host "📦 Installing Background Remover Pro..." -ForegroundColor Cyan

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
$Shortcut.Description = "Background Remover Pro - AI-Powered Background Removal"
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
Write-Host "✅ Background Remover Pro has been uninstalled." -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
"@
$uninstallScript | Out-File -FilePath "$defaultPath\uninstall.ps1" -Encoding UTF8

Write-Host ""
Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run Background Remover from:" -ForegroundColor Cyan
Write-Host "  • Desktop shortcut" -ForegroundColor White
Write-Host "  • Start menu" -ForegroundColor White
Write-Host "  • $defaultPath\BGRemover.exe" -ForegroundColor White
Write-Host ""
Write-Host "To uninstall, run: $defaultPath\uninstall.ps1" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"
'@

$installScript | Out-File -FilePath "$installerDir\install.ps1" -Encoding UTF8

# Create README
Write-Host "  Creating README..." -ForegroundColor Yellow
$readmeContent = @"
# Background Remover Pro - Installation Package
# إزالة الخلفيات الاحترافي - حزمة التثبيت

المهندس حمزة ضمرة - Eng. Hamza Damra

## Installation / التثبيت

### English:
1. Right-click on `install.ps1`
2. Select "Run with PowerShell"
3. Follow the installation prompts
4. Launch from Desktop or Start Menu

### العربية:
1. انقر بزر الماوس الأيمن على `install.ps1`
2. اختر "Run with PowerShell"
3. اتبع تعليمات التثبيت
4. شغّل البرنامج من سطح المكتب أو قائمة ابدأ

## System Requirements / متطلبات النظام

- Windows 10/11 (64-bit)
- 4 GB RAM minimum
- 500 MB free disk space

## Developer / المطور

Eng. Hamza Damra
المهندس حمزة ضمرة

© 2025 All Rights Reserved
"@
$readmeContent | Out-File -FilePath "$installerDir\README.txt" -Encoding UTF8

# Create archive
Write-Host ""
Write-Host "📦 Creating ZIP archive..." -ForegroundColor Cyan
$archiveName = "BGRemover_Setup_v1.0.0.zip"
if (Test-Path $archiveName) {
    Remove-Item $archiveName -Force
}
Compress-Archive -Path "$installerDir\*" -DestinationPath $archiveName

Write-Host ""
Write-Host "✅ Installation package created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Package: .\$archiveName" -ForegroundColor Cyan
Write-Host "📁 Folder:  .\$installerDir\" -ForegroundColor Cyan
Write-Host ""
Write-Host "Distribution Instructions:" -ForegroundColor Yellow
Write-Host "  1. Share the ZIP file with users" -ForegroundColor White
Write-Host "  2. Users extract the ZIP" -ForegroundColor White
Write-Host "  3. Users run 'install.ps1' with PowerShell" -ForegroundColor White
Write-Host ""
Write-Host "✨ Ready for distribution!" -ForegroundColor Green
Write-Host "جاهز للتوزيع!" -ForegroundColor Green
Write-Host ""
