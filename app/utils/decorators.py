from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

def protected(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return fn(*args, **kwargs)
    return wrapper
