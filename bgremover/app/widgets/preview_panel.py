"""Preview panel with before/after comparison"""

from pathlib import Path
from typing import Optional
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PIL import Image


class PreviewPanel(QWidget):
    """Panel for displaying image preview with before/after comparison"""
    
    def __init__(self, i18n, parent=None):
        super().__init__(parent)
        
        self.i18n = i18n
        self.current_before_image: Optional[Path] = None
        self.current_after_image: Optional[Path] = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title = QLabel(self.i18n.t("preview.title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; color: #e0e0e0;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Before/After Container
        preview_container = QHBoxLayout()
        preview_container.setSpacing(15)
        
        # Before section
        before_section = QVBoxLayout()
        before_title = QLabel(f"📷 {self.i18n.t('preview.before')}")
        before_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #14a085; padding: 5px;")
        before_title.setAlignment(Qt.AlignCenter)
        before_section.addWidget(before_title)
        
        self.before_image_label = QLabel(self.i18n.t("preview.no_image"))
        self.before_image_label.setAlignment(Qt.AlignCenter)
        self.before_image_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px dashed #555555;
                border-radius: 8px;
                padding: 20px;
                min-height: 400px;
                font-size: 14px;
                color: #999999;
            }
        """)
        self.before_image_label.setScaledContents(False)
        before_section.addWidget(self.before_image_label, stretch=1)
        
        preview_container.addLayout(before_section, stretch=1)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setStyleSheet("color: #555555;")
        preview_container.addWidget(separator)
        
        # After section
        after_section = QVBoxLayout()
        after_title = QLabel(f"✨ {self.i18n.t('preview.after')}")
        after_title.setStyleSheet("font-size: 15px; font-weight: bold; color: #2a9d3f; padding: 5px;")
        after_title.setAlignment(Qt.AlignCenter)
        after_section.addWidget(after_title)
        
        self.after_image_label = QLabel(self.i18n.t("preview.no_image"))
        self.after_image_label.setAlignment(Qt.AlignCenter)
        self.after_image_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 2px dashed #555555;
                border-radius: 8px;
                padding: 20px;
                min-height: 400px;
                font-size: 14px;
                color: #999999;
            }
        """)
        self.after_image_label.setScaledContents(False)
        after_section.addWidget(self.after_image_label, stretch=1)
        
        preview_container.addLayout(after_section, stretch=1)
        
        layout.addLayout(preview_container, stretch=1)
    
    def set_before_image(self, file_path: Path):
        """Set before image to preview"""
        try:
            self.current_before_image = file_path
            
            # Load and display image
            pixmap = QPixmap(str(file_path))
            
            # Scale to fit
            scaled_pixmap = pixmap.scaled(
                self.before_image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.before_image_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.before_image_label.setText(f"{self.i18n.t('preview.error')}: {str(e)}")
    
    def set_after_image(self, file_path: Path):
        """Set after image to preview"""
        try:
            self.current_after_image = file_path
            
            # Load and display image
            pixmap = QPixmap(str(file_path))
            
            # Scale to fit
            scaled_pixmap = pixmap.scaled(
                self.after_image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            self.after_image_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.after_image_label.setText(f"{self.i18n.t('preview.error')}: {str(e)}")
    
    def set_image(self, file_path: Path):
        """Set image to preview (backward compatibility - shows in before)"""
        self.set_before_image(file_path)
    
    def clear(self):
        """Clear preview"""
        self.current_before_image = None
        self.current_after_image = None
        self.before_image_label.clear()
        self.before_image_label.setText(self.i18n.t("preview.no_image"))
        self.after_image_label.clear()
        self.after_image_label.setText(self.i18n.t("preview.no_image"))
    
    def clear_after(self):
        """Clear only after preview"""
        self.current_after_image = None
        self.after_image_label.clear()
        self.after_image_label.setText(self.i18n.t("preview.no_image"))
    
    def resizeEvent(self, event):
        """Handle resize event"""
        super().resizeEvent(event)
        
        # Rescale before image if one is loaded
        if self.current_before_image and self.current_before_image.exists():
            pixmap = QPixmap(str(self.current_before_image))
            scaled_pixmap = pixmap.scaled(
                self.before_image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.before_image_label.setPixmap(scaled_pixmap)
        
        # Rescale after image if one is loaded
        if self.current_after_image and self.current_after_image.exists():
            pixmap = QPixmap(str(self.current_after_image))
            scaled_pixmap = pixmap.scaled(
                self.after_image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.after_image_label.setPixmap(scaled_pixmap)
