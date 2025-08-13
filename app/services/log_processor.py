from app.utils.logger import logger

def extract_errors(log_content: str) -> list:
    errors = []
    lines = log_content.splitlines()
    for line in lines:
        if 'ERROR' in line:
            error_start = line.find('ERROR') + 6
            error_message = line[error_start:].strip()
            errors.append(error_message)
    return errors