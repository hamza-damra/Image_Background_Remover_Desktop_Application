"""Installation verification script"""

import sys

print("🔍 Checking Background Remover Installation...")
print("=" * 50)

errors = []
warnings = []

# Check Python version
print("\n1. Python Version:")
version_info = sys.version_info
print(f"   ✓ Python {version_info.major}.{version_info.minor}.{version_info.micro}")

if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 8):
    errors.append("Python 3.8+ is required")

# Check required packages
print("\n2. Required Packages:")

required_packages = [
    ("PySide6", "PySide6"),
    ("rembg", "rembg"),
    ("onnxruntime", "onnxruntime"),
    ("PIL", "Pillow"),
    ("cv2", "opencv-python"),
    ("numpy", "numpy"),
    ("pydantic", "pydantic"),
    ("loguru", "loguru"),
    ("pytest", "pytest"),
]

for import_name, package_name in required_packages:
    try:
        __import__(import_name)
        print(f"   ✓ {package_name}")
    except ImportError:
        print(f"   ✗ {package_name} - NOT INSTALLED")
        errors.append(f"Missing package: {package_name}")

# Check project structure
print("\n3. Project Structure:")

from pathlib import Path

project_root = Path(__file__).parent
required_dirs = [
    "bgremover",
    "bgremover/app",
    "bgremover/app/core",
    "bgremover/app/ui",
    "bgremover/app/widgets",
    "models",
    "tests",
    "build",
]

for dir_path in required_dirs:
    full_path = project_root / dir_path
    if full_path.exists():
        print(f"   ✓ {dir_path}/")
    else:
        print(f"   ✗ {dir_path}/ - MISSING")
        errors.append(f"Missing directory: {dir_path}")

# Check critical files
print("\n4. Critical Files:")

critical_files = [
    "bgremover/app/main.py",
    "bgremover/app/core/pipeline.py",
    "bgremover/app/ui/main_window.py",
    "requirements.txt",
    "README.md",
]

for file_path in critical_files:
    full_path = project_root / file_path
    if full_path.exists():
        print(f"   ✓ {file_path}")
    else:
        print(f"   ✗ {file_path} - MISSING")
        errors.append(f"Missing file: {file_path}")

# Check translations
print("\n5. Translation Files:")

i18n_files = ["en.json", "ar.json"]
i18n_dir = project_root / "bgremover" / "app" / "ui" / "i18n"

for file_name in i18n_files:
    full_path = i18n_dir / file_name
    if full_path.exists():
        print(f"   ✓ {file_name}")
    else:
        print(f"   ✗ {file_name} - MISSING")
        warnings.append(f"Missing translation: {file_name}")

# Summary
print("\n" + "=" * 50)

if errors:
    print("❌ INSTALLATION INCOMPLETE")
    print("\nErrors:")
    for error in errors:
        print(f"   • {error}")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"   • {warning}")
    
    print("\n💡 To fix:")
    print("   1. Run: setup.ps1")
    print("   2. Or manually: pip install -r requirements.txt")
    sys.exit(1)

elif warnings:
    print("⚠️  INSTALLATION INCOMPLETE (with warnings)")
    print("\nWarnings:")
    for warning in warnings:
        print(f"   • {warning}")
    print("\n✓ Core functionality should work")
    sys.exit(0)

else:
    print("✅ INSTALLATION COMPLETE")
    print("\n🚀 Ready to run!")
    print("\nNext steps:")
    print("   • Run GUI: python -m bgremover.app.main")
    print("   • Run CLI: python -m bgremover.cli --help")
    print("   • Run tests: pytest")
    print("   • Build app: pyinstaller build/pyinstaller.spec")
    sys.exit(0)
