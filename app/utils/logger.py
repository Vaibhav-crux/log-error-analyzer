import logging
from logging.handlers import RotatingFileHandler
from app.core.config import settings
import os

def setup_logger():
    os.makedirs(settings.LOG_DIR, exist_ok=True)
    logger = logging.getLogger('LogErrorAnalyzer')
    logger.setLevel(logging.DEBUG)
    
    file_handler = RotatingFileHandler(
        os.path.join(settings.LOG_DIR, 'app.log'),
        maxBytes=5_000_000,
        backupCount=3
    )
    file_handler.setLevel(logging.DEBUG)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    log_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()