from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def add_rate_limiter_middleware(app):
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    return limiter