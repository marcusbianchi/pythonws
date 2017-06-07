from functools import wraps
from jsonschema import validate
import sys
from flask import (
    current_app,
    jsonify,
    request,
)


def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            request.get_json()
        except:
            msg = "payload must be a valid json"
            return msg, 400
        return f(*args, **kw)
    return wrapper


def validate_schema(schema_name):
	def decorator(f):
		@wraps(f)
		def wrapper(*args, **kw):
			try:
				json = request.get_json()				
				validate(json, current_app.config[schema_name])
			except :
				e = sys.exc_info()[0]
				return str(e), 400
			return f(*args, **kw)
		return wrapper
	return decorator