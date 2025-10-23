"""Application settings management with Pydantic"""

import json
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


class OutputSettings(BaseModel):
    """Output configuration settings"""
    format: Literal["png", "webp", "jpg"] = "png"
    quality: int = Field(default=95, ge=1, le=100)
    background_type: Literal["transparent", "color", "image"] = "transparent"
    background_color: str = "#FFFFFF"
    background_image: Optional[str] = None
    canvas_width: Optional[int] = None
    canvas_height: Optional[int] = None
    center_object: bool = True
    margin: int = Field(default=0, ge=0)
    feather_edges: int = Field(default=0, ge=0, le=50)


class QualitySettings(BaseModel):
    """Quality and refinement settings"""
    alpha_matting: bool = False
    alpha_matting_foreground_threshold: int = Field(default=240, ge=0, le=255)
    alpha_matting_background_threshold: int = Field(default=10, ge=0, le=255)
    remove_small_objects: bool = True
    min_object_size: int = Field(default=100, ge=0)
    smooth_edges: bool = True
    edge_smooth_kernel: int = Field(default=5, ge=1, le=15)


class Settings(BaseModel):
    """Main application settings"""
    version: str = "1.0.0"
    language: Literal["ar"] = "ar"  # اللغة العربية فقط
    theme: Literal["dark", "light", "auto"] = "dark"
    
    # Directories
    last_input_dir: Optional[str] = None
    last_output_dir: Optional[str] = None
    
    # Processing
    output: OutputSettings = Field(default_factory=OutputSettings)
    quality: QualitySettings = Field(default_factory=QualitySettings)
    
    # UI State
    window_width: int = 1280
    window_height: int = 800
    window_maximized: bool = False
    
    # Performance
    max_workers: int = Field(default=4, ge=1, le=16)
    use_gpu: bool = False
    
    @classmethod
    def get_settings_path(cls) -> Path:
        """Get path to settings file"""
        config_dir = Path.home() / ".bgremover"
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir / "settings.json"
    
    @classmethod
    def load(cls) -> "Settings":
        """Load settings from file"""
        settings_path = cls.get_settings_path()
        
        if settings_path.exists():
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                return cls(**data)
            except Exception as e:
                print(f"Failed to load settings: {e}. Using defaults.")
                return cls()
        
        return cls()
    
    def save(self) -> bool:
        """Save settings to file"""
        try:
            settings_path = self.get_settings_path()
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(self.model_dump(), f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to save settings: {e}")
            return False
    
    def migrate(self) -> None:
        """Migrate settings from older versions if needed"""
        # Add migration logic here when version changes
        if self.version != "1.0.0":
            # Perform migration
            self.version = "1.0.0"
            self.save()


# Singleton instance
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """Get singleton settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings.load()
    return _settings_instance


def update_settings(settings: Settings) -> bool:
    """Update singleton settings instance"""
    global _settings_instance
    _settings_instance = settings
    return settings.save()
