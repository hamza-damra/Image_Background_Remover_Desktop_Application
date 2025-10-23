"""
cx_Freeze setup script for creating MSI installer
"""
import sys
from pathlib import Path
from cx_Freeze import setup, Executable

# Base directory
base_dir = Path(__file__).parent

# Build options
build_exe_options = {
    "packages": [
        "PySide6",
        "rembg",
        "PIL",
        "cv2",
        "numpy",
        "onnxruntime",
        "pydantic",
        "loguru",
        "pooch",
    ],
    "includes": [
        "bgremover.app.main",
        "bgremover.app.ui.main_window",
        "bgremover.app.widgets.settings_panel",
        "bgremover.app.widgets.image_list_widget",
        "bgremover.app.widgets.preview_widget",
        "bgremover.app.core.pipeline",
        "bgremover.app.core.settings",
        "bgremover.app.core.batch_processor",
        "bgremover.app.ui.i18n_manager",
    ],
    "excludes": [
        "tkinter",
        "unittest",
        "email",
        "html",
        "http",
        "xml",
        "pydoc",
        "pymatting",
        "numba",
        "llvmlite",
    ],
    "include_files": [
        (str(base_dir / "bgremover" / "app" / "ui" / "i18n"), "lib/bgremover/app/ui/i18n"),
        (str(base_dir / "README_AR.md"), "README_AR.md"),
        (str(base_dir / "LICENSE"), "LICENSE"),
        (str(base_dir / "CREDITS.md"), "CREDITS.md"),
    ],
    "optimize": 2,
}

# MSI options
bdist_msi_options = {
    "add_to_path": False,
    "initial_target_dir": r"[ProgramFilesFolder]\BGRemover",
    "install_icon": None,  # Add icon path if you have one
    "upgrade_code": "{12345678-1234-5678-1234-567812345678}",  # Unique GUID for upgrades
}

# Base for GUI application (no console window)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

# Executable configuration
executables = [
    Executable(
        script="bgremover/app/main.py",
        base=base,
        target_name="BGRemover.exe",
        icon=None,  # Add icon path if you have one
        shortcut_name="BGRemover",
        shortcut_dir="DesktopFolder",
    )
]

# Setup configuration
setup(
    name="BGRemover",
    version="1.0.0",
    description="أداة إزالة الخلفية من الصور بتقنية الذكاء الاصطناعي",
    author="Eng. Hamza Damra - المهندس حمزة ضمرة",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": bdist_msi_options,
    },
    executables=executables,
)
