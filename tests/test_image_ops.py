"""Test image operations"""

import pytest
from PIL import Image
import numpy as np

from bgremover.app.core.image_ops import ImageOperations


@pytest.fixture
def test_image():
    """Create a test image"""
    return Image.new('RGBA', (100, 100), color=(255, 0, 0, 255))


@pytest.fixture
def test_mask():
    """Create a test mask"""
    return Image.new('L', (100, 100), color=255)


def test_apply_feather(test_image, test_mask):
    """Test feathering"""
    ops = ImageOperations()
    result = ops.apply_feather(test_image, test_mask, feather_amount=5)
    
    assert result is not None
    assert result.mode == "RGBA"
    assert result.size == test_image.size


def test_resize_with_padding(test_image):
    """Test resize with padding"""
    ops = ImageOperations()
    result = ops.resize_with_padding(
        test_image,
        target_size=(200, 200),
        center=True,
        margin=10
    )
    
    assert result is not None
    assert result.size == (200, 200)


def test_apply_solid_background(test_image):
    """Test solid background"""
    ops = ImageOperations()
    result = ops.apply_solid_background(test_image, (255, 255, 255))
    
    assert result is not None
    assert result.mode == "RGB"
    assert result.size == test_image.size


def test_apply_image_background(test_image):
    """Test image background"""
    ops = ImageOperations()
    bg_image = Image.new('RGB', (100, 100), color=(0, 0, 255))
    
    result = ops.apply_image_background(test_image, bg_image, resize_bg=True)
    
    assert result is not None
    assert result.mode == "RGBA"
    assert result.size == test_image.size


def test_refine_mask_morphology():
    """Test mask refinement"""
    ops = ImageOperations()
    
    # Create a simple mask
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[40:60, 40:60] = 255
    
    result = ops.refine_mask_morphology(
        mask,
        remove_small_objects=True,
        min_object_size=10,
        smooth_edges=True,
        kernel_size=3
    )
    
    assert result is not None
    assert result.shape == mask.shape


def test_auto_crop_transparent(test_image):
    """Test auto crop"""
    ops = ImageOperations()
    
    # Create image with transparent borders
    img = Image.new('RGBA', (200, 200), color=(0, 0, 0, 0))
    img.paste(test_image, (50, 50))
    
    result = ops.auto_crop_transparent(img, margin=5)
    
    assert result is not None
    # Should be smaller than original
    assert result.width <= img.width
    assert result.height <= img.height


def test_create_gradient_background():
    """Test gradient background"""
    ops = ImageOperations()
    
    result = ops.create_gradient_background(
        size=(200, 200),
        color1=(255, 0, 0),
        color2=(0, 0, 255),
        direction="vertical"
    )
    
    assert result is not None
    assert result.mode == "RGB"
    assert result.size == (200, 200)
