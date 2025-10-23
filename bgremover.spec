# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Background Remover
المهندس حمزة ضمرة - Eng. Hamza Damra
"""

import sys
from pathlib import Path

block_cipher = None

# Get the project root directory
project_root = Path.cwd()
app_dir = project_root / 'bgremover'

# Collect all data files
datas = [
    (str(app_dir / 'app' / 'ui' / 'i18n' / '*.json'), 'bgremover/app/ui/i18n'),
    (str(app_dir / 'app' / 'ui' / 'assets'), 'bgremover/app/ui/assets'),
]

# Hidden imports for modules that PyInstaller might miss
hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'rembg',
    'onnxruntime',
    'scipy',
    'scipy.ndimage',
    'PIL',
    'PIL.Image',
    'cv2',
    'numpy',
    'pydantic',
    'loguru',
    'requests',
    'pooch',
]

a = Analysis(
    ['bgremover/app/main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'pytest',
        'test',
        'tkinter',
        'matplotlib',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BGRemover',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(app_dir / 'app' / 'ui' / 'assets' / 'icon.ico') if (app_dir / 'app' / 'ui' / 'assets' / 'icon.ico').exists() else None,
    version='version_info.txt',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BGRemover',
)
