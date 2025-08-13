from flask_cors import CORS
from app.core.config import settings

def add_cors_middleware(app):
    CORS(app, resources={r"/api/*": {"origins": settings.ALLOWED_ORIGINS}})