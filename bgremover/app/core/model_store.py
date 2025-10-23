"""Model download and verification"""

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional
import requests
from loguru import logger


class ModelStore:
    """Manages ML model download, verification, and storage"""
    
    # Model URLs and checksums
    MODELS = {
        "u2net": {
            "url": "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx",
            "sha256": "60024c5c889badc19c04ad937298a77da6dc8df30476a58540a7e99dff9b74dc",
            "filename": "u2net.onnx",
            "size_mb": 176
        }
    }
    
    def __init__(self, models_dir: Optional[Path] = None):
        """
        Initialize model store
        
        Args:
            models_dir: Directory to store models (default: ./models)
        """
        if models_dir is None:
            # Use models directory in project root
            models_dir = Path(__file__).parent.parent.parent.parent / "models"
        
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        self.checksums_file = self.models_dir / "checksums.json"
        self._load_checksums()
    
    def _load_checksums(self) -> None:
        """Load verified checksums from file"""
        if self.checksums_file.exists():
            try:
                with open(self.checksums_file, "r") as f:
                    self.verified_checksums = json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load checksums: {e}")
                self.verified_checksums = {}
        else:
            self.verified_checksums = {}
    
    def _save_checksums(self) -> None:
        """Save verified checksums to file"""
        try:
            with open(self.checksums_file, "w") as f:
                json.dump(self.verified_checksums, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save checksums: {e}")
    
    def _calculate_sha256(self, file_path: Path) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        return sha256_hash.hexdigest()
    
    def verify_model(self, model_name: str) -> bool:
        """
        Verify if model exists and has correct checksum
        
        Args:
            model_name: Name of the model to verify
        
        Returns:
            True if model is valid, False otherwise
        """
        if model_name not in self.MODELS:
            logger.error(f"Unknown model: {model_name}")
            return False
        
        model_info = self.MODELS[model_name]
        model_path = self.models_dir / model_info["filename"]
        
        if not model_path.exists():
            logger.info(f"Model {model_name} not found at {model_path}")
            return False
        
        # Check if already verified
        if model_name in self.verified_checksums:
            stored_checksum = self.verified_checksums[model_name]
            if stored_checksum == model_info["sha256"]:
                logger.info(f"Model {model_name} already verified")
                return True
        
        # Verify checksum
        logger.info(f"Verifying {model_name} checksum...")
        actual_checksum = self._calculate_sha256(model_path)
        expected_checksum = model_info["sha256"]
        
        if actual_checksum == expected_checksum:
            logger.success(f"Model {model_name} verified successfully")
            self.verified_checksums[model_name] = actual_checksum
            self._save_checksums()
            return True
        else:
            logger.error(f"Checksum mismatch for {model_name}")
            logger.error(f"Expected: {expected_checksum}")
            logger.error(f"Actual: {actual_checksum}")
            return False
    
    def download_model(self, model_name: str, progress_callback=None) -> bool:
        """
        Download model from URL
        
        Args:
            model_name: Name of the model to download
            progress_callback: Optional callback for progress updates (current, total)
        
        Returns:
            True if download successful, False otherwise
        """
        if model_name not in self.MODELS:
            logger.error(f"Unknown model: {model_name}")
            return False
        
        model_info = self.MODELS[model_name]
        model_path = self.models_dir / model_info["filename"]
        
        # Check if already exists and valid
        if self.verify_model(model_name):
            logger.info(f"Model {model_name} already exists and is valid")
            return True
        
        # Download
        logger.info(f"Downloading {model_name} from {model_info['url']}...")
        logger.info(f"Expected size: ~{model_info['size_mb']} MB")
        
        try:
            response = requests.get(model_info["url"], stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(model_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback:
                            progress_callback(downloaded, total_size)
            
            logger.success(f"Downloaded {model_name} successfully")
            
            # Verify downloaded file
            if self.verify_model(model_name):
                return True
            else:
                logger.error("Downloaded file failed verification")
                model_path.unlink()
                return False
                
        except Exception as e:
            logger.error(f"Failed to download {model_name}: {e}")
            if model_path.exists():
                model_path.unlink()
            return False
    
    def get_model_path(self, model_name: str) -> Optional[Path]:
        """
        Get path to model file, downloading if necessary
        
        Args:
            model_name: Name of the model
        
        Returns:
            Path to model file, or None if unavailable
        """
        if model_name not in self.MODELS:
            logger.error(f"Unknown model: {model_name}")
            return None
        
        model_info = self.MODELS[model_name]
        model_path = self.models_dir / model_info["filename"]
        
        # Verify or download
        if not self.verify_model(model_name):
            logger.info(f"Model {model_name} needs to be downloaded")
            if not self.download_model(model_name):
                return None
        
        return model_path


# Singleton instance
_model_store_instance: Optional[ModelStore] = None


def get_model_store() -> ModelStore:
    """Get singleton model store instance"""
    global _model_store_instance
    if _model_store_instance is None:
        _model_store_instance = ModelStore()
    return _model_store_instance
