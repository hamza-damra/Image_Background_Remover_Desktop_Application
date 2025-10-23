# Create MSI Installer
# إنشاء ملف تثبيت MSI
# المهندس حمزة ضمرة - Eng. Hamza Damra

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "   MSI Installer Creation Tool      " -ForegroundColor Cyan
Write-Host "  المهندس حمزة ضمرة                 " -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check if WiX Toolset is installed
Write-Host "🔍 Checking for WiX Toolset..." -ForegroundColor Cyan

$wixPath = "C:\Program Files (x86)\WiX Toolset v3.11\bin"
if (!(Test-Path $wixPath)) {
    Write-Host ""
    Write-Host "❌ WiX Toolset not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "WiX Toolset is required to create MSI installers." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please download and install WiX Toolset from:" -ForegroundColor Yellow
    Write-Host "https://wixtoolset.org/releases/" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Alternative: Use the simplified installer script instead:" -ForegroundColor Yellow
    Write-Host ".\create_installer_simple.ps1" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

# Check if executable exists
if (!(Test-Path "dist\BGRemover\BGRemover.exe")) {
    Write-Host "❌ Executable not found!" -ForegroundColor Red
    Write-Host "Please run build_exe.ps1 first to build the executable." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Run: .\build_exe.ps1" -ForegroundColor Cyan
    exit 1
}

Write-Host "✓ WiX Toolset found" -ForegroundColor Green
Write-Host "✓ Executable found" -ForegroundColor Green
Write-Host ""

# Create license RTF file
Write-Host "✓ Creating license file..." -ForegroundColor Green
$licenseContent = @"
{\rtf1\ansi\ansicpg1252\deff0\nouicompat{\fonttbl{\f0\fnil\fcharset0 Calibri;}}
{\*\generator Riched20 10.0.19041}\viewkind4\uc1 
\pard\sa200\sl276\slmult1\b\f0\fs28\lang9 MIT License\b0\fs22\par
\par
Copyright (c) 2025 Hamza Damra\par
\par
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\par
\par
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\par
\par
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\par
\par
\b Developer:\b0  Eng. Hamza Damra\par
}
"@
$licenseContent | Out-File -FilePath "license.rtf" -Encoding ASCII

Write-Host "✓ License file created" -ForegroundColor Green
Write-Host ""

# Compile WiX
Write-Host "🔨 Compiling installer (Step 1/2)..." -ForegroundColor Cyan
& "$wixPath\candle.exe" installer.wxs -out installer.wixobj

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Compilation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Compilation successful" -ForegroundColor Green
Write-Host ""

# Link WiX
Write-Host "🔗 Linking installer (Step 2/2)..." -ForegroundColor Cyan
& "$wixPath\light.exe" installer.wixobj -ext WixUIExtension -out "BGRemover_Setup.msi"

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "❌ Linking failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "✅ MSI Installer created successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📦 Installer: .\BGRemover_Setup.msi" -ForegroundColor Cyan
Write-Host ""
Write-Host "You can now distribute this MSI file!" -ForegroundColor Green
Write-Host "المستخدمون يمكنهم تثبيت البرنامج بسهولة الآن!" -ForegroundColor Green
Write-Host ""
