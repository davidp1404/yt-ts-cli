"""
Logging configuration for YouTube Transcript CLI.
"""

import logging
import sys


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels in non-silent mode."""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add color to the levelname
        if record.levelname in self.COLORS:
            record.levelname = f"{self.COLORS[record.levelname]}{record.levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


def setup_logging(silent: bool = False, verbose: bool = False, use_colors: bool = False) -> logging.Logger:
    """
    Setup logging configuration for the application.
    
    Args:
        silent: If True, suppress all logging output
        verbose: If True, enable debug level logging with timestamps
        use_colors: If True, use colored output (disabled by default for professional look)
    
    Returns:
        Configured logger instance
    """
    if silent:
        # In silent mode, completely disable all logging
        logging.disable(logging.CRITICAL)
        # Get our specific logger and configure it
        logger = logging.getLogger('yt_ts_cli')
        logger.handlers.clear()
        logger.setLevel(logging.CRITICAL + 1)
        logger.addHandler(logging.NullHandler())
        logger.propagate = False
        return logger
    
    # Re-enable logging if it was disabled
    logging.disable(logging.NOTSET)
    
    # Get the root logger and clear all handlers
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    
    # Get our specific logger
    logger = logging.getLogger('yt_ts_cli')
    logger.handlers.clear()
    
    # Configure logging level
    if verbose:
        level = logging.DEBUG
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    else:
        level = logging.INFO
        log_format = '%(levelname)s: %(message)s'
    
    # Create handler that outputs to stderr (so it doesn't interfere with stdout)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)
    
    # Choose formatter based on color preference
    if use_colors and sys.stderr.isatty():
        formatter = ColoredFormatter(log_format)
    else:
        formatter = logging.Formatter(log_format)
    
    handler.setFormatter(formatter)
    
    # Configure logger
    logger.setLevel(level)
    logger.addHandler(handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


class SuppressYtDlpLogger:
    """Custom logger that suppresses all yt-dlp output."""
    
    def debug(self, msg): 
        pass
    
    def info(self, msg): 
        pass
    
    def warning(self, msg): 
        pass
    
    def error(self, msg): 
        pass
    
    def critical(self, msg):
        pass
