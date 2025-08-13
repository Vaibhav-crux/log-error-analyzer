from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.schemas.log import validate_error_list
from app.services.log_processor import extract_errors
from app.services.gemini import analyze_error_with_gemini
from app.utils.logger import logger
from app.core.config import settings
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

log_bp = Blueprint("log", __name__)
limiter = Limiter(key_func=get_remote_address)

@log_bp.route("/upload", methods=["POST"])
@limiter.limit("5/minute")
def upload_file():
    if 'logfile' not in request.files:
        logger.error("No file part in request")
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['logfile']
    if file.filename == '':
        logger.error("No file selected")
        return jsonify({"message": "No selected file"}), 400
    
    if not file.filename.lower().endswith((".log", ".txt")):
        logger.error(f"Invalid file type: {file.filename}")
        return jsonify({"message": "Invalid file type"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(settings.UPLOAD_DIR, filename)
    
    try:
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file.save(filepath)
        logger.info(f"File saved: {filepath}")
    except Exception as e:
        logger.error(f"Failed to save file {filename}: {str(e)}")
        return jsonify({"message": f"Failed to save file: {str(e)}"}), 500
    
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            log_content = f.read()
        logger.info(f"Successfully read file: {filename}, size: {len(log_content)} chars")
    except Exception as e:
        logger.error(f"Failed to read file {filename}: {str(e)}")
        return jsonify({"message": f"Failed to read file: {str(e)}"}), 500
    
    errors = extract_errors(log_content)
    logger.info(f"Found {len(errors)} errors in log file")
    logger.debug(f"Extracted errors: {errors}")
    
    return jsonify({
        "message": "Errors extracted, ready for processing",
        "errors": errors
    })

@log_bp.route("/process_errors", methods=["POST"])
@limiter.limit("10/minute")
def process_errors():
    try:
        data = request.get_json()
        if not data or 'errors' not in data:
            logger.error("No errors provided in request")
            return jsonify({"message": "No errors provided"}), 400
        
        errors = validate_error_list(data)
        if not errors:
            logger.error("Invalid error list format")
            return jsonify({"message": "Invalid error list format"}), 400
        
        error_results = []
        for error_message in errors:
            result = analyze_error_with_gemini(error_message)
            if result:
                error_results.append(result)
            else:
                error_results.append({
                    "error": error_message,
                    "description": "Failed to analyze error with Gemini API",
                    "resolve_technique": "Check the Gemini API configuration or try again later."
                })
        
        logger.info(f"Processed {len(error_results)} errors with Gemini API")
        logger.debug(f"Response: {error_results}")
        return jsonify({
            "message": "Error analysis complete",
            "errors": error_results
        })
    except Exception as e:
        logger.error(f"Failed to process errors: {str(e)}")
        return jsonify({"message": f"Failed to process errors: {str(e)}"}), 500