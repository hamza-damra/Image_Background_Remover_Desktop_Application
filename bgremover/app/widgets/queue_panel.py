"""Queue panel for managing processing tasks"""

from pathlib import Path
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QListWidgetItem,
    QPushButton, QLabel, QHBoxLayout
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QDragEnterEvent, QDropEvent


class QueuePanel(QWidget):
    """Panel for displaying and managing the processing queue"""
    
    files_added = Signal(int)  # count
    item_selected = Signal(Path)  # file_path
    
    def __init__(self, i18n, parent=None):
        super().__init__(parent)
        
        self.i18n = i18n
        self.files: List[Path] = []
        
        self._setup_ui()
        
        # Enable drag and drop
        self.setAcceptDrops(True)
    
    def _setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(self.i18n.t("queue.title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; color: #e0e0e0;")
        layout.addWidget(title)
        
        # List widget
        self.list_widget = QListWidget()
        self.list_widget.setAlternatingRowColors(True)
        self.list_widget.itemClicked.connect(self._on_item_clicked)
        self.list_widget.setStyleSheet("font-size: 13px;")
        layout.addWidget(self.list_widget)
        
        # Info label
        self.info_label = QLabel(f"0 {self.i18n.t('queue.items')}")
        self.info_label.setStyleSheet("padding: 8px; font-size: 13px; color: #e0e0e0;")
        layout.addWidget(self.info_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton(self.i18n.t("queue.add_images"))
        add_btn.clicked.connect(self._on_add_clicked)
        button_layout.addWidget(add_btn)
        
        remove_btn = QPushButton(self.i18n.t("queue.remove_all"))
        remove_btn.clicked.connect(self.clear)
        button_layout.addWidget(remove_btn)
        
        layout.addLayout(button_layout)
        
        # Drag drop hint
        hint = QLabel(self.i18n.t("queue.drag_drop"))
        hint.setStyleSheet("color: gray; font-style: italic; padding: 10px;")
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint)
    
    def add_files(self, file_paths: List[Path]):
        """Add files to queue"""
        count = 0
        for file_path in file_paths:
            if file_path.is_file() and file_path.suffix.lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.webp']:
                if file_path not in self.files:
                    self.files.append(file_path)
                    
                    item = QListWidgetItem(file_path.name)
                    item.setData(Qt.UserRole, file_path)
                    item.setToolTip(str(file_path))
                    self.list_widget.addItem(item)
                    count += 1
        
        if count > 0:
            self._update_info()
            self.files_added.emit(count)
    
    def get_all_files(self) -> List[Path]:
        """Get all files in queue"""
        return self.files.copy()
    
    def get_file_by_id(self, task_id: int) -> Path:
        """Get file by task ID"""
        if 0 <= task_id < len(self.files):
            return self.files[task_id]
        return None
    
    def get_item_count(self) -> int:
        """Get number of items in queue"""
        return len(self.files)
    
    def clear(self):
        """Clear the queue"""
        self.files.clear()
        self.list_widget.clear()
        self._update_info()
    
    def update_item_status(self, task_id: int, status: str):
        """Update item status"""
        if task_id < self.list_widget.count():
            item = self.list_widget.item(task_id)
            
            if status == "processing":
                item.setBackground(Qt.yellow)
                item.setText(f"⏳ {item.data(Qt.UserRole).name}")
            elif status == "completed":
                item.setBackground(Qt.green)
                item.setText(f"✓ {item.data(Qt.UserRole).name}")
            elif status == "failed":
                item.setBackground(Qt.red)
                item.setText(f"✗ {item.data(Qt.UserRole).name}")
    
    def _update_info(self):
        """Update info label"""
        self.info_label.setText(f"{len(self.files)} {self.i18n.t('queue.items')}")
    
    def _on_item_clicked(self, item: QListWidgetItem):
        """Handle item clicked"""
        file_path = item.data(Qt.UserRole)
        self.item_selected.emit(file_path)
    
    def _on_add_clicked(self):
        """Handle add button clicked"""
        # This would open file dialog, but we'll let the main window handle it
        pass
    
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event: QDropEvent):
        """Handle drop"""
        files = []
        for url in event.mimeData().urls():
            file_path = Path(url.toLocalFile())
            if file_path.is_file():
                files.append(file_path)
            elif file_path.is_dir():
                # Add all images from directory
                for ext in ['*.png', '*.jpg', '*.jpeg', '*.bmp', '*.webp']:
                    files.extend(file_path.glob(ext))
        
        if files:
            self.add_files(files)
