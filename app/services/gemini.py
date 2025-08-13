import google.generativeai as genai
import json
from app.core.config import settings
from app.utils.logger import logger

def analyze_error_with_gemini(error_message: str):
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
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        logger.info(f"Sending error to Gemini API: {error_message[:100]}...")
        response = model.generate_content(prompt.format(error_message=error_message))
        logger.debug(f"Gemini API response (first 500 chars): {response.text[:500]}...")
        
        if not response.text or response.text.strip() == '':
            logger.error("Gemini API returned empty response")
            return None
        
        json_start = response.text.find('```json') + 7
        json_end = response.text.rfind('```')
        if json_start == 6 or json_end == -1:
            logger.error("No valid JSON found in Gemini response")
            logger.debug(f"Raw response: {response.text}")
            return None
        
        json_str = response.text[json_start:json_end].strip()
        try:
            json_data = json.loads(json_str)
            logger.info("Successfully parsed Gemini API response")
            logger.debug(f"Parsed JSON: {json.dumps(json_data, indent=2)}")
            return json_data
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini API response: {str(e)}")
            logger.debug(f"Raw response: {response.text}")
            return None
    except Exception as e:
        logger.error(f"Gemini API error: {str(e)}")
        return None