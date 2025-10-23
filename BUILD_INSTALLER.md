# 📦 Building Installer for Background Remover Pro

**المهندس حمزة ضمرة - Eng. Hamza Damra**

---

## 🚀 Quick Start (3 Steps)

### 1. Check if ready to build

```powershell
.\check_build_ready.ps1
```

### 2. Build everything

```powershell
# Simple Installer (No external tools needed)
.\build_all.ps1

# OR

# MSI Installer (Requires WiX Toolset)
.\build_all.ps1 -CreateMSI
```

### 3. Distribute

Share the generated file:
- **Simple:** `BGRemover_Setup_v1.0.0.zip`
- **MSI:** `BGRemover_Setup.msi`

---

## 📚 Detailed Guide

See [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for comprehensive instructions.

---

## ⚡ Available Scripts

| Script | Description |
|--------|-------------|
| `check_build_ready.ps1` | Verify system is ready to build |
| `build_exe.ps1` | Build executable only |
| `create_installer_simple.ps1` | Create ZIP installer |
| `create_msi.ps1` | Create MSI installer (needs WiX) |
| `build_all.ps1` | All-in-one build script |

---

## 🎯 Common Commands

```powershell
# Full build (recommended)
.\build_all.ps1

# Build executable only
.\build_exe.ps1

# Create installer from existing build
.\build_all.ps1 -SkipBuild

# Create MSI installer
.\build_all.ps1 -CreateMSI
```

---

## 📦 Output Files

### Simple Installer
- `BGRemover_Setup_v1.0.0.zip` - Distribution package
- `BGRemover_Installer\` - Extracted files

### MSI Installer
- `BGRemover_Setup.msi` - Windows installer

### Executable
- `dist\BGRemover\BGRemover.exe` - Standalone executable
- `dist\BGRemover\` - All required files

---

## 🔧 Troubleshooting

### "Python not found"
Install Python 3.10+ from https://python.org

### "Virtual environment not found"
Run: `.\setup.ps1`

### "PyInstaller not found"
```powershell
.\venv\Scripts\Activate.ps1
pip install pyinstaller
```

### "WiX Toolset not found" (MSI only)
Download from: https://wixtoolset.org/releases/

Or use Simple Installer instead:
```powershell
.\build_all.ps1  # Without -CreateMSI flag
```

---

## ✅ Pre-Build Checklist

- [ ] Python 3.10+ installed
- [ ] Virtual environment created (`venv\`)
- [ ] Dependencies installed
- [ ] Application tested and working
- [ ] 2GB+ free disk space
- [ ] (MSI only) WiX Toolset installed

---

## 📄 Files Needed for Build

### Essential:
- `bgremover/` - Application code
- `bgremover.spec` - PyInstaller config
- `version_info.txt` - Version info
- `requirements.txt` - Dependencies

### For MSI (optional):
- `installer.wxs` - WiX configuration
- WiX Toolset installed

---

## 📧 Support

**Developer:** Eng. Hamza Damra - المهندس حمزة ضمرة

For issues or questions, refer to:
- [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) - Comprehensive guide
- [BUILD.md](BUILD.md) - Build documentation

---

**© 2025 Hamza Damra. All Rights Reserved.**
