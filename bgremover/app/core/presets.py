"""Preset management for common use cases"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from loguru import logger


@dataclass
class Preset:
    """Preset configuration"""
    name: str
    description: str
    # Output settings
    format: str = "png"
    quality: int = 95
    background_type: str = "transparent"
    background_color: str = "#FFFFFF"
    canvas_width: Optional[int] = None
    canvas_height: Optional[int] = None
    center_object: bool = True
    margin: int = 0
    feather_edges: int = 0
    # Quality settings
    alpha_matting: bool = False
    remove_small_objects: bool = True
    min_object_size: int = 100
    smooth_edges: bool = True
    edge_smooth_kernel: int = 5


class PresetManager:
    """Manages presets for common use cases"""
    
    # Built-in presets
    BUILTIN_PRESETS = {
        "transparent": Preset(
            name="Transparent - Web",
            description="PNG شفاف للويب - Transparent PNG for web use",
            format="png",
            background_type="transparent",
        ),
        
        "marketplace": Preset(
            name="Marketplace 1600×1600",
            description="مثالي للمتاجر الإلكترونية - Perfect for e-commerce platforms",
            format="png",
            background_type="transparent",
            canvas_width=1600,
            canvas_height=1600,
            center_object=True,
            margin=50,
        ),
        
        "white_bg": Preset(
            name="Product - White Background",
            description="خلفية بيضاء للمنتجات - White background for products",
            format="jpg",
            quality=95,
            background_type="color",
            background_color="#FFFFFF",
        ),
        
        "social_media_square": Preset(
            name="Social Media Square",
            description="مربع 1080×1080 لوسائل التواصل - 1080×1080 square for social media",
            format="png",
            background_type="transparent",
            canvas_width=1080,
            canvas_height=1080,
            center_object=True,
            margin=40,
        ),
        
        "product_photography": Preset(
            name="Product Photography",
            description="تصوير احترافي للمنتجات - Professional product photography",
            format="png",
            background_type="transparent",
            canvas_width=2000,
            canvas_height=2000,
            center_object=True,
            margin=100,
            alpha_matting=True,
            smooth_edges=True,
            edge_smooth_kernel=7,
        ),
        
        "catalog_print": Preset(
            name="Catalog / Print",
            description="للكتالوجات والطباعة - For catalogs and print",
            format="png",
            quality=100,
            background_type="color",
            background_color="#F5F5F5",
            canvas_width=2400,
            canvas_height=3000,
            center_object=True,
            margin=150,
        ),
    }
    
    def __init__(self):
        """Initialize preset manager"""
        self.presets_dir = Path.home() / ".bgremover" / "presets"
        self.presets_dir.mkdir(parents=True, exist_ok=True)
        self.presets_file = self.presets_dir / "custom_presets.json"
        
        self.custom_presets: Dict[str, Preset] = {}
        self._load_custom_presets()
    
    def _load_custom_presets(self) -> None:
        """Load custom presets from file"""
        if self.presets_file.exists():
            try:
                with open(self.presets_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                for key, preset_data in data.items():
                    self.custom_presets[key] = Preset(**preset_data)
                
                logger.info(f"Loaded {len(self.custom_presets)} custom presets")
            except Exception as e:
                logger.error(f"Failed to load custom presets: {e}")
    
    def _save_custom_presets(self) -> bool:
        """Save custom presets to file"""
        try:
            data = {key: asdict(preset) for key, preset in self.custom_presets.items()}
            
            with open(self.presets_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.success("Custom presets saved")
            return True
        except Exception as e:
            logger.error(f"Failed to save custom presets: {e}")
            return False
    
    def get_preset(self, preset_id: str) -> Optional[Preset]:
        """
        Get preset by ID
        
        Args:
            preset_id: Preset identifier
        
        Returns:
            Preset object or None if not found
        """
        # Check built-in presets first
        if preset_id in self.BUILTIN_PRESETS:
            return self.BUILTIN_PRESETS[preset_id]
        
        # Check custom presets
        return self.custom_presets.get(preset_id)
    
    def list_presets(self) -> List[Dict[str, str]]:
        """
        List all available presets
        
        Returns:
            List of preset info dicts with id, name, description
        """
        presets = []
        
        # Built-in presets
        for preset_id, preset in self.BUILTIN_PRESETS.items():
            presets.append({
                "id": preset_id,
                "name": preset.name,
                "description": preset.description,
                "type": "builtin"
            })
        
        # Custom presets
        for preset_id, preset in self.custom_presets.items():
            presets.append({
                "id": preset_id,
                "name": preset.name,
                "description": preset.description,
                "type": "custom"
            })
        
        return presets
    
    def save_preset(self, preset_id: str, preset: Preset) -> bool:
        """
        Save a custom preset
        
        Args:
            preset_id: Unique identifier
            preset: Preset object
        
        Returns:
            True if successful
        """
        # Don't allow overwriting built-in presets
        if preset_id in self.BUILTIN_PRESETS:
            logger.error(f"Cannot overwrite built-in preset: {preset_id}")
            return False
        
        self.custom_presets[preset_id] = preset
        return self._save_custom_presets()
    
    def delete_preset(self, preset_id: str) -> bool:
        """
        Delete a custom preset
        
        Args:
            preset_id: Preset identifier
        
        Returns:
            True if successful
        """
        # Can't delete built-in presets
        if preset_id in self.BUILTIN_PRESETS:
            logger.error(f"Cannot delete built-in preset: {preset_id}")
            return False
        
        if preset_id not in self.custom_presets:
            logger.error(f"Preset not found: {preset_id}")
            return False
        
        del self.custom_presets[preset_id]
        return self._save_custom_presets()
    
    def export_preset(self, preset_id: str, export_path: Path) -> bool:
        """
        Export preset to JSON file
        
        Args:
            preset_id: Preset identifier
            export_path: Path to save JSON file
        
        Returns:
            True if successful
        """
        preset = self.get_preset(preset_id)
        if preset is None:
            logger.error(f"Preset not found: {preset_id}")
            return False
        
        try:
            with open(export_path, "w", encoding="utf-8") as f:
                json.dump(asdict(preset), f, indent=2, ensure_ascii=False)
            
            logger.success(f"Preset exported to {export_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to export preset: {e}")
            return False
    
    def import_preset(self, import_path: Path, preset_id: str) -> bool:
        """
        Import preset from JSON file
        
        Args:
            import_path: Path to JSON file
            preset_id: ID to assign to imported preset
        
        Returns:
            True if successful
        """
        try:
            with open(import_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            preset = Preset(**data)
            return self.save_preset(preset_id, preset)
        except Exception as e:
            logger.error(f"Failed to import preset: {e}")
            return False


# Singleton instance
_preset_manager_instance: Optional[PresetManager] = None


def get_preset_manager() -> PresetManager:
    """Get singleton preset manager instance"""
    global _preset_manager_instance
    if _preset_manager_instance is None:
        _preset_manager_instance = PresetManager()
    return _preset_manager_instance
