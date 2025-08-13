import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger():
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logger
    logger = logging.getLogger('LogAnalyzer')
    logger.setLevel(logging.DEBUG)  # Capture all levels of logs
    
    # Create rotating file handler (max 5MB, keep 3 backups)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=5_000_000,  # 5MB
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    
    # Create console handler for real-time output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Show INFO and above in console
    
    # Define log format
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger