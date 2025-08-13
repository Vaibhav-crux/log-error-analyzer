from flask_compress import Compress

def add_gzip_middleware(app):
    Compress(app)