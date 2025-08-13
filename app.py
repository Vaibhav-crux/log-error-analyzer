import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import logging
from logger import setup_logger

app = Flask(__name__, template_folder='frontend')

# Configuration
app.config['UPLOAD_FOLDER'] = 'Uploads'
app.config['ALLOWED_EXTENSIONS'] = {'log', 'txt'}

# Enable CORS for requests from Live Server (port 5500)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Setup logging
logger = setup_logger()

# Configure Gemini API
GEMINI_API_KEY = 'GEMINI_API_KEY'  # Your provided key
try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API configured successfully")
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_errors(log_content):
    """Extract ERROR lines from log content."""
    errors = []
    lines = log_content.splitlines()
    for line in lines:
        if 'ERROR' in line:
            error_start = line.find('ERROR') + 6
            error_message = line[error_start:].strip()
            errors.append(error_message)
    return errors

def analyze_error_with_gemini(error_message):
    """Send a single error to Gemini API and get JSON response."""
    prompt = """
Analyze the following error message and provide:
- error: The error message
- description: A brief explanation of why this error occurred
- resolve_technique: Steps to resolve the error

Return the result as a valid JSON object with keys "error", "description", and "resolve_technique". Ensure the response is strictly JSON, enclosed in ```json``` code fences.

Error message:
{error_message}
"""
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info(f"Sending error to Gemini API: {error_message[:100]}...")
        response = model.generate_content(prompt.format(error_message=error_message))
        logger.debug(f"Gemini API response (first 500 chars): {response.text[:500]}...")
        
        # Check if response is empty
        if not response.text or response.text.strip() == '':
            logger.error("Gemini API returned empty response")
            return None
        
        # Extract JSON from response
        json_start = response.text.find('```json') + 7
        json_end = response.text.rfind('```')
        if json_start == 6 or json_end == -1:
            logger.error("No valid JSON found in Gemini response")
            logger.debug(f"Raw response: {response.text}")
            return None
        
        json_str = response.text[json_start:json_end].strip()
        try:
            json_data = json.loads(json_str)
            logger.info("Successfully parsed Gemini API response for error")
            logger.debug(f"Parsed JSON: {json.dumps(json_data, indent=2)}")
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini API response as JSON: {str(e)}")
            logger.debug(f"Raw response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return None

@app.route('/')
def index():
    logger.info("Serving index page")
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    logger.info(f"Received upload request, method: {request.method}, headers: {dict(request.headers)}")
    
    if 'logfile' not in request.files:
        logger.error("No file part in request")
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['logfile']
    if file.filename == '':
        logger.error("No file selected")
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            logger.info(f"File saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save file {filename}: {str(e)}")
            return jsonify({'error': f'Failed to save file: {str(e)}'}), 500
        
        # Read log content
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                log_content = f.read()
            logger.info(f"Successfully read file: {filename}, size: {len(log_content)} chars")
        except Exception as e:
            logger.error(f"Failed to read file {filename}: {str(e)}")
            return jsonify({'error': f'Failed to read file: {str(e)}'}), 500
        
        # Extract errors
        errors = extract_errors(log_content)
        logger.info(f"Found {len(errors)} errors in log file")
        logger.debug(f"Extracted errors: {errors}")
        
        return jsonify({
            'message': 'Errors extracted, ready for processing',
            'errors': errors
        })
    
    logger.error(f"Invalid file type: {file.filename}")
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/process_errors', methods=['POST'])
def process_errors():
    logger.info(f"Received process_errors request, method: {request.method}, headers: {dict(request.headers)}")
    
    try:
        data = request.get_json()
        if not data or 'errors' not in data:
            logger.error("No errors provided in request")
            return jsonify({'error': 'No errors provided'}), 400
        
        error_results = []
        for error_message in data['errors']:
            result = analyze_error_with_gemini(error_message)
            if result:
                error_results.append(result)
            else:
                error_results.append({
                    'error': error_message,
                    'description': 'Failed to analyze error with Gemini API',
                    'resolve_technique': 'Check the Gemini API configuration or try again later.'
                })
        
        logger.info(f"Processed {len(error_results)} errors with Gemini API")
        logger.debug(f"Response JSON: {json.dumps({'errors': error_results}, indent=2)}")
        return jsonify({
            'message': 'Error analysis complete',
            'errors': error_results
        })
    except Exception as e:
        logger.error(f"Failed to process errors: {str(e)}")
        return jsonify({'error': f'Failed to process errors: {str(e)}'}), 500

if __name__ == '__main__':
    logger.info("Starting Flask application")
    app.run(debug=True)