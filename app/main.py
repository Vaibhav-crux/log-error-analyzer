from flask import Flask
from app.middleware.cors import add_cors_middleware
from app.middleware.error_handler import add_error_handler_middleware
from app.middleware.gzip import add_gzip_middleware
from app.middleware.logging import add_logging_middleware
from app.middleware.rate_limiter import add_rate_limiter_middleware
from app.routes.log import log_bp
from app.utils.logger import logger

app = Flask(__name__, static_folder="../frontend", static_url_path="/frontend")

# Apply middleware
add_cors_middleware(app)
add_error_handler_middleware(app)
add_gzip_middleware(app)
add_logging_middleware(app)
add_rate_limiter_middleware(app)

# Register blueprints
app.register_blueprint(log_bp, url_prefix="/api")

if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(host="127.0.0.1", port=5000, debug=True)