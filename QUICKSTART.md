# ⚡ Quick Start Guide

## 5-Minute Setup

### Step 1: Install Python (if not installed)
Download from: https://www.python.org/downloads/
- Minimum version: Python 3.8
- ✅ Check "Add Python to PATH" during installation

### Step 2: Setup Project
```powershell
# Open PowerShell in project directory
cd "c:\Users\Hamza Damra\Documents\image manu"

# Run setup script
.\setup.ps1
```

**What this does:**
- Creates virtual environment
- Installs all dependencies
- Sets up directories
- ~5 minutes depending on internet speed

### Step 3: Run Application
```powershell
# Option 1: Use run script (recommended)
.\run.ps1

# Option 2: Manual run
python -m bgremover.app.main
```

**First run:**
- AI model will download automatically (~176MB)
- Takes 3-5 minutes (one-time only)
- Requires internet connection

---

## 🎯 First Task: Remove Your First Background

### 1. Add Images
- **Drag & drop** your images into the left panel
- Or click **"Open"** button

### 2. Choose Output Location
- Click **output directory** in toolbar
- Select where to save results

### 3. Select Settings (Optional)
Use a preset for quick start:
- Click **"Presets"** tab on right
- Select **"Transparent - Web"**
- Click **"Apply"**

### 4. Process
- Click **"Start Processing"**
- Wait for green checkmarks ✓
- Done! Check your output folder

---

## 🚀 Command Line (Advanced)

Process images from terminal:

```powershell
# Basic usage
python -m bgremover.cli --input ./photos --output ./results

# With preset
python -m bgremover.cli --input ./photos --output ./results --preset marketplace

# Custom settings
python -m bgremover.cli --input ./photos --output ./results --bg-color "#FFFFFF" --size 1600x1600
```

---

## ✅ Verify Installation

```powershell
python check_install.py
```

This checks:
- ✓ Python version
- ✓ Required packages
- ✓ Project structure
- ✓ Critical files

---

## 🐛 Quick Troubleshooting

### "python" not recognized
**Fix:** Add Python to PATH or use full path:
```powershell
C:\Python39\python.exe -m bgremover.app.main
```

### ModuleNotFoundError
**Fix:** Install dependencies:
```powershell
pip install -r requirements.txt
```

### Model download fails
**Fix:** Check internet connection, or download manually:
```powershell
# See models/README.md for manual download instructions
```

### Application crashes on start
**Fix:** Check Python version:
```powershell
python --version  # Should be 3.8+
```

---

## 📚 Learn More

- **Full Documentation:** [USER_GUIDE.md](USER_GUIDE.md)
- **Build Executable:** [BUILD.md](BUILD.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 💡 Pro Tips

1. **Use Presets** - Save time with ready-made configurations
2. **Batch Process** - Add multiple images at once
3. **Keyboard Shortcuts** - `Ctrl+O` to open, `Ctrl+Enter` to start
4. **Arabic Support** - Click EN/ع button to switch languages

---

**Need Help?**
- Check [USER_GUIDE.md](USER_GUIDE.md) for detailed instructions
- Open an issue on GitHub
- Review [BUILD.md](BUILD.md) for technical issues

---

**Ready to Start!** 🎉

Run: `.\run.ps1` or `python -m bgremover.app.main`
