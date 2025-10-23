"""Internationalization (i18n) manager"""

import json
from pathlib import Path
from typing import Dict, Optional
from loguru import logger


class I18n:
    """Manages translations for the application - Arabic only"""
    
    def __init__(self, language: str = "ar"):
        """
        Initialize i18n manager
        
        Args:
            language: Language code (ar only)
        """
        self.language = "ar"  # اللغة العربية فقط
        self.translations: Dict[str, any] = {}
        self.i18n_dir = Path(__file__).parent / "i18n"
        
        self.load_language("ar")
    
    def load_language(self, language: str = "ar") -> bool:
        """
        Load translations for Arabic language
        
        Args:
            language: Language code (ar only)
        
        Returns:
            True if successful
        """
        translation_file = self.i18n_dir / "ar.json"
        
        if not translation_file.exists():
            logger.error(f"Translation file not found: {translation_file}")
            return False
        
        try:
            with open(translation_file, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
            
            self.language = "ar"
            logger.info(f"Loaded translations for: ar")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load translations: {e}")
            return False
    
    def t(self, key: str, *args) -> str:
        """
        Get translated string
        
        Args:
            key: Translation key (dot-separated path, e.g., "menu.file")
            *args: Format arguments
        
        Returns:
            Translated string or key if not found
        """
        # Navigate through nested dictionary
        parts = key.split(".")
        value = self.translations
        
        try:
            for part in parts:
                value = value[part]
            
            # Format with arguments if provided
            if args:
                return value.format(*args)
            
            return value
            
        except (KeyError, TypeError):
            logger.warning(f"Translation not found: {key}")
            return key
    
    def is_rtl(self) -> bool:
        """
        Check if current language is RTL (Right-to-Left)
        
        Returns:
            True (Arabic is always RTL)
        """
        return True  # العربية دائماً من اليمين لليسار


# Global instance
_i18n_instance: Optional[I18n] = None


def get_i18n(language: Optional[str] = None) -> I18n:
    """
    Get global i18n instance
    
    Args:
        language: Optional language (ignored, always Arabic)
    
    Returns:
        I18n instance
    """
    global _i18n_instance
    
    if _i18n_instance is None:
        _i18n_instance = I18n("ar")
    
    return _i18n_instance


def set_language(language: str) -> bool:
    """
    Set application language (always Arabic)
    
    Args:
        language: Language code (ignored)
    
    Returns:
        True
    """
    return True  # اللغة دائماً عربية
