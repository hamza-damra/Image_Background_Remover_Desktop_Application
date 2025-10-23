# 🚀 Build and Run Guide

**Developer:** المهندس حمزة ضمرة - Eng. Hamza Damra

---

## Quick Start (Development)

### 1. Setup Environment

```powershell
# Automated setup (Recommended)
.\setup.ps1

# Or manual setup:
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run the Application

```powershell
# Quick run
.\run.ps1

# Or manual:
python -m bgremover.app.main
```

---

## 📦 Building for Distribution

### Option 1: Simple Installer (Recommended) ✅

**No external tools required!**

```powershell
# Build everything at once
.\build_all.ps1

# This creates:
# - BGRemover_Setup_v1.0.0.zip (for distribution)
# - BGRemover_Installer\ (folder with all files)
```

**What you get:**
- ZIP file ready to share
- Auto-install script for users
- Desktop & Start Menu shortcuts
- Clean uninstaller

**For end users:**
1. Extract the ZIP
2. Run `install.ps1` with PowerShell
3. Follow the prompts

---

### Option 2: MSI Installer (Professional)

**Requires:** [WiX Toolset v3.11](https://wixtoolset.org/releases/)

```powershell
# Build with MSI
.\build_all.ps1 -CreateMSI

# This creates:
# - BGRemover_Setup.msi
```

**What you get:**
- Professional MSI installer
- Shows in Add/Remove Programs
- Standard Windows installation
- Official uninstaller

**For end users:**
1. Double-click `BGRemover_Setup.msi`
2. Follow installation wizard
3. Done!

---

## 🔨 Step-by-Step Build Process

### Step 1: Build Executable Only

```powershell
.\build_exe.ps1
```

**This will:**
- Activate virtual environment
- Install PyInstaller if needed
- Build executable with PyInstaller
- Copy additional files
- Create models directory

**Output:** `dist\BGRemover\BGRemover.exe`

### Step 2: Create Installer Package

```powershell
# For Simple Installer
.\create_installer_simple.ps1

# For MSI Installer (requires WiX)
.\create_msi.ps1
```

---

## 📋 Build Files Explained

### Configuration Files

- **bgremover.spec** - PyInstaller configuration
- **version_info.txt** - Executable version info
- **installer.wxs** - WiX MSI configuration (for MSI only)

### Build Scripts

- **build_exe.ps1** - Builds the executable
- **create_installer_simple.ps1** - Creates ZIP installer
- **create_msi.ps1** - Creates MSI installer
- **build_all.ps1** - All-in-one build script

### For detailed instructions, see: [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md)

## Testing

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=bgremover --cov-report=html

# Run specific test file
pytest tests/test_pipeline.py -v
```

## CLI Usage

```powershell
# Process images from command line
python -m bgremover.cli --input "path/to/images" --output "path/to/output" --preset marketplace

# Options:
#   --input: Input directory with images
#   --output: Output directory
#   --preset: Preset name (transparent, marketplace, white_bg, etc.)
#   --bg-color: Background color (hex: #FFFFFF)
#   --size: Output size (WIDTHxHEIGHT, e.g., 1600x1600)
#   --lang: Language (ar/en)
```

## First Run

On first run, the application will:
1. Download the U²-Net model (~176MB)
2. Verify the model checksum
3. Store it in the `models/` directory

This only happens once. Subsequent runs will use the cached model.

## Troubleshooting

### "Model not found" error

The model will be downloaded automatically. Ensure you have:
- Internet connection (first run only)
- ~200MB free disk space
- Write permissions in the application directory

### "Import Error" when running

Make sure all dependencies are installed:

```powershell
pip install -r requirements.txt
```

### Application doesn't start

Check Python version:

```powershell
python --version
# Should be 3.8 or higher
```

### Slow processing

- Close other applications to free up RAM
- Reduce batch size
- Disable alpha matting in quality settings

### Arabic text not displaying correctly

- Restart the application after changing language
- Ensure translation files exist in `bgremover/app/ui/i18n/`

## Performance Tips

1. **Use presets**: They're optimized for common use cases
2. **Batch processing**: Process multiple images at once for efficiency
3. **Disable alpha matting**: Faster processing at slight quality cost
4. **Adjust worker count**: Settings → Max Workers (default: 4)

## File Structure

```
dist/BackgroundRemover/
├── BackgroundRemover.exe      # Main executable
├── models/
│   └── u2net.onnx            # AI model (downloaded on first run)
├── bgremover/
│   └── app/
│       └── ui/
│           └── i18n/         # Translation files
└── [various DLLs and dependencies]
```

## Command Line Arguments

```powershell
python -m bgremover.app.main [OPTIONS]

Options:
  --lang LANG        Set language (en/ar)
  --theme THEME      Set theme (dark/light/auto)
  --debug            Enable debug logging
```

## Building for Other Platforms

### macOS

```bash
# Install dependencies
pip install -r requirements.txt

# Build
pyinstaller build/pyinstaller_mac.spec

# Create DMG
hdiutil create -volname "Background Remover" \
  -srcfolder dist/BackgroundRemover.app \
  -ov -format UDZO \
  dist/BackgroundRemover.dmg
```

### Linux

```bash
# Install dependencies
pip install -r requirements.txt

# Build
pyinstaller build/pyinstaller_linux.spec

# Create AppImage (requires appimagetool)
# Follow AppImage packaging guidelines
```

## Environment Variables

- `BGREMOVER_DATA_DIR`: Override data directory (default: `~/.bgremover`)
- `BGREMOVER_LOG_LEVEL`: Set log level (DEBUG/INFO/WARNING/ERROR)

## Development

### Code Style

```powershell
# Format code
black bgremover/

# Lint
flake8 bgremover/
```

### Adding New Presets

Edit `bgremover/app/core/presets.py` and add to `BUILTIN_PRESETS`.

### Adding Translations

1. Add translations to `bgremover/app/ui/i18n/<lang>.json`
2. Restart application

## Support

For issues, please check:
1. This guide
2. README.md
3. GitHub Issues

---

Made with ❤️ for developers and designers
