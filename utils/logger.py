"""
Centralized logging utility for Medical Cost Prediction API
"""

import logging
import os
from pathlib import Path
from typing import Optional
from core.config import LOG_CONFIG

def setup_logger(
    name: str = LOG_CONFIG['name'],
    log_level: str = LOG_CONFIG['level'],
    log_file: Optional[Path] = None
):
    """
    Set up and configure logger with both console and optional file handlers.

    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional path to log file. If None, only logs to console.

    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers = []

    # Log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

    # Console handler (always added)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler if log_file is provided
    if log_file:
        # Ensure log directory exists
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

# Default logger instance
logger = setup_logger(
    log_level=LOG_CONFIG['level'],
    log_file=LOG_CONFIG['log_file']
)