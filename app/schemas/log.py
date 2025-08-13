def validate_error_list(data):
    if not isinstance(data, dict) or 'errors' not in data:
        return None
    if not isinstance(data['errors'], list) or not all(isinstance(e, str) for e in data['errors']):
        return None
    return data['errors']