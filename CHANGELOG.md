# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-23

### Added
- Initial release of Background Remover
- Desktop GUI application with PySide6
- Batch processing with queue management
- Drag and drop support
- Multiple output formats (PNG, WebP, JPEG)
- Background options:
  - Transparent background
  - Solid color background
  - Image background replacement
- Canvas resizing and centering
- Image refinement options:
  - Alpha matting
  - Small object removal
  - Edge smoothing
  - Feathering
- Built-in presets:
  - Transparent - Web
  - Marketplace 1600×1600
  - Product - White Background
  - Social Media Square
  - Product Photography
  - Catalog / Print
- Custom preset creation and management
- Arabic and English language support with RTL
- Dark and light theme support
- Before/after preview panel
- Command-line interface (CLI)
- Comprehensive unit tests
- PyInstaller build configuration
- Automatic model download and verification
- Processing history
- Settings persistence
- Keyboard shortcuts
- Error handling and user feedback

### Technical
- U²-Net model for background removal
- ONNX Runtime for inference
- Local processing (no cloud services)
- Multi-threaded batch processing
- Pydantic for settings validation
- Loguru for logging
- Cross-platform support (Windows, macOS, Linux)

### Documentation
- Comprehensive README with setup instructions
- BUILD.md with detailed build instructions
- CONTRIBUTING.md for contributors
- Code documentation and docstrings
- Sample test suite

## [Unreleased]

### Planned Features
- GPU acceleration support
- Additional models (U²-Net Human Seg, etc.)
- Video background removal
- Gradient background generation
- Smart auto-crop
- Batch preset application
- Processing history with re-export
- More built-in presets
- Plugin system
- Integration with cloud storage
- macOS and Linux native packaging
- Installer creation (MSI, DMG, DEB)

---

## Release Notes

### Version 1.0.0

This is the first stable release of Background Remover. The application is fully functional and ready for production use.

**Key Features:**
- Professional background removal using AI
- Complete offline operation
- Bilingual interface (Arabic/English)
- Batch processing capabilities
- Flexible output options
- Cross-platform compatibility

**Known Issues:**
- First run requires internet for model download (~176MB)
- Alpha matting can be slow on older CPUs
- Very high-resolution images (>8000px) may cause memory issues

**System Requirements:**
- Windows 10/11, macOS 10.15+, or Linux
- Python 3.8 or higher
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

**How to Update:**
- Download the latest release
- Replace the executable or pull from git
- Settings and presets are preserved

---

For detailed changes, see the [commit history](https://github.com/yourusername/bgremover/commits/main).
