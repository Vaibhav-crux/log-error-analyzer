from flask import jsonify
from app.utils.logger import logger

def add_error_handler_middleware(app):
    @app.errorhandler(400)
    def bad_request(e):
        logger.error(f"Bad request: {str(e)}")
        return jsonify({"message": str(e.description)}), 400

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500