"""Settings panel for configuring output and quality"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTabWidget, QFormLayout, QComboBox,
    QSpinBox, QCheckBox, QSlider, QLabel, QPushButton, QColorDialog,
    QFileDialog, QLineEdit, QHBoxLayout, QGroupBox
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QColor

from bgremover.app.core.settings import Settings
from bgremover.app.core.presets import get_preset_manager


class SettingsPanel(QWidget):
    """Panel for configuring processing settings"""
    
    settings_changed = Signal()
    
    def __init__(self, settings: Settings, i18n, parent=None):
        super().__init__(parent)
        
        self.settings = settings
        self.i18n = i18n
        self.preset_manager = get_preset_manager()
        
        self._setup_ui()
        self._load_settings()
    
    def _setup_ui(self):
        """Setup UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(self.i18n.t("settings_panel.title"))
        title.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        layout.addWidget(title)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Style tabs with better contrast and larger fonts
        tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #3d3d3d;
                background-color: #1e1e1e;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #2d2d2d;
                color: #e0e0e0;
                padding: 12px 24px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-size: 14px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #0d7377;
                color: #ffffff;
            }
            QTabBar::tab:hover:!selected {
                background-color: #3d3d3d;
            }
            QLabel {
                font-size: 13px;
                color: #e0e0e0;
            }
            QComboBox, QSpinBox, QLineEdit {
                font-size: 13px;
                padding: 6px;
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
            }
            QCheckBox {
                font-size: 13px;
                color: #e0e0e0;
                spacing: 8px;
            }
            QPushButton {
                font-size: 13px;
                padding: 8px 16px;
                background-color: #0d7377;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a085;
            }
        """)
        
        # Output tab
        output_tab = self._create_output_tab()
        tabs.addTab(output_tab, self.i18n.t("settings_panel.tab_output"))
        
        # Quality tab
        quality_tab = self._create_quality_tab()
        tabs.addTab(quality_tab, self.i18n.t("settings_panel.tab_quality"))
        
        # Presets tab
        presets_tab = self._create_presets_tab()
        tabs.addTab(presets_tab, self.i18n.t("settings_panel.tab_presets"))
        
        layout.addWidget(tabs)
    
    def _create_output_tab(self) -> QWidget:
        """Create output settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Format
        self.format_combo = QComboBox()
        self.format_combo.addItems(["png", "webp", "jpg"])
        self.format_combo.currentTextChanged.connect(self._on_setting_changed)
        layout.addRow(self.i18n.t("settings_panel.output_format"), self.format_combo)
        
        # Quality
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(1, 100)
        self.quality_slider.setValue(95)
        self.quality_slider.valueChanged.connect(self._on_setting_changed)
        
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.quality_slider)
        self.quality_label = QLabel("95")
        self.quality_slider.valueChanged.connect(lambda v: self.quality_label.setText(str(v)))
        quality_layout.addWidget(self.quality_label)
        
        layout.addRow(self.i18n.t("settings_panel.output_quality"), quality_layout)
        
        # Background type
        bg_group = QGroupBox(self.i18n.t("settings_panel.background_type"))
        bg_layout = QVBoxLayout(bg_group)
        
        self.bg_transparent = QCheckBox(self.i18n.t("settings_panel.bg_transparent"))
        self.bg_transparent.setChecked(True)
        self.bg_transparent.toggled.connect(self._on_bg_type_changed)
        bg_layout.addWidget(self.bg_transparent)
        
        self.bg_color = QCheckBox(self.i18n.t("settings_panel.bg_color"))
        self.bg_color.toggled.connect(self._on_bg_type_changed)
        bg_layout.addWidget(self.bg_color)
        
        color_layout = QHBoxLayout()
        self.bg_color_input = QLineEdit("#FFFFFF")
        self.bg_color_input.textChanged.connect(self._on_setting_changed)
        color_layout.addWidget(self.bg_color_input)
        
        color_btn = QPushButton(self.i18n.t("settings_panel.choose_color"))
        color_btn.clicked.connect(self._on_choose_color)
        color_layout.addWidget(color_btn)
        bg_layout.addLayout(color_layout)
        
        self.bg_image = QCheckBox(self.i18n.t("settings_panel.bg_image"))
        self.bg_image.toggled.connect(self._on_bg_type_changed)
        bg_layout.addWidget(self.bg_image)
        
        image_layout = QHBoxLayout()
        self.bg_image_input = QLineEdit()
        self.bg_image_input.textChanged.connect(self._on_setting_changed)
        image_layout.addWidget(self.bg_image_input)
        
        image_btn = QPushButton(self.i18n.t("settings_panel.browse"))
        image_btn.clicked.connect(self._on_choose_bg_image)
        image_layout.addWidget(image_btn)
        bg_layout.addLayout(image_layout)
        
        layout.addRow(bg_group)
        
        # Canvas size
        canvas_group = QGroupBox(self.i18n.t("settings_panel.canvas_size"))
        canvas_layout = QFormLayout(canvas_group)
        
        self.canvas_width = QSpinBox()
        self.canvas_width.setRange(0, 10000)
        self.canvas_width.setSuffix(" px")
        self.canvas_width.setSpecialValueText(self.i18n.t("settings_panel.auto_size"))
        self.canvas_width.valueChanged.connect(self._on_setting_changed)
        canvas_layout.addRow(self.i18n.t("settings_panel.width"), self.canvas_width)
        
        self.canvas_height = QSpinBox()
        self.canvas_height.setRange(0, 10000)
        self.canvas_height.setSuffix(" px")
        self.canvas_height.setSpecialValueText(self.i18n.t("settings_panel.auto_size"))
        self.canvas_height.valueChanged.connect(self._on_setting_changed)
        canvas_layout.addRow(self.i18n.t("settings_panel.height"), self.canvas_height)
        
        self.center_object = QCheckBox(self.i18n.t("settings_panel.center_object"))
        self.center_object.setChecked(True)
        self.center_object.toggled.connect(self._on_setting_changed)
        canvas_layout.addRow(self.center_object)
        
        layout.addRow(canvas_group)
        
        # Margin
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 500)
        self.margin_spin.setSuffix(" px")
        self.margin_spin.valueChanged.connect(self._on_setting_changed)
        layout.addRow(self.i18n.t("settings_panel.margin"), self.margin_spin)
        
        # Feather edges
        self.feather_spin = QSpinBox()
        self.feather_spin.setRange(0, 50)
        self.feather_spin.setSuffix(" px")
        self.feather_spin.valueChanged.connect(self._on_setting_changed)
        layout.addRow(self.i18n.t("settings_panel.feather_edges"), self.feather_spin)
        
        return widget
    
    def _create_quality_tab(self) -> QWidget:
        """Create quality settings tab"""
        widget = QWidget()
        layout = QFormLayout(widget)
        
        # Alpha matting
        self.alpha_matting = QCheckBox(self.i18n.t("settings_panel.alpha_matting"))
        self.alpha_matting.toggled.connect(self._on_setting_changed)
        layout.addRow(self.alpha_matting)
        
        desc = QLabel(self.i18n.t("settings_panel.alpha_matting_desc"))
        desc.setStyleSheet("color: gray; font-size: 11px;")
        desc.setWordWrap(True)
        layout.addRow(desc)
        
        # Remove small objects
        self.remove_small = QCheckBox(self.i18n.t("settings_panel.remove_small_objects"))
        self.remove_small.setChecked(True)
        self.remove_small.toggled.connect(self._on_setting_changed)
        layout.addRow(self.remove_small)
        
        self.min_object_size = QSpinBox()
        self.min_object_size.setRange(0, 10000)
        self.min_object_size.setValue(100)
        self.min_object_size.valueChanged.connect(self._on_setting_changed)
        layout.addRow(self.i18n.t("settings_panel.min_object_size"), self.min_object_size)
        
        # Smooth edges
        self.smooth_edges = QCheckBox(self.i18n.t("settings_panel.smooth_edges"))
        self.smooth_edges.setChecked(True)
        self.smooth_edges.toggled.connect(self._on_setting_changed)
        layout.addRow(self.smooth_edges)
        
        self.edge_smooth = QSpinBox()
        self.edge_smooth.setRange(1, 15)
        self.edge_smooth.setValue(5)
        self.edge_smooth.valueChanged.connect(self._on_setting_changed)
        layout.addRow(self.i18n.t("settings_panel.edge_smooth_kernel"), self.edge_smooth)
        
        return widget
    
    def _create_presets_tab(self) -> QWidget:
        """Create presets tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Preset selector
        self.preset_combo = QComboBox()
        
        # Mapping from preset IDs to translation keys
        preset_translations = {
            "transparent": "presets.transparent",
            "marketplace": "presets.marketplace",
            "white_bg": "presets.white_bg",
            "social_media_square": "presets.social_media_square",
            "product_photography": "presets.product_photography",
            "catalog_print": "presets.catalog_print"
        }
        
        # Load presets
        presets = self.preset_manager.list_presets()
        for preset in presets:
            preset_id = preset["id"]
            # Use translation if available, otherwise use original name
            if preset_id in preset_translations:
                display_name = self.i18n.t(preset_translations[preset_id])
            else:
                display_name = preset["name"]
            
            self.preset_combo.addItem(display_name, preset_id)
        
        layout.addWidget(QLabel(self.i18n.t("settings_panel.preset_select")))
        layout.addWidget(self.preset_combo)
        
        # Apply button
        apply_btn = QPushButton(self.i18n.t("settings_panel.preset_apply"))
        apply_btn.clicked.connect(self._on_apply_preset)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        
        return widget
    
    def _load_settings(self):
        """Load settings into UI"""
        # Output
        self.format_combo.setCurrentText(self.settings.output.format)
        self.quality_slider.setValue(self.settings.output.quality)
        
        if self.settings.output.background_type == "transparent":
            self.bg_transparent.setChecked(True)
        elif self.settings.output.background_type == "color":
            self.bg_color.setChecked(True)
        else:
            self.bg_image.setChecked(True)
        
        self.bg_color_input.setText(self.settings.output.background_color)
        
        if self.settings.output.background_image:
            self.bg_image_input.setText(self.settings.output.background_image)
        
        if self.settings.output.canvas_width:
            self.canvas_width.setValue(self.settings.output.canvas_width)
        
        if self.settings.output.canvas_height:
            self.canvas_height.setValue(self.settings.output.canvas_height)
        
        self.center_object.setChecked(self.settings.output.center_object)
        self.margin_spin.setValue(self.settings.output.margin)
        self.feather_spin.setValue(self.settings.output.feather_edges)
        
        # Quality
        self.alpha_matting.setChecked(self.settings.quality.alpha_matting)
        self.remove_small.setChecked(self.settings.quality.remove_small_objects)
        self.min_object_size.setValue(self.settings.quality.min_object_size)
        self.smooth_edges.setChecked(self.settings.quality.smooth_edges)
        self.edge_smooth.setValue(self.settings.quality.edge_smooth_kernel)
    
    def _on_setting_changed(self):
        """Handle setting changed"""
        # Update settings object
        self.settings.output.format = self.format_combo.currentText()
        self.settings.output.quality = self.quality_slider.value()
        
        if self.bg_transparent.isChecked():
            self.settings.output.background_type = "transparent"
        elif self.bg_color.isChecked():
            self.settings.output.background_type = "color"
        else:
            self.settings.output.background_type = "image"
        
        self.settings.output.background_color = self.bg_color_input.text()
        self.settings.output.background_image = self.bg_image_input.text() or None
        
        self.settings.output.canvas_width = self.canvas_width.value() or None
        self.settings.output.canvas_height = self.canvas_height.value() or None
        self.settings.output.center_object = self.center_object.isChecked()
        self.settings.output.margin = self.margin_spin.value()
        self.settings.output.feather_edges = self.feather_spin.value()
        
        self.settings.quality.alpha_matting = self.alpha_matting.isChecked()
        self.settings.quality.remove_small_objects = self.remove_small.isChecked()
        self.settings.quality.min_object_size = self.min_object_size.value()
        self.settings.quality.smooth_edges = self.smooth_edges.isChecked()
        self.settings.quality.edge_smooth_kernel = self.edge_smooth.value()
        
        self.settings_changed.emit()
    
    def _on_bg_type_changed(self, checked):
        """Handle background type change"""
        if checked:
            sender = self.sender()
            if sender == self.bg_transparent:
                self.bg_color.setChecked(False)
                self.bg_image.setChecked(False)
            elif sender == self.bg_color:
                self.bg_transparent.setChecked(False)
                self.bg_image.setChecked(False)
            else:
                self.bg_transparent.setChecked(False)
                self.bg_color.setChecked(False)
        
        self._on_setting_changed()
    
    def _on_choose_color(self):
        """Open color picker"""
        color_dialog = QColorDialog(QColor(self.bg_color_input.text()), self)
        color_dialog.setLayoutDirection(Qt.RightToLeft)
        color = color_dialog.getColor()
        if color.isValid():
            self.bg_color_input.setText(color.name())
    
    def _on_choose_bg_image(self):
        """Choose background image"""
        file_dialog = QFileDialog(self)
        file_dialog.setLayoutDirection(Qt.RightToLeft)
        file_path, _ = file_dialog.getOpenFileName(
            self,
            self.i18n.t("dialogs.choose_bg_image_title"),
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )
        
        if file_path:
            self.bg_image_input.setText(file_path)
    
    def _on_apply_preset(self):
        """Apply selected preset"""
        preset_id = self.preset_combo.currentData()
        preset = self.preset_manager.get_preset(preset_id)
        
        if preset:
            # Apply preset to settings
            self.settings.output.format = preset.format
            self.settings.output.quality = preset.quality
            self.settings.output.background_type = preset.background_type
            self.settings.output.background_color = preset.background_color
            self.settings.output.canvas_width = preset.canvas_width
            self.settings.output.canvas_height = preset.canvas_height
            self.settings.output.center_object = preset.center_object
            self.settings.output.margin = preset.margin
            self.settings.output.feather_edges = preset.feather_edges
            
            self.settings.quality.alpha_matting = preset.alpha_matting
            self.settings.quality.remove_small_objects = preset.remove_small_objects
            self.settings.quality.min_object_size = preset.min_object_size
            self.settings.quality.smooth_edges = preset.smooth_edges
            self.settings.quality.edge_smooth_kernel = preset.edge_smooth_kernel
            
            # Reload UI
            self._load_settings()
            self.settings_changed.emit()
