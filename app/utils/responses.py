def success_response(data=None, message=None, status_code=200):
    response = {"status": "success"}
    if message:
        response["message"] = message
    if data is not None:
        response["data"] = data
    return response, status_code

def error_response(message, status_code=400, errors=None):
    response = {"status": "error", "message": message}
    if errors:
        response["errors"] = errors
    return response, status_code
