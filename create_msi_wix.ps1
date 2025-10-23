# Create MSI Installer using WiX Toolset
# This script creates a Windows MSI installer from the PyInstaller build

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BGRemover MSI Creator" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if WiX is installed
Write-Host "Checking for WiX Toolset..." -ForegroundColor Yellow
$candle = Get-Command candle.exe -ErrorAction SilentlyContinue
$light = Get-Command light.exe -ErrorAction SilentlyContinue

if (-not $candle -or -not $light) {
    Write-Host "ERROR: WiX Toolset not found!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install WiX Toolset first:" -ForegroundColor Yellow
    Write-Host "1. Run: .\install_wix.ps1 (as Administrator)" -ForegroundColor Cyan
    Write-Host "   OR" -ForegroundColor Yellow
    Write-Host "2. Download from: https://github.com/wixtoolset/wix3/releases" -ForegroundColor Cyan
    Write-Host ""
    exit 1
}

Write-Host "WiX Toolset found!" -ForegroundColor Green

# Check if PyInstaller build exists
Write-Host "Checking for PyInstaller build..." -ForegroundColor Yellow

if (-not (Test-Path "dist\BGRemover\BGRemover.exe")) {
    Write-Host "ERROR: PyInstaller build not found!" -ForegroundColor Red
    Write-Host "Please run: .\build_simple.ps1 first" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

Write-Host "PyInstaller build found!" -ForegroundColor Green
Write-Host ""

# Create WiX source file
Write-Host "Generating WiX configuration..." -ForegroundColor Yellow

$wixContent = @"
<?xml version="1.0" encoding="UTF-8"?>
<Wix xmlns="http://schemas.microsoft.com/wix/2006/wi">
  <Product Id="*" 
           Name="BGRemover" 
           Language="1033" 
           Version="1.0.0.0" 
           Manufacturer="Eng. Hamza Damra" 
           UpgradeCode="12345678-1234-5678-1234-567812345678">
    
    <Package InstallerVersion="200" 
             Compressed="yes" 
             InstallScope="perMachine" 
             Description="Background Removal Tool - AI Powered"
             Comments="Created by Eng. Hamza Damra" />

    <MajorUpgrade DowngradeErrorMessage="A newer version is already installed." />
    <MediaTemplate EmbedCab="yes" />

    <Feature Id="ProductFeature" Title="BGRemover" Level="1">
      <ComponentGroupRef Id="ProductComponents" />
      <ComponentRef Id="ApplicationShortcut" />
      <ComponentRef Id="DesktopShortcut" />
    </Feature>

    <Directory Id="TARGETDIR" Name="SourceDir">
      <Directory Id="ProgramFilesFolder">
        <Directory Id="INSTALLFOLDER" Name="BGRemover" />
      </Directory>
      
      <Directory Id="ProgramMenuFolder">
        <Directory Id="ApplicationProgramsFolder" Name="BGRemover"/>
      </Directory>
      
      <Directory Id="DesktopFolder" Name="Desktop" />
    </Directory>

    <DirectoryRef Id="ApplicationProgramsFolder">
      <Component Id="ApplicationShortcut" Guid="11111111-1111-1111-1111-111111111111">
        <Shortcut Id="ApplicationStartMenuShortcut"
                  Name="BGRemover"
                  Description="Background Removal Tool"
                  Target="[INSTALLFOLDER]BGRemover.exe"
                  WorkingDirectory="INSTALLFOLDER"/>
        <RemoveFolder Id="CleanUpShortCut" Directory="ApplicationProgramsFolder" On="uninstall"/>
        <RegistryValue Root="HKCU" Key="Software\BGRemover" Name="installed" Type="integer" Value="1" KeyPath="yes"/>
      </Component>
    </DirectoryRef>

    <DirectoryRef Id="DesktopFolder">
      <Component Id="DesktopShortcut" Guid="22222222-2222-2222-2222-222222222222">
        <Shortcut Id="DesktopShortcut"
                  Name="BGRemover"
                  Description="Background Removal Tool"
                  Target="[INSTALLFOLDER]BGRemover.exe"
                  WorkingDirectory="INSTALLFOLDER"/>
        <RegistryValue Root="HKCU" Key="Software\BGRemover" Name="desktop" Type="integer" Value="1" KeyPath="yes"/>
      </Component>
    </DirectoryRef>

    <ComponentGroup Id="ProductComponents" Directory="INSTALLFOLDER">
      <!-- Main executable -->
      <Component Id="BGRemoverExe" Guid="33333333-3333-3333-3333-333333333333">
        <File Id="BGRemoverExeFile" Source="dist\BGRemover\BGRemover.exe" KeyPath="yes" />
      </Component>
    </ComponentGroup>

  </Product>
</Wix>
"@

$wixContent | Out-File -FilePath "bgremover_msi.wxs" -Encoding UTF8

# Use heat.exe to harvest all files from dist\BGRemover
Write-Host "Harvesting application files..." -ForegroundColor Yellow
& heat.exe dir "dist\BGRemover" -cg ProductComponents -gg -scom -sreg -sfrag -srd -dr INSTALLFOLDER -var var.SourceDir -out bgremover_files.wxs

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to harvest files!" -ForegroundColor Red
    exit 1
}

# Compile WiX source
Write-Host "Compiling WiX source..." -ForegroundColor Yellow
& candle.exe -dSourceDir="dist\BGRemover" bgremover_msi.wxs bgremover_files.wxs -out build\

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: WiX compilation failed!" -ForegroundColor Red
    exit 1
}

# Link to create MSI
Write-Host "Linking MSI installer..." -ForegroundColor Yellow
& light.exe -out "BGRemover_v1.0.0.msi" build\bgremover_msi.wixobj build\bgremover_files.wixobj -ext WixUIExtension

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   MSI Created Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    $msiFile = Get-Item "BGRemover_v1.0.0.msi"
    Write-Host "MSI Installer:" -ForegroundColor Cyan
    Write-Host "  File: $($msiFile.Name)" -ForegroundColor White
    Write-Host "  Path: $($msiFile.FullName)" -ForegroundColor White
    Write-Host "  Size: $([math]::Round($msiFile.Length / 1MB, 2)) MB" -ForegroundColor White
    Write-Host ""
    Write-Host "You can now distribute this MSI file!" -ForegroundColor Green
    Write-Host "Users can double-click to install." -ForegroundColor Green
    
    # Clean up temp files
    Write-Host ""
    Write-Host "Cleaning up temporary files..." -ForegroundColor Yellow
    Remove-Item "bgremover_msi.wxs" -Force -ErrorAction SilentlyContinue
    Remove-Item "bgremover_files.wxs" -Force -ErrorAction SilentlyContinue
    Remove-Item "build\*.wixobj" -Force -ErrorAction SilentlyContinue
    Remove-Item "build\*.wixpdb" -Force -ErrorAction SilentlyContinue
    
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "   MSI Creation Failed!" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

Write-Host ""
