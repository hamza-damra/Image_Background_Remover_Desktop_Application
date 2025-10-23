"""Image processing operations"""

from typing import Tuple, Optional
import numpy as np
from PIL import Image, ImageFilter, ImageOps
import cv2
from loguru import logger


class ImageOperations:
    """Image processing utilities"""
    
    @staticmethod
    def apply_feather(image: Image.Image, mask: Image.Image, feather_amount: int) -> Image.Image:
        """
        Apply feathering (soft edges) to mask
        
        Args:
            image: Source image
            mask: Alpha mask
            feather_amount: Feather radius in pixels
        
        Returns:
            Image with feathered edges
        """
        if feather_amount <= 0:
            return image
        
        # Apply Gaussian blur to mask
        mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=feather_amount))
        
        # Apply mask to image
        result = Image.new("RGBA", image.size)
        result.paste(image, (0, 0))
        result.putalpha(mask_blurred)
        
        return result
    
    @staticmethod
    def resize_with_padding(
        image: Image.Image,
        target_size: Tuple[int, int],
        center: bool = True,
        margin: int = 0,
        bg_color: Tuple[int, int, int, int] = (255, 255, 255, 0)
    ) -> Image.Image:
        """
        Resize image to fit target size with padding/margin
        
        Args:
            image: Source image
            target_size: (width, height) target size
            center: Center the image in canvas
            margin: Margin from edges in pixels
            bg_color: Background color (R, G, B, A)
        
        Returns:
            Resized and padded image
        """
        target_width, target_height = target_size
        
        # Apply margin
        if margin > 0:
            target_width -= margin * 2
            target_height -= margin * 2
        
        # Calculate scaling to fit
        image.thumbnail((target_width, target_height), Image.Resampling.LANCZOS)
        
        # Create canvas
        canvas = Image.new("RGBA", (target_width + margin * 2, target_height + margin * 2), bg_color)
        
        # Calculate position
        if center:
            x = (canvas.width - image.width) // 2
            y = (canvas.height - image.height) // 2
        else:
            x = margin
            y = margin
        
        # Paste image onto canvas
        canvas.paste(image, (x, y), image if image.mode == "RGBA" else None)
        
        return canvas
    
    @staticmethod
    def apply_solid_background(
        image: Image.Image,
        bg_color: Tuple[int, int, int]
    ) -> Image.Image:
        """
        Replace transparent background with solid color
        
        Args:
            image: Source image with alpha channel
            bg_color: Background color (R, G, B)
        
        Returns:
            Image with solid background
        """
        if image.mode != "RGBA":
            return image
        
        # Create background
        background = Image.new("RGB", image.size, bg_color)
        background.paste(image, (0, 0), image)
        
        return background
    
    @staticmethod
    def apply_image_background(
        foreground: Image.Image,
        background: Image.Image,
        resize_bg: bool = True
    ) -> Image.Image:
        """
        Replace transparent background with another image
        
        Args:
            foreground: Source image with alpha channel
            background: Background image
            resize_bg: Resize background to match foreground
        
        Returns:
            Composited image
        """
        if foreground.mode != "RGBA":
            foreground = foreground.convert("RGBA")
        
        # Resize background if needed
        if resize_bg and background.size != foreground.size:
            background = background.resize(foreground.size, Image.Resampling.LANCZOS)
        
        # Convert background to RGBA
        if background.mode != "RGBA":
            background = background.convert("RGBA")
        
        # Composite
        result = Image.alpha_composite(background, foreground)
        
        return result
    
    @staticmethod
    def refine_mask_morphology(
        mask: np.ndarray,
        remove_small_objects: bool = True,
        min_object_size: int = 100,
        smooth_edges: bool = True,
        kernel_size: int = 5
    ) -> np.ndarray:
        """
        Refine mask using morphological operations
        
        Args:
            mask: Binary mask (0-255)
            remove_small_objects: Remove small isolated regions
            min_object_size: Minimum object size to keep
            smooth_edges: Apply morphological smoothing
            kernel_size: Kernel size for smoothing
        
        Returns:
            Refined mask
        """
        mask_refined = mask.copy()
        
        # Remove small objects
        if remove_small_objects:
            # Find contours
            contours, _ = cv2.findContours(
                mask_refined,
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )
            
            # Filter by size
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < min_object_size:
                    cv2.drawContours(mask_refined, [contour], -1, 0, -1)
        
        # Smooth edges
        if smooth_edges and kernel_size > 0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
            # Opening (remove noise)
            mask_refined = cv2.morphologyEx(mask_refined, cv2.MORPH_OPEN, kernel)
            # Closing (fill gaps)
            mask_refined = cv2.morphologyEx(mask_refined, cv2.MORPH_CLOSE, kernel)
        
        return mask_refined
    
    @staticmethod
    def refine_mask_bilateral(
        mask: np.ndarray,
        diameter: int = 9,
        sigma_color: int = 75,
        sigma_space: int = 75
    ) -> np.ndarray:
        """
        Refine mask using bilateral filter (edge-preserving smoothing)
        
        Args:
            mask: Binary mask (0-255)
            diameter: Diameter of pixel neighborhood
            sigma_color: Filter sigma in color space
            sigma_space: Filter sigma in coordinate space
        
        Returns:
            Refined mask
        """
        return cv2.bilateralFilter(mask, diameter, sigma_color, sigma_space)
    
    @staticmethod
    def auto_crop_transparent(image: Image.Image, margin: int = 0) -> Image.Image:
        """
        Auto-crop image to content bounding box
        
        Args:
            image: Source image with alpha channel
            margin: Additional margin around content
        
        Returns:
            Cropped image
        """
        if image.mode != "RGBA":
            return image
        
        # Get alpha channel
        alpha = image.split()[-1]
        
        # Get bounding box
        bbox = alpha.getbbox()
        
        if bbox is None:
            return image
        
        # Apply margin
        if margin > 0:
            bbox = (
                max(0, bbox[0] - margin),
                max(0, bbox[1] - margin),
                min(image.width, bbox[2] + margin),
                min(image.height, bbox[3] + margin)
            )
        
        return image.crop(bbox)
    
    @staticmethod
    def create_gradient_background(
        size: Tuple[int, int],
        color1: Tuple[int, int, int],
        color2: Tuple[int, int, int],
        direction: str = "vertical"
    ) -> Image.Image:
        """
        Create gradient background
        
        Args:
            size: (width, height)
            color1: Start color (R, G, B)
            color2: End color (R, G, B)
            direction: "vertical", "horizontal", "diagonal"
        
        Returns:
            Gradient image
        """
        width, height = size
        
        if direction == "vertical":
            gradient = np.linspace(0, 1, height).reshape(-1, 1)
            gradient = np.repeat(gradient, width, axis=1)
        elif direction == "horizontal":
            gradient = np.linspace(0, 1, width).reshape(1, -1)
            gradient = np.repeat(gradient, height, axis=0)
        else:  # diagonal
            x = np.linspace(0, 1, width)
            y = np.linspace(0, 1, height)
            gradient = (x + y.reshape(-1, 1)) / 2
        
        # Create RGB image
        r = (color1[0] * (1 - gradient) + color2[0] * gradient).astype(np.uint8)
        g = (color1[1] * (1 - gradient) + color2[1] * gradient).astype(np.uint8)
        b = (color1[2] * (1 - gradient) + color2[2] * gradient).astype(np.uint8)
        
        rgb = np.stack([r, g, b], axis=2)
        
        return Image.fromarray(rgb, mode="RGB")
