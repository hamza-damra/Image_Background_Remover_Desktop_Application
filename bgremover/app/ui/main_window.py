"""Main application window"""

from pathlib import Path
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QToolBar, QPushButton, QFileDialog, QMessageBox, QLabel,
    QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QAction
from loguru import logger

from bgremover.app.core.settings import Settings, get_settings, update_settings
from bgremover.app.core.batch_worker import BatchWorker
from bgremover.app.ui.i18n_manager import get_i18n
from bgremover.app.widgets.queue_panel import QueuePanel
from bgremover.app.widgets.preview_panel import PreviewPanel
from bgremover.app.widgets.settings_panel import SettingsPanel


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, settings: Settings):
        super().__init__()
        
        self.settings = settings
        self.i18n = get_i18n(settings.language)
        self.batch_worker = BatchWorker(max_workers=settings.max_workers)
        
        self.output_dir = Path(settings.last_output_dir) if settings.last_output_dir else Path.home()
        
        self._setup_ui()
        self._connect_signals()
        self._apply_theme()
        self._apply_language()
        
        logger.info("Main window initialized")
    
    def _setup_ui(self):
        """Setup user interface"""
        self.setWindowTitle(self.i18n.t("app_name"))
        self.resize(self.settings.window_width, self.settings.window_height)
        
        if self.settings.window_maximized:
            self.showMaximized()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left panel - Queue
        self.queue_panel = QueuePanel(self.i18n)
        main_layout.addWidget(self.queue_panel, stretch=1)
        
        # Center panel - Preview
        self.preview_panel = PreviewPanel(self.i18n)
        main_layout.addWidget(self.preview_panel, stretch=2)
        
        # Right panel - Settings
        self.settings_panel = SettingsPanel(self.settings, self.i18n)
        main_layout.addWidget(self.settings_panel, stretch=1)
        
        # Create toolbar
        self._create_toolbar()
        
        # Create menu bar
        self._create_menubar()
        
        # Create status bar
        self.statusBar().showMessage(self.i18n.t("messages.model_ready"))
    
    def _create_toolbar(self):
        """Create main toolbar with improved buttons"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(28, 28))
        toolbar.setStyleSheet("""
            QToolBar {
                spacing: 8px;
                padding: 8px;
            }
        """)
        self.addToolBar(Qt.TopToolBarArea, toolbar)
        
        # Open button
        self.open_btn = QPushButton(f" 📁 {self.i18n.t('toolbar.open')}")
        self.open_btn.setShortcut("Ctrl+O")
        self.open_btn.setMinimumWidth(120)
        self.open_btn.setMinimumHeight(40)
        self.open_btn.clicked.connect(self._on_open_images)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d5f;
            }
        """)
        toolbar.addWidget(self.open_btn)
        
        toolbar.addSeparator()
        
        # Start button
        self.start_btn = QPushButton(f" ▶️ {self.i18n.t('toolbar.start')}")
        self.start_btn.setShortcut("Ctrl+Return")
        self.start_btn.setMinimumWidth(140)
        self.start_btn.setMinimumHeight(40)
        self.start_btn.clicked.connect(self._on_start_processing)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #2a9d3f;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #34c759;
            }
            QPushButton:pressed {
                background-color: #1f7d30;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        toolbar.addWidget(self.start_btn)
        
        # Pause button
        self.pause_btn = QPushButton(f" ⏸️ {self.i18n.t('toolbar.pause')}")
        self.pause_btn.setMinimumWidth(100)
        self.pause_btn.setMinimumHeight(40)
        self.pause_btn.clicked.connect(self._on_pause_processing)
        self.pause_btn.setEnabled(False)
        self.pause_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff9500;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ffaa33;
            }
            QPushButton:pressed {
                background-color: #cc7700;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        toolbar.addWidget(self.pause_btn)
        
        # Cancel button
        self.cancel_btn = QPushButton(f" ⛔ {self.i18n.t('toolbar.cancel')}")
        self.cancel_btn.setShortcut("Esc")
        self.cancel_btn.setMinimumWidth(100)
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.clicked.connect(self._on_cancel_processing)
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff3b30;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #ff5549;
            }
            QPushButton:pressed {
                background-color: #cc2f26;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
        """)
        toolbar.addWidget(self.cancel_btn)
        
        toolbar.addSeparator()
        
        # Clear button
        self.clear_btn = QPushButton(f" 🗑️ {self.i18n.t('toolbar.clear')}")
        self.clear_btn.setMinimumWidth(100)
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.clicked.connect(self._on_clear_queue)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #5e5e5e;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #737373;
            }
            QPushButton:pressed {
                background-color: #4a4a4a;
            }
        """)
        toolbar.addWidget(self.clear_btn)
        
        toolbar.addSeparator()
        
        # Output directory
        output_label = QLabel(f" {self.i18n.t('toolbar.output_dir')}: ")
        output_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #e0e0e0;")
        toolbar.addWidget(output_label)
        
        self.output_btn = QPushButton(f"📂 {str(self.output_dir.name)}")
        self.output_btn.setMinimumWidth(150)
        self.output_btn.setMinimumHeight(40)
        self.output_btn.setToolTip(str(self.output_dir))
        self.output_btn.clicked.connect(self._on_choose_output_dir)
        self.output_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #5e5e5e;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """)
        toolbar.addWidget(self.output_btn)
        
        # Add spacer
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        toolbar.addWidget(spacer)
    
    def _create_menubar(self):
        """Create menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(self.i18n.t("menu.file"))
        
        open_images_action = file_menu.addAction(self.i18n.t("menu.open_images"))
        open_images_action.setShortcut("Ctrl+O")
        open_images_action.triggered.connect(self._on_open_images)
        
        open_folder_action = file_menu.addAction(self.i18n.t("menu.open_folder"))
        open_folder_action.triggered.connect(self._on_open_folder)
        
        file_menu.addSeparator()
        
        exit_action = file_menu.addAction(self.i18n.t("menu.exit"))
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        
        # Help menu
        help_menu = menubar.addMenu(self.i18n.t("menu.help"))
        
        about_action = help_menu.addAction(self.i18n.t("menu.about"))
        about_action.triggered.connect(self._on_about)
    
    def _connect_signals(self):
        """Connect signals"""
        # Queue panel signals
        self.queue_panel.files_added.connect(self._on_files_added)
        self.queue_panel.item_selected.connect(self._on_item_selected)
        
        # Settings panel signals
        self.settings_panel.settings_changed.connect(self._on_settings_changed)
        
        # Batch worker signals
        self.batch_worker.task_started.connect(self._on_task_started)
        self.batch_worker.task_completed.connect(self._on_task_completed)
        self.batch_worker.task_failed.connect(self._on_task_failed)
        self.batch_worker.batch_progress.connect(self._on_batch_progress)
        self.batch_worker.batch_completed.connect(self._on_batch_completed)
    
    def _apply_theme(self):
        """Apply theme to window"""
        if self.settings.theme == "dark":
            self._apply_dark_theme()
        else:
            self._apply_light_theme()
    
    def _apply_dark_theme(self):
        """Apply dark theme"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #1e1e1e;
                color: #e0e0e0;
                font-size: 13px;
            }
            QToolBar {
                background-color: #2d2d2d;
                border-bottom: 1px solid #3d3d3d;
                padding: 10px;
                spacing: 10px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
                min-height: 32px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d5f;
            }
            QPushButton:disabled {
                background-color: #3d3d3d;
                color: #666666;
            }
            QMenuBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
                font-size: 13px;
                padding: 4px;
            }
            QMenuBar::item {
                padding: 8px 12px;
                background-color: transparent;
            }
            QMenuBar::item:selected {
                background-color: #0d7377;
                border-radius: 4px;
            }
            QMenu {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                font-size: 13px;
            }
            QMenu::item {
                padding: 8px 24px;
            }
            QMenu::item:selected {
                background-color: #0d7377;
            }
            QStatusBar {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border-top: 1px solid #3d3d3d;
                font-size: 13px;
                padding: 6px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 13px;
            }
            QListWidget {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                font-size: 13px;
                padding: 4px;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QListWidget::item:selected {
                background-color: #0d7377;
            }
            QListWidget::item:hover {
                background-color: #3d3d3d;
            }
        """)
    
    def _apply_light_theme(self):
        """Apply light theme"""
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #ffffff;
                color: #212121;
            }
            QToolBar {
                background-color: #f5f5f5;
                border-bottom: 1px solid #e0e0e0;
                padding: 8px;
                spacing: 8px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d5f;
            }
            QPushButton:disabled {
                background-color: #e0e0e0;
                color: #9e9e9e;
            }
        """)
    
    def _apply_language(self):
        """Apply language and RTL if needed"""
        if self.i18n.is_rtl():
            self.setLayoutDirection(Qt.RightToLeft)
        else:
            self.setLayoutDirection(Qt.LeftToRight)
    
    def _create_rtl_messagebox(self, icon, title, text, buttons=QMessageBox.Ok):
        """Create a message box with RTL support"""
        msg_box = QMessageBox(self)
        msg_box.setIcon(icon)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(buttons)
        msg_box.setLayoutDirection(Qt.RightToLeft)
        return msg_box
    
    def _on_open_images(self):
        """Handle open images action"""
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.ExistingFiles)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.webp)")
        file_dialog.setLayoutDirection(Qt.RightToLeft)
        
        if file_dialog.exec():
            files = [Path(f) for f in file_dialog.selectedFiles()]
            self.queue_panel.add_files(files)
    
    def _on_open_folder(self):
        """Handle open folder action"""
        file_dialog = QFileDialog(self)
        file_dialog.setLayoutDirection(Qt.RightToLeft)
        folder = file_dialog.getExistingDirectory(
            self,
            self.i18n.t("dialogs.open_folder_title"),
            str(Path.home())
        )
        
        if folder:
            folder_path = Path(folder)
            # Find all images in folder
            image_files = []
            for ext in ["*.png", "*.jpg", "*.jpeg", "*.bmp", "*.webp"]:
                image_files.extend(folder_path.glob(ext))
                image_files.extend(folder_path.glob(ext.upper()))
            
            if image_files:
                self.queue_panel.add_files(image_files)
    
    def _on_choose_output_dir(self):
        """Handle choose output directory"""
        file_dialog = QFileDialog(self)
        file_dialog.setLayoutDirection(Qt.RightToLeft)
        folder = file_dialog.getExistingDirectory(
            self,
            self.i18n.t("dialogs.save_output_title"),
            str(self.output_dir)
        )
        
        if folder:
            self.output_dir = Path(folder)
            self.output_btn.setText(f"📂 {self.output_dir.name}")
            self.output_btn.setToolTip(str(self.output_dir))
            self.settings.last_output_dir = str(self.output_dir)
            update_settings(self.settings)
    
    def _on_start_processing(self):
        """Start batch processing"""
        if self.queue_panel.get_item_count() == 0:
            msg_box = self._create_rtl_messagebox(
                QMessageBox.Warning,
                self.i18n.t("dialogs.warning_title"),
                self.i18n.t("messages.no_images_selected")
            )
            msg_box.exec()
            return
        
        # Get files from queue
        files = self.queue_panel.get_all_files()
        
        # Add tasks to batch worker
        self.batch_worker.add_tasks(
            files,
            self.output_dir,
            self.settings.output,
            self.settings.quality
        )
        
        # Start processing
        if self.batch_worker.start():
            self.start_btn.setEnabled(False)
            self.pause_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
            self.statusBar().showMessage(self.i18n.t("messages.processing_started"))
    
    def _on_pause_processing(self):
        """Pause processing"""
        self.batch_worker.pause()
        self.statusBar().showMessage(self.i18n.t("messages.processing_paused"))
    
    def _on_cancel_processing(self):
        """Cancel processing"""
        msg_box = self._create_rtl_messagebox(
            QMessageBox.Question,
            self.i18n.t("dialogs.confirm"),
            self.i18n.t("dialogs.cancel_processing_confirm"),
            QMessageBox.Yes | QMessageBox.No
        )
        reply = msg_box.exec()
        
        if reply == QMessageBox.Yes:
            self.batch_worker.cancel()
            self.statusBar().showMessage(self.i18n.t("messages.processing_cancelled"))
    
    def _on_clear_queue(self):
        """Clear the queue"""
        if self.queue_panel.get_item_count() > 0:
            msg_box = self._create_rtl_messagebox(
                QMessageBox.Question,
                self.i18n.t("dialogs.confirm"),
                self.i18n.t("dialogs.clear_queue_confirm"),
                QMessageBox.Yes | QMessageBox.No
            )
            reply = msg_box.exec()
            
            if reply == QMessageBox.Yes:
                self.queue_panel.clear()
                self.batch_worker.clear()
    
    def _on_files_added(self, count: int):
        """Handle files added to queue"""
        self.statusBar().showMessage(self.i18n.t("messages.images_added", count))
    
    def _on_item_selected(self, file_path: Path):
        """Handle item selected in queue"""
        # Show original image in before section
        self.preview_panel.set_before_image(file_path)
        # Clear after section
        self.preview_panel.clear_after()
    
    def _on_settings_changed(self):
        """Handle settings changed"""
        update_settings(self.settings)
    
    def _on_task_started(self, task_id: int):
        """Handle task started"""
        self.queue_panel.update_item_status(task_id, "processing")
        
        # Show the current image being processed
        file_path = self.queue_panel.get_file_by_id(task_id)
        if file_path:
            self.preview_panel.set_before_image(file_path)
            self.preview_panel.clear_after()
    
    def _on_task_completed(self, task_id: int, output_path: Path):
        """Handle task completed"""
        self.queue_panel.update_item_status(task_id, "completed")
        
        # Show the result in after section
        if output_path and output_path.exists():
            self.preview_panel.set_after_image(output_path)
        
        logger.info(f"Task {task_id} completed: {output_path}")
    
    def _on_task_failed(self, task_id: int, error: str):
        """Handle task failed"""
        self.queue_panel.update_item_status(task_id, "failed")
        logger.error(f"Task {task_id} failed: {error}")
    
    def _on_batch_progress(self, completed: int, total: int):
        """Handle batch progress"""
        progress_text = f"{completed}/{total}"
        self.statusBar().showMessage(f"{self.i18n.t('messages.processing_started')}: {progress_text}")
    
    def _on_batch_completed(self, successful: int, failed: int):
        """Handle batch completed"""
        # Re-enable/disable toolbar buttons after batch completes
        self.start_btn.setEnabled(True)
        self.pause_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        
        message = self.i18n.t("messages.batch_completed", successful, failed)
        self.statusBar().showMessage(message)
        
        msg_box = self._create_rtl_messagebox(
            QMessageBox.Information,
            self.i18n.t("dialogs.success_title"),
            message
        )
        msg_box.exec()
    
    def _on_about(self):
        """Show about dialog"""
        about_text = """
<div dir="rtl" style="text-align: right; font-family: 'Segoe UI', 'Tahoma', sans-serif;">
    <h2 style="color: #14a085; text-align: center; margin-bottom: 20px;">إزالة الخلفيات</h2>
    
    <table dir="rtl" style="width: 100%; margin: 10px 0;">
        <tr>
            <td style="text-align: right; padding: 5px;"><b style="color: #14a085;">الإصدار:</b></td>
            <td style="text-align: left; padding: 5px;">1.0.0</td>
        </tr>
        <tr>
            <td colspan="2" style="text-align: right; padding: 10px 5px; line-height: 1.6;">
                تطبيق احترافي لإزالة خلفيات الصور مدعوم بالذكاء الاصطناعي، قم بإزالة خلفيات الصور محلياً بدون خدمات سحابية.
            </td>
        </tr>
        <tr>
            <td style="text-align: right; padding: 5px;"><b style="color: #14a085;">الترخيص:</b></td>
            <td style="text-align: left; padding: 5px;">MIT</td>
        </tr>
    </table>
    
    <hr style="border: none; border-top: 2px solid #0d7377; margin: 20px 0;">
    
    <div style="background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0d7377, stop:1 #14a085);
                padding: 20px; border-radius: 10px; margin: 15px 0; text-align: center;">
        <p style="color: white; font-size: 16px; font-weight: bold; margin: 8px 0;">
            💻 تم التطوير بواسطة
        </p>
        <p style="color: white; font-size: 22px; font-weight: bold; margin: 12px 0; letter-spacing: 1px;">
            المهندس حمزة ضمرة
        </p>
        <p style="color: #e8f9f9; font-size: 15px; margin: 8px 0; font-style: italic;">
            Eng. Hamza Damra
        </p>
    </div>
    
    <p style="text-align: center; font-size: 13px; color: #888; margin: 15px 0; line-height: 1.6;">
        🚀 بناء احترافي باستخدام<br>
        <b style="color: #14a085;">Python & PySide6</b>
    </p>
    
    <p style="text-align: center; font-size: 11px; color: #666; margin: 10px 0;">
        U²-Net Deep Learning Model<br>
        GPU Accelerated Processing
    </p>
</div>
"""
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("حول")
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.NoIcon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        
        # Apply RTL layout and styling
        msg_box.setLayoutDirection(Qt.RightToLeft)
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: #2d2d2d;
                min-width: 500px;
            }
            QLabel {
                min-width: 480px;
                max-width: 500px;
                color: #e0e0e0;
                padding: 10px;
            }
            QPushButton {
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 30px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
            QPushButton:pressed {
                background-color: #0a5d5f;
            }
        """)
        
        msg_box.exec()
    
    def closeEvent(self, event):
        """Handle window close"""
        # Check if processing
        status = self.batch_worker.get_status()
        if status["is_running"]:
            msg_box = self._create_rtl_messagebox(
                QMessageBox.Question,
                self.i18n.t("dialogs.confirm"),
                self.i18n.t("dialogs.exit_while_processing"),
                QMessageBox.Yes | QMessageBox.No
            )
            reply = msg_box.exec()
            
            if reply == QMessageBox.No:
                event.ignore()
                return
            
            self.batch_worker.cancel()
        
        # Save window state
        self.settings.window_width = self.width()
        self.settings.window_height = self.height()
        self.settings.window_maximized = self.isMaximized()
        update_settings(self.settings)
        
        event.accept()
