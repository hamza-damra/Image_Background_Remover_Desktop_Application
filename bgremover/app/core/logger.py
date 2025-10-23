"""Logger configuration using loguru"""

import sys
from pathlib import Path
from loguru import logger


def setup_logger(log_level: str = "INFO") -> logger:
    """
    Setup application logger
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        Configured logger instance
    """
    # Remove default handler
    logger.remove()
    
    # Add console handler with colors
    if sys.stderr:
        logger.add(
            sys.stderr,
            format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            level=log_level,
            colorize=True,
        )
    
    # Add file handler for persistent logs
    log_dir = Path.home() / ".bgremover" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        log_dir / "bgremover_{time:YYYY-MM-DD}.log",
        rotation="1 day",
        retention="7 days",
        compression="zip",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=log_level,
    )
    
    return logger


# Export configured logger
__all__ = ["setup_logger", "logger"]
