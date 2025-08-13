from flask import request
from app.utils.logger import logger
import time

def add_logging_middleware(app):
    @app.before_request
    def log_request():
        app.start_time = time.time()

    @app.after_request
    def log_response(response):
        duration = time.time() - app.start_time
        logger.info(
            f"Request: {request.method} {request.url} - "
            f"Status: {response.status_code} - Duration: {duration:.2f}s"
        )
        return response