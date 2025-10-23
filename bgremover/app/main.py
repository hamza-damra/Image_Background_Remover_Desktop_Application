"""Main application entry point"""

import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt, QTranslator, QLocale
from PySide6.QtGui import QIcon

from bgremover.app.core.logger import setup_logger
from bgremover.app.core.settings import Settings
from bgremover.app.ui.main_window import MainWindow


def main():
    """Main entry point for the application"""
    # Setup logger
    logger = setup_logger()
    logger.info("Starting Background Remover application...")
    
    # Enable High DPI scaling (Qt 6.10+ way)
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    # Create application
    app = QApplication(sys.argv)
    app.setApplicationName("إزالة الخلفيات")
    app.setOrganizationName("BGRemover")
    app.setApplicationVersion("1.0.0")
    
    # Enable RTL layout for Arabic
    app.setLayoutDirection(Qt.RightToLeft)
    
    # Set application icon
    icon_path = Path(__file__).parent / "ui" / "assets" / "icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))
    
    # Load settings
    try:
        settings = Settings.load()
        logger.info(f"Settings loaded. Language: {settings.language}")
    except Exception as e:
        logger.warning(f"Failed to load settings: {e}. Using defaults.")
        settings = Settings()
        settings.save()
    
    # Create and show main window
    try:
        window = MainWindow(settings)
        window.show()
        logger.info("Main window displayed successfully")
    except Exception as e:
        logger.error(f"Failed to create main window: {e}")
        sys.exit(1)
    
    # Run application
    exit_code = app.exec()
    logger.info(f"Application exited with code: {exit_code}")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
