"""Background removal pipeline"""

from pathlib import Path
from typing import Optional, Tuple
import numpy as np
from PIL import Image
import os
import sys
from loguru import logger

# Workaround for numba/pymatting compatibility issues with Python 3.13+
# Disable alpha matting features if they fail to load
ALPHA_MATTING_AVAILABLE = False
try:
    from rembg import remove, new_session
    # Test if alpha matting is actually available by checking for pymatting
    try:
        import pymatting
        ALPHA_MATTING_AVAILABLE = True
    except ImportError:
        ALPHA_MATTING_AVAILABLE = False
        logger.warning("Alpha matting not available (pymatting not installed)")
except Exception as e:
    logger.error(f"Error loading rembg: {e}")
    raise

from bgremover.app.core.model_store import get_model_store
from bgremover.app.core.settings import OutputSettings, QualitySettings
from bgremover.app.core.image_ops import ImageOperations


class BackgroundRemovalPipeline:
    """Main pipeline for background removal"""
    
    def __init__(self, model_name: str = "u2net"):
        """
        Initialize pipeline
        
        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name
        self.session = None
        self.image_ops = ImageOperations()
        self._initialize_model()
    
    def _initialize_model(self) -> bool:
        """Initialize the ML model"""
        try:
            logger.info(f"Initializing model: {self.model_name}")
            
            # Get model path (download if needed)
            model_store = get_model_store()
            model_path = model_store.get_model_path(self.model_name)
            
            if model_path is None:
                logger.error("Failed to get model path")
                return False
            
            # Create rembg session
            self.session = new_session(self.model_name)
            logger.success(f"Model {self.model_name} initialized successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize model: {e}")
            return False
    
    def process_image(
        self,
        input_path: Path,
        output_path: Path,
        output_settings: OutputSettings,
        quality_settings: QualitySettings
    ) -> bool:
        """
        Process a single image
        
        Args:
            input_path: Path to input image
            output_path: Path to save output
            output_settings: Output configuration
            quality_settings: Quality configuration
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Processing: {input_path.name}")
            
            # Load image
            input_image = Image.open(input_path)
            
            # Convert to RGB if needed
            if input_image.mode not in ("RGB", "RGBA"):
                input_image = input_image.convert("RGB")
            
            # Remove background
            # Only use alpha matting if available and enabled
            use_alpha_matting = ALPHA_MATTING_AVAILABLE and quality_settings.alpha_matting
            
            try:
                if use_alpha_matting:
                    output_image = remove(
                        input_image,
                        session=self.session,
                        alpha_matting=True,
                        alpha_matting_foreground_threshold=quality_settings.alpha_matting_foreground_threshold,
                        alpha_matting_background_threshold=quality_settings.alpha_matting_background_threshold,
                    )
                else:
                    output_image = remove(
                        input_image,
                        session=self.session,
                    )
            except Exception as e:
                # Fallback: if alpha matting fails, try without it
                if "alpha matting" in str(e).lower() or "pymatting" in str(e).lower():
                    logger.warning(f"Alpha matting not available, using basic removal: {e}")
                    output_image = remove(
                        input_image,
                        session=self.session,
                    )
                else:
                    raise
            
            # Ensure RGBA
            if output_image.mode != "RGBA":
                output_image = output_image.convert("RGBA")
            
            # Apply mask refinement
            if quality_settings.remove_small_objects or quality_settings.smooth_edges:
                output_image = self._refine_mask(output_image, quality_settings)
            
            # Apply feathering
            if output_settings.feather_edges > 0:
                alpha = output_image.split()[-1]
                output_image = self.image_ops.apply_feather(
                    output_image,
                    alpha,
                    output_settings.feather_edges
                )
            
            # Apply background
            output_image = self._apply_background(output_image, output_settings)
            
            # Resize and position if needed
            if output_settings.canvas_width and output_settings.canvas_height:
                target_size = (output_settings.canvas_width, output_settings.canvas_height)
                
                # Get background color for padding
                if output_settings.background_type == "transparent":
                    bg_color = (255, 255, 255, 0)
                elif output_settings.background_type == "color":
                    hex_color = output_settings.background_color.lstrip("#")
                    r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
                    bg_color = (r, g, b, 255)
                else:
                    bg_color = (255, 255, 255, 255)
                
                output_image = self.image_ops.resize_with_padding(
                    output_image,
                    target_size,
                    center=output_settings.center_object,
                    margin=output_settings.margin,
                    bg_color=bg_color
                )
            
            # Save output
            self._save_image(output_image, output_path, output_settings)
            
            logger.success(f"Saved: {output_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to process {input_path.name}: {e}")
            return False
    
    def _refine_mask(
        self,
        image: Image.Image,
        quality_settings: QualitySettings
    ) -> Image.Image:
        """Refine the alpha mask"""
        # Extract alpha channel
        alpha = np.array(image.split()[-1])
        
        # Apply morphological refinement
        alpha_refined = self.image_ops.refine_mask_morphology(
            alpha,
            remove_small_objects=quality_settings.remove_small_objects,
            min_object_size=quality_settings.min_object_size,
            smooth_edges=quality_settings.smooth_edges,
            kernel_size=quality_settings.edge_smooth_kernel
        )
        
        # Replace alpha channel
        result = image.copy()
        result.putalpha(Image.fromarray(alpha_refined))
        
        return result
    
    def _apply_background(
        self,
        image: Image.Image,
        output_settings: OutputSettings
    ) -> Image.Image:
        """Apply background based on settings"""
        if output_settings.background_type == "transparent":
            # Keep transparent
            return image
        
        elif output_settings.background_type == "color":
            # Solid color background
            hex_color = output_settings.background_color.lstrip("#")
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return self.image_ops.apply_solid_background(image, (r, g, b))
        
        elif output_settings.background_type == "image" and output_settings.background_image:
            # Image background
            try:
                bg_image = Image.open(output_settings.background_image)
                return self.image_ops.apply_image_background(image, bg_image, resize_bg=True)
            except Exception as e:
                logger.error(f"Failed to load background image: {e}")
                return image
        
        return image
    
    def _save_image(
        self,
        image: Image.Image,
        output_path: Path,
        output_settings: OutputSettings
    ) -> None:
        """Save image with proper format and quality"""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if output_settings.format == "png":
            image.save(output_path, "PNG", optimize=True)
        
        elif output_settings.format == "webp":
            image.save(
                output_path,
                "WEBP",
                quality=output_settings.quality,
                method=6
            )
        
        elif output_settings.format == "jpg":
            # Convert to RGB for JPEG
            if image.mode == "RGBA":
                # Apply white background for JPEG
                bg = Image.new("RGB", image.size, (255, 255, 255))
                bg.paste(image, (0, 0), image)
                image = bg
            
            image.save(
                output_path,
                "JPEG",
                quality=output_settings.quality,
                optimize=True
            )


# Singleton instance
_pipeline_instance: Optional[BackgroundRemovalPipeline] = None


def get_pipeline() -> BackgroundRemovalPipeline:
    """Get singleton pipeline instance"""
    global _pipeline_instance
    if _pipeline_instance is None:
        _pipeline_instance = BackgroundRemovalPipeline()
    return _pipeline_instance
