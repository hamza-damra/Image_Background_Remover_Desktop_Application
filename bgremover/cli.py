"""Command Line Interface for batch processing"""

import argparse
import sys
from pathlib import Path
from typing import List
from loguru import logger

from bgremover.app.core.pipeline import get_pipeline
from bgremover.app.core.settings import OutputSettings, QualitySettings
from bgremover.app.core.presets import get_preset_manager
from bgremover.app.core.logger import setup_logger


def find_images(input_path: Path) -> List[Path]:
    """
    Find all images in a directory
    
    Args:
        input_path: Directory path
    
    Returns:
        List of image paths
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp']
    images = []
    
    if input_path.is_file():
        if input_path.suffix.lower() in image_extensions:
            images.append(input_path)
    elif input_path.is_dir():
        for ext in image_extensions:
            images.extend(input_path.glob(f'*{ext}'))
            images.extend(input_path.glob(f'*{ext.upper()}'))
    
    return sorted(images)


def process_images(
    input_paths: List[Path],
    output_dir: Path,
    output_settings: OutputSettings,
    quality_settings: QualitySettings,
    suffix: str = "_nobg"
) -> tuple:
    """
    Process multiple images
    
    Args:
        input_paths: List of input image paths
        output_dir: Output directory
        output_settings: Output configuration
        quality_settings: Quality configuration
        suffix: Filename suffix
    
    Returns:
        Tuple of (successful_count, failed_count)
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    pipeline = get_pipeline()
    
    successful = 0
    failed = 0
    
    total = len(input_paths)
    
    for i, input_path in enumerate(input_paths, 1):
        logger.info(f"Processing {i}/{total}: {input_path.name}")
        
        # Create output filename
        output_filename = f"{input_path.stem}{suffix}.{output_settings.format}"
        output_path = output_dir / output_filename
        
        try:
            success = pipeline.process_image(
                input_path,
                output_path,
                output_settings,
                quality_settings
            )
            
            if success:
                successful += 1
                logger.success(f"✓ Saved: {output_path.name}")
            else:
                failed += 1
                logger.error(f"✗ Failed: {input_path.name}")
        
        except Exception as e:
            failed += 1
            logger.error(f"✗ Error processing {input_path.name}: {e}")
    
    return successful, failed


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Background Remover - CLI for batch processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Process all images in a directory
  python -m bgremover.cli --input ./photos --output ./output
  
  # Use a preset
  python -m bgremover.cli --input ./photos --output ./output --preset marketplace
  
  # Custom background color
  python -m bgremover.cli --input ./photos --output ./output --bg-color "#FF0000"
  
  # Custom canvas size
  python -m bgremover.cli --input ./photos --output ./output --size 1600x1600
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help='Input directory or file'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help='Output directory'
    )
    
    # Optional arguments
    parser.add_argument(
        '--preset', '-p',
        type=str,
        help='Preset name (transparent, marketplace, white_bg, etc.)'
    )
    
    parser.add_argument(
        '--format', '-f',
        type=str,
        choices=['png', 'webp', 'jpg'],
        default='png',
        help='Output format (default: png)'
    )
    
    parser.add_argument(
        '--quality', '-q',
        type=int,
        default=95,
        help='Output quality 1-100 (default: 95)'
    )
    
    parser.add_argument(
        '--bg-color',
        type=str,
        help='Background color in hex (e.g., #FFFFFF)'
    )
    
    parser.add_argument(
        '--bg-image',
        type=str,
        help='Background image path'
    )
    
    parser.add_argument(
        '--size',
        type=str,
        help='Canvas size in format WIDTHxHEIGHT (e.g., 1600x1600)'
    )
    
    parser.add_argument(
        '--margin',
        type=int,
        default=0,
        help='Margin in pixels (default: 0)'
    )
    
    parser.add_argument(
        '--suffix',
        type=str,
        default='_nobg',
        help='Output filename suffix (default: _nobg)'
    )
    
    parser.add_argument(
        '--alpha-matting',
        action='store_true',
        help='Enable alpha matting for better quality (slower)'
    )
    
    parser.add_argument(
        '--lang',
        type=str,
        choices=['en', 'ar'],
        default='en',
        help='Language for messages (default: en)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    
    args = parser.parse_args()
    
    # Setup logger
    log_level = "DEBUG" if args.debug else "INFO"
    setup_logger(log_level)
    
    # Validate paths
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)
    
    output_dir = Path(args.output)
    
    # Find images
    logger.info(f"Searching for images in: {input_path}")
    images = find_images(input_path)
    
    if not images:
        logger.error("No images found")
        sys.exit(1)
    
    logger.info(f"Found {len(images)} images")
    
    # Configure settings
    if args.preset:
        # Load preset
        preset_manager = get_preset_manager()
        preset = preset_manager.get_preset(args.preset)
        
        if preset is None:
            logger.error(f"Preset not found: {args.preset}")
            logger.info("Available presets:")
            for p in preset_manager.list_presets():
                logger.info(f"  - {p['id']}: {p['name']}")
            sys.exit(1)
        
        logger.info(f"Using preset: {preset.name}")
        
        # Create settings from preset
        output_settings = OutputSettings(
            format=preset.format,
            quality=preset.quality,
            background_type=preset.background_type,
            background_color=preset.background_color,
            canvas_width=preset.canvas_width,
            canvas_height=preset.canvas_height,
            center_object=preset.center_object,
            margin=preset.margin,
            feather_edges=preset.feather_edges
        )
        
        quality_settings = QualitySettings(
            alpha_matting=preset.alpha_matting,
            remove_small_objects=preset.remove_small_objects,
            min_object_size=preset.min_object_size,
            smooth_edges=preset.smooth_edges,
            edge_smooth_kernel=preset.edge_smooth_kernel
        )
    else:
        # Create settings from arguments
        background_type = "transparent"
        if args.bg_color:
            background_type = "color"
        elif args.bg_image:
            background_type = "image"
        
        canvas_width = None
        canvas_height = None
        if args.size:
            try:
                width, height = args.size.lower().split('x')
                canvas_width = int(width)
                canvas_height = int(height)
            except ValueError:
                logger.error(f"Invalid size format: {args.size}. Use WIDTHxHEIGHT")
                sys.exit(1)
        
        output_settings = OutputSettings(
            format=args.format,
            quality=args.quality,
            background_type=background_type,
            background_color=args.bg_color or "#FFFFFF",
            background_image=args.bg_image,
            canvas_width=canvas_width,
            canvas_height=canvas_height,
            center_object=True,
            margin=args.margin
        )
        
        quality_settings = QualitySettings(
            alpha_matting=args.alpha_matting
        )
    
    # Process images
    logger.info("Starting batch processing...")
    successful, failed = process_images(
        images,
        output_dir,
        output_settings,
        quality_settings,
        args.suffix
    )
    
    # Summary
    logger.info("=" * 50)
    logger.success(f"✓ Completed: {successful}/{len(images)} images")
    if failed > 0:
        logger.error(f"✗ Failed: {failed}/{len(images)} images")
    logger.info(f"Output directory: {output_dir}")
    logger.info("=" * 50)
    
    # Exit code
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
